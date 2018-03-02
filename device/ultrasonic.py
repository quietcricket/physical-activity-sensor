##
# Ultrasonic library for MicroPython's pyboard.
# Compatible with HC-SR04 and SRF04.
#
# Copyright 2014 - Sergio Conde Gómez <skgsergio@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import machine
import utime

# Pin configuration.
# WARNING: Do not use PA4-X5 or PA5-X6 as the echo pin without a 1k resistor.

class Ultrasonic:
    def __init__(self, tPin, ePin):
        self.triggerPin = tPin
        self.echoPin = ePin

        # Init trigger pin (out)
        self.trigger = machine.Pin(self.triggerPin, machine.Pin.OUT)
        self.trigger.off()

        # Init echo pin (in)
        self.echo = machine.Pin(self.echoPin, machine.Pin.IN)

    def distance_in_cm(self):
        start = 0
        end = 0

        # Create a microseconds counter.

        # Send a 10us pulse.
        self.trigger.on()
        utime.sleep_us(10)
        self.trigger.off()
        t=machine.time_pulse_us(self.echo,1)
        # Calc the duration of the recieved pulse, divide the result by
        # 2 (round-trip) and divide it by 29 (the speed of sound is
        # 340 m/s and that is 29 us/cm).
        dist_in_cm = (t / 2) / 29

        return str(int(dist_in_cm))