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
	'protocolName': 'Aspiration_test_with_chip_01-03-2022.py', 
	'author': 'Alejandro Brozalez', 
	'description': 'Aspiration test with chip' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('Aspiration_test-01-22.json')

micropots_3 = chips[0].get_location_by_nickname
custom = plates[0]

# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------

custom = custom.pot_position_for_protocol 

# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_syringe_model("HAMILTON_175")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(5000, clean_water)

myProtocol.dispense_to(500, micropots_3('A1'))

myProtocol.dispense_to(500, micropots_3('A2'))

myProtocol.dispense_to(500, micropots_3('A3'))

myProtocol.dispense_to(500, micropots_3('A4'))

myProtocol.dispense_to(500, micropots_3('A5'))

myProtocol.dispense_to(500, micropots_3('B1'))

myProtocol.dispense_to(500, micropots_3('B2'))

myProtocol.dispense_to(500, micropots_3('B3'))

myProtocol.dispense_to(500, micropots_3('B4'))

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()