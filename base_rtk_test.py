import serial
import time

clrGGA = '$PUBX,40,GGA,0,0,0,0*5A\r\n'
clrGLL = '$PUBX,40,GLL,0,0,0,0*5C\r\n'
clrRMC = '$PUBX,40,RMC,0,0,0,0*47\r\n'
clrVTG = '$PUBX,40,VTG,0,0,0,0*5E\r\n'
clrGSA = '$PUBX,40,GSA,0,0,0,0*4E\r\n'
clrGSV = '$PUBX,40,GSV,0,0,0,0*59\r\n'

CFGPRTbase = 'B5620600140001000000C0080000004B000000002000000000004ECD'
CFGPRTbaseTEST = 'B5620600140001000000C0080000004B000000002000000000001122'
ACKACKpoll = 'B562050100000617'
ACKNAKpoll = 'B562050000000514'

def read_msgs(ublox):
    i = 0
    time.sleep(.5)
    while(ublox.in_waiting > 0):
        print('# of bytes to be read:' + str(ublox.in_waiting))
        print('loop #' + str(i))
        i = i + 1
        print(ublox.readline())
        #print('\n\r')
    return

base_stn = serial.Serial('/dev/ttyACM0',9600)
#print(CFGPRTbase.encode('utf-8'))
CFGPRTbaseTEST = bytes.fromhex(CFGPRTbaseTEST)
ACKACKpoll = bytes.fromhex(ACKACKpoll)
#ACKNAKpoll = bytes.fromhex(ACKNAKpoll)
read_msgs(base_stn)
print('-----clearing default messages-----')
#base_stn.write(clrGGA.encode('utf-8'))
base_stn.write(clrGLL.encode('utf-8'))
base_stn.write(clrRMC.encode('utf-8'))
base_stn.write(clrVTG.encode('utf-8'))
base_stn.write(clrGSA.encode('utf-8'))
base_stn.write(clrGSV.encode('utf-8'))
print('-----reading leftover messages-----')
read_msgs(base_stn)
base_stn.write(CFGPRTbaseTEST)
base_stn.write(ACKACKpoll)
print('-----reading results of CFGPRT-----')
read_msgs(base_stn)
print('finished reading messages')
base_stn.close()


