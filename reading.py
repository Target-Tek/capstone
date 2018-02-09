'''
Created on Feb 7, 2018

@author: Keith
'''
import time
import serial
import binascii


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


def readMsg(serialIn):
    firstByte = serialIn.read(1)
    if firstByte == b'$':
        return NMEA_readMsg(firstByte, serialIn).decode('utf-8')
    else:
        ubxMsg = ''.join('{:02x}'.format(x) for x in UBX_readMsg(firstByte, serialIn))
        return 'UBX: 0x' + ubxMsg + '\r\n'
        
    
    
ublox = serial.Serial(
    port = 'COM4',
    baudrate = 9600)
UBX_config_prt = bytes.fromhex('B5620600140001000000C0080000004B000000002000000000004ECD')
i = 0
while(1):
    while(ublox.in_waiting > 0):
        print(readMsg(ublox), end='')
              
    ublox.write(UBX_config_prt)
    time.sleep(1)
    
    #print('\n\r')
