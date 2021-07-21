"""
FLAG CLASS  
    The purpose of this class is to implement flags that allow for
    going around scope issues with declaring new variables vs assigning
    new values to existing variables on a bigger scope. See the 
    sending_syringe flag in web_app to see its utility
"""

class Flag:
    def __init__(self):
        self.value = False

    def activate(self):
        self.value = True

    def deactivate(self):
        self.value = False

    def read(self):
        return self.value