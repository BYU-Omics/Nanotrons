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
	'protocolName': 'Buffer_fluorescein_test_uL.py', 
	'author': 'Yhann Masbernat / Alex Buttars', 
	'description': 'Buffer Fluorescein test using syringe 1705.' 
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
2000000
# ------------START OF PROTOCOL---------------------------------

# L wells 
myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('G11'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('G12'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('G13'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('G14'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('G15'))

# M wells H1
myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('H11'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('H12'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('H13'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('H14'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('H15'))

# N wells

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('I11'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('I12'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('I13'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('I14'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('I15'))

# O wells 

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('J11'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('J12'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('J13'))
myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('J14'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('J15'))

# P wells

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('K11'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('K12'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('K13'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('K14'))

myProtocol.aspirate_from(20000, custom('A5'))
myProtocol.dispense_to(20000, corning_384('K15'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()