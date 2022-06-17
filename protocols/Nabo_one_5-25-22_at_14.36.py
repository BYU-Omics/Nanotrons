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

infusion_rate = 500  #nL/s
withdraw_rate = 500  #nL/s


myProtocol.set_syringe_model("HAMILTON_1705.json")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash(500) # <- You can input a custom flow rate in nL/s if desired. 
# ------------START OF PROTOCOL---------------------------------

# A wells 

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('A1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('A2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('A3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('A4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('A5'), infusion_rate)

# B wells
myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('B1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('B2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('B3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('B4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('B5'), infusion_rate)

# C wells

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('C1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('C2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('C3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('C4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('C5'), infusion_rate)

# D wells 

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('D1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('D2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('D3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('D4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('D5'), infusion_rate)

# E wells

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('E1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('E2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('E3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('E4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('E5'), infusion_rate)



myProtocol.mid_wash(rate = 500) # <- You can input a custom flow rate in nL/s if desired.

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water(500) # <- You can input a custom flow rate in nL/s if desired.
myProtocol.end_of_protocol()