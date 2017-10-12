#!/usr/bin/env python3


import requests
import json
import  re
import os
import sys


###################################
###################################

def _url(path):
    """
    """
    return('http://10.38.34.192'  + path)


def add_task(summary, description=""):
    """
    """
    return(requests.post(_url('/rest/login')))

def get_tasks():
    """
    """
    return(request.get(_url('')))
    
    
def main():
    
    r = requests.post("http://10.38.34.192/rest/login", auth=('admin','password'))
    print(r.json)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print(r.cookies)
    Auth = r.headers.get('Authorization')
    #session = r.session()
    print(Auth)
    
    Auth_send={'Authorization':'%s'%Auth}
    print(Auth_send)
    
    
    ###########################################################################
    ###########################################################################
    ####
    ####   Container        switch
    ####     list                  fibrechannel-switch
    ####     
    ####     leaf                   domain-id
    ####
    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch", headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)
    ras = re.compile('name>([\:0-9a-f]+)</n')
    ras = ras.findall(r.text)
    print(type(ras))
    print(ras)
    wwn = ras[0]


    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/domain-id" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)
    
    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/user-friendly-name" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/fcid" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/vf-id" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/principal" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/enabled-state" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/up-time" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/model" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/firmware-version" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/ip-address" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/domain-name" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/fabric-user-friendly-name" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/ag-mode" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)


###############################################################################
###############################################################################
####
####          LOGOUT           LOGOUT
####
###############################################################################

    r = requests.post("http://10.38.34.192/rest/logout", headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    
    sys.exit()








    r = requests.get("http://10.38.34.192/rest/running/zoning/effective-configuration", headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.34.192/rest/running/fabric/fabric-switch", headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    
    r = requests.get("http://10.38.34.192/rest/running/brocade-interface/fibrechannel-statistics", headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    
    ###########################################################
    ###########################################################
    #### to run the up-time request you need the wwn of the switch
    ####   the first request get the info to capture the wwn
    ####
    #### 
    print("#"*120)
    print("Fibrechannel-switch")
    print("#"*120)  
    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch", headers=Auth_send)
    print(r.json)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print('@'*80)
    print(r.encoding)
    ras = re.compile('name>([\:0-9a-f]+)</n')
    ras = ras.findall(r.text)
    print(type(ras))
    print(ras)
    wwn = ras[0]
    print(type(wwn))
    print(wwn)
    print("#"*120)
    print("Fibrechannel-switch/up-time")
    print("#"*120)
    r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/up-time" % wwn, headers=Auth_send)
    #print(r.json)
    #print(r.text)
    #print(r.headers)
    if r.status_code != 200:
        print("error with the request")
        print(r.text)
    else:
        pass
    
    



    r = requests.post("http://10.38.34.192/rest/logout", headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    

if __name__ == '__main__':
    
    main()
