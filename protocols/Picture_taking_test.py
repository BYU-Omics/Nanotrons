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

# myProtocol.adjust_syringe(-100)

# ------------END OF HEADING-------------------------------------------------

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED-----------

# Labware file loaded: Alex_config.json

micropots_3 = chips[0].get_location_by_nickname 
custom = plates[0].get_location_by_nickname 

#----------START OF PROTOCOL----------------------------------------

myProtocol.take_picture(micropots_3('B5'))

myProtocol.take_picture(micropots_3('B6'))

myProtocol.take_picture(micropots_3('B7'))

myProtocol.take_picture(micropots_3('B8'))


#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()