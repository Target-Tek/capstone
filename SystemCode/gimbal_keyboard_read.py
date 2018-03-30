import curses
#import time
from curses import wrapper
from time import sleep
#import pigpio
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep


#step_frequency = 8000    # Frequency of steps. You can change this.
DIR = 20         # Direction GPIO Pin first motor
STEP = 21    # Step GPIO Pin first motor
STEP2 = 26    # Step GPIO PIN second motor
DIR2 = 12    # Direction for second motor
#ENABLE = 16    # GPIO pin for enable which should be set low for steppers to work
delay = .000025
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
    steps =1000        #This is the initial step size of 1.8 degrees
    stdscr.clear()
    stdscr.nodelay(True)
    print("Running some program")
    camera = PiCamera()
    camera.start_preview()
    #sleep(10000)
    #camera.stop_preview()
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
            
        elif direction == ord('6'):
            stdscr.addstr("I want to move right")
            #pi.write(DIR, True)
            for x in range(steps):
                GPIO.output(DIR,ccw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay)
            #pi.set_PWM_dutycycle(STEP, 128)        # 50% On 50% Off
            #pi.set_PWM_frequency(STEP, step_frequency)    # 4000 pulses per second
                
        elif direction == ord('8'):
            stdscr.addstr("I want to move up")
            #pi.write(DIR2, True)
            for x in range(steps):
                GPIO.output(DIR2,cw)
                GPIO.output(STEP2,GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP2,GPIO.LOW)
                sleep(delay)
            #pi.set_PWM_dutycycle(STEP2, 128)        # 50% On 50% Off
            #pi.set_PWM_frequency(STEP2, step_frequency)
        elif direction == ord('4'):
            stdscr.addstr("I want to move left")
            #pi.write(DIR, False)
            for x in range(steps):
                GPIO.output(DIR,cw)
                GPIO.output(STEP,GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP,GPIO.LOW)
                sleep(delay)
            #pi.set_PWM_dutycycle(STEP, 128)        # 50% On 50% Off
            #pi.set_PWM_frequency(STEP, step_frequency)    # 4000 pulses per second
        elif direction == ord('2'):
            stdscr.addstr("I want to move down")
            #pi.write(DIR2, True)
            for x in range(steps):
                GPIO.output(DIR2,ccw)
                GPIO.output(STEP2,GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP2,GPIO.LOW)
                sleep(delay)
            #pi.set_PWM_dutycycle(STEP2, 128)        # 50% On 50% Off
            #pi.set_PWM_frequency(STEP2, step_frequency)
        elif direction == ord('9'):
            stdscr.addstr("Large Step size")
            steps = 1000    #This is a step size of .18 degrees
        elif direction == ord('7'):
            stdscr.addstr("Medium Step size")
            steps = 100    #This is a step size of .18 degrees
        elif direction == ord('3'):
            stdscr.addstr("Small Step size")
            steps = 10    #This is a step size of .018 degrees
        elif direction == ord('1'):
            stdscr.addstr("Tiny Step size")
            steps = 1    #This is a step size of .0018 degrees
        elif direction == ord('0'):
            stdscr.addstr("Finished Pointing")
            break
        else:
            stdscr.addstr("I dont'know that key")
            #direction = '0'
            #pi.set_PWM_dutycycle(STEP, 0)
            #pi.set_PWM_dutycycle(STEP2, 0)
            #pi.set_PWM_frequency(STEP, 0)
            #pi.set_PWM_frequency(STEP2, 0)

def startScanning():
    wrapper(main)