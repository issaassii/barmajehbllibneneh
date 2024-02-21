import sys
import os.path
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
regs = {"r0":"","r1":"","r2":"","r3":"","r4":"","r5":"","r6":"","r7":"","r8":"","r9":""}
definedVars = []
barmajehFlag = False
tejhizFlag = False
afterIzaFlag = False
lst = []
Lcounter = 0
fileFlag = False

if (len(sys.argv)>1):
    if (os.path.isfile(sys.argv[1])):
        if(sys.argv[1].endswith(".bbl")):
            filename = str(sys.argv[1])
            global assembFileName
            assembFileName = filename.split(".")[0]
            fileFlag = True
        else:
            print("File provided is not a BBL program")
    else:
        print("File provided does not exist")
else:
    print("No file provided")

def main():
    global afterIzaFlag
    global Lcounter
    global tejhizFlag
    global barmajehFlag
# check if commandline argument exists, get commandline argument
    file = open(filename,"r")
    if checkIndentation(filename):
        for line in file:
            exp = ""
            check = line.split()
            if line.strip():
                #check which section we are in
                if check[0] == "tejhez#" and len(check) == 1:
                    tejhizFlag = True
                    barmajehFlag = False
                elif check[0] == "barmajeh#" and len(check) == 1:
                    barmajehFlag = True
                    tejhizFlag = False
                    
                #if tejhiz, check if ra2m
                if tejhizFlag == True and  check[0]=="ra2m":
                        if AssigIntchecker(check):
                            exp+="mov "+setValue(check[1])+" ,#"+check[3]
                            definedVars.append(check[1])
                        if exp != "" :
                            lst.append(exp)
                #check if
                if tejhizFlag == True and check[0] in LETTERS:
                        if AssignVarChecker(check):
                            exp+="addi "+setValue(check[0])+" ,"+setValue(check[2])+" ,#0"
                        if exp != "" :
                            lst.append(exp)
                        
                if barmajehFlag == True and check[0] in LETTERS :
                        if checkAnd(check) and afterIzaFlag == False:
                            exp+="aand "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                        elif checkOrr(check)  and afterIzaFlag == False:
                            exp+="orr "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                        elif checkAnd(check) and afterIzaFlag == True:
                            exp+="L"+str(Lcounter)+": "
                            exp+="and "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                            Lcounter+=1
                        elif checkOrr(check)  and afterIzaFlag == True:
                            exp+="L"+str(Lcounter)+": "
                            exp+="orr "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                            Lcounter+=1
                        
                        if exp != "" :
                            lst.append(exp)
                    #check if iza statement
                if barmajehFlag == True and check[0] == "iza" and check[-1] == ":":
                        if checkIf(check):
                            if check[1] in definedVars and check[-2] in definedVars:
                                exp+="cmp "+setValue(check[1])+" ,"+setValue(check[-2])
                                lst.append(exp)
                                exp=""
                                exp+="beq "+" L"+str(Lcounter)   
                                lst.append(exp)                 
                                afterIzaFlag=True
        return lst
    else:
        raise ValueError("There is an error in your code")

def get_keys_by_value(dct, value):
    return [k for k, v in dct.items() if v == value]
      
         #set register value                           
def setValue(value):
   
    for key in regs:
        if regs[key] == value:
            return key
    for key in regs:
        if regs[key] == "":
            regs[key] = value
            return str(key)
    raise ValueError("All registers are full")

#syntax checking functions
def checkIf(arr):
    if len(arr) != 5:
        return False
    if arr[1] not in definedVars :
        return False
    if arr[2] != "=":
        return False
    if arr[3] not in definedVars:
        return False
    return True
    
def checkOrr(arr):
     if(len(arr)!= 5):
        return False
     if arr[0] not in LETTERS:
        return False
     if arr[2] not in definedVars  :
        return False
     if arr[1] != "=":
        return False
     if arr[3] != "|":
         return False
     if arr[4] not in definedVars:
         return False
        
     return True
        
def checkAnd(arr):
     if(len(arr)!= 5):
        return False
     if arr[0] not in LETTERS:
        return False
     if arr[2] not in definedVars  :
        return False
     if arr[1] != "=":
        return False
     if arr[3] != "&":
         return False
     if arr[4] not in definedVars:
         return False
        
     return True

def AssignVarChecker(arr):
    if(len(arr)!= 3):
        return False
    if arr[0] not in LETTERS:
        return False
    if arr[2] not in definedVars:
        return False
    if arr[1] != "=":
        return False
    return True

     
def AssigIntchecker(arr):
    if(len(arr)!= 4):
        return False
    if arr[0] != "ra2m":
        return False
    if arr[1] not in LETTERS:
        return False
    if arr[2] != "=":
        return False
    if not arr[3].isnumeric():
        return False
    return True

def countTabs(filename):
    file = open(filename,"r")
    TabList = [] 
    for line in file:
        counter = 0
        if line.strip():
            for i in line :
                if i != "\t":
                        TabList.append(counter)
                        break
                counter+=1
    return TabList

def checkIndentation(filename):
    lst = ["barmajeh#","tejhez#","iza"]
    indentation_lst = countTabs(filename)
    first_word_lst = getFirstWord(filename)
    stack = []
    for i in range(len(indentation_lst)-1):
        if first_word_lst[i] in lst and len(stack) == 0 :
                stack.append(first_word_lst[i])
        if first_word_lst[i] in lst and len(stack) != 0:
                return True

def getFirstWord(filename):
    file = open(filename,"r")
    lst = []
    for line in file:
        if line.strip():
            lst.append(line.split()[0])
    return lst
 
if (__name__ == "__main__"):
    if (fileFlag):
        Main = main()
        newFile = open(assembFileName+".s","w")
        for i in Main:
            newFile.write("\n")
            newFile.write(i)
        print("Success")