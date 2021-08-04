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

myProtocol.dispense_to(0, custom('A1'))
myProtocol.adjust_syringe()

#----------START OF PROTOCOL----------------------------------------

myProtocol.set_block_temp(4, 0)

for number in range(0, 1):
    myProtocol.take_picture(micropots_3('B2'))
    myProtocol.take_picture(micropots_3('B5'))
    myProtocol.take_picture(micropots_3('B8'))

    myProtocol.close_lid()

    myProtocol.set_lid_temp(39)

    myProtocol.set_block_temp(37, 15)

    myProtocol.deactivate_lid()

    myProtocol.set_block_temp(4, 0)

    myProtocol.open_lid()

#--------------END OF PROTOCOL--------------

myProtocol.dispense_to(0, custom('A1'))
myProtocol.adjust_syringe()

myProtocol.end_of_protocol()