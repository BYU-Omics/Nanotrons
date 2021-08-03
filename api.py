"""
This class is the interface between the user writing a simple protocol and the coordinator. This is just
a smalled coordinator that does not know about all the other functions and what they do step by step. It limits
the user to write only neccessary commands to perform protocols. 
"""
from coordinator import *
import sys

LABWARE = sys.argv[1]
# If we're not in the top level
# And we're trying to call the file directly
# add the submodules to $PATH
# sys.path[0] is the current file's path
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')

PLATE_DEPTH = "Plate's depth"

class Api:
    def __init__(self):
        self.coordinator = Coordinator()
        self.current_labware_depth = None

    def adjust_syringe(self, position):
        self.coordinator.adjust_syringe(position)

    def load_labware_setup(self, file_name):
        return self.coordinator.load_labware_setup(file_name)

    def aspirate_from(self, amount, source):
        self.coordinator.aspirate_from(amount, source, self.current_labware_depth)

    def dispense_to(self, amount, to):
        self.coordinator.dispense_to(amount, to, self.current_labware_depth)

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
        self.coordinator.go_to_deck_slot('12')
        self.coordinator.disconnect_all()

    def set_plate_depth(self, plate: Plate, depth = PLATE_DEPTH):
        self.current_labware_depth = self.coordinator.set_plate_depth(plate, depth)

