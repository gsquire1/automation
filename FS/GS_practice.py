#!/usr/bin/env python3


import requests
import json
import re
import os
import sys     
import time
import untangle


###############################################################################
###############################################################################
 

switch_ip = "10.38.36.33"



class rest_cfg:

    def __init__(self, ):
        pass


    def rest_login(self, s_ip, username, passwrd):
        """
    
        """
        loginpath =  "http://" + s_ip + "/rest/login"
        return(requests.post(loginpath, auth=(username,passwrd)))

    def rest_logout(self, ):
        pass        
    
    def get_wwn(self, s_ip, auth_value):
        """
        
        """
        Auth_strng = {'Authorization':'%s'%auth_value}
        
        path_to_wwn =  "http://" + s_ip + "/rest/running/switch/fibrechannel-switch"
        return(requests.get(path_to_wwn, headers=Auth_strng))
        
        
        
###############################################################################
#### add this to another file
######

class get_top_level_list:
 
    def domain_id(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def user_friendly_name(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )    
    def fcid(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def vf_id(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def principal(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def enabled_state(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def up_time(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def model(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def firmware_version(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def  ip_address(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def domain_name(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def fabric_user_friendly_name(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
    def ag_mode(self):
        return("/rest/running/switch/fibrechannel-switch/name/" )
###############################################################################
####    helper to retrieve the URI 
####
    
    def dispatch(self, cmd):
        """
        """
        #method_name =  "cmd_" + str(cmd)
        print("@"*10)
        #print(cmd)
        underscore_cmd = cmd.replace("-", "_")
        print(underscore_cmd)
        print("@"*10)
        try:
            m = getattr(get_top_level_list(),underscore_cmd)
            
        except AttributeError:
            print(method_name, "not found")
        print(m())
        return(m)

def _url( sw_ip, wwn, path, cmd ):
    """
    """
    return("http://" + sw_ip  + path + wwn + "/" + cmd)

def add_task(summary, description=""):
    """
    """
    return(requests.post(_url('/rest/')))

def get_tasks(command, switch_ip, wwn, Auth_send):
    """
    """
    sem = get_top_level_list()
    p = sem.dispatch(command)
    cmplt_path = _url(switch_ip, wwn, p(), command )

    r = requests.get(cmplt_path, headers=Auth_send)
    return(r)
    
def get_tasks_name(command, switch_ip, wwn, Auth_send, get_this_name):
    """
    """
    sem = get_top_level_list()
    p = sem.dispatch(command)
    cmplt_path = _url(switch_ip, wwn, p(), command )
    cmplt_path = cmplt_path + get_this_name
    
    r = requests.get(cmplt_path, headers=Auth_send)
    return(r)
    
###############################################################################
###############################################################################
####
####
####
###############################################################################

def main():
    
    ####  chewy2
    switch_ip = "10.38.36.33"
    ####    Odin
    #switch_ip = "10.38.34.178"
    ####    stinger
    #switch_ip = "10.38.34.182"

    user = "admin"
    passwrd = "fibranne"
    fid = 31
    #fid = 0
    sm = rest_cfg()

    r = sm.rest_login(switch_ip, user, passwrd)
    
    #r = rest_login(switch_ip, user, passwrd)
    #r = requests.post("http://10.38.34.192/rest/login", auth=('admin','password'))
    print(r.json)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print(r.cookies)
    Auth = r.headers.get('Authorization')
    print("((((((((((((((((((AUTHAUTHAUTHAUTHAUTHAUTH)))))))))))))))))))))))))))")
    print(Auth)
    Auth_send={'Authorization':'%s'%Auth}
    print("(((((((((((((((((AUTHSENDAUTHSENDAUTHSEND)))))))))))))))))))))))))))")
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
    #r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch", headers=Auth_send)

    print(r.json)
    print(r.text)
    #print(r.headers)
    ras = re.compile('name>([\:0-9a-f]+)</n')
    ras = ras.findall(r.text)
    print(type(ras))
    print(ras)
    wwn = ras[0]


    sem = get_top_level_list()
    print("@"*80)
    p = sem.dispatch("domain-id")
    cmplt_path = _url(switch_ip, wwn, p(),  "domain-id")
    print(p())
    print(cmplt_path)
     
    r = requests.get(cmplt_path, headers=Auth_send)
    print(r.json)
    print(r.text)
    #print(r.headers)
    print("@"*80)
        
    p = sem.dispatch("user-friendly-name")
    cmplt_path = _url(switch_ip, wwn, p(), "user-friendly-name" )
    print(p())
    print(cmplt_path)
    
    r = requests.get(cmplt_path, headers=Auth_send)
    #print(r.json)
    print(r.text)
    print(r.status_code)
    #print(r.headers)
    print("@"*80)
    
    #r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch/name/%s/domain-id" % wwn , headers=Auth_send)
    #print(r.json)
    #print(r.text)
    #print(r.headers)
    
    
    fcs = ['domain-id', 'user-friendly-name', 'fcid', 'vf-id', 'principal', 'enabled-state', 'up-time', 'model', 'firmware-version', 'ip-address', 'domain-name', 'fabric-user-friendly-name', 'ag-mode']
    fcs = ['domain-id', 'user-friendly-name', 'fcid', 'vf-id']
    
    for c in fcs:    
        s = get_tasks(c, switch_ip, wwn, Auth_send)
        print("$"*80)
        print(s.json)
        print(s.status_code)
        print(s.text)
        print("&"*80)
        time.sleep(1)

           
    fcs = ['vf-id',]
     
    for c in fcs:    
        s = get_tasks(c, switch_ip, wwn, Auth_send)
        print("$"*80)
        print(s)
        print(s.json)
        print(s.status_code)
        print(s.text)
        print("&"*80)
        print("((((((((((((((Start the magic))))))))))))))")
        #print(json.dumps(s.text))   #  this is not what we want
        doc = untangle.parse(s.text)
        #child_0 = doc.Response.fibrechannel_switch.name.cdata[0]
        wwn = doc.Response.fibrechannel_switch.name.cdata
        vf_id = doc.Response.fibrechannel_switch.vf_id.cdata
        
        print("wwn =  %s  " %  wwn)
        print("vf_id =  %s  "  % vf_id)
        print("&"*80)
        time.sleep(1)
        
    
    r = requests.post("http://10.38.34.192/rest/logout", headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    
    
    sys.exit()
    #    def dispatch(self, switch_ip, cmd, auth , fid):
    




if __name__ == '__main__':
    
    main()