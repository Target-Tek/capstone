import serial
import time
import binascii
from reading import readMsg

clrGGA = '$PUBX,40,GGA,0,0,0,0*5A\r\n'
clrGLL = '$PUBX,40,GLL,0,0,0,0*5C\r\n'
clrRMC = '$PUBX,40,RMC,0,0,0,0*47\r\n'
clrVTG = '$PUBX,40,VTG,0,0,0,0*5E\r\n'
clrGSA = '$PUBX,40,GSA,0,0,0,0*4E\r\n'
clrGSV = '$PUBX,40,GSV,0,0,0,0*59\r\n'


CFGTMODE3_100M = 'B5 62 06 71 28 00 00 01 00 00 00 00 00 00 00 00 \
                 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3C 00 \
                 00 00 40 42 0F 00 00 00 00 00 00 00 00 00 6D E5'
                 
CFGTMODE3_2M = 'B5 62 06 71 28 00 00 00 01 00 00 00 00 00 00 00 \
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 2C 01 \
                00 00 20 4E 00 00 00 00 00 00 00 00 00 00 3B 62'

             
NAV_SVIN_POLL = "B5 62 01 3B 00 00 3C B5"             
             
CFG_CHECK = 'B5 62 06 71 00 00 77 6B'

CFG_PRT_Base = 'B5 62 06 00 14 00 01 00 00 00 D0 08 00 00 00 4B \
		  00 00 00 00 20 00 00 00 00 00 5E CD'

#CFGTMODE3 = 'B5 62 06 71 28 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 2C 01 00 00 20 4E 00 00 00 00 00 00 00 00 00 00 3C 88'
#CFGPRTbase = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 00 00 20 00 00 00 00 00 4E CD'
MSG1005 = 'B5 62 06 01 08 00 F5 05 00 01 00 00 00 00 0A 73'
MSG1077 = 'B5 62 06 01 08 00 F5 4D 00 01 00 00 00 00 52 6B'
MSG1087 = 'B5 62 06 01 08 00 F5 57 00 01 00 00 00 00 5C B1'
MSG1230 = 'B5 62 06 01 08 00 F5 E6 00 01 00 00 00 00 EB 9A'
MSG1005poll = 'B5 62 06 01 02 00 F5 05 03 20'
MSG1077poll = 'B5 62 06 01 02 00 F5 4D 4B 68'
MSG1087poll = 'B5 62 06 01 02 00 F5 57 55 72'
MSG1230poll = 'B5 62 06 01 02 00 F5 E6 E4 01'

NAVSVINpoll = 'B5 62 01 3B 00 00 3C B5'
NAVPVTpoll = 'B5 62 01 07 00 00 08 19'

def read_msgs(ublox):
    time.sleep(1)
    print('# of bytes to be read: ' + str(ublox.in_waiting))
    while(ublox.in_waiting > 0):
        print(readMsg(ublox), end = '')
    return

def read_bytes(ublox):
    time.sleep(1)
    msglength = ublox.in_waiting
    msg = []
    while(ublox.in_waiting > 0):
        byte = ublox.read()
        hex_byte = binascii.hexlify(byte)
        ascii_byte = hex_byte.decode('ascii')
        msg.append(ascii_byte)
    list = ''.join(msg)
    print(list)
    return

##print('-----opening serial connection-----')
base_stn = serial.Serial('/dev/ttyACM0',9600)
print('-----reading init messages-----')
read_msgs(base_stn)
##print('-----clearing default messages-----')
##base_stn.write(clrGGA.encode('utf-8'))
##base_stn.write(clrGLL.encode('utf-8'))
##base_stn.write(clrRMC.encode('utf-8'))
##base_stn.write(clrVTG.encode('utf-8'))
##base_stn.write(clrGSA.encode('utf-8'))
##base_stn.write(clrGSV.encode('utf-8'))
##print('-----reading leftover messages-----')
##read_msgs(base_stn)
print('-----writing RTK GPS enable messages-----')
base_stn.write(bytes.fromhex(CFGTMODE3_2M)) #step1: SVIN
base_stn.write(bytes.fromhex(CFG_PRT_Base)) #step2: RTCM3 out on UART1
base_stn.write(bytes.fromhex(MSG1005)) #step3: Station coordinates
base_stn.write(bytes.fromhex(MSG1077)) #GPS coordinates
base_stn.write(bytes.fromhex(MSG1087)) #GLONASS observations
base_stn.write(bytes.fromhex(MSG1230)) #GLONASS code-phase biases
##time.sleep(5)
print('-----reading results of RTK config messages-----')
read_msgs(base_stn)
print('-----reading results of NAVSVINpoll-----')
secBtwnRead = 1
i = 0
j = 0
##while j < 3:
for x in range(0,120)
    print(str(i) + 'seconds')
    i = i + secBtwnRead
    j = j + 1
    base_stn.write(bytes.fromhex(NAVSVINpoll))
	read_msgs(base_stn)
    time.sleep(secBtwnRead - 1)
##base_stn.write(bytes.fromhex(MSG1005poll))
##base_stn.write(bytes.fromhex(MSG1077poll))
##base_stn.write(bytes.fromhex(MSG1087poll))
##base_stn.write(bytes.fromhex(MSG1230poll))
##read_bytes(base_stn)
print('-----end of script-----')
base_stn.close()


