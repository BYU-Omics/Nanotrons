import json

"""
This class holds two main things:
1.) the location of 'mySample' this changes every loop and is the well location being worked on
2.) a list from nicknames.json of the vials names and their locations. (e.g., Buffer : P 1c3)
This allows for the person writing the script to say move to 'buffer' or 'waste' instead of
having to know the locations of the each vial in the plate. Additionally, if you want to move
a vial you just have to change the nicknames.json file and not the script, which will probably
not change much since most scripts will always be the same. (QC or wet scripts)
"""
class Nicknames():
    def __init__(self):
        self.mySample = "" # this will hold to location of each sample for each loop
        self.nicknames = self.get_nicknames() # store all the locations from nicknames.json
        pass

    def get_nicknames(self): # this returns the dictionary from nicknames.json
        # read file
        with open("nicknames.json", 'r') as myfile:
            data = myfile.read()
        # parse file
        obj = json.loads(data)
        return obj

    def get_nickname_location(self, nickname):
        return self.nicknames['name'][nickname]

#myNicknames = Nicknames()
#print(myNicknames.nicknames)
#print(myNicknames.get_nickname_location("buffer"))