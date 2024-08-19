
#   If needed install missing Python module dotenv
#   pip install python-dotenv


#   Import requested Python modules

import requests
import json
import urllib3
urllib3.disable_warnings()
import time
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

#   Load variables from .env

HOST_FILE = os.getenv('HOST_FILE')

URL_GETID = os.getenv('URL_GETEID')
URL_MIGRATE = os.getenv('URL_MIGRATE')

API_SECRET_KEY = os.getenv('API_SECRET_KEY')
API_VERSION = os.getenv('API_VERSION')

WORKLOAD_SECURITY_POLICY_ID = os.getenv('WORKLOAD_SECURITY_POLICY_ID')

PROXY_TYPE_TO_CONTACT_WORKLOADSECURITY = os.getenv('PROXY_TYPE_TO_CONTACT_WORKLOADSECURITY')
PROXY_ID_TO_CONTACT_WORKLOADSECURITY = os.getenv('PROXY_ID_TO_CONTACT_WORKLOADSECURITY')

#   Get HostID from Hostname
#   Hostnames are loaded in computer_list.txt
#   Hostnames must match hostnames in Deep Security Manager

#   Read list of hostnames frmo computer_list.txt one by one and pass it to 
#   Get computer ID from list of hostnames

#   Read from computer_list.txt
HOST_FILE = open((HOST_FILE), 'r')
while HOST_FILE:
    line  = HOST_FILE.readline()
    line = line.replace('\n', '')
    if line == "":
        break

#   Get computer ID from list of hostnames
#   from Deep Security Manager
#   search by fieldName hostName

    url_getid = (URL_GETID)
    payload = json.dumps({
            "searchCriteria": [
                {
                "fieldName": "hostName",
                "stringValue": (line),
                "stringWildcards": False
                }
            ]
            })
    headers = {
        'api-version': (API_VERSION),
        'api-secret-key': (API_SECRET_KEY),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url_getid, headers=headers, data=payload, verify=False).json()

#   Convert output to JSON and extract 
#   hostName and ID

    data = json.dumps(response, indent = 2)
    data = json.loads(data)
    hostname = data['computers'][0]['hostName']
    ID = data['computers'][0]['ID']

#   Migration
    url_migrate = (URL_MIGRATE)
    ID = int(ID)
    print("HostID: ",(ID), " ","Hostname: ", (hostname))
    payload = json.dumps({
        "computerID": int(ID),
        "workloadSecurityPolicyID": (WORKLOAD_SECURITY_POLICY_ID)
#        ,
#        "proxyTypeToContactWorkloadSecurity": (PROXY_TYPE_TO_CONTACT_WORKLOADSECURITY)
#        "proxyIDToContactWorkloadSecurity": (PROXY_ID_TO_CONTACT_WORKLOADSECURITY)    
    })
    headers = {
        'api-version': (API_VERSION),
        'api-secret-key': (API_SECRET_KEY),
        'Content-Type': 'application/json'
}

    response = requests.request("POST", url_migrate, headers=headers, data=payload, verify=False)
    print(response.text)
    
HOST_FILE.close()   