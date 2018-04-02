# Target-Tek (BYU Capstone Team 19) Accelerometer Calibration Code.
# Calibrate our accelerometer by taking a number of readings
# from equally spaced points around a circle. Averaging these will
# give us a golden reference value for the accelerometer.
# Author: Lukas Nordlin
# 1/18/2018

# Requires Python 3.4 or later
# For the ADXL335

# IMPORTANT: You must 'sudo raspi-config' and enable I2C before this script will work!

from time import sleep # Give us access to a clock and time.sleep(seconds).
from math import pi # Used for converting from radians to degrees.
import RPi.GPIO as GPIO # Used for GPIO and driving the stepper 
from ADCPi import ADCPi # Used for reading the accelerometer.

class Accelerometer:
    # Constants for all class instances.
    number_of_readings = 8	# Take 8 readings at 45 degree increments.
    settling_time_delay_s = 1.000	# Wait this many ms for device to settle before taking a reading.
    volts_per_g = 0.11 # Approximately how many volts per g.
    # Stepper motor interface parameters
    step_frequency = 4000
    degrees_per_step = 0.002
    delay = .00005 # Delay parameter for driving steppers.
    DIR = 20
    STEP = 21
    CW = 0
    CCW = 1
    STEP2 = 26
    DIR2 = 12
    ENABLE = 16

    # Constructor. Initializes things to zero.
    def __init__(self):
        self.count = 0	# Initialize count. How many readings have we taken.
        self.x_golden, self.y_golden, self.z_golden = 0.561187, 0.563388, -1    # Initialize to error value.
        self.x_readings, self.y_readings, self.z_readings = [], [], []   # Initialize data vectors.
        self.adc = ADCPi(0x68, 0x69, 18) # Create an ADC object at the correct address with the minimum output data rate
        # Stepper code
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Accelerometer.DIR,GPIO.OUT)
        GPIO.setup(Accelerometer.DIR2,GPIO.OUT)
        GPIO.setup(Accelerometer.STEP,GPIO.OUT)
        GPIO.setup(Accelerometer.STEP2,GPIO.OUT)
        # Step tracking
        self.cw_steps_taken_from_baseline = 0

    def eighth_rotation(self):
        for x in range(25000): # One eighth of a full rotation.
            GPIO.output(Accelerometer.DIR,Accelerometer.CW)
            GPIO.output(Accelerometer.STEP,GPIO.HIGH)
            sleep(Accelerometer.delay)
            GPIO.output(Accelerometer.STEP,GPIO.LOW)
            sleep(Accelerometer.delay)

    def self_level(self):
        [x_offset, y_offset] = self.offset() # Read angular offset in degrees
        steps = abs(int(y_offset / Accelerometer.degrees_per_step))
        if y_offset < 0:
            GPIO.output(Accelerometer.DIR2,Accelerometer.CW)
            self.cw_steps_taken_from_baseline = self.cw_steps_taken_from_baseline + steps
        else:
            GPIO.output(Accelerometer.DIR2,Accelerometer.CCW)
            self.cw_steps_taken_from_baseline = self.cw_steps_taken_from_baseline - steps
        for i in range(steps):
            GPIO.output(Accelerometer.STEP2,GPIO.HIGH)
            sleep(Accelerometer.delay)
            GPIO.output(Accelerometer.STEP2,GPIO.LOW)
            sleep(Accelerometer.delay)

    def calibrate(self):
        while self.count < 8:
            sleep(Accelerometer.settling_time_delay_s)
            [x_read, y_read] = self.raw_output() # Read accelerometer output data.
            # Append new data to array
            self.x_readings.append(x_read) # Save reading to array.
            self.y_readings.append(y_read) # Save reading to array.
            self.eighth_rotation() # Rotate to position for next reading.
            self.count = self.count + 1   # Increment count of how many readings have been taken.
        # Do the math and compute the averages.
        self.x_golden = sum(self.x_readings) / 8.0
        self.y_golden = sum(self.y_readings) / 8.0

    def raw_output(self):
        # Gives the raw accelerometer output, interpreted as numbers.
        return [self.adc.read_voltage(7), self.adc.read_voltage(8)]

    def offset(self):
        # Returns a vector containing angular offsets from level, in degrees.
        [x_read, y_read] = self.raw_output() # Read accelerometer data.
        x_read = x_read - self.x_golden # Find our error in LSBs.
        y_read = y_read - self.y_golden # Find our error in LSBs.
        x_offset = x_read / Accelerometer.volts_per_g# Convert our error to g's.
        y_offset = y_read / Accelerometer.volts_per_g # Convert our error to g's.
        # Small-angle approximation: The g's we are off by
        # is equal to the radians we are off by.
        x_offset = x_offset * 180 / pi # Convert to degrees.
        y_offset = y_offset * 180 / pi # Convert to degrees.
        return [x_offset, y_offset] # Angular offset from level in degrees

    def offset_total(self):
        # Return overall angular error from level.
        [x_offset, y_offset] = self.offset() # Compute individual offsets.
        return float(x_offset**2 + y_offset**2)**0.5 # Combine them.
