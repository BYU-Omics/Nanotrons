"""
This class is the interface between the user writing a simple protocol and the coordinator. This is just
a smalled coordinator that does not know about all the other functions and what they do step by step. It limits
the user to write only neccessary commands to perform protocols. 
"""
from coordinator import *
import sys
import requests

LABWARE = sys.argv[1]
# If we're not in the top level
# And we're trying to call the file directly
# add the submodules to $PATH
# sys.path[0] is the current file's path
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')
WEB_ADDRESS = 'http://localhost:5000/'

my_data = {'name': 'True'}

PLATE_DEPTH = "Plate's depth"

SYRINGE_BOTTOM = -190
SYRINGE_SWEET_SPOT = -165 # Place where the plunger is at 3/4 from the top to bottom
SYRINGE_TOP = -90

class Api:
    def __init__(self):
        self.coordinator = Coordinator()
        self.current_labware_depth = None
        self.clean_water = None
        self.wash_water = None
        self.waste_water = None
        self.amount_wanted = None
        
    def set_washing_positions(self, clean_water, wash_water, waste_water):
        self.clean_water = clean_water
        self.wash_water = wash_water
        self.waste_water = waste_water

    def start_wash(self):
        # Go to waste and SYRINGE_BOTTOM
        self.coordinator.go_to_position(self.waste_water)
        self.coordinator.move_plunger(SYRINGE_BOTTOM)

        # Go to wash, SYRINGE_TOP, SYRINGE_BOTTOM
        self.coordinator.go_to_position(self.wash_water)
        self.coordinator.move_plunger(SYRINGE_TOP)
        self.coordinator.move_plunger(SYRINGE_BOTTOM)

        # Go to clean, SYRINGE_SWEET_SPOT
        self.coordinator.go_to_position(self.clean_water)
        self.coordinator.move_plunger(SYRINGE_SWEET_SPOT)

        # Airgap
        self.coordinator.air_gap()

    def mid_wash(self, left_over = 200, cushion_1 = 200, cushion_2 = 300):
        # Go to waste, dispense left overs
        self.coordinator.go_to_position(self.waste_water)
        self.coordinator.dispense(left_over, SLOW_SPEED)
        
        # Go to wash, aspirate amount wanted + Cushion 1, dipense amount wanted + Cushion 2
        self.coordinator.go_to_position(self.wash_water)
        self.coordinator.aspirate(self.amount_wanted + cushion_1)
        self.coordinator.dispense(self.amount_wanted + cushion_2)

        # Go to clean, go to sweet spot
        self.coordinator.go_to_position(self.clean_water)
        self.coordinator.move_plunger(SYRINGE_SWEET_SPOT)

        # Airgap
        self.coordinator.air_gap()

    def air_gap(self):
        self.coordinator.air_gap()

    def load_labware_setup(self, file_name):
        return self.coordinator.load_labware_setup(file_name)

    def aspirate_from(self, volume, source):
        self.coordinator.aspirate_from(volume, source)
        self.amount_wanted = volume

    def dispense_to(self, volume, to):
        self.coordinator.dispense_to(volume, to)

    def open_lid(self):
        self.coordinator.open_lid()

    def close_lid(self):
        self.coordinator.close_lid()

    def deactivate_lid(self):
        self.coordinator.deactivate_lid()

    def deactivate_block(self):
        self.coordinator.deactivate_block()

    def set_temperature(self ,temp: float, hold_time:  float = None):
        self.coordinator.set_temperature(temp, hold_time)

    def set_lid_temp(self, temp: float):
        self.coordinator.set_lid_temp(temp)

    def set_block_temp(self, target_temp, holding_time_in_minutes):
        self.coordinator.set_block_temp(target_temp, holding_time_in_minutes)

    def set_tempdeck_temp(self, celcius, holding_time_in_minutes):
        self.coordinator.set_tempdeck_temp(celcius, holding_time_in_minutes)

    def deactivate_tempdeck(self):
        self.coordinator.deactivate_tempdeck()

    def deactivate_all(self):
        self.coordinator.deactivate_all()

    def end_of_protocol(self):
        self.coordinator.end_of_protocol()

    def void_plate_depth(self, plate: Plate, void: bool = False):
        self.coordinator.void_plate_depth(plate, void)

    def take_picture(self, source = None):
        if source != None:
            self.coordinator.go_to_position_to_take_picture(source)
        requests.post(WEB_ADDRESS, json=my_data)