"""
LABWARE CLASS
    This class allows for labware (Chip and Plate) components management, like adding, deleting, and getting parameters
    from each of them.
"""

from models_manager import LABWARE_CHIP, LABWARE_PLATE
from chip import Chip
from plate import Plate
import sys

import os
import json

RELATIVE_PATH_L = "/saved_labware"
RELATIVE_PATH_W = "\\saved_labware"
LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
JSON_EXTENTION = '.json'

class Labware_class:
    def __init__(self):
        self.chip_list = []
        self.plate_list = []
        self.syringe_model = []

    """
    SETTERS SECTION
    """
    def add_chip(self, new_chip):
        # add new_chip to the list of chips
        self.chip_list.append(new_chip)

    def remove_chip(self, chip_index):
        print(f"Chips: {self.chip_list}")
        self.chip_list.pop(chip_index)


    def add_plate(self, new_plate):
        # add new_plate to the list of chips
        self.plate_list.append(new_plate)

    def remove_plate(self, plate_index):
        print(f"Plates: {self.plate_list}")
        self.plate_list.pop(plate_index)

    def reset_chip_list(self):
        print(f"Reseting the chips\n Chips: {self.chip_list}")
        self.chip_list.clear()
    
    def reset_plate_list(self):
        print(f"Reseting the plates\n Plates: {self.plate_list}")
        self.plate_list.clear()

    def set_syringe_model(self, model_name):
        self.syringe_model = model_name

    """
    GETTERS SECTION
    """
    def get_syringe_model(self):
        return self.syringe_model
    
    def get_chip_models(self):
        models = dict()
        for chip in self.chip_list:
            models[chip.get_model_name()] = chip.get_location_by_index(0)        
        return models
    
    def get_plate_models(self):
        # models = []
        # for plate in self.plate_list:
        #         models.append(plate.get_model_name())
        
        models = dict()
        for plate in self.plate_list:
            models[plate.get_model_name()] = plate.get_location_by_index(0)
        
        print(f"Models: {models}")#A TEST, DELETE
        return models

    def get_current_labware(self):
        labware = dict()
        labware["chips"] = self.get_chip_models()
        labware["plates"] = self.get_plate_models()
        labware["syringe"] = self.get_syringe_model()
        return labware

    def get_well_location(self, chip, well_nickname):
        location = self.chip_list[chip].get_location_by_nickname(well_nickname)
        return location

    def get_pot_location(self, plate, pot_nickname):
        location = self.plate_list[plate].get_location_by_nickname(pot_nickname)
        return location

    # String input looks like: "p 1E3" or "c 1B3" : "[component] [component_index][well/pot nickname]"
    def check_well_pot_existence(self, container):
        # Unpack variables from the input string
        component = container.split()[0]
        index = int(container.split()[1][0])
        nickname = container.split()[1][1:]

        # Verify existence of the container specified
        if component == LABWARE_CHIP:
            return self.chip_list[index].verify_nickname_existence(nickname)

        elif component == LABWARE_PLATE:
            return self.plate_list[index].verify_nickname_existence(nickname)

    """
    SAVE/LOAD LABWARE 
        This section either saves/loads Chip and Plate objects to/from a dictionary
        The format of the dictionary is the following:

        labware_dictionary = {
            "chips": [
                {
                    # Properties of Chip #1
                },
                {
                    # Properties of Chip #2
                },
                ...
                {
                    # Properties of Chip #n
                }
            ],
            "plates: [
                {
                    # Properties of Plate #1
                },
                {
                    # Properties of Plate #2
                },
                ...
                {
                    # Properties of Plate #n
                }
            ]
        }

        chip_properties = {
            "model": "model_name", 
            "grid": [row, col],
            "well_locations": [ (X1, Y1, Z1), (X2, Y2, Z2), ... , (Xn, Yn, Zn)],
            "well_types": [type_1, type_2, ..., type_n],
            "well_nicknames": ["#1", "#2", ... , "#n"],
        }

        plate_properties = {
            "model": "model_name", 
            "grid": [row, col],
            "pot_locations": [ (X1, Y1, Z1), (X2, Y2, Z2), ... , (Xn, Yn, Zn)],
            "pot_depths": [type_1, type_2, ..., type_n],
            "pot_nicknames": ["#1", "#2", ... , "#n"],
        }
    """
    # This method parses the list of chips and plates and outputs a dictionary with all the parameters of all the labware components
    def labware_to_dictionary(self):
        labware_dictionary = dict()
        labware_dictionary["chips"] = list()
        labware_dictionary["plates"] = list()

        # Iterate through chips list, extract properties of each chip, and store in labware_dictionary
        for chip in self.chip_list:
            chip_properties = chip.export_chip_properties()
            labware_dictionary["chips"].append(chip_properties)

        # Iterate through plates list, extract properties of each plate, and store in labware_dictionary
        for plate in self.plate_list:
            plate_properties = plate.export_plate_properties()
            labware_dictionary["plates"].append(plate_properties)
        return labware_dictionary

    def dictionary_to_labware(self, labware_dictionary):        
        chips_list = labware_dictionary["chips"] # This is a list of dictionaries, each of which containes prooperties for a given chip
        plates_list = labware_dictionary["plates"] # This is a list of dictionaries, each of which containes prooperties for a given plate
        # Iterate through chips_list and create a Chip object out of each dictionary
        for chip_properties in chips_list:
            new_chip = Chip(chip_properties=chip_properties)
            self.chip_list.append(new_chip)

        # Iterate through plates_list and create a Plate object out of each dictionary
        for plate_properties in plates_list:
            new_plate = Plate(plate_properties=plate_properties)
            self.plate_list.append(new_plate)
            
    def get_path_to_saved_labware_folder(self):
        current_path = os.getcwd() # Returns a string representing the location of this file
        if os.name == LINUX_OS:
            path_of_interest = current_path + RELATIVE_PATH_L # Joins the current location with the name of the folder thhat contains all the saved labware setup files
        elif os.name == WINDOWS_OS:
            path_of_interest = current_path + RELATIVE_PATH_W
        return path_of_interest

    def save_labware_to_file(self, file_name):
        # Path
        folder_path = self.get_path_to_saved_labware_folder()
        file_path = os.path.join(folder_path, file_name + JSON_EXTENTION) # Add the name of the file of interest to that path string

        # Create a json file
        output_file = open(file_path, "w")

        # Create a dictionary out of the current labware 
        labware_dictionary = self.labware_to_dictionary()

        # Dump the labware dictionary into the json file
        json.dump(labware_dictionary, output_file)

    def load_labware_from_file(self, file_name):
        # Path
        folder_path = self.get_path_to_saved_labware_folder()
        file_path = os.path.join(folder_path, file_name) # Add the name of the file of interest to that path string
        # Open an existing json file
        input_file = open(file_path, "r")

        # Create a dictionary out of the data in the specified json file
        labware_dictionary = json.load(input_file)

        # Create labware out of the dictionary
        self.dictionary_to_labware(labware_dictionary)

        chip_number = 0
        plate_number = 0

        for key in labware_dictionary:
            if key == 'chip':
                chip_number += 1
            elif key == 'plate':
                plate_number += 1
        
    def available_saved_labware_files(self):
        path = os.listdir(self.get_path_to_saved_labware_folder())
        return path

