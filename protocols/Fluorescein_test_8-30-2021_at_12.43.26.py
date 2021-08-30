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
	'protocolName': 'Fluorescein_test_8-30-2021_at_12.43.26.py', 
	'author': 'Nathaniel Axtel', 
	'description': 'Fluorescein test' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Fluo_test_30-08.json')

corning_384 = plates[0] 
custom = plates[1] 
custom_small = plates[2] 

# If the depth has been voided for any of the plates, this is specified here:

myProtocol.void_plate_depth(plate = custom, void = True)
myProtocol.void_plate_depth(plate = custom_small, void = True)

# -----------PREPROTOCOL SETUP-------------------

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

myProtocol.aspirate_from(500, custom_small('A1'))

myProtocol.dispense_to(100, corning_384('B1'))
myProtocol.dispense_to(100, corning_384('C1'))
myProtocol.dispense_to(100, corning_384('D1'))
myProtocol.dispense_to(100, corning_384('E1'))
myProtocol.dispense_to(100, corning_384('A1'))

myProtocol.mid_wash()

myProtocol.aspirate_from(250, custom_small('B1'))

myProtocol.dispense_to(50, corning_384('A2'))
myProtocol.dispense_to(50, corning_384('B2'))
myProtocol.dispense_to(50, corning_384('C2'))
myProtocol.dispense_to(50, corning_384('D2'))
myProtocol.dispense_to(50, corning_384('E2'))

myProtocol.mid_wash()

myProtocol.aspirate_from(100, custom_small('C1'))

myProtocol.dispense_to(20, corning_384('A3'))
myProtocol.dispense_to(20, corning_384('B3'))
myProtocol.dispense_to(20, corning_384('C3'))
myProtocol.dispense_to(20, corning_384('D3'))
myProtocol.dispense_to(20, corning_384('E3'))

myProtocol.mid_wash()

myProtocol.aspirate_from(50, custom_small('D1'))

myProtocol.dispense_to(10, corning_384('A4'))
myProtocol.dispense_to(10, corning_384('B4'))
myProtocol.dispense_to(10, corning_384('C4'))
myProtocol.dispense_to(10, corning_384('D4'))
myProtocol.dispense_to(10, corning_384('E4'))

myProtocol.mid_wash()

myProtocol.aspirate_from(50, custom_small('E1'))

myProtocol.dispense_to(10, corning_384('A5'))
myProtocol.dispense_to(10, corning_384('B5'))
myProtocol.dispense_to(10, corning_384('C5'))
myProtocol.dispense_to(10, corning_384('D5'))
myProtocol.dispense_to(10, corning_384('E5'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()