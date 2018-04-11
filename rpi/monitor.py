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

# Timeout, for detecting distance.
# Happens when the sound wave doesn't hit anything, or it is blocked by some moving object
TIMEOUT_DURATION = 500.0 / 34300 * 2

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)  # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(1)

data = []
last_good_reading = 0


def read_distance():
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    # while GPIO.input(GPIO_ECHO) == 0:
    #     start = time.time()

    global last_good_reading
    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()
        # Return last good reading if timeout
        if stop - start > TIMEOUT_DURATION:
            return last_good_reading

    # Calculate pulse length
    elapsed = stop - start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)

    last_good_reading = int(round(elapsed * 34300 / 2))
    return last_good_reading


if __name__ == '__main__':
    DATA_FOLDER = 'pas-data'
    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)

    # 5 readings per second
    READ_FREQUENCEY = 0.2
    LOG_SIZE = 60 / READ_FREQUENCEY

    # Log the data every 1 minute
    t = datetime.now()
    minute = t.minute
    hour = t.hour
    while True:
        data.append(str(read_distance()))
        ct = datetime.now()
        # Still the same minute
        if ct.minute == minute:
            time.sleep(READ_FREQUENCEY)
            continue
        folder = '%s/%i-%02i-%02i' % (DATA_FOLDER, ct.year, ct.month, ct.day)
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open('%s/%02i:%02i.txt' % (folder, hour, minute), 'w') as f:
            f.write(','.join(data))
        # a new minute
        minute = ct.minute
        hour = ct.hour
        data = []
    # Reset GPIO settings
    GPIO.cleanup()
