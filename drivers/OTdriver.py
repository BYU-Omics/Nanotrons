"""
Description of the program:

    This code contains a child class that is used to control the robot by single step movements. 
    The parent class is the driver that Opentrons have created to send commands to the OT2 
    
    In order to move a single axis an amount of units, we pass in the unit we want to use and the 
    amount we want the tobot to move every step. There is a function on SmoothieDriver_3_0_0 class 
    that returns the position as a dicctionary in the following format: 

        { 'X': 150, 'Y': 150, 'Z': 170.15, 'A': 218.0, 'B': 0.0, 'C': 0.0}
volume
    The move on a single axis happens by using the method SmoothieDriver_3_0_0.move() wich moves to a 
    specified coordinate, but in this case we only change the coordinate that we need keeping the rest
    the same. 

"""
from opentrons.drivers.smoothie_drivers.driver_3_0 import SmoothieDriver_3_0_0 as SM, SmoothieError
from opentrons.config.robot_configs import build_config
from serial.tools import list_ports
import os
from constants import RUNNING_APP_FOR_REAL

X_MAX= 418
X_MIN= 25
Y_MAX= 340
Y_MIN= 5
Z_MAX= 170.15
Z_MIN= 10 
A_MAX= 170.15
A_MIN= 10 
B_MAX= 0
B_MIN= -1*190 # TO-DO: change thee limit according to the syringe we are sugin. note for self. 
C_MAX= 0
C_MIN= -1*190 
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
MAX_SPEED = 130

MIDDLE_STEP = 7
HALF = 0.5
XYZ = 'X Y Z'

LEFT = 'Left' #X
RIGHT = 'Right' #B

WINDOWS_OT_PORT = 'COM4'
WINDOWS_OT_SER = 'A50285BIA'
LINUX_OT_PORT = '/dev/ttyACM0'
MACBOOK_OT_PORT = "/dev/cu.usbserial-A50285BI"
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'

list_of_sizes = [0.015, 0.05, 0.1, 0.5, 1, 4.5, 9, 13, 30, 51.5, 63, 67.5, 69.5, 103.5]

class OT2_nanotrons_driver(SM):
    def __init__(self):#, port):
        super().__init__(config=build_config({}))

        # Atributes that control the size and speed of the X Y and Z axis. 
        #   When changed, all of them move at the same rate
        self.xyz_step_size = STEP_SIZE
        self.xyz_step_speed = STEP_SPEED
        self._port = None
        # Attributes that control the size and speed of the plunger. 
        self.s_step_size = list_of_sizes[MIDDLE_STEP] #Step size for the syringe
        self.s_step_speed = SLOW_SPEED #Step speed for the syringe

        self.nL = 0 #nanoliters that the syringe is currently working with
        self.side = LEFT 
        self.flag = True
        self.i = MIDDLE_STEP
        self.tc_flag = True
        self.tc_lid_flag = 'Open'
        if RUNNING_APP_FOR_REAL:
            self.connect_driver()
        else:
            print("Not connected to the OT port")

# Functions that help movements
        
    def check_for_valid_move(self, pos, axis, size) -> bool:
        # print(pos)
        """
        This function checks for limits. If the user tries to go too far, the move 
        will not be executed. Returns false if the move is outside the allowed limits
        """
        # if self.tc_flag == True:
        #     if (axis == 'X' and (pos < TC_X) and axis == 'Y' and (pos > TC_Y)):
        #     if axis == 'Z':
        #         if (self.tc_lid_flag == 'open' and pos < TC_Z_OPEN_LID):
        #             return False
        #         elif (self.tc_lid_flag == 'closed' and pos < TC_Z_CLOSED_LID):
        #             return False
        #     elif axis == 'A' and (pos > A_MAX or pos < A_MIN):
        #         return False

        # kind of works
        # print(self._position)
        # if self.tc_flag == True and ((self._position['X'] + size) < TC_X) and ((self._position['Y'] + size) > TC_Y) and ((self._position['Z'] + size) < TC_Z_OPEN_LID):
        #     return False

        if axis == 'X' and (pos > X_MAX or pos < X_MIN):
            return False
        elif axis == 'Y' and (pos > Y_MAX or pos < Y_MIN):
            return False
        elif axis == 'Z' and (pos > Z_MAX or pos < Z_MIN):
            return False
        elif axis == 'A' and (pos > A_MAX or pos < A_MIN):
            return False
        elif axis == 'B' and (pos > B_MAX or pos < B_MIN):
            return False
        elif axis == 'C' and (pos > C_MAX or pos < C_MIN):
            return False
        else:
            return True

    def check_speed(self, step_size):
        """
        This function sets a speed acording to the step size given.
        There are only 2 different speeds that are assigned: Slow, Medium and High
        """
        if step_size <= SHORT_MEDIUM_STEP_LIMIT:
            return SLOW_SPEED
        elif step_size <= MEDIUM_LONG_STEP_LIMIT:
            return MEDIUM_SPEED
        else:
            return HIGH_SPEED

    def double_step_size_XYZ(self, dummyarg):
        """"
        This function first checks for the current step
        size so that it does not go over the limit, and then it doubles it.
        """
        if self.i < (len(list_of_sizes) -1):
            self.i += 1
            self.xyz_step_size = list_of_sizes[self.i]
            print(f"Stepping {self.xyz_step_size}[mm]")
        else:
            print("Trying to move morethan allowed predefined steps")
            print(f"The stepping size is currently set to {self.xyz_step_size}")

    def half_step_size_XYZ(self, dummyarg):
        """"
        This function first checks for the current step
        size so that it does not go over the limit, and then it halves it.
        """
        if self.i > 0:
            self.i -= 1
            self.xyz_step_size = list_of_sizes[self.i]
            print(f"Stepping {self.xyz_step_size}[mm]")
        else:
            print("Trying to move morethan allowed predefined steps")
            print(f"The stepping size is currently set to {self.xyz_step_size}")

# Functions to move the different axis, X, Y, Z and sirenge:    

    def move_up(self, step_size = STEP_SIZE):  
        """
        This functions moves the pippetes by steps. 
        """
        y_pos = self._position['Y'] # stores the current position
        y_pos += step_size # adds a step size to the current position
        if(self.check_for_valid_move(y_pos, 'Y', step_size)): # if the future position is a valid move 
            self.move({'Y': y_pos}, speed= self.check_speed(step_size)) # move to the indicated position
        else:
            pass # if the move is not valid just dont move 

    def move_down(self, step_size = STEP_SIZE):
        y_pos = self._position['Y'] # stores the current position
        y_pos -= step_size # adds a step size to the current position
        if(self.check_for_valid_move(y_pos, 'Y', step_size*(-1))): # if the future position is a valid move 
            self.move({'Y': y_pos}, speed= self.check_speed(step_size)) # move to the indicated position
        else:
            pass # if the move is not valid just dont move 

    def move_left(self, step_size = STEP_SIZE):
        x_pos = self._position['X'] # stores the current position
        x_pos -= step_size # adds a step size to the current position
        if(self.check_for_valid_move(x_pos, 'X', step_size*(-1))): # if the future position is a valid move 
            self.move({'X': x_pos}, speed= self.check_speed(step_size)) # move to the indicated position
        else:
            pass

    def move_right(self, step_size = STEP_SIZE):
        x_pos = self._position['X'] # stores the current position
        x_pos += step_size # adds a step size to the current position
        if(self.check_for_valid_move(x_pos, 'X', step_size)): # if the future position is a valid move 
            self.move({'X': x_pos}, speed= self.check_speed(step_size)) # move to the indicated position
        else:
            pass

    def pipete_R_Down(self, step_size = STEP_SIZE):
        z_pos = self._position['A'] # stores the current position
        z_pos -= step_size # adds a step size to the current position
        if(self.check_for_valid_move(z_pos, 'A', step_size*(-1))): # if the future position is a valid move 
            self.move({'A': z_pos}, speed= self.check_speed(step_size)) # move to the indicated position
        else:
            pass

    def pipete_R_Up(self, size = STEP_SIZE):
        z_pos = self._position['A'] # stores the current position
        z_pos += size # adds a step size to the current position
        if(self.check_for_valid_move(z_pos, 'A', size)): # if the future position is a valid move 
            self.move({'A': z_pos}, speed= self.check_speed(size)) # move to the indicated position
        else:
            pass
    
    def pipete_L_Down(self, size = STEP_SIZE):
        z_pos = self._position['Z'] # stores the current position
        z_pos -= size # adds a step size to the current position
        if(self.check_for_valid_move(z_pos, 'Z', size*(-1)) ): # if the future position is a valid move 
            self.move({'Z': z_pos}, speed= self.check_speed(size)) # move to the indicated position
        else:
            pass

    def pipete_L_Up(self, size = STEP_SIZE):
        z_pos = self._position['Z'] # stores the current position
        z_pos += size # adds a step size to the current position
        if(self.check_for_valid_move(z_pos, 'Z', size) ): # if the future position is a valid move 
            self.move({'Z': z_pos}, speed= self.check_speed(size)) # move to the indicated position
        else:
            pass

    def plunger_L_Up(self, size: float = STEP_SIZE, speed = SLOW_SPEED):
        print(f"Size aspirating:{size}")
        # if self.flag == True:
        #     size = S_STEP_SIZE
        b_pos: float = self._position['B'] # stores the current position
        b_pos += size # adds a step size to the current position
        if(self.check_for_valid_move(b_pos, 'B', size)): # if the future position is a valid move 
            self.move({'B': b_pos}, speed= self.s_step_speed) # move to the indicated position

    def plunger_L_Down(self, size: float = STEP_SIZE, speed = SLOW_SPEED):
        print(f"Size aspirating:{size}")
        # if self.flag == True:
        #     size = S_STEP_SIZE
        b_pos: float = self._position['B'] # stores the current position
        b_pos -= size # adds a step size to the current position
        if(self.check_for_valid_move(b_pos, 'B', size*(-1))):
            self.move({'B': b_pos}, speed= self.s_step_speed) # move to the indicated position

    def plunger_R_Up(self, size: float = STEP_SIZE, speed = SLOW_SPEED):
        if self.flag == True:
            size = S_STEP_SIZE
        c_pos: float = self._position['C'] # stores the current position
        c_pos = c_pos + size # adds a step size to the current position
        if(self.check_for_valid_move(c_pos, 'B', size)): # if the future position is a valid move 
            self.move({'C': c_pos}, speed= self.s_step_speed) # move to the indicated position

    def plunger_R_Down(self, size: float = STEP_SIZE, speed = SLOW_SPEED):
        if self.flag == True:
            size = S_STEP_SIZE
        c_pos: float = self._position['C'] # stores the current position
        c_pos = c_pos - size # adds a step size to the current position
        if(self.check_for_valid_move(c_pos, 'B', size*(-1))): # if the future position is a valid move 
            self.move({'C': c_pos}, speed= self.s_step_speed) # move to the indicated position

## These functions are just as the ones without the _aut but the logic is a little
## different since they are used by coordinator/volume etc. The step size input in 
## this case comes with a negative sign if it goes down, so both have the same sign. 

    def plunger_L_Up_aut(self, size = STEP_SIZE, speed = SLOW_SPEED):
        b_pos = self._position['B']
        b_pos += size
        self.move({'B': b_pos}, speed= self.s_step_speed) # move to the indicated position

    def plunger_L_Down_aut(self, size = STEP_SIZE, speed = SLOW_SPEED):
        b_pos = self._position['B']
        b_pos += size
        self.move({'B': b_pos}, speed= self.s_step_speed) # move to the indicated position

    def plunger_R_Up_aut(self, size = STEP_SIZE, speed = SLOW_SPEED):
        c_pos = self._position['C']
        c_pos += size
        self.move({'C': c_pos}, speed= self.s_step_speed) # move to the indicated position

    def plunger_R_Down_aut(self, size = STEP_SIZE, speed = SLOW_SPEED):
        c_pos = self._position['C']
        c_pos += size
        self.move({'C': c_pos}, speed= self.s_step_speed) # move to the indicated position

# Getters and Setters 
    def get_side(self):
        return self.side;
        
    def get_x_motor_index(self):
        return 'X'

    def get_y_motor_index(self):
        return 'Y'

    def get_z_motor_index(self):
        return 'Z'

    def get_syringe_motor_index(self):
        return 'S'

    def get_step_size_xyz_motor(self):
        return (self.xyz_step_size)

    def get_step_size_syringe_motor(self):
        return self.s_step_size

    def get_step_speed_xyz_motor(self):
        return self.xyz_step_speed

    def get_step_speed_syringe_motor(self):
        return self.s_step_speed

    def get_motor_base_speed(self):
        return SLOW_SPEED

    def get_motor_max_speed(self):
        return MAX_SPEED
    
    def get_nL(self):
        return self.nL

    def set_step_size_xyz_motor(self, new_step_size):
        self.xyz_step_size = new_step_size

    def set_step_size_syringe_motor(self, new_step_size):
        self.s_step_size = new_step_size

    def set_step_speed_xyz_motor(self, new_step_speed):
        self.s_step_speed = new_step_speed

    def set_step_speed_syringe_motor(self, new_step_speed):
        self.s_step_speed = new_step_speed

    def set_nL(self, nL):
        self.nL = nL

    def set_tc_flag(self, is_tc_mounted: bool):
        self.tc_flag = is_tc_mounted

    def set_tc_lid_flag(self, status: str):
        self.tc_lid_flag = status


# Joystick functions

    def joystick_step_x_motor(self, direction = 1):
        if direction > 0:
            self.move_right(self.xyz_step_size)
        elif direction < 0:
            self.move_left(self.xyz_step_size)
        else:
            pass
            
    def joystick_step_y_motor(self, direction = 1):
        if direction > 0:
            self.move_down(self.xyz_step_size)
        elif direction < 0:
            self.move_up(self.xyz_step_size)
        else:
            pass

    def joystick_step_z_motor_up(self, side):
        if self.side == LEFT:
            self.pipete_L_Up(self.xyz_step_size)
        if self.side == RIGHT:    
            self.pipete_R_Up(self.xyz_step_size)
    
    def joystick_step_z_motor_down(self, dummyarg):
        if self.side == LEFT:
            self.pipete_L_Down(self.xyz_step_size)
        if self.side == RIGHT:    
            self.pipete_R_Down(self.xyz_step_size)

    def joystick_step_syringe_motor(self, direction = 1):
        if self.side == LEFT:    
            if direction > 0:
                self.plunger_L_Down(self.s_step_size, self.s_step_speed)
            elif direction < 0:
                self.plunger_L_Up(self.s_step_size, self.s_step_speed)
            else:
                pass

        elif self.side == RIGHT:        
            if direction > 0:
                self.plunger_R_Down(self.s_step_size, self.s_step_speed)
            elif direction < 0:
                self.plunger_R_Up(self.s_step_size, self.s_step_speed)
            else:
                pass

# Stepper functions 

    def step(self, device):
        if device == 'X':
            self.step_x_motor()
        if device == 'Y':
            self.step_y_motor()
        if device == 'Z':
            self.step_z_motor()
        if device == 'S':
            self.joystick_step_syringe_motor()

    def step_x_motor(self, step_size="DEFAULT"):
        if (step_size == "DEFAULT"):
            step_size = self.xyz_step_size
        if step_size > 0:
            self.move_right(step_size)
        else:
            self.move_left(step_size)
        
    def step_y_motor(self, step_size="DEFAULT"):
        if (step_size == "DEFAULT"):
            step_size = self.xyz_step_size
        if step_size > 0:
            self.move_up(step_size)
        else:
            self.move_down(step_size)

    def step_z_motor(self, step_size="DEFAULT"):
        # print(f"step_z_motor size: {step_size}")
        if (step_size == "DEFAULT"):
            step_size = self.xyz_step_size
        if step_size > 0:
            # print("step_size")
            self.pipete_L_Up(step_size)
        else:
            # print("step_size")
            self.pipete_L_Down(step_size)

    def step_syringe_motor(self, step_size="DEFAULT"):
        if (step_size == "DEFAULT"):
            step_size = self.s_step_size
        if step_size < 0:
            # print(f"Down: {step_size}")
            self.plunger_L_Up_aut(step_size)
        elif step_size > 0:
            # print(f"Up: {step_size}")
            self.plunger_L_Down_aut(step_size)
        
# Other functions

    def move_to(self, location):
        # print(location)
        # x = location["X"] #or self.ot_control._position["X"]
        # y = location["Y"] #or self.ot_control._position["Y"]
        # z = location["Z"] #or self.ot_control._position["Z"]

        x = location[0] #or self.ot_control._position["X"]
        y = location[1] #or self.ot_control._position["Y"]
        z = location[2] #or self.ot_control._position["Z"]

        current_z_pos = self._position['Z']
        if current_z_pos != z:
            self.move({'Z': Z_MAX}, speed= MEDIUM_SPEED)
        elif current_z_pos == z and (current_z_pos + 30) < Z_MAX:
            self.move({'Z': current_z_pos + 30}, speed= MEDIUM_SPEED)
        else:
            self.move({'Z': current_z_pos}, speed= MEDIUM_SPEED)
        if(self.check_for_valid_move(y, 'Y', None)):
            # First move the Y axis so that it does not collapse with the thermocycler
            self.move({'Y': y}, speed= MEDIUM_SPEED)
            if(self.check_for_valid_move(x, 'X', None)):
                self.move({'X': x}, speed= MEDIUM_SPEED)
                if(self.check_for_valid_move(z, 'Z', None)):
                    self.move({'Z': z}, speed= MOVE_TO_SPEED)

    def change_to_L_axis(self, dummyarg):
        # This function allows the controller to have more functionality
        self.side = LEFT
            
    def change_to_R_axis(self, dummyarg):
        # This function allows the controller to have more functionality
        self.side = RIGHT

    def get_motor_coordinates(self):
        x = self._position['X']
        y = self._position['Y']
        z = self._position['Z']
        return x, y, z
    
    def home_all(self, dummyarg):
        # print("Example:  'X Y Z A B C' or 'all' ")
        try:
            self.home('X Y Z A')
        except SmoothieError:
            self.home('A') # Home the syringe
        
    def stop_motor(self, device = 'XYZABC'):
        self.disengage_axis(device)

    def nothing(self, argument = 1):
        pass
    
    def screen_info(self, dummyarg):
        print("............................................")
        print("")
        print(f"Step size S set to:          {self.s_step_size}") 
        print(f"Nanoliters to pick up:       {self.nL}")
        print(f"Step size XYZ set to:        {self.xyz_step_size}")
        print(f"Pipette controlling:         {self.side}")
        print(f"X: {self.position['X']}   Y: {self.position['Y']}   Z: {self.position['Z']}  S_B:  {self._position['B']} S_C:  {self._position['C']}")
        print("")
        print("............................................")

    def find_port(self):
        """
        This allows the class to connect to a port when called, this makes the calling chain cleaner. 
        It is basicaly a ger_port_by_name from the driver_3_0_0 that does not work
        """
        ports = list_ports.comports()
        operating_system = os.name
        for p in ports:
            # print(p)
            if operating_system == WINDOWS_OS and p.serial_number == WINDOWS_OT_SER:
                self._port = p.device
                print(f"OT2 connected to: {p}")
            elif operating_system == LINUX_OS:
                if p == LINUX_OT_PORT or p.device == MACBOOK_OT_PORT:
                    self._port = p.device
                    # print(self._port)
                    print(f"OT2 connected to: {p}")
                else: 
                    # print(f"Port not found: {p.device}")
                    pass
            # else:
            #     print(f"No operating system recognized: {operating_system}")
            
    def connect_driver(self):
        """
        This function is called at the beginning of the class in the init function to connect the robot
        """
        self.find_port()
        self.connect(self._port)

def test():
    robot = OT2_nanotrons_driver()
    robot.find_port()

if __name__ == '__main__':
    test()
