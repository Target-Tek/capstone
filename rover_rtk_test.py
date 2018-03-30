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

NAVPVTpoll = 'B5 62 01 07 00 00 08 19'
NAVRELPOSNEDpoll = 'B5 62 01 3C 00 00 3D B8'

#CFGPRTrover = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 20 00 00 00 00 00 00 00 4E 0D'#old
CFGPRTrover = 'B5 62 06 00 14 00 01 00 00 00 D0 08 00 00 00 4B 00 00 20 00 00 00 00 00 00 00 5E 0D'#new

def read_msgs(ublox):
    time.sleep(1)
    while(ublox.in_waiting > 0):
        #print('# of bytes to be read:' + str(ublox.in_waiting))
        print(readMsg(ublox), end = '')       
    return

def clearDefaultMsgs(ublox):
    ublox.write(clrGGA.encode('utf-8'))
    ublox.write(clrGLL.encode('utf-8'))
    ublox.write(clrRMC.encode('utf-8'))
    ublox.write(clrVTG.encode('utf-8'))
    ublox.write(clrGSA.encode('utf-8'))
    ublox.write(clrGSV.encode('utf-8'))
    
def enableRTKMsgs(ublox):
    ublox.write(bytes.fromhex(CFGPRTrover))
    
def pollRelativePostion(ublox):
    ublox.write(bytes.fromhex(NAVRELPOSNEDpoll))
    read_msgs(ublox)
    
if __name__ == '__main__':
    rover = serial.Serial('/dev/ttyACM0',9600)
    
    read_msgs(rover)
    print('-----clearing default messages-----')
    clearDefaultMsgs(rover)
    
    ##print('-----reading leftover messages-----')
    ##read_msgs(rover)
    print('-----writing RTK GPS enabling messages-----')
    enableRTKMsgs(rover)
    print('-----reading results of RTK GPS messages-----')
    #time.sleep(1)
    secBtwnRead = 1
    i = 0
    j = 0
    for x in range(0,2700):
        print(str(i) + 'seconds')
        i = i + secBtwnRead
        j = j + 1
        rover.write(bytes.fromhex(NAVPVTpoll))
        pollRelativePostion(rover)
        time.sleep(secBtwnRead - 1)
    print('-----end of script-----')
    rover.close()
