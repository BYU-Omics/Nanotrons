"""
PROFILES CLASS 

    This class specifies the mapping between inputs from the Joystick and methods from the main driving classes of the system, such as
    MotorSeries, Scripter, or Joystick. Every time there is a key/hat/axis event on the Joystick, Coordinator checks for the method 
    associated to that input element inside the mapping contained in this class and executes it. 
    A Profile object is constructed receiving the name of an input json file containing the mapping, but it can also take another file 
    as input anytime to change the mapping. In addition, it can export the current mapping to a json file so that it can be used later. 
    The purpose of these importing/exporting functionalities is to allow for the system to support different mappings
"""

from drivers.OTdriver import *
from joystick import *
import inspect
import json
import sys

CURRENT_DIRECTORY = sys.path[0] + '\\controller_profiles\\'

class Profile:
    def __init__(self, file):

        nothing_f = self.nothing # This is just a "pass" function (placeholder for the mapping dictionariy/list below)
        
        # This maps specific button names to methods in the MotorSeries class
        self.buttons_mapping = {"A":nothing_f, "B":nothing_f, "X":nothing_f, "Y":nothing_f, "LB":nothing_f, 
                        "RB":nothing_f, "BACK":nothing_f, "START":nothing_f, "LSTICK":nothing_f, 
                        "RSTICK":nothing_f, "XBOX":nothing_f, "NOTHING":nothing_f} # The dictionary that maps buttons to functions
        
        # This maps specific hat names to methods in the MotorSeries class
        self.hats_mapping = { "UP":nothing_f, "DOWN":nothing_f, "LEFT":nothing_f, "RIGHT":nothing_f, "NOTHING":nothing_f}

        # This maps functions to the corresponding axes with the index of the list as the parameter or iteration                
        self.axes_mapping = [nothing_f, nothing_f, nothing_f, nothing_f, nothing_f, nothing_f] # Index 2 is the axis for the triggers

        self.load_profile(file)

    # This returns the name assigned to the current profile
    def get_profile_name(self):
        return self.profile_name

    # This returns the function object associated to the given button
    def get_button_function(self, button):
        return self.buttons_mapping[button]

    # This returns the function object associated to the given hat
    def get_hat_function(self, hat):
        return self.hats_mapping[hat]

    # This returns the function object associated to the given axis
    def get_axis_function(self, axis_index):
        return self.axes_mapping[axis_index]

    # This returns the mapping of all the buttons (string - function)
    def get_buttons_mapping(self):
        return self.buttons_mapping

    # This returns the mapping of all the axes (string - function)
    def get_axes_mapping(self):
        return self.axes_mapping

    # This returns the mapping of all the hats (string - function)
    def get_hats_mapping(self):
        return self.hats_mapping

    # This returns the function associated to the provided string name. It searches on all the classes specified inside of the method
    def find_method(self, function_name):
        # print("Function name: {}".format(function_name))
        method = getattr(OT2_nanotrons_driver, function_name, "NOT_FOUND")
        # if method == "NOT_FOUND":
        #     method = getattr(Scripter, function_name, "NOT_FOUND")
        if method == "NOT_FOUND":
            method = getattr(XboxJoystick, function_name, "NOT_FOUND")
        # print("Method: {}".format(method))
        return method

    # This returns the amount of arguments needed by a method (this is not yet in use but might come in handy to not have the need for dummy arguments in function definitions that don't take arguments)
    def function_requires_args(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters.values()
        return len(parameters)

    # This sets the name for the current profile
    def set_profile_name(self, name):
        self.profile_name = name

    # This sets the mapping of a button to a given function
    def set_button_function(self, button, function_name):
        method = self.find_method(function_name)
        self.buttons_mapping[button] = method

    # This sets the mapping of a hat to a given function
    def set_hat_function(self, hat, function_name):
        method = self.find_method(function_name)
        self.hats_mapping[hat] = method

    # This sets the mapping of an axis to a given function
    def set_axis_function(self, axis_index, function_name):
        method = self.find_method(function_name)
        self.axes_mapping[axis_index] = method

    # This loads the provided file onto the Profile object. It DOES NOT check for erroneous input. The file is supposed to be formatted correctly
    def load_profile(self, file_name = 'default_profile.py'):
        # print(CURRENT_DIRECTORY)
        path_to_file = CURRENT_DIRECTORY + file_name
        # print(path_to_file)
        json_path = open(path_to_file, "r")
        myFile = json.load(json_path)
        for line in myFile.items():
            key, value = line
            if key in self.buttons_mapping.keys():
                self.buttons_mapping[key] = self.find_method(value)
            elif key in self.hats_mapping.keys():
                self.hats_mapping[key] = self.find_method(value)
            else:
                self.axes_mapping[int(key)] = self.find_method(value)

    # This exports the current profile mappings onto a file. Its name is specified in the constructor of the instance of the Profile object
    def export_profile(self):
        file_name = f"{self.profile_name}.json"
        myFile = open(file_name, "w")
        data = dict()

        for button, function in self.buttons_mapping.items():
            data[button] = function.__name__

        for hat, function in self.hats_mapping.items():
            data[hat] = function.__name__
        
        for axis_index in range(len(self.axes_mapping)):
            data[f"{axis_index}"] = self.axes_mapping[axis_index].__name__
        
        json.dump(data, myFile)
        print(f"Profile was succesfully exported to {file_name}")

    # This is a sort of getter function of the class that returns the names of all the methods in the Profile class
    def get_methods(self):
        return [inspect.getmembers(Profile, predicate=inspect.isfunction)[i][0] for i in range(len(inspect.getmembers(Profile, predicate=inspect.isfunction)))]

    def nothing(self):
        # This is the function executed by all the buttons that don't have an associated action (placeholder so that if the 
        # button is pressed, the program doesn't throw an exception saying that the button is not registered in the mapping
        # dictionary)
        pass

    def to_string_buttons_mapping(self):
        mapping = "BUTTONS MAPPING\n"
        #print("key: {}, value: {}".format(self.buttons_mapping.keys(), self.buttons_mapping.values()))
        for key, value in self.buttons_mapping.items():
            #print("key: {}, value: {}".format(key, value))
            mapping = mapping + f"[{key}] - {value.__name__}\n"
        return mapping

    def to_string_hats_mapping(self):
        mapping = "HATS MAPPING\n"
        for key, value in self.hats_mapping.items():
            mapping = mapping + f"[{key}] - {value.__name__}\n"
        return mapping

    def to_string_axes_mapping(self):
        mapping = "AXES MAPPING\n"
        #print("to_string_axes_mapping")
        for i in range(len(self.axes_mapping)):
            # print(f"self.axes_mapping[i]: {self.axes_mapping[i]}")
            mapping = mapping + f"[{i}] - {self.axes_mapping[i].__name__}\n"
        return mapping


def testing():
    seba = Profile("default_profile.json")
    seba.set_profile_name("seba_profile")
    print(seba.to_string_buttons_mapping())
    print(seba.to_string_hats_mapping())
    print(seba.to_string_axes_mapping())
    seba.export_profile()

if __name__ == "__main__":
    testing()