"""
JOYSTICK CLASS 
    This implements the methods needed to read the inputs from an Xbox 360 controller. It also
    handles operational discrepancies of pygame 1.9.6 between Windows and Raspberry OS (any linux
    OS really )
"""

import pygame

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

AXES_DICT = {(0,-1):"L_STICK_LEFT",(0,1):"L_STICK_RIGHT",(1,1):"L_STICK_DOWN",(1,-1):"L_STICK_UP",
             (2,-1):"R_STICK_LEFT",(2,1):"R_STICK_RIGHT",(3,1):"R_STICK_DOWN",(3,-1):"R_STICK_UP",
             (4,-1):"L_TRIGGER",(4,1):"L_TRIGGER",(5,-1):"R_TRIGGER",(5,1):"R_TRIGGER"}

HATS_USED_DICT = { (0,1):"HAT_UP", (0,-1):"HAT_DOWN", (-1,0):"HAT_Left", (1,0):"HAT_RIGHT"}

STOP_LISTEN_WINDOWS = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0] # Bumpers pressed under pygame in Windows
STOP_LISTEN_RASPBERRY = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0] # Bumpers pressed under pygame in Raspberry OS

LEFT_BUMPER_INDEX = 4
RIGHT_BUMPER_INDEX = 5

WINDOWS_OS = "w"
RASPBERRY_OS = "r"

TRIGGERS_AXIS = 2
SENSITIVE_AXES = [0, 1, 3, 4] # These are the indeces of the two axes that correspond to each joystick in the Xbox controller
THRESHOLD = 0.4 # This is the minimum value a joystick axes has to be to be read, otherwise it's considered 0

AXES = [0, 0, 0, 0, -1, -1]
HATS = [(0,0)]
BUTTONS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class XboxJoystick:
    """
    INITIAL VALUES 
    """
    def __init__(self, operating_system):
        # Store the value of the OS string given in the argument
        self.os = operating_system # Either the string "w" for windows or "r" for raspberry pi

       # Initialize the pygame library
        pygame.init()
        pygame.joystick.init()

        # Detect and initialize the first joystick in the list
        self.joystick = pygame.joystick.Joystick(0)
        # self.joystick.init()
        # self.name = self.joystick.get_name()
        # print(f"Joystick initialized: {self.name}")

        self.axes = []
        self.hats = []
        self.buttons = []
               
        self.pressed_button = []
        self.pressed_hat = []
        self.pressed_axis = []

        self.keep_listening = False
        
        # self.axes_direction = [1, 1, 1, 1, 1, 1] # This is a multiplier to the argument of the function that moves the motor associated to the axis. It can be inverted depending on the user preferences
        # self.bumpers_direction = 1

    def reset_values(self):
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 11 elements. Windows will only use 10 bu tRaspberry OS requires the 11 elements
        self.hats = [0, 0, 0, 0] # Each hat state (Arrow buttons)
        self.axes = [0, 0, 0, 0, 0, 0] # Each axis state
        self.keep_listening = False

    def false_axes_event_filter(self):
        for i in SENSITIVE_AXES:
            if abs(self.axes[i]) < THRESHOLD:
                self.axes[i] = 0


    def get_hats(self):
        return self.hats



    # This returns the index in self.hats (self.hats is a list) that corresponds to a given string representing a hat ("UP", "LEFT", "DOWN", etc)
    def get_hats_dict_index(self, hat):
        return HATS_DICT_INDECES[hat]
    
    # This returns the value of a given button provided the string that represents it
    def get_button_by_name(self, name):
        if self.os == WINDOWS_OS:
            return self.buttons[BUTTONS_DICT_REVERSED_W[name]]
        elif self.os == RASPBERRY_OS:
            return self.buttons[BUTTONS_DICT_REVERSED_R[name]]

    def listen(self):

        self.reset_values() # reset the values read from the last call for listen_one()
        self.keep_listening = True
        while (self.keep_listening):

            for event in pygame.event.get(): # User did something.
                
                # Button down events, just like it sounds (when you press a button)
                if event.type == pygame.JOYBUTTONDOWN:
                    previous_buttons = self.buttons
                    self.buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
                    if (self.buttons != BUTTONS and previous_buttons == BUTTONS):
                        # print(f"buttons: {self.joystick.get_numbuttons()}, {self.buttons}")
                        # print("")
                        # count += 1
                        # print(f" event count: {count}")

                        for button in range(len(self.buttons)):
                            if self.buttons[button] != 0:
                                self.pressed_button.append(BUTTONS_DICT_W[button])
                                print(f"Pressed button is: {self.pressed_button} \n") 
                
                # Releasing buttons are treated as separate events from pressing them down, updates position values
                elif event.type == pygame.JOYBUTTONUP:
                    self.buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
                    print(f"buttons on release: {self.joystick.get_numbuttons()}, {self.buttons}")
                    


                # Hat motion events (aka D-pad)
                elif event.type == pygame.JOYHATMOTION:
                    previous_hats = self.hats
                    self.hats = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]
                    if (self.hats != HATS) and (previous_hats == HATS):
                        # print(f"hats: {self.joystick.get_numhats()}, {self.hats}")
                        # print("")
                        # count += 1
                        # print(f" event count: {count}")

                        for hat in range(len(self.hats)):
                            if self.hats[hat] in HATS_USED_DICT: # only using left, right, up, and down, ignores diagonals
                                self.pressed_hat.append(HATS_USED_DICT[self.hats[hat]])
                        print(f"Pressed hat is: {self.pressed_hat} \n")

                # Axis motion events (aka triggers and thumbsticks)
                elif event.type == pygame.JOYAXISMOTION:
                    previous_axes = self.axes
                    self.axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
                    self.false_axes_event_filter()
                    if (self.axes != AXES) and (previous_axes == AXES):
                        # print(f"axes: {self.joystick.get_numaxes()}, {self.axes}")
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
                        print(f"Pressed axis is: {self.pressed_axis} \n")

                
    # This returns a list of strings that represent all the buttons that are currently being pressed
        # When this function gets called, it reads the list self.buttons and for every element that is 
        # set to 1, it will append the corresponding value ("A", "X", "Y", etc.) to the list that it
        # will return. This will then feed the input for a Profile object which will execute the 
        # associated function
    
    def deliver_joy(self):
        return self.pressed_button, self.pressed_axis, self.pressed_hat

    # Sets to False the boolean that controls the listen() loop
    def stop_listening(self):
        self.keep_listening = False
        pygame.quit()