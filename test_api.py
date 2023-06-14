import requests
import json
from requests.auth import HTTPBasicAuth

f = open("login.txt", "r")
lines = f.readlines()
f.close()
email = lines[0].strip('\n')
password = lines[1]
URL = "https://api.clicktime.com/v2/me"
URL2 = "https://api.clicktime.com/v2/jobs"

response = requests.get(URL,auth=HTTPBasicAuth(email,password))
vin = response.json()
token = vin['data']['AuthToken']['Token']
respone2 = requests.get(URL2,headers={'Authorization': 'TOKEN {}'.format(token)}).json()
print(respone2)

clients = respone2['data'][0]['ClientID']


def checkProperty(property):
  for i in range(len(respone2['data'])):
    if respone2['data'][i][property] is None:
        print(property + " not found in object " + str(i))
    else:
        print(property + " found")

checkProperty('ClientID')
checkProperty('EndDate')
checkProperty('ID')
checkProperty('IsActive')
checkProperty('JobNumber')
checkProperty('Name')
checkProperty('Notes')