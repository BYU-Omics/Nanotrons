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

myProtocol.set_syringe_model("HAMILTON_175")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(600, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(100, corning_384('L11'))
myProtocol.dispense_to(100, corning_384('L12'))
myProtocol.dispense_to(100, corning_384('L13'))
myProtocol.dispense_to(100, corning_384('L14'))
myProtocol.dispense_to(100, corning_384('L15'))

myProtocol.mid_wash()

myProtocol.aspirate_from(300, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(50, corning_384('M11'))
myProtocol.dispense_to(50, corning_384('M12'))
myProtocol.dispense_to(50, corning_384('M13'))
myProtocol.dispense_to(50, corning_384('M14'))
myProtocol.dispense_to(50, corning_384('M15'))

myProtocol.mid_wash()

myProtocol.aspirate_from(120, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(20, corning_384('N11'))
myProtocol.dispense_to(20, corning_384('N12'))
myProtocol.dispense_to(20, corning_384('N13'))
myProtocol.dispense_to(20, corning_384('N14'))
myProtocol.dispense_to(20, corning_384('N15'))
myProtocol.mid_wash()

myProtocol.aspirate_from(60, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(10, corning_384('O11'))
myProtocol.dispense_to(10, corning_384('O12'))
myProtocol.dispense_to(10, corning_384('O13'))
myProtocol.dispense_to(10, corning_384('O14'))
myProtocol.dispense_to(10, corning_384('O15'))

myProtocol.mid_wash()
myProtocol.aspirate_from(30, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(5, corning_384('P11'))
myProtocol.dispense_to(5, corning_384('P12'))
myProtocol.dispense_to(5, corning_384('P13'))
myProtocol.dispense_to(5, corning_384('P14'))
myProtocol.dispense_to(5, corning_384('P15'))
myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()