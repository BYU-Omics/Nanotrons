"""
VIDEOSTREAM CLASS
    This class allows for extracting frames from a hardware camera connected to the hardware running the script
"""

import cv2
from threading import Thread

class VideoStream:
    def __init__(self, src = 0):
        self.stream = cv2.VideoCapture(src) # Initialize the stream from camera object in index 0
        (self.grabbed, self.frame) = self.stream.read() # Extract frame
        self.stopped = False
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.update)
        t.start()
        return self
    
    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
    
    def read(self):
        return self.frame # cv2.flip(self.frame, 1) -> This returns the frame flipped with respect to the Y axis (a parameter of any positive number does that)
    
    def stop(self):
        self.stopped = True

