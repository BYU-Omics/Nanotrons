"""
    Template for writing protocols. 

    Instructions: 
        'aspirate_from' assumes nanoliters
        'dispense_to' 
"""

try:
    from api import *
except ImportError:
    CURRENT_DIRECTORY
    from api import *

# ----------CREATE A PROTOCOL OBJECT
myProtocol = Api() 

# ----------IMPORT THE CALIBRATION FOR THIS PROTOCOL: this is done from the executer, it is specified on the GUI
chips, plates = myProtocol.load_labware_setup(LABWARE)

# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED

# chip = chips[0].get_location_by_nickname
custom = plates[0].get_location_by_nickname
custom_small = plates[1].get_location_by_nickname
corning = plates[2].get_location_by_nickname

# ----------ADJUSTING SYRINGE

myProtocol.adjust_syringe(-125)

# --------------STARTTING PROTOCOL--------------

# Aspirate 50 nL from custom A2 #Air gap
myProtocol.aspirate_from(100, custom('A2'))

# Aspirate 600 nL from small well A1 #1.2 mM NaFL
myProtocol.aspirate_from(600, custom_small('A1'))

# Dispense 50 nL into custom A1 #Waste
myProtocol.dispense_to(50, custom('A1'))

# Dispense 100 nL into Corning wells A18, B18, C18, D18 and E18
myProtocol.dispense_to(100, corning('A6'))
myProtocol.dispense_to(100, corning('B6'))
myProtocol.dispense_to(100, corning('C6'))
myProtocol.dispense_to(100, corning('D6'))
myProtocol.dispense_to(100, corning('E6'))

# Dispense 100 nL into custom A1 #Waste
myProtocol.dispense_to(100, custom('A1'))

# Aspirate 50 nL from custom A2 #Air gap
myProtocol.aspirate_from(50, custom('A2'))

# Aspirate 350 nL from small well B1 #2.4 mM NaFL
myProtocol.aspirate_from(350, custom_small('B1'))

# Dispense 50 nL into custom A1 #Waste
myProtocol.dispense_to(50, custom('A1'))

# Dispense 50 nL into Corning wells A19, B19, C19, D19 and E19
myProtocol.dispense_to(50, corning('A7'))
myProtocol.dispense_to(50, corning('B7'))
myProtocol.dispense_to(50, corning('C7'))
myProtocol.dispense_to(50, corning('D7'))
myProtocol.dispense_to(50, corning('E7'))

# Dispense 100 nL into custom A1 #Waste
myProtocol.dispense_to(100, custom('A1'))

# Aspirate 50 nL from custom A2 #Air gap
myProtocol.aspirate_from(50, custom('A2'))

# Aspirate 200 nL from small well C1 #6.0 mM NaFL
myProtocol.aspirate_from(200, custom_small('C1'))

# Dispense 50 nL into custom A1 #Waste
myProtocol.dispense_to(50, custom('A1'))

# Dispense 20 nL into Corning wells A20, B20, C20, D20 and E20
myProtocol.dispense_to(20, corning('A8'))
myProtocol.dispense_to(20, corning('B8'))
myProtocol.dispense_to(20, corning('C8'))
myProtocol.dispense_to(20, corning('D8'))
myProtocol.dispense_to(20, corning('E8'))

# Dispense 100 nL into custom A1 #Waste
myProtocol.dispense_to(100, custom('A1'))

# Aspirate 50 nL from custom A2 #Air gap
myProtocol.aspirate_from(50, custom('A2'))

# Aspirate 150 nL from small well D1 #10.0 mM NaFL
myProtocol.aspirate_from(150, custom_small('D1'))

# Dispense 50 nL into custom A1 #Waste
myProtocol.dispense_to(50, custom('A1'))

# Dispense 10 nL into Corning wells A21, B21, C21, D21 and E21
myProtocol.dispense_to(10, corning('A9'))
myProtocol.dispense_to(10, corning('B9'))
myProtocol.dispense_to(10, corning('C9'))
myProtocol.dispense_to(10, corning('D9'))
myProtocol.dispense_to(10, corning('E9'))

# Dispense 100 nL into custom A1 #Waste
myProtocol.dispense_to(50, custom('A1'))

#--------------REQUIRED FOR THE END OF PROTOCOL--------------

myProtocol.end_of_protocol()
