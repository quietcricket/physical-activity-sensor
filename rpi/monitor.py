
# Import required Python libraries
from datetime import datetime
import time
import os
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24
# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)  # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(1)

data = []


def read_distance():
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()

    # Calculate pulse length
    elapsed = stop - start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2
    return round(distance, 1)

# Create a folder to keep all the data
if not os.path.exists('data'):
    os.mkdir('data')

if __name__ == '__main__':

    # 10 readings per second
    READ_FREQUENCEY=0.1
    # save the log once per minute 
    LOG_FREQUENCY=60/READ_FREQUENCEY

    while True:
        data.append(str(read_distance()))
        if len(data) ==LOG_FREQUENCY:
            t=datetime.now()
            with open(t.strftime('data/%Y-%m-%d.txt'),'a') as f:
                f.write(t.strftime('%H:%M')+','.join()+"\n")
                data = []
        else:
            time.sleep(READ_FREQUENCEY)
    # Reset GPIO settings
    GPIO.cleanup()

