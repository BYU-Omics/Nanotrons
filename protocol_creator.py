"""
    This class allows the user to create a 


"""

import sys
import os
from pathlib import Path
import json
# RELATIVE_PATH_TO_PROTOCOLS_W = ''
RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = 'protocols/'

RELATIVE_PATH_TO_LABWARE_W = '.\\saved_labware\\'
RELATIVE_PATH_TO_LABWARE_L = 'saved_labware/'

START_OF_PROTOCOL_TEXT = "#----------START OF PROTOCOL----------------------------------------\n"


LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

# Class ProtocolCreator

class ProtocolCreator:
    def __init__(self) -> None:
        self.contents = []
        self.index_for_new_command = None


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

    def get_file_contents(self, filename):
        path = self.get_path_to_protocols(filename)
        with open(path, "r") as f:
            contents = f.readlines()
        f.close()
        return contents

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
        content = []
        with open(path) as f:
            data = json.load(f)
        chips = data['chips']
        plates = data['plates']
        content.append("\n\n# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED-----------\n\n")
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

    def add_cmd_to_protocol_file(self, filename, cmd):
        contents = self.get_file_contents(filename)
        line_count = 0
        txt_to_add = "\n" + cmd + "\n\n"
        while line_count < len(contents):
            # print(f"line[{line_count}]{contents[line_count]}")
            if contents[line_count] == START_OF_PROTOCOL_TEXT:
                print(contents[line_count + 2][:9])
                if contents[line_count + 1] == '#--------------END OF PROTOCOL--------------\n':
                    print("Adding first command")
                    contents.insert(line_count + 1, txt_to_add)
                    break
                elif contents[line_count + 2][:10] == 'myProtocol':
                    print("Adding rest of the commands")
                    contents.insert(line_count + 1, txt_to_add)
                    break

            line_count += 1
        end_contents = ""
        for line in contents:
            end_contents += line
        self.write_contents_to_file(filename, end_contents)
       
                
    def write_contents_to_file(self, filename, content):
        path = self.get_path_to_protocols(filename)
        with open(path, 'r+') as f:
            f.write(content)
        f.close()

    def add_comments(self):
        pass

    def create_protocol(self, heading, labware, end_of_protocol, filename):
        txt = heading + labware + end_of_protocol
        content = ""
        for line in txt:
            content += line 
        self.write_contents_to_file(filename, content)
        
    
    def erase_command(self):
        pass

    def erase_comments(self):
        pass

    def display_protocol_commands(self):
        for line in self.contents:
            if 'myProtocol.' in line:
                print(line.strip("'myProtocol"))
        pass

    def display_protocol_comments(self):
        for line in self.contents:
            if line[0] == '#':
                print(line)

def test():
    creator = ProtocolCreator()
    protocol_name = "protocol_4.py"
    labware_name = "Test_for_protocols.json"
    
    # 
    new_name = creator.create_name_for_new_file()
    creator.create_new_file(new_name)
    heading = creator.get_file_contents("protocol_heading.txt")
    labware = creator.create_protocol_labware_txt(labware_filename=labware_name)
    eof = creator.get_file_contents("protocol_eof.txt")
    creator.create_protocol(heading, labware, eof, new_name)

    location = "custom('A2')"
    cmd = creator.create_command_txt(filename= new_name, cmd="dispense_to", volume=10, location=location)
    creator.add_cmd_to_protocol_file(filename=new_name, cmd=cmd)
    creator.add_cmd_to_protocol_file(filename=new_name, cmd=cmd)
    

if __name__ == "__main__":
    test()
