import serial
from sys import platform
import rover_rtk_test
import accelerometer
from SystemCode import gimbal_keyboard_read
from rover_rtk_test import pollRelativePostion
from reading import RelPosNED, HpPosLLH
from coordmath import getAzElFromDiff, CreateLLA, CreateAngles
#from rover_rtk_test import rover
#from email.mime import base

# STEPS


# GPS - Initialize rover RTK Mode
print("initializing RTK Mode")

#How do we know if this is the right port or not?
if platform == 'linux' or platform == "linux2":
    port = '/dev/ttyACM0'
else:
    port = 'COM8'
ublox = serial.Serial(port,9600)

rover_rtk_test.read_msgs(ublox)
print('clearing default messages')
rover_rtk_test.clearDefaultMsgs(ublox)
print('enabling RTK Messages input')
rover_rtk_test.enableRTKMsgs(ublox)

print('RTK Mode enabled')


# Prompt User to initiate Establishing Level
while True:
    response = input('Establish level? (1.Yes,  2. No)')
    if (str(response).lower()[0] == '1'):
        break

acc = accelerometer.Accelerometer() # Create Accelerometer object.
#acc.calibrate() # Note: calibrate() is not currently functional. Measured level values are hardcoded into self_level(). Just call that.


# Prompt User to point to remote unit
print("Point gimbal to remote unit.")
# Give instructions on how to do so.
print('Use 4 to move left, 6 to move right')
print('8 to move up, and 2 to move down')
print('Change speed by pressing (low) 1, 3, 7, or 9 (high)')
print('press 0 when finished')
    # Allow the user to point things
gimbal_keyboard_read.startScanning()
#Establish North
# notify of waiting for RTK fix
print('Waiting for RTK-GPS fix')
# Confirm RTK fix  (have a time out?)
rover_rtk_test.read_msgs(ublox)
hasFix = False
while (not hasFix):
    rover_rtk_test.pollRelativePostion(ublox)
    hasFix = RelPosNED.getMostRecent().rtkFix

# Ensure GPS has RTK Fix I.E. Read again a little later.
print('RTK-GPS fix obtained')
    # Get Relative Position
diffVec = RelPosNED.getMostRecent().getRelPos()
print('relative position of ')
    #PRINT RELATIVE POSITION
gimbalToRemote = [-x for x in diffVec]
print(gimbalToRemote)    
    # Calculate Azimuth and Elevation Angle
AzEl = getAzElFromDiff(gimbalToRemote[0], gimbalToRemote[1], gimbalToRemote[2])
print('Azimuth and Elevation angles of')
print(AzEl)
print('Correlated with heading and pitch of')
    #TODO PRINT PITCH AND HEADING should come from Encoders?
PiHe = acc.offset()
print('TODO!  There is no way to get the current pitch and heading of the system')

#Prompt to enter Pointing Target
changePoint = True
while (changePoint):
    beginPoint = False
    while (not beginPoint):
        finishGPSEntry = False
        while not finishGPSEntry:
            proceed = False
            while not proceed:
                print('Enter Target GPS coordinate in Degrees, Degrees, and Feet (separated by commas)')
                response = input('Target Coordinates: ')
                targetCoors = [x.strip() for x in response.split(',')]
                if (len(targetCoors) >= 3) :
                    repeat = True
                    while repeat:
                        print('Target Coordinate = (' + str(targetCoors[0]) + ', ' + str(targetCoors[1]) + ', ' + str(targetCoors[2]) + ').')
                        response = input('Is this correct? (1.Yes,  2. No)')
                        if (str(response).lower()[0] == '1'):
                            proceed = True
                            repeat = False
                        elif (str(response).lower()[0] == '2'):
                            repeat = False
                
            #Make LLA coordinate
            targetLLA = CreateLLA(targetCoors[0], targetCoors[1], targetCoors[2])
            #Give option to enter gimbal unit GPS location
            rover_rtk_test.pollHPLLA(ublox)
            print('Current Station GPS location calculated as ')
            print(HpPosLLH.getMostRecent().getLLA())
            baseCoors = HpPosLLH.getMostRecent().getLLA()
            response = input('Enter Station coordinate? (1.Yes,  2. No)')
            if (str(response).lower()[0] == '1'):
                proceed = False
                while not proceed:
                    print('Enter Station GPS coordinate in Degrees, Degrees, and Feet (separated by commas)')
                    response = input('Station Coordinates: ')
                    baseCoors = [x.strip() for x in response.split(',')]
                    if (len(baseCoors) >= 3) :
                        repeat = True
                        while repeat:
                            print('Station Coordinate = (' + baseCoors[0] + ', ' + baseCoors[1] + ', ' + baseCoors[2] + ').')
                            response = input('Is this correct? (1.Yes,  2. No)')
                            if (str(response).lower()[0] == '1'):
                                proceed = True
                                repeat = False
                            elif (str(response).lower()[0] == '2'):
                                repeat = False
                #Make an LLA coordinate
                baseLLA = CreateLLA(baseCoors[0], baseCoors[1], baseCoors[2])
            
            #Confirm data and Prompt to start pointing calculation
            repeat = True
            while repeat:
                print('Data as entered:')
                print('Base Station GPS Location: (' + str(baseCoors[0]) + ', ' + str(baseCoors[1]) + ', ' + str(baseCoors[2]) + ').')
                print('Taget Station GPS Location: (' + str(targetCoors[0]) + ', ' + str(targetCoors[1]) + ', ' + str(targetCoors[2]) + ').')
                response = input('Is this correct? (1.Yes,  2. No)')
                if (str(response).lower()[0] == '1'):
                    finishGPSEntry = True
                    repeat = False
                elif (str(response).lower()[0] == '2'):
                    repeat = False
            
        #Calculate the absolute and delta Az El (Range?)
        roPiHe = CreateAngles(0, PiHe[0], PiHe[1]) #TODO, replace with actual roll Pitch and heading vals.
        #Report these data and the necessary rotations to point
        solution = AzEl(baseLLA,roPiHe,targetLLA)
        repeat = True
        while (repeat):
            print('Pitch: ' + PiHe[0])
            print('Heading: ' + PiHe[1])
            print('Elevation' + AzEl[0])
            print('Azimuth: ' + AzEl[1])
            print('By Rotating on Pitch and on Heading')
            solution.displaySol()
            response = input('Proceed with Pointing? (1.Yes,  2. No)')
            if (str(response).lower()[0] == '1'):
                beginPoint = True
                repeat = False
            elif (str(response).lower()[0] == '2'):
                repeat = False
            

    #Begin Pointing
    #TODO: Pointing code (code that takes the offsets as calculated by Palmer's math code, and rotates those number of degrees on az and el.A

    delay1 = .0005
    delay2 = .00001
    delay3 = .000025
    cw = 0
    ccw = 1
    DIR = 20
    STEP = 21
    DIR2 = 12
    STEP2 = 26
    
    El_steps = solution.getRelEl() * 200000 / 360 # Remove magic numbers later lol
    El_steps1 = min(El_steps, 1000)
    El_steps2 = min(El_steps-1000, 1000)
    El_steps3 = El_steps - El_steps1 - El_steps2
    Az_steps  = solution.getRelAz() * 200000 / 360 # Remove magic numbers later lol
    Az_steps1 = min(Az_steps, 1000)
    Az_steps2 = min(Az_steps-1000, 1000)
    Az_steps3 = Az_steps - Az_steps1 - Az_steps2

    # Ramp code for rotating gimbal to target.

    for x in range(Az_steps1):
	GPIO.output(DIR,ccw)
	GPIO.output(STEP,GPIO.HIGH)
	sleep(delay1)
	GPIO.output(STEP,GPIO.LOW)
	sleep(delay1)
    for x in range(Az_steps2):
	GPIO.output(DIR,ccw)
	GPIO.output(STEP,GPIO.HIGH)
	sleep(delay2)
	GPIO.output(STEP,GPIO.LOW)
	sleep(delay2)
    for x in range(Az_steps3):
	GPIO.output(DIR,ccw)
	GPIO.output(STEP,GPIO.HIGH)
	sleep(delay3)
	GPIO.output(STEP,GPIO.LOW)
	sleep(delay3)

    for x in range(El_steps1):
	GPIO.output(DIR2,ccw)
	GPIO.output(STEP2,GPIO.HIGH)
	sleep(delay1)
	GPIO.output(STEP2,GPIO.LOW)
	sleep(delay1)
    for x in range(El_steps2):
	GPIO.output(DIR2,ccw)
	GPIO.output(STEP2,GPIO.HIGH)
	sleep(delay2)
	GPIO.output(STEP2,GPIO.LOW)
	sleep(delay2)
    for x in range(El_steps3):
	GPIO.output(DIR2,ccw)
	GPIO.output(STEP2,GPIO.HIGH)
	sleep(delay3)
	GPIO.output(STEP2,GPIO.LOW)
	sleep(delay3)

    #Prompt to change target coordinate.
    repeat = True
    while (repeat):
        print('Current Target Coordinate: ' + str(targetCoors[0]) + ', ' + str(targetCoors[1]) + ', ' + str(targetCoors[2]) + ')')
        response = input('Change Target Coordinate? (1.Yes,  2. No)')
        if (str(response).lower()[0] == '1'):
            changePoint = True
            repeat = False
        elif (str(response).lower()[0] == '2'):
            repeat = True
       
