"""
Description of the program:

    This code contains a child class that is used to control the robot by single step movements. 
    The parent class is the driver that Opentrons have created to send commands to the OT2 
    
    In order to move a single axis an amount of units, we pass in the unit we want to use and the 
    amount we want the robot to move every step. There is a function on SmoothieDriver_3_0_0 class 
    that returns the position as a dicctionary in the following format: 

        { 'X': 150, 'Y': 150, 'Z': 170.15, 'A': 218.0, 'B': 0.0, 'C': 0.0}
volume
    The move on a single axis happens by using the method SmoothieDriver_3_0_0.move() wich moves to a 
    specified coordinate, but in this case we only change the coordinate that we need keeping the rest
    the same. 

"""
from opentrons.drivers.smoothie_drivers.driver_3_0 import SmoothieDriver_3_0_0 as SM, SmoothieError
from opentrons.config.robot_configs import build_config
from serial.tools import list_ports
import os
from constants import RUNNING_APP_FOR_REAL, UNIT_CONVERSION
import labware_class 

X_MAX = 418
X_MIN = 25
Y_MAX = 340
Y_MIN = 5

LEFT_PIPETTE_ATTACHED = True
Z_MAX_NO_PIPETTE = 218
Z_MIN_NO_PIPETTE = 78
Z_MAX_WITH_PIPETTE = 170.15 # values for when pipette is attached
Z_MIN_WITH_PIPETTE = 20 # values for when pipette is attached

RIGHT_PIPETTE_ATTACHED = False
A_MAX_NO_PIPETTE = 218
A_MIN_NO_PIPETTE = 78
A_MAX_WITH_PIPETTE = 170.15 # values for when pipette is attached
A_MIN_WITH_PIPETTE = 20 # values for when pipette is attached

B_MAX = 0
B_MIN = -50
C_MAX = 0
C_MIN = -50
TC_X = 211
TC_Y = 155
TC_Z_OPEN_LID = 170
TC_Z_CLOSED_LID = 170
DEFAULT_STEP_SIZE = 10 # Used for manual and protocol control when step size is not specified

SHORT_MEDIUM_STEP_LIMIT = 10 # used for determining appropriate motor speeds
MEDIUM_LONG_STEP_LIMIT = 50 # used for determining appropriate motor speeds
APPROACH_DISTANCE = 10 # Distance from target where robot slows down if needed

DEFAULT_STEP_SPEED = 10 # default speed for protocols (only used if user forgets to specify speeds) 
SLOW_SPEED = 10 
MEDIUM_SPEED = 40
HIGH_SPEED = 160

SYRINGE_LIMITS_DICT = {"upper_syringe_limit": B_MAX, "lower_syringe_limit": B_MIN} # limits are determined by specific syringe model
SYRINGE_SLOW_SPEED = 0.3 * UNIT_CONVERSION #mm/s (The syringe motor distances are off by a factor of UNIT_CONVERSION) 
SYRINGE_DEFAULT_STEP = 1 * UNIT_CONVERSION #mm (The syringe motor distances are off by a factor of UNIT_CONVERSION)

list_of_sizes = [0.01, 0.1, 1, 5, 10, 25, 50, 100] # step sizes available for manual control
DEFAULT_STEP_INDEX = 2 # Determines starting step size for manual control from list_of_sizes

LEFT = 'Left' #A
RIGHT = 'Right' #B

WINDOWS_OT_PORT = 'COM4'
WINDOWS_OT_SER = 'A50285BIA'
LINUX_OT_PORT = '/dev/ttyACM0'
MACBOOK_OT_PORT = "/dev/cu.usbserial-A50285BI"
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'



class OT2_nanotrons_driver(SM):
    def __init__(self):#, port):
        super().__init__(config=build_config({}))

        # Atributes that control the size and speed of the X Y and Z axis. 
        #   When changed, all of them move at the same rate
        self.xyz_step_size = DEFAULT_STEP_SIZE
        self.xyz_step_speed = DEFAULT_STEP_SPEED
        
        self._port = None
        # Attributes that control the size and speed of the plunger. 
        self.syringe_step_size = SYRINGE_DEFAULT_STEP #Step size for the syringe in mm.
        self.syringe_step_speed = SYRINGE_SLOW_SPEED #Step speed for the syringe

        self.right_pipette_attached = RIGHT_PIPETTE_ATTACHED
        self.left_pipette_attached = LEFT_PIPETTE_ATTACHED
        if self.left_pipette_attached:
            self.z_max = Z_MAX_WITH_PIPETTE
            self.z_min = Z_MIN_WITH_PIPETTE
        else:
            self.z_max = Z_MAX_NO_PIPETTE
            self.z_min = Z_MIN_NO_PIPETTE
        if self.right_pipette_attached:
            self.z_max = Z_MAX_WITH_PIPETTE
            self.z_min = Z_MIN_WITH_PIPETTE
        else:
            self.a_max = A_MAX_NO_PIPETTE
            self.a_min = A_MIN_NO_PIPETTE

        self.nL = 0 #nanoliters that the syringe is currently working with
        self.side = LEFT 
        self.flag = True
        self.xyz_step_size_index = DEFAULT_STEP_INDEX
        self.tc_flag = True
        self.tc_lid_flag = 'Open'
        if RUNNING_APP_FOR_REAL:
            self.connect_driver()
        else:
            print("Not connected to the OT port")

# Functions that help movements
        
    def check_for_valid_move(self, pos, axis, syringe_parameters = SYRINGE_LIMITS_DICT) -> bool:
        # print(pos)
        """
        This function checks for limits. If the user tries to go too far, the move 
        will not be executed. Returns false if the move is outside the allowed limits
        """

        if axis == 'X' and (pos > X_MAX or pos < X_MIN):
            print("x_max:", X_MAX, "x_min", X_MIN, "x_requested", pos)
            return False
        elif axis == 'Y' and (pos > Y_MAX or pos < Y_MIN):
            print("Y_max:", Y_MAX, "Y_min", Y_MIN, "Y_requested", pos)
            return False
        elif axis == 'Z' and (pos > self.z_max or pos < self.z_min):
            print("z_max:", self.z_max, "z_min", self.z_min, "z_requested", pos)
            return False
        elif axis == 'A' and (pos > self.a_max or pos < self.a_min):
            print("A_max:", self.a_max, "A_min", self.a_min, "A_requested", pos)
            return False
        elif axis == 'B' and (pos > syringe_parameters["upper_syringe_limit"] or pos < syringe_parameters["lower_syringe_limit"]):
            print("B_max:", B_MAX, "B_min", B_MIN, "B_requested", pos)
            return False
        elif axis == 'C' and (pos > syringe_parameters["upper_syringe_limit"] or pos < syringe_parameters["lower_syringe_limit"]):
            print("C_max:", C_MAX, "C_min", C_MIN, "C_requested", pos)
            return False
        else:
            return True

    def check_speed(self, step_size):
        """
        This function sets a speed acording to the step size given.
        There are 3 different speeds that are assigned: Slow, Medium and High
        """
        if step_size <= SHORT_MEDIUM_STEP_LIMIT:
            return SLOW_SPEED
        elif step_size < MEDIUM_LONG_STEP_LIMIT:
            return MEDIUM_SPEED
        else:
            return HIGH_SPEED

    def step_size_up(self):
        """"
        xyz_step_size is assigned from a list of available step sizes.
        This function first checks that the current step size is not the maximum step size on the list.
        If it is not, then xyz_step size is assigned to the next size up in the list.
        """
        if self.xyz_step_size_index < (len(list_of_sizes) -1):
            self.xyz_step_size_index += 1
            self.xyz_step_size = list_of_sizes[self.xyz_step_size_index]
            print(f"\nManual Movement set to {self.xyz_step_size} mm\n")
        else:
            print("\nCannot further increase or decrease the Manual Control movement size")
            print(f"Manual Movement set to {self.xyz_step_size} mm\n")

    def step_size_down(self):
        """"
        xyz_step_size is assigned from a list of available step sizes.
        This function first checks that the current step size is not the minimum step size on the list.
        If it is not, then xyz_step size is assigned to the next size down in the list.
        """
        if self.xyz_step_size_index > 0:
            self.xyz_step_size_index -= 1
            self.xyz_step_size = list_of_sizes[self.xyz_step_size_index]
            print(f"Stepping {self.xyz_step_size}[mm]")
        else:
            print(f"{str(self.xyz_step_size)} is the lowest step size allowed")

# Functions to move the different axis, X, Y, Z and syringe: 



    def move_forward(self, step_size = DEFAULT_STEP_SIZE):  
        """
        This functions moves the pippetes by steps. 
        """
        y_pos = self._position['Y'] # stores the current position
        y_pos += step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(y_pos, 'Y')): # if the future position is a valid move 
                self.move({'Y': y_pos-APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'Y': y_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(y_pos, 'Y')): # if the future position is a valid move 
                self.move({'Y': y_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")  

    def move_back(self, step_size = DEFAULT_STEP_SIZE):
        y_pos = self._position['Y'] # stores the current position
        y_pos -= step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(y_pos, 'Y')): # if the future position is a valid move 
                self.move({'Y': y_pos+APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'Y': y_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(y_pos, 'Y')): # if the future position is a valid move 
                self.move({'Y': y_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n") 

    def move_left(self, step_size = DEFAULT_STEP_SIZE):
        x_pos = self._position['X'] # stores the current position
        x_pos -= step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(x_pos, 'X')): # if the future position is a valid move 
                self.move({'X': x_pos+APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'X': x_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(x_pos, 'X')): # if the future position is a valid move 
                self.move({'X': x_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")

    def move_right(self, step_size = DEFAULT_STEP_SIZE):
        x_pos = self._position['X'] # stores the current position
        x_pos += step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(x_pos, 'X')): # if the future position is a valid move 
                self.move({'X': x_pos-APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'X': x_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(x_pos, 'X')): # if the future position is a valid move 
                self.move({'X': x_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")

    def A_axis_Down(self, step_size = DEFAULT_STEP_SIZE):
        a_pos = self._position['A'] # stores the current position
        a_pos -= step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(a_pos, 'A')): # if the future position is a valid move 
                self.move({'A': a_pos+APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'A': a_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(a_pos, 'A')): # if the future position is a valid move 
                self.move({'A': a_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")

    def A_axis_Up(self, step_size = DEFAULT_STEP_SIZE):
        a_pos = self._position['A'] # stores the current position
        a_pos += step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(a_pos, 'A')): # if the future position is a valid move 
                self.move({'A': a_pos-APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'A': a_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(a_pos, 'A')): # if the future position is a valid move 
                self.move({'A': a_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")
    
    def Z_axis_Down(self, step_size = DEFAULT_STEP_SIZE):
        z_pos = self._position['Z'] # stores the current position
        z_pos -= step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(z_pos, 'Z')): # if the future position is a valid move 
                self.move({'Z': z_pos+APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'Z': z_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(z_pos, 'Z')): # if the future position is a valid move 
                self.move({'Z': z_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")

    def Z_axis_Up(self, step_size = DEFAULT_STEP_SIZE):
        z_pos = self._position['Z'] # stores the current position
        z_pos += step_size # adds a step size to the current position
        if step_size > APPROACH_DISTANCE:
            if(self.check_for_valid_move(z_pos, 'Z')): # if the future position is a valid move 
                self.move({'Z': z_pos-APPROACH_DISTANCE}, speed= self.check_speed(step_size)) # move near the indicated position at higher speed
                self.move({'Z': z_pos}, speed= SLOW_SPEED) # move to the indicated position at slow speed
            else:
                print("\nRequested move is not valid!\n")
        else:
            if(self.check_for_valid_move(z_pos, 'Z')): # if the future position is a valid move 
                self.move({'Z': z_pos}, speed= self.check_speed(step_size)) # move to the indicated position
            else:
                print("\nRequested move is not valid!\n")

    def plunger_L_Up(self, size: float = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED, syringe_model = labware_class.SYRINGE_MODEL, syringe_parameters = SYRINGE_LIMITS_DICT):
        # print(f"Size aspirating:{size}")
        # if self.flag == True:
        #     size = S_STEP_SIZE
        if syringe_model != labware_class.SYRINGE_MODEL:
            speed = float(speed)
            b_pos: float = self._position['B'] # stores the current position
            b_pos += size # adds a step size to the current position
            if(self.check_for_valid_move(b_pos, 'B', syringe_parameters)): # if the future position is a valid move 
                # print(f"This is in OTdriver (Plunger L up)")
                # print(f"step size is {(size / UNIT_CONVERSION)}")
                # print(f"current plunger speed is: {speed} mm/s")
                # good_speed = input("Is this a good speed (y/n): ")
                # if good_speed == "y":
                self.move({'B': b_pos}, speed = speed) # move to the indicated position
                # # else:
                #     speed = float(input("What speed would you like to use (mm/s): "))
                #     self.move({'B': b_pos}, speed = speed) # move to the indicated position
                #     print(f"New B position: {b_pos}")
            else:
                print(f"Cannot move to {b_pos}")
                print(f"Current position is: {self._position['B']}")
                print(f"Requested distance is: {size}")
                print(f'Upper limit for left syringe: {syringe_parameters["upper_syringe_limit"]}')
                    # Add print for boundary position

        else:
            print("Please select a syringe model (L-up)")

    def plunger_L_Down(self, size: float = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED, syringe_model = labware_class.SYRINGE_MODEL, syringe_parameters = SYRINGE_LIMITS_DICT):
        # print(f"Size aspirating:{size}")
        # if self.flag == True:
        #     size = S_STEP_SIZE
        if syringe_model != labware_class.SYRINGE_MODEL:
            speed = float(speed)
            b_pos: float = self._position['B'] # stores the current position
            b_pos -= size # adds a step size to the current position
            if(self.check_for_valid_move(b_pos, 'B', syringe_parameters)):
                self.move({'B': b_pos}, speed = speed) # move to the indicated position
            else:
                print(f"Cannot move to {b_pos}")
                print(f"Current position is: {self._position['B']}")
                print(f"Requested step size is: {size}")
                print(f'Lower limit for left syringe: {syringe_parameters["lower_syringe_limit"]}')
                    # Add print for boundary position

        else:
            print("Please select a syringe model (L-down)")

    def plunger_R_Up(self, size: float = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED, syringe_model = labware_class.SYRINGE_MODEL, syringe_parameters = SYRINGE_LIMITS_DICT):
        #if self.flag == True:
           # size = S_STEP_SIZE
        if syringe_model != labware_class.SYRINGE_MODEL:
            speed = float(speed)
            c_pos: float = self._position['C'] # stores the current position
            c_pos = c_pos + size # adds a step size to the current position
            if(self.check_for_valid_move(c_pos, 'C', syringe_parameters)): # if the future position is a valid move 
                    self.move({'C': c_pos}, speed = speed) # move to the indicated position
            else:
                print(f"Cannot move to {c_pos}")
                print(f"Current position is: {self._position['B']}")
                print(f"Requested step size is: {size}")
                    # Add print for boundary position

        else:
            print("Please select a syringe model")

    def plunger_R_Down(self, size: float = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED, syringe_model = labware_class.SYRINGE_MODEL, syringe_parameters = SYRINGE_LIMITS_DICT):
       # if self.flag == True:
           # size = S_STEP_SIZE
        if syringe_model != labware_class.SYRINGE_MODEL:
            speed = float(speed)
            c_pos: float = self._position['C'] # stores the current position
            c_pos = c_pos - size # adds a step size to the current position
            if(self.check_for_valid_move(c_pos, 'C', syringe_parameters)): # if the future position is a valid move 
                # print(f"step size is {(size / UNIT_CONVERSION)}")
                # print(f"current plunger speed is: {speed} mm/s")
                # good_speed = input("Is this a good speed (y/n): ")
                # if good_speed == "y":
                    self.move({'C': c_pos}, speed = speed) # move to the indicated position
                # else:
                #     speed = float(input("What speed would you like to use (mm/s): "))
                #     self.move({'C': c_pos}, speed = speed) # move to the indicated position
                # print(f"New C position: {c_pos}")
            else:
                print(f"Cannot move to {c_pos}")
                print(f"Current position is: {self._position['B']}")
                print(f"Requested step size is: {size}")
                    # Add print for boundary position

        else:
            print("Please select a syringe model")

    def remove_left_pipette(self):
        self.left_pipette_attached = False
        self.z_max = Z_MAX_NO_PIPETTE
        self.z_min = Z_MIN_NO_PIPETTE
        print("Removing left pipette in settings.")
        print("Make sure left pipette is really removed!")

    def attach_left_pipette(self):
        self.left_pipette_attached = True
        self.z_max = Z_MAX_WITH_PIPETTE
        self.z_min = Z_MIN_WITH_PIPETTE
        print("Attaching left pipette in settings.")
        print("Make sure left pipette is really attached!")

    def remove_right_pipette(self):
        self.right_pipette_attached = False
        self.a_max = A_MAX_NO_PIPETTE
        self.a_min = A_MIN_NO_PIPETTE
        print("Removing right pipette in settings.")
        print("Make sure right pipette is really removed!")

    def attach_right_pipette(self):
        self.right_pipette_attached = True
        self.a_max = A_MAX_WITH_PIPETTE
        self.a_min = A_MIN_WITH_PIPETTE
        print("Attaching right pipette in settings.")
        print("Make sure right pipette is really attached!")
    
    def update_pipette_attachment_status(self):
        print("updating pipette status\n")
        if self.side == LEFT:
            print(f"current side is {self.side}")
            if self.left_pipette_attached:
                print("left pipette was attached\n")
                self.remove_left_pipette()
            elif not self.left_pipette_attached:
                print("left pipette was not attached\n")
                self.attach_left_pipette()
    
        elif self.side == RIGHT:
            print(f"current side is {self.side}")
            if self.right_pipette_attached:
                print("right pipette was attached\n")
                self.remove_right_pipette()
            elif not self.right_pipette_attached:
                print("right pipette was not attached\n")
                self.attach_right_pipette()
        
        else:
            print("pipette status failed to update")
                


## These functions are just as the ones without the _aut but the logic is a little
## different since they are used by coordinator/volume etc. The step size input in 
## this case comes with a negative sign if it goes down, so both have the same sign. 

    def plunger_L_Up_aut(self, size = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED):
        b_pos = self._position['B']
        b_pos += size
        self.move({'B': b_pos}, speed= speed) # move to the indicated position

    def plunger_L_Down_aut(self, size = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED):
        b_pos = self._position['B']
        b_pos += size
        self.move({'B': b_pos}, speed= speed) # move to the indicated position

    def plunger_R_Up_aut(self, size = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED):
        c_pos = self._position['C']
        c_pos += size
        self.move({'C': c_pos}, speed= speed) # move to the indicated position

    def plunger_R_Down_aut(self, size = SYRINGE_DEFAULT_STEP, speed = SYRINGE_SLOW_SPEED):
        c_pos = self._position['C']
        c_pos += size
        self.move({'C': c_pos}, speed= speed) # move to the indicated position

# Getters and Setters 
    def get_side(self):
        return self.side;
        
    def get_x_motor_index(self):
        return 'X'

    def get_y_motor_index(self):
        return 'Y'

    def get_z_motor_index(self):
        return 'Z'

    def get_syringe_motor_index(self):
        return 'S'

    def get_step_size_xyz_motor(self):
        return (self.xyz_step_size)

    def get_step_size_syringe_motor(self):
        return self.syringe_step_size

    def get_step_speed_xyz_motor(self):
        return self.xyz_step_speed

    def get_step_speed_syringe_motor(self):
        return self.syringe_step_speed
    
    def get_nL(self):
        return self.nL

    def set_step_size_xyz_motor(self, new_step_size):
        self.xyz_step_size = new_step_size
    
    def set_step_speed_xyz_motor(self, new_step_speed):
        self.xyz_step_speed = new_step_speed

    def set_step_size_syringe_motor(self, new_step_size):
        self.syringe_step_size = new_step_size

    def set_step_speed_syringe_motor(self, new_step_speed):
        self.syringe_step_speed = new_step_speed

    def set_nL(self, nL):
        self.nL = nL

    def set_tc_flag(self, is_tc_mounted: bool):
        self.tc_flag = is_tc_mounted

    def set_tc_lid_flag(self, status: str):
        self.tc_lid_flag = status


        
# Other functions

    def move_to(self, location):

        x = location[0] #or self.ot_control._position["X"]
        y = location[1] #or self.ot_control._position["Y"]
        z = location[2] #or self.ot_control._position["Z"]

        current_z_pos = self._position['Z']
        
        if current_z_pos == z and (current_z_pos + 25) < self.z_max:
            self.move({'Z': current_z_pos + 25}, speed= MEDIUM_SPEED)
        elif current_z_pos + 40 < self.z_max:
            self.move({'Z': current_z_pos + 40}, speed= MEDIUM_SPEED)
        else:
            self.move({'Z': self.z_max}, speed= MEDIUM_SPEED)
        if(self.check_for_valid_move(y, 'Y')):
            # First move the Y axis so that it does not collide with the thermocycler
            self.move({'Y': y}, speed= MEDIUM_SPEED)
            if(self.check_for_valid_move(x, 'X')):
                self.move({'X': x}, speed= MEDIUM_SPEED)
                if(self.check_for_valid_move(z, 'Z')):
                    if (current_z_pos + 5) < self.z_max:
                        self.move({'Z': current_z_pos + 5}, speed= MEDIUM_SPEED)
                    self.move({'Z': z}, speed= SLOW_SPEED)

    def change_vertical_axis(self):
        # This function allows the controller to have more functionality
        if self.side == LEFT:
            self.side = RIGHT
            print("Vertical axis: RIGHT")
        elif self.side == RIGHT:
            self.side = LEFT
            print("Vertical axis: Left")
        else:
            print("Vertical Axis Error!")
            
    def report_current_position(self):
        # This function allows the controller to have more functionality
        X_position: float = self._position['X']
        Y_position: float = self._position['Y']
        print("")
        print(f"Current X position: {X_position}")
        print(f"Current Y position: {Y_position}")
        if self.side == LEFT:
            if self.left_pipette_attached:
                print("Left pipette is attached in settings")
                # print(f"Z_max is {self.z_max}")
                # print(f"Z_min is {self.z_min}")
            else:
                print("Left pipette is NOT attached in settings")
                # print(f"Z_max is {self.z_max}")
                # print(f"Z_min is {self.z_min}")
            print(f"Current Z is {self._position['Z']}")
            print(f"Syringe position is {self._position['B']}\n")
            
        elif self.side == RIGHT:
            if self.right_pipette_attached:
                print("Right pipette is attached in settings")
                # print(f"A_max is {self.a_max}")
                # print(f"A_min is {self.a_min}")
            else:
                print("Right pipette is NOT attached in settings")
                # print(f"A_max is {self.a_max}")
                # print(f"A_min is {self.a_min}")
            print(f"Current A is {self._position['A']}")
            print(f"Syringe position is {self._position['C']}\n")
        else:
            print("Vertical Axis Error!\n")

    def get_motor_coordinates(self):
        x = self._position['X']
        y = self._position['Y']
        z = self._position['Z']
        return x, y, z
    
    def home_all(self):
        # print("Example:  'X Y Z A B C' or 'all' ")
        try:
            self.home('X Y Z A')
        except SmoothieError:
            self.home('A') # Home the syringe
        
    def stop_motor(self, device = 'XYZABC'):
        self.disengage_axis(device)

    def nothing(self, argument = 1):
        pass
    
    def screen_info(self):
        print("............................................")
        print("")
        print(f"Step size S set to:          {self.syringe_step_size}") 
        print(f"Nanoliters to pick up:       {self.nL}")
        print(f"Step size XYZ set to:        {self.xyz_step_size}")
        print(f"Pipette controlling:         {self.side}")
        print(f"X: {self.position['X']}   Y: {self.position['Y']}   Z: {self.position['Z']}  S_B:  {self._position['B']} S_C:  {self._position['C']}")
        print("")
        print("............................................")

    def find_port(self):
        """
        This allows the class to connect to a port when called, this makes the calling chain cleaner. 
        It is basicaly a ger_port_by_name from the driver_3_0_0 that does not work
        """
        ports = list_ports.comports()
        operating_system = os.name
        for p in ports:
            # print(p)
            if operating_system == WINDOWS_OS and p.serial_number == WINDOWS_OT_SER:
                self._port = p.device
                print(f"\nOT2 connected to: {p}\n")
            elif operating_system == LINUX_OS:
                if p == LINUX_OT_PORT or p.device == MACBOOK_OT_PORT:
                    self._port = p.device
                    # print(self._port)
                    print(f"\nOT2 connected to: {p}\n")
                else: 
                    # print(f"Port not found: {p.device}")
                    pass
            # else:
            #     print(f"No operating system recognized: {operating_system}")
            
    def connect_driver(self):
        """
        This function is called at the beginning of the class in the init function to connect the robot
        """
        # self.disconnect()
        self.find_port()
        self.connect(self._port)

def test():
    robot = OT2_nanotrons_driver()
    robot.find_port()

if __name__ == '__main__':
    test()
