"""
This class is the interface between the user writing a simple protocol and the coordinator. This is just
a smalled coordinator that does not know about all the other functions and what they do step by step. It limits
the user to write only neccessary commands to perform protocols. 
"""
from coordinator import *
import sys
import requests

# If we're not in the top level
# And we're trying to call the file directly
# add the submodules to $PATH
# sys.path[0] is the current file's path
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')
WEB_ADDRESS = 'http://localhost:5000/'

class Api:
    def __init__(self):
        self.coordinator = Coordinator()
        self.current_labware_depth = None
        self.folder_for_this_protocol = 'default_folder'
        self.protocol_flags = {'take_pic': 'True', 'folder': 'Protocol Pictures', 'protocol_folder': f'{self.folder_for_this_protocol}'}

    def set_washing_positions(self, clean_water, wash_water, waste_water):
        self.coordinator.set_washing_positions(clean_water, wash_water, waste_water)

    def set_syringe_model(self, model_name):
        self.coordinator.myLabware.set_syringe_model(model_name)

    def start_wash(self):
        self.coordinator.start_wash()

    def mid_wash(self, left_over = STANDARD_LEFT_OVER, cushion_1 = STANDARD_CUSHION_1, cushion_2 = STANDARD_CUSHION_2):
        self.coordinator.mid_wash(left_over, cushion_1, cushion_2)

    def air_gap(self):
        self.coordinator.air_gap()

    def load_labware_setup(self, file_name):
        return self.coordinator.load_labware_setup(file_name)

    def aspirate_from(self, volume, source):
        self.coordinator.aspirate_from(volume, source)
        self.amount_wanted = volume

    def dispense_to(self, volume, to):
        self.coordinator.set_amount_wanted(volume)
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
        print(f"Sending {self.protocol_flags['protocol_folder']} folder to webapp")
        requests.post(WEB_ADDRESS, json=self.protocol_flags)

    def set_pictures_folder(self,  folder: str = 'protocol_pics'):
        print(f"API: Folder for pics set to: {folder} ")
        self.protocol_flags["protocol_folder"] = self.folder_for_this_protocol = folder