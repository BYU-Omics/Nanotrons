"""
    Template for writing protocols. 

    Instructions: 
        'aspirate_from' assumes nanoliters
        'dispense_to' 
"""

#-----------IMPORT THE USED PAKAGES---------------------------------------

import sys
LABWARE = sys.argv[1]
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')

try:
    from api import *
except ImportError:
    CURRENT_DIRECTORY
    from api import *

# ----------CREATE A PROTOCOL OBJECT--------------------------------------

myProtocol = Api() 

# ----------IMPORT THE CALIBRATION FOR THIS PROTOCOL: this is done from the executer, it is specified on the GUI

chips, plates = myProtocol.load_labware_setup(LABWARE)

# ------------END OF HEADING-------------------------------------------------

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED-----------

# Labware file loaded: Test_for_protocols.json

micropots_3 = chips[0].get_location_by_nickname 
corning_384 = plates[0].get_location_by_nickname 
custom = plates[1].get_location_by_nickname 
corning_384_2 = plates[2].get_location_by_nickname 
custom_3 = plates[3].get_location_by_nickname 
custom_4 = plates[4].get_location_by_nickname 
custom_small = plates[5].get_location_by_nickname 
custom_small_5 = plates[6].get_location_by_nickname 

#----------START OF PROTOCOL----------------------------------------

myProtocol.aspirate_from(100, custom('A1'))

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()