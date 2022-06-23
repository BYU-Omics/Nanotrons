"""
JOYSTICK CLASS 
    This implements the methods needed to read the inputs from an Xbox 360 controller. It also
    handles operational discrepancies of pygame 1.9.6 between Windows and Raspberry OS (any linux
    OS really )
"""

import pygame
import time

# JOYSTICK BUTTONS MAPPING
BUTTONS_DICT_W = { 0:"A", 1:"B", 2:"X", 3:"Y", 4:"LB", 
                 5:"RB", 6:"BACK", 7:"START", 8:"LSTICK", 
                 9:"RSTICK" }

BUTTONS_DICT_R = { 0:"A", 1:"B", 2:"X", 3:"Y", 4:"LB", 
                 5:"RB", 6:"BACK", 7:"START", 8:"XBOX", 9:"LSTICK", 
                 10:"RSTICK" }

BUTTONS_DICT_REVERSED_W = { "A":0, "B":1, "X":2, "Y":3, "LB":4, 
                 "RB":5, "BACK":6, "START":7, "LSTICK":8, 
                 "RSTICK":9 }

BUTTONS_DICT_REVERSED_R = { "A":0, "B":1, "X":2, "Y":3, "LB":4, 
                 "RB":5, "BACK":6, "START":7, "XBOX":8, "LSTICK":9, 
                 "RSTICK":10 }

HATS_USED_DICT = { (0,1):"HAT_UP", (0,-1):"HAT_DOWN", (-1,0):"HAT_Left", (1,0):"HAT_RIGHT"}
HATS_USED_LIST = [(0,1), (0,-1), (-1,0), (1,0)] 

AXES_DICT = {(0,-1):"L_STICK_LEFT",(0,1):"L_STICK_RIGHT",(1,1):"L_STICK_DOWN",(1,-1):"L_STICK_UP",
             (2,-1):"R_STICK_LEFT",(2,1):"R_STICK_RIGHT",(3,1):"R_STICK_DOWN",(3,-1):"R_STICK_UP",
             (4,-1):"L_TRIGGER",(4,1):"L_TRIGGER",(5,-1):"R_TRIGGER",(5,1):"R_TRIGGER"}

WINDOWS_OS = "w"
RASPBERRY_OS = "r"
THRESHOLD = 0.8 # This is the minimum value a joystick axes has to be to be read, otherwise it's considered 0

AXES = [0, 0, 0, 0, -1, -1]
HATS = [(0,0)]
BUTTONS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

SENSITIVE_AXES = [0, 1, 2, 3]

class XboxJoystick:
    """
    INITIAL VALUES 
    """
    def __init__(self, operating_system):
        # Store the value of the OS string given in the argument
        self.os = operating_system # Either the string "w" for windows or "r" for raspberry pi

        self.pygame_running = False
        self.controller_1 = None
        self.stop_joystick = False

        self.axes = []
        self.hats = []
        self.buttons = []

        self.pressed_button = []
        self.pressed_hat = []
        self.pressed_axis = []

    # this function is used to reset the values of pressed inputs lists before adding new ones
    def reset_values(self):
        self.pressed_button = []
        self.pressed_hat = []
        self.pressed_axis = [] 

    # initializes pygame, pygame.joystick, and an instance of the controller (xbox style controller) 
    def start_pygame(self):

        if self.pygame_running == False:
            print("Controller Initialized")
            pygame.init()
            pygame.joystick.init()
            self.controller_1 = pygame.joystick.Joystick(0)
            self.pygame_running = True

    # deinitializes pygame, pygame.joystick, and an instance of the controller (xbox style controller)
    def end_pygame(self):
        
        if self.pygame_running == True:
            pygame.quit()
            pygame.joystick.quit()
            self.pygame_running = False
    
    # this function prevents light/unintended axis events from calling axis commands
    def false_axes_event_filter(self):
        for i in SENSITIVE_AXES:
            if abs(self.axes[i]) < THRESHOLD:
                self.axes[i] = 0

    # this function is used to retrieve the pressed inputs lists
    def deliver_joy(self):
        return self.pressed_button, self.pressed_hat, self.pressed_axis

    """
    LISTEN SECTION
    """
    # Listens to the controller's input
    def listen(self):

        listening = True

        while listening:
   
            for event in pygame.event.get(): # User did something.
                
                self.reset_values()  

                if self.stop_joystick == True:
                    print("Stopping Joystick")
                    self.end_pygame()
                    listening = False
                    return listening

                # Button down events, just like it sounds (when you press a button)
                elif event.type == pygame.JOYBUTTONDOWN:
                    previous_buttons = self.buttons
                    self.buttons = [self.controller_1.get_button(i) for i in range(self.controller_1.get_numbuttons())]
                    if (self.buttons != BUTTONS and previous_buttons == BUTTONS):
                        # print(f"buttons: {self.myControler.get_numbuttons()}, {self.buttons}")
                        # print("")
                        # count += 1
                        # print(f" event count: {count}")

                        

                        for button in range(len(self.buttons)):
                            if self.buttons[button] != 0:
                                self.pressed_button.append(BUTTONS_DICT_W[button])
                                # print(f"Pressed button is in pygame_practice: {self.pressed_button}\n")

                        time.sleep(0.5)

                
                # Releasing buttons are treated as separate events from pressing them down, updates position values
                elif event.type == pygame.JOYBUTTONUP:
                    self.buttons = [self.controller_1.get_button(i) for i in range(self.controller_1.get_numbuttons())]
                    # print(f"buttons on release: {self.controller_1.get_numbuttons()}, {self.buttons}")
                    


                # Hat motion events (aka D-pad)
                elif event.type == pygame.JOYHATMOTION:
                    previous_hats = self.hats
                    self.hats = [self.controller_1.get_hat(i) for i in range(self.controller_1.get_numhats())]
                    if (self.hats != HATS) and (previous_hats == HATS):
                        # print(f"hats: {self.controller_1.get_numhats()}, {self.hats}")
                        # print("")
                        # count += 1
                        # print(f" event count: {count}")

                        for hat in range(len(self.hats)):
                            if self.hats[hat] in HATS_USED_LIST: # only using left, right, up, and down, ignores diagonals
                                self.pressed_hat.append(HATS_USED_DICT[self.hats[hat]])
                        # print(f"Pressed hat is in pygame_practice: {self.pressed_hat}\n")
                        time.sleep(0.5)




                # Axis motion events (aka triggers and thumbsticks)
                elif event.type == pygame.JOYAXISMOTION:
                    previous_axes = self.axes
                    self.axes = [self.controller_1.get_axis(i) for i in range(self.controller_1.get_numaxes())]
                    self.false_axes_event_filter()
                    if (self.axes != AXES) and (previous_axes == AXES):
                        # print(f"axes: {self.controller_1.get_numaxes()}, {self.axes}")
                        # print("")
                        # count += 1
                        # print(f" event count: {count}")

                        for axis in range(len(self.axes)):
                            if self.axes[axis] != AXES[axis]:
                                if self.axes[axis] > 0:
                                    axis_key = (axis,1)
                                elif self.axes[axis] < 0:
                                    axis_key = (axis,-1)
                        self.pressed_axis.append(AXES_DICT[axis_key])
                        # print(f"Pressed axis is in pygame_practice: {self.pressed_axis}\n")
                        time.sleep(0.5)
                        
                else: 
                    pass