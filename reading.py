'''
Created on Feb 7, 2018

@author: Keith
'''
import time
import serial
import binascii
import ctypes

#calculates the UBX checksum over payload.
# and returns that checkSum as two bytes in
# a bytearray
def UBX_genCheckSum(payload):
    CHK_A = 0;
    CHK_B = 0;
    one_byte = 255;
    for ch in payload:
        CHK_A += ch;
        CHK_B += CHK_A;
    CHK_A = one_byte & CHK_A
    CHK_B = one_byte & CHK_B
    return bytearray([CHK_A, CHK_B])


# takes and returns bytes-like object
#calculates the checksum from all but the first two bytes
#and appends them to a new bytearray which is returned
def UBX_appendChecksum(message_no_checkSum):
    payload = message_no_checkSum[2:]
    chkSum = UBX_genCheckSum(payload)
    baMessage = bytearray(message_no_checkSum)
    for chkVal in chkSum:
        baMessage.append(chkVal)
    return baMessage


#takes bytes-like message and compares the checksum
#calculated over the bytes not including the first two bytes
# nor the last 2 bytes
# returns true if the bytes match
def UBX_validateCheckSum(message):
    payload = message[2:-2]
    ourChkSum = UBX_genCheckSum(payload);
    for i in range(0, 2):
        if message[i - 2] != ourChkSum[i]:
            print('checkSum failed: ')
            print(message)
            return False
        
    return True

def UBX_readMsg(firstByte, serialIn):
    msg = bytearray(firstByte)
    for i in range(0,5):
        nextByte = serialIn.read(1)
        msg.append(nextByte[0])
    
    length = msg[4] + msg[5]*256
    for i in range(0, length):
        nextByte = serialIn.read(1)
        msg.append(nextByte[0])
    
    for i in range(0,2):
        nextByte = serialIn.read(1)
        msg.append(nextByte[0])
    
    if UBX_validateCheckSum(msg):
        return msg;
    else:
        return bytearray()
    
def NMEA_readMsg(firstByte, serialIn):
    msg = firstByte
    msg = msg + serialIn.readline()
    #checkSum for NMEA
    return msg

def parseUbxNavSvin(ubxMsg):
    ubxMsgStr = ''.join('{:02x}'.format(x) for x in ubxMsg)
	uTimeOfTheWeek = getUnsigned(ubxMsg[8:12], 4)
	uDurationPassed = getUnsigned(ubxMsg[12:16], 4)
	meanX = getSigned(ubxMsg[16:20], 4)
	meanY = getSigned(ubxMsg[20:24], 4)
	meanZ = getSigned(ubxMsg[24:28], 4)
	meanXHP = getSigned(ubxMsg[28:29], 1)
	meanYHP = getSigned(ubxMsg[29:30], 1)
	meanZHP = getSigned(ubxMsg[30:31], 1)
	meanAcc = getUnsigned(ubxMsg[32:36], 4)
	posObs = getUnsigned(ubxMsg[36:40], 4)
	validSurvey = getUnsigned(ubxMsg[40:41], 1)
	activeSurvey = getUnsigned(ubxMsg[41:42], 1)
	SVIN_interpreted = "UBX-NAV-SVIN: " + ubxMsgStr + "\n\r" \
		+ "Time of Week: " + str(uTimeOfTheWeek) + "\n\r" \
		+ "Suverying for: " + str(uDurationPassed) + "\n\r" \
		+ "ECEF position in m: (" + str((meanX / 100.0) + (meanXHP / 10000.0)) + "," \
		+ str((meanY / 100.0) + (meanYHP / 10000.0)) + "," \
		+ str((meanZ / 100.0) + (meanZHP / 10000.0)) + ")\n\r" \
		+ "Accuracy in m: " + str(meanAcc / 10000.0) + "\n\r" \
		+ "Sample count: " + str(posObs) + "\n\r" \
		+ "SVIN valid?: " + str(True if validSurvey else False) + "\n\r" \
		+ "SVIN active?: " + str(True if activeSurvey else False) + "\n\r" \
		+ "\n\r"
	return SVIN_interpreted
	
	
def parseUbxMsg(ubxMsg):
    if ubxMsg[2] ==  1 and ubxMsg[3] == 59: # 0x01 
        return parseUbxNavSvin(ubxMsg)
    else:
		ubxMsgStr = ''.join('{:02x}'.format(x) for x in ubxMsg)
        return 'UBX: 0x' + ubxMsgStr + '\r\n'

def getUnsigned(val, length):
    retVal = 0;
    for x in range(0, length):
        retVal = val[x] << (8 * x)
    return retVal

def getSigned(val, length):
    asUnsigned = getUnsigned(val, length);
    return ctypes.c_long(asUnsigned).value

def readMsg(serialIn):
    firstByte = serialIn.read(1)
    if firstByte == b'$':
        return NMEA_readMsg(firstByte, serialIn).decode('utf-8')
    else:
        ubxMsg = UBX_readMsg(firstByte, serialIn)
        return parseUbxMsg(ubxMsg)
        
    
    
#ublox = serial.Serial(
#    port = 'COM4',
#    baudrate = 9600)
##UBX_NAV_SVIN_msg =  bytes.fromhex('b562012c28000000000050c3000000000000000000000000000000000000000000000000000000000000000000778e')
##UBX_config_prt = bytes.fromhex('B5620600140001000000C0080000004B000000002000000000004ECD')
##print(parseUbxMsg(UBX_NAV_SVIN_msg))
#i = 0
#while(1):
#    while(ublox.in_waiting > 0):
#        print(readMsg(ublox), end='')
              
#    ublox.write(UBX_config_prt)
#    time.sleep(1)
    
    #print('\n\r')
