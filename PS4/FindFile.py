import re
import os
import time

global buffer_string
buffer_string=b""
buffer_size=1024

def bufferedSample(filehandle, size=512):
    while True:
        nextpart=filehandle.read(size)
        if not nextpart:
            break
        yield nextpart

     
with open("input/seq.hex", "rb") as input_handler:
    print("ready")
    for sample in bufferedSample(input_handler, 10):
        print(sample)
        print(dir(sample))
        print(type(sample))
        b"".join([buffer_string,sample])
        if (len(buffer_string) > buffer_size):
            chop_before=len(buffer_string)-buffer_size
            buffer_string=buffer_string[chop_before:buffer_size:]
        print("Length now {}".format(len(buffer_string)))

        
s_bytes=int(input("Match (number) of beginning bytes:"))
e_bytes=int(input("Match (number) of ending bytes:"))

with open("input/ABCD.txt", "rb") as input_handler:
    pattern=input_handler.read()

pat_len=int(len(pattern))

opening=pattern[:s_bytes:]
type(pat_len)
type(e_bytes)
begin=int(pat_len-e_bytes)
closing=pattern[begin::]
print("From {} to {}".format(opening,closing))
expression=opening+b".*"+closing
print( expression)        
        
contents=[]
with open("input/seq.hex", "rb") as image_handler:
    for sample in bufferedSample(image_handler, 10):
        print("{}:{}".format(expression,sample))
        contents.extend(re.findall(expression, sample, re.DOTALL ))   
        print(contents)
        time.sleep(1)
        print("{} entries found".format(len(contents)))

with open("output/message.txt", "wb") as output_handler:
    for bytesfound in contents:
        output_handler.write(bytesfound)
       

    