import serial
from sys import platform
#import rover_rtk_test
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
#ublox = serial.Serial(port,9600)

#rover_rtk_test.read_msgs(ublox)
print('clearing default messages')
#rover_rtk_test.clearDefaultMsgs(ublox)
print('enabling RTK Messages input')
#rover_rtk_test.enableRTKMsgs(ublox)

print('RTK Mode enabled')


# Prompt User to initiate Establishing Level
while True:
    response = input('Establish level? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
    if (str(response).lower()[0] == 'y'):
        break

# TODO: Establish Level


# Prompt User to point to remote unit
print("Point gimbal to remote unit.")
# Give instructions on how to do so.
print('Use 4 to move left, 6 to move right')
print('8 to move up, and 2 to move down')
print('press 0 when finished')
    # Allow the user to point things

#Establish North
# notify of waiting for RTK fix
print('Waiting for RTK-GPS fix')
# Confirm RTK fix  (have a time out?)

# Ensure GPS has RTK Fix
print('RTK-GPS fix obtained')
    # Get Relative Position
print('relative position of ')
    #PRINT RELATIVE POSITION
    # Calculate Azimuth and Elevation Angle
print('Azimuth and Elevation at ')
    #PRINT ABSOLUTE AZIMUTH AND ELEVATION
print('Correlated with heading and pitch of')
    #PRINT PITCH AND HEADING

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
                        response = input('Is this correct? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
                        if (str(response).lower()[0] == 'y'):
                            proceed = True
                            repeat = False
                        elif (str(response).lower()[0] == 'n'):
                            repeat = False
                
            #Make LLA coordinate
            
            #Give option to enter gimbal unit GPS location
            print('Current Station GPS location calculated as ')
            #PRINT CURRENT STATION GPS LOCATION WITH ACCURACY
            response = input('Enter Station coordinate? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
            if (str(response).lower()[0] == 'y'):
                proceed = False
                while not proceed:
                    print('Enter Station GPS coordinate in Degrees, Degrees, and Feet (separated by commas)')
                    response = input('Station Coordinates: ')
                    baseCoors = [x.strip() for x in response.split(',')]
                    if (len(baseCoors) >= 3) :
                        repeat = True
                        while repeat:
                            print('Station Coordinate = (' + baseCoors[0] + ', ' + baseCoors[1] + ', ' + baseCoors[2] + ').')
                            response = input('Is this correct? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
                            if (str(response).lower()[0] == 'y'):
                                proceed = True
                                repeat = False
                            elif (str(response).lower()[0] == 'n'):
                                repeat = False
            #Make an LLA coordinate
            
            #Confirm data and Prompt to start pointing calculation
            repeat = True
            while repeat:
                print('Data as entered:')
                print('Base Station GPS Location: (' + str(baseCoors[0]) + ', ' + str(baseCoors[1]) + ', ' + str(baseCoors[2]) + ').')
                print('Taget Station GPS Location: (' + str(targetCoors[0]) + ', ' + str(targetCoors[1]) + ', ' + str(targetCoors[2]) + ').')
                response = input('Is this correct? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
                if (str(response).lower()[0] == 'y'):
                    finishGPSEntry = True
                    repeat = False
                elif (str(response).lower()[0] == 'n'):
                    repeat = False
            
        #Calculate the absolute and delta Az El (Range?)
        #Report these data and the necessary rotations to point
        repeat = True
        while (repeat):
            print('Pitch: ')
            print('Heading: ')
            print('Elevation')
            print('Azimuth: ')
            print('By Rotating on Pitch and on Heading')
            print('New Pitch: ')
            print('New Heading: ')
            print('New Elevation: ')
            print('New Azimuth: ')
            response = input('Proceed with Pointing? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
            if (str(response).lower()[0] == 'y'):
                beginPoint = True
                repeat = False
            elif (str(response).lower()[0] == 'n'):
                repeat = False
            

    #Begin Pointing
    #Prompt to change target coordinate.
    repeat = True
    while (repeat):
        print('Current Target Coordinate: ' + str(targetCoors[0]) + ', ' + str(targetCoors[1]) + ', ' + str(targetCoors[2]) + ')')
        response = input('Change Target Coordinate? (\033[4mY\033[0mes/\033[4mN\033[0mo)')
        if (str(response).lower()[0] == 'y'):
            changePoint = True
            repeat = False
        elif (str(response).lower()[0] == 'n'):
            repeat = True
        