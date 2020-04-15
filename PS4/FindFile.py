import re
import hashlib
import gc
import os
import struct
import io
# Philip Waters
# Carves encrypted minecraft save data from PS4
# Does not find key data unless it is from a key exported during saved data management

#Yield Generator to iterate over file reading small chunks
def bufferedSample(filehandle, size=32768):
    while True:
        nextpart=filehandle.read(size)
        if not nextpart:
            break
        yield nextpart
        
def deviceNibbler(nibblefile, start=0, length=96):
    with open(nibblefile, "rb") as nibble_handler:
        nibble_handler.seek(start)
        nibble=nibble_handler.read(length)
    gc.collect()
    return nibble
   
def backNibbles(nibblefile, windowsize=10, skipbyte=0):
    start_counter=skipbyte
    buffer_length=windowsize*2
    
    with open(nibblefile, "rb") as size_checker:
        file_length=os.fstat(size_checker.fileno()).st_size    
    
    while start_counter < file_length:
        nibble_buffer=deviceNibbler(nibblefile, start_counter, buffer_length)
        start_counter=start_counter+windowsize
        #gc.collect()
        yield(nibble_buffer)

#Trim Files to size
def trimBytes(byte_string, size):
    f=io.BytesIO(byte_string)
    return f.read(size)
        
def findKeyFiles(imagefile='input/BedrockLevelInfoCache.bin'):
    key_pattern=b'\x70\x66\x73\x53\x4b\x4b\x65\x79\x08.{79}'
    try: 
    #for image_part in bufferedSample(image_handler, file_size):
        for image_part in backNibbles(imagefile, 8*32768):
        #for image_part in backNibbles('output/a5a8d8be9e623dce510eb5b55d4a285e', 88):
            for match in re.findall(key_pattern, image_part, re.DOTALL):
                print("found Something")
                result_hash=hashlib.md5(match).hexdigest()

                with open(result_hash + ".bin", "wb") as key_handler:
                    key_handler.write(match)    
    except:
        print("error")
        
def debugOutput(buffer_string):
    start_list=[x.hex() for x in re.findall(b".",buffer_string[0:256:], re.DOTALL)]
    for row in range(0,16):
                print(start_list[(row*16):(row+1)*16])
                
    print("........")
    #One off troubleshooting adjustment for hex display alignment with linux dd
    #e.g (b".",buffer_string[-258::]
    #The file handle reader is eating my 0x0a newlines and the grid goes out of alignment.
    #Solve with re.DOTALL
    stop_list=[x.hex() for x in re.findall(b".",buffer_string[-256::], re.DOTALL)]
    for row in range(0,16):
        print(stop_list[(row*16):(row+1)*16])
        
imagefile="input/MineCraft"
#imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/dev/sdb27"       
#imagefile="input/BedRockTest"

#file_size_in_mb=115 #(5,30,60,90...)
#bytes_per_part=32
#sizecode=hex(file_size_in_mb*bytes_per_part)

#Some examples of files I found. 
#be00 = 48640 * 32768 = 1593835520 = 1.5GB  1520
#bd04 = 48388 * 32768 = 1585577984 =1.5 GB 1512
#0e43 = 3651 * 32768 = 115MB
#0b40 = 2880 / 90 = 32 = 43 mb
#0562  = 1378 * 32768 = 45154304
#0870 = 1920 / 60 = 32
#03c0 = 960 / 30 = 32
#00be = 190 * 32768 = 6225920, 6 MB
#00a0 = 160 / 5 = 32
#0008 = 8*32768 = 262144

#Maximum Size we're looking for.
sizecode=hex(63004)
print("Maximum Size Code that can be found is {}".format(sizecode))
bytes_per_block=32*1024
max_size=int(sizecode,16)*bytes_per_block

#16-byte lines are appended together for for flexible alteration of match pattern.
#Where I have found files that are discrepancies from normal, I replace \xBB with .
#We'll add .* to the end, Join the string together, and pop .* off so we can use it later if we need.
#We have a dependency on index 0030 (line 4) because there is a match pattern group that holds the size. 
minecraft_dump=[]

#LINE1
minecraft_dump.append(b''.join([b'\x01\x00\x00\x00\x00\x00\x00\x00\x0b',b'.',b'\x33\x01\x00\x00\x00\x00'])) 
#\x2a is failing to be treated properly by re. Bug?
######################(b'\x01\x00\x00\x00\x00\x00\x00\x00\x0b\x2a\x33\x01\x00\x00\x00\x00') 

#LINE2
#minecraft_dump.append(b''.join([b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',b'.',b'\x00\x0d\x00\x00\x00'])) 
#Bigger file ends 000001000d000000, smaller file 000000000d000000
#####################(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0d\x00\x00\x00')
#Make it more generic 
minecraft_dump.append(b''.join([b'.{16}'])) 

#LINE3
#minecraft_dump.append(b''.join([b'\x00',b'.',b'.',b'\x00',b'.',b'\x00\x00\x00',b'\x01\x00\x00\x00\x00\x00\x00\x00'])) 
#Older file starts 0080000001 new file starts 000010000
#######################(b'\x00\x80\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
#Make it more Generic
minecraft_dump.append(b''.join([b'.{16}'])) 


#LINE4
#minecraft_dump.append(b''.join([b'.',b'.',b'\x00\x00\x00\x00\x00\x00',b'(..)',b'\x00\x00\x00\x00\x00\x00'])) 
#This line contains the file size indicator, also may begin 0004 or 4000
#######################(b''.join([b'\x00\x04\x00\x00\x00\x00\x00\x00',b'..',b'.',b'\x00\x00\x00\x00\x00']))
#Make it more Generic
minecraft_dump.append(b''.join([b'.{8}(..).{6}'])) 


#LINE5
#minecraft_dump.append(b''.join([b'.',b'.',b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'])) 
# bigger file begins 0001, smaller file begins 0017 the rest are zeros, 
#but all following lines differ enormously between big/small though small/small and big/big have similarities
#######################(b'\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

#LINE6
##minecraft_dump.append(b'\x00\x00\x01\x00\x1e\x00\x01\x00')
#minecraft_dump.append(b''.join([b'\x00\x00\x01\x00',b'.',b'\x00', b'.', b'\x00']))
#######################minecraft_dump.append(b'\x00\x00\x01\x00\x1e\x00\x01\x00')
#minecraft_dump.append(b''.join([b'.{', bytes(suffix_length), b'}']))

minecraft_dump.append(b'.*')

minecraft_pattern=b''.join(minecraft_dump)      

#Remove greedy glob in case we want to use the pattern basis later
del(minecraft_dump[-1])

#Minimum Size needed to match the entire file of a data slice that overlaps is filesize*2 - 1 byte. 
#I'll eat one byte for the doubt and simplicity. We'll use ByteIO to trim it down later 
#as the ending match pattern is non-deterministic, but the file size code is reliable. 
buffer_limit=2*max_size

results=[];
result_hash=b'';
try: 
    for image_part in backNibbles(imagefile, buffer_limit):
        try:
            result=re.search(minecraft_pattern, image_part, re.DOTALL)   
            #Take results from this chunk and write a file
            if result: 
                print("Found something")
                
                #Extract File Size from the capture group
                fsize=int(struct.unpack('<h',result.group(1))[0])
                result_size=fsize*32*1024
                print("File Claims it should be {}, but I have {} bytes".format(result_size, len(result.group(0))))              
                
                #Trim the file to size
                trimmed_file=trimBytes(result.group(0),result_size)
                #Let's save the file according to the hash of the data we want to keep
                result_hash=hashlib.md5(trimmed_file).hexdigest()
                
                #I'm collecting garbage all the time
                #I confess I don't know how often I need to
                #Previous versions had memory issues. The execution cost appears minimal
                #And I need all the memory I can get when I output the files. 

                gc.collect()
                with open("output/" + str(result_hash) + "", "wb") as output_handler:
                    output_handler.write(trimmed_file)
                #gc.collect()
                
                           
        except (MemoryError) as e:
            print(e)
                
        except (KeyboardInterrupt):
            raise
        finally:   
            print("New Image Part. Garbage Collection")
            gc.collect()
except KeyboardInterrupt:    
    for result in results:
        with open("output/" + str(result_hash) + "", "wb") as output_handler:
            output_handler.write(trimmed_file)
    
                
        

       

    