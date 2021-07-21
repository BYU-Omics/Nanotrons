print("In protocol_1.py")

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

myApp = Coordinator() 

myApp.load_labware_setup(filename)

# chip = myApp.myLabware.chip_list[0].get_location_by_nickname

custom = myApp.myLabware.plate_list[0].get_location_by_nickname
custom_small = myApp.myLabware.plate_list[1].get_location_by_nickname
corning = myApp.myLabware.plate_list[2].get_location_by_nickname

# ADJUSTING SYRINGE

myApp.ot_control.move({'B': -125})

# STARTTING PROTOCOL

# Aspirate 50 nL from custom A2 #Air gap
myApp.goto_and_aspirate(100, custom('A2'))

# Aspirate 600 nL from small well A1 #1.2 mM NaFL
myApp.goto_and_aspirate(600, custom_small('A1'))

# Dispense 50 nL into custom A1 #Waste
myApp.goto_and_dispense(50, custom('A1'))

# Dispense 100 nL into Corning wells A18, B18, C18, D18 and E18
myApp.goto_and_dispense(100, corning('F14'))
myApp.goto_and_dispense(100, corning('G14'))
myApp.goto_and_dispense(100, corning('H14'))
myApp.goto_and_dispense(100, corning('I14'))
myApp.goto_and_dispense(100, corning('J14'))

# Dispense 100 nL into custom A1 #Waste
myApp.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from custom A2 #Air gap
myApp.goto_and_aspirate(50, custom('A2'))

# Aspirate 350 nL from small well B1 #2.4 mM NaFL
myApp.goto_and_aspirate(350, custom_small('B1'))

# Dispense 50 nL into custom A1 #Waste
myApp.goto_and_dispense(50, custom('A1'))

# Dispense 50 nL into Corning wells A19, B19, C19, D19 and E19
myApp.goto_and_dispense(50, corning('F15'))
myApp.goto_and_dispense(50, corning('G15'))
myApp.goto_and_dispense(50, corning('H15'))
myApp.goto_and_dispense(50, corning('I15'))
myApp.goto_and_dispense(50, corning('J15'))

# Dispense 100 nL into custom A1 #Waste
myApp.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from custom A2 #Air gap
myApp.goto_and_aspirate(50, custom('A2'))

# Aspirate 200 nL from small well C1 #6.0 mM NaFL
myApp.goto_and_aspirate(200, custom_small('C1'))

# Dispense 50 nL into custom A1 #Waste
myApp.goto_and_dispense(50, custom('A1'))

# Dispense 20 nL into Corning wells A20, B20, C20, D20 and E20
myApp.goto_and_dispense(20, corning('F16'))
myApp.goto_and_dispense(20, corning('G16'))
myApp.goto_and_dispense(20, corning('H16'))
myApp.goto_and_dispense(20, corning('I16'))
myApp.goto_and_dispense(20, corning('J16'))

# Dispense 100 nL into custom A1 #Waste
myApp.goto_and_dispense(100, custom('A1'))

# Aspirate 50 nL from custom A2 #Air gap
myApp.goto_and_aspirate(50, custom('A2'))

# Aspirate 150 nL from small well D1 #10.0 mM NaFL
myApp.goto_and_aspirate(150, custom_small('D1'))

# Dispense 50 nL into custom A1 #Waste
myApp.goto_and_dispense(50, custom('A1'))

# Dispense 10 nL into Corning wells A21, B21, C21, D21 and E21
myApp.goto_and_dispense(10, corning('F17'))
myApp.goto_and_dispense(10, corning('G17'))
myApp.goto_and_dispense(10, corning('H17'))
myApp.goto_and_dispense(10, corning('I17'))
myApp.goto_and_dispense(10, corning('J17'))

# Dispense 100 nL into custom A1 #Waste
myApp.goto_and_dispense(50, custom('A1'))