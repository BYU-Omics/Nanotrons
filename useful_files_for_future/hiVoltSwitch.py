"""
Jacob Davis. Created: Oct 16 2020

jacobmdavis4@gmail.com

hiVoltSwitch.py

OVERVIEW: This file controls the High Voltage Switch with raspberry pi GPIO
pins 6 and 12. When 3.3V is sent to pin6 the left cannel is opened. If 3.3V
is sent to pin12 the right channel is opened. To make this work, when one
is set to 3.3V the other is turned off (0V).


CONTROLS:
When starting the program, the left channel is opened.

Left Arrow: Open Left Channel
Right Arrow: Open Right Channel
Space: Toggle Channels
Escape: quit


PSEUDO CODE:

1.) initialize and open left channel to start

2.) wait key strokes
    -if left arrow: go to left position
        -pin6.on()   (3.3V)
        -pin12.off() (0v)
    -if right arrow: go to right position
        -pin12.on()  (3.3V)
        -pin6.off()  (0V)
    -if spacebar: toggle
        -if  left, go to right
        -if right, go to left
    -if escape: exit
        -sys.exit()



"""



#---------------------------------imports-----------------------------------
#import pygame, sys
#from random import random
#from pygame.locals import *
from gpiozero import LED, Button

#--------------------------------variables----------------------------------
channels = ["Left", "Right"]
channelIndex = 0 #0 is left, 1 is right

#------------------------------set up GPIO Pins----------------------------
#use led for GPIO output
#you can write to LED, so you can control the Actuator
pin6 = LED(6)  #goes to left side
pin12 = LED(12) #goes to right side

#deine resolution
#resolution = (600,400) #this is length and width of window

#init the screen
#pygame.init()
#resolution = (1,1) #for some reason pygame needs a screen to get keystrokes
#screen = pygame.display.set_mode(resolution)   
#clock = pygame.time.Clock() #controls frame rate

#------------------------------END VARIABLES--------------


class HiVoltageSwitch:
    def __init__(self, startPosition):
        self.channels = ["Left", "Right"]
        self.channelIndex = 0 #0 is left, 1 is right
        self.calibrate(startPosition) # initialize this to the right side based off the actuators

    #-------------------------------Move to position A-------------------------
    def openLeftChannel(self):
        pin6.on()
        pin12.off()
        self.channelIndex = 0
        
        return self.channelIndex           

    #---------------------------------Move to position B----------------------- 
    def openRightChannel(self):
        pin12.on()
        pin6.off()
        self.channelIndex = 1
        
        return self.channelIndex
    
    #---------------------------------Toggle------------------
    #switches channel
    def toggle(self):
        if self.channelIndex == 0:
            self.channelIndex = self.openRightChannel()
        elif self.channelIndex == 1:
            self.channelIndex = self.openLeftChannel()
            
        return self.channelIndex
            
    #------------------------------------calibrate-----------------------------
    def calibrate(self, startPosition): 
        """This sets the channel to the desired position when you call the run function.
           it generally is based off the actuator. See the coordinator class inits.

        Args:
            channelIndex ([int]): [0 or 1 for channel left or right]
        """
        if startPosition == 1:
            self.openLeftChannel()
        elif startPosition == 0:
            self.openRightChannel()
        else:
            print("/n****ERROR: switch not calibrated to either position left or right")
            
        print("/n/n SWTICH POSITION INDEX:")
        print(self.channelIndex)


    #-----------------------------------print instructions-----------------------
    '''def printInstructions(self):   
        print("Instructions")
        print("Left Arrow: Open Left Channel")
        print("Right Arrow: Open Right Channel")
        print("Spacebar: Toggle Channel")
        print("Escape: quit")'''

    #----------------------------------------RUN---------------------------------
    def run(self, channelIndex):
    
        self.calibrate(channelIndex)
        #self.printInstructions()
        print()
        
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and channelIndex == 0:
                        channelIndex = self.openRightChannel(channelIndex)
                    if event.key == pygame.K_LEFT  and channelIndex == 1:
                        channelIndex = self.openLeftChannel(channelIndex)
                    if event.key == pygame.K_SPACE: #toggle
                        channelIndex = self.toggle(channelIndex)
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                print(channels[channelIndex]) #print position to terminal

    def test_switch(self): # test function to see if the code works the way I think it should
        #self.calibrate(1)

        inputVal = "on" 

        while(inputVal != "quit"):
            if inputVal == "off": # should disconnect wires
                pass
            elif inputVal == "on": # should connect wired
                self.toggle() 
            else:
                print("non-valid option")

            inputVal = input()
            
# commment this in to test this file alone
#mySwitch = HiVoltageSwitch(0)
#mySwitch.test_switch()


