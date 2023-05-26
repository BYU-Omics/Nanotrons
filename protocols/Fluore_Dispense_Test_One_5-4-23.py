       
"""

"""

import sys
import time 

try:
    from api import *
except ImportError:
    sys.path.append(sys.path[0] + '\\..') # current directory
    from api import *

myProtocol = Api() # creates a protocol object using the Api

metadata = {
	'protocolName': 'Fluore_Dispense_Test_4-26-23.py', 
	'author': 'Nathaniel Axtell', 
	'description': 'fluorescein dispensing characterization with new standards' 
}



# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

# the load_labware_setup method uses the calibration file information to 
# create instances of the Model class to represent each piece of labware on the deck
# and returns them in a list
models = myProtocol.load_labware_setup('4-25-23_fluoro_calibration.json')

'''
WARNING: Make sure the following indices match the order in the calibration file!!!
'''

# the well_position_for_protocol method takes a string of an alphanumeric well designation
# and retrieves xyz coordinates corresponding to a well's 
corning_384 = models[0].well_position_for_protocol
custom = models[1].well_position_for_protocol
custom_small = models[2].well_position_for_protocol


# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------



# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('B2')
clean_water = custom('C3')
dip_water = custom('D4')
empty_well = custom('D1')

infusion_rate = 50  #nL/s
withdraw_rate = 50  #nL/s
wash_rate = 100 #nL/s

wells_per_group = 5 
group_01_wells = ['L13','M13','N13','O13','P13']
group_02_wells = ['L14','M14','N14','O14','P14']
group_03_wells = ['L15','M15','N15','O15','P15']
group_04_wells = ['L16','M16','N16','O16','P16']
group_05_wells = ['L17','M17','N17','O17','P17']
mix_1 = custom_small('A2') # 1 mM
mix_2 = custom_small('C2') # 2 mM
mix_3 = custom_small('E2') # 5 mM
mix_4 = custom_small('G2') # 10 mM
mix_5 = custom_small('I2') # 20 mM



myProtocol.set_syringe_model("HAMILTON_1701.json")

myProtocol.set_washing_positions(clean_water, wash_water, waste_water)

print("\nStarting with syringe wash!\n")
myProtocol.start_wash(wash_rate) # <- You can input a custom flow rate in nL/s if desired. 
# ------------START OF PROTOCOL---------------------------------
 

# mix_1 group dispense
print("\nStarting mix_1 group dispense!")
print("Time: ", {time.strftime("%H:%M:%S", time.gmtime())}, "\n")

target_delivery_volume = 100
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_1, withdraw_rate)
for well in group_01_wells:
    myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else    
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_2 group dispense
print("\nStarting mix_2 group dispense!")
print("Time: ", {time.strftime("%H:%M:%S", time.gmtime())}, "\n")

target_delivery_volume = 50
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_2, withdraw_rate)
for well in group_02_wells:
    myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_3 group dispense
print("\nStarting mix_3 group dispense!")
print("Time: ", {time.strftime("%H:%M:%S", time.gmtime())}, "\n")

target_delivery_volume = 20
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_3, withdraw_rate)
for well in group_03_wells:
    myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_4 group dispense
print("\nStarting mix_4 group dispense!")
print("Time: ", {time.strftime("%H:%M:%S", time.gmtime())}, "\n")

target_delivery_volume = 10
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_4, withdraw_rate)
for well in group_04_wells:
    myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_5 group dispense
print("\nStarting mix_5 group dispense!")
print("Time: ", {time.strftime("%H:%M:%S", time.gmtime())}, "\n")

target_delivery_volume = 5
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_5, withdraw_rate)
for well in group_05_wells:
    myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(0, empty_well, infusion_rate) # Code goes crazy on first command of for loop, this line protects everything else
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water(50) # <- You can input a custom flow rate in nL/s if desired.
myProtocol.end_of_protocol()