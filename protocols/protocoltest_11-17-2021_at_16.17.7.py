"""
    Instructions: 
        This protocol has been created with the class protocol_creator.
        If this file is edited it must need to be renamed modifiying the date of edition.        
"""
import sys 

try:
    from api import *
except ImportError:
    sys.path.append(sys.path[0] + '\\..') # current directory
    from api import *

myProtocol = Api() # creates a protocol object using the Api

metadata = {
	'protocolName': 'protocoltest_11-17-2021_at_16.17.7.py', 
	'author': 'ALEJANDRO', 
	'description': 'Missing information' 
}

# WARNING: Not able to set labware

# WARNING: Dispensing and aspirating from bottom of ALL plates.

# -----------PREPROTOCOL SETUP-------------------

# WARNING: Not able to retrieve labware location

# WARNING: No washing configurations have been set. 

# ------------START OF PROTOCOL---------------------------------

# WARNING: No commands were given.

#--------------END OF PROTOCOL--------------

myProtocol.end_of_protocol()