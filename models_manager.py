"""
MODELS MANAGER CLASS
    The purpose of this class is to keep an accurate list of available models for both chips and plates to deliver to the system when needing to 
    select a model to calibrate. It does so by accessing the file path to each category of components (chips, plates, and syringes)
"""
import os
import json

LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LABWARE_SYRINGE = "s"

RELATIVE_PATH_TO_CHIPS_W = "\\models\\chips"
RELATIVE_PATH_TO_PLATES_W = "\\models\\plates"
RELATIVE_PATH_TO_SYRINGES_W = "\\models\\syringes"

RELATIVE_PATH_TO_CHIPS_R = "/models/chips"
RELATIVE_PATH_TO_PLATES_R = "/models/plates"
RELATIVE_PATH_TO_SYRINGES_R = "/models/syringes"

class ModelsManager:
    def __init__(self, operating_system):
        self.operating_system = operating_system # Either "w" or "r" for windows and raspberry os
        self.models = dict() # Disctionary with 2 keys: "chips" and "plates", each of which has a list of models
    
    # This returns a path to the folder that contains the model files of the specified component type
    def get_path(self, component_type):
        current_path = os.getcwd() # returns the current directory (where this file is stored) ---------> MIGHT BE PROBLEMATIC if this class is imported and run on a different path, will this return the path of the file that called this module or will it return the path of this file?
        relative_path = "" # relative path with respect to the path where this file is contained
        if (component_type == LABWARE_CHIP):
            if (self.operating_system == "w"):
                relative_path = RELATIVE_PATH_TO_CHIPS_W
            elif (self.operating_system == "r"):
                relative_path = RELATIVE_PATH_TO_CHIPS_R

        elif (component_type == LABWARE_PLATE):
            if (self.operating_system == "w"):
                relative_path = RELATIVE_PATH_TO_PLATES_W
            elif (self.operating_system == "r"):
                relative_path = RELATIVE_PATH_TO_PLATES_R

        elif (component_type == LABWARE_SYRINGE):
            if (self.operating_system == "w"):
                relative_path = RELATIVE_PATH_TO_SYRINGES_W
            elif (self.operating_system == "r"):
                relative_path = RELATIVE_PATH_TO_SYRINGES_R
        path_of_interest = current_path + relative_path
        return path_of_interest

    # Returns the list of models for chips
    def get_component_models(self, component_type):
        component_models = list() # Create an empty list to store the names of each file
        path_of_interest = self.get_path(component_type) # This command gets the path to the chips folder
        component_models = [f.split(".")[0] for f in os.listdir(path_of_interest) if os.path.isfile(os.path.join(path_of_interest, f))] # This returns a list of all the files in the path_of_interest
            
        return component_models

    # Every time it returns the most recent list of models
    def get_stored_models(self):
        self.models["chips"] = self.get_component_models(LABWARE_CHIP)
        self.models["plates"] = self.get_component_models(LABWARE_PLATE)
        self.models["syringes"] = self.get_component_models(LABWARE_SYRINGE)
        return self.models

    # This returns the parameters (contents of a file) of the specified model as a dictionary
        # Arguments: "c" (for chip), "p" (for plate), "s" (for syringe)
    def get_model_parameters(self, component_type, component_model):
        path_to_models_folder = self.get_path(component_type)
        file_path = ""

        if (self.operating_system == "w"):
            print(f"Component model: {component_model}")
            file_path = open(path_to_models_folder + "\\" + str(component_model).strip("[]'") + ".json")

        elif (self.operating_system == "r"):
            file_path = open(path_to_models_folder + "/" + str(component_model).strip("[]'") + ".json")
        
        parameters = json.load(file_path)

        return parameters

    def save_new_model_file(self, component_type, new_model_name, properties):
        path_to_type = self.get_path(component_type)
        output_file = ""

        if (self.operating_system == "w"):
            output_file = open(path_to_type + "\\" + new_model_name + ".json", "w")
        
        elif (self.operating_system == "r"):
            output_file = open(path_to_type + "/" + new_model_name + ".json", "w")
        
        json.dump(properties, output_file)

    def create_chip_model(self, new_model_name, grid, point_distance, well_distance, row_types, nicknames):
        properties = { 
            "grid": grid, # This is a list: [rows,columns]
            "pointDistance": point_distance, # float number
            "wellDistance": well_distance, # float number
            "rowTypes": row_types, # list of strings: ["BS","B", "BS"]
            "nicknames": nicknames # List of lists with strings in them, each sublist holds the nicknames of a row
        }
        self.save_new_model_file(LABWARE_CHIP, new_model_name, properties)

    def create_plate_model(self, new_model_name, grid, pot_distance_r, pot_distance_c, pot_depth, nicknames):
        properties = {
            "grid": grid, # This is a list: [rows,columns]
            "potDistance_r": pot_distance_r, # float number
            "potDistance_c": pot_distance_c, # float number
            "potDepth": pot_depth, # float number or list, to specify a common or specific depth accorss all pots respectively
            "nicknames": nicknames # List of lists with strings in them, each sublist holds the nicknames of a row
        }
        self.save_new_model_file(LABWARE_PLATE, new_model_name, properties)

    def create_syringe_model(self, new_model_name, volume, inner_diameter):
        properties = {
            "volume": volume, # float number
            "inner_diameter": inner_diameter, # float number
        }
        self.save_new_model_file(LABWARE_SYRINGE, new_model_name, properties)     
        

if __name__ == "__main__":
    myModelManager = ModelsManager("w")
    myModels = myModelManager.get_stored_models()
    print(f"myModels: {myModels}")
    example_parameters = myModelManager.get_model_parameters(LABWARE_CHIP,"SZ001")
    print(f"Example Model: {example_parameters}")
    row_types = example_parameters["rowTypes"]
    print(f"Parsing through parameters. Example: rowTypes = {row_types}")
