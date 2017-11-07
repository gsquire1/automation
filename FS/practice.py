#!/usr/bin/env python3


import requests
import json
import re
import os
import sys


###############################################################################
###############################################################################

switch_ip = "10.38.36.33"



class rest_cfg:

    def __init__(self, ):
        pass


    def rest_login(self, s_ip, username, passwrd):
        """
    
        """
        loginpath =  s_ip + "/rest/login"
        return(requests.post(_url(loginpath), auth=(username,passwrd)))


    def get_wwn(self, s_ip, auth_value):
        """
        
        """
        Auth_strng = {'Authorization':'%s'%auth_value}
        path_to_wwn =  s_ip + "/rest/running/switch/fibrechannel-switch"
        return(requests.get(_url(path_to_wwn), headers=Auth_strng))
        
        
        
###############################################################################
#### add this to another file
######

class get_top_level_list:
 
    def domain_id(self):
        return("/rest/running/switch/fibrechannel-switch/name/")
    
    def user_friendly_name(self):
        return("/rest/running/switch/fibrechannel-switch/name/")
      
    def dispatch(self, cmd):
        """
        """
        method_name =  "cmd_" + str(cmd)
        print("@"*10)
        print(cmd)
        print("@"*10)
        try:
            m = getattr(get_top_level_list(),cmd,'name')
            print(m)
            
        except AttributeError:
            print(method_name, "not found")
        
        return(m)
        
        
        

def _url(path):
    """
    """
    return("http://" + path)
    
    #return('http://10.38.36.33'  + path)


def add_task(summary, description=""):
    """
    """
    return(requests.post(_url('/rest/')))



def get_tasks(command):
    """
    """
    return(request.get(_url('')))
    
    

#def rest_login_old(s_ip,username,passwrd,):
  #  """
    #
    #"""
    #loginpath =  s_ip + "/rest/login"
    #response = requests.post(_url(loginpath), auth=(username,passwrd))
    #
    #return(response)



def main():
    
    switch_ip = "10.38.36.33"
    user = "admin"
    passwrd = "fibranne"
    
    sem = get_top_level_list()
    print("@"*50)
    p = sem.dispatch("domain_id")
    print(p())
    print("@"*50)
    p = sem.dispatch("user_friendly_name")
    print(p())
    print("@"*50)
    
    #sys.exit()
    
    
    
    sm = rest_cfg()

    r = sm.rest_login(switch_ip, user, passwrd)
    
    #r = rest_login(switch_ip, user, passwrd)
    #r = requests.post("http://10.38.36.33/rest/login", auth=('admin','password'))
    print(r.json)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print(r.cookies)
    Auth = r.headers.get('Authorization')
    print(Auth)
    Auth_send={'Authorization':'%s'%Auth}
    print(Auth_send)
    
    
    r = sm.get_wwn(switch_ip, Auth)
    
    
    ###########################################################################
    ###########################################################################
    ####
    ####   Container        switch
    ####     list                  fibrechannel-switch
    ####     
    ####     leaf                   domain-id
    ####
    #r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch", headers=Auth_send)

    print(r.json)
    print(r.text)
    print(r.headers)
    ras = re.compile('name>([\:0-9a-f]+)</n')
    ras = ras.findall(r.text)
    print(type(ras))
    print(ras)
    wwn = ras[0]


    
    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/domain-id" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)
    
    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/user-friendly-name" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/fcid" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/vf-id" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/principal" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/enabled-state" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/up-time" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/model" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/firmware-version" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/ip-address" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/domain-name" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/fabric-user-friendly-name" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/ag-mode" % wwn , headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)


###############################################################################
###############################################################################
####
####          LOGOUT           LOGOUT
####
###############################################################################

    #r = requests.post("http://10.38.36.33/rest/logout", headers=Auth_send)
    #print(r.json)
    #print(r.status_code)
    
    #sys.exit()








    r = requests.get("http://10.38.36.33/rest/running/zoning/effective-configuration", headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    r = requests.get("http://10.38.36.33/rest/running/fabric/fabric-switch", headers=Auth_send)
    print(r.json)
    print(r.text)
    print(r.headers)

    
    r = requests.get("http://10.38.36.33/rest/running/brocade-interface/fibrechannel-statistics", headers=Auth_send)
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
    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch", headers=Auth_send)
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
    r = requests.get("http://10.38.36.33/rest/running/switch/fibrechannel-switch/name/%s/up-time" % wwn, headers=Auth_send)
    #print(r.json)
    #print(r.text)
    #print(r.headers)
    if r.status_code != 200:
        print("error with the request")
        print(r.text)
    else:
        pass
    
    



    r = requests.post("http://10.38.36.33/rest/logout", headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    

if __name__ == '__main__':
    
    main()
