from datetime import datetime  
import json


today = str(datetime.now())   

def logEntry (mxg,nameFile):
    
    with open(nameFile, 'a') as f:
        f.write("\n["+today+"] "+mxg)

def logRead (nameFile):
    a=""
    with open(nameFile, 'r') as f:
        a=f.read()
    a=a.replace("'", '"')
    return a

def startLogBookRecord(nameFile, startTime):
    logEntry(" *******************************************" , nameFile)  
    logEntry(" ***            STAR FOR TODAY            ***   " + str(today), nameFile)  
    logEntry(" *******************************************" , nameFile)  
    print("startTime : "+str(startTime))
    logEntry("startTime : "+str(startTime), nameFile)  

def endLogBookRecord(nameFile,totalTime):
    logEntry("Total Time : "+str(totalTime), nameFile)  
    logEntry(" ***            END FOR TODAY            ***   " + str(today), nameFile)  

     
def logEntrynodate (nameFile,mx): 
    with open(nameFile, 'a') as f:
        f.write("\n "+mx)

