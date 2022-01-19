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
	'description': 'Fluorescein test.' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Fluo_Test_01-19.json')

custom = plates[1] 
custom_small = plates[2] 
corning_384 = plates[0]

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

myProtocol.dispense_to(100, corning_384('A19'))
myProtocol.dispense_to(100, corning_384('A20'))
myProtocol.dispense_to(100, corning_384('A21'))
myProtocol.dispense_to(100, corning_384('A22'))
myProtocol.dispense_to(100, corning_384('A23'))

myProtocol.mid_wash()

myProtocol.aspirate_from(250, custom_small('B1'))

myProtocol.dispense_to(50, corning_384('B19'))
myProtocol.dispense_to(50, corning_384('B20'))
myProtocol.dispense_to(50, corning_384('B21'))
myProtocol.dispense_to(50, corning_384('B22'))
myProtocol.dispense_to(50, corning_384('B23'))

myProtocol.mid_wash()

myProtocol.aspirate_from(100, custom_small('C1'))

myProtocol.dispense_to(20, corning_384('C19'))
myProtocol.dispense_to(20, corning_384('C20'))
myProtocol.dispense_to(20, corning_384('C21'))
myProtocol.dispense_to(20, corning_384('C22'))
myProtocol.dispense_to(20, corning_384('C23'))

myProtocol.mid_wash()

myProtocol.aspirate_from(50, custom_small('D1'))

myProtocol.dispense_to(10, corning_384('D19'))
myProtocol.dispense_to(10, corning_384('D20'))
myProtocol.dispense_to(10, corning_384('D21'))
myProtocol.dispense_to(10, corning_384('D22'))
myProtocol.dispense_to(10, corning_384('D23'))

myProtocol.mid_wash()

myProtocol.aspirate_from(25, custom_small('D1'))

myProtocol.dispense_to(5, corning_384('E19'))
myProtocol.dispense_to(5, corning_384('E20'))
myProtocol.dispense_to(5, corning_384('E21'))
myProtocol.dispense_to(5, corning_384('E22'))
myProtocol.dispense_to(5, corning_384('E23'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()