"""
CHAMBER CONFIGURER CLASS
    This class implements the functionalities needed to receive the configurations
    of a Chamber object from the user and export them to a JSON file. This file will
    be used to specify the properties of all the Chip and Plate objects to create the 
    Chamber object
"""

import json

class LabwareCreator:
    def __init__(self):
        self.chamber_configuration = { "chips": [], "plates": [] }

    def add_chip_configuration(self, grid, point_distance, well_distance, row_types, nicknames):
        properties_object = { 
            "grid":grid, # This is a list: [rows,columns]
            "pointDistance": point_distance, # float number
            "wellDistance": well_distance, # float number
            "rowTypes":row_types, # list of strings: ["BS","B", "BS"]
            "nicknames":nicknames # List of lists with strings in them, each sublist holds the nicknames of a row
        }
        self.chamber_configuration["chips"].append(properties_object)
    
    def add_plate_configuration(self, grid, pot_distance_x, pot_distance_y, pot_depth, nicknames):
        properties_object = {
            "grid":grid, # This is a list: [rows,columns]
            "potDistance X":pot_distance_x, # float number
            "potDistance Y":pot_distance_y, # float number
            "potDepth":pot_depth, # float number or list, to specify a common or specific depth accorss all pots respectively
            "nicknames":nicknames # List of lists with strings in them, each sublist holds the nicknames of a row
        }
        self.chamber_configuration["plates"].append(properties_object)

    def reset_configurations(self):
        self.chamber_configuration = { "chips": [], "plates": [] }

    def export_configurations(self, file_name):
        if file_name[-5:] != ".json":
            file_name = file_name + ".json"
        json_file = open(file_name, "w")
        json.dump(self.chamber_configuration, json_file)
        print(f"Configurations succesfully exported to {file_name}")

