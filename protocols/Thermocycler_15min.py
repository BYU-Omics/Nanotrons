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

myProtocol.aspirate_from(100, custom('A2'))

myProtocol.aspirate_from(1000, custom('A1'))

myProtocol.dispense_to(1000, micropots_3('A1'))

myProtocol.aspirate_from(1000, custom('A1'))

myProtocol.dispense_to(1000, micropots_3('C1'))

myProtocol.aspirate_from(1000, custom('A1'))

myProtocol.dispense_to(1000, micropots_3('A9'))

myProtocol.aspirate_from(1000, custom('A1'))

myProtocol.dispense_to(1000, micropots_3('C9'))

myProtocol.aspirate_from(1400, custom('A1'))

myProtocol.dispense_to(200, micropots_3('A2'))
myProtocol.dispense_to(200, micropots_3('A3'))
myProtocol.dispense_to(200, micropots_3('A4'))
myProtocol.dispense_to(200, micropots_3('A5'))
myProtocol.dispense_to(200, micropots_3('A6'))
myProtocol.dispense_to(200, micropots_3('A7'))
myProtocol.dispense_to(200, micropots_3('A8'))

myProtocol.aspirate_from(1400, custom('A1'))

myProtocol.dispense_to(200, micropots_3('B2'))
myProtocol.dispense_to(200, micropots_3('B3'))
myProtocol.dispense_to(200, micropots_3('B4'))
myProtocol.dispense_to(200, micropots_3('B5'))
myProtocol.dispense_to(200, micropots_3('B6'))
myProtocol.dispense_to(200, micropots_3('B7'))
myProtocol.dispense_to(200, micropots_3('B8'))

myProtocol.aspirate_from(1400, custom('A1'))

myProtocol.dispense_to(200, micropots_3('C2'))
myProtocol.dispense_to(200, micropots_3('C3'))
myProtocol.dispense_to(200, micropots_3('C4'))
myProtocol.dispense_to(200, micropots_3('C5'))
myProtocol.dispense_to(200, micropots_3('C6'))
myProtocol.dispense_to(200, micropots_3('C7'))
myProtocol.dispense_to(200, micropots_3('C8'))

for number in range(0, 55):
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