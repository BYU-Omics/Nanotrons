# Nanotrons
OT2 project

## Overview 

Nanotrons allows [Opentrons OT2 pippeting robot](https://opentrons.com/ot-2/) OT2 pippeting robot, [Thermocycler](https://opentrons.com/modules/thermocycler-module), and [Tempdeck](https://opentrons.com/modules/temperature-module/) modules users to handle small amounts of volumes with a modified pipette and API for the OT2

This repository contains the source code for the Nanotrons API and OT GUI. You can find the Opentrons repository [here](https://github.com/Opentrons/opentrons). 

## Installation

We are working to make it as easy as possible.

Download the IDE of your prefference and install Python 3. Once you are all set continue to the following commands

```python
>>> pip install opentrons # Either would work
>>> pip3 install opentrons
>>> git clone https://github.com/BYU-Omics/Nanotrons.git
```
Then install all the neccessary packages with the correct versions. There migth be some packages that will through an error if its not installed correctly, but sometimes there is no error messages. These are examples of some of the libraries at the time of creating this repository. Use ```python pip list ``` to make sure they match.  

Examples:
```python
Jinja2                3.0.1
Flask                 2.0.1   
Flask-SocketIO        4.3.1   
pygame                1.9.6
python-engineio       3.13.2
python-socketio       4.6.0
opencv-python         4.5.2.54
opentrons             4.4.0
opentrons-shared-data 4.4.0
Werkzeug              2.0.1
Scipy                 1.7.1
```

## GUI

The GUI(Graphical User Interface) can be opened from a [python file](./web_app.py) using the Flask library. It can be run as a localhost on 'http://localhost:5000/'


# Calibration

1) Connect to the robot using a [USB to TTL adaptor](https://www.amazon.com/Converter-Terminated-Galileo-BeagleBone-Minnowboard/dp/B06ZYPLFNB/ref=asc_df_B06ZYPLFNB/?tag=hyprod-20&linkCode=df0&hvadid=309773039951&hvpos=&hvnetw=g&hvrand=7153277742910700235&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9029857&hvtargid=pla-599566704604&psc=1).
2) Make sure the Thermocycler is connected to the computer, not the Raspberry Pi board on the OT2
3) Make sure both cameras, one on the OT2 and the microscope, are also connected to the computer. 
4) Start the robot with the switch on the 'raspi' mode. 
5) Once the robot has homed the Z and A axes whe the blue botton is settled install a pipette. We use the P20 model. 
6) Home the robot from the Opentrons app.
7) Flip the switch to the Debug mode.
8) Run web_app.py. 

# Protocol example 

File: [protocol_1.py](https://github.com/BYU-Omics/Nanotrons/blob/master/protocols/protocol_1.py)

# Contribution

Our lab would be happy to add features to the GUI. If there are questions about the OT2 you would most likely find the answer on the support page. [Example](https://support.opentrons.com/en/articles/2831465-using-the-ot-2-s-camera)

# Setting example

![IMG-6306](https://user-images.githubusercontent.com/78994282/126675111-b10758fb-d809-47ed-8b32-7ee8edd3b83c.jpg)

![IMG-6307](https://user-images.githubusercontent.com/78994282/126675464-7a01ee2c-23be-4b81-91f2-bf61e17e8e93.jpg)

![IMG-6309](https://user-images.githubusercontent.com/78994282/126675468-3a6d0d3f-97c7-47e8-86d9-1e6ccb74bccf.jpg)

![IMG-6311](https://user-images.githubusercontent.com/78994282/126675753-04d3f52f-b761-465c-a594-ae208aaa2a38.jpg)






