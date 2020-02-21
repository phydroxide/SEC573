import sys
import csv

   
def namesFromList(field_tuple):
    return(field_tuple[1])

def printFields(field_tuple):
    print("{}: {}".format(field_tuple[0],field_tuple[1]))
    
def fileToDict(input_handler, startrow=0):
    #File to Dict takes an input handler and the row to start on. 
    #It returns a list of dictionaries and another of fields
    
    #Skip lines until the line specified
    for skipfirst in range(1,startrow,1):
        print("Dropping Row: {}".format(skipfirst)) 
        print("Containing: {}".format(next(input_handler))) 
    
    
    #We have to read the first row to get the headers    
    reader=csv.DictReader(input_handler)
    #So hold onto this first row
    holddict=next(reader)
    
    #Now Read the fields and print a menu
    fieldlist=list(enumerate(reader._fieldnames))
    maplist=list(map(printFields, fieldlist))
    print(maplist)

    print("Pick Which Columns From Above (e.g. 1,2,3,5).")
    column_set=input("Specify * for All: ")
    
    #The names list contains the string values of the dictionary keys
    nameslist=[]
    if column_set  == "*":
        nameslist=list(map(namesFromList,fieldlist))
        print(nameslist)
    else:
        nameslist=[]
        for index in column_set.split(","):
            nameslist.append(fieldlist[int(index)][1])
        print(nameslist)
        
    #Prepare to return the list of dictionary rows
    dictlist=[]
    dictlist.append(holddict)
    
    #Build the list. Use an iterator if you want to stop in the middle
    #i=0  
    for row in reader:
        #i=i+1
        #print(i)
        dictlist.append(row) 
        #if i==1:
        #    break
    return(dictlist, nameslist)    
    

#BEGIN MAIN   
filename=""
try:
    filename=sys.argv[1]
except: 
    print("You can specify a filename on the commandline: {} file.csv".format(sys.argv[0]))

print("File from Command Line: {}".format(filename))    
if not filename:   
    filename=input("Specify Filename: ")
    print("File Specified: {}".format(filename))    




startrow=int(input("Start Row Number: "))
print(startrow)

with open(filename, "r") as input_handler:     
    ordered_dict,nameslist=fileToDict(input_handler,startrow)  
input_handler.close

with open("output.csv", "w", newline='\n', encoding='utf-8') as output_handler:
    writer=csv.DictWriter(output_handler, nameslist,extrasaction="ignore")
    writer.writeheader()
    for dictitem in ordered_dict:
        writer.writerow(dictitem)
        
output_handler.close()

