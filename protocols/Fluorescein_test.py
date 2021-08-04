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
custom_small = plates[2].get_location_by_nickname 

#----------START OF PROTOCOL----------------------------------------

myProtocol.aspirate_from(50, custom['A2'])

myProtocol.aspirate_from(600, custom_small['A1'])

myProtocol.dispense_to(50, custom['A1'])

myProtocol.dispense_to(100, corning_384['A18'])
myProtocol.dispense_to(100, corning_384['B18'])
myProtocol.dispense_to(100, corning_384['C18'])
myProtocol.dispense_to(100, corning_384['D18'])
myProtocol.dispense_to(100, corning_384['E18'])

myProtocol.dispense_to(100, custom['A1'])

myProtocol.aspirate_from(50, custom['A2'])

myProtocol.aspirate_from(350, custom_small['B1'])

myProtocol.dispense_to(50, custom['A1'])

myProtocol.dispense_to(50, corning_384['A19'])
myProtocol.dispense_to(50, corning_384['B19'])
myProtocol.dispense_to(50, corning_384['C19'])
myProtocol.dispense_to(50, corning_384['D19'])
myProtocol.dispense_to(50, corning_384['E19'])

myProtocol.dispense_to(100, custom['A1'])

myProtocol.aspirate_from(50, custom['A2'])

myProtocol.aspirate_from(200, custom_small['C1'])

myProtocol.dispense_to(50, custom['A1'])

myProtocol.dispense_to(20, corning_384['A20'])
myProtocol.dispense_to(20, corning_384['B20'])
myProtocol.dispense_to(20, corning_384['C20'])
myProtocol.dispense_to(20, corning_384['D20'])
myProtocol.dispense_to(20, corning_384['E20'])

myProtocol.dispense_to(100, custom['A1'])

myProtocol.aspirate_from(50, custom['A2'])

myProtocol.aspirate_from(150, custom_small['D1'])

myProtocol.dispense_to(50, custom['A1'])

myProtocol.dispense_to(10, corning_384['A21'])
myProtocol.dispense_to(10, corning_384['B21'])
myProtocol.dispense_to(10, corning_384['C21'])
myProtocol.dispense_to(10, corning_384['D21'])
myProtocol.dispense_to(10, corning_384['E21'])

myProtocol.dispense_to(100, custom['A1'])

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()