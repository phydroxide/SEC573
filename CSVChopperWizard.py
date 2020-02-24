import sys
import csv
import os
import errno
import time




def mapOwners():
#Owner Map Function. File containing name mapping should be in directory as a parent to input
    #Open ownermap file
    with open("ownermap.csv", "r") as input_handler:     
        reader=csv.reader(input_handler, skipinitialspace=True, delimiter=',', quotechar='"')
        global ownermap_dict
        ownermap_dict={}
        for line in reader:
            #Convert into dictionary entry ownermap[col_1_owner]=col_2_email. Zero-based list
            ownermap_dict[line[0]]=line[1]
        input_handler.close
      
def namesFromList(field_tuple):
#The column needed paired with the value of that column. 
    #Mapping this function gives me just a list of column names
    return(field_tuple[1])

def printFields(field_tuple):
#Print a list of all the columns for a menu.
    #print("{}: {}".format(field_tuple[0],field_tuple[1]))
    return("{}: {}".format(field_tuple[0],field_tuple[1]))
    
def fileToDict(input_handler, startrow=0, which_columns=""):
#Read the file into a python dictionary following SCS Compliance rules Kjirsten gave.  
#File to Dict takes an input handler and the row to start on. 
#It returns a list of dictionaries and another of fields
    
    #https://confluence.rightnowtech.com/display/SaaSComp/Vulnerability+Management+Tooling+-+ORCA
    #Remove
    #3 D: NetBIOS 
    #4 E: Tracking Method
    #6 G: IP Status
    #13 N: Protocol
    #14 O: FQDN
    #15 P: SSL
    #22 W: Bugtraq ID
    #24 Y: CVSS Base
    #25 Z: CVSS Temporal
    #29 AD: CVSS3 Base
    #30 AE: CVSS3 Temporal
    #36 AK: Ticket State
    #37 AL: Instance
    
    #Inject column at the end:
    #Owner
    
    #Skip lines until the line specified
    for skipfirst in range(1,startrow,1):
        print("Dropping Row: {}".format(skipfirst)) 
        contents=next(input_handler)
        #print("Containing: {}\n".format(contents)) 
    time.sleep(1)    
    
    #We have to read the first row to get the headers    
    reader=csv.DictReader(input_handler, skipinitialspace=True)
 
    #So hold onto this first row
    holddict=next(reader)
    owner=holddict["Asset Short Name"]
    holddict.update({'Owner':ownermap_dict[holddict["Asset Short Name"]]})

    
    #Now Read the fields and print a menu
    fieldlist=list(enumerate(reader._fieldnames))
    maplist=list(map(printFields, fieldlist))
    
    #If user didn't specify columns on the command line, prompt and set with user input.     
    if not which_columns:
        for item in maplist:
            print(item)
        print("Pick Which Columns From Above (e.g. 1,2,3,5).")
        column_set=input("Specify * for All, 'default' for ORCA2020 format: ")
    #If they did specify columns by a keyword, 
    #prepare to expand by temporarily setting columns to the same value
    elif which_columns=="default":
        column_set="default"
    #If they did pass the values take them as is. 
    else:
        column_set=which_columns    
 
    #Now expand the values for any special keyword if any
    if column_set=="default" or  column_set =="":
        column_set="0,1,2,5,7,8,9,10,11,12,16,17,18,19,20,21,23,26,27,28,31,32,33,34,35,38"
       
    #The names list contains the string values of the dictionary keys
    nameslist=[]
    
    #If the user just said everything, we have to expand that for them.
    #We just use what was read in, but also append the owner column for the header.
    if column_set  == "*":
        nameslist=list(map(namesFromList,fieldlist))
        nameslist.append('Owner')
        print("Using All Columns:\n {}\n".format(nameslist))
    #If not everything, we have to go through and pick out specific ones.
    #Use the index they specified to create the list of friendly names
    #Again set the Owner column because the header list has been reset, 
    #Also, owner belongs at the end.
    else:
        nameslist=[]
        for index in column_set.split(","):
            nameslist.append(fieldlist[int(index)][1])
        nameslist.append('Owner')

        print("Using Columns:\n {}\n".format(nameslist))
        time.sleep(1)
        
    #Prepare to return the list of dictionary rows
    dictlist=[]
    dictlist.append(holddict)
    
    #Build the list. Use an iterator if you want to stop in the middle
    #i=0  
    for row in reader:
        owner=row["Asset Short Name"]
        ownerEmail=ownermap_dict[owner]
        row.update({'Owner':ownerEmail})
        dictlist.append(row) 
    return(dictlist, nameslist)    

def autowrite(): 
    
    directory=os.getcwd()
    indir=directory + "/input"
    outdir=directory + "/output"
    
    #Let's be nice and drop an empty dir here to coach the user
    if not os.path.exists(indir):
        try:
            print("You Forgot to create an ./input directory to hold your .csv files!")
            os.makedirs(indir)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    for infile in os.listdir(indir):
        ordered_dict,nameslist=({},[])
        if infile.endswith(".csv"):
            print("Now Reading {}.\n".format(infile))
            time.sleep(1)
            print("Using ORCA Defaults to prepare file.\n")
            time.sleep(1)

            with open(indir + "/" + infile, "r") as input_handler:     
                ordered_dict,nameslist=fileToDict(input_handler,19,"default")  
            input_handler.close

            outfile = outdir + "/" + infile 

            if not os.path.exists(os.path.dirname(outfile)):
                try:
                    os.makedirs(os.path.dirname(outfile))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            
            print("Writing file {}.\n".format(outfile))
            with open(outfile, "w", newline='\n', encoding='utf-8') as output_handler:
                writer=csv.DictWriter(output_handler, nameslist,extrasaction="ignore")
                writer.writeheader()
                for dictitem in ordered_dict:
                    writer.writerow(dictitem)
            time.sleep(1)
            
#BEGIN MAIN   
def interactive(file_passed, start_row, field_string):
    filename=""
    print 
    try:
        filename=file_passed
    except: 
        print("Error no file passed")
    
    if not filename:
        print("You can specify a filename on the commandline: {} file.csv".format(sys.argv[0]))

    print("File from Command Line: {}".format(filename))    
    if not filename:   
        filename=input("Specify Filename: ")
        print("File Specified: {}".format(filename)) 
    if not start_row:   
        startrowuser=int(input("Start Row Number: "))
        start_row=startrowuser
    print(start_row)
    
        
 
    with open(filename, "r") as input_handler:     
        ordered_dict,nameslist=fileToDict(input_handler,start_row,field_string)  
    input_handler.close
    
    out_filename=os.getcwd() + "/output/" + filename
    if not os.path.exists(os.path.dirname(out_filename)):
        try:
            os.makedirs(os.path.dirname(out_filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(out_filename, "w", newline='\n', encoding='utf-8') as output_handler:
        writer=csv.DictWriter(output_handler, nameslist,extrasaction="ignore")
        writer.writeheader()
        for dictitem in ordered_dict:
            writer.writerow(dictitem)
        
    output_handler.close()
    
if __name__ == "__main__":
    check_auto=""
    fields=""
    row_start=0
    
    #Prepare Owner to Email Mapping
    mapOwners()


    try:
        check_auto=sys.argv[1]
    except: 
        print("Required Option 1 Missing. (Filename or '-auto')")
        
    if len(sys.argv) > 2:
        try:
            row_start=sys.argv[2]
        except: 
            print("Optional Option 2 Missing. (Begin row X)")
        
    if len(sys.argv) > 3:    
        try:
            fields=sys.argv[3]
        except: 
            print("Optional Option 3 Missing. (List of fields, e.g. 1,2,3,4,10)")    
        
  
    if check_auto == "-auto":
        autowrite()
    else:
        filename=check_auto
        interactive(filename, int(row_start), fields)
    

