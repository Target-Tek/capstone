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
import spidev # Import py-spidev library for SPI communications.

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
        self.spi = spidev.SpiDev() # Create SPI object.
        self.spi.open(0,0) # Open SPI object for communication.
        self.spi.max_speed_hz = 100000 # Set communication rate
        self.spi.mode = 0b11 # Set CPOL/CPHA
        self.spi.xfer([0x2D, 0x08]) # Turn on accelerometer's measurement mode.

    def test(self):
        # A test method, reading the device ID registers of the accelerometer
        # and comparing them to known values.
        msg = [0xC0, 0x00, 0x00, 0x00] # Message to read the three device registers.
        received = self.spi.xfer(msg) # Communicate with accelerometer.
        desired = [0x00, 0xAD, 0x1D, 0xCB] # This is what we should get back.
        print('Received message: ', received)
        print(' Desired message: ', desired)

    def calibrate(self):
        # TODO: reset gimbal to zero position.
        while self.count < 8:
            # TODO: Rotate gimbal.
            sleep(Accelerometer.time_to_rotate_s)    # Allow time for rotation.
            sleep(Accelerometer.settling_time_delay_s)   # Allow time for device to settle.
            # TODO: Read from SPI and append new data to lists.
            # Output registers for X and Y axes are 0x32 - 0x35.
            # First two bits are both set high, the first bit indicating a read
            # and the second indicating a multi-byte read, so our message is 0xF2.
            msg = [0xF2, 0x00, 0x00, 0x00, 0x00] # First byte we get back is junk.
            data = self.spi.xfer(msg) # Send data over SPI and read output.
            # Interpret bytes as numbers
            x_read = (data[2] << 8) + data[1]
            y_read = (data[4] << 8) + data[3]
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
        # Gives the raw accelerometer output.
        msg = [0xF2, 0x00, 0x00, 0x00, 0x00] # Message to be sent.
        data = self.spi.xfer(msg) # Send data over SPI and read output.
        data = data[1:] # Throw away the first (junk) byte.
        return data

    def x_offset(self):
        pass # TODO: give difference from level in x direction

    def y_offset(self):
        pass # TODO: give difference from level in y direction

    def offset(self):
        # Return overall angular error from level.
        return float(x_offset(self)**2 + y_offset(self)**2)**0.5
