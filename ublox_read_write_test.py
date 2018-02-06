#!/usb/bin/python

import serial
import time
#these messages disable the default messages
#output by the ublox
clrGGA = '$PUBX,40,GGA,0,0,0,0*5A\r\n'
clrGLL = '$PUBX,40,GLL,0,0,0,0*5C\r\n'
clrRMC = '$PUBX,40,RMC,0,0,0,0*47\r\n'
clrVTG = '$PUBX,40,VTG,0,0,0,0*5E\r\n'
clrGSA = '$PUBX,40,GSA,0,0,0,0*4E\r\n'
clrGSV = '$PUBX,40,GSV,0,0,0,0*59\r\n'

#opens a USB connection to the ublox
ublox = serial.Serial('/dev/ttyACM0', 9600)
print('ublox opened')
#allows the ublox time to push messages to the output queue
time.sleep(1)
i = 0
#while loop reads all messages in the ublox output queue
while(ublox.in_waiting > 0):
    print('# of bytes to be read:' + str(ublox.in_waiting))
    print('loop #' + str(i))
    i = i + 1
    print(ublox.readline())
#writes the clear messages to the ublox.  Comment
#to pick which messages you don't want to disable
print('-----clearing default messages-----')
#ublox.write(clrGGA.encode('utf-8'))
ublox.write(clrGLL.encode('utf-8'))
ublox.write(clrRMC.encode('utf-8'))
ublox.write(clrVTG.encode('utf-8'))
ublox.write(clrGSA.encode('utf-8'))
ublox.write(clrGSV.encode('utf-8'))
#allows the ublox time to push messages to the output queue
time.sleep(1)
#while loop reads all messages in the ublox output queue.
#Disabled messages should not be recieved
while(ublox.in_waiting > 0):
    print('# of bytes to be read:' + str(ublox.in_waiting))
    print('loop #' + str(i))
    i = i + 1
    print(ublox.readline())
#closes the USB serial connection between the pi and ublox
ublox.close()