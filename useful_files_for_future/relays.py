"""
Jacob Davis. Jan 12 2021

relays.py

OVERVIEW: this files controls three relay switches that will be used for the MS and LC contact 
closure. It is set up for all three relays to work, but at the time of this file's creation we 
should only need access to two relays.

WHAT IS A RELAY: A relay is just a simple switch that that can be flipped with a signal instead
of manually. This will allow us to connect and disconect the proper wires for the contact closure
to start the LC pump and the MS. 

The board we are using is called "RPI Relay Board" and is sold by waveshare.
https://www.waveshare.com/rpi-relay-board.htm
https://www.waveshare.com/wiki/RPi_Relay_Board
search "demo code" on the wiki page to access the source code in several languages.

If you go to the wiki page (see links above) you will see that generally this board is placed
directly on top of the Rpi and attaches to all the GPIO pins. However, we need to have a cooling
fan attached to the RPI which means this will not be able to mount on top of the RPI. 

To handle this we will just be connecting the needed pins from the Rpi directly to the relay board.
You should only need access to the 5v, 3.3v, and pins 26, 20, and 21 as listed on the wiki.

PROBLEM: as stated above pins 26, 20, and 21 are the pins used to control each of the three relays.
These pins are currently being used by the actuators as they need a grid of 6 pins where at least
five of them are GPIO pins. All you need to know is that if we wanted to use these exact pins, we 
would need to make new cables for the actuators, and we do not want to do that. 

SOLUTION: The solution to this problem is rather simple. instead of manually connecting to pins
26, 20, and 21, we just connect to any other three pins and use them to control the relays. 

Below is the code and we used pins 2, 3, and 4 for this. This is just a random selection becuase
they were next to eachother and were close to a 3.3v and 5v which I think are needed to power the relays. 

Make sure you connect the wires you want to connect into the center and right channels of the relays
 _______
|_1_2_3_| each relay has 3 inputs. Connect the contact closure wires to numbers 2 and 3. 

CONTROLING THE RELAYS: See the top of the wiki page (remember that the circle with an X in it 
represents an LED). Its basically explains that a low voltage (0v from the GPIO pins) will connect 
the center to the right and turn on the LED. A high voltage will connect the center to the left 
and turn off the LEDs.

*Note that the board we have has 3 relays you can access. 

"""



##################################################

#           P26 ----> Relay_Ch1
#			P20 ----> Relay_Ch2
#			P21 ----> Relay_Ch3

# note that these are the pins we need to connect to on the relay board from the RPI.
#       P2 --> P26
#       P3 --> P20
#       P4 --> P21

# this means that pins 2,3, and 4 control relays 1,2, and 3 respectively. 

##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

# the wires connecting the RPi to the relay board are attacked to the RPis GPIO pins 2, 3, and 4
# any 3 would do, I picked these at random. 
Relay_Ch1 = 2  #26   the old numbers were comented out. 
Relay_Ch2 = 3  #20   they come from the source code on the wiki (see above links)
Relay_Ch3 = 4  #21


class Relays:
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(Relay_Ch1,GPIO.OUT)
		GPIO.setup(Relay_Ch2,GPIO.OUT)
		GPIO.setup(Relay_Ch3,GPIO.OUT)


	def relay_off(self, number): # takes a number 1, 2, or 3 for the relay you want to change
		GPIO.setup((number+1),GPIO.HIGH) # remember that low voltage turns on the LED and connects 
										# the center and right channels
		# note that (number + 1) was a convenient way to code this becuase the channel numbers 
		# 1, 2, and 3 are connected to pins 2, 3, and 4. If they were connected to a more random
		# set of pin numbers, then you could just use some if statements like
		# if number == 1: then relay_channel = Relay_Ch1

	def relay_on(self, number): # takes a number 1, 2, or 3 for the relay you want to change
		GPIO.setup((number+1),GPIO.LOW) # remember that low voltage turns on the LED and connects 
										# the center and right channels
		# if you are confused about (number+1) see comments in relay_off

	def test_relays(self): # test function to see if the code works the way I think it should
		inputVal = "on" 
		while(inputVal != "quit"):
			if inputVal == "off": # should disconnect wires
				self.relay_off(1)
			elif inputVal == "on": # should connect wired
				self.relay_on(1) 
			else:
				print("non-valid option")

			inputVal = input()

	
#to test this file, uncomment the following line and run this file 
#Relays().test_relays()

