from API_Hubspot import *
from booklogging import *
from API_VIES import *
from datetime import datetime  
import time



today = str(datetime.now())  
startTime = time.perf_counter()
endTime= time.perf_counter()
totalTime = time.perf_counter()
count = 0
#9056008673
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
            validatedRxp = validateVat(vat, True).upper().strip()  
            print("validatedRxp : "+validatedRxp)
            logEntry("validatedRxp : "+validatedRxp, logbooktxtName)            
            if validatedRxp=="INVALID_INPUT":
               # companyCountry = getPropertiByCompanyID ("country",idCompany)
                print("enteu em if validatedRxp==INVALID_INPUT ")
                print("companyCountry : "+companyCountry+" iscountryEU"+ str(iscountryEU(companyCountry)))
                if iscountryEU(companyCountry):
                   print("enteu em if iscountryEU(companyCountry)") 
                   countrycode = euCountryCode(companyCountry).upper().strip()
                   print("countrycode : "+ countrycode)
                   tempVat = countrycode+vat
                   tempvalidatedRxp = validateVat(tempVat, True).upper().strip()
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
            
            print("IsItEU? : " + str(iscountryEU(companyCountry)))  
                  
            if not iscountryEU(companyCountry):
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
    
    

 
validateVATonHubspotTest("18426264595")

