"""
MODEL CLASS
    This class serves the purpose of encapsulating each plate with its intuitive parameters such as pot locations,
    pot types, and nicknames. Pot is defined as the container that can hold a vial containing reagent.
    The indeces of each pot (in the pot_locations list) correspond to their geographical location on a rectangle 
    laying down on its long side, going from left to right on each row, and going row by row from top to bottom
"""

class Model:
    # Plate can be either partially constructed with basic parameters (model and grid) and be calibrated/populated later or fully constructed with a dictionary of pre-recorded parameters
    def __init__(self, model_name = "default", grid = "default", model_properties = None):
        # Normal initialization (no properties dictionary provided)
        if (model_properties == None):
            self.model = model_name
            self.grid = grid
            self.offset = 0
            amount_of_wells = grid[0] * grid[1]
            self.well_locations = [ () for _ in range(amount_of_wells) ]
            self.well_depths = [ 0 for _ in range(amount_of_wells) ] # This will say how deep is a pot
            self.nicknames = [ "" for _ in range(amount_of_wells) ] # Assigns a nickname to each well given their index
            self.nicknames_inv = {} # Maps the nicknames to a specific well index
            self.void_depth: bool = False 
        # If a plate is being created from a dictionary of pre-recorded parameters 
        else:
            self.import_model_properties(model_properties)
            self.void_depth: bool = False 

    # Stores the location of a specified pot
    def set_location(self, well_index, location_tuple):
        self.well_locations[well_index] = location_tuple
    
    # Stores the nickname of a specified pot
    def set_nickname(self, well_index, nickname):
        self.nicknames[well_index] = nickname
        self.nicknames_inv[nickname] = well_index

    # Gets the nickname stored for the specified pot
    def get_nickname(self, well_index):
        return self.nicknames[well_index]

    # Checks if a specified pot (by its nickname) exists in the Plate object
    def verify_nickname_existence(self, nickname):
        return nickname in self.nicknames

    # Stores the depth of the speficied pot
    def set_well_depth(self, well_index, well_depth):
        self.well_depths[well_index] = well_depth

    def void_model_depth(self, void: bool = False):
        self.void_depth = void


    # Gets the depth of the speficied pot 
    def get_well_depth(self, well_index):
        return self.well_depths[well_index]

    # Gets the grid arrangement speficied on initialization
    def get_grid(self):
        return self.grid
    
    # Returns the location of a given pot specified by its nickname    
    def get_location_by_nickname(self, well_nickname):
        return self.well_locations[self.nicknames_inv[well_nickname]]

    def well_position_for_protocol(self, well_nickname):
        location = self.well_locations[self.nicknames_inv[well_nickname]]
        x = location[0]
        y = location[1]
        z = location[2]
        depth = self.get_well_depth(0)
        location_with_depth = [x, y, z - depth]
        if self.void_depth:
            # print("Depth has been voided. Returning calibration point level.")
            return location
        else:
            # print(f"Depth for {self.get_model_name()} has not been voided. Going to the bottom of plate. ")
            return location_with_depth

    # Returns the location of a given pot specified by its index
    def get_location_by_index(self, well_index):
        return self.well_locations[well_index]

    # Returns a string representation of all the attributes of the Plate object
    def to_string_plate(self):
        description = f"Model: {self.model}"
        description = description + f"Grid: {self.grid}\n"
        description = description + f"Pot Locations:\n {self.well_locations}\n"
        description = description + f"Pot Depths:\n {self.well_depths}\n"
        description = description + f"Nicknames:\n {self.nicknames}\n"

        return description

    # Returns the model stored during initialization of the object
    def get_model_name(self):
        return self.model

    def export_model_properties(self):
        model_properties = dict()

        model_properties["model"] = self.model # Load model name
        model_properties["grid"] = self.grid # Load grid
        model_properties["well_locations"] = self.well_locations # Load well_locations
        model_properties["well_depths"] = self.well_depths # Load well_types
        model_properties["well_nicknames"] = self.nicknames # Load well_nicknames
        model_properties["offset"] = self.offset

        return model_properties

    # This method receives a dictionary with plate properties and fills up the internal variables of the instance of Plate with those
    def import_model_properties(self, model_properties):
        self.model = model_properties["model"] # Load model name
        self.grid = model_properties["grid"] # Load grid
        self.well_locations = model_properties["well_locations"] # Load pot_locations
        self.well_depths = model_properties["well_depths"] # Load pot_depths
        self.nicknames = model_properties["well_nicknames"] # Load pot_nicknames
        self.offset = model_properties["offset"]
        self.nicknames_inv = dict()
        for index in range(len(self.nicknames)):
            self.nicknames_inv[self.nicknames[index]] = index

