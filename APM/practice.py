#!/usr/bin/env python3

import os,sys
sys.path.append('/home/automation/lib/FOS')
#sys.path.append('/home/automation/lib/MAPS')
#sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')


import requests
# import json
# import  re
# import os
# import sys     
# import time
# import untangle


import logging
import argparse
import rest_cmd_lib
###############################################################################
###############################################################################


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    pp.add_argument("ip", help="IP address of SUT")
    pp.add_argument("fid", type=int, default=128, help="Choose the FID to operate on")
    pp.add_argument("user", help="username for SUT")
    pp.add_argument("pw", help="password of user")
    
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp 

def parse_args(args):
    
    verb_value = "99"
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])

    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    parser.add_argument('-cp',  '--cmdprompt', help="switch is already at command prompt")
    parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
    parser.add_argument('-r',   '--steps', type=int, help="Steps that will be executed")
    parser.add_argument('-ftp_ip', '--ftp_ipaddress', help="ftp address of server to upload the config file")
    parser.add_argument('-ftp_n', '--ftp_username', help="ftp username of server to upload the config file")
    parser.add_argument('-ftp_p', '--ftp_password', help="ftp password of server to upload the config file")
    parser.add_argument("-cfg_p", "--config_path", help="the path of folder to upload the config file\nif left blank default ftp folder is used")
    
    #parser.add_argument('-p', '--password', help="password")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    #group.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")
    
    args = parser.parse_args()
    print(args)
    
    # if not args.chassis_name and not args.ipaddr:
    #     print("Chassis Name or IP address is required")
    #     sys.exit()
    #     
    # if args.cmdprompt and not args.switchtype:
    #     print("To start at the command prompt the switch type is needed.")
    #     sys.exit()
    #     
    # if not args.cmdprompt and args.switchtype:
    #     print('To start at the command prompt both switch type and command prompt is requried')
    #     sys.exit()
    # #print("Connecting to IP :  " + args.ip)
    # #print("user             :  " + args.user)
    # #verbose    = args.verbose
    # if not args.ftp_ipaddress or not args.ftp_username or not args.ftp_password:
    #     print("ftp information is required")
    #     sys.exit()
     

    return(parser.parse_args())

###############################################################################
###############################################################################
###############################################################################

# class rest_cfg:
# 
#     def __init__(self, pa):
#         self.fid          = pa.fid
#         self.user      = pa.user
#         self.pwrd     = pa.pw
#         self.ip           = pa.ip
#         self.Auth    =  self.rest_login()
#         self.verbose  = pa.verbose
#         
#     def get_Auth(self, ):
#         return(self.Auth)
#     
#     def test(self, ):
#         print("#"*80)
#         print("\nTEST of rest_cfg")
#         print(self.ip)
#         print(self.fid)
#         print(self.user)
#         print(self.pwrd)
#         return()
#     
#     def rest_login(self, ):
#         """
#     
#         """
#         
#         loginpath =  "http://" + self.ip + "/rest/login"
#         r = (requests.post(loginpath, auth=(self.user , self.pwrd)))
#         
#         Auth = r.headers.get('Authorization')
#         print(Auth)
#         Auth_send={'Authorization':'%s'%Auth}
#         print(Auth_send)
#     
# ###############################################################################
# ###############################################################################
#         if r.status_code == 403:    ####  max limit for REST sessions reached
#             print(r.text)
#             sys.exit()
#         return(Auth_send)        
# 
#     def rest_logout(self, ):
#         """
#         """
#         #r = requests.post("http://%s/rest/logout" % pa.ip , headers=Auth_send)
#         r = requests.post("http://%s/rest/logout" % self.ip , headers=self.Auth)
#         print(r.status_code)    
#         if r.status_code == 204:
#             print("successful logout\n\n")
#         else:
#             print("logout was not successful\n\n")
#         return(r)
#     
#     def get_wwn(self,  fid = -1):
#         """
#         
#         """
#         #Auth_strng = {'Authorization':'%s'%auth_value}
#         
#         if fid < 1 :
#             path_to_wwn =  "http://" + self.ip + "/rest/running/switch/fibrechannel-switch"
#         else:
#             path_to_wwn =  "http://" + self.ip + "/rest/running/switch/fibrechannel-switch" + "?vf-id=" + str(fid)
#         
#         try: 
#             s = requests.get(path_to_wwn, headers=self.Auth)            
#             doc = untangle.parse(s.text)
#             done = doc.Response.fibrechannel_switch.name.cdata
#         except AttributeError:
#             print("Error during untangle - None was returned")
#             print("Please check that the correct FID is used    ")
#             done = "Untangle Error"
#         except:
#             print("Error in untagle" , sys.exc_info()[0] )
#             done = "Untangle Error"
#         return(done)
#             
#     def fs_leaf(self, word, wwn, fid = -1):
#         """
#         return the info for a specified leaf in the module
#             brocade-fabric-switch  yang file 
#         
#         """
#         
#         
#         try:
#             
#             s = get_tasks(word, self.ip, wwn, self.Auth , "fab_switch", fid )
#             #print("fs_leaf_debug___"*10)
#             #print(s.text)
#             #print("fs_leaf_end_____"*10)
#             doc = untangle.parse(s.text)
#             #print("fs_leaf_debug___"*10)
#             #print(doc)
#             #print("fs_leaf_end_____"*10)
#             done = "none"
#             if "vf-id" == word:
#                 done = doc.Response.fabric_switch.vf_id.cdata
#             if "wwn" == word:
#                 done = doc.Response.fabric_switch.name.cdata
#             if "switch-user-friendly-name"  == word:
#                 done = doc.Response.fabric_switch.switch_user_friendly_name.cdata
#             if "chassis-wwn"  == word:
#                 done = doc.Response.fabric_switch.chassis_wwn.cdata
#             if "chassis-user-friendly-name" == word:
#                 done = doc.Response.fabric_switch.chassis_user_friendly_name.cdata              
#             if "domain-id" == word:
#                 done = doc.Response.fabric_switch.domain_id.cdata
#             if "principal" == word:
#                 done = doc.Response.fabric_switch.principal.cdata
#             if "fcid" == word:
#                 done = doc.Response.fabric_switch.fcid.cdata
#             if "ip-address" == word:
#                 done = doc.Response.fabric_switch.ip_address.cdata
#             if "fcip-address"  == word:
#                 done = doc.Response.fabric_switch.fcip_address.cdata
#             if "ipv6-address" == word:
#                 done = doc.Response.fabric_switch.ipv6_address.cdata
#             if "firmware-version" == word:
#                 done = doc.Response.fabric_switch.firmware_version.cdata
#             
#             if done == "none":
#                 pass
#                 print("\n\nError in fs_leaf the command requested is not one of the\
#                       \ncommand requested was  %s    \
#                       \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
#                       \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
#                       \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    
#  
#         except AttributeError:
#             print("Error during untangle - None was returned")
#             done = "Untangle Error"
#         except:
#             print("Error in untagle" , sys.exc_info()[0] )
#             print("fs_leaf")
#             done = "Untangle Error"
#         return(done)
#               
#     def fcs_leaf(self, word, wwn, fid = -1):
#         """return the info for a specified leaf in the module
#             brocade-fibrecahnnel-switch  yang file 
#         
#         """
#         #vf_id = doc.Response.fibrechannel_switch.vf_id.cdata
#         # s = get_tasks('vf-id', switch_ip, wwn, Auth_send)   ## command from below
#         s = get_tasks(word,switch_ip, wwn,Auth_send, "fc_switch", fid )
#         
#         doc = untangle.parse(s.text)
#         try:
#                 
#             if "vf-id" == word:
#                 done = doc.Response.fibrechannel_switch.vf_id.cdata
#             if "domain-id" == word:
#                 done =  doc.Response.fibrechannel_switch.domain_id.cdata
#             if "fcid"  == word:
#                 done =  doc.Response.fibrechannel_switch.fcid.cdata
#             if "user-friendly-name" == word:
#                 done =  doc.Response.fibrechannel_switch.user_friendly_name.cdata
#             if "enabled-state" == word:
#                 done =  doc.Response.fibrechannel_switch.enabled_state.cdata
#             if "up-time"  == word:
#                 done =  doc.Response.fibrechannel_switch.up_time.cdata
#             if "model" == word:
#                 done = doc.Response.fibrechannel_switch.model.cdata
#             if "firmware-version"  == word:
#                 done =  doc.Response.fibrechannel_switch.firmware_version.cdata
#             if "ip-address"  == word:
#                 done =  doc.Response.fibrechannel_switch.ip_address.ip_address.cdata        
#             if "domain-name"  == word:
#                 done =  doc.Response.fibrechannel_switch.domain_name.cdata
#             if "fabric-user-friendly-name"  == word:
#                 done =  doc.Response.fibrechannel_switch.fabric_user_friendly_name.cdata
#             if "ag-mode"  == word:
#                 done =  doc.Response.fibrechannel_switch.ag_mode.cdata    
#             if "principal"  == word:
#                 done =  doc.Response.fibrechannel_switch.principal.cdata 
#         #    'domain-id', 'user-friendly-name', 'fcid', 'vf-id', 'principal', 'enabled-state',
#         #    'up-time', 'model', 'firmware-version', 'ip-address', 'domain-name', 'fabric-user-friendly-name', 'ag-mode'
#         
#         
#             if done == "none":
#             
#                 print("\n\nError in fs_leaf the command requested is not one of the\
#                     \ncommand requested was  %s    \
#                     \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
#                     \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
#                     \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    
# 
#         
#         except AttributeError:
#             print("Error during untangle - None was returned")
#             done = "Untangle Error"
#         except:
#             print("Error in untagle" , sys.exc_info()[0] )
#             done = "Untangle Error"
#         return(done)
#     
#         
###############################################################################
#### add this to another file
######
# 
# class get_top_level_list_fibrechannel_switch:
#  
#     def domain_id(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def user_friendly_name(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )    
#     def fcid(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def vf_id(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def principal(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def enabled_state(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def up_time(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def model(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def firmware_version(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def  ip_address(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def domain_name(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def fabric_user_friendly_name(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
#     def ag_mode(self):
#         return("/rest/running/switch/fibrechannel-switch/name/" )
# ###############################################################################
# ####    helper to retrieve the URI 
# ####
#     
#     def dispatch(self, cmd):
#         """
#         """
#         #method_name =  "cmd_" + str(cmd)
#         print("@"*10)
#         print(cmd)
#         underscore_cmd = cmd.replace("-", "_")
#         print("@"*10)
#         try:
#             m = getattr(get_top_level_list_fibrechannel_switch(),underscore_cmd)
#             
#         except AttributeError:
#             print(method_name, "not found")
#         
#         return(m)
# 
# def _url( sw_ip, wwn, path, cmd, fid=-1 ):
#     """
#     """
#     if fid > 0:
#         print("#"*80)
#         a = "http://" + sw_ip  + path + wwn + "/" + cmd + "?vf-id=" + str(fid)
#         print(a)
#         print("#"*80)
#         return("http://" + sw_ip  + path + wwn + "/" + cmd + "?vf-id=" + str(fid))
#         
#     else:
#         return("http://" + sw_ip  + path + wwn + "/" + cmd)

# def add_task(summary, description=""):
#     """
#     """
#     return(requests.post(_url('/rest/')))

# def get_tasks(command, switch_ip, wwn, Auth_send, list_name, fid = -1):
#     """ 
#     """
#     #sem = get_top_level_list_fibrechannel_switch()
#     #p = sem.dispatch(command)
#     #print("==================  get tasks function   ===================")
#     #print("M"*80)
#     
#     
#     
#     if list_name == "fc_switch":
#         top_level = "/rest/running/switch/fibrechannel-switch/name/"
#         
#     if list_name == "fab_switch":
#         top_level = "/rest/running/fabric/fabric-switch/name/"
#        
#     cmplt_path = _url(switch_ip, wwn, top_level, command , fid)
#     r = requests.get(cmplt_path, headers=Auth_send)
# 
#     return(r)
#     
# def get_fc_switch_leaf(switch_ip, wwn, Auth_send, word, fid = -1):
#     """return the info for a specified leaf in the module
#         brocade-fibrecahnnel-switch  yang file 
#     
#     """
#     #vf_id = doc.Response.fibrechannel_switch.vf_id.cdata
#     # s = get_tasks('vf-id', switch_ip, wwn, Auth_send)   ## command from below
#     s = get_tasks(word,switch_ip, wwn,Auth_send, "fc_switch", fid )
#     
#     doc = untangle.parse(s.text)
#     try:
#             
#         if "vf-id" == word:
#             done = doc.Response.fibrechannel_switch.vf_id.cdata
#         if "domain-id" == word:
#             done =  doc.Response.fibrechannel_switch.domain_id.cdata
#         if "fcid"  == word:
#             done =  doc.Response.fibrechannel_switch.fcid.cdata
#         if "user-friendly-name" == word:
#             done =  doc.Response.fibrechannel_switch.user_friendly_name.cdata
#         if "enabled-state" == word:
#             done =  doc.Response.fibrechannel_switch.enabled_state.cdata
#         if "up-time"  == word:
#             done =  doc.Response.fibrechannel_switch.up_time.cdata
#         if "model" == word:
#             done = doc.Response.fibrechannel_switch.model.cdata
#         if "firmware-version"  == word:
#             done =  doc.Response.fibrechannel_switch.firmware_version.cdata
#         if "ip-address"  == word:
#             done =  doc.Response.fibrechannel_switch.ip_address.ip_address.cdata        
#         if "domain-name"  == word:
#             done =  doc.Response.fibrechannel_switch.domain_name.cdata
#         if "fabric-user-friendly-name"  == word:
#             done =  doc.Response.fibrechannel_switch.fabric_user_friendly_name.cdata
#         if "ag-mode"  == word:
#             done =  doc.Response.fibrechannel_switch.ag_mode.cdata    
#         if "principal"  == word:
#             done =  doc.Response.fibrechannel_switch.principal.cdata 
#     #    'domain-id', 'user-friendly-name', 'fcid', 'vf-id', 'principal', 'enabled-state',
#     #    'up-time', 'model', 'firmware-version', 'ip-address', 'domain-name', 'fabric-user-friendly-name', 'ag-mode'
#     except AttributeError:
#         print("Error during untangle - None was returned")
#         done = "Untangle Error"
#     except:
#         print("Error in untagle" , sys.exc_info()[0] )
#         done = "Untangle Error"
#     return(done)



###############################################################################
###############################################################################
####
####
####
# ###############################################################################
# def pa_stuff(pa):
#     print(pa.ip)
#     print(pa)
#     print(pa.ip)
#     print(pa.fid)
#     print(pa.user)
#     print(pa.pw)
#     print(pa.quiet)
#     print(pa.verbose)
#     print(pa.cmdprompt)
#     print("@"*40)
#  
#     return()
# 

def main():
    
    
    pa = parse_args(sys.argv)
    print(pa)
    print(pa.ip)
    print(pa.fid)
    print(pa.user)
    print(pa.pw)
    print(pa.quiet)
    print(pa.verbose)
    print(pa.cmdprompt)
    print("@"*40)
    print("="*80)
  
###############################################################################
###############################################################################
####
####    create object  to be able to send rest commands
####
 ###############################################################################
###############################################################################

    sm = rest_cmd_lib.rest_cfg(pa)
    sm.test()            ################### this can be removed 
    
    #r31 = sm.get_wwn(31)
    #rd = sm.get_wwn()
    # print("="*80)
    # print(r31)
    # print("="*80)
    # print("#"*80)
    # print("wwn "*20)
    # print(r31)
    # print("#"*80)
    # print("wwn "*20) 
    #print(rd)
    #print("#"*80)
    #print("wwn "*20)
    ###########################################################################
    ###########################################################################
    ####
    ####   Container        switch
    ####     list                  fibrechannel-switch
    ####     
    ####     leaf                   domain-id
    ####
    #r = requests.get("http://10.38.34.192/rest/running/switch/fibrechannel-switch", headers=Auth_send)

    #wwn = rd
    #wwn31 =  r31
    
###############################################################################
###############################################################################
####
####     get the Autherization and wwn for the fid to 
####         
###############################################################################
###############################################################################

    wwn = sm.get_wwn(pa.fid)
    wwn = sm.get_wwn(14)
    Auth_send = sm.get_Auth()

    r = requests.get("http://%s/rest/running/switch/fibrechannel-switch"  % ( pa.ip) , headers=Auth_send)
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)
    r = requests.get("http://%s/rest/running/switch/fibrechannel-switch/name/%s" % (pa.ip, wwn) , headers=Auth_send)
     
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)
    # 
    # r = requests.get("http://%s/rest/running/fabric/fabric-switch" % (pa.ip) , headers=Auth_send)
    #  
    # print("@"*80)
    # print(r.text)
    # print("@"*80)
    # print("@"*80)
    #   
    # r = requests.get("http://%s/rest/running/fabric/fabric-switch?vf-id=31" % (pa.ip) , headers=Auth_send)
    # 
    # print("@"*80)
    # print(r.text)
    # print("@"*80)
    # print("@"*80)
    # 
    # #r = requests.get("http://%s/rest/running/fabric/fabric-switch/name/%s/fcid/?vf-id=31" % (pa.ip,wwn31) , headers=Auth_send)
    # #r = requests.get("http://%s/rest/running/fabric/fabric-switch/name/%s/fcid" % (pa.ip,wwn) , headers=Auth_send)
    # r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg/cfg-name/cfg-name/%s/fcid" % (pa.ip,wwn) , headers=Auth_send)
    # print("@"*80)
    # print(r.text)
    # print("@"*80)
    # print("@"*80)
    # 
    # # friendly_name_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "switch-user-friendly-name" ) 
    # # 
    # # print("=G"*80)
    # # print("=G"*80)    
    # # print("User Friendly name")
    # # print(friendly_name_from_fabric_switch)
    # # 
    print("=H"*80)
    print("=H"*80)
    domain_id_from_fabric_switch = sm.fs_leaf( "domain-id" , wwn)

    wwn_from_fabric_switch = sm.fs_leaf( "chassis-wwn" , wwn)
    chass_friendly_name_from_fabric_switch = sm.fs_leaf("chassis-user-friendly-name" , wwn)
    friendly_name_from_fabric_switch  = sm.fs_leaf(  "switch-user-friendly-name" , wwn) 
    pricipal_from_fabric_switch = sm.fs_leaf( "principal" , wwn)
    fcid_from_fabric_switch = sm.fs_leaf( "fcid" , wwn)
    ipaddr_from_fabric_switch = sm.fs_leaf( "ip-address", wwn)
    fcipaddr_from_fabric_switch = sm.fs_leaf( "fcip-address" , wwn)
    ipv6addr_from_fabric_switch = sm.fs_leaf( "ipv6-address" , wwn)
    firmrev_from_fabric_switch = sm.fs_leaf("firmware-version" , wwn) 
          
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print(friendly_name_from_fabric_switch)
    print(wwn_from_fabric_switch)
    print(domain_id_from_fabric_switch)
    print(pricipal_from_fabric_switch )  
    print(fcid_from_fabric_switch )  
    print(ipaddr_from_fabric_switch )  
    print(fcipaddr_from_fabric_switch ) 
    print(ipv6addr_from_fabric_switch )
    print(firmrev_from_fabric_switch )
    print(chass_friendly_name_from_fabric_switch)
        
    print("=T"*80)
    print("=T"*80)
       
    
    
    test_error_message = sm.fs_leaf("jibberish" , wwn) 
    print("=T"*80)
    print("=T"*80)
     
    
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################  
    
    
    
    # if group == "fs":
    # #if group == "all":
    #     friendly_name_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "switch-user-friendly-name" ) 
    #     wwn_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "chassis-wwn" ) 
    #     chass_friendly_name_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "chassis-user-friendly-name" )
    #     domain_id_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "domain-id" )
    #     pricipal_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "principal" )
    #     fcid_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn31,Auth_send, "fcid" ,31)
    #     ipaddr_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn31,Auth_send, "ip-address" ,31)
    #     fcipaddr_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn31,Auth_send, "fcip-address" ,31 )
    #     ipv6addr_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "ipv6-address" )
    #     firmrev_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "firmware-version" ) 
    #     
    #     print(wwn_from_fabric_switch)
    # 
    #if group == "fc":
    #if group == "all":
    # principal_switch = get_fc_switch_leaf(pa.ip, wwn31,Auth_send, "principal" , 31) 
    # vf_state = get_fc_switch_leaf(pa.ip, wwn31,Auth_send, "vf-id", 31)
    # principal_switch = get_fc_switch_leaf(pa.ip, wwn31,Auth_send, "principal" , 31)
    # domain_id =  get_fc_switch_leaf(pa.ip, wwn,Auth_send, "domain-id")
    # fcid =  get_fc_switch_leaf(pa.ip, wwn,Auth_send, "fcid")
    # user_friendly_name =  get_fc_switch_leaf(pa.ip, wwn,Auth_send, "user-friendly-name")
    # enabled_state = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "enabled-state")
    # up_time = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "up-time")
    # model = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "model")
    # firmware_version= get_fc_switch_leaf(pa.ip, wwn,Auth_send, "firmware-version")
    # ip_address = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "ip-address")
    # domain_name  = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "domain-name")
    # fabric_u_f_name  = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "fabric-user-friendly-name")
    # ag_mode  = get_fc_switch_leaf(pa.ip, wwn,Auth_send, "ag-mode")
    # 
    # 
    # rr = requests.get("http://%s/rest/running/brocade-interface/fibrechannel?vf-id=31" % (pa.ip) , headers=Auth_send)
    # print("@_G"*40)
    # print(rr.text)
    # print("@"*80)
    # print("@_E"*40)
    # 
    # prt = "0%2f23"
    # r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/%s/crc-errors?vf-id=31" % (pa.ip,prt) , headers=Auth_send)
    # #r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/name" % (pa.ip ) , headers=Auth_send)
    # print("@_G"*40)
    # print(r.text)
    # try:
    #     d = untangle.parse(r.text)
    #     dd = untangle.parse(rr.text)
    #     print("@_B_"*40)
    #     print(r.content)
    #     print("@_B_"*40)
    #     print(r.url)
    #     print("@_B_"*40)
    #     print(d)
    #     print("@_B_"*40)
    #     done = d.Response.fibrechannel_statistics.crc_errors.cdata
    #     print(done)
    #     print("END_"*40)
    #     done = d.Response.fibrechannel_statistics.name.cdata
    #     print(done)
    #     print("END_"*40)
    # 
    #     done = dd.Response.fibrechannel[0].name.cdata
    #     print(done)
    #     print("END_3"*40)
    #     
    #     ll = len(dd.Response.fibrechannel)
    #     print("length  %s   " %  ll)
    #     
    #     port_list = []
    #     for x in range(ll):
    #         print(x)
    #         
    #         pl = dd.Response.fibrechannel[x].name.cdata
    #         print(pl)
    #         print(type(dd.Response.fibrechannel[x].name.cdata))
    #         port_list += [pl]
    #     print(port_list)
    #     
    #     done = dd.Response.fibrechannel[0].name.cdata
    #     print(done)
    #     print("END_3"*40)
    #     
    #     
    # except:
    #     print("Error in untagle" , sys.exc_info()[0] )
    #     done = "Untangle Error"
    #     
    # print("@"*80)
    # print("@_E_"*40)
    # 
    # 
    # prt = "0%2f23"
    # #####   
    # r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/%s/in-link-resets?vf-id=31" % (pa.ip, prt) , headers=Auth_send)
    # 
    # print("@_H"*40)
    # print(r.text)
    # print("@"*80)
    # print("@_E"*40)
    # 
    # #bfc_wwn = get_bfc_wwn()
    # 
    # 
    # 
    # 
    # 
    # if pa.verbose > 0:
    #     print("vf_id                                 :  %s  "  % vf_state)
    #     print("principal switch                      :  %s "  %  principal_switch)
    #     print("domian_id                             :  %s  " % domain_id)
    #     print("fcid                                  :  %s  " % fcid )
    #     print("user_friendly_name                    :  %s  "  %  user_friendly_name)
    #     print("switch state                          :  %s  " % enabled_state )
    #     print("up-time                               :  %s  "  %  up_time)
    #     print("model                                 :  %s   "  %  model)
    #     print("firmware-version                      :  %s  "  % firmware_version)
    #     print("ip-address                            :  %s  "  %  ip_address)
    #     print("domain-name                           :  %s  "  %  domain_name)
    #     print("fabric-user-friendly-name             :  %s  "  % fabric_u_f_name)
    #     print("ag-mode                               :  %s  "  % ag_mode)
    #     
    # print("&"*80)
    # time.sleep(1)
    # 
    #firmrev_from_fabric_switch = get_fabric_switch_leaf(pa.ip, wwn,Auth_send, "firmware-version" ) 
    #print(firmrev_from_fabric_switch)
    
    #r = requests.post("http://%s/rest/logout" % pa.ip , headers=Auth_send)
    #print(r.status_code)
        
    r = sm.rest_logout()
    print(r.status_code)
    
    #sys.exit()
    
    
   

if __name__ == '__main__':
    
    main()
