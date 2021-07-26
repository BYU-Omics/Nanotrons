import pygame
from OTdriver import OT2_nanotrons_driver as OT2

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
        # print("aqui en el thread")
        self.reset_values() # reset the values read from the last call for listen_one()
        # print(f"Started listening to {self.name}!")
        self.keep_listening = True
        while (self.keep_listening):
            # print("while")
            # EVENT DETECTION AND PRINT
            # print(pygame.event.get())
            # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.otdriver.move_up(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_DOWN:
                        self.otdriver.move_down(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_LEFT:
                        self.otdriver.move_left(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_RIGHT:
                        self.otdriver.move_right(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_q:
                        self.otdriver.pipete_L_Up(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_a:
                        self.otdriver.pipete_L_Down(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_w:
                        self.otdriver.pipete_R_Up(step_size= self.otdriver.xyz_step_size)
                    elif event.key == pygame.K_s:
                        self.otdriver.pipete_R_Down(step_size= self.otdriver.xyz_step_size)

    # Sets to False the boolean that controls the listen() loop
    def stop_listening(self, dummy_arg):
        self.keep_listening = False


def testing():
    driver = OT2
    controller = Keyboard()
    controller.listen(driver)
    
    

if __name__ == "__main__":
    testing()