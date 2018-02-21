import serial
import time
import reading
from reading import readMsg

clrGGA = '$PUBX,40,GGA,0,0,0,0*5A\r\n'
clrGLL = '$PUBX,40,GLL,0,0,0,0*5C\r\n'
clrRMC = '$PUBX,40,RMC,0,0,0,0*47\r\n'
clrVTG = '$PUBX,40,VTG,0,0,0,0*5E\r\n'
clrGSA = '$PUBX,40,GSA,0,0,0,0*4E\r\n'
clrGSV = '$PUBX,40,GSV,0,0,0,0*59\r\n'

CFGPRTrover = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 20 00 00 00 00 00 00 00 4E 0D'

def read_msgs(ublox):
    i = 0
    time.sleep(1)
    while(ublox.in_waiting > 0):
        print('# of bytes to be read:' + str(ublox.in_waiting))
        print('loop #' + str(i))
        i = i + 1
        print(ublox.readline())
    return

rover = serial.Serial('/dev/ttyACM0',9600)

read_msgs(rover)
print('-----clearing default messages-----')
rover.write(clrGGA.encode('utf-8'))
rover.write(clrGLL.encode('utf-8'))
rover.write(clrRMC.encode('utf-8'))
rover.write(clrVTG.encode('utf-8'))
rover.write(clrGSA.encode('utf-8'))
rover.write(clrGSV.encode('utf-8'))
##print('-----reading leftover messages-----')
##read_msgs(rover)
print('-----writing RTK GPS enabling messages-----')
rover.write(CFGPRTrover)
print('-----reading results of RTK GPS messages-----')
time.sleep(1)
while base_stn.in_waiting > 0:
    print(readMsg(base_stn), end='') read_msgs(rover)
#print(base_stn.read(rover.in_waiting))
print('-----end of script-----')
rover.close()


