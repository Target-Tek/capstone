# Target-Tek (BYU Capstone Team 19) Accelerometer Calibration Code.
# Calibrate our accelerometer by taking a number of readings
# from equally spaced points around a circle. Averaging these will
# give us a golden reference value for the accelerometer.
# Author: Lukas Nordlin
# 1/18/2018

# Requires Python 3.4 or later
# For the ADXL313

# IMPORTANT: You must 'sudo raspi-config' and enable SPI before this script will work!

from time import sleep # Give us access to a clock and time.sleep(seconds).
from statistics import mean # Take averages. Requires 3.4 or later.
from spidev import * # Import py-spidev library for SPI communications.
from numpy import int8 # For converting two's complement bytes to ints
from math import pi # Used for converting from radians to degrees.
import RPi.GPIO as GPIO # Used for GPIO and driving the stepper 

class Accelerometer:
    # Constants for all class instances.
    number_of_readings = 8	# Take 8 readings at 45 degree increments.
    settling_time_delay_s = .500	# Wait this many ms for device to settle before taking a reading.
    lsb_per_g = 1024 # Least significant bits per g, used to interpret output.
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
        self.x_golden, self.y_golden, self.z_golden = -1, -1, -1    # Initialize to error value.
        self.x_readings, self.y_readings, self.z_readings = [], [], []   # Initialize data vectors.
        self.spi = SpiDev() # Create SPI object.
        self.spi.open(0,0) # Open SPI object for communication.
        self.spi.max_speed_hz = 100000 # Set communication rate
        self.spi.mode = 0b11 # Set CPOL/CPHA
#        self.spi.xfer([0x2C, 0x06]) # Set lowest output data rate for minimum noise.
#        self.spi.xfer([0x31, 0x80]) # Set full resolution mode, 1024 LSB/g.
        self.spi.xfer([0x2D, 0x08]) # Turn on accelerometer's measurement mode.
        # Stepper code
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Accelerometer.DIR,GPIO.OUT)
        GPIO.setup(Accelerometer.DIR2,GPIO.OUT)
        GPIO.setup(Accelerometer.STEP,GPIO.OUT)
        GPIO.setup(Accelerometer.STEP2,GPIO.OUT)

    def test(self):
        # A test method, reading the device ID registers of the accelerometer
        # and comparing them to known values.
        msg = [0xC0, 0x00, 0x00, 0x00] # Message to read the three device registers.
        received = self.spi.xfer(msg) # Communicate with accelerometer.
        desired = [0x00, 0xAD, 0x1D, 0xCB] # This is what we should get back.
        print('First byte is junk and does not have to match.')
        print('Received message: ', received)
        print(' Desired message: ', desired)

    def eighth_rotation(self):
        for x in range(25000): # One eighth of a full rotation.
            GPIO.output(Accelerometer.DIR,Accelerometer.CW)
            GPIO.output(Accelerometer.STEP,GPIO.HIGH)
            sleep(Accelerometer.delay)
            GPIO.output(Accelerometer.STEP,GPIO.LOW)
            sleep(Accelerometer.delay)

    def self_level(self):
        [x_offset, y_offset] = self.offset() # Read angular offset in degrees
        if y_offset > 0:
            GPIO.output(Accelerometer.DIR2,Accelerometer.CW)
        else:
            GPIO.output(Accelerometer.DIR2,Accelerometer.CCW)
        for i in range(int(y_offset / Accelerometer.degrees_per_step)):
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
        # Level the platform.
        self.self_level()

    def raw_output(self):
        # Gives the raw accelerometer output, interpreted as numbers.
        # Output registers for X and Y axes are 0x32 - 0x35.
        # First two bits are both set high, the first bit indicating a read
        # and the second indicating a multi-byte read, so our message is 0xF2.
        msg = [0xF2, 0x00, 0x00, 0x00, 0x00] # Message to be sent.
        data = self.spi.xfer(msg) # Send data over SPI and read output.
        output = [] # Initialize output data array
        # Interpret bytes as numbers
        output.append((int8(data[2]) << 8) + int8(data[1])) # Concatenate bytes
        output.append((int8(data[4]) << 8) + int8(data[3])) # Concatanate bytes
        return output

    def offset(self):
        # Returns a vector containing angular offsets from level, in degrees.
        [x_read, y_read] = self.raw_output() # Read accelerometer data.
        x_read = x_read - self.x_golden # Find our error in LSBs.
        y_read = y_read - self.y_golden # Find our error in LSBs.
        x_offset = x_read / Accelerometer.lsb_per_g # Convert our error to g's.
        y_offset = y_read / Accelerometer.lsb_per_g # Convert our error to g's.
        # Small-angle approximation: The g's we are off by
        # is equal to the radians we are off by.
        x_offset = x_offset * 180 / pi # Convert to degrees.
        y_offset = y_offset * 180 / pi # Convert to degrees.
        return [x_offset, y_offset] # Angular offset from level in degrees

    def offset_total(self):
        # Return overall angular error from level.
        [x_offset, y_offset] = self.offset() # Compute individual offsets.
        return float(x_offset(self)**2 + y_offset(self)**2)**0.5 # Combine them.
