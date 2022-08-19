"""
    Template for writing protocols. 

    Instructions: 
        'aspirate_from' assumes nanoliters
        'dispense_to' 
"""

#-----------IMPORT THE USED PAKAGES---------------------------------------

import sys
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')

try:
    from api import *
except ImportError:
    CURRENT_DIRECTORY
    from api import *

# ----------CREATE A PROTOCOL OBJECT--------------------------------------

myProtocol = Api() 

metadata = {
'protocolName': 'Evap_test.py', 
	'author': 'Yhann Masbernat', 
	'description': 'Evap test.' 
}
# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

models = myProtocol.load_labware_setup('TC2_08_16_2022.json')

custom = models[0]
microPots_chip = models[1]

# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------# 

chip_1 = microPots_chip.well_position_for_protocol
custom = custom.well_position_for_protocol  

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

infusion_rate = 50  #nL/s
withdraw_rate = 50  #nL/s

myProtocol.set_syringe_model("HAMILTON_175.json")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash(50)

# ------------START OF PROTOCOL---------------------------------
myProtocol.close_lid()
myProtocol.set_block_temp(4)
myProtocol.set_block_temp(4, 2)
myProtocol.open_lid()

myProtocol.aspirate_from(1050, custom('A5'), withdraw_rate)
myProtocol.dispense_to(50, custom('A5'), infusion_rate)

myProtocol.dispense_to(200, chip_1('A1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A3'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A5'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A7'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A9'), infusion_rate)

myProtocol.dispense_to(0, custom('A1'), infusion_rate)

myProtocol.deactivate_block()
myProtocol.close_lid()
myProtocol.set_lid_temp(37)
myProtocol.set_block_temp(37, 30)
myProtocol.deactivate_lid()
myProtocol.set_block_temp(4, 15)
myProtocol.open_lid()
myProtocol.deactivate_block()

myProtocol.mid_wash(rate = 50)
myProtocol.fill_syringe_with_water(50)
myProtocol.end_of_protocol()