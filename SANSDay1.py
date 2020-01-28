#Philip Waters
#Jan 28, 2020
#Proof of Concept study guide for UTF8 
#Day 1 of SANS SEC573 - Python for Pen Testers
#I built this code for my 8 year old son to play with. 
#It shows various examples how to turn binary, int, or hex
#Into UTF-8 and does some boundary handling to make it easy for kids

def output_utf8(bytesobject):
    return bytesobject.decode('utf8')
    
def byte_string_four_by_8bit(val1, val2, val3, val4):
    valstring="{}{} {}{}".format(format(val1, 'x'), format(val2, 'x'), format(val3,'x'), format(val4, 'x'))
    return valstring;

def byte_string_two_by_16bit(vala, valb):
    valstring="{} {}".format(format(vala, 'x'), format(valb, 'x'))
    return valstring
     
def byte_string_add_two_int(val1, val2, val3, val4):
    vala=(val1<<8)+val2
    valb=(val3<<8)+val4
    valstring=byte_string_two_by_16bit(vala, valb)
    return valstring 

def print_by_offset(val1, val2, val3, val4):  
    vala=val1+0xf0 #0xe0+0b10000000
    valb=val2+0x80
    valc=val3+0x80
    vald=val4+0x80
    valstring=byte_string_add_two_int(vala, valb, valc, vald)
    
    try:
        print("{} {} {} {}: {},{},{},{}: {}".format(format(vala,'b'), format(valb, 'b'), format(valc,'b'), format(vald,'b'), int(val1), int(val2), int(val3), int(val4), output_utf8(bytes.fromhex(valstring))))
    except ValueError as error:
        print("For first byte 0xf0 (0)")
        print("second byte must result byte >0x90 (16+)")
        print("For first byte 0xf4 (4)")
        print("second byte must result byte <0x90 (Up to +16)")

        print("Range for other bytes must be at least 1 and less than 64")
        print(error)
        


#print(bytes(b'\xf0\x80\x90\x8f').decode("utf_8"))
#hexstring="f09f 908d" 
#print(output_utf8(bytes.fromhex(hexstring)))

#hexstring=byte_string_four_by_8bit(0xf0, 0x9f, 0x90, 0x8d)
#output_utf8(bytes.fromhex(hexstring))

#hexstring=byte_string_add_two_int(int(0xf0), 0x9f, 0x90, 0x8d)
#output_utf8(bytes.fromhex(hexstring))


#1111000010011111 1001000010001101
#hexstring=byte_string_two_by_16bit(0b1111000010011111, 0b1001000010001101)
#output_utf8(bytes.fromhex(hexstring))
#i=0, j=31, k=16, l=13 = 🐍
for i in range(0,1):
    for j in range(0,32): #Max 0,64
        if i == 0 and j < 16:  
            print("{}, {}".format(i,j))       
        elif i == 4 and j >= 16:
            print("{}, {}".format(i,j))              
        else:    
            for k in range(0,32): #Max 0,64
                for l in range(0,32):
                    print_by_offset(i, j, k, l) #


