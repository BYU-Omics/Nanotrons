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

# ----------IMPORT THE CALIBRATION FOR THIS PROTOCOL: this is done from the executer, it is specified on the GUI

chips, plates = myProtocol.load_labware_setup("Recording.json")

# ------------END OF HEADING-------------------------------------------------

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED-----------

# Labware file loaded: Test_for_protocols.json

micropots_3 = chips[0].get_location_by_nickname 
custom = plates[1].get_location_by_nickname 

# -----------PREPROTOCOL SETUP-------------------

# Designater wells for washing tip

waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_washing_positions(clean_water=clean_water, wash_water=wash_water, waste_water=waste_water)

# If there are any depth voided they are listed here

myProtocol.void_plate_depth(plates[1], True)

myProtocol.start_wash()

#----------START OF PROTOCOL----------------------------------------

myProtocol.set_block_temp(4, 0)

myProtocol.aspirate_from(1000, clean_water)

myProtocol.dispense_to(1000, micropots_3('A1'))

myProtocol.aspirate_from(1000, clean_water)

myProtocol.dispense_to(1000, micropots_3('C1'))

myProtocol.aspirate_from(1000, clean_water)

myProtocol.dispense_to(1000, micropots_3('A9'))

myProtocol.aspirate_from(1000, clean_water)

myProtocol.dispense_to(1000, micropots_3('C9'))

myProtocol.aspirate_from(1400, clean_water)

myProtocol.dispense_to(200, micropots_3('A2'))
myProtocol.dispense_to(200, micropots_3('A3'))
myProtocol.dispense_to(200, micropots_3('A4'))
myProtocol.dispense_to(200, micropots_3('A5'))
myProtocol.dispense_to(200, micropots_3('A6'))
myProtocol.dispense_to(200, micropots_3('A7'))
myProtocol.dispense_to(200, micropots_3('A8'))

myProtocol.aspirate_from(1400, clean_water)

myProtocol.dispense_to(200, micropots_3('B2'))
myProtocol.dispense_to(200, micropots_3('B3'))
myProtocol.dispense_to(200, micropots_3('B4'))
myProtocol.dispense_to(200, micropots_3('B5'))
myProtocol.dispense_to(200, micropots_3('B6'))
myProtocol.dispense_to(200, micropots_3('B7'))
myProtocol.dispense_to(200, micropots_3('B8'))

myProtocol.aspirate_from(1400, clean_water)

myProtocol.dispense_to(200, micropots_3('C2'))
myProtocol.dispense_to(200, micropots_3('C3'))
myProtocol.dispense_to(200, micropots_3('C4'))
myProtocol.dispense_to(200, micropots_3('C5'))
myProtocol.dispense_to(200, micropots_3('C6'))
myProtocol.dispense_to(200, micropots_3('C7'))
myProtocol.dispense_to(200, micropots_3('C8'))

myProtocol.take_picture(clean_water)

myProtocol.set_tempdeck_temp(4, 10)

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()