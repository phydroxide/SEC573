import sys
import csv
import time
from test.libregrtest.utils import printlist
filename=sys.argv[1]

def namesFromList(field_tuple):
    return(field_tuple[1])

def printFields(field_tuple):
    print("{}: {}".format(field_tuple[0],field_tuple[1]))
    
def fileToDict(input_handler, startrow=0):
    for skipfirst in range(1,startrow,1):
        print("Dropping Row: {}".format(skipfirst)) 
        print("Containing: {}".format(next(input_handler))) 
        
    reader=csv.DictReader(input_handler)
    holddict=next(reader)
    fieldlist=list(enumerate(reader._fieldnames))
    maplist=list(map(printFields, fieldlist))
    print(maplist)

    print("Pick Which Columns From Above (1,2,3,5)")
    column_set=input("Specify * for All")
    nameslist=[]
    if column_set  == "*":
        nameslist=list(map(namesFromList,fieldlist))
        print(nameslist)
    else:
        nameslist=[]
        for index in column_set.split(","):
            nameslist.append(fieldlist[int(index)][1])
        print(nameslist)

    #    column_set=map(nameList)
   

 
    #print(type(fieldlist))
    #print(list(fieldlist))
    
   # printFields(0, "Plugin")
    
    #print(dir(reader))
    time.sleep(2)
    dictlist=[]
    dictlist.append(holddict)
    i=0
    for row in reader:
    
        i=i+1
        print(i)
        dictlist.append(row) 
        if i==1:
            break
    return(dictlist, nameslist)    
    
      
thisfile=input("Specify Filename:")
print(filename)
startrow=int(input("Start Row Number:"))
print(startrow)
with open(filename, "r") as input_handler: 
    
    ordered_dict,nameslist=fileToDict(input_handler,startrow)  
    print("{}".format(nameslist))
input_handler.close

with open("output.csv", "w") as output_handler:
    writer=csv.DictWriter(output_handler, nameslist)
    print(writer.fieldnames)
    for dictitem in ordered_dict:
        print(dir(dictitem))
        
output_handler.close()

