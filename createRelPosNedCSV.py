import re


with open('RTK test 3_7_18 interpretted') as f:
    regex = re.compile('m\s[NED]\s\+\-|m,\s|m\n') #'m [NED] +-|m,\s', 
    for line in f:
        if (line[0:10] == "position: "):
            msgIn = line[10:]
            vals = regex.split(msgIn)
            #("interpretting " + msgInHex);
            outLine = ",".join(map(str, vals))
            print(outLine)