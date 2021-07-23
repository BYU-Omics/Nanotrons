"""
COORDINATOR CLASS 
    This is the class that serves as an interface between the server (web_app.py) and the motor system comprised of all of the other classes that 
    regulate in one way or another the operation of the OT2 motors.
    There are 6 main blocks of code that implement the basic functionalities of the motor system:

    I. Manual Control
        This section takes care of opening a separate thread that "listens" to the inputs the user provides through the joystick, while the main thread
        executes in an infinite loop any methods associated to the inputs received on the joystick. The infinite loop running on the main thread stops 
        when the "listening" of the joystick is terminated, which can happen whenever the stop_listen() method is called within the joystick or by
        calling the stop_manual_control() method from within Coordinator (found in this section).

    II. Instantaneous Commands
        This section provides the ability to move the motors to any location recognized either as a well or pot in the system. There is a common method 
        called by both procedures called go_to_position() which only receives an x, y, z coordinate as input and goes there with the motors. Therefore,
        the other methods just take care of obtaining the x,y,z coordinate for the specified well or pot and then call the go_to_position() method with
        that coordinate as the parameter.

    III. PROTOCOL METHODS SECTION
        This section specifies methods needed to execute a scripted set of instructions recorded on an external file.

    IV. Labware
        This section defines a variety of methods that have to do with the creation, calibration, deletion, diretories, and models available for labware. 
        It also contains a method that allows for selecting a syringe model.

    V. Settings
        This section contains two main methods: get_current_settings() and update_setting(). The first returns a dictionary with all the relevant 
        settings of the system and the second updates a specific setting provided a setting name and the new value for it.There is also the 
        get_linked_joystick_axis_index() method which is a supporting function for the operation of both methods described above. It serves the purpose 
        of returning the joystick axis number linked to each coordinate axis in the motor system.

    VI. Feedback
        This section provides current values for dynamic variables and states such as the current X,Y,Z coordinate of the motors, and current gear, and 
        also adjusts values for variables that regulate the feedback sent to the user (like how fast the coordinates are refreshed on the web page).
"""

from OTdriver import OT2_nanopots_driver, SLOW_SPEED
from TDdriver import TempDeck
from TCdriver import Thermocycler
from joystick import XboxJoystick
from joystick_profile import *
from labware_class import *
from models_manager import ModelsManager
from calibration import *
from deck import *
import asyncio
# from high_level_script_reader import HighLevelScriptReader	
import threading
import math	
import time
import logging
import os
import sys
from collections import deque 
import constants

DISTANCE = 10 #mm
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
UNIT_CONVERSION  = 4.23 #3.8896 4.16
INBETWEEN_LIFT_DISTANCE = -10 # Default distance the syringe will be lifted/lowered when going from one nanopots well\reagent pot to another
LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LABWARE_SYRINGE = "s"
DEFAULT_PROFILE = "default_profile.json"
FROM_NANOLITERS = 0.001
REFRESH_COORDINATE_INTERVAL = 0.1
ASPIRATE_SPEED = SLOW_SPEED
POSITION_IN_Z_TO_PLACE_WHEN_GOING_TO_SLOT = 150
TIME_TO_SETTLE = 0.5 #SECONDS

def interrupt_callback(res):
    sys.stderr.write(res)

class Coordinator:
    def __init__(self):
        """ Initialize the class and instanciate all the subordinate classes

        Args:method_name
            joystick_profile ([json file name]): specify a file with the mapping between joystick elements and methods triggered when those elements are pressed by user
        """
        operating_system = ""
        os_recognized = os.name
        if os_recognized == WINDOWS_OS:
            logging.info("Operating system: Windows")
            operating_system = "w"
        elif os_recognized == LINUX_OS:
            logging.info("Operating system: Linux")
            operating_system = "r"
        self.myLabware = Labware_class("HAMILTON_175")
        self.joystick_profile = DEFAULT_PROFILE
        self.ot_control = OT2_nanopots_driver()
        self.tc_control = Thermocycler(interrupt_callback=interrupt_callback)
        self.td_control = TempDeck()
        self.myController = XboxJoystick(operating_system)
        self.myProfile = Profile(self.joystick_profile)
        self.myModelsManager = ModelsManager(operating_system)
        self.coordinates_refresh_rate = REFRESH_COORDINATE_INTERVAL
        self.deck = Deck()
        self.user_input = 0
        
        # initialize the logging info format
        format = "%(asctime)s: %(message)s" #format logging
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")

    """
    MANUAL CONTROL SECTION
        The only method that should be called on an instance of the Application class is manual_control(). The
        rest of the methods are supporting functions for the operation of manual_control()
    """
    def monitor_joystick(self):
        """ This method reads the values being collected from triggered inputs in the joystick and executes the methods associated with them
        """
        axes = self.myController.deliver_axes() # Dictionary with the axes index and value that are being pressed
        buttons = self.myController.deliver_buttons() # List with strings according to the buttons currently being pressed
        hats = self.myController.deliver_hats() # List with strings according to the buttons currently being pressed
        
        for axis_index in range(len(self.myController.axes[:5])): # 5 is to reject the last index in the list in case there is one (for Unix OS)
            if axis_index == 2:
                if self.myController.axes[2] > 0:
                    print("ASPIRATE")
                    self.aspirate(self.user_input, SLOW_SPEED)
                elif self.myController.axes[2] < 0:
                    print("DISPENSE")
                    self.dispense(self.user_input, SLOW_SPEED)
                else:
                    pass
            method_name = self.myProfile.get_axis_function(axis_index).__name__            
            method = getattr(self.ot_control, method_name, False)
            method(self.myController.axes[axis_index])

        if (len(buttons) != 0):
            for button in buttons:
                if button == "START":
                    self.user_input = input("Enter volume to aspirate in nanoliters: ")
                method_name = self.myProfile.get_button_function(button).__name__
                method = getattr(self.ot_control, method_name, False)
                if not method:
                    method = getattr(self.myController, method_name, False)
                method(self.myController.get_button_by_name(button))

        if (len(hats) != 0):
            for hat in hats:
                method_name = self.myProfile.get_hat_function(hat).__name__
                method = getattr(self.ot_control, method_name, False)
                method(self.myController.get_hats()[self.myController.get_hats_dict_index(hat)])

    def manual_control(self):
        """ This method opens a secondary thread to listen to the input of the joystick (have a real time update of the triggered inputs) and calls monitor_joystick on the main thread on a loop
        """
        t1 = threading.Thread(target=self.myController.listen)
        t1.start()
        while(t1.is_alive()):
            self.monitor_joystick()
            time.sleep(0.2) # Debounce method, so that it allows for the user to loose the button 

    def stop_manual_control(self):
        """ This method turns off the flag that enables listening to the joystick, which triggers killing manual control given that the loop depends on that flag
        """
        self.myController.stop_listening("") # It as a "" as an argument because it askes for a dummy argument for the method(self.myController.get_hats()[self.myController.get_hats_dict_index(hat)])

    def home_all_motors(self):
        """ This method homes all the motors on the OT2 except for the Syringes
        """
        self.ot_control.home("X Y Z A") # Not B and C

    def up_step_size(self):
        """ This method goes through a list of predefined steps 
        """
        self.ot_control.double_step_size_XYZ("") # "" is the dummy argument
    
    def down_step_size(self):
        """ This method goes through a list of predefined steps  """
       
        self.ot_control.half_step_size_XYZ("") # "" is the dummy argument
    
    """
    INSTANTANEOUS COMMANDS SECTION
        This section contains code that can send instantaneous commands to the motors to go to
        a specific well or pot in a given chip or plate, respectively. It also implements methods that
        allow for either picking up or dropping off spcific amounts of volumes of liquid 
    """
    def go_to_position(self, location):
        """ 
        This method moves the motor system to a target 3D location on a sequence of safety displacements as follows:
            1. Lift Z axis
            2. Move to the X and Y target positions
            3. Descend to the Z target position

        Args:
            location ([tuple]): contains three float numbers indicating a target 3D coordinate
        """
        self.ot_control.move_to(location=location)
        
    def go_to_deck_slot(self, slot):
        slot_number = float(slot)
        logging.info(f"Moving to slot {slot}")
        x= self.deck.get_slot_center(slot)[0]
        y = self.deck.get_slot_center(slot)[1]
        z = POSITION_IN_Z_TO_PLACE_WHEN_GOING_TO_SLOT
        location = [x, y, z]
        if (slot_number == 7 or slot_number == 8 or slot_number == 10 or slot_number == 11):
            self.open_lid() # We open the lid first to avoid collitions
            if self.ot_control.tc_lid_flag == 'open': 
                self.go_to_position(location)
        else:   
            self.go_to_position(location)        

    def go_to_well(self, chip, well_nickname):
        """ This method moves the system to the location assigned to a specific well in a chip by retrieving the location from myLabware and then calling go_to_position()

        Args:
            chip ([int]): this is the index of the Chip object contained in Labware
            well_nickname ([str]): this is a string representing the nickname of the well i.e. 'C4' or 'D11'
        """
        # Get the location of the well by its nickname
        location = self.myLabware.get_well_location(chip, well_nickname) # [x, y, z]
        self.go_to_position(location)

    def go_to_pot(self, plate, pot_nickname):
        """ This method moves the system to the location assigned to a specific pot in a plate by retrieving the location from myLabware and then calling go_to_position()

        Args:
            plate ([int]): this is the index of the Plate object contained in Labware
            pot_nickname ([str]): this is a string representing the nickname of the well i.e. 'C4' or 'D9'
        """
        # Get the location of the well by its nickname
        location = self.myLabware.get_pot_location(plate, pot_nickname) # [x, y, z]
        self.go_to_position(location)

    def movexyz(self, x, y, z):
        coordinates = { 'X': x, 'Y': y, 'Z': z }
        self.go_to_position(coordinates)

    def move(self, location, nicknames):
        if location == "mySample":
            logging.info(f"Moving to '{location}' at '{nicknames.mySample}'")
            locationString = nicknames.mySample
        else:
            logging.info(f"Moving to '{location}' at '{nicknames.get_nickname_location(location)}'")
            locationString = nicknames.get_nickname_location(location)

        # parse the string. Ex. p 1c4 --> type = 'p', number = 1, position = 'c4'
        type = locationString[0]
        number = locationString[2]
        position = locationString[3:]
        # call function to move motors (move_to_pot() or move_to_well())
        if type == 'p':
            self.go_to_pot(int(number), position)
        elif type == 'c':
            self.go_to_well(int(number), position)
        else:
            logging.info("ERROR: cannot move to any location other than POT or WELL")
    
    def pick_up_liquid(self, volume, speed = SLOW_SPEED): 
        """ Sends a command to the syringe motor to displace a distance that is equivalent to aspirating a given volume of liquid

        Args:
            volume ([float]): volume of liquid to be aspirated. UNIT: NANOLITERS
            speed ([float]): speed at which the given volume of liquid will be aspirated. UNIT: MILIMITERS/SECOND
        """     
        step_displacement = self.volume_to_displacement_converter(volume) 
        self.ot_control.set_step_size_syringe_motor(step_displacement)
        self.ot_control.plunger_L_Up(size=self.ot_control.s_step_size)

    def drop_off_liquid(self, volume, speed =SLOW_SPEED):
        """ Sends a command to the syringe motor to displace a distance that is equivalent to dispensing a given volume of liquid

        Args:
            volume ([float]): volume of liquid to be dispensed,. UNIT: NANOLITERS
            speed ([float]): speed at which the given volume of liquid will be dispensed. UNIT: MILIMITERS/SECOND
        """
        step_displacement = self.volume_to_displacement_converter(volume)
        self.ot_control.set_step_size_syringe_motor(step_displacement)
        self.ot_control.plunger_L_Down(size=self.ot_control.s_step_size)
    
    def volume_to_displacement_converter(self, volume):
        """ This method converts a certain amount of volume into displacement needed to move that amount of liquid in the syringe by retrieving the syringe dimensions from the system and doing some simple math

        Args:
            volume ([float]): volume of liquid to be converted. UNIT: NANOLITERS

        Returns:
            [float]: displacement that results in the displacement of the provided volume on the syringe. UNIT: MILIMETERS
        """
        # Get the current syringe model
        syringe_model = self.myLabware.get_syringe_model()

        # Extract syringe radius
        syringe_parameters = self.myModelsManager.get_model_parameters(LABWARE_SYRINGE, syringe_model)
        diameter = syringe_parameters["inner_diameter"] # This parameter has units of mm
        radius = diameter / 2

        # Calculate area and distance (height of the cylindric volume)
        area = (math.pi * radius * radius) # Basic formula for area
        distance_in_mm = volume * FROM_NANOLITERS / area # Volume is assumed to come in nanoLiters to it's converted to microliters to perform accurate calculations
        distance_to_feed_to_stepper_motor = distance_in_mm * UNIT_CONVERSION

        # Return the distance needed to displace that amount of volume
        self.ot_control.set_step_size_syringe_motor(distance_to_feed_to_stepper_motor)
        return distance_to_feed_to_stepper_motor

    def set_syringe_speed(self, nLminSpeed):
        mmspeed = self.volume_to_displacement_converter(nLminSpeed)/60
        
    def aspirate(self, volume, speed): 
        """ Pick up amount in nL and speed in nL/min  """
        logging.info(f"Aspirating {volume} nL at speed {speed} nL/s")
        self.pick_up_liquid(int(volume))

    def dispense(self, amount, speed): 
        """ Drop of amount in nL and speed in nL/min  """
        logging.info(f"Dispensing {amount} nL at speed {speed} nL/s")
        self.drop_off_liquid(int(amount))

    """
    LABWARE METHODS SECTION
        This section specifies methods related to the adding and removing of labware components
    """
    def get_component_models_location(self, component_type):
        """ Obtains the path in the system files to the location of chip, plate, or syringe model files

        Args:
            component_type ([str]): either 'c', 'p', or 's' for chip, plate, or syringe, respectively

        Returns:
            [str]: string describing the path to the location of the files of the specified component type
        """
        return self.myModelsManager.get_path(component_type)

    def get_available_component_models(self):
        """ Retrieve the available models registered in the system for chips, plates, and syringes

        Returns:
            [dict]: dictionary with three keys ("chips", "plates", and "syringes") that map to strings that correspond to the names of each of the models
        """
        return self.myModelsManager.get_stored_models()

    def create_new_chip_model(self, properties):
        """This method creates a new chip model (in a json file) using the provided dictionary of parameters and calling the corresponding
        method in ModelsManager which actually imports things to a file and saves it on the right directory

        Args:
            properties ([dict]): defines all the parameters for a new chip model (according to the properties defined in a regular chip file)
        """
        new_model_name = properties["chip_new_model_name"]
        grid = [int(properties["chip_grid_rows"]), int(properties["chip_grid_columns"])]
        point_distance = float(properties["chip_point_distance"])
        well_distance = float(properties["chip_well_distance"])
        row_types = properties["row_types"]
        nicknames = properties["nicknames"]
        self.myModelsManager.create_chip_model(new_model_name, grid, point_distance, well_distance, row_types, nicknames)
    
    def create_new_plate_model(self, properties):
        """This method creates a new plate model (in a json file) using the provided dictionary of parameters and calling the corresponding
        method in ModelsManager which actually imports things to a file and saves it on the right directory

        Args:
            properties ([dict]): defines all the parameters for a new plate model (according to the properties defined in a regular plate file)
        """
        new_model_name = properties["plate_new_model_name"]
        grid = [int(properties["plate_grid_rows"]), int(properties["plate_grid_columns"])]
        pot_distance_r = float(properties["plate_pot_distance_r"])
        pot_distance_c = float(properties["plate_pot_distance_c"])
        pot_depth = float(properties["plate_pot_depth"])
        nicknames = properties["nicknames"]
        self.myModelsManager.create_plate_model(new_model_name, grid, pot_distance_r, pot_distance_c, pot_depth, nicknames)
    
    def create_new_syringe_model(self, properties):
        """This method creates a new syringe model (in a json file) using the provided dictionary of parameters and calling the corresponding
        method in ModelsManager which actually imports things to a file and saves it on the right directory

        Args:
            properties ([dict]): defines all the parameters for a new syringe model (according to the properties defined in a regular syringe file)
        """
        new_model_name = properties["syringe_new_model_name"]
        volume = float(properties["syringe_volume"])
        inner_diameter = float(properties["syringe_inner_diameter"])
        self.myModelsManager.create_syringe_model(new_model_name, volume, inner_diameter)

    def get_current_labware(self):
        """ Obtains a disctionary with the components currently calibrated and loaded onto the system and ready to be used

        Returns:
            [dict]: dictionary with three keys ("chips", "plates", and "syringe") that map to lists of Chip and Plate onbjects and string with the name of the syringe being used
        """
        return self.myLabware.get_current_labware()

    def get_full_current_labware(self):
        """ This method returns a dictionary with all the labware components and their properties. For description on detailed contents, visit the documentation on labware_to_dictionary() in the Labware class

        Returns:
            [dict]: dictionary with all the labware components and all their properties
        """
        return self.myLabware.labware_to_dictionary()

    def save_labware_setup(self, output_file_name):
        """ Exports all the calibrated components to a file that can later be loaded onto the system to avoid recalibrating each component individually

        Args:
            output_file_name ([str]): desired name of output file
        """
        self.myLabware.save_labware_to_file(output_file_name)
    
    def load_labware_setup(self, input_file_name):
        """ Import previously calibrated and saved labware components from a json file to avoid recalibrating them individually

        Args:
            input_file_name ([str]): name of desired input file
        """
        self.myLabware.load_labware_from_file(input_file_name)
        chip_list = self.myLabware.chip_list
        plate_list = self.myLabware.plate_list
        return chip_list, plate_list
    

    def get_available_labware_setup_files(self):
        """ Obtain the list of available files with previously calibrated and exported labware components

        Returns:
            [list]: list of strings of names of files with previously calibrated labware components 
        """
        return self.myLabware.available_saved_labware_files()

    def guess_fourth_calibration_point(self, calibration_points):
        """ Guess the fourth point that defines a rectangle (plane) in 3D

        Args:
            calibration_points ([list]): list of three lists, each of which represents a point in 3 dimensions

        Returns:
            [list]: list containing 3 float numbers representing a 3D point in space that completes a rectangle with the three points provided in the argument of the function
        """

        return guess_fourth_calibration_point(calibration_points)
        
    def add_labware_component(self, labware_component, component_model, calibration_points):
        """ Add a labware component to the list of calibrated components in the system

        Args:
            labware_component ([str]): describes whether the component is a chip ('c') or a plate ('p')
            component_model ([str]): model name of the component being added
            calibration_points ([list]): list with the calibration points of the component
        """
        # This method finds the file named component_model and returns the content of that file as a dictionary
        component_parameters = self.myModelsManager.get_model_parameters(labware_component, component_model)

        if (labware_component == LABWARE_CHIP):
            mapped_well_locations = map_out_wells(component_parameters, calibration_points) # Map out components within the chip
            new_chip = create_chip(component_model, component_parameters, mapped_well_locations) # Create Chip object with all the internal information it needs
            self.myLabware.add_chip(new_chip) # Add chip to Chamber

        elif (labware_component == LABWARE_PLATE):
            mapped_pot_locations = map_out_pots(component_parameters, calibration_points) # Map out components within the plate
            new_plate = create_plate(component_model, component_parameters, mapped_pot_locations) # Create Plate object with all the internal information it needs
            self.myLabware.add_plate(new_plate) # Add plate to Chamber

    def remove_labware_component(self, labware_component, component_index):
        """ Delete a calibrated labware component from the list of current labware components

        Args:
            labware_component ([str]): describes whether the component is a chip ('c') or a plate ('p')
            component_index ([int]): index of the component in the list of chips or plates
        """
        if (labware_component == LABWARE_CHIP):
            self.myLabware.remove_chip(component_index)
            
        elif (labware_component == LABWARE_PLATE):
            self.myLabware.remove_plate(component_index)

    def set_syringe_model(self, syringe_model):
        """ Set the model of the syringe currenly being operated

        Args:
            syringe_model ([str]): name of the model of syringe
        """
        self.myLabware.set_syringe_model(syringe_model)

    """
    SETTINGS SECTION
    """
    
    def get_current_settings(self):
        """ Retrieve the current state of all the relevant settings of the system and store them in a dictionary

        Returns:
            [dict]: contains a mapping of setting keywords and values for all the relevant settings of the system
        """
        settings_dict = dict()

        settings_dict["coordinate_refresh_rate"] = self.coordinates_refresh_rate

        settings_dict["syringe_model"] = self.get_current_labware()["syringe"]
        settings_dict["syringe_default_speed"] = self.ot_control.get_step_speed_syringe_motor()
        
        settings_dict["xyz_axis_step_size"] = self.ot_control.get_step_size_xyz_motor()
        settings_dict["xyz_axis_step_speed"] = self.ot_control.get_step_speed_xyz_motor()
        settings_dict["x_axis_orientation"] = self.myController.get_axis_direction(self.get_linked_joystick_axis_index("x"))
        return settings_dict

    def update_setting(self, property_name, value):
        """ Update the value of a given setting in the system

        Args:
            property_name ([str]): keyword that matches the value of any of the if statements within this method
            value ([various]): value to be loaded on the setting being updated
        """
        # Go through all the cases and adjust the appropriate property

        if property_name == "coordinate_refresh_rate":
            self.coordinates_refresh_rate = float(value)

        elif property_name == "syringe_model":
            self.set_syringe_model(value)
        elif property_name == "syringe_default_speed":
            self.ot_control.set_step_speed_syringe_motor(float(value))

        elif property_name == "xyz_axis_step_size":
            self.ot_control.set_step_size_xyz_motor(float(value))
        elif property_name == "xyz_axis_step_speed":
            self.ot_control.set_step_speed_xyz_motor(float(value))
        elif property_name == "xyz_axis_gearbox":
            self.ot_control.set_x_motor_gearbox([float(i) for i in value.split(",")])
     

        # ADD MORE SETTING HANDLERS BELOW. FORMAT:
        # elif property_name == "xxxxxxxxxxx":
        #     pass
        
        else:
            logging.info(f"ERROR: {property_name} PROPERTY NOT LINKED TO ANY MODIFICATION ON THE SYSTEM\n") 


    """
    FEEDBACK SECTION
        This section is meant to define methods that retrieve information from the 
        components of the system
    """
    
    def get_current_coordinates(self):
        """ Gets the position of each of the stages associated with 3 dimensional motion: X, Y, and Z axes

        Returns:
            [float]: three float numbers rounded to the third decimal point representing X, Y, and Z coordinates
        """
        return (self.ot_control._position['X'], self.ot_control._position['Y'], self.ot_control._position['Z'])

    def get_coordinate_refresh_rate(self):
        """ Get the period for refreshing the coordinates in the GUI

        Returns:
            [float]: time elapsed between every instance when the coordinates are refreshed in the GUI
        """
        return self.coordinates_refresh_rate

    def set_coordinate_refresh_rate(self, new_rate):
        """ Set the period for refreshing the coordinates in the GUI

        Args:
            new_rate ([float]): time elapsed between every instance when the coordinates are refreshed in the GUI
        """
        self.coordinates_refresh_rate = new_rate

    '''
    PROTOCOL METHODS SECTION FOR OT2
        This section defines methods that get called to facilitate reading a script of instructions 
    '''
    def aspirate_from(self, amount, source):
        """This will go to the position of the source and aspirate an amount in nL"""
        self.go_to_position(source)
        self.aspirate(amount, ASPIRATE_SPEED)
        time.sleep(TIME_TO_SETTLE) # Allow some time to the syringe to aspirate

    def dispense_to(self, amount, to):
        """This will go to the position of the destination and dispense an amount in nL"""
        print(f"Go to {to} and dispense ")
        self.go_to_position(to)
        self.dispense(amount, ASPIRATE_SPEED)
        time.sleep(TIME_TO_SETTLE) # Allow some time to the syringe to dispense
    
    """
    PROTOCOL METHODS SECTION FOR THERMOCYCLER 
    """
    
    def tc_connect(self):
        asyncio.run(self.tc_control.connect(port= self.tc_port))

    def open_lid(self):
        self.go_to_deck_slot('12') # for avoiding collitions
        asyncio.run(self.tc_control.open())
        self.ot_control.set_tc_lid_flag('open')

    def close_lid(self):
        self.go_to_deck_slot('12') # for avoiding collitions
        asyncio.run(self.tc_control.close())
        self.ot_control.set_tc_lid_flag('closed')

    def deactivate_all(self):
        asyncio.run(self.tc_control.deactivate_all())
    
    def deactivate_lid(self):
        asyncio.run(self.tc_control.deactivate_lid())

    def deactivate_block(self):
        asyncio.run(self.tc_control.deactivate_block())

    def set_temperature(self ,temp: float, hold_time:  float = None):
        asyncio.run(self.tc_control.set_temperature(temp, hold_time))

    def set_lid_temp(self, temp: float):
        asyncio.run(self.tc_control.set_lid_temperature(temp))

    def tc_disconnect(self):
        self.tc_control.disconnect()

    def set_block_temp(self, target_temp, holding_time_in_minutes):
        hold_time_in_secs = holding_time_in_minutes * 60
        self.set_temperature(temp=target_temp, hold_time=hold_time_in_secs)
        current_temp = float(self.tc_control.get_block_temp())
        logging.info("Checking temperature of the block")
        logging.info(f"Current_temp = {current_temp} [C] ---- Target Temperature = {target_temp} [C]")
        
        # While the target temperature has not been reached within a 1 of allowance check every five seconds and then continue to hold for specified time
        while (float(current_temp) < (float(target_temp) - 1)) or (float(current_temp) > (float(target_temp) + 1)):
            current_temp = self.tc_control.get_block_temp()
            time.sleep(5)
            logging.info(f"Current_temp = {current_temp} [C]")
        logging.info("Target temperature {current_temp} [C] reached")

        logging.info(f"Holding for {holding_time_in_minutes} minutes.")
        min_count = 0 # init for tcounting the minutes to hold

        # here we start the holding time. We check every half a minute and exit the loop when the time holding is equal than the time to hold
        while float(min_count) < float(holding_time_in_minutes):
            time.sleep(30)
            min_count = min_count + 0.5
        logging.info("Holding time done. Proceeding to complete next step.")


    """
    PROTOCOL METHODS SECTION FOR TEMPDECK 
    """

    def set_tempdeck_temp(self, celcius, holding_time_in_minutes):
        hold_time_in_secs = holding_time_in_minutes * 60
        self.td_control.start_set_temperature(celcius)
        current_temp = self.get_tempdeck_temp()
        logging.info("Checking temperature of the TempDeck")
        logging.info(f"Current_temp = {current_temp} [C] ---- Target Temperature = {celcius} [C]")

        # While the target temperature has not been reached within a 1 of allowance check every five seconds and then continue to hold for specified time
        while (float(current_temp) < (float(celcius) - 1)) or (float(current_temp) > (float(celcius) + 1)):
            current_temp = self.get_tempdeck_temp()
            time.sleep(5)
            logging.info(f"Current_temp = {current_temp} [C]")
            print(self.check_tempdeck_status())
        logging.info("Target temperature {current_temp} [C] reached")

        logging.info(f"Holding for {holding_time_in_minutes} minutes.")
        min_count = 0 # init for tcounting the minutes to hold

        # here we start the holding time. We check every half a minute and exit the loop when the time holding is equal than the time to hold
        while float(min_count) < float(holding_time_in_minutes):
            time.sleep(30)
            min_count = min_count + 0.5
        logging.info("Holding time done. Proceeding to complete next step.")

    def deactivate_tempdeck(self):
        self.td_control.deactivate()

    def get_tempdeck_temp(self):
        self.td_control.update_temperature()
        time.sleep(0.01)
        return self.td_control.temperature

    def check_tempdeck_status(self):
        return self.td_control.status

    """
    RUN PROTOCOL COORDINATION SECTION
    """

    def pause_protocol(self):
        """This method pauses the protocol process"""
        pass

    def verify_container_existence(self, container_description):
        """Verify that a given well or pot exists in a given chip or plate, respectively, by providing a coded description
            String input looks like: "p 1E3" or "c 1B3" : "[component] [component_index][well/pot nickname]"

        Args:
            container_description ([str]): string that describes what container needs to be verified
        """
        return self.myLabware.check_well_pot_existence(container_description)

    def connect_all(self):
        """This method connects the modules connected to the computer"""
        self.disconnect_all()
        self.tc_control._connection = self.tc_control._connect_to_port()
        self.ot_control.connect_driver()
        self.td_control.connect(self.ot_control._port)

    def disconnect_all(self):
        """This method disconnects the modules connected to the computer"""
        self.tc_disconnect()
        self.ot_control.disconnect()
        self.ot_control.disconnect()

def test():
    myApp = Coordinator()
    
    # myApp.go_to_deck_slot('6')
    # myApp.close_lid()
    # myApp.set_block_temp(4, 5)
    # myApp.set_syringe_model("HAMILTON_175")
    # myApp.home_all_motors()
    # myApp.manual_control()
    # myApp.go_to_position([200, Y_MIN, 40 ])

if __name__ == "__main__":
    test()


