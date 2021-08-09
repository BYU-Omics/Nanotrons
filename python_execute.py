import subprocess
import os
import sys
import signal
import asyncio
# from opentrons import api
# from coordinator import *

# RELATIVE_PATH_TO_PROTOCOLS_W = ''
RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = 'protocols/'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'


class Py_Execute:
    def __init__(self):
        self.filename: str = 'protocol.py'
        self.calibration_file_name: str = 'calibration.json'
        self.syringe_model: str = 'HAMILTON_175'
        self.p = None
        self.path_to_file = None

    def set_calibration_file_name(self, name):
        print(f"Calibration filename: {name}")
        self.calibration_file_name = name

    def set_file_name(self, name):
        self.filename = name

    def get_file_name(self):
        return self.filename

    def set_syringe_file_name(self, name):
        self.syringe_model = name

    def execute_python_protocol(self):
        first_arg = self.set_get_path()
        second_arg = self.calibration_file_name
        third_arg = self.syringe_model
        cmd = 'python' + ' ' + first_arg + ' ' + second_arg + ' ' + third_arg
        # print(f"cmd: {cmd}")
        self.p = subprocess.Popen(cmd, shell=True)
        out, err= self.p.communicate()
        print(err)
        print(out)

    def set_get_path(self):
        path = sys.path
        if os.name == LINUX_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_PROTOCOLS_L
        elif os.name == WINDOWS_OS:
            relative_path = RELATIVE_PATH_TO_PROTOCOLS_W
        # print(f"relative_path: {relative_path}")
        self.path_to_file =  relative_path + self.filename 
        return self.path_to_file


    def stop_execution(self):
        # print("Terminate protocol")
        first_arg = self.set_get_path()
        second_arg = self.calibration_file_name
        third_arg = self.syringe_model
        cmd = 'python' + ' ' + first_arg + ' ' + second_arg + ' ' + third_arg
        subprocess.Popen(cmd, shell=True).kill()

    def display_contents(self):
        # print(f"self.set_get_path(): {self.set_get_path()}")
        with open(self.set_get_path(), 'r') as f:
            contents = f.readlines()
            print(contents)
            return contents
    # def continue_execution(self):
    #     os.kill(self.p.pid, signal.SIGCONT)

def test():
    print(os.name)
    executer = Py_Execute()
    protocol_name = "protocol_5.py"
    calibration_name = "Alex_config.json"
    executer.set_calibration_file_name(calibration_name)
    executer.set_file_name(protocol_name)
    # executer.execute_python_protocol()
    executer.display_contents()
    # executer.pause_execution()
    # executer.continue_execution()

if __name__== '__main__':
    # print(os.name)
    test()