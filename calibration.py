"""
CALIBRATION MODULE
    This module defines standard methods that help in the calibration of Chip and Plate objects
"""

import numpy as np
from chip import Chip
from plate import Plate


"""
SHARED CALIBRATION METHODS
"""

# This method receives three calibration points and guesses the fourth (fourth corner of the Chip/Plate component)
def guess_fourth_calibration_point(calibration_points):
    
    ordered_calibration_points = reorder_calibration_points(calibration_points) # The three calibration points need to be in the right order or the contructor vectors won't be set properly

    bl = ordered_calibration_points[0]
    br = ordered_calibration_points[1] 
    fl = ordered_calibration_points[0]

    # back_left to back_right
    accross_vector = []
    accross_vector.append(br[0] - bl[0])
    accross_vector.append(br[1] - bl[1])
    accross_vector.append(br[2] - bl[2])

    # back_left to front_left
    down_vector = []
    down_vector.append(fl[0] - bl[0])
    down_vector.append(fl[1] - bl[1])
    down_vector.append(fl[2] - bl[2])
    # Constructor vectors
    vector_a = np.array(ordered_calibration_points[1]) - np.array(ordered_calibration_points[0])
    vector_b = np.array(ordered_calibration_points[2]) - np.array(ordered_calibration_points[0])

    # Vector arithmetic
    vector_c = vector_a + vector_b

    # Calculate 4th point
    fourth_calibration_point = np.array(ordered_calibration_points[0]) + vector_c
    return fourth_calibration_point

# This method receives a list of three points in space (a list) and reorders them to be understandable for the system
    # DESIRED ORDER (as if a rectangle of callibration points were laying on the long side as the base):
    # i. Top left callibration point
    # ii. Top right callibration point
    # iii. Bottom left callibration point
    # NOTE: the order of the points matters both for guessing the 4th calibration point right and for creating the plane for mapping out the wells/pots in a grid

def reorder_calibration_points(calibration_points):

    # Make arrays from calibration points
    a = np.array(calibration_points[0])
    b = np.array(calibration_points[1])
    c = np.array(calibration_points[2])
    # Create vectors. Formatted in tuples: (point1, point2, vector_numpy_array)
    v0 = (b,c,c - b)
    v1 = (a,c,c - a)
    v2 = (a,b,b - a)
    vectors = [v0,v1,v2]
    magnitudes = []

    # get magnitude of each vector, compiled to list
    for vector in range(len(calibration_points)):
        magnitude = np.linalg.norm(vectors[vector][2])
        magnitudes.append(magnitude)
    
    index_of_back_left = magnitudes.index(max(magnitudes)) # Finds the index of the vector that connects the diagonal (it will have the max magnitude).
    back_left_point = calibration_points[index_of_back_left] # index_of_back_left corresponds to index of back left point in calibration_points

    # get "back-right" calibration point, aka closest calibration point to robot home position
    ref_point = [418.0, 350.0, 170.15] # Robot home position
    r = np.array(ref_point)
    r1 = (r, a, a-r)
    r2 = (r, b, b-r)
    r3 = (r, c, c-r)
    ref_vectors = [r1, r2, r3]
    ref_magnitudes = []
    # get magnitude of each vector, compiled to list
    for vector in range(len(calibration_points)):
        magnitude = np.linalg.norm(ref_vectors[vector][2])
        ref_magnitudes.append(magnitude)

    index_of_back_right = ref_magnitudes.index(min(ref_magnitudes))
    back_right_point = calibration_points[index_of_back_right]

    calibration_point_list = [] # copy of calibration_points list to be manipulated
    for point in calibration_points:
        calibration_point_list.append(point)

    ordered_points = [] # list to be returned
    
    calibration_point_list.pop(calibration_point_list.index(back_left_point))
    calibration_point_list.pop(calibration_point_list.index(back_right_point))

    front_left_point = calibration_point_list[0]

    ordered_points.append(back_left_point)
    ordered_points.append(back_right_point)
    ordered_points.append(front_left_point)

    return ordered_points

# This method returns all the nicknames as a continuous single list from a list of lists
def get_nicknames(nicknames_list):
    single_list = []
    for index in range(len(nicknames_list)):
        single_list = single_list + nicknames_list[index]

    return single_list


"""
CALIBRATION METHODS
"""
# This method takes the parameters of the plate plus its calibration points and returns a list of the locations of all the pots in that plate
def calibrate_model(chip_parameters, calibration_points):
    ordered_calibration_points = reorder_calibration_points(calibration_points)   
    
    grid = chip_parameters["grid"]
    plate_rows = grid[0] # change to take value from model parameters
    plate_columns = grid[1] # change to take value from model parameters
    calibration_offset = chip_parameters["offset"] # change to take value from model parameters

    bl = ordered_calibration_points[0]
    br = ordered_calibration_points[1] 
    fl = ordered_calibration_points[2]
    

    # back_left to back_right
    accross_vector = []
    accross_vector.append((br[0] - bl[0]) / (2*calibration_offset + plate_columns -1))
    accross_vector.append((br[1] - bl[1]) / (2*calibration_offset + plate_columns -1))
    accross_vector.append((br[2] - bl[2]) / (2*calibration_offset + plate_columns -1))

    # back_left to front_left
    down_vector = []
    down_vector.append((fl[0] - bl[0]) / (plate_rows -1))
    down_vector.append((fl[1] - bl[1]) / (plate_rows -1))
    down_vector.append((fl[2] - bl[2]) / (plate_rows -1))

    # so well coordinate start reference can change without changing back_left
    ref_point = bl

    # populate the matrix with well coordinates
    plate_index = 0
    well_coordinate_list = []
    for i in range(0, plate_rows):
        for j in range(0, plate_columns):
            point_to_add = []
            point_to_add.append(ref_point[0] + (calibration_offset + j) * accross_vector[0])
            point_to_add.append(ref_point[1] + (calibration_offset + j) * accross_vector[1])
            point_to_add.append(ref_point[2] + (calibration_offset + j) * accross_vector[2])
            well_coordinate_list.append(point_to_add)
            plate_index += 1
 
        ref_point[0] = ref_point[0] + down_vector[0]
        ref_point[1] = ref_point[1] + down_vector[1]
        ref_point[2] = ref_point[2] + down_vector[2]
        
    
        
    return well_coordinate_list

def create_component(model_name, plate_parameters, pot_locations):

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
    new_component = Plate(model_name=model_name, grid=grid)

    # Store the locations, nicknames, and well types of the wells in the chip
    for index in range(amount_of_pots):
        new_component.set_location(index, pot_locations[index])
        new_component.set_nickname(index, nicknames[index])
        new_component.set_pot_depth(index, pot_depth[index])

    return new_component

