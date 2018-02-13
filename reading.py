'''
Created on Feb 7, 2018

@author: Keith
'''

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
    print(payload)
    ourChkSum = UBX_genCheckSum(payload);
#    for val in ourChkSum:
#        print(hex(val))
    for i in range(0, 2):
        if message[i - 2] != ourChkSum[i]:
            return False
        
    return True


    

msgString = 'B5620600140001000000C0080000004B000000002000000000004ECD'

msg = bytearray.fromhex(msgString)

print (UBX_validateCheckSum(msg))   