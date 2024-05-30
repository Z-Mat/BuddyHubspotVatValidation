
import http.client
import json
import re
from time import sleep
from booklogging import *

logbooktxtName = "logbook.txt"
EuCOuntriesDict = { 
    "austria":"AT",
   "belgium":"BE", 
   "bulgaria":"BG", 
   "croatia":"HR",
   "republic of cyprus" :"CY", "cyprus":"CY",
   "czech republic":"CZ", "czechia":"CZ",
   "denmark":"DK", 
   "estonia":"EE", 
   "finland":"FI", 
   "france":"FR", 
   "germany":"DE", 
   "greece":"EL", 
   "hungary":"HU", 
   "ireland":"IE", 
   "italy":"IT", 
   "latvia":"LV", 
   "lithuania":"LT", 
   "luxembourg":"LU", 
   "malta":"MT", 
   "netherlands":"NL",
   "poland":"PL", 
   "portugal":"PT", 
   "romania":"RO", 
   "slovakia":"SK", 
   "slovenia":"SL", 
   "spain":"ES",
   "sweden":"SE",
   "northen ireland":"XI"
}


def iscountryEU(country):
    mycompanyCountry = country.strip().lower()
    if mycompanyCountry in EuCOuntriesDict:
        return True
    else:
        return False
    
def euCountryCode(country):
    mycountry=country.strip().lower()
    if iscountryEU(mycountry):
        return EuCOuntriesDict[mycountry]
    else:
        return False

def validateVat (aVat, controlTextOn):
#  logEntry( "\n", logbooktxtName) 
  print("Estou em validateVAT form API_VIES this is avat : "+ str(aVat))
  logEntry( "--> validateVat : " + str(aVat) , logbooktxtName)
  if not aVat:
    logEntry( "------> END : " + "Vat was null = "+ str(aVat) +". Did not call VIES.", logbooktxtName)
    return "No call - Vat null"
  else: 
    #variables
    items = ""
    CountryCode="TT"
    VATnumber="12345678"
    thisVat = aVat.replace(" ", "")
    
    CountryCode = thisVat[:2]
    VATnumber = thisVat[2:]
    
    # match = re.match(r"([a-z]+)([0-9]+)", thisVat, re.I)
    # print("is it a match? : "+str(match))
     try:
       if thisVat:
           items = match.groups()   
           CountryCode = items[0]
           VATnumber = items[1]
     except:
       return "INVALID_INPUT " + thisVat + " - nocall"
    
    #CALL
    logEntry( "-> Call : " + " CountryCode " + CountryCode + " VATnumber " + VATnumber, logbooktxtName)
    conn = http.client.HTTPSConnection("ec.europa.eu", timeout=30)
    payload = ''
    headers = {}

    conn.request("GET", "/taxation_customs/vies/rest-api/ms/"+CountryCode+"/vat/"+VATnumber, payload, headers)
    res = conn.getresponse()
    data = res.read()
  
    rxp = data.decode("utf-8")
    rxpList =json.loads(rxp)
    logEntry( "-> Call rxp : " + str(rxpList) , logbooktxtName)     
    #print( "This VAT is : " + rxpList.get('userError') )
    #print( "Name: " + rxpList.get('name'))
    #print( "Address: " + rxpList.get('address'))
    
    rxpPlusDate = rxpList.get('userError')
    logEntry( "END : " + " rxpPlusDate : " + rxpPlusDate , logbooktxtName)   
  return rxpPlusDate


