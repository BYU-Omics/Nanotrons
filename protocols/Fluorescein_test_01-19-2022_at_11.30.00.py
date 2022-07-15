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
	'author': 'Alejandro Brozalez / Yhann Masbernat', 
	'description': 'Fluorescein test.' 
}

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

chips, plates = myProtocol.load_labware_setup('flou_test_7_6_2022.json')

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

infusion_rate = 50  #nL/s
withdraw_rate = 50  #nL/s

myProtocol.set_syringe_model("HAMILTON_175.json")

myProtocol.set_washing_positions(custom('A3'), custom('A2'), custom('A1'))

myProtocol.start_wash(50)

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(600, custom_small('A1'), withdraw_rate)
myProtocol.dispense_to(50, custom_small('A1'), infusion_rate)
myProtocol.dispense_to(0, custom('D1'), infusion_rate)

myProtocol.dispense_to(100, corning_384('F16'), infusion_rate)
myProtocol.dispense_to(100, corning_384('F17'), infusion_rate)
myProtocol.dispense_to(100, corning_384('F18'), infusion_rate)
myProtocol.dispense_to(100, corning_384('F19'), infusion_rate)
myProtocol.dispense_to(100, corning_384('F20'), infusion_rate)

myProtocol.mid_wash(rate = 50)

myProtocol.aspirate_from(350, custom_small('B1'), withdraw_rate)
myProtocol.dispense_to(50, custom_small('B1'), infusion_rate)
myProtocol.dispense_to(0, custom('D1'), infusion_rate)

myProtocol.dispense_to(50, corning_384('G16'), infusion_rate)
myProtocol.dispense_to(50, corning_384('G17'), infusion_rate)
myProtocol.dispense_to(50, corning_384('G18'), infusion_rate)
myProtocol.dispense_to(50, corning_384('G19'), infusion_rate)
myProtocol.dispense_to(50, corning_384('G20'), infusion_rate)

myProtocol.mid_wash(rate = 50)
myProtocol.aspirate_from(170, custom_small('C1'), withdraw_rate)
myProtocol.dispense_to(50, custom_small('C1'), infusion_rate)
myProtocol.dispense_to(0, custom('D1'), infusion_rate)

myProtocol.dispense_to(20, corning_384('H16'), infusion_rate)
myProtocol.dispense_to(20, corning_384('H17'), infusion_rate)
myProtocol.dispense_to(20, corning_384('H18'), infusion_rate)
myProtocol.dispense_to(20, corning_384('H19'), infusion_rate)
myProtocol.dispense_to(20, corning_384('H20'), infusion_rate)

myProtocol.mid_wash(rate = 50)

myProtocol.aspirate_from(110, custom_small('D1'), withdraw_rate)
myProtocol.dispense_to(50, custom_small('D1'), infusion_rate)
myProtocol.dispense_to(0, custom('D1'), infusion_rate)

myProtocol.dispense_to(10, corning_384('I16'), infusion_rate)
myProtocol.dispense_to(10, corning_384('I17'), infusion_rate)
myProtocol.dispense_to(10, corning_384('I18'), infusion_rate)
myProtocol.dispense_to(10, corning_384('I19'), infusion_rate)
myProtocol.dispense_to(10, corning_384('I20'), infusion_rate)

myProtocol.mid_wash(rate = 50)
myProtocol.aspirate_from(80, custom_small('D1'), withdraw_rate)
myProtocol.dispense_to(50, custom_small('D1'), infusion_rate)
myProtocol.dispense_to(0, custom('D1'), infusion_rate)

myProtocol.dispense_to(5, corning_384('J16'), infusion_rate)
myProtocol.dispense_to(5, corning_384('J17'), infusion_rate)
myProtocol.dispense_to(5, corning_384('J18'), infusion_rate)
myProtocol.dispense_to(5, corning_384('J19'), infusion_rate)
myProtocol.dispense_to(5, corning_384('J20'), infusion_rate)

myProtocol.mid_wash(rate = 50)

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water(50)
myProtocol.end_of_protocol()