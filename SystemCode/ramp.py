import curses
#import time
from curses import wrapper
from time import sleep
#import pigpio
import RPi.GPIO as GPIO

#step_frequency = 8000    # Frequency of steps. You can change this.
DIR = 20         # Direction GPIO Pin first motor
STEP = 21    # Step GPIO Pin first motor
STEP2 = 26    # Step GPIO PIN second motor
DIR2 = 12    # Direction for second motor
#ENABLE = 16    # GPIO pin for enable which should be set low for steppers to work
delay1 = .0005
delay2 = .00001
delay3 = .000025

cw = 0
ccw = 1
# Connect to pigpiod daemon
#pi = pigpio.pi()

# Set up pins as an output
#pi.set_mode(DIR, pigpio.OUTPUT)
#pi.set_mode(STEP, pigpio.OUTPUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR,GPIO.OUT)
GPIO.setup(STEP,GPIO.OUT)
GPIO.setup(DIR2,GPIO.OUT)
GPIO.setup(STEP2,GPIO.OUT)

# Define Intial Values for integers
i = 1
j = 1
k = 1
l = 1

def main(stdscr):
    steps = 5000        #This is the initial step size of 1.8 degrees
    step1 = 1000
    step2 = 2000
    step3 = steps-step1-step2
    stdscr.clear()
    stdscr.nodelay(True)
    print("Running some program")
    while True:
        # Store the key value in the variable 'direction'
        direction = stdscr.getch()
        # clear the terminal
        stdscr.clear()
        sleep(.0025)
        #pi.write(ENABLE, False)

        if direction == -1:
            stdscr.addstr("No key press")
            #pi.set_PWM_dutycycle(STEP, 0)
            #pi.set_PWM_dutycycle(STEP2, 0)
            #pi.set_PWM_frequency(STEP, 0)
            #pi.set_PWM_frequency(STEP2, 0)
            
        elif direction == ord('5'):
            stdscr.addstr("RAMPING")
            #pi.write(DIR, True)
            for x in range(step1):
                GPIO.output(DIR,ccw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay1)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay1)
            for x in range(step2):
                GPIO.output(DIR,ccw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay2)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay2)
            for x in range(step3):
                GPIO.output(DIR,ccw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay3)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay3)
            #pi.set_PWM_dutycycle(STEP, 128)        # 50% On 50% Off
            #pi.set_PWM_frequency(STEP, step_frequency)    # 4000 pulses per second
                
        elif direction == ord('4'):
            stdscr.addstr("RAMPING")
            #pi.write(DIR, True)
            for x in range(step1):
                GPIO.output(DIR,cw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay1)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay1)
            for x in range(step2):
                GPIO.output(DIR,cw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay2)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay2)
            for x in range(step3):
                GPIO.output(DIR,cw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay3)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay3)
            #pi.set_PWM_dutycycle(STEP, 128)        # 50% On 50% Off
            #pi.set_PWM_frequency(STEP, step_frequency)    # 4000 pulses per second
                
        
        else:
            stdscr.addstr("I dont'know that key")
            #direction = '0'
            #pi.set_PWM_dutycycle(STEP, 0)
            #pi.set_PWM_dutycycle(STEP2, 0)
            #pi.set_PWM_frequency(STEP, 0)
            #pi.set_PWM_frequency(STEP2, 0)

wrapper(main)