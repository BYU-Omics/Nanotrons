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

myProtocol.dispense_to(100, corning_384('F7'))
myProtocol.dispense_to(100, corning_384('F8'))
myProtocol.dispense_to(100, corning_384('F9'))
myProtocol.dispense_to(100, corning_384('F10'))
myProtocol.dispense_to(100, corning_384('F11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(300, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))


myProtocol.dispense_to(50, corning_384('G7'))
myProtocol.dispense_to(50, corning_384('G8'))
myProtocol.dispense_to(50, corning_384('G9'))
myProtocol.dispense_to(50, corning_384('G10'))
myProtocol.dispense_to(50, corning_384('G11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(120, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))


myProtocol.dispense_to(20, corning_384('H7'))
myProtocol.dispense_to(20, corning_384('H8'))
myProtocol.dispense_to(20, corning_384('H9'))
myProtocol.dispense_to(20, corning_384('H10'))
myProtocol.dispense_to(20, corning_384('H11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(60, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(10, corning_384('I7'))
myProtocol.dispense_to(10, corning_384('I8'))
myProtocol.dispense_to(10, corning_384('I9'))
myProtocol.dispense_to(10, corning_384('I10'))
myProtocol.dispense_to(10, corning_384('I11'))

myProtocol.mid_wash()

myProtocol.aspirate_from(30, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))

myProtocol.dispense_to(5, corning_384('J7'))
myProtocol.dispense_to(5, corning_384('J8'))
myProtocol.dispense_to(5, corning_384('J9'))
myProtocol.dispense_to(5, corning_384('J10'))
myProtocol.dispense_to(5, corning_384('J11'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()