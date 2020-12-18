def is_perfect_cube(number):
    number=abs(number)
    result=format(round(number ** (1/3)) ** 3, '.12g')
    if (str(number)==str(result)): 
        return True
    else:
        return False

for i in range(1,52):
    row=""
    for j in range(1,52):
        if(is_perfect_cube(i*j)):
            row=row+"{0:>5}".format("*"+str(i*j))
            #print(str(row))
            #row=" "*(len(row))
            #row=""
        else:
            row=row+"{0:>5}".format(i*j)
    print(str(row))
