import threading
import time
import sys
import csv
import logging
import json
import pandas #reading csv files
import pathlib #?

from nicknames import Nicknames
from stopIndicator import StopIndicator
from scriptTimingValues import ScriptTimingValues

#code for testing

'''
class Coordinator: # pseudo class that represents the coordinator
    def __init__(self):
        pass
    def move(self, location, nicknames): # takes string for location to move to
        if location == "mySample":
            logging.info(f"Moving to '{location}' at '{nicknames.mySample}'")
        else:
            logging.info(f"Moving to '{location}' at '{nicknames.get_nickname_location(location)}'")
    def movexyz(self, location, cow, nicknames): # takes string for location to move to
        logging.info(f"Moving to '{location}' '{cow}' at '{location}'")
    
    def aspirate(self, amount, speed): # pick up amount in nL and speed in nL/s
        logging.info(f"Aspirating {amount} nL at speed {speed} nL/s")
    
    def dispense(self, amount, speed): # drop of amount in nL and speed in nL/s
        logging.info(f"Dispensing {amount} nL at speed {speed} nL/s")
    def start_timer(self, seconds, name): # makes a time and a name and makes a timer from the timer class
        logging.info(f"Making timer called '{name}' that lasts for {seconds} seconds")
    
    def wait_timer(self, name): # waits for a specific timer to finish
        logging.info(f"Waiting timer called '{name}' to finish")

    def wait(self, seconds): # pauses system for a number of seconds
        logging.info(f"Wait for {seconds} seconds")
        time.sleep(seconds)

    def toggle_valve(self): # toggles the valve, no parameters
        logging.info(f"Toggled Valve")

    def MS_contact_closure(self):
        logging.info(f"MS_contact_closure")

    def toggle_high_voltage_switch(self):
        logging.info(f"toggle_high_voltage_switch")

    def LC_contact_closure(self):
        logging.info(f"LC_contact_closure")

'''

class HighLevelScriptReader:  # should call read from coordinator file
    def __init__(self, myCoordinator): # init all variables and store needed data
        """
        Initialize all variables
        Args:
            myCoordinator ([type]): [description]
        """
        # you may need to also pass in a coordinator object to access the function names
        self.myCoordinator = myCoordinator # this has the functions that move the motors
        self.wellList = []    # will hold all of the wells
        self.scriptList = []  # holds all their corresponding scripts
        self.batchName = "" # stores name of the batch
        self.get_excel_data() # loads data into the lists
        
        self.currentGradientTime = 0
        self.nextGradientTime = 0
        self.scriptIndex = 0 # this lets you know what number sample you are on. 
        self.percentComplete = 0 # stores the percent complete to display in the GUI
        self.secondsTillComplete = 0 # stores approximate number of seconds it will take to complete batch
        self.nicknames = Nicknames() # create nickname object. Holds locations of waste and buffers. Also stores location of mySample
        self.batchCompletionDate = 0 # holds date for when the batch will be finished
        self.myStopIndicator = StopIndicator() # holds values for stop values
        self.currentWell = "n/a"


        self.emptyTimingValues = ScriptTimingValues(0, 0, 0, 0) # make object with zero values to fill array at start
        self.previousTimingValues = [self.emptyTimingValues]#[emptyTimingValues, emptyTimingValues, emptyTimingValues] # holds the current, previous, and 2nd previous samples timing value objects 
        # *note: gradient^-1 indicates the gradient time from the previous sample. SPE^-2 would be the SPE time from two samples ago

        format = "%(asctime)s: %(message)s" #format logging
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")

    def get_excel_data(self):  # saves batch data into two lists: wellList, ScriptList
        pathToBatch = "batches/batch.csv"
        batchFile = pathlib.Path(pathToBatch)
        if batchFile.exists ():
            batchFail = True
        else:
            batchFail = False
 
        while batchFail == False:
            self.batchName = input("Invalid batch. Try again: ")
            pathToBatch = "batches/" + self.batchName + ".csv"
            batchFile = pathlib.Path(pathToBatch)
            if batchFile.exists ():
                batchFail = True
            else:
                batchFail = False

        # -----Get list from CSV batch.csv with Pandas. This is used for the RPi because the RPi doesn't have excel-----
        
        col_list = ['Locations', 'Scripts']
        df = pandas.read_csv(pathToBatch, usecols=col_list)
        self.wellList = list(df['Locations'])
        self.scriptList = df['Scripts']
                
        '''
        # -----Get list from excel batch.xlsx. This is used on my Mac becuase pandas gives me Numpy errors----
        loc = ('batch.xlsx')  # save location of batch file
        wb = xlrd.open_workbook(loc)  # open Workbook
        sheet = wb.sheet_by_index(0)  # open Workbook
        
        # Get first column----------------    
        for i in range(sheet.nrows-1):  # loops for first column except first row
            # check to make sure there are no empty cells
            # i+1 starts with second row (first row is a lable)
            if sheet.cell_value(i+1, 0) == "":
                print("ERROR: wellList is has empty cell in list. Check batch.xlcx row", i+2)
                sys.exit()
            self.wellList.append(sheet.cell_value(i+1, 0))  # adds well to list
        # print(self.wellList)
        
        # Get Second column----------------
        for i in range(sheet.nrows-1):  # loops for second column except first row
            # check to make sure there are no empty cells
            # i+1 starts with second row (first row is a lable)
            if sheet.cell_value(i+1, 1) == "":
                print("ERROR: ScriptList is has empty cell in list. Check batch.xlcx row", i+2)
                sys.exit()
            self.scriptList.append(sheet.cell_value(i+1, 1))  # adds well to list
        # If one list is longer, the code thinks that the smaller on is missing data and throws
        # an error. The error check handles errors for missing data. Does not check if data is valid.
        '''
        
    def set_timing_values(self, script): # sets the values for MStime, LCtime, gradientTime, SPEtime, prevMStime, prevGradientTime

        # set new values from JSON script file
        path_to_script = "../scripts/" + script # moves to script folder
        with open(path_to_script, 'r') as myfile: # open file
            data = myfile.read()
        # parse file
        obj = json.loads(data)

        MStime, LCtime, gradientTime = self.get_script_times(script)
        

        # store current values
        
    def verify_wells(self):  # checks all the wells in CSV to make sure they all exist
        print("Verifying Wells...")

        for well in self.wellList:
            well_exists = self.myCoordinator.verify_container_existence(well)
            if not well_exists:
                print(f"ERROR: {well} does not exist. Verify that the batch file contains only existing wells", "\n")
                return False

        print("SUCCESS!", "\n")
        return True

    def verify_json(self):   # checks all the json files in CSV to make sure they all exist
        print("Verifying Script files...")

        for script in self.scriptList: # open and close each json file, if one is missing it will throw error
            path_to_file = "../scripts/" + script # get path to script
            file = ""
            try:
                file = open(path_to_file)
            except:
                print(f"Script {script} not found on the record")
                return False
            else:
                file.close()
        
        print("SUCCESS!", "\n")
        return True

    def convert_sec_to_day(self, n): # takes in time in seconds and converts to day, hour, minute, second
        """
        Args:
            n ([int]): [number of seconds to complete a batch]
        """
        days = int(n / (24 * 3600))  # calculate days
  
        n = n % (24 * 3600)
        hours = int(n / 3600) # calculate hours
  
        n %= 3600
        minutes = int(n / 60) # calculate minutes
  
        n %= 60
        seconds = int(n)#calculate seconds
         
        # log this info 
        logging.info("\"%s\" estimated completion in: %s d %s h %s m %s s", self.batchName, days, hours, minutes, seconds)

    def estimate_end_time(self): # calculates how long the script will take to complete
        
        # add the first gradient time (thread) and all gradients from batch scripts
        # add first gradient to this. (About 35 minutes for dry or QCtime for wet)
        self.secondsTillComplete += self.currentGradientTime *3

        firstFile = True

        for script in self.scriptList: # for all the scripts in batch
            path_to_script = "../scripts/" + script # moves to script folder
            with open(path_to_script, 'r') as myfile: # open file
                data = myfile.read()
            # parse file
            obj = json.loads(data)

            # add up all gradient times from each script to see how long it will take
            self.secondsTillComplete += (obj['gradientTime']) # note that this is in seconds
            if firstFile:
                self.secondsTillComplete += obj['gradientTime']*2 #because the extra ones at the end
                firstFile = False #updates variable

        self.batchCompletionDate = time.asctime( time.localtime(time.time() + self.secondsTillComplete))
        logging.info("\"%s\" estimated completion on: %s", self.batchName, self.batchCompletionDate)

        self.convert_sec_to_day(self.secondsTillComplete) # prints message for when it will be done
        if input("          Is this okay? (y/n): ") == "n":
            sys.exit()

    def get_script_times(self, script): # takes a script and returns its timing values
        """
        Args:
            script ([str]): [the name of the script used to prepare the sample at the well location. e.g., "qc.json"]

        Returns:
            MStime [int]: [time from start of loop time to turn on MS] 
            LCtime  [int]: [time from end of loop time to turn on MS] 
            gradientTime [int]: [this generally become the total loop time]
        """
        path_to_script = "../scripts/" + script # moves to script folder
        with open(path_to_script, 'r') as myfile: # open file
            data = myfile.read()
        # parse file
        obj = json.loads(data)

        # store current values
        LCtime = (obj['LCtime']) # time before the end that you should trigger the LC
        MStime = (obj['MStime'])  # time when you should turn on the MS
        gradientTime = (obj['gradientTime']) # total time for gradientThread
        SPEtime = (obj['SPEtime']) # time to load sample from collection tube into the SPE

        timing_val_object = ScriptTimingValues(LCtime, MStime, gradientTime, SPEtime) # make a timing object for the script
        self.previousTimingValues.insert(0, timing_val_object) # push the current to the front of the list

        return MStime, LCtime, gradientTime

    def hard_stop(self): # stops batch entirely, stops loading and the rest of the LC and MS calls
        self.myStopIndicator.turn_on_hardStop()

    def stop_load(self): # stops batch after loading current sample. Loaded samples still go to the MS
        self.myStopIndicator.turn_on_stopLoad()

    # NOT IMPLEMENTED AT THE MOMENT. need to add batch queueing first
    def pause_batch(self): # this pauses the batch so you can add scripts to the queue (stops you from runnning the finishup routine and starting over. saves maybe 3 hours)
        pass

    def setup(self, script):  # check excel file to make sure its format is valid, sets first gradient, estimate end time
        """
        Args:
            script ([str]): [the name of the script used to prepare the sample at the well location. e.g., "qc.json"]
        """
        # check all cells make sure none are empty
        # make sure size of each array is same
        if ( ( not self.verify_wells() ) or ( not self.verify_json() ) ):
            print ("VERIFICATION FAILED. CANNOT RUN THE PROVIDED BATCH")
            return False
        
        else:
            # print out estimated completion time ask for approval
            self.estimate_end_time()
            self.scriptIndex = 0 # used to track the index of the wellList to get corresponding script. reset for every batch
            self.myStopIndicator.reset() # reset the stop indicators back to false for every batch
            return True

    def shoot_sample_thread(self, well): # controls timing of "shooting" the samples into the MS
        """        
        # this taks times from set_timing_values and converts them into wait times in the total gradient time (~35 minutes)
        # ex: start -> wait 9 min -> turn on MS -> wait 16 min -> turn on LC -> wait 10 min -> end loop 
        
        Args:
            well ([str]): [holds the location of the sample we want to load. e.g., 'P1c4']
            firstLoad ([bool]): [true on first load. Says not to do the MS on this loop]
            lastLoad ([bool]): [true on last load. Says not to start LC this loop]
        """
        # this taks times from set_timing_values and converts them into wait times in the total gradient time (~35 minutes)
        # ex: start -> wait 9 min -> turn on MS -> wait 16 min -> turn on LC -> wait 10 min -> end loop 
        
        '''totalTime = self.prevGradientTime
        turnOnMS = self.prevMStime
        turnOnLC = totalTime - turnOnMS - self.LCtime
        endLoop = self.LCtime'''

        # Total time of the current run, and total time of the nextRun. 
        totalTimeCurrent = max(self.previousTimingValues[2].Gradient_time, self.previousTimingValues[1].SPE_time)
        totalTimeNext = max(self.previousTimingValues[1].Gradient_time, self.previousTimingValues[0].SPE_time)
        
        #
        turnOnLC = totalTimeCurrent + totalTimeNext - self.previousTimingValues[2].LC_time #the current sample is third in the stored values
        switchValve = totalTimeCurrent + totalTimeNext
        turnOnMS = self.previousTimingValues[2].MS_time #the current sample is third in the stored values
        
        logging.info("THREAD: Gradient Thread '%s': Started", well)

        if (turnOnLC < 0):
            print("******************************************ERROR*********************************************")
        endLoop = self.previousTimingValues[2].LC_time
     
        time.sleep(turnOnLC) #wait to turn on the LC        
        # self.myCoordinator.LC_contact_closure()
        time.sleep(endLoop) # wait until valve cycle should end. This is the time it takes for the LC pump to finish
        # Actuator toggled elsewhere
        time.sleep(turnOnMS)
        # self.myCoordinator.MS_contact_closure()
        # self.myCoordinator.toggle_high_voltage_switch()
        logging.info("THREAD: Gradient Thread '%s': Complete!", well)

    def shoot_valve_thread(self, well):
        totalTimeCurrent = max(self.previousTimingValues[2].Gradient_time, self.previousTimingValues[1].SPE_time)
        time.sleep(totalTimeCurrent)
        # self.myCoordinator.toggle_valve()

    def load_sample(self, well, scriptName):  # reads and calls commands from script to load next sample
        """
        Args:
            well ([str]): [holds the location of the sample we want to load. e.g., 'P1c4']
            scriptName ([str]): [the name of the script used to prepare the sample at the well location. e.g., "qc.json"]
        """
        
        # print message stating that a script has begun
        logging.info("Loading sample %s '%s' with '%s': Started", self.scriptIndex, well, scriptName)
        
        # read file
        path_to_script = "../scripts/" + scriptName # moves to script folder
        with open(path_to_script, 'r') as myfile:
            data = myfile.read()

        # parse file
        obj = json.loads(data)

        # print name and drscription from top of JSON script file
        logging.info("Name: %s", str(obj['name'])) # Print name of script
        logging.info("Description: %s", str(obj['description'])) # Print script description

        #loop for all commands in json script
        for command in obj['commands']:
            # check to see if we should stop loading
            if self.myStopIndicator.hardStop == True:
                break # if hardStop then we break to loop and stop loading

            # save command parameters in a list
            params = command['parameters']

            # for just move add nickname to parameter list
            if command['type'] == "move":
                params.append(self.nicknames)

            # use getattr to call the correct function in coordinator
            # unpack the parameters list with (*params)
            # if params is empty list it passes nothing
            #coordinator = Coordinator()
            getattr(self.myCoordinator, command['type'])(*params)

            # wait 1 second to make testing feel more real
            #if command['type'] != 'wait':
            #    time.sleep(5) #this is for testing and can be removed

        # print that the sample is done being loaded
        logging.info("Loading Sample '%s': Complete!", well)

    def finish_run(self, well):
        valveThread = threading.Thread(target = self.shoot_valve_thread, args=(well,))
        valveThread.start()

    def run(self):
        """    
        # This is the main function for the reader. It handles all the looping and the program
        # should stay in this function for the entire time it is running (numWells * ~35mins = time spent in run).
        # This handles making the timing threads for the Gradient and calls all the necessry functions
        # from the coordinator to do so. 
        #
        # - Load sample into the valve (<35 minutes)
        # - Send that sample to the MS (~35 minutes)
        #
        # First  loop loads first sample
        # Second loop send first sample to MS and loads second sample
        # After last loop loads last sample, Send last sample to MS

        Returns:
            [bool]: [returns true when run is complete, this is not used anywhere at the moment]
        """
        print("") #Add line to make output easier to read
        if (self.setup(self.scriptList[self.scriptIndex]) ): # setup the all needed data, error check batch
            
            self.set_timing_values(self.scriptList[self.scriptIndex]) #gets the values for the current run
            self.set_timing_values(self.scriptList[self.scriptIndex+1]) #gets the values for the next run
            
            lastWell = ""
            #loop for all wells. this may also include vials for QC loading
            for well in self.wellList:
                '''for value in self.previousTimingValues:
                    print(value.Gradient_time)
                    print(value.SPE_time)
                    print(value.MS_time)
                    print(value.LC_time)
                    print("-")'''

                print("\n")
                # set the timing values for the first loop
                if (self.scriptIndex + 2 < len(self.scriptList)):
                    self.set_timing_values(self.scriptList[self.scriptIndex+2]) #gets the values for the run after next
                else:
                    self.set_timing_values(self.scriptList[self.scriptIndex]) #comparing the current one with itself at the end will be fine


                # set the location of 'mySample' to well for each loop
                self.nicknames.mySample = well

                #make gradient threads
                gradientThread = threading.Thread(target = self.shoot_sample_thread, args=(well,))
                gradientThread.start()
                valveThread = threading.Thread(target = self.shoot_valve_thread, args=(well,))
                valveThread.start()

                # load next sample while thread is running--------------------------------------------------
                self.load_sample(well, self.scriptList[self.scriptIndex]) # load next sample with appropirate script

                # make sure loading next sample is faster than gradient thread--------------------------------------------------

                # Update variables--------------------------------------------------
                self.convert_sec_to_day(self.secondsTillComplete) # print time until complete
                self.percentComplete = round(((self.scriptIndex + 1 )/ len(self.scriptList)) * 100) # update percent complete. round for clean output
                # 0% complete until the first sample is all the way done (i.e 2 loops)
                logging.info(f"Sample {str(self.scriptIndex+1)} of {str(len(self.scriptList))} complete: {str(self.percentComplete)}%") # print percent complete
                self.scriptIndex += 1 # next well may have a different script than the one we just did
                
                print("----------------------------------------------------------") # add white space for output readibility
                while valveThread.is_alive(): #wait here until the previous sample is done being sent to MS
                    pass                         #when this is done toggle valve and start next loop

                lastWell = well

                if self.myStopIndicator.stopLoad or self.myStopIndicator.hardStop == True:
                    print("No more samples will be loaded. Either stopLoad or hardStop was called")
                    break # stop loading more samples if either is set to true

                
            self.scriptIndex = 0 #reset the script index for the next batch

            if self.myStopIndicator.hardStop == True:
                print("hardStop Called. All function calls have stopped. Finish up routine Skipped")
                success = False # return false
            else:
                print("stopLoad Called. Finish up routine will be executed and then program will end")
                success = True
            self.finish_run(lastWell)
            
            return success
        
        else:
            return print("SETUP FAILED. CANNOT RUN THE PROVIDED BATCH")



'''
# comment in or out the following 3 lines to test just this file. 
# You will have to Comment in the psudo coordinator class at the top of this file
Coordinator = Coordinator()
myReader = HighLevelScriptReader(Coordinator)
myReader.run()

'''