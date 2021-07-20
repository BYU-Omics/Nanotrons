"""
JOYSTICK CLASS 
    This implements the methods needed to read the inputs from an Xbox 360 controller. It also
    handles operational discrepancies of pygame 1.9.6 between Windows and Raspberry OS (any linux
    OS really )
"""

import pygame
import inspect

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

"""
RAW HATS READING 
    (0,1):"UP", (0,-1):"DOWN", 
    (-1,0):"LEFT", (1,0):"RIGHT", 
    (0,0):"NOTHING", (1,1):"UP-RIGHT", 
    (-1,-1):"DOWN-LEFT", (1,-1):"DOWN-RIGHT", 
    (-1,1):"UP-LEFT"
"""
# This maps the values of the raw hat reading to the corresponding indices in the self.hats list
RAW_HATS_DICT = { (0,1):[0], (0,-1):[1], (-1,0):[2], (1,0):[3],
                  (1,1):[0,3], (-1,-1):[1,2], (1,-1):[1,3], (-1,1):[0,2], 
                  (0,0):["hola"] }

# HATS BUTTONS MAPPING (corresponding indeces in the self.hats list)
HATS_DICT = {0:"UP", 1:"DOWN", 2:"LEFT", 3:"RIGHT"}

HATS_DICT_INDECES = {"UP":0, "DOWN":1, "LEFT":2, "RIGHT":3}

STOP_LISTEN_WINDOWS = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0] # Bumpers pressed under pygame in Windows
STOP_LISTEN_RASPBERRY = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0] # Bumpers pressed under pygame in Raspberry OS

LEFT_BUMPER_INDEX = 4
RIGHT_BUMPER_INDEX = 5

WINDOWS_OS = "w"
RASPBERRY_OS = "r"

TRIGGERS_AXIS = 2
ERRONEOUS_AXES = [0, 1, 3, 4] # These are the indeces of the two axes that correspond to each joystick in the Xbox controller
THRESHOLD = 0.4 # This is the minimum value a joystick axes has to be to be read, otherwise it's considered 0

class XboxJoystick:
    """
    INITIAL VALUES 
    """
    def __init__(self, operating_system):
        # Store the value of the OS string given in the argument
        self.os = operating_system # Either the string "w" for windows or "r" for raspberry pi

        # Initialize the pygame library
        pygame.init()

        # Initialize the joystick library
        pygame.joystick.init()
        # Detect and initialize the first joystick in the list
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.name = self.joystick.get_name()
        print(f"Joystick initialized: {self.name}")

        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 11 elements. Windows will only use 10 but Raspberry OS requires the 11 elements
        self.axes = [0, 0, 0, 0, 0, 0] # Each axis state
        
        self.hats = [0, 0, 0, 0] # Each hat (arrow) has a state
        self.keep_listening = False
        
        self.axes_direction = [1, 1, 1, 1, 1, 1] # This is a multiplier to the argument of the function that moves the motor associated to the axis. It can be inverted depending on the user preferences
        self.bumpers_direction = 1

    def reset_values(self):
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 11 elements. Windows will only use 10 bu tRaspberry OS requires the 11 elements
        self.hats = [0, 0, 0, 0] # Each hat state (Arrow buttons)
        self.axes = [0, 0, 0, 0, 0, 0] # Each axis state
        self.keep_listening = False

    """
    GETTERS
    """
    def get_buttons(self):
        return self.buttons

    def get_hats(self):
        return self.hats

    def get_axes(self):
        return self.axes

    # This returns the index in self.hats (self.hats is a list) that corresponds to a given string representing a hat ("UP", "LEFT", "DOWN", etc)
    def get_hats_dict_index(self, hat):
        return HATS_DICT_INDECES[hat]

    # This is a list of either 1's or -1's that are a multiplier to the respective axis reading (to invert or revert the reading of a given axis)
    def get_axis_direction(self, axis_index):
        return self.axes_direction[axis_index]

    # This converts the corresponding multiplier within self.axes_direction from a 1 into a -1 and viceversa
    def set_axis_direction(self, axis_index, direction):
        self.axes_direction[axis_index] = direction
    
    # dummy_argument is a placeholder,  when we call a method from motor series it could be called by a button which by itself doesn't always
        # provide an argument (like letter buttons) but sometimes it does (like bumpers) so to generalize the method call a dummy argument is added
    def invert_bumpers_direction(self, dummy_argument):
        self.bumpers_direction = self.bumpers_direction * (-1)
    
    # This returns the value of a given button provided the string that represents it
    def get_button_by_name(self, name):
        if self.os == WINDOWS_OS:
            return self.buttons[BUTTONS_DICT_REVERSED_W[name]]
        elif self.os == RASPBERRY_OS:
            return self.buttons[BUTTONS_DICT_REVERSED_R[name]]

    """
    READING SECTION
    """
    # Read the state of the axes in the joystick
    def read_axes(self):
        self.axes = [round(self.joystick.get_axis(i), 3) for i in range(self.joystick.get_numaxes())] # rounded to 1 decimal point bc the stick axes are never actually 0 (they have an error that starts on the second decimal point of the reading)
        
        # print("Pre processing of axes: ", self.to_string_axes())
        
        # The following lines of code implement a fix for uniform operation of the pygame library between windows and raspberry os
        if (self.os == RASPBERRY_OS):
            var1 = self.axes[3]
            self.axes[3] = self.axes[4]
            self.axes[4] = var1
            
            if self.joystick.get_axis(2) == 0:
                self.axes[2] = -1
            if self.joystick.get_axis(5) == 0:
                self.axes[5] = -1
            
            if self.axes[2] != -1:
                trigger_axis = self.axes[2]
                self.axes[TRIGGERS_AXIS] = (trigger_axis + 1)/2
            elif self.axes[5] != -1:
                trigger_axis = self.axes[5]
                self.axes[TRIGGERS_AXIS] = -1*(trigger_axis + 1)/2
            else:
                # both axes are not being pressed or both are being pressed
                self.axes[TRIGGERS_AXIS] = 0
        
        self.axes_error_filter() # Apply the filter to the analog error of the joysticks in the controller

        # Multiply each final value by the direction of the axes defined in self.axes_direction
        self.axes = [ self.axes[i] * self.axes_direction[i] for i in range(len(self.axes))]
        
        # print("Post processing of axes: ", self.to_string_axes())

    # Read the state of the buttons in the joystick
    def read_buttons(self):
        self.buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        if self.buttons[LEFT_BUMPER_INDEX] == 1:
            self.buttons[LEFT_BUMPER_INDEX] = 1 * self.bumpers_direction
        if self.buttons[RIGHT_BUMPER_INDEX] == 1:
            self.buttons[RIGHT_BUMPER_INDEX] = -1 * self.bumpers_direction

    # Read the state of the hats in the joystick
    def read_hats(self):
        raw_hats= self.joystick.get_hat(0) # This is a tuple in the format (x,y),  but we'll convert it to [a, b, c, d] with each letter being the arrow pressed
        indeces_list = RAW_HATS_DICT[raw_hats]
        for index in range(len(self.hats)):
            if index in indeces_list:
                if ( (HATS_DICT[index] == "DOWN") or (HATS_DICT[index] == "RIGHT") ):                    
                    self.hats[index] = 1
                else:
                    self.hats[index] = -1
            else:
                self.hats[index] = 0
                
    # Filtering of the axes of the joysticks, who carry an analog error by factory
    def axes_error_filter(self):
        for i in ERRONEOUS_AXES:
            if abs(self.axes[i]) < THRESHOLD:
                self.axes[i] = 0

    # This returns a list of strings that represent all the buttons that are currently being pressed
        # When this function gets called, it reads the list self.buttons and for every element that is 
        # set to 1, it will append the corresponding value ("A", "X", "Y", etc.) to the list that it
        # will return. This will then feed the input for a Profile object which will execute the 
        # associated function
    def deliver_buttons(self):
        pressed_buttons = []
        for button in range(len(self.buttons)):
            if self.buttons[button] != 0:
                if self.os == WINDOWS_OS:
                    # print("deliver_buttons")
                    pressed_buttons.append(BUTTONS_DICT_W[button])
                elif self.os == RASPBERRY_OS:
                    pressed_buttons.append(BUTTONS_DICT_R[button])
        return pressed_buttons

    # This returns a list of strings that represent all the hats that are currently being pressed
        # When this function gets called, it reads the list self.hats and for every element that is 
        # set to 1, it will append the corresponding value ("A", "X", "Y", etc.) to the list that it
        # will return. This will then feed the input for a Profile object which will execute the 
        # associated function
    def deliver_hats(self):
        pressed_hats = []
        for hat in range(len(self.hats)):
            if ( (self.hats[hat] == 1) or (self.hats[hat] == -1) ):
                # print("deliver_hats")
                pressed_hats.append(HATS_DICT[hat])
        
        return pressed_hats

    # This returns a dictionary that represent all the axes that are currently not in their natural position
    def deliver_axes(self):
        axes_to_deliver = {}
        for axis in range(5): # This ignores the 6th index which is just garbage from the pygame library
            if self.axes[axis] != 0:
                # print("deliver_axes")
                axes_to_deliver[axis] = self.axes[axis]
        return axes_to_deliver

    """
    LISTEN SECTION
    """
    # Listens to the controller's input
    def listen(self):
        # print("aqui en el thread")
        self.reset_values() # reset the values read from the last call for listen_one()
        # print(f"Started listening to {self.name}!")
        self.keep_listening = True
        while (self.keep_listening):
            # print("while")
            # EVENT DETECTION AND PRINT
            # print(pygame.event.get())
            # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.JOYBUTTONDOWN:
                    self.read_buttons()
                    # print(self.get_buttons())
                    # print(self.deliver_buttons())

                elif event.type == pygame.JOYBUTTONUP:
                    self.read_buttons()
                    # print(self.deliver_buttons())

                elif event.type == pygame.JOYAXISMOTION:
                    self.read_axes()
                    # print(self.deliver_axes())
                    # print(self.get_axes())

                elif event.type == pygame.JOYHATMOTION:
                    self.read_hats()
                    # print(self.deliver_hats())
                    # print(self.to_string_hats())

    # Sets to False the boolean that controls the listen() loop
    def stop_listening(self, dummy_arg):
        self.keep_listening = False

    """
    TO STRING SECTION 
    """
    def to_string_buttons(self):
        return f"Buttons: {self.buttons}"

    def to_string_hats(self):
        return f"Hats: {self.hats}"

    def to_string_axes(self):
        return f"Axes: {self.axes}"

    def to_string_trigger(self):
        return f"Trigger: {self.axes[2]}"


def testing():
    os = WINDOWS_OS
    print(F"TESTING JOYSTICK -> OS: {os}")
    controller = XboxJoystick(os)
    controller.listen()
    

if __name__ == "__main__":
    testing()