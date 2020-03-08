import re
import os
s_bytes=4 #int(input("Match (number) of beginning bytes:"))
e_bytes=4 #int(input("Match (number) of ending bytes:"))

with open("input/pattern.txt", "rb") as input_handler:
    pattern=input_handler.read()

pat_len=int(len(pattern))
opening=pattern[:s_bytes:]
type(pat_len)
type(e_bytes)
begin=int(pat_len-e_bytes)
closing=pattern[begin::]
print("From {} to {}".format(opening,closing))
        
with open("input/image.raw", "rb") as input_handler:
    image=input_handler.read() 
    
contents=re.findall(opening + b".*" + closing, image)   
   
print(contents)
    