import re
import hashlib
import gc
import os
import struct
import io

#Open Sample File
#Open Device 
#Find instance where file begins
#Find File Size
#Start from beginning and grab file of size x
#Write file with Hash name
#Look above and below for pfskey




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
        gc.collect()
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
        
#imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/dev/sdb27"       
#imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/PS4/sdb27copy"
imagefile="input/MineCraft"
#imagefile="input/BedRockTest"
#imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/PS4/sdb7copy"

#file_size_in_mb=115 #(5,30,60,90...)
#bytes_per_part=32
#sizecode=hex(file_size_in_mb*bytes_per_part)

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

sizecode=hex(63004)
print(sizecode)
bytes_per_block=32*1024
file_size=int(sizecode,16)*bytes_per_block



#TODO - Why does the block device not always match on more than one row of bytes
#Comment out later lines for less specificity
minecraft_dump=[]

minecraft_dump.append(b''.join([b'\x01\x00\x00\x00\x00\x00\x00\x00\x0b',b'.',b'\x33\x01\x00\x00\x00\x00'])) 
#\x2a is failing to be treated properly by re
######################(b'\x01\x00\x00\x00\x00\x00\x00\x00\x0b\x2a\x33\x01\x00\x00\x00\x00') 

minecraft_dump.append(b''.join([b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',b'.',b'\x00\x0d\x00\x00\x00'])) 
#Bigger file ends 000001000d000000, smaller file 000000000d000000
#####################(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0d\x00\x00\x00')

minecraft_dump.append(b''.join([b'\x00',b'.',b'.',b'\x00',b'.',b'\x00\x00\x00',b'\x01\x00\x00\x00\x00\x00\x00\x00'])) 
#Older file starts 0080000001 new file starts 000010000
#######################(b'\x00\x80\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')

minecraft_dump.append(b''.join([b'.',b'.',b'\x00\x00\x00\x00\x00\x00',b'(..)',b'\x00\x00\x00\x00\x00\x00'])) 
#This line contains the file size indicator, also may begin 0004 or 4000
#######################(b''.join([b'\x00\x04\x00\x00\x00\x00\x00\x00',b'..',b'.',b'\x00\x00\x00\x00\x00']))

minecraft_dump.append(b''.join([b'.',b'.',b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'])) 
# bigger file begins 0001, smaller file begins 0017 the rest are zeros, 
#but all following lines differ enormously between big/small though small/small and big/big have similarities
#######################(b'\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

##minecraft_dump.append(b'\x00\x00\x01\x00\x1e\x00\x01\x00')
minecraft_dump.append(b''.join([b'\x00\x00\x01\x00',b'.',b'\x00', b'.', b'\x00']))
#######################minecraft_dump.append(b'\x00\x00\x01\x00\x1e\x00\x01\x00')
#minecraft_dump.append(b''.join([b'.{', bytes(suffix_length), b'}']))

minecraft_dump.append(b'.*')

minecraft_pattern=b''.join(minecraft_dump)      

#Remove greedy glob in case we want to use the pattern basis later
del(minecraft_dump[-1])

buffer_limit=2*file_size

results=[];
result_hash=b'';
try: 
    #for image_part in bufferedSample(image_handler, file_size):
    for image_part in backNibbles(imagefile, buffer_limit):
        try:
            result=re.search(minecraft_pattern, image_part, re.DOTALL)   
            #Take results from this chunk and write a file
            if result: 
                print("found something")
                
                #Extract File Size from the capture group
                fsize=int(struct.unpack('<h',result.group(1))[0])
                print("File Claims it should be {}, but I have {} bytes".format(fsize*32768, len(result.group(0))))              
                
                print("{}{}".format(dir(result), type(result.groups())))
                result_hash=hashlib.md5(result.group(0)).hexdigest()

                gc.collect()
                with open("output/" + str(result_hash) + "", "wb") as output_handler:
                    output_handler.write(trimBytes(bytes(result.group(0)), fsize*32768))
                gc.collect()
                
                           
        except (MemoryError) as e:
            gc.collect()
            print("trying to write file, no promises though")
            with open("output/partialresult", "wb") as output_handler:
                output_handler.write(results[0])
            print(e)
                
        except (KeyboardInterrupt):
            raise
        finally:   
            print("Garbage Collection")
            gc.collect()
except KeyboardInterrupt:
        #print("Interrupted, Cleaning Up")
        #print("Length {} | Type {} | ID {}".format(len(results), type(results), id(results)))
    for result in results:
        with open("output/" + str(result_hash) + "", "wb") as output_handler:
            output_handler.write(result)
    
                
        

       

    