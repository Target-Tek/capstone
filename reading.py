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
    
def parseUbxNavDGPS(ubxMsg):
    ubxMsgStr = ''.join('{:02x}'.format(x) for x in ubxMsg)
    msgContent = ubxMsg[6:]
    timeOfWeek = getTimeOfWeek(msgContent[0:4])
    age = getSigned(msgContent[4:8], 4)
    baseId = getSigned(msgContent[8:10], 2)
    baseHealth = getSigned(msgContent[10:12], 2)
    numCh = getUnsigned(msgContent[12:13], 1)
    status = getUnsigned(msgContent[13:14], 1)
    for x in range(0, numCh):
        offset = 12*x
        satID = getUnsigned(msgContent[16 + offset:17 + offset], 1)
        flags = getSigned(msgContent[17 + offset:18 + offset], 1)
        ageC = getUnsigned(msgContent[18 + offset: 20 + offset], 2)
        pseudoCorrection = getUnsigned(msgContent[20 + offset: 24 + offset], 4)
        pseudoRateCorrection = getUnsigned(msgContent[24 + offset: msgContent[28 + offset]], 4)
    #Do something with the data
    
def parseUbxNavRelposned(ubxMsg):
    ubxMsgStr = ''.join('{:02x}'.format(x) for x in ubxMsg)
    msgContent = ubxMsg[6:]
    version = getUnsigned(msgContent[0:1], 1)
    refStationID = getUnsigned(msgContent[2:4], 2)
    timeOfWeek = getTimeOfWeek(msgContent[4:8])
    relPosN = getSigned(msgContent[8:12], 4)    # cm
    relPosE = getSigned(msgContent[12:16], 4)   # cm
    relPosD = getSigned(msgContent[16:20], 4)   # cm
    relPosHPN = getSigned(msgContent[20:21], 1) # .1 mm
    relPosHPE = getSigned(msgContent[21:22], 1) # .1 mm
    relPosHPD = getSigned(msgContent[22:23], 1) # .1 mm
    accN = getUnsigned(msgContent[24:28], 4)    # .1 mm
    accE = getUnsigned(msgContent[28:32], 4)    # .1 mm
    accD = getUnsigned(msgContent[32:36], 4)    # .1 mm
    flags = getUnsigned(msgContent[36:40], 4)   # .1 mm
    relPosN_m = (relPosN / 100.0) + (relPosHPN / 10000.0)
    relPosE_m = (relPosE / 100.0) + (relPosHPE / 10000.0)
    relPosD_m = (relPosD / 100.0) + (relPosHPD / 10000.0)
    accN_meters = accN / 10000.0
    accE_meters = accE / 10000.0
    accD_meters = accD / 10000.0
    gnss_ok = (flags & (1)) == 1
    difSoln = ((flags >> 1) & 1) == 1
    relPosValid = ((flags >> 2) & 1) == 1
    carrSoln = ((flags >> 3) & 3)
    isMoving = ((flags >> 5) & 1) == 1
    refPosMiss = ((flags >> 6) & 1) == 1
    refObsMiss = ((flags >> 7) & 1) == 1
    
    return "UBX-NAV-RELPOSNED " + ubxMsgStr + "\n" +\
            "ver" + str(version) + " station " + str(refStationID) + "\n" +\
            timeOfWeek.getFullString() + "\n" +\
            "position: " + str(relPosN_m) + "m N +-" + str(accN_meters) + "m, "\
            + str(relPosE_m) + "m E +-" + str(accE_meters) + "m, "\
            + str(relPosD_m) + "m D +-" + str(accD_meters) + "m\n" +\
            "gnssOk? " + str(gnss_ok) + " diffSoln? " + str(difSoln) + " relPosValid? "+ str(relPosValid) +"\n" +\
            "carrSoln: " + ("No soln" if carrSoln == 0 else ("float" if (carrSoln == 1) else ("fix" if (carrSoln == 2) else "Err"))) + "\n" +\
            "isMoving? " + str(isMoving) + " extrapRefPos? " + str(refPosMiss) + " extrapRebObs" + str(refObsMiss)
    

def parseUbxNavSvin(ubxMsg):
    ubxMsgStr = ''.join('{:02x}'.format(x) for x in ubxMsg)
    msgContent = ubxMsg[6:]
    uTimeOfTheWeek = getTimeOfWeek(msgContent[4:8])
    uDurationPassed = getUnsigned(msgContent[8:12], 4)
    meanX = getSigned(msgContent[12:16], 4)
    meanY = getSigned(msgContent[16:20], 4)
    meanZ = getSigned(msgContent[20:24], 4)
    meanXHP = getSigned(msgContent[24:25], 1)
    meanYHP = getSigned(msgContent[25:26], 1)
    meanZHP = getSigned(msgContent[26:27], 1)
    meanAcc = getUnsigned(msgContent[28:32], 4)
    posObs = getUnsigned(msgContent[32:36], 4)
    validSurvey = getUnsigned(msgContent[36:37], 1)
    activeSurvey = getUnsigned(msgContent[37:38], 1)
    x = (meanX / 100.0) + (meanXHP / 10000.0)
    y = (meanY / 100.0) + (meanYHP / 10000.0)
    z = (meanZ / 100.0) + (meanZHP / 10000.0)
    acc = meanAcc / 10000.0

    globals()['surveyInState'] = SurveyInStatus(ubxMsgStr, uTimeOfTheWeek, uDurationPassed, \
                                                x, y, z, acc, posObs, validSurvey,\
                                                activeSurvey)
    return surveyInState.getFullString()
    
    
def parseUbxMsg(ubxMsg):
    if ubxMsg[2] ==  1 and ubxMsg[3] == 59: # 0x01 , 0x3B
        return parseUbxNavSvin(ubxMsg)
    if ubxMsg[2] == 1 and ubxMsg [3] == 0x3C:
        return parseUbxNavRelposned(ubxMsg)
    else:
        ubxMsgStr = ''.join('{:02x}'.format(x) for x in ubxMsg)
        return 'UBX: 0x' + ubxMsgStr + '\r\n'

class SurveyInStatus:        
    def __init__(self, MSG, timeOfWeek, duration, x, y, z, \
                    accuracy, samples, valid, active):
        self.MSG = MSG
        self.currentTime = timeOfWeek
        self.duration = duration
        self.ECEFx = x
        self.ECEFy = y
        self.ECEFz = z
        self.ECEFaccuracy = accuracy
        self.samples = samples;
        self.isValid = valid;
        self.isActive = active;
        
    def getFullString(self):
        return "UBX-NAV-SVIN: " + self.MSG + "\n\r" \
        + "Time of Week: " + self.currentTime.getFullString() + "\n\r" \
        + "Suverying for: " + str(self.duration) + "\n\r" \
        + "ECEF position in m: (" + str(self.ECEFx) + "," \
        + str(self.ECEFy) + "," \
        + str(self.ECEFz) + ")\n\r" \
        + "Accuracy in m: " + str(self.ECEFaccuracy) + "\n\r" \
        + "Sample count: " + str(self.samples) + "\n\r" \
        + "SVIN valid?: " + str(True if self.isValid else False) + "\n\r" \
        + "SVIN active?: " + str(True if self.isActive else False) + "\n\r" \
        + "\n\r"
    MSG = -1
    currentTime = -1
    duration = -1
    ECEFx = -1
    ECEFy = -1
    ECEFz = -1
    ECEFaccuracy = -1
    samples = -1
    isValid = False
    isActive = False
        
class TimeOfWeek:
    CONST_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    MS_IN_SEC = 1000
    SEC_IN_DAY = 86400
    SEC_IN_HOUR = 3600
    SEC_IN_MINUTE = 60
    
    def __init__(self, milliseconds):
        self.inMs = milliseconds
        seconds = self.inMs // self.MS_IN_SEC;
        #print (seconds)
        self.numDay = seconds // self.SEC_IN_DAY;
        seconds = seconds - self.numDay * self.SEC_IN_DAY
        self.numHour = seconds // self.SEC_IN_HOUR
        seconds = seconds - self.numHour * self.SEC_IN_HOUR
        self.numMin = seconds // self.SEC_IN_MINUTE
        seconds = seconds - self.numMin * self.SEC_IN_MINUTE
        self.numSec = seconds
        
    def getFullString(self):
        day = -1
        if self.numDay < 7 and self.numDay >= 0:
            day = self.CONST_DAYS[self.numDay]
        else:
            day = "ERR_DAY"
        
        return "" + str(self.inMs) + "ms - " + day + " " + str(self.numHour) + ":" + str(self.numMin) + ":" + str(self.numSec)
        
    inMs = -1
    numDay = -1
    numHour = -1
    numMin = -1
    numSec = -1

        
def getTimeOfWeek(val):
    inMs = getUnsigned(val[0:4], 4)
    return TimeOfWeek(inMs)
        
def getUnsigned(val, length):
    #print(''.join('{:02x}'.format(x) for x in val))
    retVal = 0;
    for x in range(0, length):
        nextPart = val[x] << (8*x)
        retVal = retVal + nextPart
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
        
        
surveyInState = SurveyInStatus(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1)

        
#ublox = serial.Serial(
#    port = 'COM4',
#    baudrate = 9600)
#CFGPRTbase_revised = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 20 00 00 00 00 00 00 00'
#CFGPRT_msg = bytes.fromhex(CFGPRTbase_revised)
#CFGPRT_msg = UBX_appendChecksum(CFGPRT_msg)
#print (CFGPRT_msg)
#print (parseUbxMsg(CFGPRT_msg))
#UBX_NAV_SVN_msg =  bytes.fromhex('b562 013b 2800 00 000000 87654321 0000000000000000000000000000000000000000000000000000000000000000778e')
#UBX_config_prt = bytes.fromhex('B5620600140001000000C0080000004B000000002000000000004ECD')
#print(parseUbxMsg(UBX_NAV_SVN_msg))
#i = 0
#while(1):
#    while(ublox.in_waiting > 0):
#        print(readMsg(ublox), end='')
              
#    ublox.write(UBX_config_prt)
#    time.sleep(1)
    
    #print('\n\r')
