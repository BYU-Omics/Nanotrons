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
	'protocolName': 'Evaporation_test', 
	'author': 'Nathaniel Axtel', 
	'description': 'This is the evaporation test that takes a pictue every 15 min' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Evap_test_09-17.json')

micropots_3_top = chips[0].get_location_by_nickname
micropots_3_btm = chips[1].get_location_by_nickname
custom = plates[0].pot_position_for_protocol 

# If the depth has been voided for any of the plates, this is specified here:

# myProtocol.void_plate_depth(plate = custom, void = True)

# -----------PREPROTOCOL SETUP-------------------

pictures_folder = metadata['protocolName']
myProtocol.set_pictures_folder('protocol_pics')
# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_washing_positions(clean_water, wash_water, waste_water)
# myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.take_picture(waste_water)


#--------------END OF PROTOCOL--------------

# myProtocol.end_of_protocol()