#!/usr/bin/python
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_1.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013

# Import required Python libraries
import time
import os
import RPi.GPIO as GPIO
import logging
from logging.handlers import TimedRotatingFileHandler

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

logger = logging.getLogger('Physical Activityes')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('data/activities.log', when="midnight")
logger.addHandler(handler)
if not os.path.exists('data'):
    os.mkdir('data')
print "Ultrasonic Measurement"

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


while True:
    data.append(str(read_distance()))
    if len(data) >= 100:
        logger.info(','.join(data))
        data = []
    else:
        time.sleep(0.1)
# Reset GPIO settings
GPIO.cleanup()
