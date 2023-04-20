import pygame
from drivers.OTdriver import OT2_nanotrons_driver as OT2

class Keyboard:
    def __init__(self, driver = OT2):
        self.otdriver = driver
        self.keep_listening = False


    def reset_values(self):
        self.keep_listening = False
    """
    LISTEN SECTION
    """
    # Listens to the controller's input
    def listen(self):
        self.reset_values() # reset the values read from the last call for listen_one()
        self.keep_listening = True
        while (self.keep_listening):
            # EVENT DETECTION AND PRINT
            # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.otdriver.move_forward(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_DOWN:
                        self.otdriver.move_back(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_LEFT:
                        self.otdriver.move_left(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_RIGHT:
                        self.otdriver.move_right(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_q:
                        self.otdriver.Z_axis_Up(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_a:
                        self.otdriver.Z_axis_Down(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_w:
                        self.otdriver.A_axis_Up(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_s:
                        self.otdriver.A_axis_Down(step_size= self.otdriver.xyz_step_size)

    # Sets to False the boolean that controls the listen() loop
    def stop_listening(self, dummy_arg):
        self.keep_listening = False


def testing():
    driver = OT2
    controller = Keyboard()
    controller.listen(driver)
    
    

if __name__ == "__main__":
    testing()