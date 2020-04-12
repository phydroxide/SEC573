import re
import time
import hashlib
from _ast import Try

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
#TODO Start Byte offset
#length 16129000000 slice 15875000000:
#and cleanup in yield

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


#Read in pattern to match and capture user's desires on where to start/end
#pattern_file="input/BedrockUserSettingsStorage"
#pattern_file="input/BedrockUserSettingsStorage.bin"
pattern_file="input/MineCraft"

with open(pattern_file, "rb") as input_handler:
    pattern=input_handler.read()

pattern_length=len(pattern)

while True:
    try:
        s_bytes=int(input("Match (number) of beginning bytes < {}:".format(pattern_length)))
        if s_bytes > pattern_length-1:
            print("Select beginning bytes leaving at least one to anchor at the end. Try Again.")
        elif s_bytes <= 0:
            print("Must Select at least one start byte. Try again.")
        else:
            break
    except:
        print("Invalid Input")
    

remain=pattern_length-s_bytes
while True:
    try:
        e_bytes=int(input("Match (number) of ending bytes <= {}:".format(remain)))
        if e_bytes > remain:
            print("Not Enough Bytes Left. Try Again.")
        elif e_bytes <=0:
            print("Must select some number of ending bytes. Try again.")
        else:
            break
    except:
        print("Invalid Input")
        
    
start_pattern=pattern[:s_bytes:]
end_index=int(pattern_length-e_bytes)
end_pattern=pattern[end_index::]

print("Searching for patterns starting \n{} and ending \n{}\n\n".format(start_pattern,end_pattern))
time.sleep(1)

#override for my minecraft data
end_pattern=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" #+end_pattern
#end_pattern=b".{39,80}" #+end_pattern

#Construct regular expression to search
re_expression=br''.join([start_pattern,br"..*",end_pattern]) #b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" #+end_pattern
print(re_expression)

#emptyhash=hashlib.md5()
#emptyhash.update(b"")
#empty_digest=str(emptyhash.hexdigest())
            
contents={}
#contents[empty_digest]=b""


#print(list(contents.items()))  
#time.sleep(3)


last_chunk=bytearray(br'')
print("Byte Builder zeroed out to length {}".format(len(last_chunk)))
buffer_limit=2*file_size

#imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/PS4/sdb27copy"
imagefile="input/MineCraft"
with open(imagefile, "rb") as image_handler:
    try: 
        for image_part in bufferedSample(image_handler, file_size):
            buffer_string=br''.join([last_chunk,image_part])
            new_length=len(buffer_string)
            #print("Total Byte Builder Length {}".format(new_length))
            #Show Start and End of current sample read
            #5243136        

            #start_list=[x.hex() for x in re.findall(b".",buffer_string[0:256:], re.DOTALL)]
            #for row in range(0,16):
            #    print(start_list[(row*16):(row+1)*16])
            #    
            #print("........")
        
            #One off troubleshooting adjustment for hex display alignment with linux dd
            #e.g (b".",buffer_string[-258::]
            #The file handle reader is eating my 0x0a newlines and the grid goes out of alignment.
            #Solve with re.DOTALL
            #stop_list=[x.hex() for x in re.findall(b".",buffer_string[-256::], re.DOTALL)]
            #for row in range(0,16):
            #    print(stop_list[(row*16):(row+1)*16])
             
            #print("Sample Chunks of lengths {} and {}".format(len(start_list),len(stop_list)))

            last_chunk=buffer_string
            if (new_length > buffer_limit):
                trunc_start=new_length-buffer_limit 
                print("length {} slice {}:".format(new_length,trunc_start))
                buffer_string=bytes(buffer_string[trunc_start::])
            
                #print(buffer_string)
            try:
                results=re.findall(br"".join([re_expression]), buffer_string, re.DOTALL)   
                print("Done {} \n {}".format(len(results),contents.keys()))
                #time.sleep(1)
                #Take results from this chunk and append to found dictionary
                for result in results:
                    hasher=hashlib.md5()
                    hasher.update(result)
                    result_hash=hasher.hexdigest()
                    contents[result_hash]=bytes(result)  
                for entry in contents.values():
                    print("Length {} | Type {} | ID {}".format(len(entry), type(entry), id(entry)))
                for hash_result,bytesfound in list(contents.items()):
                    with open("output/" + str(hash_result) + "", "wb") as output_handler:
                        output_handler.write(bytesfound)
                contents={}
                #contents[empty_digest]=b""           
            except (MemoryError) as e:
                #print("interrupted. Now will write file {}".format(e))
                #for entry in contents.values():
                #    print("Length {} | Type {} | ID {}".format(len(entry), type(entry), id(entry)))
                #for hash_result,bytesfound in list(contents.items()):
                #    with open("output/" + str(hash_result) + "", "wb") as output_handler:
                #        output_handler.write(bytesfound)
                contents={}
                contents[empty_digest]=b""
            except (KeyboardInterrupt):
                raise
            #finally:   
            #    print("Yay I stayed in the loop!")
    except KeyboardInterrupt:
        print("Interrupted, Cleaning Up")
        for entry in contents.values():
            print("interrupted. Now will write file {}".format(e))
            print("Length {} | Type {} | ID {}".format(len(entry), type(entry), id(entry)))
            for hash_result,bytesfound in list(contents.items()):
                with open("output/" + str(hash_result) + "", "wb") as output_handler:
                    output_handler.write(bytesfound)
                
        
#print(contents)
    
       

    