

msg = input('input hex message\n\r')
msg = bytes.fromhex(msg)
print(msg)
CK_A = 0
CK_B = 0
one_byte = 255
for x in range(2, (len(msg)-2)):
    CK_A = CK_A + msg[x]
    CK_B = CK_B + CK_A
byte_A = one_byte & CK_A
byte_B = one_byte & CK_B
CK_A = hex(byte_A)
CK_B = hex(byte_B)
print(CK_A)
print(CK_B)

