print("In protocol_2.py")

try:
    # Works when we're at the top lovel and we call main.py
    from coordinator import Coordinator
except ImportError:
    # If we're not in the top level
    # And we're trying to call the file directly
    import sys
    # add the submodules to $PATH
    # sys.path[0] is the current file's path
    path = sys.path[0]#"c:\\Users\\RTK Lab\\Documents\\PJ\\nanopots_dev\\OT2"
    print(path)

    sys.path.append(sys.path[0] + '\\..')
    from coordinator import Coordinator

filename = sys.argv[1]

myProtocol = Coordinator() 

myProtocol.load_labware_setup(filename)

# chip = myProtocol.myLabware.chip_list[0].get_location_by_nickname
corning = myProtocol.myLabware.plate_list[0].get_location_by_nickname
custom = myProtocol.myLabware.plate_list[1].get_location_by_nickname
custom_small = myProtocol.myLabware.plate_list[2].get_location_by_nickname

# ADJUSTING SYRINGE

myProtocol.ot_control.move({'B': -125})


myProtocol.goto_and_aspirate(50, custom('A2'))

# Aspirate 3100 nL from small well A1 #120 uM NaFL
myProtocol.goto_and_aspirate(3100, custom_small('A1'))

# Dispense 50 nL into well A1 #Waste
myProtocol.goto_and_dispense(50, custom('A1'))

# Dispense 1000 nL into Corning wells A6, B6, and C6
myProtocol.goto_and_dispense(1000, corning('K19'))
myProtocol.goto_and_dispense(1000, corning('L19'))
myProtocol.goto_and_dispense(1000, corning('M19'))

# Dispense 100 nL into well A1 #Waste
myProtocol.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from well A2 #Air gap
myProtocol.goto_and_aspirate(50, custom('A2'))

# Aspirate 2100 nL from small well B1 #120 uM NaFL
myProtocol.goto_and_aspirate(2100, custom_small('A1'))

# Dispense 50 nL into well A1 #Waste
myProtocol.goto_and_dispense(50, custom('A1'))

# Dispense 1000 nL into Corning wells D6 and E6
myProtocol.goto_and_dispense(1000, corning('N19'))
myProtocol.goto_and_dispense(1000, corning('O19'))

# Dispense 100 nL into well A1 #Waste
myProtocol.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from well A2 #Air gap
myProtocol.goto_and_aspirate(50, custom('A2'))

# Aspirate 2600 nL from small well C1 #0.24 mM NaFL
myProtocol.goto_and_aspirate(2600, custom_small('B1'))

# Dispense 50 nL into well A1 #Waste
myProtocol.goto_and_dispense(50, custom('A1'))

# Dispense 500 nL into Corning wells A7, B7, C7, D7 and E7
myProtocol.goto_and_dispense(500, corning('K20'))
myProtocol.goto_and_dispense(500, corning('L20'))
myProtocol.goto_and_dispense(500, corning('M20'))
myProtocol.goto_and_dispense(500, corning('N20'))
myProtocol.goto_and_dispense(500, corning('O20'))

# Dispense 100 nL into well A1 #Waste
myProtocol.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from well A2 #Air gap
myProtocol.goto_and_aspirate(50, custom('A2'))
# Aspirate 600 nL from small well G1 #1.2 mM NaFL
myProtocol.goto_and_aspirate(600, custom_small('C1'))

# Dispense 50 nL into well A1 #Waste
myProtocol.goto_and_dispense(50, custom('A1'))

# Dispense 100 nL into Corning wells A11, B11, C11, D11 and E11
myProtocol.goto_and_dispense(100, corning('K21'))
myProtocol.goto_and_dispense(100, corning('L21'))
myProtocol.goto_and_dispense(100, corning('M21'))
myProtocol.goto_and_dispense(100, corning('N21'))
myProtocol.goto_and_dispense(100, corning('O21'))

# Dispense 100 nL into well A1 #Waste
myProtocol.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from well A2 #Air gap
myProtocol.goto_and_aspirate(50, custom('A2'))

# Aspirate 350 nL from small well H1 #2.4 mM NaFL
myProtocol.goto_and_aspirate(350, custom_small('D1'))

# Dispense 50 nL into well A1 #Waste
myProtocol.goto_and_dispense(50, custom('A1'))

# Dispense 50 nL into Corning wells A12, B12, C12, D12 and E12
myProtocol.goto_and_dispense(50, corning('K22'))
myProtocol.goto_and_dispense(50, corning('L22'))
myProtocol.goto_and_dispense(50, corning('M22'))
myProtocol.goto_and_dispense(50, corning('N22'))
myProtocol.goto_and_dispense(50, corning('O22'))

# Dispense 100 nL into well A1 #Waste
myProtocol.goto_and_dispense(100, custom('A1')) 