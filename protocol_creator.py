"""
    This class allows the user to create a protocol


"""

from typing import List

from opentrons_shared_data.deck.dev_types import Metadata
from plate import Plate
import sys
import os
from pathlib import Path
import json
import csv
import re
import datetime

# RELATIVE_PATH_TO_PROTOCOLS_W = ''
RELATIVE_PATH_TO_PROTOCOLS_W = '\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = '/protocols/'

RELATIVE_PATH_TO_LABWARE_W = '\\saved_labware\\'
RELATIVE_PATH_TO_LABWARE_L = '/saved_labware/'

START_OF_PROTOCOL_TEXT = "# ------------START OF PROTOCOL---------------------------------\n"


LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

# Texxt for the commands 
SET_WASHING_POSITIONS_CMD = 'set_washing_positions'
START_WASH_CMD = 'start_wash'
MID_WASH_CMD = 'mid_wash'
AIR_GAP_CMD = 'air_gap'
LOAD_LABWARE_SET_UP_CMD = 'load_labware_setup'
END_OF_PROTOCOL_CMD = 'end_of_protocol'
ASPIRATE_CMD = 'aspirate_from'
DISPENSE_CMD = 'dispense_to'
OPEN_LID_CMD = 'open_lid'
CLOSE_LID_CMD = 'close_lid'
DEACTIVATE_LID_CMD = 'deactivate_lid'
DEACTIVATE_BLOCK_CMD = 'deactivate_block'
SET_BLOCK_TEMP_CMD = 'set_block_temp'
SET_LID_TEMP_CMD = 'set_lid_temp'
SET_TEMPDECK_TEMP_CMD = 'set_tempdeck_temp'
DEACTIVATE_TEMPDECK_CMD = 'deactivate_tempdeck'
DEACTIVATE_ALL_CMD = 'deactivate_all'
TAKE_PICTURE = 'take_picture'
VOID_PLATE_DEPTH_CMD = 'void_plate_depth'
PLATE_DEPTH = "Plate's depth"
TEXT_FOR_VOID_DEPTH_PLATES = "# If the depth has been voided for any of the plates, this is specified here:\n\n"
NO_PLATES_DEPTH_VOIDED_TXT = "# WARNING: Dispensing and aspirating from bottom of ALL plates.\n" 
MY_PROTOCOL_TXT = "myProtocol."
CALIBRATION_ORDER_TXT = "# ----------CHIPS AND PLATES ARE LOADED IN THE ORDER THEY WERE CALIBRATED, this determines the index-----------\n\n"
PRE_PROTOCOL_SETUP_TXT = "# -----------PREPROTOCOL SETUP-------------------\n\n"
END_OF_PROTOCOL_TXT = '# --------------END OF PROTOCOL--------------\n'
CMD = 'cmd'
VOLUME = 'volume'
LABWARE = 'labware'
LOCATION = 'location'
TEMP = 'temp'
HOLDING_TIME = 'holding_time'
PLATE = 'plate'
DEPTH = 'depth'
SOURCE = 'source'

# Class ProtocolCreator

class ProtocolCreator:
    def __init__(self) -> None:
        self.contents = []
        self.index_for_old_command = 0
        self.labware_name_stored = ""

    # ------FILE HANDLING SECTION----------

    def get_path_to_protocols(self, filename: str) -> str:
        """This function builds the path to a file in the protocol's folder
            given the same of the file

        Args:
            filename ([type]): a name for a file to open

        Returns:
            path_to_file str: returns a string that contains the path
        """        
        path = sys.path
        if os.name == LINUX_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_PROTOCOLS_L
        elif os.name == WINDOWS_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_PROTOCOLS_W
        path_to_file =  relative_path + filename
        return path_to_file

    def get_path_to_labware(self, filename: str) -> str:
        """This function builds the path to a file tthat is in the labware folder
            given the name of the file

        Args:
            filename (str): a name for a file to open

        Returns:
            str: returns a string that contains the path
        """        
        path = sys.path
        if os.name == LINUX_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_LABWARE_L
        elif os.name == WINDOWS_OS:
            relative_path = path[0] + RELATIVE_PATH_TO_LABWARE_W
        path_to_file =  relative_path + filename
        return path_to_file
    
    def create_new_file(self, filename: str):
        """This function creates a new file in the directory

        Args:
            filename (str): a name for a file to open
        """           
        path = self.get_path_to_protocols(filename)
        f = open(path, "x")
        return path

    def delete_existing_file_in_prot_folder(self, filename: str):
        """This function deletes a file located in the protocols folder 

        Args:
            filename (str): a name for a file to delete
        """        
        path = self.get_path_to_protocols(filename)
        os.remove(path)
        print(f"File {filename} removed from directory.")

    def get_file_contents(self, filename: str) -> list:
        """This function

        Args:
            filename (str): a name for a file to open

        Returns:
            list: list containing all the lines in a file 
        """        
        path = self.get_path_to_protocols(filename)
        with open(path, "r") as f:
            contents = f.readlines()
        f.close()
        return contents

    def write_contents_to_file(self, filename: str, content):
        """This function take a list and write the elements in to a file 

        Args:
            filename (str): a name for a file to open
            content (list): what its going to be written in the file
        """        
        path = self.get_path_to_protocols(filename)
        with open(path, 'r+') as f:
            f.write(content)
        f.close()

    # ------TXT HANDLING SECTION----------

    def create_name_for_new_file(self, extension: str) -> str:
        """This function creates a name for a new file with a csv or py extension.
            if the filename already exist in the directory of protocols it will
            create a new one with a different index so that it does not replace the previous one
        Args:
            extension (str): this is the extension that you are trying to create the file with 

        Returns:
            str: the name for the new file to create. 
        """           
        protocol = "My Protocol"
        current_time =  datetime.datetime.now()
        counter = 0
        if extension == 'py':
            extension = ".py"
        elif extension == 'csv':
            extension = ".csv"
        date_and_time = f" {current_time.month}-{current_time.day}-{current_time.year} at {current_time.hour}.{current_time.minute}.{current_time.second}"
        new_file_name = protocol + date_and_time + extension
        path = self.get_path_to_protocols(new_file_name)
        while Path(path).is_file():
            counter += 1
            new_file_name = protocol + '_' + str(counter) + extension
            path = self.get_path_to_protocols(new_file_name)
        return new_file_name

    def create_protocol_labware_txt(self, labware_filename: str) -> list:
        """This function puts together the texts used as a template for the labware 
        that this protocol will use

        Args:
            labware_filename (str): this is the name of a json file containing all the locations
            for the calibrated labware that the protocol will use

            this ends looking like this for example:
                micropots_3 = chips[0] 
                corning_384 = plates[0] 
                custom = plates[1] 
                custom_small = plates[2] 

        Returns:
            list: text as a list of the contents to put in the protocol
        """  
        path = self.get_path_to_labware(labware_filename)
        content = []
        with open(path) as f:
            data = json.load(f)
        chips = data['chips']
        plates = data['plates']
        content.append(CALIBRATION_ORDER_TXT)
        content.append(f"chips, plates = myProtocol.load_labware_setup('{labware_filename}')\n\n" 
)
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
            content.append(f"{chip_name} = chips[{chip_count}] \n")
            chip_count += 1
            chip_names_list.append(chip_name)
        for plate in plates:
            plate_name = plate['model'].lower()
            if plate_name in plate_names_list:
                plate_name += f"_{copy_plate}"
                copy_plate += 1
            plate_names_list.append(plate_name)
            content.append(f"{plate_name} = plates[{plate_count}] \n")
            plate_count +=1
        return content, chip_names_list, plate_names_list

    def create_protocol_labware_location_txt(self, chip_names_list: list, plate_names_list: list) -> list:
        """This function creates the text that will allow the protocol to use the location for each pot or well
            it ends looking like this as an example: 
            
                micropots_3 = micropots_3.get_location_by_nickname 
                corning_384 = corning_384.get_location_by_nickname 
                custom = custom.get_location_by_nickname 
                custom_small = custom_small.get_location_by_nickname 


        Args:
            chip_names_list (list): list of the names for the chips used in the labware configuration file 
            plate_names_list (list): list of the names for the plates used in the labware configuration file 

        Returns:
            list: list of lines containing the context to write to the protocol file 
        """        
        content = []
        for chip in chip_names_list:
            content.append(f"{chip} = {chip}.get_location_by_nickname \n")
        for plate in plate_names_list:
            content.append(f"{plate} = {plate}.get_location_by_nickname \n")
        return content

    def create_protocol_voided_depth_for_labware(self, labware_filename: str, list_of_voided_plates: list = None) -> list:
        """This function creates the txt that will go into the protocol file 
            indicating which plates will have their depth voided, this means that the z axis will not move 
            the plate's specified depth in the .json file. This is a very important step becaue if 
            it is not in the protocol it will be assumed that the z axis will move Xmm down when aspirating 
            or dispensing liquid. This downward movement could break the instruments on the way and the mount. 
            Only the human user can check this so far.

        Args:
            labware_filename (str): name for a file with the labware calibration 
            list_of_voided_plates (list, optional): Plates that the user desires to void the depth. Defaults to None.

        Returns:
            list: the contents to write in the file as a list.
        """        
        path = self.get_path_to_labware(labware_filename)
        plate_count = 0
        plate_names_list = []
        content = []
        content.append(TEXT_FOR_VOID_DEPTH_PLATES)
        with open(path) as f:
            data = json.load(f)
            plates = data['plates']
            #create the list of names of plates that were calibrated
            for plate in plates:
                plate_name = plate['model'].lower()
                plate_names_list.append(plate_name)
            #search for the plates that the depth will be voided. 
            # for each plate calibrated, if this name matches a plate in the voided list
            for plate_name in plate_names_list:
                if plate_name in list_of_voided_plates:
                    content.append(self.create_command_txt(cmd = VOID_PLATE_DEPTH_CMD, 
                                                           plate = plate_name,  
                                                           plate_index=plate_count, 
                                                           void = True) + '\n')
                plate_count += 1
        plates_voided_txt = ""
        for cmd in content:
            plates_voided_txt += cmd + '\n'
        return content

    def create_command_txt(self, cmd = None, 
                                 volume = None, 
                                 labware = None, 
                                 location = None, 
                                 temp = None, 
                                 holding_time = None, 
                                 plate: Plate = None, 
                                 void: bool = None, 
                                 plate_index: int = None,
                                 clean_water = None, 
                                 wash_water = None, 
                                 waste_water = None,
                                 left_over = None, 
                                 cushion_1 = None, 
                                 cushion_2 = None) -> str:
        """[summary]

        Args:
            cmd ([type], optional): [description]. Defaults to None.
            volume ([type], optional): [description]. Defaults to None.
            labware ([type], optional): [description]. Defaults to None.
            location ([type], optional): [description]. Defaults to None.
            temp ([type], optional): [description]. Defaults to None.
            holding_time ([type], optional): [description]. Defaults to None.
            plate (Plate, optional): [description]. Defaults to None.
            void (bool, optional): [description]. Defaults to None.
            plate_index (int, optional): [description]. Defaults to None.
            clean_water ([type], optional): [description]. Defaults to None.
            wash_water ([type], optional): [description]. Defaults to None.
            waste_water ([type], optional): [description]. Defaults to None.
            left_over ([type], optional): [description]. Defaults to None.
            cushion_1 ([type], optional): [description]. Defaults to None.
            cushion_2 ([type], optional): [description]. Defaults to None.

        Returns:
            str: [description]
        """                                 
        cmd_text = MY_PROTOCOL_TXT
        if cmd == ASPIRATE_CMD:
            cmd_text += f"{cmd}(volume = {volume}, {SOURCE} = {labware}('{location}'))"
        elif cmd == DISPENSE_CMD:
            cmd_text += f"{cmd}(volume = {volume}, to = {labware}('{location}'))"
        elif cmd == OPEN_LID_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == CLOSE_LID_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == DEACTIVATE_LID_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == DEACTIVATE_BLOCK_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == SET_BLOCK_TEMP_CMD:
            cmd_text += f"{cmd}(target_temp = {temp}, holding_time_in_minutes = {holding_time})"
        elif cmd == SET_LID_TEMP_CMD:
            cmd_text += f"{cmd}(temp = {temp})"
        elif cmd == SET_TEMPDECK_TEMP_CMD:
            cmd_text += f"{cmd}(celcius = {temp}, holding_time_in_minutes = {holding_time})"
        elif cmd == DEACTIVATE_TEMPDECK_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == DEACTIVATE_ALL_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == TAKE_PICTURE:
            cmd_text += f"{cmd}()" 
        elif cmd == VOID_PLATE_DEPTH_CMD:
            cmd_text += f"{cmd}(plate = {plate}, void = {void})"
        elif cmd == SET_WASHING_POSITIONS_CMD:
            cmd_text += f"{cmd}({clean_water}, {wash_water}, {waste_water})"
        elif cmd == START_WASH_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == MID_WASH_CMD:
            cmd_text += f"{cmd}()"
        elif cmd == AIR_GAP_CMD:
            cmd_text += f"{cmd}({left_over}, {cushion_1}, {cushion_2})"
        return cmd_text

    def create_cmd_argumens_from_text(self, cmd_text:str) -> dict:
        """This function recognices a command on a protocol and it disects its parts finding the arguments
            returning these as a dictionary to later process them easily

        Args:
            cmd_text (str): This is the command to disect in a string form

        Returns:
            dict: Disctionary with the arguments 
        """        
        cmd_dictionary: dict = {}
        left_side_of_parenthesys = cmd_text.split("(", 1)[0]
        right_side_of_parenthesys = cmd_text.split("(", 1)[1]
        clean_right_side = right_side_of_parenthesys.replace("))", ")")
        command = left_side_of_parenthesys.split(".")[1]
        cmd_dictionary.update({CMD: f"{command}"}) 
        arguments = clean_right_side.split(", ")
        for argument in arguments:
            argument = argument.split(" = ")
            if SOURCE in argument:
                source_arg = argument[1].strip(")")
                source_arg = source_arg.split("(")
                labware = source_arg[0]
                location = source_arg[1].strip("'")
                cmd_dictionary.update({f"{LABWARE}": f"{labware}"})
                cmd_dictionary.update({f"{LOCATION}": f"{location}"})
            else:
                cmd_dictionary.update({f"{argument[0]}": f"{argument[1]}"}) 
        return cmd_dictionary
   
    def create_metadata_txt(self, metadata: dict = None, 
                                  protocol_name: str = None, 
                                  author: str = None, 
                                  description: str = None) -> list:
        """This function puts together the information passed to it to create a text that 
            will appear in the protocol heading. This contains the author, name of the protocol and
            brief description

        Args:
            metadata (dict, optional): This could be a json file or simple dictionary with the information. Defaults to None.
            protocol_name (str, optional): name given to the protocol. Defaults to None.
            author (str, optional): who is editing the protocol. Defaults to None.
            description (str, optional): brief explanation of the purpose of the protocol. Defaults to None.

        Returns:
            list: [description]
        """                                  
        txt = ['\n\n']
        if metadata:
            # if a dictionary with thte information is given
            protocol_name = metadata['protocolName']
            author = metadata['author']
            description = metadata['description']
            metadata_txt = f"metadata = {metadata}"
        else:
            # if the protocol_name, author, description are passed to the function
            protocol_name, author, description = protocol_name, author, description
            metadata_txt = f"metadata = {{\n\t'protocolName': '{protocol_name}', \n\t'author': '{author}', \n\t'description': '{description}' \n}}\n\n"
        txt.append(metadata_txt)
        return txt

    def create_washing_wells_config_txt(self, waste_water_well: str = None, 
                                              wash_water_well: str = None, 
                                              clean_water_well: str= None) -> list:
        """Puts together the text that indicates which locations from the labware set up will be used as 
            the waste, wash and clean water so that the syringe can be washed on the start and in the midwash

        Args:
            waste_water_well (str): a location on the labware
            wash_water_well (str): a location on the labware
            clean_water_well (str): a location on the labware

        Returns:
            list: returns the content to be written to the protocol heading
        """               

        if waste_water_well and wash_water_well and clean_water_well:
            waste_water = waste_water_well # custom('A1')
            wash_water = wash_water_well # custom('A2')
            clean_water = clean_water_well # custom('A3')

            waste_water_txt = f"waste_water = {waste_water}\n"
            wash_water_txt = f"wash_water = {wash_water}\n"
            clean_water_txt = f"clean_water = {clean_water}\n\n"

            cmd_set = self.create_command_txt(cmd = SET_WASHING_POSITIONS_CMD, 
                                            clean_water=clean_water, 
                                            waste_water=waste_water, 
                                            wash_water=wash_water) 
            cmd_start = self.create_command_txt(cmd = START_WASH_CMD)
            content = ["# Designated wells for washing tip\n", waste_water_txt, 
                                                            wash_water_txt, 
                                                            clean_water_txt, 
                                                            cmd_set, "\n\n" , 
                                                            cmd_start, "\n"]
        else:
            content = ["# WARNING: No washing configurations have been set. ", "\n"]
        return content
        
    # ------PROTOCOL FILE HANDLING SECTION----------

    def add_cmd_to_protocol_file(self, filename: str, cmd: str):
        """This function takes a protocol, and finds the end of the protocol and adds a command

        Args:
            filename (str): name of the protocol file to be modified 
            cmd (str): a command with one of the api.py functions 
        """        
        contents = self.get_file_contents(filename)
        line_count = 0
        txt_to_add: str = "\n" + cmd + "\n"
        while line_count < len(contents):
            if "--START OF PROTOCOL--" in contents[line_count]:
                if "END OF PROTOCOL" in contents[line_count + 2]:
                    contents.insert(line_count + 1, txt_to_add)
                    self.index_for_old_command = line_count + 2
                    break
                elif "myProtocol" in contents[self.index_for_old_command][:10]:
                    contents.insert(line_count + 1, txt_to_add)
                    self.index_for_old_command += 2 
                    break
            line_count += 1  
        end_contents = ""
        for line in contents:
            end_contents += line
        self.write_contents_to_file(filename, end_contents)

    def delete_existing_protocol(self, filename: str):
        """This function delets a protocol, but it stores on memory as an attribute the labware file that was loaded into the protocol

        Args:
            filename (str): The name of the file to be deleted
        Returns:
            [str]: [description]
        """            
        contents = self.get_file_contents(filename)
        labware_loaded = ""
        for line in contents:
            if 'Labware file loaded' in line:
                labware_loaded = line[23:]
        self.delete_existing_file_in_prot_folder(filename)
        labware_name = labware_loaded.strip("\n")
        return labware_name
        

    def reset_file_commands(self, filename: str):
        """This function takes an existing protocol and deletes the commands used on it. 

        Args:
            filename (str): Name of the protocol file to be modified 
        """
        contents = self.get_file_contents(filename)
        labware_loaded = ""
        start_of_cmd_indx = 0
        end_of_cmd_indx = 0
        counter = 0
        for line in contents:
            if "START OF PROTOCOL" in line:
                start_of_cmd_indx = counter
            if "END OF PROTOCOL" in line:
                end_of_cmd_indx = counter
            counter += 1
        for line_indx in range(start_of_cmd_indx, end_of_cmd_indx):
            contents.pop(start_of_cmd_indx + 1)
            if "END OF PROTOCOL" in contents[start_of_cmd_indx + 1]:
                contents.insert(start_of_cmd_indx + 1, "\n")
                break
        self.delete_existing_file_in_prot_folder(filename)
        self.create_new_file(filename)

        end_contents = ""
        for line in contents:
            end_contents += line
        self.write_contents_to_file(filename, end_contents)
        
    def add_cmd_to_end_of_protocol_file(self, filename: str, cmd: str):
        """This function read the file, and adds a command to the end of the file 

        Args:
            filename (str): a name for the file to edit
            cmd (str): an api command
        """        
        contents = self.get_file_contents(filename)
        line_count = 0
        txt_to_add = "\n" + cmd + "\n"
        while line_count < len(contents):
            if contents[line_count + 2] == END_OF_PROTOCOL_TXT:
                contents.insert(line_count + 1, txt_to_add)
                break
            line_count += 1      
        end_contents = ""
        for line in contents:
            end_contents += line
        self.write_contents_to_file(filename, end_contents)

    def add_list_of_commands_to_protocol_file(self, filename: str, list_of_cmds: list):
        """This function reverses the list and ads it to the protocol file 

        Args:
            filename (str): a name for a file 
            list_of_cmds (list): list of api commands 
        """        
        for command in reversed(list_of_cmds):
            self.add_cmd_to_protocol_file(filename=filename, cmd=command) 
                
    def create_protocol_file(self, labware_name = None, 
                                   filename: str = None, 
                                   voided_plates: list = None, 
                                   list_of_commands: list = None, 
                                   author: str = 'User name', 
                                   description: str = 'Missing information',
                                   waste_water_well: str = '',
                                   wash_water_well: str = '',
                                   clean_water_well: str = '') -> str:
        """This is the main function for the protocol creator. This function crates a new file with 
           all the input from the user. It creates a readable file for the executer. Organizes the order of elements 
           to be written to the protocol like the heading, configuration and several other parts 

        Args:
            labware_name ([type]): name of the json file located in saved_labware
            filename (str, optional): filename for the new script. Defaults to None.
            voided_plates (list, optional): list of plates that the depth will not be taken into account. Defaults to None.
            list_of_commands (list, optional): list of the commands for the protocol. Defaults to None.
            author (str, optional): name of the author of the protocol. Defaults to ''.
            description (str, optional): brief explanation of the protocol. Defaults to ''.
            waste_water_well (str, optional): a position in which the waste water is located for the protocol. Defaults to ''.
            wash_water_well (str, optional): a position in which the wash water is located for the protocol. Defaults to ''.
            clean_water_well (str, optional): a position in which the clean water is located for the protocol. Defaults to ''.

        Returns:
            str: the name of the new file created 
        """                                   
        current_time =  datetime.datetime.now()
        flag_for_checking = True
        # Set the name for the file to write. 
        if filename != None:
            new_name = filename + f" {current_time.month}-{current_time.day}-{current_time.year} at {current_time.hour}.{current_time.minute}.{current_time.second}" + ".py"
        else:
            # if there is no name given freate a new name.
            new_name = self.create_name_for_new_file(extension='py')
    
        path = self.create_new_file(new_name) # create the file on directory

        heading = self.get_file_contents("protocol_heading.txt") # Text for heading 
        metadata = self.create_metadata_txt(protocol_name=new_name, author=author, description=description)
        if labware_name != None:
            labware, chips, plates = self.create_protocol_labware_txt(labware_filename=labware_name) # Text for the labware used (chips and plates loaded)
            labware_location = self.create_protocol_labware_location_txt(chips, plates)
            if voided_plates != None:
                voided_plate_txt = self.create_protocol_voided_depth_for_labware(labware_name, voided_plates)
            else:
                voided_plate_txt = [NO_PLATES_DEPTH_VOIDED_TXT]
        else:
            labware_name = '# WARNING: No labware name has been given\n'
            labware = '# WARNING: Not able to set labware\n'
            labware_location = '# WARNING: Not able to retrieve labware location\n'
            voided_plate_txt = [NO_PLATES_DEPTH_VOIDED_TXT]

        
        start_of_protocol_txt = [START_OF_PROTOCOL_TEXT] # Start adding text to a list to build the final text
        pre_protocol_setup_txt = [PRE_PROTOCOL_SETUP_TXT]
        
        washing_config_txt = self.create_washing_wells_config_txt(waste_water_well=waste_water_well, 
                                                                  wash_water_well=wash_water_well, 
                                                                  clean_water_well=clean_water_well)
        end_of_protocol = self.get_file_contents("protocol_eof.txt")
        newline = ["\n"]
        
        txt = [heading, 
               metadata, 
               labware, 
               newline, 
               voided_plate_txt, 
               newline, 
               pre_protocol_setup_txt, 
               labware_location, 
               newline, 
               washing_config_txt, 
               newline, 
               start_of_protocol_txt, 
               newline, 
               end_of_protocol]
        content = ""
        for block in txt:
            for line in block:
                content += line
        self.write_contents_to_file(new_name, content)
        if labware_name != None:
            if list_of_commands != None:
                if self.check_that_commands_match_labware(list_of_commands = list_of_commands, chips = chips, plates = plates):
                    self.add_list_of_commands_to_protocol_file(filename=new_name, list_of_cmds=list_of_commands)
            else:
                flag_for_checking = False
                self.add_list_of_commands_to_protocol_file(filename=new_name, list_of_cmds=['# WARNING: No commands were given.'])
        else:
            flag_for_checking = False
            self.add_list_of_commands_to_protocol_file(filename=new_name, list_of_cmds=['# WARNING: Not able to write commands to the protocol.'])
        if flag_for_checking == False:
            print("Something went wrong while writting the file. Check 'WARNINGS' messages before running.")
        print(f"File '{new_name}' written to '{path.strip(new_name)}'")
        return new_name

    # ------PROTOCOL COMMAND'S LIST HANDLING SECTION----------   

    def check_that_commands_match_labware(self, list_of_commands: list = None, chips: list = None, plates: list  = None) -> bool:
        """Thif function will received the labware that the user is trying to use along with the commands, then
           it checks that the commands are using the labware that it has been added to the protocol and returns
           a boolean 

        Args:
            list_of_commands (list, optional): [description]. Defaults to None.

        Returns:
            [bool]: This is a boolean indicating that the labware and commands match or not
        """       
        chips_that_match = [] 
        plates_that_match = [] 
        matched = None
        for command in list_of_commands:
            for chip in chips:
                if chip in command and chip not in chips_that_match:
                    chips_that_match.append(chip)
            for plate in plates:
                if plate in command and plate not in plates_that_match:
                    plates_that_match.append(plate)
        if set(chips_that_match) == set(chips) and set(plates_that_match) == set(plates):
            matched = True
        else: 
            print("The calibrated items do not match the commands to execute.")
            matched = False
        return matched

    def get_list_of_commands_from_file(self, filename: str) -> list:
        """This function reads a file and it gets the commands that it has into a list to be processed for another function

        Args:
            filename (str): name of the file in which we are getting the commands 

        Returns:
            list: list of the commands for better handling 
        """        
        contents = self.get_file_contents(filename)
        commands_list = []
        for line in contents:
            if 'myProtocol.' in line:
                if LOAD_LABWARE_SET_UP_CMD in line:
                    pass
                elif END_OF_PROTOCOL_CMD in line:
                    pass
                else:
                    commands_list.append(line)
        return commands_list

    def create_list_of_commands(self) -> list:
        """Simple function that initialices a new list of commands 

        Returns:
            list: list of commands empty
        """        
        new_list_of_commands = [] 
        return new_list_of_commands

    def erase_command(self, commands: list, position: int):
        """This function is so that we can pop a command from the list 

        Args:
            commands (list): list of commands 
            position (int): an index in which the desired command to erase is located

        Returns:
            [type]: modified list of commands 
        """        
        if commands.count == 0:
            print("No commands in list of commands")
        else:
            commands.pop(position)
        return commands

    def add_command_to_a_position_on_list(self, cmd: str, commands: list, position: int) -> list:
        """This function takes a commands and it inserts it into a list in the position given 

        Args:
            cmd (str): a commands from the api
            commands (list): list of commands to add to 
            position (int): index in which the desired command will be inserted

        Returns:
            list: modified list of commands 
        """        
        commands.insert(position, cmd)
        return commands

    def add_command_to_end_of_list(self, cmd: str, commands: list) -> list:
        """This function adds a commnands to the end of a list of commands. Similar to the 
        add command to the end of the protocol but working with lists 

        Args:
            cmd (str): a command from the api
            commands (list): [description]

        Returns:
            list: [description]
        """        
        commands.append(cmd)
        return commands
    
    # ------PROTOCOL CSV HANDLING SECTION-----

    def convert_csv_to_cmd_list(self, filename: str) -> list:
        """This function reads a csv file formated as cmd,volume,labware,location,temp,holding_time,plate,depth for the columns

        Args:
            filename (str): a name for a csv file

        Returns:
            list: returns a list with the commands on the csv file
        """        
        path_to_file = self.get_path_to_protocols(filename)
        colums_names = []
        cmd_list = []
        with open(path_to_file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    for key in row.keys():
                        colums_names.append(key)
                    line_count += 1
                cmd = row[CMD]
                if VOLUME in colums_names:
                    volume = row[VOLUME]
                else:
                    volume = None
                if LABWARE in colums_names:
                    labware = row[LABWARE]
                else:
                    labware = None
                if LOCATION in colums_names:
                    location = row[LOCATION]
                else:
                    location = None
                if TEMP in colums_names:
                    temp = row[TEMP]
                else:
                    temp = None
                if HOLDING_TIME in colums_names:
                    holding_time = row[HOLDING_TIME]
                else:
                    holding_time = None
                if PLATE in colums_names:
                    plate = row[PLATE]
                else:
                    plate = None
                if DEPTH in colums_names:
                    depth = row[DEPTH]
                else:
                    depth = None
                cmd_list.append(self.create_command_txt(cmd=cmd,
                                                        volume=volume, 
                                                        labware=labware, 
                                                        location=location, 
                                                        temp=temp, 
                                                        holding_time=holding_time, 
                                                        plate=plate, 
                                                        depth=depth))
                line_count += 1
        return cmd_list
    
    def convert_cmd_list_to_csv(self, list_of_commands: list):
        """This function takes a list of commands and it converts it to csv file formated as the example

        Args:
            list_of_commands (list): list of commands from the api
        """        
        csv_filename = self.create_name_for_new_file('csv')
        path_to_file = self.get_path_to_protocols(csv_filename)
        first_row = [CMD, VOLUME, LABWARE, LOCATION, TEMP, HOLDING_TIME, PLATE, DEPTH]
        list_of_dict = self.convert_list_of_cmds_to_list_of_dict(list_of_commands)
        with open(path_to_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=first_row)
            writer.writeheader()
            for command in list_of_dict:
                writer.writerow(command)

    def convert_list_of_cmds_to_list_of_dict(self, list_of_commands: list) -> dict:
        """This function converts commands on a list to a dictionary for easier access

        Args:
            list_of_commands (list): list of commands 

        Returns:
            dict: dictionary with the keys: arguments, values: assignments
        """        
        dict_list: list = []
        for command in list_of_commands:
            command_to_dict = self.create_cmd_argumens_from_text(command)
            dict_list.append(command_to_dict)
        return dict_list


    # ------PROTOCOL DISPLAY SECTION----------

    def display_protocol_commands(self):
        """this function prints to the screen the command contents of a list. 
        """        
        for line in self.contents:
            if 'myProtocol.' in line:
                print(line.strip("'myProtocol"))
        pass

    def display_protocol_comments(self):
        """This function prints to the screen the comments of a protocol
        """        
        for line in self.contents:
            if line[0] == '#':
                print(line)

# ------FUNCTION TESTS SECTION----------

def tets_creation_of_file():
    creator = ProtocolCreator()

    cmd_1 = "myProtocol.aspirate_from(volume = 10, source = custom('A1'))"
    cmd_2 = "myProtocol.aspirate_from(volume = 5000, source = corning_384('A2'))"
    cmd_3 = "myProtocol.set_block_temp(4, 0)"
    cmd_4 = "myProtocol.close_lid()"
    cmd_5 = "myProtocol.set_lid_temp(39)"
    cmd_6 = "myProtocol.set_block_temp(37, 15)"
    cmd_7 = "myProtocol.deactivate_lid()"
    cmd_8 = "myProtocol.aspirate_from(volume = 10, source = micropots_3('A1'))"
    cmd_9 = "myProtocol.aspirate_from(volume = 5000, source = custom_small('A2'))"
    list_of_commands = [cmd_1, cmd_2, cmd_3, cmd_4, cmd_5, cmd_6, cmd_7, cmd_8, cmd_9]

    name_of_file = "Testing_matching"
    author = 'Alejandro Brozalez'
    description = 'I am testing how this protocol creator works.'
    labware = "Fluorescein_test.json"
    plates_to_void_depth = ['custom']
    waste = "custom('A1')"
    wash = "custom('A2')"
    clean = "custom('A3')"

    # CREATE A PROTOCOL WITH ALL PARAMETERS SPECIFIED 
    if True:
        name_of_file = creator.create_protocol_file(labware_name=labware, 
                                                    list_of_commands=list_of_commands, 
                                                    voided_plates=plates_to_void_depth,
                                                    author=author,
                                                    description=description,
                                                    waste_water_well=waste,
                                                    wash_water_well=wash,
                                                    clean_water_well=clean,
                                                    filename=name_of_file)

    # CREATE A PROTOCOL WITHOUT WASHING SETUP
    if False:
        name_of_file = creator.create_protocol_file(labware_name=labware, 
                                                    list_of_commands=list_of_commands, 
                                                    voided_plates=plates_to_void_depth,
                                                    author=author,
                                                    description=description,
                                                    filename=name_of_file)

    if False:
        name_of_file = creator.create_protocol_file()

    if False:
        name_of_file = creator.create_protocol_file(list_of_commands=list_of_commands, 
                                                    voided_plates=plates_to_void_depth,
                                                    author=author,
                                                    description=description,
                                                    filename=name_of_file)



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
    name = "protocol_5.py"
    location = "custom('A2')"
    new_list = creator.create_list_of_commands()
    cmd = creator.create_command_txt(filename= name, cmd=DISPENSE_CMD, volume=10, location=location)
    creator.add_command_to_end_of_list(cmd, new_list)
    creator.add_list_of_commands_to_protocol_file(name, new_list)
    location = "custom('A4')"
    cmd = creator.create_command_txt(filename= name, cmd=DISPENSE_CMD, volume=10, location=location)
    creator.reset_file_commands(name)
    creator.add_command_to_end_of_list(cmd, new_list)
    creator.add_list_of_commands_to_protocol_file(name, new_list)
    # creator.delete_existing_protocol(name)
    # creator.reset_file_commands(name)

def tests_voiding_depth_of_plates():
    creator = ProtocolCreator()
    labware = "Fluorescein_test.json"
    cmd = "myProtocol.aspirate_from(volume = 50, source = custom('A1'))"
    cmd2 = "myProtocol.aspirate_from(volume = 50, source = corning_384('A2'))"
    cmd_3 = "myProtocol.set_block_temp(4, 0)"
    cmd_4 = "myProtocol.close_lid()"
    cmd_5 = "myProtocol.set_lid_temp(39)"
    cmd_6 = "myProtocol.set_block_temp(37, 15)"
    cmd_7 = "myProtocol.deactivate_lid()"
    plates_to_void_depth = ['custom', 'corning_384']
    list_of_commands = [cmd, cmd2, cmd_3, cmd_4, cmd_5, cmd_6, cmd_7]
    # creator.create_protocol_file(labware_name=labware, voided_plates=plates_to_void_depth, list_of_commands=list_of_commands)
    creator.create_protocol_file(labware_name=labware, list_of_commands=list_of_commands)

def tests_csv():
    creator = ProtocolCreator()
    labware = "Fluorescein_test.json"
    csv_name = "test_protocol.csv"
    # protocol_name = creator.create_protocol_file(labware)
    # cmd_list = creator.convert_csv_to_cmd_list(csv_name)
    # creator.add_list_of_commands_to_protocol_file(protocol_name, cmd_list)
    cmd = "myProtocol.aspirate_from(volume = 50, source = custom('A1'))"
    cmd2 = "myProtocol.aspirate_from(volume = 50, source = corning_384('A2'))"
    cmd_3 = "myProtocol.set_block_temp(4, 0)"
    cmd_4 = "myProtocol.close_lid()"
    cmd_5 = "myProtocol.set_lid_temp(39)"
    cmd_6 = "myProtocol.set_block_temp(37, 15)"
    cmd_7 = "myProtocol.deactivate_lid()"
    # # print(cmd)
    # cmd_dictionary = creator.create_cmd_argumens_from_text(cmd)
    # print(cmd_dictionary)
    # cmd2_dictionary = creator.create_cmd_argumens_from_text(cmd2)
    # print(cmd2_dictionary)
    # creator.convert_cmd_dict_to_csv(cmd_dictionary)
    # creator.convert_cmd_dict_to_csv(cmd2_dictionary)

    
    # creator.create_protocol_voided_depth_for_labware(labware, plates_to_void_depth)
    # creator.convert_cmd_list_to_csv(list_of_commands)
    
def tests_matching_of_labware_with_commands():
    creator = ProtocolCreator()
    cmd_1 = "myProtocol.aspirate_from(volume = 10, source = custom('A1'))"
    cmd_2 = "myProtocol.aspirate_from(volume = 5000, source = corning_384('A2'))"
    cmd_3 = "myProtocol.set_block_temp(4, 0)"
    cmd_4 = "myProtocol.close_lid()"
    cmd_5 = "myProtocol.set_lid_temp(39)"
    cmd_6 = "myProtocol.set_block_temp(37, 15)"
    cmd_7 = "myProtocol.deactivate_lid()"
    cmd_8 = "myProtocol.aspirate_from(volume = 10, source = micropots_3('A1'))"
    list_of_commands = [cmd_1, cmd_2, cmd_3, cmd_4, cmd_5, cmd_6, cmd_7, cmd_8]
    plates_names = ['custom', 'corning_384']
    chips_name = ['micropots_3']
    print(creator.check_that_commands_match_labware(list_of_commands=list_of_commands, chips=chips_name, plates=plates_names))

def test():
    tets_creation_of_file()
    # tests_adding_lists_of_commands()
    # tests_adding_a_command_to_the_end_of_file()
    # tests_handling_commands()
    # tests_voiding_depth_of_plates()
    # tests_csv()
    # tests_matching_of_labware_with_commands()

if __name__ == "__main__":
    test()
