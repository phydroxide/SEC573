import gc
import os
import re
import hashlib

def deviceNibbler(nibblefile, start=0, length=3):
    with open(nibblefile, "rb") as nibble_handler:
        nibble_handler.seek(start)
        nibble=nibble_handler.read(length)
        #print("Reading at {} bytes of {}".format(start, os.fstat(nibble_handler.fileno()).st_size))
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

def findKeyFiles(imagefile):
    key_pattern=b'\x70\x66\x73\x53\x4b\x4b\x65\x79' #\x08'
    try: 
    #for image_part in bufferedSample(image_handler, file_size):
        for image_part in backNibbles(imagefile, 88*32768):
        #for image_part in backNibbles('output/a5a8d8be9e623dce510eb5b55d4a285e', 88):
            #print(len(image_part))
            for match in re.findall(key_pattern, image_part, re.DOTALL):
                print("found Something")
                result_hash=hashlib.md5(match).hexdigest()

                with open("keys/" + result_hash + ".bin", "wb") as key_handler:
                    key_handler.write(match)
    except e:
        print("Error {}".format(e))
        
        
#imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/dev/sdb27"
imagefile="/media/pwaters/56e05090-43ef-4899-826f-ccf168689305/dev/sdb27"

#imagefile="/media/pwaters/Expansion D/PS4/SAVEDATA/535c60e842394321.old/CUSA00744/BedrockWorldyTaBXlbQwQA@P3.bin"
findKeyFiles(imagefile)