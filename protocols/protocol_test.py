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

myApp.goto_and_dispense(0, corning('F14'))
myApp.goto_and_dispense(0, corning('G14'))
myApp.goto_and_dispense(0, corning('H14'))
myApp.goto_and_dispense(0, corning('I14'))
myApp.goto_and_dispense(0, corning('J14'))

myApp.disconnect_all()
