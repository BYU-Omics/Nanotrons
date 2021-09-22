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
        self.filename: str = 'no_name.py'
        self.calibration_file_name: str = 'calibration.json'
        self.syringe_model: str = 'HAMILTON_175'
        self.p = None
        self.path_to_file = None

    def set_calibration_file_name(self, name: str = None):
        print(f"Calibration filename: {name}")
        if ".json" not in name:
            print("Not a valid filename for the protocol calibration file, please use a file with the 'json' extension")
        elif name == None:
            print("The file name has not been selected properly. ")
        else:
            self.calibration_file_name = name

    def set_file_name(self, name: str = None):
        if ' ' in name:
            print("WARNING: There is a space on the name. Please replace it with an '_' before running the protocol.")
        elif ".py" not in name:
            print("WARNING: Please select a filename with the 'py' extension")
        elif name == None:
            print("WARNING: The file name for protocol has not been properly set.")
        else:
            self.filename = name

    def get_file_name(self):
        return self.filename

    def set_syringe_file_name(self, name):
        self.syringe_model = name

    def execute_python_protocol(self):
        if self.set_get_path():
            first_arg = self.set_get_path()
        else:
            sys.exit()
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
        if self.filename == "- Select a Protocol -":
            print("No protocol selected")
            return None
        else:
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

    def info_from_protocol(self) -> list:
        labware_calibration_file_name = "None set"
        author = "None set"
        description = "None set"
        try:
            if self.filename == None or self.filename == "- Select a Protocol -":
                print("No file has been selected")
                contents = "None set"
                labware_calibration_file_name = "None set"
                author = "None set"
                description = "None set"
                return [contents, labware_calibration_file_name, author, description]
            else:
                with open(self.set_get_path(), 'r') as f:
                    contents = f.readlines()
                    for line in contents:
                        if "load_labware_setup" in line:
                            labware_calibration: str = line[45:]
                            labware_calibration_file_name = labware_calibration.replace('(','').replace(')','').replace("'", "").replace("\n", "") # To get only the name as a string
                        if "author" in line:
                            author: str = line[12:]
                            author = author.replace("'", '').replace(",", '')
                        if "description" in line:
                            description: str = line[15:]
                            description = description.replace("'", '').replace(",", '')
                    return [contents, labware_calibration_file_name, author, description]
        except TypeError:
            return None
        except FileNotFoundError:
            print("File was not found on folder")
            return None
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