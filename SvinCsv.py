import re


with open('survery_in_data.txt') as f:
    regex = re.compile('Accuracy in m: |\n') #'m [NED] +-|m,\s', 
    for line in f:
        if (line[0:15] == "Accuracy in m: "):
            msgIn = line[15:]
            vals = regex.split(msgIn)
            #("interpretting " + msgInHex);
            outLine = ",".join(map(str, vals))
            print(outLine)
