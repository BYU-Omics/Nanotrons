"""
Jacob Davis. Nov 5 2020
actuator.py
OVERVIEW: This file activates and deactivates specific GPIO pins on the RPi
which are connected to the control pins on the VICI actuator model EUD-A. Other
models should work with this code. This class is controlled by a controller class
which calls the toggle function. 
CONTROL PINS: there are 6 pins as shown below
|-----------|  
|  1  2  3  |
|  4  5  6  |
|-----------|
Position A is controlled by pin 4
Pin 1 goes high (3.3V) when the actuator reaches position A
Position B is controlled by pin 6
Pin 3 goes high (3.3V) when the actuator reaches position B
Pin 2 is used to make the controls. When pins 2 and 4 are shorted together
the actuator moves to position A. It moves to position B when pins 2 and 6
are shorted together. They are shorted by the RPi by connecting pin 2 to a
GPIO pin and then setting its voltage to 0V (pins 4 and 6 are set to 3.3V.
Then when the RPi turns one of them off (0V), it is like they are shorted
together. The signal can be turned back to 3.3V and the actuator will
remain in its position until the next control.
Pin 5 is unused
CONNECTING TO THE RPi: you will probably need a schematic of RPi4 pin nums.
Pin 1 ---> GPIO 20
Pin 2 ---> GPIO 26
Pin 3 ---> GPIO 19
Pin 4 ---> GPIO 16
Pin 5 ---> Unused/Ground
Pin 6 ---> GPIO 21
*Note that these are the 6 pins (including ground) closed to ethernet port
*There should be a cable that I made for this to work, but if not, you can
make another with this
CONTROL INTERFACE:
When starting the program, the actuator remain in its current position
calling actuator.toggle() will switch the valve from its current position and return new position index.
calling actuator.getPosition() return current position
"""

#---------------------------------imports-----------------------------------
import time
import sys
from gpiozero import LED, Button

#--------------------------------constants---------------------------------
SIGNAL_HOLD = 0.2 #control signals must last at least 20ms
                 #anything less than 70 and you start to pick up errors with mechanical change
                 #becuase it will think it is in position A and B at the same time. This delay gives it time to change.

#--------------------------------variables----------------------------------
#positionIndex = 0 #0 is A, 1 is B

#------------------------------set up GPIO Pins-----ACTUATOR 1-----------------------
#use led for GPIO output
#you can write to LED, so you can control the Actuator
pin16 = LED(16)
pin21 = LED(21)
pin26 = LED(26)

#use buttons for GPIO inputs
#you can read from buttons. 3.3V is on, 0V is off.
pin19 = Button(19) #check position B
pin20 = Button(20) #check position A
pin26.off() #this one needs to be grounded always

#------------------------------set up GPIO Pins------ACTUATOR 2----------------------
#use led for GPIO output
#you can write to LED, so you can control the Actuator
pin11 = LED(11)
pin10 = LED(10)
pin25 = LED(25)

#use buttons for GPIO inputs
#you can read from buttons. 3.3V is on, 0V is off.
pin8 = Button(8) #check position B
pin9 = Button(9) #check position A

pin25.off() #this one needs to be grounded always

#-------------------------------------END VARIABLES-------------------------------

#this class controls the actuator. When powered on it remains in its position until toggle is called
#toggle is the only function that should be called. Getposition can also be called.
class Actuator:
    def __init__(self):
        pass
    #-------------------------------------get Position-------------------------
    def getPosition(self):
        positionIndex = -1
        
        if pin20.is_pressed and pin19.is_pressed: #error
            print("Error: Actuator - both positions register as true. Maybe: Do not toggle quickly.")
            #sys.exit()
        elif not pin20.is_pressed and not pin19.is_pressed: #error
            print("Error: Actuator is not in position A or B or Powered off. Check power connection.")
            sys.exit()
        elif pin20.is_pressed and not pin19.is_pressed: #good position A
            positionIndex = 0 #a
        elif not pin20.is_pressed and pin19.is_pressed: #good position B
            positionIndex = 1 #b
        
        return positionIndex
    #-------------------------------Move to position A-------------------------
    def movePosA(self):
        #print("move A")
        pin16.off() #16 is connected to the first actuator
        pin11.off() #11 is connected to the second
        time.sleep(SIGNAL_HOLD)
        pin16.on()
        pin11.on()
        time.sleep(SIGNAL_HOLD) #hold for a bit to avoid error from mechanical change (if you dont wait, it will
                                #register as both position A and B simutaneously and throw error)

    #---------------------------------Move to position B----------------------- 
    def movePosB(self):
        #print("move B")
        pin21.off() #21 is connected to the first actuator
        pin10.off() #10 is connected to the second
        time.sleep(SIGNAL_HOLD)
        pin21.on()
        pin10.on()
        time.sleep(SIGNAL_HOLD) #hold for a bit to avoid error from mechanical change (if you dont wait, it will
                                #register as both position A and B simutaneously and throw error)
    #---------------------------------Toggle-----------------------------------
    #this will switch positions no matter what the current position is
    #if its in A, go to B. If its in B, go to A. 
    def toggle(self):
        positionIndex = self.getPosition()
        
        if positionIndex == 0: #it is in position A
            self.movePosB()        #move to B
            self.movePosB()        #move to B
            #I added in this call twice because it only toggle every other time
            #I am not sure why, but calling it twice fixes the problem. May be a timing issue
        elif positionIndex == 1: #it is in position B
            self.movePosA()        #move to A
            self.movePosA()        #move to A
        else:
            print("Error: Actuator cannot toggle. No registered position.")
            #sys.exit()

        time.sleep(SIGNAL_HOLD)  #hold for a bit to avoid error from mechanical change (if you dont wait, it will
                                 #register as both position A and B simutaneously and throw error)
        
        return self.getPosition() #return new position
    
    #----------------------------Test-----------------------
    def test(self):
        print(self.toggle())
        time.sleep(1.5)
        
        print(self.toggle())
        time.sleep(1.5)
        
        print(self.toggle())

#to test this file, uncomment the following line and run this file 
#Actuator().toggle()