import subprocess
import os
import sys
import signal
import asyncio
# from opentrons import api
# from coordinator import *

# RELATIVE_PATH_TO_PROTOCOLS_W = ''
RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = '/protocols/'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'


class Py_Execute:
    def __init__(self):
        self.filename: str = 'Protocol.py'
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
        cmd = 'python' + ' ' + first_arg 
        self.p = subprocess.Popen(cmd, shell=True)
        out, err= self.p.communicate()
        if err == None:
            print("Protocol ended without errors")
        else:
            print(err)
            if out != None:
                print(out)
    def set_get_path(self):
        path = sys.path
        if os.name == LINUX_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_PROTOCOLS_L
        elif os.name == WINDOWS_OS:
            relative_path = RELATIVE_PATH_TO_PROTOCOLS_W
        self.path_to_file =  relative_path + self.filename 
        return self.path_to_file

    def pause_execution(self):
        print("Pausing execution")
        os.kill(self.p.pid, signal.SIGSTOP)

    def continue_execution(self):
        print("Continuing execution")
        os.kill(self.p.pid, signal.SIGCONT)

    def stop_execution(self):
        print("Terminate protocol")
        subprocess.Popen.terminate(self=self.p)

    def display_contents(self):
        with open(self.set_get_path(), 'r') as f:
            contents = f.readlines()
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