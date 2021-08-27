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

chips, plates = myProtocol.load_labware_setup('Fluorescein_test.json')

micropots_3 = chips[0] 
corning_384 = plates[0] 
custom = plates[1] 
custom_small = plates[2] 

# If the depth has been voided for any of the plates, this is specified here:

myProtocol.void_plate_depth(plate = custom, void = True)

# -----------PREPROTOCOL SETUP-------------------

micropots_3 = micropots_3.get_location_by_nickname 
corning_384 = corning_384.get_location_by_nickname 
custom = custom.get_location_by_nickname 
custom_small = custom_small.get_location_by_nickname 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(volume = 10, source = custom('A1'))

myProtocol.aspirate_from(volume = 5000, source = corning_384('A2'))

myProtocol.set_block_temp(4, 0)

myProtocol.close_lid()

myProtocol.set_lid_temp(39)

myProtocol.set_block_temp(37, 15)

myProtocol.deactivate_lid()

myProtocol.aspirate_from(volume = 10, source = micropots_3('A1'))

myProtocol.aspirate_from(volume = 5000, source = custom_small('A2'))

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()