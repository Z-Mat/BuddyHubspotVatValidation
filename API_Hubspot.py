
import http.client
import json
from booklogging import *
from Credential import *

logbooktxtName = logbooktxtName0
logbooktxtName2 = logbooktxtName1

token= tokenHubspot
            
def getPropertiByCompanyID (thisPropertie, thisCompany):
  logEntry( "--> "+ thisPropertie , logbooktxtName) 
  propertie= thisPropertie
  companyID= thisCompany

  #CALL
  conn = http.client.HTTPSConnection("api.hubapi.com") #for by id
  payload = ''
  headers = {
    'Authorization': token,
    'Content-Type': 'application/json',
    
  }
  conn.request("GET", "/crm/v3/objects/companies/"+companyID+"?properties="+propertie, payload, headers)
  res = conn.getresponse()
  data = res.read()
  rxp = data.decode("utf-8")
  
  #working the response
  rxpList =json.loads(rxp)
  logEntry( "str(rxpList) : " + str(rxpList) , logbooktxtName) 
#  print("getPropertiByCompanyID : " + thisPropertie)
 # print("str(rxpList) : " + str(rxpList))
  
  try: 
    valueForRxp = rxpList.get('properties').get(propertie)
  except:
    valueForRxp="" 
  #RETURN
  try:
    logEntry( "END : " + valueForRxp, logbooktxtName) 
  except:
    logEntry( "END : valueForRxp is null" , logbooktxtName) 
  return valueForRxp












def updateCompanyById ( ThisFildName, ThisIdCompany, thisValue):
 
  logEntry( "-> update : " + ThisFildName + " " + thisValue, logbooktxtName) 
  conn = http.client.HTTPSConnection("api.hubapi.com")
  payload = json.dumps({
    "properties": {
      ThisFildName: thisValue
    }
  })
  headers = {
    'Authorization': token,
    'Content-Type': 'application/json'
  }
  conn.request("PATCH", "/crm/v3/objects/companies/"+ThisIdCompany, payload, headers)
  res = conn.getresponse()
  data = res.read()
  
  logstring = ("  IdCompany: " + ThisIdCompany 
               + "It was updated in HubSpot the propreitie : "+ ThisFildName 
               + " rxp: " + data.decode("utf-8")
               )
  logEntry( logstring, "logbook.txt")

def listAllIdCompanies (pageNumber):
   
  count=0 
  listAllIdCompanies = [] 
  
  while pageNumber != None:  
    print("Page :" + pageNumber)
    #logEntry("Page :" + pageNumber, logbooktxtName2) 
    conn = http.client.HTTPSConnection("api.hubspot.com",timeout=60)
    payload = ''
    headers = {
      'Authorization': token,
      'Content-Type': 'application/json',
      'Cookie': CookieHubspot
    }
    conn.request("GET", "/crm/v3/objects/companies/?properties=cvr_vat_number&after="+pageNumber, payload, headers)
    res = conn.getresponse()
    data = res.read()
    rxp = data.decode("utf-8")
    
    #working the response
    rxpList =json.loads(rxp)
    
    try:
      propertiesRxp = rxpList.get('results')
    except:
      propertiesRxp = [] 
    
    #pageNumber=None  
    
    #if count == 10:
    if 1==2:
      pageNumber=None
    else:
      try:
        pageNumber = rxpList.get('paging').get('next').get('after')
      except:
        pageNumber=None
      
    if propertiesRxp != None:
      for i in propertiesRxp:
            count+=1
            listAllIdCompanies.append(i["id"])
    #print(count)        
    #logEntry("count :" + str(count), logbooktxtName2) 
    #logEntry("", logbooktxtName2) 
    #logEntry("", logbooktxtName2) 
  #logEntry("---------------", logbooktxtName2) 

  #RETURN
  return listAllIdCompanies


def SECONDgetPropertiesByCompanyID (thiscompany):
  companyID= thiscompany
  #CALL
  conn = http.client.HTTPSConnection("api.hubapi.com") #for by id
  payload = ''
  headers = {
    'Authorization': token,
    'Content-Type': 'application/json',   
  }
  conn.request("GET", "/crm/v3/objects/companies/"+companyID+"?"+"properties=name,%20cvr_vat_number,%20vat_validation,%20vat_validation_date", payload, headers)
  res = conn.getresponse()
  data = res.read()
  rxp = data.decode("utf-8")

  #working the response
  rxpList =json.loads(rxp)
  id = str(rxpList.get('id'))
  name = str(rxpList.get('properties').get("name") )
  vat = str(rxpList.get('properties').get("cvr_vat_number") )
  vat_valid = str(rxpList.get('properties').get("vat_validation") )
  logEntry( id + " - " + vat + "               ------ " + vat_valid + " ---- " + name , "Mything.txt") 

  return rxpList


def SECONDlistAllIdCompanies (pageNumber):
       
  count=0 
  listAllIdCompanies = [] 
  
  while pageNumber != None:  
    print("Page :" + pageNumber)
    conn = http.client.HTTPSConnection("api.hubspot.com",timeout=60)
    payload = ''
    headers = {
      'Authorization': token,
      'Content-Type': 'application/json',
      'Cookie': CookieHubspot
    }
    conn.request("GET", "/crm/v3/objects/companies/?properties=name,%20cvr_vat_number,%20vat_validation,%20vat_validation_date&after="+pageNumber, payload, headers)
    res = conn.getresponse()
    data = res.read()
    rxp = data.decode("utf-8")
    
    #working the response
    rxpList =json.loads(rxp)
    
    try:
      propertiesRxp = rxpList.get('results')
    except:
      propertiesRxp = [] 
    
    #pageNumber=None  
    
    if count == 0:
      pageNumber=None
    else:
      try:
        pageNumber = rxpList.get('paging').get('next').get('after')
      except:
        pageNumber=None
    
    
    if propertiesRxp != None:
      listAllIdCompanies.append(propertiesRxp)  
      # for i in propertiesRxp:
      #       count+=1
      #       listAllIdCompanies.append(i["id"])
    print(count)        


  #RETURN
  return listAllIdCompanies




# #List = ["Geeks", "For", "Geeks"] 
# #
# #Dict = {1: 'Geeks', 2: 'For', 3: 'Geeks'} 


# company = SECONDgetPropertiesByCompanyID("9056750538")
# company2 = SECONDgetPropertiesByCompanyID("9056008674")
# company3 = SECONDgetPropertiesByCompanyID("9056772059")
# mylist = []
# mylist.append(company)
# mylist.append(company2)
# mylist.append(company3)

# for i in mylist:
#   idd = i.get('id')    
#   try: 
#     valueForRxp = i.get('properties').get("cvr_vat_number") 
#   except:
#     valueForRxp="" 
  
#   print(idd)
#   print(valueForRxp)