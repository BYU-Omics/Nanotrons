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
	'protocolName': 'Fluore_Dispense_Test_2-9-23.py', 
	'author': 'Nathaniel Axtell', 
	'description': 'fluorescein dispensing characterization with new standards' 
}



# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------

plates = myProtocol.load_labware_setup('Nathaniel_NaFl_Calibration_2-13-23.json')

corning_384 = plates[0].well_position_for_protocol
custom = plates[1].well_position_for_protocol
custom_small = plates[2].well_position_for_protocol


# If the depth has been voided for any of the plates, this is specified here:

# -----------PREPROTOCOL SETUP-------------------



# Designated wells for washing tip
waste_water = custom('A1')
wash_water = custom('B2')
clean_water = custom('C3')
dip_water = custom('D4')

infusion_rate = 50  #nL/s
withdraw_rate = 50  #nL/s
wash_rate = 100 #nL/s

wells_per_group = 6 
group_01_wells = ['A2','A4','A6','A8','A10','A12']
group_02_wells = ['B2','B4','B6','B8','B10','B12']
group_03_wells = ['C2','C4','C6','C8','C10','C12']
group_04_wells = ['D2','D4','D6','D8','D10','D12']
group_05_wells = ['E2','E4','E6','E8','E10','E12']
group_06_wells = ['F2','F4','F6','F8','F10','F12']
mix_1 = custom_small('A2') # 1 mM
mix_2 = custom_small('B2') # 2 mM
mix_3 = custom_small('C2') # 5 mM
mix_4 = custom_small('D2') # 10 mM
mix_5 = custom_small('E2') # 20 mM



myProtocol.set_syringe_model("HAMILTON_1701.json")

myProtocol.set_washing_positions(clean_water, wash_water, waste_water)

myProtocol.start_wash(wash_rate) # <- You can input a custom flow rate in nL/s if desired. 
# ------------START OF PROTOCOL---------------------------------
 

# mix_1 group dispense
target_delivery_volume = 100
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_1, withdraw_rate)
for well in group_01_wells:
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe

# mix_1 individual dispense
myProtocol.aspirate_from(100, mix_1, withdraw_rate) # creates a 100 nL buffer volume in the capillary
for well in group_06_wells:
    myProtocol.aspirate_from(target_delivery_volume, mix_1, withdraw_rate) # get target amount
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(100, waste_water, infusion_rate) # removes the 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_2 group dispense
target_delivery_volume = 50
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_2, withdraw_rate)
for well in group_02_wells:
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_3 group dispense
target_delivery_volume = 20
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_3, withdraw_rate)
for well in group_03_wells:
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_4 group dispense
target_delivery_volume = 10
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_4, withdraw_rate)
for well in group_04_wells:
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



# mix_5 group dispense
target_delivery_volume = 5
aspirate_volume = 100 + target_delivery_volume*wells_per_group # total needed plus 100 nL buffer volume
myProtocol.aspirate_from(aspirate_volume, mix_5, withdraw_rate)
for well in group_05_wells:
    myProtocol.dispense_to(0, dip_water, infusion_rate) # wash off outside of tip
    myProtocol.dispense_to(target_delivery_volume, corning_384(well), infusion_rate) # drop off target volume
myProtocol.dispense_to(100, waste_water, infusion_rate) #removes 100 nL buffer volume

myProtocol.mid_wash(wash_rate) # clean capillary and reset syringe



#--------------END OF PROTOCOL--------------

myProtocol.fill_syringe_with_water(50) # <- You can input a custom flow rate in nL/s if desired.
myProtocol.end_of_protocol()