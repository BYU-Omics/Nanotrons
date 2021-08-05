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
corning_384 = plates[0].pot_position_for_protocol
custom = plates[1].pot_position_for_protocol

# If the depth has been voided for any of the plates, this is specified here: 

myProtocol.void_plate_depth(plates[1], void = True)

# This is the calibration step to get air out of the syringe:

myProtocol.dispense_to(0, custom('A1'))
myProtocol.adjust_syringe()

#----------START OF PROTOCOL----------------------------------------

myProtocol.aspirate_from(0, custom('A2'))

myProtocol.aspirate_from(0, corning_384('A1'))

#--------------END OF PROTOCOL--------------

myProtocol.dispense_to(0, custom('A1'))
myProtocol.adjust_syringe()

myProtocol.end_of_protocol()