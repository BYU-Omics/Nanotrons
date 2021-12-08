"""
PLATE CLASS
    This class serves the purpose of encapsulating each plate with its intuitive parameters such as pot locations,
    pot types, and nicknames. Pot is defined as the container that can hold a vial containing reagent.
    The indeces of each pot (in the pot_locations list) correspond to their geographical location on a rectangle 
    laying down on its long side, going from left to right on each row, and going row by row from top to bottom
"""

class Plate:
    # Plate can be either partially constructed with basic parameters (model and grid) and be calibrated/populated later or fully constructed with a dictionary of pre-recorded parameters
    def __init__(self, model_name = "default", grid = "default", plate_properties = None):
        # Normal initialization (no properties dictionary provided)
        if (plate_properties == None):
            self.model = model_name
            self.grid = grid
            amount_of_pots = grid[0] * grid[1]
            self.pot_locations = [ () for _ in range(amount_of_pots) ]
            self.pot_depths = [ 0 for _ in range(amount_of_pots) ] # This will say how deep is a pot
            self.nicknames = [ "" for _ in range(amount_of_pots) ] # Assigns a nickname to each well given their index
            self.nicknames_inv = {} # Maps the nicknames to a specific well index
            self.void_depth: bool = False 
        # If a plate is being created from a dictionary of pre-recorded parameters 
        else:
            self.import_plate_properties(plate_properties)
            self.void_depth: bool = False 

    # Stores the location of a specified pot
    def set_location(self, pot_index, location_tuple):
        self.pot_locations[pot_index] = location_tuple
    
    # Stores the nickname of a specified pot
    def set_nickname(self, pot_index, nickname):
        self.nicknames[pot_index] = nickname
        self.nicknames_inv[nickname] = pot_index

    # Gets the nickname stored for the specified pot
    def get_nickname(self, pot_index):
        return self.nicknames[pot_index]

    # Checks if a specified pot (by its nickname) exists in the Plate object
    def verify_nickname_existence(self, nickname):
        return nickname in self.nicknames

    # Stores the depth of the speficied pot
    def set_pot_depth(self, pot_index, pot_depth):
        self.pot_depths[pot_index] = pot_depth

    def void_plate_depth(self, void: bool = False):
        self.void_depth = void
        # print(f"Voiding depth for {self.get_model_name()}, self.void_depth = {self.void_depth}")


    # Gets the depth of the speficied pot 
    def get_pot_depth(self, pot_index):
        return self.pot_depths[pot_index]

    # Gets the grid arrangement speficied on initialization
    def get_grid(self):
        return self.grid
    
    # Returns the location of a given pot specified by its nickname    
    def get_location_by_nickname(self, pot_nickname):
        return self.pot_locations[self.nicknames_inv[pot_nickname]]

    def pot_position_for_protocol(self, pot_nickname):
        location = self.pot_locations[self.nicknames_inv[pot_nickname]]
        x = location[0]
        y = location[1]
        z = location[2]
        depth = self.get_pot_depth(0)
        location_with_depth = [x, y, z - depth]
        if self.void_depth:
            # print("Depth has been voided. Returning calibration point level.")
            return location
        else:
            # print(f"Depth for {self.get_model_name()} has not been voided. Going to the bottom of plate. ")
            return location_with_depth

    # Returns the location of a given pot specified by its index
    def get_location_by_index(self, pot_index):
        return self.pot_locations[pot_index]

    # Returns a string representation of all the attributes of the Plate object
    def to_string_plate(self):
        description = f"Model: {self.model}"
        description = description + f"Grid: {self.grid}\n"
        description = description + f"Pot Locations:\n {self.pot_locations}\n"
        description = description + f"Pot Depths:\n {self.pot_depths}\n"
        description = description + f"Nicknames:\n {self.nicknames}\n"

        return description

    # Returns the model stored during initialization of the object
    def get_model_name(self):
        return self.model

    # This method returns a dictionary with a collection of all the properties of the plate
        # Format:
        # plate_properties = {
        #     "model": "model_name", 
        #     "grid": [row, col],
        #     "pot_locations": [ (X1, Y1, Z1), (X2, Y2, Z2), ... , (Xn, Yn, Zn)],
        #     "pot_depths": [type_1, type_2, ..., type_n],
        #     "pot_nicknames": ["#1", "#2", ... , "#n"],
        # }
    def export_plate_properties(self):
        plate_properties = dict()

        plate_properties["model"] = self.model # Load model name
        plate_properties["grid"] = self.grid # Load grid
        plate_properties["pot_locations"] = self.pot_locations # Load well_locations
        plate_properties["pot_depths"] = self.pot_depths # Load well_types
        plate_properties["pot_nicknames"] = self.nicknames # Load well_nicknames

        return plate_properties

    # This method receives a dictionary with plate properties and fills up the internal variables of the instance of Plate with those
    def import_plate_properties(self, plate_properties):
        self.model = plate_properties["model"] # Load model name
        self.grid = plate_properties["grid"] # Load grid
        self.pot_locations = plate_properties["pot_locations"] # Load pot_locations
        self.pot_depths = plate_properties["pot_depths"] # Load pot_depths
        self.nicknames = plate_properties["pot_nicknames"] # Load pot_nicknames
        self.nicknames_inv = dict()
        for index in range(len(self.nicknames)):
            self.nicknames_inv[self.nicknames[index]] = index

