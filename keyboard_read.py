import curses
import time
from curses import wrapper
from time import sleep
import pigpio

step_frequency = 4000	# Frequency of steps. You can change this.
DIR = 20     	# Direction GPIO Pin
STEP = 21	# Step GPIO Pin
STEP2 = 26	# Step GPIO PIN second motor
DIR2 = 12	# Direction for second motor
ENABLE = 16	# GPIO pin for enable which should be set low for steppers to work

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)


def main(stdscr):
	stdscr.clear()
	stdscr.nodelay(True)
	print("Running some program")
	while True:
		# Store the key value in the variable 'direction'
		direction = stdscr.getch()
		# clear the terminal
		stdscr.clear()
		time.sleep(.025)
		pi.write(ENABLE, False)

		if direction == -1:
			stdscr.addstr("No key press")
			pi.set_PWM_dutycycle(STEP, 0)
			pi.set_PWM_dutycycle(STEP2, 0)
			pi.set_PWM_frequency(STEP, 0)
			pi.set_PWM_frequency(STEP2, 0)

		elif direction == ord('6'):
			stdscr.addstr("I want to move right")
			pi.write(DIR, True)
			pi.set_PWM_dutycycle(STEP, 128)		# 50% On 50% Off
			pi.set_PWM_frequency(STEP, step_frequency)	# 4000 pulses per second

		elif direction == ord('8'):
			stdscr.addstr("I want to move up")
			pi.write(DIR2, True)
			pi.set_PWM_dutycycle(STEP2, 128)		# 50% On 50% Off
			pi.set_PWM_frequency(STEP2, step_frequency)
		elif direction == ord('4'):
			stdscr.addstr("I want to move left")
			pi.write(DIR, False)
			pi.set_PWM_dutycycle(STEP, 128)		# 50% On 50% Off
			pi.set_PWM_frequency(STEP, step_frequency)	# 4000 pulses per second

		elif direction == ord('2'):
			stdscr.addstr("I want to move down")
			pi.write(DIR2, True)
			pi.set_PWM_dutycycle(STEP2, 128)		# 50% On 50% Off
			pi.set_PWM_frequency(STEP2, step_frequency)
		else:
			stdscr.addstr("I dont'know that key")
			direction = '0'
			pi.set_PWM_dutycycle(STEP, 0)
			pi.set_PWM_dutycycle(STEP2, 0)
			pi.set_PWM_frequency(STEP, 0)
			pi.set_PWM_frequency(STEP2, 0)

wrapper(main)

