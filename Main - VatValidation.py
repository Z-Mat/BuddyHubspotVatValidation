from API_Hubspot import *
from booklogging import *
#from API_VIES import *
from VIES_API import VIES_JM
from datetime import datetime  
import time


logbooktxtName = "logOFHubspor-vat-validation.txt"
today = str(datetime.now())  
startTime = time.perf_counter()
endTime= time.perf_counter()
totalTime = time.perf_counter()
count = 0
#4481388009

def validateVATonHubspotTest (thisCompany):
    vat = ""
    companyCountry = ""
    validatedRxp = ""
    idCompany=thisCompany 
    
    
    print("idCompany : "+idCompany)
    logEntry("idCompany : "+idCompany, logbooktxtName)  
    
    validatedRxp = str(getPropertiByCompanyID ("vat_validation",idCompany))
    print("validatedRxp : "+str(validatedRxp))
    validatedRxp = validatedRxp.upper().strip()
    print("vat_validation : ."+str(validatedRxp)+".") 
    logEntry("vat_validation : "+str(validatedRxp), logbooktxtName) 
    
    if validatedRxp not in ["VALID","NEU"]: # != "VALID": or vat_validation != "NEU": note: https://stackoverflow.com/questions/66642494/logical-operator-or-in-python-not-working-as-intended 
        vat = getPropertiByCompanyID ("cvr_vat_number",idCompany)
        companyCountry = str(getPropertiByCompanyID ("country",idCompany))
        
        print("companyCountry : "+companyCountry+" vat : "+str(vat))
        logEntry("vat : "+str(vat)+" companyCountry : "+companyCountry, logbooktxtName) 
                
        if vat not in ["",None,"None"]: #!= None and vat !="":
            print("entrei va tnot none")
            validatedRxp = VIES_JM.validateVat(vat, True).upper().strip()  
            print("validatedRxp : "+validatedRxp)
            logEntry("validatedRxp : "+validatedRxp, logbooktxtName)            
            if validatedRxp=="INVALID_INPUT":
               # companyCountry = getPropertiByCompanyID ("country",idCompany)
                print("enteu em if validatedRxp==INVALID_INPUT ")
                print("companyCountry : "+companyCountry+" iscountryEU"+ str(VIES_JM.iscountryEU(companyCountry)))
                if VIES_JM.iscountryEU(companyCountry):
                   print("enteu em if iscountryEU(companyCountry)") 
                   countrycode = VIES_JM.euCountryCode(companyCountry).upper().strip()
                   print("countrycode : "+ countrycode)
                   tempVat = countrycode+vat
                   tempvalidatedRxp = VIES_JM.validateVat(tempVat, True).upper().strip()
                   print("tempVat : "+tempVat)
                   print("tempvalidatedRxp : "+str(tempvalidatedRxp))
                   if tempvalidatedRxp.upper().strip() == "VALID":
                    print("entrei no update")
                    updateCompanyById ( "cvr_vat_number", idCompany, tempVat)
                    validatedRxp=tempvalidatedRxp
                    print("update with tempvat : "+tempVat+"and validatedRXP == "+ tempvalidatedRxp)
                else:
                    validatedRxp="NEU"
            print("update vat_validation with : "+ validatedRxp)
            updateCompanyById ( "vat_validation", idCompany, validatedRxp)
            updateCompanyById ( "vat_validation_date", idCompany, today) 
        else:#IF VAT NONE 
            
            print("IsItEU? : " + str(VIES_JM.iscountryEU(companyCountry)))  
                  
            if not VIES_JM.iscountryEU(companyCountry):
                validatedRxp = "NEU"
            else:
                validatedRxp = "No call - Vat null"
  
            updateCompanyById ( "vat_validation", idCompany, validatedRxp)          
            updateCompanyById ( "vat_validation_date", idCompany, today)
            print("update : "+ validatedRxp)
            logEntry("update : " +validatedRxp, logbooktxtName) 
    else:
        print("No call - VALID")
        logEntry("No call - VALID", logbooktxtName) 
   
    print("END")
    logEntry("END", logbooktxtName) 
    
  
    print("\n")
    logEntry("", logbooktxtName) 
    
    

startLogBookRecord(logbooktxtName, startTime)
#companyList = listAllIdCompanies("0")
companyList = listAllIdCompanies("4481388009")

for i in companyList:
    count=count+1
    thisCompany=str(i)        
    print("count : " + str(count))
    logEntry("count : " + str(count), logbooktxtName) 
    logEntry("Time : "+str(time.perf_counter()), logbooktxtName)         
    validateVATonHubspotTest(thisCompany)

endTime= time.perf_counter()
totalTime = endTime - startTime
print("startTime : "+str(startTime))
print("endTime : "+str(endTime))
print("totalTime : "+str(totalTime))
    
endLogBookRecord(logbooktxtName,totalTime)
    
#updateCompanyById ( "vat_validation", "9056008673", "")

# validateVATonHubspotTest("9056008673")