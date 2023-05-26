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
	'author': 'Alex Buttars & Yhann Masbernat', 
	'description': 'Evap test.' 
}
# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

labware = myProtocol.load_labware_setup('Run4_10_27.json')

custom = labware[0]
chip_1 = labware[1]
chip_2 = labware[2]
custom_small = labware[3]

# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------# 

chip_1 = chip_1.well_position_for_protocol
chip_2 = chip_2.well_position_for_protocol
custom = custom.well_position_for_protocol
custom_small = custom_small.well_position_for_protocol

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

#A Row Chip 1
myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A1'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A2'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A3'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A4'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A5'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A6'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A7'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A8'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('A9'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

#B Row
myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B1'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B2'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B3'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B4'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B5'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B6'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B7'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B8'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('B9'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

#C Row
myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C1'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C2'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C3'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C4'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C5'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C6'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C7'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C8'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_1('C9'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

#chip_2 row A
myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A1'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A2'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A3'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A4'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A5'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A6'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A7'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A8'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('A9'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

#B Row
myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B1'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B2'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B3'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B4'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B5'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B6'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B7'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B8'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('B9'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

#C Row
myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C1'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C2'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C3'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C4'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C5'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C6'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C7'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C8'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)

myProtocol.aspirate_from(300, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)
myProtocol.dispense_to(200, chip_2('C9'), infusion_rate)
myProtocol.dispense_to(50, custom('D1'), infusion_rate)



myProtocol.dispense_to(0, custom('A1'), infusion_rate)
myProtocol.mid_wash(rate = 50)
myProtocol.fill_syringe_with_water(50)

myProtocol.end_of_protocol()