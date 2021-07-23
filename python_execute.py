import subprocess
import os
import sys
import signal
# from opentrons import api
# from coordinator import *

# RELATIVE_PATH_TO_PROTOCOLS_W = ''
<<<<<<< HEAD
RELATIVE_PATH_TO_PROTOCOLS_W = 'protocols\\'
=======
RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
>>>>>>> newrepo
RELATIVE_PATH_TO_PROTOCOLS_L = '/protocols/'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'


class Py_Execute:
    def __init__(self):
        self.filename: str = 'protocol.py'
        self.calibration_file_name: str = 'calibration.json'
        self.p = None

    def set_calibration_file_name(self, name):
        print(f"Calibration filename: {name}")
        self.calibration_file_name = name

    def set_file_name(self, name):
        self.filename = name

    def execute_python_protocol(self):
        path = sys.path
        print(path[0])
        if os.name == LINUX_OS:
            cmd = 'python' + ' ' + path[0] + RELATIVE_PATH_TO_PROTOCOLS_L + self.filename + ' ' + self.calibration_file_name
        elif os.name == WINDOWS_OS:
            cmd = 'python' + ' ' + RELATIVE_PATH_TO_PROTOCOLS_W + self.filename + ' ' + self.calibration_file_name
        print(cmd)
        self.p = subprocess.Popen(cmd, shell=True)
        out, err= self.p.communicate()
        print(err)
        print(out)

<<<<<<< HEAD
    # def pause_execution(self):
    #     os.kill(self.p.pid, signal.SIGSTOP)
=======
    def stop_execution(self):
        print("Terminate protocol")
        self.p.terminate()
>>>>>>> newrepo

    # def continue_execution(self):
    #     os.kill(self.p.pid, signal.SIGCONT)

def test():
    print(os.name)
    executer = Py_Execute()
    protocol_name = "protocol_1.py"
    calibration_name = "labware_for_test.json"
    executer.set_calibration_file_name(calibration_name)
    executer.set_file_name(protocol_name)
    executer.execute_python_protocol()
    # executer.pause_execution()
    # executer.continue_execution()

if __name__== '__main__':
    # print(os.name)
    test()