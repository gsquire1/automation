#!/usr/bin/env python3


import requests
import json
import  re
import os
import sys     
import time
import untangle
import logging


###############################################################################
###############################################################################

switch_ip = "10.38.34.192"



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
    
    def get_wwn(self, s_ip, auth_value, fid = -1):
        """
        
        """
        Auth_strng = {'Authorization':'%s'%auth_value}
        
        if fid < 1 :
            path_to_wwn =  "http://" + s_ip + "/rest/running/switch/fibrechannel-switch"
        else:
            path_to_wwn =  "http://" + s_ip + "/rest/running/switch/fibrechannel-switch" + "?vf-id=" + str(fid)
         
        s = requests.get(path_to_wwn, headers=Auth_strng)
        
        doc = untangle.parse(s.text)
        done = doc.Response.fibrechannel_switch.name.cdata
        return(done)
        #return(requests.get(path_to_wwn, headers=Auth_strng))
        
        
        
###############################################################################
#### add this to another file
######

class get_top_level_list_fibrechannel_switch:
 
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
        print(cmd)
        underscore_cmd = cmd.replace("-", "_")
        print("@"*10)
        try:
            m = getattr(get_top_level_list_fibrechannel_switch(),underscore_cmd)
            
        except AttributeError:
            print(method_name, "not found")
        
        return(m)

def _url( sw_ip, wwn, path, cmd, fid=-1 ):
    """
    """
    if fid > 0:
        print("#"*80)
        a = "http://" + sw_ip  + path + wwn + "/" + cmd + "?vf-id=" + str(fid)
        print(a)
        print("#"*80)
        return("http://" + sw_ip  + path + wwn + "/" + cmd + "?vf-id=" + str(fid))
        
    else:
        return("http://" + sw_ip  + path + wwn + "/" + cmd)

def add_task(summary, description=""):
    """
    """
    return(requests.post(_url('/rest/')))

def get_tasks(command, switch_ip, wwn, Auth_send, list_name, fid = -1):
    """ 
    """
    #sem = get_top_level_list_fibrechannel_switch()
    #p = sem.dispatch(command)
    
    if list_name == "fc_switch":
        top_level = "/rest/running/switch/fibrechannel-switch/name/"
        
    if list_name == "fab_switch":
        top_level = "/rest/running/fabric/fabric-switch/name/"
       
    cmplt_path = _url(switch_ip, wwn, top_level, command , fid)
    r = requests.get(cmplt_path, headers=Auth_send)

    return(r)
    
def get_fc_switch_leaf(switch_ip, wwn, Auth_send, word, fid = -1):
    """return the info for a specified leaf in the module
        brocade-fibrecahnnel-switch  yang file 
    
    """
    #vf_id = doc.Response.fibrechannel_switch.vf_id.cdata
    # s = get_tasks('vf-id', switch_ip, wwn, Auth_send)   ## command from below
    s = get_tasks(word,switch_ip, wwn,Auth_send, "fc_switch", fid )
    
    doc = untangle.parse(s.text)
    
    if "vf-id" == word:
        done = doc.Response.fibrechannel_switch.vf_id.cdata
    if "domain-id" == word:
        done =  doc.Response.fibrechannel_switch.domain_id.cdata
    if "fcid"  == word:
        done =  doc.Response.fibrechannel_switch.fcid.cdata
    if "user-friendly-name" == word:
        done =  doc.Response.fibrechannel_switch.user_friendly_name.cdata
    if "enabled-state" == word:
        done =  doc.Response.fibrechannel_switch.enabled_state.cdata
    if "up-time"  == word:
        done =  doc.Response.fibrechannel_switch.up_time.cdata
    if "model" == word:
        done = doc.Response.fibrechannel_switch.model.cdata
    if "firmware-version"  == word:
        done =  doc.Response.fibrechannel_switch.firmware_version.cdata
    if "ip-address"  == word:
        done =  doc.Response.fibrechannel_switch.ip_address.ip_address.cdata        
    if "domain-name"  == word:
        done =  doc.Response.fibrechannel_switch.domain_name.cdata
    if "fabric-user-friendly-name"  == word:
        done =  doc.Response.fibrechannel_switch.fabric_user_friendly_name.cdata
    if "ag-mode"  == word:
        done =  doc.Response.fibrechannel_switch.ag_mode.cdata    
    if "principal"  == word:
        done =  doc.Response.fibrechannel_switch.principal.cdata 
#    'domain-id', 'user-friendly-name', 'fcid', 'vf-id', 'principal', 'enabled-state',
#    'up-time', 'model', 'firmware-version', 'ip-address', 'domain-name', 'fabric-user-friendly-name', 'ag-mode'
        
    return(done)


def get_fabric_switch_leaf(switch_ip, wwn, Auth_send, word, fid = -1):
    """return the info for a specified leaf in the module
        brocade-fabric-switch  yang file 
    
    """
 
    s = get_tasks(word,switch_ip, wwn,Auth_send, "fab_switch", fid )
    print("debug___"*10)
    print(s.text)
    print("end_____"*10)
    doc = untangle.parse(s.text)
    print("debug___"*10)
    print(doc)
    print("end_____"*10)
    if "vf-id" == word:
        done = doc.Response.fabric_switch.vf_id.cdata
    if "wwn" == word:
        done = doc.Response.fabric_switch.name.cdata
    done = doc.Response.fabric_switch.name.cdata
        
        
    return(done)

###############################################################################
###############################################################################
####
####
####
###############################################################################

def main():
    
    ####  chewy2
    switch_ip = "10.38.34.192"
    ####    Odin
    #switch_ip = "10.38.34.178"
    ####    stinger
    switch_ip = "10.38.34.182"
    #### wedge
    switch_ip = "10.38.34.190"

    user = "admin"
    passwrd = "password"
    fid = 31
    
    
    
    sm = rest_cfg()
    r = sm.rest_login(switch_ip, user, passwrd)
    print(r.json)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    print(r.cookies)
    Auth = r.headers.get('Authorization')
    print(Auth)
    Auth_send={'Authorization':'%s'%Auth}
    print(Auth_send)
    
    
    print("#"*80)
    print("wwn "*20)
    r31 = sm.get_wwn(switch_ip, Auth, fid)
   # print(r31.text)
    print(r31)
    print("#"*80)
    print("wwn "*20)

    rd = sm.get_wwn(switch_ip, Auth, fid=-1)
    
    print(rd)
    print("#"*80)
    print("wwn "*20)
    
    ###########################################################################
    ###########################################################################
    ####
    ####   Container        switch
    ####     list                  fibrechannel-switch
    ####     
    ####     leaf                   domain-id
    ####
    #r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch", headers=Auth_send)

    wwn = rd
    wwn31 =  r31


    # sem = get_top_level_list_fibrechannel_switch()
    # print("@"*80)
    # p = sem.dispatch("domain-id")
    # cmplt_path = _url(switch_ip, wwn, p(),  "domain-id")
    # print(p())
    # print(cmplt_path)
    # 
    # r = requests.get(cmplt_path, headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    # 
    # print("@"*80)
    # 
    # 
    # p = sem.dispatch("user-friendly-name")
    # cmplt_path = _url(switch_ip, wwn, p(), "user-friendly-name" )
    # print(p())
    # print(cmplt_path)
    # 
    # r = requests.get(cmplt_path, headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.status_code)
    # print(r.headers)
    # print("@"*80)
    # 
    # fcs = ['domain-id', 'user-friendly-name', 'fcid', 'vf-id', 'enabled-state', 'up-time', 'model', 'firmware-version', 'ip-address', 'domain-name', 'fabric-user-friendly-name', 'ag-mode', 'principal']
    # fcs = ['domain-id', 'user-friendly-name', 'fcid', 'vf-id']
    # for c in fcs:    
    #  
    #     s = get_tasks(c, switch_ip, wwn, Auth_send)
    #     print("$"*80)
    #     print(s.json)
    #     print(s.status_code)
    #     print(s.text)
    #     print("&"*80)
    #     time.sleep(1)
    #r = requests.get("http://%s/rest/running/switch/fibrechannel-switch/name"  % ( switch_ip, wwn) , headers=Auth
    r = requests.get("http://%s/rest/running/switch/fibrechannel-switch/name/%s/up-time" % (switch_ip, wwn) , headers=Auth_send)
    
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)
    
    r = requests.get("http://%s/rest/running/fabric/fabric-switch" % (switch_ip) , headers=Auth_send)
     
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)
      
   
   
    r = requests.get("http://%s/rest/running/fabric/fabric-switch?vf-id=31" % (switch_ip) , headers=Auth_send)
    
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)
    
    #r = requests.get("http://%s/rest/running/fabric/fabric-switch/name/%s/fcid/?vf-id=31" % (switch_ip,wwn31) , headers=Auth_send)
    #r = requests.get("http://%s/rest/running/fabric/fabric-switch/name/%s/fcid" % (switch_ip,wwn) , headers=Auth_send)
    #print("@"*80)
    #print(r.text)
    #print("@"*80)
    #print("@"*80)
    
    
    
    friendly_name_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "switch-user-friendly-name" ) 
    wwn_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "chassis-wwn" ) 
    chass_friendly_name_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "chassis-user-friendly-name" )
    domain_id_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "domain-id" )
    pricipal_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "principal" )
    fcid_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "fcid" )
    ipaddr_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "ip-address" )
    fcipaddr_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "fcip-address" )
    ipv6addr_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "ipv6-address" )
    firmrev_from_fabric_switch = get_fabric_switch_leaf(switch_ip, wwn,Auth_send, "firmware-version" ) 
    
    print(wwn_from_fabric_switch)
    

    principal_switch = get_fc_switch_leaf(switch_ip, wwn31,Auth_send, "principal" , 31) 
    vf_state = get_fc_switch_leaf(switch_ip, wwn31,Auth_send, "vf-id", 31)
    principal_switch = get_fc_switch_leaf(switch_ip, wwn31,Auth_send, "principal" , 31)
    domain_id =  get_fc_switch_leaf(switch_ip, wwn,Auth_send, "domain-id")
    fcid =  get_fc_switch_leaf(switch_ip, wwn,Auth_send, "fcid")
    user_friendly_name =  get_fc_switch_leaf(switch_ip, wwn,Auth_send, "user-friendly-name")
    enabled_state = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "enabled-state")
    up_time = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "up-time")
    model = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "model")
    firmware_version= get_fc_switch_leaf(switch_ip, wwn,Auth_send, "firmware-version")
    ip_address = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "ip-address")
    domain_name  = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "domain-name")
    fabric_u_f_name  = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "fabric-user-friendly-name")
    ag_mode  = get_fc_switch_leaf(switch_ip, wwn,Auth_send, "ag-mode")
    

    print("vf_id                                 :  %s  "  % vf_state)
    print("principal switch                      :  %s "  %  principal_switch)
    print("domian_id                             :  %s  " % domain_id)
    print("fcid                                  :  %s  " % fcid )
    print("user_friendly_name                    :  %s  "  %  user_friendly_name)
    print("switch state                          :  %s  " % enabled_state )
    print("up-time                               :  %s  "  %  up_time)
    print("model                                 :  %s   "  %  model)
    print("firmware-version                      :  %s  "  % firmware_version)
    print("ip-address                            :  %s  "  %  ip_address)
    print("domain-name                           :  %s  "  %  domain_name)
    print("fabric-user-friendly-name             :  %s  "  % fabric_u_f_name)
    print("ag-mode                               :  %s  "  % ag_mode)
    
    print("&"*80)
    time.sleep(1)
    
    r = requests.post("http://10.38.34.192/rest/logout", headers=Auth_send)
    print(r.status_code)
    
   

if __name__ == '__main__':
    
    main()
