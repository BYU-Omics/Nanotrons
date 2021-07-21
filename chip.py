"""
CHIP CLASS
    This class serves the purpose of encapsulating each chip with its intuitive parameters such as well locations,
    well types, and nicknames.
    The indeces of each well (in the well_locations list) correspond to their geographical location on a rectangle 
    laying down on its long side, going from left to right on each row, and going row by row from top to bottom
"""

class Chip:
    # Chip can be either partially constructed with basic parameters (model and grid) and be calibrated/populated later or fully constructed with a dictionary of pre-recorded parameters
    def __init__(self, model_name = "default", grid = "default", chip_properties = None):
        # Normal initialization (no properties dictionary provided)
        if (chip_properties == None):
            self.model = model_name
            self.grid = grid
            amount_of_wells = grid[0] * grid[1]
            self.well_locations = [ list() for _ in range(amount_of_wells) ]
            self.well_types = [ "" for _ in range(amount_of_wells) ] # This will say wether the well of the given index is big or small 
            self.nicknames = [ "" for _ in range(amount_of_wells) ] # Assigns a nickname to each well given their index
            self.nicknames_inv = {} # Maps the nicknames to a specific well index (revrese mapping)
        
        # If a chip is being created from a dictionary of pre-recorded parameters 
        else:
            self.import_chip_properties(chip_properties)

    # Stores the location of a specified well
    def set_location(self, well_index, location_tuple):
        self.well_locations[well_index] = location_tuple
    
    # Stores the nickname of a specified well
    def set_nickname(self, well_index, nickname):
        self.nicknames[well_index] = nickname
        self.nicknames_inv[nickname] = well_index

    # Gets the nickname stored for the specified well
    def get_nickname(self, well_index):
        return self.nicknames[well_index]

    # Checks if a specified well (by its nickname) exists in the Chip object
    def verify_nickname_existence(self, nickname):
        return nickname in self.nicknames

    # Stores what type of well the speficied well is (big or small)
    def set_well_type(self, well_index, well_type):
        self.well_types[well_index] = well_type

    # Gets the size of the speficied well 
    def get_well_type(self, well_index):
        return self.well_types[well_index]

    # Gets the grid arrangement speficied on initialization
    def get_grid(self):
        return self.grid
    
    # Returns the location of a given well specified by its nickname
    def get_location_by_nickname(self, well_nickname):
        return self.well_locations[self.nicknames_inv[well_nickname]]

    # Returns the location of a given well specified by its index
    def get_location_by_index(self, well_index):
        return self.well_locations[well_index]

    # Returns a string representation of all the attributes of the Chip object
    def to_string_chip(self):
        description = f"Model: {self.model}"
        description = description + f"Grid: {self.grid}\n"
        description = description + f"Well Locations:\n {self.well_locations}\n"
        description = description + f"Well Types:\n {self.well_types}\n"
        description = description + f"Nicknames:\n {self.nicknames}\n"

        return description

    # Returns the model stored during initialization of the object
    def get_model_name(self):
        return self.model

    # This method returns a dictionary with a collection of all the properties of the chip
        # Format:
        # chip_properties = {
        #     "model": # model #, 
        #     "grid": [row, col],
        #     "well_locations": [ (X1, Y1, Z1), (X2, Y2, Z2), ... , (Xn, Yn, Zn)],
        #     "well_types": [type_1, type_2, ..., type_n],
        #     "well_nicknames": ["#1", "#2", ... , "#n"],
        # }
    def export_chip_properties(self):
        chip_properties = dict()

        chip_properties["model"] = self.model # Load model name
        chip_properties["grid"] = self.grid # Load grid
        chip_properties["well_locations"] = self.well_locations # Load well_locations
        chip_properties["well_types"] = self.well_types # Load well_types
        chip_properties["well_nicknames"] = self.nicknames # Load well_nicknames

        return chip_properties

    # This method receives a dictionary with chip properties and fills up the internal variables of the instance of Chip with those
    def import_chip_properties(self, chip_properties):
        self.model = chip_properties["model"] # Load model name
        self.grid = chip_properties["grid"] # Load grid
        self.well_locations = chip_properties["well_locations"] # Load well_locations
        self.well_types = chip_properties["well_types"] # Load well_types
        self.nicknames = chip_properties["well_nicknames"] # Load well_nicknames
        self.nicknames_inv = dict()
        for index in range(len(self.nicknames)):
            self.nicknames_inv[self.nicknames[index]] = index

