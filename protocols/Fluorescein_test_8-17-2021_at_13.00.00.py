"""
    Template for writing protocols. 

    Instructions: 
        'aspirate_from' assumes nanoliters
        'dispense_to' 
"""

#---------------------------IMPORT THE USED LIBRARIES-------------------------------

import sys
LABWARE = sys.argv[1]
CURRENT_DIRECTORY = sys.path.append(sys.path[0] + '\\..')

try:
    from api import *
except ImportError:
    CURRENT_DIRECTORY
    from api import *

#---------------------------CREATE A PROTOCOL OBJECT--------------------------------

myProtocol = Api() 

#-------------------IMPORT THE CALIBRATION FOR THIS PROTOCOL: 
            # This is done from the executer, it is specified on the GUI.
            # Chips and plates are loaded in the order they were calibrated.""" 

chips, plates = myProtocol.load_labware_setup(LABWARE)

#---------------------------END OF HEADING------------------------------------------

# ------------START OF PROTOCOL CONFIGURATION--------------------------------

metadata = {
    'protocolName': 'Nanotrons Test',
    'author': 'Alejandro Brozalez',
    'description': 'Testing robot'
}

# Labware file loaded: Test_for_protocols.json

corning_384 = plates[0]
custom_small = plates[1]
custom = plates[2]

# If there are any depth voided they are listed here

myProtocol.void_plate_depth(custom, True)

# -----------PREPROTOCOL SETUP-------------------

corning_384 = plates[0].pot_position_for_protocol
custom_small = plates[1].pot_position_for_protocol
custom = plates[2].pot_position_for_protocol

# Designated wells for washing tip

waste_water = custom('A1')
wash_water = custom('A2')
clean_water = custom('A3')

myProtocol.set_washing_positions(clean_water, wash_water, waste_water)

myProtocol.start_wash()

#----------START OF PROTOCOL----------------------------------------

myProtocol.aspirate_from(500, custom_small('A1'))

myProtocol.dispense_to(100, corning_384('A16'))
myProtocol.dispense_to(100, corning_384('B16'))
myProtocol.dispense_to(100, corning_384('C16'))
myProtocol.dispense_to(100, corning_384('D16'))
myProtocol.dispense_to(100, corning_384('E16'))

myProtocol.mid_wash()

myProtocol.aspirate_from(250, custom_small('B1'))

myProtocol.dispense_to(50, corning_384('A19'))
myProtocol.dispense_to(50, corning_384('B19'))
myProtocol.dispense_to(50, corning_384('C19'))
myProtocol.dispense_to(50, corning_384('D19'))
myProtocol.dispense_to(50, corning_384('E19'))

myProtocol.mid_wash()

myProtocol.aspirate_from(100, custom_small('C1'))

myProtocol.dispense_to(20, corning_384('A20'))
myProtocol.dispense_to(20, corning_384('B20'))
myProtocol.dispense_to(20, corning_384('C20'))
myProtocol.dispense_to(20, corning_384('D20'))
myProtocol.dispense_to(20, corning_384('E20'))

myProtocol.mid_wash()

myProtocol.aspirate_from(50, custom_small('D1'))

myProtocol.dispense_to(10, corning_384('A21'))
myProtocol.dispense_to(10, corning_384('B21'))
myProtocol.dispense_to(10, corning_384('C21'))
myProtocol.dispense_to(10, corning_384('D21'))
myProtocol.dispense_to(10, corning_384('E21'))

myProtocol.mid_wash()

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()