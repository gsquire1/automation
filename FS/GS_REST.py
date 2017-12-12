#!/usr/bin/env python3


import requests
import json
import re
import os
import sys     
import time
import untangle

#sys.path.append ("/opt/python/lib/python3.4/site-packages/")
###################################
###################################

ip = '10.38.34.190'

def _url(path):
    """
    """
    #return('http:// ip  + path)


def add_task(summary, description=""):
    """
    """
    return(requests.post(_url('/rest/login')))

def get_tasks():
    """
    """
    return(request.get(_url('')))
    
    
def main():
    
    r = requests.post("http://%s/rest/login" % ip, auth=('admin','password'))
    # loginpath =  "http://" + ip + "/rest/login"
    #print(r.text)
    #print(r.headers)
    print('((((((((((((((((((AUTH HERE))))))))))))))))))')
    Auth = r.headers.get('Authorization')
    #print(r.status_code)
    #print(Auth)
    Auth_send={'Authorization':'%s'%Auth}
    print(Auth_send)
    # print(r.text)
    # print(r.headers)
    # print(r.cookies)
    # Auth = r.headers.get('Authorization')
    # print("this is AUTH")
    # print(Auth)
    
    ###########################################################################
    ###########################################################################
    ####
    ####   Container        switch
    ####     list                  fibrechannel-switch
    ####     
    ####     leaf                   domain-id
    ####
    fs = requests.get("http://%s/rest/running/switch/fibrechannel-switch" % ip , headers=Auth_send)
    print(fs.json)
    print(fs.text)
    print(fs.headers)
    ras = re.compile('name>([\:0-9a-f]+)</n')
    ras = ras.findall(fs.text)
    print(type(ras))
    print(ras)
    wwn = ras[0]
    
    # print('\n\n\n')   
    # print('(((((((((((((((((((((EFFECTIVE_CONFIGURATION)))))))))))))))))))))')
    # r = requests.get("http://10.38.36.33/rest/running/zoning/effective-configuration",  headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # #print(r.headers)
    
    print('\n\n\n')
    print('(((((((((((((((((((((DEFINED_CONFIGURATION)))))))))))))))))))))))')    
    r = requests.get("http://%s/rest/running/zoning/defined-configuration" % ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    #print(r.headers)
    
    print('\n\n\n')
    print('(((((((((((((((((((((DEFINED_CONFIGURATION_TESTING)))))))))))))))))))))))')    
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg/cfg-name/FID_10/member-zone/zone-name/" % ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)
    
    # print('\n\n\n')
    # print('(((((((((((((((((((((DOMAIN ID)))))))))))))))))))))))')
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/domain-id" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # print('\n\n\n')
    # print('(((((((((((((((((((((USER-FRIENDLY NAME)))))))))))))))))))))))')      
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/user-friendly-name" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/fcid" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/vf-id" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/principal" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/enabled-state" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/up-time" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/model" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/firmware-version" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/ip-address" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/domain-name" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/fabric-user-friendly-name" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/ag-mode" % wwn , headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)

    ######## This prints all stats for all ports ##############################
    # r = requests.get("http://10.38.36.33/rest/running/brocade-interface/fibrechannel-statistics", headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    
    
    ###########################################################
    ###########################################################
    #### to run the up-time request you need the wwn of the switch
    ####   the first request get the info to capture the wwn
    ####
    #### 
    # print("#"*120)
    # print("Fibrechannel-switch")
    # print("#"*120)  
    # #r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch", headers=Auth_send)
    # print(fs.json)
    # print(fs.status_code)
    # print(fs.text)
    # print(fs.headers)
    # print('@'*80)
    # print(fs.encoding)
    # # ras = re.compile('name>([\:0-9a-f]+)</n')
    # # ras = ras.findall(r.text)
    # # print(type(ras))
    # # print(ras)
    # # wwn = ras[0]
    # print(type(wwn))
    # print(wwn)
    # print("#"*120)
    # print("Fibrechannel-switch/up-time")
    # print("#"*120)
    # r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/up-time" % wwn, headers=Auth_send)
    # #print(r.json)
    # print(r.text)
    # #print(r.headers)
    # if r.status_code != 200:
    #     print("error with the request")
    #     print(r.text)
    # else:
    #     pass

###############################################################################
###############################################################################
####
####          LOGOUT           LOGOUT
####
###############################################################################

    ####   LOGOUT   ####
    print('LOGOUT____HERE')
    r = requests.post("http://%s/rest/logout"% ip, headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    if r.status_code == 204:
        print("successful logout\n\n")
    else:
        print("logout was not successful\n\n")
    sys.exit(0)
    

if __name__ == '__main__':
    
    main()
