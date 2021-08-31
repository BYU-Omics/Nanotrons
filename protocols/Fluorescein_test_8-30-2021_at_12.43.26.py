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

chips, plates = myProtocol.load_labware_setup('Fluo_test_08-30.json')


custom = plates[0] 
custom_small = plates[1] 
corning_384 = plates[2]

# If the depth has been voided for any of the plates, this is specified here:

myProtocol.void_plate_depth(plate = custom, void = True)
myProtocol.void_plate_depth(plate = custom_small, void = True)

# -----------PREPROTOCOL SETUP-------------------

corning_384 = corning_384.pot_position_for_protocol 
custom = custom.pot_position_for_protocol 
custom_small = custom_small.pot_position_for_protocol 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(500, custom_small('A1'))

myProtocol.dispense_to(100, corning_384('B14'))
myProtocol.dispense_to(100, corning_384('C14'))
myProtocol.dispense_to(100, corning_384('D14'))
myProtocol.dispense_to(100, corning_384('A14'))
myProtocol.dispense_to(100, corning_384('E14'))

myProtocol.mid_wash()

myProtocol.aspirate_from(250, custom_small('B1'))

myProtocol.dispense_to(50, corning_384('A15'))
myProtocol.dispense_to(50, corning_384('B15'))
myProtocol.dispense_to(50, corning_384('C15'))
myProtocol.dispense_to(50, corning_384('D15'))
myProtocol.dispense_to(50, corning_384('E15'))

myProtocol.mid_wash()

myProtocol.aspirate_from(100, custom_small('C1'))

myProtocol.dispense_to(20, corning_384('A16'))
myProtocol.dispense_to(20, corning_384('B16'))
myProtocol.dispense_to(20, corning_384('C16'))
myProtocol.dispense_to(20, corning_384('D16'))
myProtocol.dispense_to(20, corning_384('E16'))

myProtocol.mid_wash()

myProtocol.aspirate_from(50, custom_small('D1'))

myProtocol.dispense_to(10, corning_384('A17'))
myProtocol.dispense_to(10, corning_384('B17'))
myProtocol.dispense_to(10, corning_384('C17'))
myProtocol.dispense_to(10, corning_384('D17'))
myProtocol.dispense_to(10, corning_384('E17'))

myProtocol.mid_wash()

myProtocol.aspirate_from(25, custom_small('D1'))

myProtocol.dispense_to(5, corning_384('A18'))
myProtocol.dispense_to(5, corning_384('B18'))
myProtocol.dispense_to(5, corning_384('C18'))
myProtocol.dispense_to(5, corning_384('D18'))
myProtocol.dispense_to(5, corning_384('E18'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()