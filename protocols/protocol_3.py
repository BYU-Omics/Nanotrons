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

myApp = Coordinator() 

myApp.load_labware_setup(filename)

chip = myApp.myLabware.chip_list[0].get_location_by_nickname
# corning = myApp.myLabware.plate_list[0].get_location_by_nickname
custom = myApp.myLabware.plate_list[1].get_location_by_nickname
# custom_small = myApp.myLabware.plate_list[2].get_location_by_nickname

# ADJUSTING SYRINGE

myApp.ot_control.move({'B': -125})

myApp.set_block_temp(4, 0)

myApp.goto_and_aspirate(3500, custom('A3'))

myApp.goto_and_dispense(50, custom('A1'))

myApp.goto_and_dispense(1000, chip('A1'))
myApp.goto_and_dispense(200, chip('A2'))
myApp.goto_and_dispense(200, chip('A3'))
myApp.goto_and_dispense(200, chip('A4'))
myApp.goto_and_dispense(200, chip('A5'))
myApp.goto_and_dispense(200, chip('A6'))
myApp.goto_and_dispense(200, chip('A7'))
myApp.goto_and_dispense(200, chip('A8'))
myApp.goto_and_dispense(1000, chip('A9'))

myApp.goto_and_dispense(50, custom('A1'))

myApp.goto_and_aspirate(1900, custom('A3'))

myApp.goto_and_dispense(50, custom('A1'))

myApp.goto_and_dispense(200, chip('B1'))
myApp.goto_and_dispense(200, chip('B2'))
myApp.goto_and_dispense(200, chip('B3'))
myApp.goto_and_dispense(200, chip('B4'))
myApp.goto_and_dispense(200, chip('B5'))
myApp.goto_and_dispense(200, chip('B6'))
myApp.goto_and_dispense(200, chip('B7'))
myApp.goto_and_dispense(200, chip('B8'))
myApp.goto_and_dispense(200, chip('B9'))

myApp.goto_and_dispense(50, custom('A1'))

myApp.goto_and_aspirate(3500, custom('A3'))

myApp.goto_and_dispense(50, custom('A1'))

myApp.goto_and_dispense(1000, chip('C1'))
myApp.goto_and_dispense(200, chip('C2'))
myApp.goto_and_dispense(200, chip('C3'))
myApp.goto_and_dispense(200, chip('C4'))
myApp.goto_and_dispense(200, chip('C5'))
myApp.goto_and_dispense(200, chip('C6'))
myApp.goto_and_dispense(200, chip('C7'))
myApp.goto_and_dispense(200, chip('C8'))
myApp.goto_and_dispense(1000, chip('C9'))

myApp.goto_and_dispense(50, custom('A1'))

myApp.close_lid()

myApp.set_lid_temp(70)
myApp.set_block_temp(70, 180)

myApp.deactivate_lid()

myApp.set_block_temp(4, 0)

myApp.open_lid()