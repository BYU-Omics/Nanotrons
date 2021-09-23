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

chips, plates = myProtocol.load_labware_setup('Evap_Test_09-23.json')

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
myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

chip_list = [micropots_3_top, micropots_3_btm]


# myProtocol.take_picture(waste_water)
# myProtocol.open_lid()

myProtocol.set_block_temp(4, 0)

for chip in chip_list:

    myProtocol.aspirate_from(1800, custom('A3'))

    myProtocol.dispense_to(200, chip('A1'))
    myProtocol.dispense_to(200, chip('A2'))
    myProtocol.dispense_to(200, chip('A3'))
    myProtocol.dispense_to(200, chip('A4'))
    myProtocol.dispense_to(200, chip('A5'))
    myProtocol.dispense_to(200, chip('A6'))
    myProtocol.dispense_to(200, chip('A7'))
    myProtocol.dispense_to(200, chip('A8'))
    myProtocol.dispense_to(200, chip('A9'))

    myProtocol.aspirate_from(1800, custom('A3'))

    myProtocol.dispense_to(200, chip('B1'))
    myProtocol.dispense_to(200, chip('B2'))
    myProtocol.dispense_to(200, chip('B3'))
    myProtocol.dispense_to(200, chip('B4'))
    myProtocol.dispense_to(200, chip('B5'))
    myProtocol.dispense_to(200, chip('B6'))
    myProtocol.dispense_to(200, chip('B7'))
    myProtocol.dispense_to(200, chip('B8'))
    myProtocol.dispense_to(200, chip('B9'))

    myProtocol.aspirate_from(1800, custom('A3'))

    myProtocol.dispense_to(200, chip('C1'))
    myProtocol.dispense_to(200, chip('C2'))
    myProtocol.dispense_to(200, chip('C3'))
    myProtocol.dispense_to(200, chip('C4'))
    myProtocol.dispense_to(200, chip('C5'))
    myProtocol.dispense_to(200, chip('C6'))
    myProtocol.dispense_to(200, chip('C7'))
    myProtocol.dispense_to(200, chip('C8'))
    myProtocol.dispense_to(200, chip('C9'))

for number in range(0, 54):

    myProtocol.open_lid()

    myProtocol.take_picture(micropots_3_top('B2'))
    myProtocol.take_picture(micropots_3_top('B5'))
    myProtocol.take_picture(micropots_3_top('B8'))

    myProtocol.take_picture(micropots_3_btm('B2'))
    myProtocol.take_picture(micropots_3_btm('B5'))
    myProtocol.take_picture(micropots_3_btm('B8'))

    myProtocol.close_lid()

    myProtocol.set_block_temp(37, 15)

    myProtocol.set_block_temp(4, 0)

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()