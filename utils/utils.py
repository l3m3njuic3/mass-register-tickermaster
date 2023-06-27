import time
import random 

def human_type(element, message):
    for char in message:
        time.sleep(random.uniform(0.1, 0.7))
        element.send_keys(char)