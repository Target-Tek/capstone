from reading import parseUbxMsg

with open('RTK test 3_7_18') as f:
    for line in f:
        #print(line[0:6])
        if (line[0:5] == "UBX: "):
            msgInHex = line[7:-1]
            #("interpretting " + msgInHex);
            print(parseUbxMsg(bytes.fromhex(msgInHex)), end='')
        else:
            print(line, end='')