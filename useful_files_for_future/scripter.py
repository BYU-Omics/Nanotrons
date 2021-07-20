"""
SCRIPTER CLASS 
    This class implements an object that is able to:
    1. Receive an order to start recording
    2. Records the absolute/relative displacements on a list
    3. Receive a command to import those recordings to a file
    4. Receive an order to stop recording and clear the list of records

    A dummy_arg is included in all the functions that don't accept parameters so that there is a 
    placeholder to the value of the button when the method gets called
"""

from moves import Move
from scripter_helper import *
import json

class Scripter:
    def __init__(self, motor_series, script_type, script_name):
        self.mySeries = motor_series
        self.recording = False
        self.script_name = script_name
        self.script_type = script_type # It can be either "r" for relative or "a" for absolute
        self.script = []
        self.checkpoints = []

    # This adjustst the way the script is recorded. It can only be changed before starting to record
    def change_script_type(self, script_type):
        if (self.recording == False):
            self.script_type = script_type
        else:
            print("Script type cannot be changed. Recording has already started.")

    # This changes the name of the file the script it written onto
    def change_script_name(self, script_name):
        self.script_name = script_name

    # This returns the type of script being recorded (absolute or relative)
    def get_script_type(self, dummy_arg):
        return self.script_type
    
    # This sets the boolean of recording to True (meaning we have started recording)
    def start_recording(self, dummy_arg):
        self.recording = True

    # This sets the recording boolean to False and resets the variables to start a new recording later
    def stop_recording(self, dummy_arg):
        self.recording = False
        self.script = []
        self.checkpoints = [] # This will be a list of lists. The latter is a snapshot of the positions of all the motors

    # This records a displacement (either absolute or relative)
    def record_displacements(self, dummy_arg, speed_list = []):

        if len(self.script) == 0:
            self.start_recording(dummy_arg)

        if (speed_list == []):
            speed_list = [self.mySeries.get_motor_max_speed(i) for i in range(len(self.mySeries.get_motor_list()))]
        
        self.checkpoints.append(checkpoint(self.mySeries))

        if len(self.checkpoints) == 1:
            print("First checkpoint recorded!")

            if (self.script_type == "a"):
                # record the checkpoint as the first move
                line = format_abs_line(self.checkpoints[0], self.checkpoints[0], self.checkpoints[0], speed_list, True)
                # append the string line to the list of moves
                self.script.append(line)

        elif len(self.checkpoints) == 2:
            line = ""
            # run the diff for each motor
            diff = checkpoint_diff(self.checkpoints[0], self.checkpoints[1]) # List of the difference of each element between checkpoints
            if (self.script_type == "a"):
                line = format_abs_line(self.checkpoints[0], self.checkpoints[1], diff, speed_list)
            elif (self.script_type == "r"):
                line = format_rel_line(diff, speed_list)
            # append the string line to the list of moves
            self.script.append(line)
            # replace the oldest checkpoint with the newest one
            self.checkpoints[0] = self.checkpoints[1]
            # pop the last element of the list (duplicated now), to leave room for a new checkpoint
            self.checkpoints.pop(1)
            print("Displacement(s) recorded!")

    # This deletes the last recorded displacement in the list
    def delete_last_displacement(self, dummy_arg):
        if len(self.script) > 0:
            self.script.pop(-1)
            print("Previously recorded move succesfully deleted.")
        else:
            print("No moves recorded, can't delete any moves.")

    # This saves the list of moves to a file and stops recording
    def save_script(self, dummy_arg):
        if len(self.script) == 0:
            print("No moves stored so far. Cannot save to file")
            return
        
        data = [self.script_type] + self.script
        path = open(self.script_name, "w")
        json.dump(data, path)

        self.stop_recording(dummy_arg)
        print(f"Moves succesfully written to {self.script_name}")

    """
    HIGH LEVEL SCRIPTING
        This section involves the creation of a "high level script" that only specifies names of components and
        arbitraty values to them. It also translates such script into an understandable format of of script such
        as the one created when recording positions from a joystick

        Considerations:
            - Every time we add a command, it is preceded by a lift in the Z axis so that there's no equipment 
            damage
            - Each command has the following elements:
                i. action: move/suck up/spit out/wait
                ii. attribute: target well/pot (move)/ ml (suck up)/ ml (spit out)/ seconds (wait)
                iii. speed: default max (move)/ default syringe (suck up/spit out) / NA (wait)
                iv. duration: "NA" (move/suck up/spit out) / seconds (wait)

    """

    def translate_high_leve_script(self, high_script):
        pass

    def add_high_level_action(self, param1, param2, param3, param4 = 1):
        pass

    def create_high_level_script(self):
        pass