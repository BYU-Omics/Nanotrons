"""
CALIBRATION MODULE
    This module defines standard methods that help in the calibration of Chip and Plate objects
"""

import numpy as np
from chip import Chip
from plate import Plate

CALIBRATION_POINTS = 3
SMALL_WELL = "S"
BIG_WELL = "B"

"""
SHARED CALIBRATION METHODS
"""
# Calculate the unit vector of a vector
def unit_vector(vector):
    magnitude = np.linalg.norm(vector)
    return vector/magnitude

# This method receives three calibration points and guesses the fourth (fourth corner of the Chip/Plate component)
def guess_fourth_calibration_point(calibration_points):
    ordered_calibration_points = reorder_calibration_points(calibration_points) # The three calibration points need to be in the right order or the contructor vectors won't be set properly

    # Constructor vectors
    vector_a = np.array(ordered_calibration_points[1]) - np.array(ordered_calibration_points[0])
    vector_b = np.array(ordered_calibration_points[2]) - np.array(ordered_calibration_points[0])

    # Vector arithmetic
    vector_c = vector_a + vector_b

    # Calculate 4th point
    fourth_calibration_point = np.array(ordered_calibration_points[0]) + vector_c
    # print(f"4th calibration point guessed: ({fourth_calibration_point[0]}, {fourth_calibration_point[1]}, {fourth_calibration_point[2]})")
    # print(fourth_calibration_point)
    return fourth_calibration_point

# This method receives a list of three points in space (a list) and reorders them to be understandable for the system
    # DESIRED ORDER (as if a rectangle of callibration points were laying on the long side as the base):
    # i. Top left callibration point
    # ii. Top right callibration point
    # iii. Bottom left callibration point
    # NOTE: the order of the points matters both for guessing the 4th calibration point right and for creating the plane for mapping out the wells/pots in a grid
def reorder_calibration_points(calibration_points):
    magnitudes = []
    ordered_points = []
    # Create points
    a = np.array(calibration_points[0])
    b = np.array(calibration_points[1])
    c = np.array(calibration_points[2])
    # Create vectors. Formatted in tuples: (point1, point2, vector_numpy_array)
    v0 = (a,b,b - a)
    v1 = (b,c,c - b)
    v2 = (a,c,c - a)
    vectors = [v0,v1,v2]
    # Vertex point: index corresponds to the vector number, the value at that index is the point that is not part of the vector
    vertices = [c, a, b]

    for vector in range(CALIBRATION_POINTS):
        magnitude = np.linalg.norm(vectors[vector][2])
        magnitudes.append(magnitude)
    
    index_max = magnitudes.index(max(magnitudes)) # Finds the index of the vector that connects the diagonal (it will have the max magnitude)
    vectors.pop(index_max) # We get rid of the vector that makes the diagonal
    magnitudes.pop(index_max)
    reference_point = vertices[index_max] # This is the point that is not included in the diagonal vector (numpy array)
    vertices.pop(index_max)

    index_max = magnitudes.index(max(magnitudes)) # Find the index of the vector that makes the long side of the rectangle
    vector_points = [ vectors[index_max][0], vectors[index_max][1] ] # Points that make the long side of the rectangle
    ordered_points.append(list(reference_point)) # Append to the return value the first element (vertice of the three points)
    # Append to the return value the second element (second point in the long side vector)
    if list(vector_points[0]) != list(reference_point):
        ordered_points.append(list(vector_points[0]))
    else:
        ordered_points.append(list(vector_points[1]))

    # Append to the return value the third element (point not involved in the long side vector)
    ordered_points.append(list(vertices[index_max]))

    return ordered_points

# This method returns all the nicknames as a continuous single list from a list of lists
def get_nicknames(nicknames_list):
    single_list = []
    for index in range(len(nicknames_list)):
        single_list = single_list + nicknames_list[index]

    return single_list

"""
CHIP CALIBRATION METHODS
"""
# This method takes the parameters of the chip plus its calibration points and returns a list of the locations of all the wells in that chip
def map_out_wells(chip_parameters, calibration_points):
    ordered_calibration_points = reorder_calibration_points(calibration_points) # The three calibration points need to be in the right order or the contructor vectors won't be set properly
    # Extract useful information from chip_parameters
    grid = chip_parameters["grid"]
    point_distance = chip_parameters["pointDistance"]
    well_distance = chip_parameters["wellDistance"]

    locations = [] # This is the list of tuples with the locations of all the wells in a chip, that will be returned: [ (x,y,z), ...]
    
    # Define points
    point_a = np.array(ordered_calibration_points[0]) # This point will be the reference for all vectors and displacements
    point_b = np.array(ordered_calibration_points[1])
    point_c = np.array(ordered_calibration_points[2])

    # Define vectors 
    v1 = point_b - point_a
    v2 = point_c - point_a

    # Define unit vectors
    u1 = unit_vector(v1) # Horizontal unit vector
    u2 = unit_vector(v2) # Vertical unit vector

    # Initial horizontal offset
    d = point_distance

    # Go through each row and column, create locations, and append them to the locations list
        # NOTE: the order in which they are stored is row by row from left to right, using an imaginary
        # rectangular table laying down on its long side
    for row in range(grid[0]):
        for column in range(grid[1]):
            displacement = u1 * (d + column * well_distance) + u2 * (row * well_distance) # Formula for spanning a plane with two vectors and an initial displacement
            new_location = point_a + displacement # Calculated location of the new well
            x,y,z = new_location # Unpack locations from the numpy array
            array_location = [x, y, z]
            new_tuple = (x,y,z) # Pack locations in appropriate format
            # locations.append(new_tuple)
            locations.append(array_location)
    # print("Calibration Points")
    # print(ordered_calibration_points)
    
    # print("Mapped Locations")
    # print(locations)
    return locations#locations

# This method is provided a grid and row_types and returns a list with the type of well that corresponds to each index
def get_well_types(grid, row_types):
    # Calculate the amount of wells that will be considered
    amount_of_wells = grid[0] * grid[1]
    list_of_well_types = [ None for _ in range(amount_of_wells)]
    well_index = 0

    for row in range(grid[0]):
        row_type = row_types[row]
        for column in range(grid[1]):
            if row_type == "BS":
                if column % 2 == 0:
                    list_of_well_types[well_index] = BIG_WELL
                else:
                    list_of_well_types[well_index] = SMALL_WELL
            elif row_type == "B":
                list_of_well_types[well_index] = BIG_WELL
            elif row_type == "S":
                list_of_well_types[well_index] = SMALL_WELL
            well_index = well_index + 1 

    return list_of_well_types

# This method creates a Chip object and sets all the pertinent parameters to it from the provided chip_parameters data and well_locations
def create_chip(model_name, chip_parameters, well_locations):

    # Unpack parameters to be used
    grid = chip_parameters["grid"]
    well_types = get_well_types(grid, chip_parameters["rowTypes"])
    nicknames = get_nicknames(chip_parameters["nicknames"])

    # Calculate the amount of wells that will be considered
    amount_of_wells = grid[0] * grid[1]

    # Create Chip object
    new_chip = Chip(model_name=model_name, grid=grid)

    # Store the locations, nicknames, and well types of the wells in the chip
    for index in range(amount_of_wells):
        new_chip.set_location(index, well_locations[index])
        new_chip.set_nickname(index, nicknames[index])
        new_chip.set_well_type(index, well_types[index])

    return new_chip

"""
PLATE CALIBRATION METHODS
"""
# This method takes the parameters of the plate plus its calibration points and returns a list of the locations of all the pots in that plate
def map_out_pots(plate_parameters, calibration_points):
    ordered_calibration_points = reorder_calibration_points(calibration_points) # The three calibration points need to be in the right order or the contructor vectors won't be set properly
    
    # Extract useful information from chip_parameters
    grid = plate_parameters["grid"]
    pot_distance_r = plate_parameters["potDistance_r"]
    pot_distance_c = plate_parameters["potDistance_c"]

    locations = [] # This is the list of tuples with the locations of all the wells in a chip, that will be returned: [ (x,y,z), ...]
    
    # Define points
    point_a = np.array(ordered_calibration_points[0]) # This point will be the reference for all vectors and displacements
    point_b = np.array(ordered_calibration_points[1])
    point_c = np.array(ordered_calibration_points[2])

    # Define vectors 
    v1 = point_b - point_a
    v2 = point_c - point_a

    # Define unit vectors
    u1 = unit_vector(v1)
    u2 = unit_vector(v2)

    # Go through each row and column, create locations, and append them to the locations list
        # NOTE: the order in which they are stored is row by row from left to right, using an imaginary
        # rectangular table laying down on its long side
    for row in range(grid[0]):
        for column in range(grid[1]):
            displacement = u1 * (column * pot_distance_c) + u2 * (row * pot_distance_r) # Formula for spanning a plane with two vectors and an initial displacement
            new_location = point_a + displacement # Calculated location of the new well
            x,y,z = new_location # Unpack locations from the numpy array
            new_tuple = (x,y,z) # Pack locations in appropriate format
            locations.append(new_tuple)

    # print(f"locations of the plate: {locations}")
    return locations

def create_plate(model_name, plate_parameters, pot_locations):

    # Unpack parameters to be used
    grid = plate_parameters["grid"]
    # Calculate the amount of pots that will be considered
    amount_of_pots = grid[0] * grid[1]
    pot_depth = 0

    # The depths of the pots can be either all the same or different for each
    if type(plate_parameters["potDepth"]) == list:
        pot_depth = plate_parameters["potDepth"]
    else:
        pot_depth = [plate_parameters["potDepth"] for _ in range(amount_of_pots)]
    nicknames = get_nicknames(plate_parameters["nicknames"])

    # Create Chip object
    new_plate = Plate(model_name=model_name, grid=grid)

    # Store the locations, nicknames, and well types of the wells in the chip
    for index in range(amount_of_pots):
        new_plate.set_location(index, pot_locations[index])
        # print(f"index:{index}, nick:{nicknames}")
        new_plate.set_nickname(index, nicknames[index])
        new_plate.set_pot_depth(index, pot_depth[index])

    return new_plate

