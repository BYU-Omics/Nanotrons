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
	'protocolName': 'Standard_fluorescein_test_uL.py', 
	'author': 'Yhann Masbernat / Alex Buttars', 
	'description': 'Standard Fluorescein test using syringe 1705.' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Fluo_Test_03-01.json')

corning_384 = plates[0]
custom = plates[1] 
custom_small = plates[2] 


# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------

corning_384 = corning_384.pot_position_for_protocol 
custom = custom.pot_position_for_protocol 
custom_small = custom_small.pot_position_for_protocol 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_syringe_model("HAMILTON_1705")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(20000, custom_small('A1')) # 10 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A6'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A7'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A8'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A9'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A10'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('B1')) # 8 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B6'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B7'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B8'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B9'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B10'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('C1')) # 6 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C6'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C7'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C8'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C9'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C10'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('D1')) # 4 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D6'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D7'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D8'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D9'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D10'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('E1')) # 2 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E6'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E7'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E8'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E9'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E10'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('F1')) # 0 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F6'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F7'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F8'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F9'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F10'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()