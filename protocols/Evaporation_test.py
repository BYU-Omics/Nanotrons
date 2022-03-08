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
	'author': 'Alejandro Brozalez', 
	'description': 'Evap test.' 
}

# ----------IMPORT THE CALIBRATION FOR THIS PROTOCOL: this is done from the executer, it is specified on the GUI

chips, plates = myProtocol.load_labware_setup('Evap_Test.json')

# ------------END OF HEADING-------------------------------------------------

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED-----------

# Labware file loaded: Test_for_protocols.json

micropots_3_top = chips[0].pot_position_for_protocol 
micropots_3_btm = chips[1].pot_position_for_protocol 
corning_384 = plates[0].pot_position_for_protocol 
custom = plates[1].pot_position_for_protocol 

chips = [micropots_3_top, micropots_3_btm]

# -----------PREPROTOCOL SETUP-------------------

corning_384 = corning_384.pot_position_for_protocol 
custom = custom.pot_position_for_protocol 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_syringe_model("HAMILTON_175")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

#----------START OF PROTOCOL----------------------------------------

for chip in chips:
    myProtocol.aspirate_from(100, custom('A2'))

    myProtocol.aspirate_from(1000, custom('A1'))

    myProtocol.dispense_to(1000, chip('A1'))

    myProtocol.aspirate_from(1000, custom('A1'))

    myProtocol.dispense_to(1000, chip('C1'))

    myProtocol.aspirate_from(1000, custom('A1'))

    myProtocol.dispense_to(1000, chip('A9'))

    myProtocol.aspirate_from(1000, custom('A1'))

    myProtocol.dispense_to(1000, chip('C9'))

    myProtocol.aspirate_from(1400, custom('A1'))

    myProtocol.dispense_to(200, chip('A2'))
    myProtocol.dispense_to(200, chip('A3'))
    myProtocol.dispense_to(200, chip('A4'))
    myProtocol.dispense_to(200, chip('A5'))
    myProtocol.dispense_to(200, chip('A6'))
    myProtocol.dispense_to(200, chip('A7'))
    myProtocol.dispense_to(200, chip('A8'))

    myProtocol.aspirate_from(1400, custom('A1'))

    myProtocol.dispense_to(200, chip('B2'))
    myProtocol.dispense_to(200, chip('B3'))
    myProtocol.dispense_to(200, chip('B4'))
    myProtocol.dispense_to(200, chip('B5'))
    myProtocol.dispense_to(200, chip('B6'))
    myProtocol.dispense_to(200, chip('B7'))
    myProtocol.dispense_to(200, chip('B8'))

    myProtocol.aspirate_from(1400, custom('A1'))

    myProtocol.dispense_to(200, chip('C2'))
    myProtocol.dispense_to(200, chip('C3'))
    myProtocol.dispense_to(200, chip('C4'))
    myProtocol.dispense_to(200, chip('C5'))
    myProtocol.dispense_to(200, chip('C6'))
    myProtocol.dispense_to(200, chip('C7'))
    myProtocol.dispense_to(200, chip('C8'))


myProtocol.close_lid()
myProtocol.set_lid_temp(37)
myProtocol.set_block_temp(37, 90)
myProtocol.deactivate_lid()
myProtocol.set_block_temp(4, 7)
myProtocol.open_lid()
myProtocol.take_picture()


for number in range(0, 55):
    myProtocol.take_picture(micropots_3_top('B2'))
    myProtocol.take_picture(micropots_3_top('B5'))
    myProtocol.take_picture(micropots_3_top('B8'))

    myProtocol.take_picture(micropots_3_btm('B2'))
    myProtocol.take_picture(micropots_3_btm('B5'))
    myProtocol.take_picture(micropots_3_btm('B8'))

#--------------END OF PROTOCOL--------------

myProtocol.dispense_to(0, custom('A1'))
myProtocol.adjust_syringe()

myProtocol.end_of_protocol()