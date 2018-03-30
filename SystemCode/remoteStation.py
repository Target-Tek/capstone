
import time
import serial
from sys import platform

from reading import readMsg, SurveyInStatus

# 60 second minimum, and 3 minute minimum on a Survey In.
CFGTMODE3_3M_60S = 'B5 62 06 71 28 00 00 00 01 00 00 00 00 00 00 00 \
                    00 00 00 00 00 00 00 00 00 00 00 00 00 00 3C 00 \
                    00 00 30 75 00 00 00 00 00 00 00 00 00 00 81 C0'
                    
#Configuration message for delivering RTCM3 messages of UHF antenna.
CFGPRTbase = 'B5 62 06 00 14 00 01 00 00 00 C0 08 00 00 00 4B 00 00 00 00 20 00 00 00 00 00 4E CD'
#Configuration messages necessary for RTK fix.
MSG1005 = 'B5 62 06 01 08 00 F5 05 00 01 00 00 00 00 0A 73'
MSG1077 = 'B5 62 06 01 08 00 F5 4D 00 01 00 00 00 00 52 6B'
MSG1087 = 'B5 62 06 01 08 00 F5 57 00 01 00 00 00 00 5C B1'
MSG1230 = 'B5 62 06 01 08 00 F5 E6 00 01 00 00 00 00 EB 9A'

# Checks the current configuration
CFG_CHECK = 'B5 62 06 71 00 00 77 6B'

# Checks the current SVIN status
NAV_SVIN_POLL = "B5 62 01 3B 00 00 3C B5"   

PREAMBLE = "STATUS: "
DATA_PREAMBLE = "DATA: "

timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
LOGFILE = "log" + timestamp + ".txt"


def printStatus(state):
    s = PREAMBLE + state
    print(s)
    printToLog(s + '\n')
    
def printData(data):
    s = DATA_PREAMBLE + data
    print(s, end='')
    printToLog(s)
    
def printToLog(toPrint):
    print("appending to file " + LOGFILE)
    logFile = open(LOGFILE, 'a');
    logFile.write(toPrint);
    logFile.close();

def start_Survey_In_program():
    print("opening file " + LOGFILE)
    logFile = open(LOGFILE, 'w+')
    logFile.close();
    
    tmp = SurveyInStatus(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    printStatus("connecting to Ublox")
    #How do we know if this is the right port or not?
    if platform == 'linux' or platform == "linux2":
        port = '/dev/ttyACM0'
    else:
        port = 'COM8'
    ublox = serial.Serial(port,9600, timeout=10)
    
    # check if device connected to is the Ublox, or not?
    
    #allow Ublox initialization
    time.sleep(3)
    #read everything the Ublox wrote.
    printStatus("reading through Ublox messages")
    while(ublox.in_waiting > 0):
        printData(readMsg(ublox))
              
    #
    printStatus("enabling RTCM3")
    ublox.write(bytes.fromhex(CFGPRTbase)) #step2: RTCM3 out on UART1
    printStatus("enabling sending Station Coordinates (1005)")
    ublox.write(bytes.fromhex(MSG1005)) #step3: Station coordinates
    printStatus("enabling sending GPS Coordinates (1077)")
    ublox.write(bytes.fromhex(MSG1077)) #GPS coordinates
    printStatus("enabling sending Station GLONASS obs (1087)")
    ublox.write(bytes.fromhex(MSG1087)) #GLONASS observations
    printStatus("enabling sending GLONASS biases (1230)")
    ublox.write(bytes.fromhex(MSG1230)) #GLONASS code-phase biases         
               
    printStatus("beginning Survey in for >=60s unti <=3m accuracy")
    ublox.write(bytes.fromhex(CFGTMODE3_3M_60S))
    printStatus("SENT CFGTMODE3: " +  CFGTMODE3_3M_60S)
    time.sleep(1)
    printStatus("reading from Ublox")
    while(ublox.inWaiting() > 0):
        printData(readMsg(ublox))
    printStatus("reporting configuration")
    ublox.write(bytes.fromhex(CFG_CHECK))
    printStatus("SENT CFG_CHECK: " + CFG_CHECK)
    time.sleep(1)
    printStatus("reading all ublox data")
    while(ublox.inWaiting() > 0):
        printData(readMsg(ublox))
      
    x = 1;
    printStatus("entering Survey-in status loop")
    while True:
        printStatus("SVIN second #" + str(x))
        x = x + 1
        ublox.write(bytes.fromhex(NAV_SVIN_POLL))
        printStatus("SENT CFG_CHECK: " + NAV_SVIN_POLL)
          
        time.sleep(1)
        while(ublox.inWaiting() > 0):
            printData(readMsg(ublox))
        #print(surveyInState.isValid)
        if tmp.isMostRecentValid():
            printStatus("Survey in complete")
            break
         
    printStatus("Printing what Ublox sends.")
    for i in range(0, 20):
        time.sleep(30)
         
        while(ublox.inWaiting() > 0):
            printData(readMsg(ublox))
        #ublox.write(bytes.fromhex(UBX_NAV_RELPOSNED))
     
    ublox.close()
    # f.close()
         
        
start_Survey_In_program()
