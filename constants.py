RUNNING_APP_FOR_REAL = True
THERMOCYCLER_CONNECTED = False
TEMPDECK_CONNECTED = False
CONTROLLER_CONNECTED = True

WINDOWS_SERIAL_PORT_OT2 = "COM4"  # This is the com port generally used by the motors on Windows, but it could be a different number
LINUX_SERIAL_PORT_OT2 = "/dev/ttyUSB0"  # This is the com port used by the motors on Linux-based operating systems (including Raspberry OS)
WINDOWS_SERIAL_PORT_TC = "COM5"
LINUX_SERIAL_PORT_TC = "/dev/ttyACM0"
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
UNIT_CONVERSION  = 4.23 #3.8896 4.16
CALIBRATION_POINTS = 3
INBETWEEN_LIFT_DISTANCE = -10 # Default distance the syringe will be lifted/lowered when going from one nanopots well\reagent pot to another
LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LABWARE_SYRINGE = "s"
DEFAULT_PROFILE = "default_profile.json"
FROM_NANOLITERS = 0.001
REFRESH_COORDINATE_INTERVAL = 0.1
ASPIRATE_SPEED = 15
LABWARE_COMPONENT_CHIP = 'c'
LABWARE_COMPONENT_PLATE = 'p'
COMPONENT_MODEL_CHIP = 'MICROPOTS_3'
COMPONENT_MODEL_CORNING = 'CORNING_384'
COMPONENT_MODEL_CUSTOM = 'CUSTOM'
COMPONENT_MODEL_CUSTOM_SM = 'CUSTOM_SMALL'
POSITION_IN_Z_TO_PLACE_WHEN_GOING_TO_SLOT = 150
TIME_TO_SETTLE = 0.5 #SECONDS


RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = '/protocols/'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

CALIBRATION_POINTS = 3
SMALL_WELL = "S"
BIG_WELL = "B"

ROW_LENGTH = 3
FIXED_TRASH_ID = 'fixedTrash'

RELATIVE_PATH_L = "OT2/saved_labware"
RELATIVE_PATH_W = "saved_labware"
LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
JSON_EXTENTION = '.json'

LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LABWARE_SYRINGE = "s"

RELATIVE_PATH_TO_CHIPS_W = "models\\chips"
RELATIVE_PATH_TO_PLATES_W = "models\\plates"
RELATIVE_PATH_TO_SYRINGES_W = "models\\syringes"

RELATIVE_PATH_TO_CHIPS_R = "models/chips"
RELATIVE_PATH_TO_PLATES_R = "models/plates"
RELATIVE_PATH_TO_SYRINGES_R = "models/syringes"

# OT_DRIVER

X_MAX= 418
X_MIN= 25
Y_MAX= 340
Y_MIN= 5
Z_MAX= 170.15
Z_MIN= 10 
A_MAX= 170.15
A_MIN= 10 
B_MAX= 18
B_MIN= -1*154 
C_MAX= 18
C_MIN= -1*154 
TC_X = 211
TC_Y = 155
TC_Z_OPEN_LID = 170
TC_Z_CLOSED_LID = 170
BC_AXIS_UNIT_CONVERTION = 4.16
STEP_SIZE = 10
S_STEP_SIZE = 10

SHORT_MEDIUM_STEP_LIMIT = 10
MEDIUM_LONG_STEP_LIMIT = 50
MAX_STEPING_SIZE = 160
MIN_STEPING_SIZE = 0.02

SPEED = 300
STEP_SPEED = 100
SLOW_SPEED = 15
MOVE_TO_SPEED = 70
MEDIUM_SPEED = 100

X_MAX_SPEED = 600
Y_MAX_SPEED = 400
Z_MAX_SPEED = 125
A_MAX_SPEED = 125
B_MAX_SPEED = 40
C_MAX_SPEED = 40

HIGH_SPEED = 300
MAX_SPEED = 400

MIDDLE_STEP = 5
HALF = 0.5
XYZ = 'X Y Z'

LEFT = 'Left' #X
RIGHT = 'Right' #B

WINDOWS_OT_PORT = 'COM4'
LINUX_OT_PORT = '/dev/ttyACM0'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

# RELATIVE_PATH_TO_PROTOCOLS_W = ''
RELATIVE_PATH_TO_PROTOCOLS_W = '.\\protocols\\' # ./ means look within the current directory
RELATIVE_PATH_TO_PROTOCOLS_L = '/protocols/'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

LID_TARGET_DEFAULT = 105.0    # Degree celsius (floats)
LID_TARGET_MIN = 37.0
LID_TARGET_MAX = 110.0
BLOCK_TARGET_MIN = 0.0
BLOCK_TARGET_MAX = 99.0
TEMP_UPDATE_RETRIES = 50
TEMP_BUFFER_MAX_LEN = 10


ERROR_KEYWORD = 'error'
ALARM_KEYWORD = 'alarm'

DEFAULT_TEMP_DECK_TIMEOUT = 1

DEFAULT_STABILIZE_DELAY = 0.1
DEFAULT_COMMAND_RETRIES = 3


TEMP_DECK_BAUDRATE = 115200

TEMP_DECK_COMMAND_TERMINATOR = '\r\n\r\n'
TEMP_DECK_ACK = 'ok\r\nok\r\n'

ALLOWED_EXTENSIONS = ['json']
LABWARE_CHIP = "c"
LABWARE_PLATE = "p"
LABWARE_SYRINGE = "s"
CAMERA_PORT = 0
PIPPETE_CAMERA_PORT = 1
RELATIVE_PATH_TO_PROTOCOLS_W = 'protocols\\'
RELATIVE_PATH_TO_PROTOCOLS_L = 'protocols/'
RELATIVE_PATH_TO_LABWARE_W = 'saved_labware\\'
RELATIVE_PATH_TO_LABWARE_L = 'saved_labware/'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
TEMP = 0
HOLD_TIME = 1
X, Y, Z = 0, 1 ,2
NUMBER_OF_CALIBRATION_POINTS = 3
FOURTH_CALIBRATION_POINT_POSITION = 3
LABWARE_COMPONENT_INDEX = 0 # 'c' or 'p'
COMPONENT_MODEL_INDEX = 1
SETTING_NAME_INDEX = 0
NEW_VALUE_INDEX = 1