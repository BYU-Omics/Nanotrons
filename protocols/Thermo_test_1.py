"""
    Template for writing protocols. 

    Instructions: 
        'aspirate_from' assumes nanoliters
        'dispense_to' 
"""

#-----------IMPORT THE USED PAKAGES---------------------------------------

import sys
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')

try:
    from api import *
except ImportError:
    CURRENT_DIRECTORY
    from api import *

# ----------CREATE A PROTOCOL OBJECT--------------------------------------

myProtocol = Api() 

metadata = {
	'protocolName': 'Evap_test.py', 
	'author': 'Yhann Masbernat', 
	'description': 'Evap test.' 
}

# ----------IMPORT THE CALIBRATION FOR THIS PROTOCOL: this is done from the executer, it is specified on the GUI

myProtocol.close_lid()
myProtocol.set_block_temp(4, 1)
myProtocol.deactivate_block()
myProtocol.open_lid()
myProtocol.close_lid()
myProtocol.set_lid_temp(37)
myProtocol.set_block_temp(37, 1)
myProtocol.deactivate_lid()
myProtocol.set_block_temp(4, 1)
myProtocol.deactivate_block()
myProtocol.open_lid()