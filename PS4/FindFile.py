import re
import os
s_bytes=2 #int(input("Match (number) of beginning bytes:"))
e_bytes=2 #int(input("Match (number) of ending bytes:"))

with open("input/photo.jpg", "rb") as input_handler:
    pattern=input_handler.read()

pat_len=int(len(pattern))
opening=pattern[:s_bytes:]
type(pat_len)
type(e_bytes)
begin=int(pat_len-e_bytes)
closing=pattern[begin::]
print("From {} to {}".format(opening,closing))
        
with open("input/image2.raw", "rb") as input_handler:
    image=input_handler.read() 
    
expression=opening+b"..*"+closing
print(expression)
contents=re.findall(expression, image, re.DOTALL )   
print(contents)
with open("output/photo.jpg", "wb") as output_handler:
    for bytesfound in contents:
        output_handler.write(bytesfound)
       

    