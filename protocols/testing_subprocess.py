"""
This is a protocol that starts a timer. This protocol helps testing the 
    start, pause, continue and stop function on the script.html page. 
"""

import time

if __name__ == "__main__":
    seconds = 0
    while seconds <= 60:
        print(seconds)
        time.sleep(1)
        seconds += 1

    