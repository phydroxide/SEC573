import time

myarray=bytearray(0)

#b'\xf0\x9f\x90\x8d' = 🐍
#b'\xf0\x9f\x84\x81' = Zero
for i in range(0xf0,0xf1): #e0... 
    for j in range(0x9f,0xA0):  #0x80 .. 0xC0
        for k in range(0x90,0x91):
            time.sleep(1)
            for l in range(0x8c,0x8f):
                myarray.append(i)
                myarray.append(j)
                myarray.append(k)
                myarray.append(l)
                print(myarray)
                print("{}{}{}{}: {},{},{},{}: {}".format(format(i,'b'), format(j, 'b'), format(k,'b'), format(l,'b'), int(i), int(j), int(k), int(l), myarray.decode('utf_8')))
                myarray=bytearray(0)