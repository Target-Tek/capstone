# Target-Tek (BYU Capstone Team 19) Accelerometer Calibration Code.
# Calibrate our accelerometer by taking a number of readings
# from equally spaced points around a circle. Averaging these will
# give us a golden reference value for the accelerometer.
# Author: Lukas Nordlin
# 1/18/2018

# Requires Python 3.4 or later

# IMPORTANT: You must 'sudo raspi-config' and enable SPI before this script will work!

from time import sleep # Give us access to a clock and time.sleep(seconds).
from statistics import mean # Take averages. Requires 3.4 or later.
from spidev import * # Import py-spidev library for SPI communications.
from numpy import int8 # For converting two's complement bytes to ints
from math import pi # Used for converting from radians to degrees.

class Accelerometer:
    # Constants for all class instances.
    number_of_readings = 8	# Take 8 readings at 45 degree increments.
    settling_time_delay_s = .500	# Wait this many ms for device to settle before taking a reading.
    time_to_rotate_s = 2.000	# Allow this long for gimbal to rotate before taking the next reading.
    lsb_per_g = 1024 # Least significant bits per g, used to interpret output.

    # Constructor. Initializes things to zero.
    def __init__(self):
        self.count = 0	# Initialize count. How many readings have we taken.
        self.x_golden, self.y_golden, self.z_golden = -1, -1, -1    # Initialize to error value.
        self.x_readings, self.y_readings, self.z_readings = [], [], []   # Initialize data vectors.
        self.spi = SpiDev() # Create SPI object.
        self.spi.open(0,0) # Open SPI object for communication.
        self.spi.max_speed_hz = 100000 # Set communication rate
        self.spi.mode = 0b11 # Set CPOL/CPHA
        self.spi.xfer([0x2C, 0x06]) # Set lowest output data rate for minimum noise.
        self.spi.xfer([0x31, 0x80]) # Set full resolution mode, 1024 LSB/g.
        self.spi.xfer([0x2D, 0x08]) # Turn on accelerometer's measurement mode.

    def test(self):
        # A test method, reading the device ID registers of the accelerometer
        # and comparing them to known values.
        msg = [0xC0, 0x00, 0x00, 0x00] # Message to read the three device registers.
        received = self.spi.xfer(msg) # Communicate with accelerometer.
        desired = [0x00, 0xAD, 0x1D, 0xCB] # This is what we should get back.
        print('First byte is junk and does not have to match.')
        print('Received message: ', received)
        print(' Desired message: ', desired)

    def calibrate(self):
        # TODO: reset gimbal to zero position.
        while self.count < 8:
            # TODO: Rotate gimbal.
            sleep(Accelerometer.time_to_rotate_s)    # Allow time for rotation.
            sleep(Accelerometer.settling_time_delay_s)   # Allow time for device to settle.
            [x_read, y_read] = self.raw_output() # Read accelerometer output data.
            # Append new data to array
            x_readings.append(x_read)
            y_readings.append(y_read)

            # END TODO
            self.count = self.count + 1   # Increment count of how many readings have been taken.
        # Do the math and compute the averages.
        self.x_golden = mean(self.x_readings)
        self.y_golden = mean(self.y_readings)
        self.z_golden = mean(self.z_readings)

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
        x_offset = x_read / lsb_per_g # Convert our error to g's.
        y_offset = y_read / lsb_per_g # Convert our error to g's.
        # Small-angle approximation: The g's we are off by
        # is equal to the radians we are off by.
        x_offset = x_offset * 180 / pi # Convert to degrees.
        y_offset = y_offset * 180 / pi # Convert to degrees.
        return [x_offset, y_offset] # Angular offset from level in degrees

    def offset_total(self):
        # Return overall angular error from level.
        [x_offset, y_offset] = self.offset() # Compute individual offsets.
        return float(x_offset(self)**2 + y_offset(self)**2)**0.5 # Combine them.
