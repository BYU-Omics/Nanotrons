# Nanotrons
OT2 project

## Overview 

Nanotrons allows Opentrons OT2 pippeting robot, Thermocycler, and Tempdeck modules users to handle small amounts of volumes with a modified pipette and API for the OT2

This repository contains the source code for the Nanotrons API and OT GUI.

## GUI

The GUI(Graphical User Interface) can be opened from a python file [Source code](./web_app.py) using the Flask library. It can be run as a localhost on 'http://localhost:5000/'

```python
# ADJUSTING SYRINGE

myApp.ot_control.move({'B': -125})

# STARTTING PROTOCOL

# Aspirate 50 nL from custom A2 #Air gap
myApp.goto_and_aspirate(100, custom('A2'))

# Aspirate 600 nL from small well A1 #1.2 mM NaFL
myApp.goto_and_aspirate(600, custom_small('A1'))
```
