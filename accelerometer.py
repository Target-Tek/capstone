# Target-Tek (BYU Capstone Team 19) Accelerometer Calibration Code.
# Calibrate our accelerometer by taking a number of readings
# from equally spaced points around a circle. Averaging these will
# give us a golden reference value for the accelerometer.
# Author: Lukas Nordlin
# 1/18/2018

# Requires Python 3.4 or later

from time import sleep # Give us access to a clock and time.sleep(seconds).
from statistics import mean # Take averages. Requires 3.4 or later.
import RPi.GPIO as GPIO # Give us GPIO access.

class Accelerometer:
    # Constants for all class instances.
    error_tolerance = 1	# Leeway in the accelerometer reading.
    number_of_readings = 8	# Take 8 readings at 45 degree increments.
    settling_time_delay_s = .500	# Wait this many ms for device to settle before taking a reading.
    time_to_rotate_s = 2.000	# Allow this long for gimbal to rotate before taking the next reading.
    number_of_flashes = 10	# Number of blinks to indicate we're done. Purely visual.
    flash_delay_s = .050	# Time between blinks. Purely visual.

    # Constructor. Initializes things to zero.
    def __init__(self):
        self.count = 0	# Initialize count. How many readings have we taken.
        self.x_golden, self.y_golden, self.z_golden = -1, -1, -1    # Initialize to error value.
        self.x_readings, self.y_readings, self.z_readings = [], [], []   # Initialize data vectors.

    def calibrate(self):
        # TODO: reset gimbal to zero position.
        while self.count < 8:
            # TODO: Rotate gimbal.
            sleep(Accelerometer.time_to_rotate_s)    # Allow time for rotation.
            sleep(Accelerometer.settling_time_delay_s)   # Allow time for device to settle.
            # TODO: Read GPIO and append new data to lists.
            self.count = self.count + 1   # Increment count of how many readings have been taken.
        # Do the math and compute the averages.
        self.x_golden = mean(self.x_readings)
        self.y_golden = mean(self.y_readings)
        self.z_golden = mean(self.z_readings)

    def x_offset(self):
        pass # TODO: give difference from level in x direction

    def y_offset(self):
        pass # TODO: give difference from level in y direction

    def offset(self):
        pass # TODO: give total difference from level overall
