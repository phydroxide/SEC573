from __future__ import print_function
import pyWars
#import local_pyWars as pyWars
import codecs

def answer1(datasample):
    return datasample+5

def answer2(datasample):
    return codecs.decode(datasample, "rot13")

def answer3(datasample):
    return codecs.decode(datasample, 'base-64');

def answer4(datasample):
    return datasample.upper();

def answer5(datasample):
    return datasample.find("SANS");

def answer6(datasample):
    result=datasample[::-1]
    #result = "".join(datasample.reversed());
    return result;
def answer7(datasample):
    return datasample+datasample[::-1] +datasample 

def answer8(datasample):
    return(datasample[1] + datasample[4] +datasample[8])

def answer9(datasample):
    return "{}{}{}".format(datasample[-1], datasample[1:-1], datasample[0] );

def answer10(datasample):
    a=datasample
    b=a[:len(a)//2][::-1]
    c=a[len(a)//2:]
    return "{}{}".format(b,c)

def answer11(datasample):
    b=datasample
    for mychar in [['E','3'], ['A','4'], ['T','7'], ['S','5'], ['G','6']]:
        b=b.replace(mychar[0],mychar[1]);
    return b 

def answer12(datasample):
    b=datasample
    return b[2] 


def answer13(datasample):
    list=[]
    for i in range(1,datasample):
        list.append(i)	
    return list 

def answer14(datasample):
    return len(datasample) 

def answer15(datasample):
    split_list=datasample.split(",")
    print("{}".format(split_list)) 
    return split_list[9] 

def answer16(datasample):
    split_sample=datasample.split(":")
    password_parts=split_sample[1].split("$")
    salt=password_parts[2]
    return salt 

def answer17(datasample):
    print(datasample[1]);
    datasample.append("Pywars rocks")
    b=list(datasample)
    c=datasample
    print("DataSample Orig: {}".format(datasample))
    print("{}".format(datasample.append("Append Returns None")))
    print("DataSample New: {}".format(datasample))
    print("B copied: {}".format(b))
    print("C pointer: {}".format(c))
    return b 

def answer18(datasample):
    b=datasample
    return sum(b) 

def answer19(datasample):
    b=datasample.split(" ")
    print(b)
    c=map(int,b)
    print("B:{}".format(b))
    print("C:{}".format(c))
    return sum(c) 

def answer20(datasample):
    string="this python stuff really is fun"
    array=string.split(" ")
    print(array)
    newstring=datasample.join(array)
    return newstring 


def answer21(datasample):
    thislist=[]
    for i in range(0,1000,datasample): 
        if i:
          thislist.append(i)
    return thislist


def answer22(datasample):
    newstring=bytes.fromhex("".join(datasample))
    #newlist=list(map(int,datasample))
    #print("Newlist: {}".format(newlist))
    #charlist=map(chr(newlist))
    #print(charlist)
    
    return newstring.decode('utf-8') 

def answer23(datasample):
    newlist=[]
    for samples in datasample:
        for item in samples:
            if item not in newlist:
                newlist.append(item)
    #newlist.extend(datasample[0])
    #newlist.extend(datasample[1])
    print(newlist)
    return sorted(newlist) 

def answer24(datasample):
    b=datasample
    return sorted(b) 

def divisible(first,second):
    first=int(first)
    second=int(second)
    remainder=second%first
    print("Remainder: {}".format(remainder))
    if remainder: 
        return "{}".format("False")
    else:
        return "{}".format("True")
   

def answer25(datasample):
    list1=[]
    list2=[]
    for valuestring in datasample:
        newpair=valuestring.split(",")
        list1.append(newpair[0])
        list2.append(newpair[1])
        #print(list(zip(list1,list2)))
    truthlist=list(map(divisible,list1,list2))
    #print(truthlist)
    return truthlist 

def answer26(datasample):
    samplelist=datasample
    return list(map(type,samplelist))
 

def answer27(datasample):
    keys=datasample.keys()
    return sorted(keys)

def answer28(datasample):
    b=datasample.values()
    return sorted(b)
 
def answer29(datasample):
    #returnlist=[]
    #for b in datasample.keys():
    #    tupleb=(b,datasample[b])
    #    returnlist.append(tuple)
    #print(sorted(returnlist))
    
    return sorted(list(datasample.items()))



def answer30(datasample):
    b=int(datasample['python'])+int(datasample['rocks'])
    return b 

from collections import Counter

def answer31(datasample):
    b=datasample['6-2017']
    c=Counter()
    c.update(b)
    numerator=float(b['Vista'])
    valuelist=list(b.values())
    denominator=sum(list(map(float,valuelist)))
    print("{}: {}/{}".format(c,numerator,denominator))
    return (numerator)

def main():
    #print("#1", d.question(1), d.answer(1, answer1(d.data(1))))
    #print("#7", d.question(7), d.answer(7, answer1(d.data(7))))
    print("#12", d.question(12), d.answer12(12, answer1(d.data(12))))


if __name__ == "__main__":
    d = pyWars.exercise()
    d.login("phydroxide","UsefulId10t")
    main()
    d.logout()
