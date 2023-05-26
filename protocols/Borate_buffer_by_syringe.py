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
	'description': 'Borate Buffer Dispensing' 
}

'''
This protocol is used to add 20 uL (20000 nL) of borate buffer to wells prior to addition of fluorescing.
'''

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('6_30_2022.json')

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

myProtocol.set_washing_positions(clean_water, wash_water, waste_water)

myProtocol.start_wash(500) # <- You can input a custom flow rate in nL/s if desired. 
# ------------START OF PROTOCOL---------------------------------

# F wells 

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('G1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('G2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('G3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('G4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('G5'), infusion_rate)

# G wells
myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('H1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('H2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('H3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('H4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('H5'), infusion_rate)

# H wells

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('I1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('I2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('I3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('I4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('I5'), infusion_rate)

# I wells 

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('J1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('J2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('J3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('J4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('J5'), infusion_rate)

# J wells

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('K1'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('K2'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('K3'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('K4'), infusion_rate)

myProtocol.aspirate_from(20000, custom('A5'), withdraw_rate)
myProtocol.dispense_to(20000, corning_384('K5'), infusion_rate)



myProtocol.mid_wash(rate = 500) # <- You can input a custom flow rate in nL/s if desired.

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water(500) # <- You can input a custom flow rate in nL/s if desired.
myProtocol.end_of_protocol()