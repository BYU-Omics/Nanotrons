"""
LABWARE CLASS
    This class allows for labware (Chip and Plate) components management, like adding, deleting, and getting parameters
    from each of them.
"""

from numpy import False_
from models_manager import LABWARE_CHIP, LABWARE_PLATE
# from model import Model
from model import Model
import sys

import os
import json

RELATIVE_PATH_L = "/saved_labware"
RELATIVE_PATH_W = "\\saved_labware"
RELATIVE_PATH_L1 = "/models/syringes"
RELATIVE_PATH_W1 = "\\models\\syringes"
LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
JSON_EXTENTION = '.json'
SYRINGE_MODEL = "HAMILTON_FAKE.json"

class Labware_class:
    def __init__(self):
        self.model_list = []
        self.syringe_model = SYRINGE_MODEL
        self.syringe_model_is_default = True

    """
    SETTERS SECTION
    """
    def add_model(self, new_model):
        # add new_plate to the list of chips
        self.model_list.append(new_model)

    def remove_model(self, model_index):
        # print(f"Plates: {self.plate_list}")
        self.model_list.pop(model_index)
    
    def reset_model_list(self):
        # print(f"Reseting the plates\n Plates: {self.plate_list}")
        self.model_list.clear()

    def set_syringe_model(self, model_name):
        self.syringe_model = model_name
        self.syringe_model_is_default = False

    """
    GETTERS SECTION
    """
    def get_syringe_model(self):
        return self.syringe_model
    
    def get_models(self):
        models = dict()
        for model in self.model_list:
            models[model.get_model_name()] = model.get_location_by_index(0)
        return models

    def get_current_labware(self):
        labware = dict()
        labware["models"] = self.get_models()
        labware["syringe"] = self.get_syringe_model()
        return labware

    def get_well_location(self, model, well_nickname):
        location = self.model_list[model].get_location_by_nickname(well_nickname)
        return location

    # String input looks like: "p 1E3" or "c 1B3" : "[component] [component_index][well/pot nickname]"
    def check_well_existence(self, container):
        # Unpack variables from the input string
        component = container.split()[0]
        index = int(container.split()[1][0])
        nickname = container.split()[1][1:]

        # Verify existence of the container specified
        if component == (LABWARE_CHIP or LABWARE_PLATE):
            return self.model_list[index].verify_nickname_existence(nickname)

    # This method parses the list of chips and plates and outputs a dictionary with all the parameters of all the labware components
    def labware_to_dictionary(self):
        labware_dictionary = dict()
        labware_dictionary["models"] = list()

        # Iterate through plates list, extract properties of each plate, and store in labware_dictionary
        if len(self.model_list) >0:
            for model in self.model_list:
                model_properties = model.export_model_properties()
                labware_dictionary["models"].append(model_properties)
        return labware_dictionary

    def dictionary_to_labware(self, labware_dictionary):        
        model_list = labware_dictionary["models"] # This is a list of dictionaries, each of which containes properties for a given model

        # Iterate through model_list and create a model object out of each dictionary
        for model_properties in model_list:
            new_model = Model(model_properties=model_properties)
            self.model_list.append(new_model)
            
    def get_path_to_saved_labware_folder(self):
        current_path = os.getcwd() # Returns a string representing the location of this file
        if os.name == LINUX_OS:
            path_of_interest = current_path + RELATIVE_PATH_L # Joins the current location with the name of the folder thhat contains all the saved labware setup files
        elif os.name == WINDOWS_OS:
            path_of_interest = current_path + RELATIVE_PATH_W
        return path_of_interest

    def get_path_to_saved_syringe_folder(self):
        current_path = os.getcwd() # Returns a string representing the location of this file
        if os.name == LINUX_OS:
            path_of_interest = current_path + RELATIVE_PATH_L1 # Joins the current location with the name of the folder thhat contains all the saved labware setup files
        elif os.name == WINDOWS_OS:
            path_of_interest = current_path + RELATIVE_PATH_W1
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

        model_number = 0

        for key in labware_dictionary:
            if key == 'models':
                model_number += 1
        
    def available_saved_labware_files(self):
        path = os.listdir(self.get_path_to_saved_labware_folder())
        return path

    def available_saved_syringe_files(self):
        path = os.listdir(self.get_path_to_saved_syringe_folder())
        return path

