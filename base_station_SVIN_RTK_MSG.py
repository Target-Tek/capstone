from reading import readMsg
#Global
surveyInState = SurveyInStatus(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1)


ublox = serial.Serial(
    port = 'COM8',
    baudrate = 9600)


CFGTMODE3_100M = 'B5 62 06 71 28 00 00 01 00 00 00 00 00 00 00 00 \
                 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3C 00 \
                 00 00 40 42 0F 00 00 00 00 00 00 00 00 00 6D E5'
                 
CFGTMODE3_2M = 'B5 62 06 71 28 00 00 00 01 00 00 00 00 00 00 00 \
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 2C 01 \
                00 00 20 4E 00 00 00 00 00 00 00 00 00 00 3B 62'

CFGTMODE3_2_3M_300S = 'B5 62 06 71 28 00 00 00 01 00 00 00 00 00 00 00 \
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 2C 01 \
                       00 00 D8 59 00 00 00 00 00 00 00 00 00 00 FE 7B'
             
NAV_SVIN_POLL = "B5 62 01 3B 00 00 3C B5"             
             
CFG_CHECK = 'B5 62 06 71 00 00 77 6B'

CFGTMODE3 = 'B5 62 06 71 28 00 00 01 00 00 00 00 00 00 00 00 \
             00 00 00 00 00 00 00 00 00 00 00 00 00 00 3C 00 \
             00 00 40 42 0F 00 00 00 00 00 00 00 00 00 6D E5'
CFGPRTbase = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 00 00 20 00 00 00 00 00 4E CD'
MSG1005 = 'B5 62 06 01 08 00 F5 05 00 01 00 00 00 00 0A 73'
MSG1077 = 'B5 62 06 01 08 00 F5 4D 00 01 00 00 00 00 52 6B'
MSG1087 = 'B5 62 06 01 08 00 F5 57 00 01 00 00 00 00 5C B1'
MSG1230 = 'B5 62 06 01 08 00 F5 E6 00 01 00 00 00 00 EB 9A'

NAV_PVT = 'B5 62 01 07 00 00 08 19 '


#CFGPRTbase_revised = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 20 00 00 00 00 00 00 00'
#CFGPRT_msg = bytes.fromhex(CFGPRTbase_revised)
#CFGPRT_msg = UBX_appendChecksum(CFGPRT_msg)
#print (CFGPRT_msg)
#print (parseUbxMsg(CFGPRT_msg))
#UBX_NAV_SVN_msg =  bytes.fromhex('b562 013b 2800 00 000000 87654321 0000000000000000000000000000000000000000000000000000000000000000778e')
#UBX_config_prt = bytes.fromhex('B5620600140001000000C0080000004B000000002000000000004ECD')
#print(parseUbxMsg(UBX_NAV_SVN_msg))

time.sleep(3)
while(ublox.in_waiting > 0):
    print(readMsg(ublox), end='')
         
#
ublox.write(bytes.fromhex(CFGPRTbase)) #step2: RTCM3 out on UART1
ublox.write(bytes.fromhex(MSG1005)) #step3: Station coordinates
ublox.write(bytes.fromhex(MSG1077)) #GPS coordinates
ublox.write(bytes.fromhex(MSG1087)) #GLONASS observations
ublox.write(bytes.fromhex(MSG1230)) #GLONASS code-phase biases         
         
ublox.write(bytes.fromhex(CFGTMODE3_2_3M_300S))
print ("SENT CFGTMODE3: " +  CFGTMODE3_2_3M_300S)
time.sleep(1)
while(ublox.inWaiting() > 0):
    print(readMsg(ublox), end='')
ublox.write(bytes.fromhex(CFG_CHECK))
print ("SENT CFG_CHECK: " + CFG_CHECK)
time.sleep(1)
while(ublox.inWaiting() > 0):
    print(readMsg(ublox), end = '')

x = 0;
while True:
    print("second #" + str(x))
    x = x + 1
    ublox.write(bytes.fromhex(NAV_SVIN_POLL))
    print ("SENT CFG_CHECK: " + NAV_SVIN_POLL)
    
    time.sleep(1)
    while(ublox.inWaiting() > 0):
        print(readMsg(ublox), end = '')
    print(surveyInState.isValid)
    if surveyInState.isValid:
        break
    
for i in range(0, 300):
    time.sleep(1)
    
    while(ublox.inWaiting() > 0):
        print(readMsg(ublox), end = '')
    ublox.write(bytes.fromhex(NAV_PVT))

ublox.close()
    
    
time.sleep(1)
    
    #print('\n\r')