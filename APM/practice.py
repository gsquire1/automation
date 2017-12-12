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
import logging

###############################################################################
###############################################################################
###############################################################################
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

####
####  file handler for logging
fh = logging.FileHandler('rest_switch_log_practice.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
####
####  console handler for logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)



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
    
###############################################################################
###############################################################################
####
####     get the Autherization and wwn for the fid to 
####         
###############################################################################
###############################################################################

    wwn = sm.get_wwn(pa.fid)
    Auth_send = sm.get_Auth()

###############################################################################
###############################################################################
####
####    do some testing
####
###############################################################################
###############################################################################

    logger.info('Start of rest commands')

    r = requests.get("http://%s/rest/running/switch/fibrechannel-switch"  % ( pa.ip) , headers=Auth_send)
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)

    print("=H"*80)
    print("=H"*80)

    logger.info('@'*120)
    logger.info('================ Start of Fabric Switch commands ===================')
    
    domain_id_from_fabric_switch = sm.fs_leaf( "domain-id" , wwn, pa.fid)
    logger.info("domain id is  :  %s " %  domain_id_from_fabric_switch)
    
    logger.info('End of domain-id command =====================================')
    logger.info('@'*120)


    wwn_from_fabric_switch = sm.fs_leaf( "chassis-wwn" , wwn, pa.fid)
    chass_friendly_name_from_fabric_switch = sm.fs_leaf("chassis-user-friendly-name" , wwn, pa.fid)
    friendly_name_from_fabric_switch  = sm.fs_leaf(  "switch-user-friendly-name" , wwn, pa.fid) 
    pricipal_from_fabric_switch = sm.fs_leaf( "principal" , wwn, pa.fid)
    fcid_from_fabric_switch = sm.fs_leaf( "fcid" , wwn, pa.fid)
    ipaddr_from_fabric_switch = sm.fs_leaf( "ip-address", wwn, pa.fid)
    fcipaddr_from_fabric_switch = sm.fs_leaf( "fcip-address" , wwn, pa.fid)
    ipv6addr_from_fabric_switch = sm.fs_leaf( "ipv6-address" , wwn, pa.fid)
    firmrev_from_fabric_switch = sm.fs_leaf("firmware-version" , wwn, pa.fid) 
          
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
 
    
    logger.info('@'*120)
    logger.info('================ Start of Fabric Switch commands ===================')
    r = requests.get("http://%s/rest/running/switch/fibrechannel-switch"  % ( pa.ip) , headers=Auth_send)
    print("@"*80)
    print(r.text)
    logger.info(r.text)
    print("@"*80)
    print("@"*80)
    print("=H"*80)
    print("=H"*80)

    ag_mode_from_fcs = sm.fcs_leaf( "ag-mode" , wwn, pa.fid)
    domain_id_from_fcs = sm.fcs_leaf( "domain-id" , wwn, pa.fid)
    domain_name_from_fcs = sm.fcs_leaf( "domain-name" , wwn, pa.fid)    
    enabled_state_from_fcs = sm.fcs_leaf( "enabled-state" , wwn, pa.fid)    
    fabric_name_from_fcs = sm.fcs_leaf( "fabric-user-friendly-name" , wwn, pa.fid)
        
 
        
        
        
        
        
        
        
    logger.info("agmode value is  :  %s " %  ag_mode_from_fcs)
    logger.info("domain id  value is  :  %s " %   domain_id_from_fcs)
    logger.info("domain name value is  :  %s " %  domain_name_from_fcs)
    logger.info("enabled state value is  :  %s " %  enabled_state_from_fcs)
    logger.info("fabric name  value is  :  %s " %  fabric_name_from_fcs)
     

    logger.info('End of domain-id command =====================================')
    logger.info('@'*120)

 
 
    #r = requests.post("http://%s/rest/logout" % pa.ip , headers=Auth_send)
    #print(r.status_code)
        
    r = sm.rest_logout()
    print(r.status_code)
    
    #sys.exit()
    
    
   

if __name__ == '__main__':
    
    main()
