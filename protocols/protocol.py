#!/usr/bin/env python
# coding: utf-8

# In[15]:


#NanoPOTS Test
from opentrons import protocol_api
from coordinator import *
DEFAULT_PROFILE = "default_profile.json"
robot_portname_rasppi = '/dev/ttyUSB1'
tc_portname = '/dev/ttyACM1' 
protocol = Coordinator(joystick_profile=DEFAULT_PROFILE)

#Metadata
metadata = {
    'protocolName': 'NanoPOTS Test',
    'author': 'Tim Skaggs <tbskaggs@gmail.com>',
    'description': 'An attempt at trying to get the OT2 to run the protocol',
    'apiLevel':"2.9"

#Protocol Run Function.
def run(protocol):
    
    #Labware
    tc_mod = protocol.load_module('Thermocycler Module')
    plate = tc_mod.load_labware('corning_96_wellplate_360ul_flat',1)
    tiprack = protocol.load_labware('opentrons_96_tiprack_20ul',2)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml',3)
    
    #Pipettes
    left_pipette = protocol.load_instrument('p20_single_gen2','left',tip_racks=[tiprack])
    
    #Commands
    left_pipette.transfer(5, reservoir['A1'], plate.columns('1','2'))
        #reservoir['A1'] has RapiGest (0.2%) solution with 10 mM DTT in 50 mM ABC
    tc_mod.close_lid()
    tc_mod.set_block_temperature(70, hold_time_minutes=30, block_max_volume=5)
    tc_mod.open_lid()
    left_pipette.transfer(5, reservoir['A2'], plate.columns('1','2'))
        #reservoir['A2'] has IAA solution (30 mM in 50 mM ABC)
    tc_mod.close_lid()
    tc_mod.set_block_temperature(25, hold_time_minutes=30, block_max_volume=10)
    tc_mod.open_lid()
    left_pipette.transfer(5, reservoir['A3'], plate.columns('1','2'))
        #reservoir['A3'] enzyme solution containing 0.025 ug Lys-C in 50 mM ABC 
    left_pipette.transfer(5, reservoir['A4'], plate.columns('1','2'))
        #reservoir['A4'] enzyme solution containing 0.025 ug trypsin in 50 mM ABC
    tc_mod.close_lid()
    tc_mod.set_block_temperature(37, hold_time_minutes=720, block_max_volume=20)
    tc_mod.open_lid()
    left_pipette.distribute(5, reservoir['A5'], plate.columns('1','2'))
        #reservoir['A4'] formic acid solution (30% v/v)
    tc_mod.close_lid()
    tc_mod.set_block_temperature(25, hold_time_minutes=60, block_max_volume=25)
    tc_mod.open_lid()


# In[ ]:




