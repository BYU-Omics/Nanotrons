# import libraries
from opentrons.hardware_control.emulation.app import SMOOTHIE_PORT
import pygame
import movements as mv
from opentrons.drivers.smoothie_drivers.driver_3_0 import SmoothieDriver_3_0_0 as SM

#from ot2_folder import driver_3_0
#setup the COM Port
robot_2_portname = '/dev/cu.usbserial-AQ00KSUJ'
robot_portname = '/dev/cu.usbserial-A50285BI'
robot_baud = 115200
robot_port = None
DISTANCE = 10 # In mm

if __name__ == '__main__':
    
    robot = mv.OT2_nanopots_driver(unit='mm', amount=DISTANCE)
    try:

        print("Connecting to robot...") 
        robot.connect(port='/dev/cu.usbserial-A50285BI')
        print("...connected to robot")
        #bowtie_pattern(X_max=150, Y_max=150)
        robot.home()
        #move_to_zero_pos()
        #robot.disengage_axis('X Y')
        #print(robot._position)

        pygame.init()

        # define some colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        # window settings
        size = [600, 600]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Simple Game")
        FPS = 60
        clock = pygame.time.Clock()

        # game loop
        playing = False
        running = True
        

        while running:
            # event handling        
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        robot.move_left()

                    if event.key == pygame.K_RIGHT:
                        robot.move_right()

                    if event.key == pygame.K_DOWN:
                        robot.move_down()
                        
                    if event.key == pygame.K_UP:
                        robot.move_up()
                        
                    if event.key == pygame.K_q:
                        robot.pipete_L_Up()
                    if event.key == pygame.K_a:
                        robot.pipete_L_Down()

                    if event.key == pygame.K_w:
                        robot.pipete_R_Up()
                    if event.key == pygame.K_s:
                        robot.pipete_R_Down()
                    if event.key == pygame.K_e:
                        robot.plunger_L_Up()
                    if event.key == pygame.K_d:
                        robot.plunger_L_Down()
                    
                    
                        

                print(robot._position)
                        

            

    except KeyboardInterrupt:
        robot.disconnect()
        print("Test Cancelled")
    except Exception as e:
        print("ERROR OCCURED")
        robot.disconnect()
        raise e
    
    print("Test done")
    robot.disconnect()



