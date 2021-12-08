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
	'protocolName': 'Fluorescein_test_11-19-2021_at_11.00.00.py', 
	'author': 'Alejandro Brozalez', 
	'description': 'Fluorescein test' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Fluo_test_03-12.json')


custom = plates[0] 
custom_small = plates[1] 
corning_384 = plates[2]

# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------

corning_384 = corning_384.pot_position_for_protocol 
custom = custom.pot_position_for_protocol 
custom_small = custom_small.pot_position_for_protocol 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_syringe_model("HAMILTON_175")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(500, custom_small('A1'))

myProtocol.dispense_to(100, corning_384('A7'))
myProtocol.dispense_to(100, corning_384('A8'))
myProtocol.dispense_to(100, corning_384('A9'))
myProtocol.dispense_to(100, corning_384('A10'))
myProtocol.dispense_to(100, corning_384('A11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(250, custom_small('B1'))

myProtocol.dispense_to(50, corning_384('B7'))
myProtocol.dispense_to(50, corning_384('B8'))
myProtocol.dispense_to(50, corning_384('B9'))
myProtocol.dispense_to(50, corning_384('B10'))
myProtocol.dispense_to(50, corning_384('B11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(100, custom_small('C1'))

myProtocol.dispense_to(20, corning_384('C7'))
myProtocol.dispense_to(20, corning_384('C8'))
myProtocol.dispense_to(20, corning_384('C9'))
myProtocol.dispense_to(20, corning_384('C10'))
myProtocol.dispense_to(20, corning_384('C11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(50, custom_small('D1'))

myProtocol.dispense_to(10, corning_384('D7'))
myProtocol.dispense_to(10, corning_384('D8'))
myProtocol.dispense_to(10, corning_384('D9'))
myProtocol.dispense_to(10, corning_384('D10'))
myProtocol.dispense_to(10, corning_384('D11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(25, custom_small('D1'))

myProtocol.dispense_to(5, corning_384('E7'))
myProtocol.dispense_to(5, corning_384('E8'))
myProtocol.dispense_to(5, corning_384('E9'))
myProtocol.dispense_to(5, corning_384('E10'))
myProtocol.dispense_to(5, corning_384('E11'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()