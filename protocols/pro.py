"""
    Instructions: 
        This protocol has been created with the class protocol_creator.
        If this file is edited it must need to be renamed modifiying the date of edition.        
"""
import sys 

try:
    from api import *
except ImportError:
    sys.path.append(sys.path[0] + '\\..') # current directory
    from api import *

myProtocol = Api() # creates a protocol object using the Api

metadata = {
	'protocolName': 'Testing_matching 8-26-2021 at 15:23:9.py', 
	'author': 'Alejandro Brozalez', 
	'description': 'I am testing how this protocol creator works.' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Recording.json')

micropots_3 = chips[0] 
custom = plates[0] 

# If the depth has been voided for any of the plates, this is specified here:

myProtocol.void_plate_depth(plate = custom, void = True)

# -----------PREPROTOCOL SETUP-------------------

micropots_3 = micropots_3.get_location_by_nickname 
custom = custom.get_location_by_nickname 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

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

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()