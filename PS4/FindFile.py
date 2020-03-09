import re
import time
import hashlib
from collections import defaultdict

#Yield Generator to iterate over file reading small chunks
def bufferedSample(filehandle, size=512):
    while True:
        nextpart=filehandle.read(size)
        if not nextpart:
            break
        yield nextpart

while True: 
    try:
        file_size=int(input("How big is the file you're looking for?"))
        break
    except:
        print("Expecting Integer Number")

#while True: 
#    try:
#        read_slice=int(input("Read file in increments of how many bytes?"))
#        break
#    except:
#        print("Expecting Integer Number")
        

#if file_size<read_slice:
#   buffer_limit=read_slice+file_size
#else:
#   buffer_limit=file_size

buffer_limit=2*file_size

#Read in pattern to match and capture user's desires on where to start/end
with open("input/LMNOPQR_S.txt", "rb") as input_handler:
    pattern=input_handler.read()

pattern_length=len(pattern)

while True:
    s_bytes=int(input("Match (number) of beginning bytes < {}:".format(pattern_length)))
    if s_bytes > pattern_length-1:
        print("Select beginning bytes leaving at least one to anchor at the end. Try Again.")
    elif s_bytes <= 0:
        print("Must Select at least one start byte. Try again.")
    else:
        break
    

remain=pattern_length-s_bytes
while True:
    e_bytes=int(input("Match (number) of ending bytes <= {}:".format(remain)))
    if e_bytes > remain:
        print("Not Enough Bytes Left. Try Again.")
    elif e_bytes <=0:
        print("Must select some number of ending bytes. Try again.")
    else:
        break

start_pattern=pattern[:s_bytes:]
end_index=int(pattern_length-e_bytes)
end_pattern=pattern[end_index::]

print("Searching for patterns starting {} and ending {}".format(start_pattern,end_pattern))
time.sleep(1)


#Construct regular expression to search
expression=start_pattern+b".*"+end_pattern
print( expression)        

#emptyhash=hashlib.md5()
#emptyhash.update(b"")
#empty_digest=str(emptyhash.hexdigest())
            
contents={}
#contents[empty_digest]=b""
last_chunk=b''
 
with open("input/seq.hex", "rb") as image_handler:
    for image_part in bufferedSample(image_handler, file_size):
        buffer_string=b"".join([last_chunk,image_part])
        new_length=len(buffer_string)
        trunc_start=new_length-buffer_limit
        last_chunk=buffer_string
        if (new_length > buffer_limit):
            buffer_string=bytes(buffer_string[trunc_start::])
       
        results=re.findall(expression, buffer_string, re.DOTALL)
        
        #Take results from this chunk and append to found dictionary
        for result in results:
            print(result)
            hasher=hashlib.md5()
            hasher.update(result)
            result_hash=hasher.hexdigest()
            contents[result_hash]=bytes(result)         
    
print(contents)
for entry in contents.values():
    print("{}:{}:{}".format(entry, type(entry), id(entry)))
        
print(contents.values())
for index,bytesfound in enumerate(contents.values()):
    with open("output/message" + str(index) +".txt", "wb") as output_handler:
        output_handler.write(bytesfound)
       

    