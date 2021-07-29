"""
    This class allows the user to create a 


"""

import sys
import os
from pathlib import Path
import json
# RELATIVE_PATH_TO_PROTOCOLS_W = ''
RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = '/protocols/'

RELATIVE_PATH_TO_LABWARE_W = '.\\saved_labware\\'
RELATIVE_PATH_TO_LABWARE_L = '/saved_labware/'

START_OF_PROTOCOL_TEXT = "#----------START OF PROTOCOL----------------------------------------\n"


LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

# Class ProtocolCreator

class ProtocolCreator:
    def __init__(self) -> None:
        self.contents = []
        self.index_for_old_command = 0
        self.labware_name_stored = ""

    #------FILE HANDLING SECTION----------

    def get_path_to_protocols(self, filename):
        path = sys.path
        if os.name == LINUX_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_PROTOCOLS_L
        elif os.name == WINDOWS_OS:
            relative_path = RELATIVE_PATH_TO_PROTOCOLS_W
        path_to_file =  relative_path + filename
        return path_to_file

    def get_path_to_labware(self, filename):
        path = sys.path
        if os.name == LINUX_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_LABWARE_L
        elif os.name == WINDOWS_OS:
            relative_path = RELATIVE_PATH_TO_LABWARE_W
        path_to_file =  relative_path + filename
        return path_to_file
    
    def create_new_file(self, name):
        path = self.get_path_to_protocols(name)
        f = open(path, "x")
        print(f"File created in {path}")

    def delete_existing_file(self, name):
        path = self.get_path_to_protocols(name)
        os.remove(path)
        print(f"File {name} removed from directory.")

    def get_file_contents(self, filename):
        path = self.get_path_to_protocols(filename)
        with open(path, "r") as f:
            contents = f.readlines()
        f.close()
        return contents

    def write_contents_to_file(self, filename, content):
        path = self.get_path_to_protocols(filename)
        with open(path, 'r+') as f:
            f.write(content)
        f.close()

    #------TXT HANDLING SECTION----------

    def create_name_for_new_file(self):
        protocol = "protocol"
        number = 0
        extension = ".py"
        new_file_name = protocol + '_' + str(number) + extension
        path = self.get_path_to_protocols(new_file_name)
        while Path(path).is_file():
            number += 1
            new_file_name = protocol + '_' + str(number) + extension
            path = self.get_path_to_protocols(new_file_name)
        return new_file_name

    def create_protocol_labware_txt(self, labware_filename):
        path = self.get_path_to_labware(labware_filename)
        print(path)
        content = []
        with open(path) as f:
            data = json.load(f)
        chips = data['chips']
        plates = data['plates']
        content.append("\n\n# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED-----------\n\n")
        content.append(f"# Labware file loaded: {labware_filename}\n\n")
        chip_count = 0
        plate_count = 0
        copy_plate = 2
        chip_names_list = []
        plate_names_list = []

        for chip in chips:
            chip_name = chip['model'].lower()
            if len(chips) == 1:
                chip_name = f"{chip_name}"
            else:
                chip_name = f"{chip_name}_{chip_count}"
            content.append(f"{chip_name} = chips[{chip_count}].get_location_by_nickname \n")
            chip_count += 1
            chip_names_list.append(chip_name)
        for plate in plates:
            plate_name = plate['model'].lower()
            if plate_name in plate_names_list:
                plate_name += f"_{copy_plate}"
                copy_plate += 1
            plate_names_list.append(plate_name)
            content.append(f"{plate_name} = plates[{plate_count}].get_location_by_nickname \n")
            plate_count +=1 
        text_for_start_of_protocol = "\n" + START_OF_PROTOCOL_TEXT
        content.append(text_for_start_of_protocol)
            
        list_of_labware = chip_names_list + plate_names_list
        return content

    def create_command_txt(self, filename,  cmd = "", volume = "", location = "", temp = "", holding_time = ""):
        cmd_text = "myProtocol."
        if cmd == 'aspirate_from':
            cmd_text += f"{cmd}(amount = {volume}, source = {location})"
        elif cmd == 'dispense_to':
            cmd_text += f"{cmd}(amount = {volume}, source = {location})"
        elif cmd == 'open_lid':
            cmd_text += f"{cmd}()"
        elif cmd == 'close_lid':
            cmd_text += f"{cmd}()"
        elif cmd == 'deactivate_lid':
            cmd_text += f"{cmd}()"
        elif cmd == 'deactivate_block':
            cmd_text += f"{cmd}()"
        elif cmd == 'set_block_temp':
            cmd_text += f"{cmd}(target_temp = {temp}, holding_time_in_minutes = {holding_time})"
        elif cmd == 'set_lid_temp':
            cmd_text += f"{cmd}(temp = {temp})"
        elif cmd == 'set_tempdeck_temp':
            cmd_text += f"{cmd}(celcius = {temp}, holding_time_in_minutes = {holding_time})"
        elif cmd == 'deactivate_tempdeck':
            cmd_text += f"{cmd}()"
        elif cmd == 'deactivate_all':
            cmd_text += f"{cmd}()"
        # print(cmd_text)
        return cmd_text

    #------PROTOCOL FILE HANDLING SECTION----------

    def add_cmd_to_protocol_file(self, filename, cmd):
        contents = self.get_file_contents(filename)
        line_count = 0
        txt_to_add = "\n" + cmd + "\n"
        while line_count < len(contents):
            # print(f"line[{line_count}]{contents[line_count]}")
            if contents[line_count] == START_OF_PROTOCOL_TEXT:
                # print(f"line[{line_count}]: {contents[line_count]}")
                # print(f"line_old command[{self.index_for_old_command}]: {contents[self.index_for_old_command]}")
                if contents[line_count + 2] == '#--------------END OF PROTOCOL--------------\n':
                    print(f"Adding first command: {txt_to_add}")
                    contents.insert(line_count + 1, txt_to_add)
                    self.index_for_old_command = line_count + 2
                    break
                elif contents[self.index_for_old_command][:10] == 'myProtocol':
                    print(f"Adding command: {txt_to_add}")
                    contents.insert(line_count + 1, txt_to_add)
                    self.index_for_old_command += 2 
                    break
            line_count += 1      
        end_contents = ""
        for line in contents:
            end_contents += line
            # print(f"line: {line}")
        self.write_contents_to_file(filename, end_contents)

    def delete_existing_protocol(self, filename):
        contents = self.get_file_contents(filename)
        labware_loaded = ""
        for line in contents:
            if 'Labware file loaded' in line:
                labware_loaded = line[23:]
        self.labware_name_stored = labware_loaded.strip("\n")
        self.delete_existing_file(filename)

    def reset_file_commands(self, filename):
        self.delete_existing_protocol(filename)
        self.create_protocol_file(self.labware_name_stored, filename)

    def add_cmd_to_end_of_protocol_file(self, filename, cmd):
        contents = self.get_file_contents(filename)
        line_count = 0
        txt_to_add = "\n" + cmd + "\n"
        while line_count < len(contents):
            # print(f"line[{line_count}]{contents[line_count]}")
            if contents[line_count + 2] == '#--------------END OF PROTOCOL--------------\n':
                print("Adding command")
                contents.insert(line_count + 1, txt_to_add)
                # self.index_for_old_command = line_count + 2
                break
                # elif contents[self.index_for_old_command][:10] == 'myProtocol':
                #     print("Adding rest of the commands")
                #     contents.insert(line_count + 1, txt_to_add)
                #     self.index_for_old_command += 2 
                #     break
            line_count += 1      
        end_contents = ""
        for line in contents:
            end_contents += line
            # print(f"line: {line}")
        self.write_contents_to_file(filename, end_contents)

    def add_list_of_commands_to_protocol_file(self, filename, list_of_cmds: list):
        for command in reversed(list_of_cmds):
            self.add_cmd_to_protocol_file(filename=filename, cmd=command) 
        print("List of commands added to {filename}")
                
    def create_protocol_file(self, labware_name, filename: str = None):
        if filename != None:
            new_name = filename
        else:
            new_name = self.create_name_for_new_file()
        self.create_new_file(new_name)
        print(labware_name)
        heading = self.get_file_contents("protocol_heading.txt")
        labware = self.create_protocol_labware_txt(labware_filename=labware_name)
        end_of_protocol = self.get_file_contents("protocol_eof.txt")
        newline = ["\n"]
        txt = heading + labware + newline + end_of_protocol
        content = ""
        for line in txt:
            content += line 
        self.write_contents_to_file(new_name, content)
        print(f"File {new_name} created in directory")

    #------PROTOCOL COMMAND'S LIST HANDLING SECTION----------   

    def get_list_of_commands_from_file(self, filename):
        contents = self.get_file_contents(filename)
        commands_list = []
        for line in contents:
            if 'myProtocol.' in line:
                if 'load_labware_setup' in line:
                    pass
                elif 'end_of_protocol' in line:
                    pass
                else:
                    commands_list.append(line)
        return commands_list

    def erase_command(self, commands: list, position):
        if commands.count == 0:
            print("No commands in list of commands")
        else:
            commands.pop(position)
        return commands

    def add_command_to_a_position_on_list(self, cmd, commands:list, position):
        commands.insert(position, cmd)
        return commands

    def add_command_to_end_of_list(self, cmd, commands: list):
        commands.append(cmd)
        return commands

    #------PROTOCOL DISPLAY SECTION----------

    def display_protocol_commands(self):
        for line in self.contents:
            if 'myProtocol.' in line:
                print(line.strip("'myProtocol"))
        pass

    def display_protocol_comments(self):
        for line in self.contents:
            if line[0] == '#':
                print(line)

#------FUNCTION TESTS SECTION----------

def tets_creation_of_file():
    creator = ProtocolCreator()
    labware = "Test_for_protocols.json"
    creator.create_protocol_file(labware)

def tests_adding_lists_of_commands():
    creator = ProtocolCreator()
    name = "protocol_0.py"
    location = "custom('A2')"
    cmd = creator.create_command_txt(filename= name, cmd="dispense_to", volume=10, location=location)
    cmd_2 = creator.create_command_txt(filename= name, cmd="open_lid")
    list_of_commands = [cmd, cmd, cmd, cmd, cmd, cmd, cmd, cmd, cmd, cmd_2, cmd, cmd_2]
    creator.add_list_of_commands_to_protocol_file(filename = name,list_of_cmds = list_of_commands)

def tests_adding_a_command_to_the_end_of_file():
    creator = ProtocolCreator()
    name = "protocol_0.py"
    location = "custom('A2')"
    cmd = creator.create_command_txt(filename= name, cmd="dispense_to", volume=10, location=location)
    creator.add_cmd_to_end_of_protocol_file(name, cmd)

def tests_handling_commands():
    creator = ProtocolCreator()
    name = "protocol_0.py"
    # commands = creator.get_list_of_commands_from_file(name)
    # print(f"Getting list of commands:\n {commands}")
    # commands = creator.erase_command(commands, 0)
    # location = "custom('A2')"
    # cmd = creator.create_command_txt(filename= name, cmd="dispense_to", volume=10, location=location)
    # creator.add_command_to_end_of_list(cmd, commands)
    # print(f"Adding a command to end of list:\n {commands}")
    # creator.add_command_to_a_position_on_list(cmd, commands, 1)
    # print(f"Adding a command to position {1} on list:\n {commands}")
    # creator.add_list_of_commands_to_protocol_file(name, commands)
    # print(f"Adding new list to file")
    # creator.delete_existing_protocol(name)
    creator.reset_file_commands(name)

def test():
    # tets_creation_of_file()
    # tests_adding_lists_of_commands()
    # tests_adding_a_command_to_the_end_of_file()
    tests_handling_commands()

if __name__ == "__main__":
    test()
