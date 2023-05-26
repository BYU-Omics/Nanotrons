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
	'protocolName': 'Fluorescein_Calibration_Curve.py', 
	'author': 'Yhann Masbernat / Alex Buttars', 
	'description': 'Dispensing 20 uL aliquots of Fluorescein Standards.' 
}

'''
This Protocol is for adding 20 uL (20000 nL) of standards into wells of a 384-well plate
for a fluorescein calibration curve to help characterize our sub-microliter dispensing.  
'''


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

myProtocol.set_washing_positions(clean_water, wash_water, waste_water)

myProtocol.start_wash()

# ------------START OF PROTOCOL---------------------------------

myProtocol.aspirate_from(20000, custom_small('A1')) # 10 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A1'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A2'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A3'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A4'))

myProtocol.aspirate_from(20000, custom_small('A1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('A5'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('B1')) # 8 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B1'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B2'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B3'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B4'))

myProtocol.aspirate_from(20000, custom_small('B1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('B5'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('C1')) # 6 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C1'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C2'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C3'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C4'))

myProtocol.aspirate_from(20000, custom_small('C1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('C5'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('D1')) # 4 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D1'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D2'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D3'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D4'))

myProtocol.aspirate_from(20000, custom_small('D1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('D5'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('E1')) # 2 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E1'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E2'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E3'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E4'))

myProtocol.aspirate_from(20000, custom_small('E1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('E5'))

myProtocol.mid_wash()

myProtocol.aspirate_from(20000, custom_small('F1')) # 0 uM Solution
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F1'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F2'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F3'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F4'))

myProtocol.aspirate_from(20000, custom_small('F1'))
myProtocol.dispense_to(0, custom('D1'))
myProtocol.dispense_to(20000, corning_384('F5'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water()
myProtocol.end_of_protocol()