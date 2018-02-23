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
import untangle
import logging

import logging
import argparse
import rest_cmd_lib
###############################################################################
###############################################################################
####
####  enable logger 
####
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
###############################################################################
###############################################################################
####   END of configuring Logger     -  ii is before the first  function  to make it global
###############################################################################
###############################################################################


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    pp.add_argument("ip", help="IP address of SUT")
    #pp.add_argument("fid", type=int, default=-1, help="Choose the FID to operate on")
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
    parser.add_argument("-f", "--fid", type=int, default=-1, help="Fid number of Switch VF to be tested - leave blank for non VF switch")
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
    
    if args.fid > 128 or args.fid < 1:
        if args.fid == -1:
            pass
        else:
            print("\n\nFID must be between 1 and 128  or blank for pizza box\n\n")
            sys.exit()
    
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
####     get the Autherization and wwn for the fid to
####
###############################################################################
###############################################################################

    sm = rest_cmd_lib.rest_cfg(pa)
 
    wwn = sm.get_wwn(pa.fid)
    Auth_send = sm.get_Auth()

###############################################################################
###############################################################################
####
####    do some testing here
####
###############################################################################
###############################################################################

    logger.info('Start of rest commands')

    domain_id_from_fcs = sm.fcs_leaf( "domain_id" ,  pa.fid)
    

    logger.info('@'*120)
    logger.info('================ Start of Fabric Switch commands ===================')
    logger.info("from lib  :  %s  " % domain_id_from_fcs )
    logger.info('End of domain-id command =====================================')
    logger.info('@'*120)

    wwn_from_fabric_switch = sm.fs_leaf( "fcid" , pa.fid)
    # chass_friendly_name_from_fabric_switch = sm.fs_leaf("chassis-user-friendly-name" , wwn, pa.fid)
    # friendly_name_from_fabric_switch  = sm.fs_leaf(  "switch-user-friendly-name" , wwn, pa.fid) 
    # pricipal_from_fabric_switch = sm.fs_leaf( "principal" , wwn, pa.fid)
    # fcid_from_fabric_switch = sm.fs_leaf( "fcid" , wwn, pa.fid)
    # ipaddr_from_fabric_switch = sm.fs_leaf( "ip-address", wwn, pa.fid)
    # fcipaddr_from_fabric_switch = sm.fs_leaf( "fcip-address" , wwn, pa.fid)
    # ipv6addr_from_fabric_switch = sm.fs_leaf( "ipv6-address" , wwn, pa.fid)
    # firmrev_from_fabric_switch = sm.fs_leaf("firmware-version" , wwn, pa.fid) 
 

    wwn_from_fabric_switch = sm.fs_leaf( "name" , pa.fid)
    chass_wwn_fs                   = sm.fs_leaf("chassis_wwn", pa.fid)
    domain_id_fs                    = sm.fs_leaf("domain_id", pa.fid)
    fcid_fs                                =  sm.fs_leaf("fcid", pa.fid)
    fcid_hex_fs                       =   sm.fs_leaf("fcid_hex", pa.fid)
    switch_name_fs                =   sm.fs_leaf("switch_user_friendly_name", pa.fid)
    chass_name_fs                =   sm.fs_leaf("chassis_user_friendly_name", pa.fid)
    firmver_fs                        =   sm.fs_leaf("firmware_version", pa.fid)
    ip_addr_fs                       =   sm.fs_leaf("ip_address", pa.fid)
    fcip_addr_fs                     =   sm.fs_leaf("fcip_address", pa.fid)
    ipv6_addr_fs                    =   sm.fs_leaf("ipv6_address", pa.fid)
    principal_fs                      =   sm.fs_leaf("principal", pa.fid)
    
    
    
    
    print("info from fabric switch leaf")
    
    print("=SM"*24)
    print("=SM"*24)
    
    print(wwn_from_fabric_switch)
    print(chass_wwn_fs)
    print(domain_id_fs)
    print(fcid_fs)
    print(fcid_hex_fs)
    print(switch_name_fs  )
    print(chass_name_fs )
    print(firmver_fs )
    print(ip_addr_fs )
    print(fcip_addr_fs )
    print(ipv6_addr_fs )
    print(principal_fs )
    
    print("WWN from get_wwn function")
    print(wwn)
    
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
    print("=T"*80)
 
    test_error_message = sm.fs_leaf("jibberish" , 22) 
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
    
    wwn_from_fcs                 =  sm.fcs_leaf("name", pa.fid)
    domain_id_from_fcs = sm.fcs_leaf( "domain_id" , pa.fid)
    fcid_fcs                               =  sm.fcs_leaf("fcid" , pa.fid)
    fcid_hex_fcs                       =   sm.fcs_leaf("fcid_hex" , pa.fid)
    user_friendly_name_fcs   =   sm.fcs_leaf("user_friendly_name", pa.fid)
    enabled_state_from_fcs = sm.fcs_leaf( "enabled_state" , pa.fid)
    uptime_fcs                        =  sm.fcs_leaf("up_time", pa.fid)
    domain_name_from_fcs = sm.fcs_leaf( "domain_name" , pa.fid)    
    principal_fcs                     =  sm.fcs_leaf("principal", pa.fid)
    
    ip_addr_fcs                       =   sm.fcs_leaf("ip_address" , pa.fid)
    model_from_fcs               =  sm.fcs_leaf("model" , pa.fid)
    firmver_fcs                       =  sm.fcs_leaf("firmware_version", pa.fid)
    vf_id_from_fcs                  =  sm.fcs_leaf("vf_id", pa.fid)
    fabric_name_from_fcs    = sm.fcs_leaf( "fabric_user_friendly_name" ,  pa.fid)
    ag_mode_from_fcs          = sm.fcs_leaf( "ag_mode" , pa.fid)
    
    
    
    
    
#  
#         
# 
# ###############################################################################
# ###############################################################################
# ####
# ####  log the results
# ####
# ###############################################################################
# ###############################################################################
# 
    logger.info('@'*120)
    logger.info('@'*120)
    logger.info("wwn from fcs  is   :  %s"  %  wwn_from_fcs)

    logger.info("domain_id_from_fcs   :  %s " %  domain_id_from_fcs  )
    logger.info("fcid_fcs value is  :  %s " %  fcid_fcs )
    logger.info("fcid_hex_fcs  value is  :  %s " %  fcid_hex_fcs  )
    logger.info("user_friendly_name_fcs value is  :  %s " %  user_friendly_name_fcs )
    logger.info("enabled_state_from_fcs value is  :  %s " %  enabled_state_from_fcs )
    logger.info("domain_name_from_fcs    value is  :  %s " %  domain_name_from_fcs  )
    logger.info("principal_fcs   value is  :  %s " %  principal_fcs   )
    
    logger.info("ip_addr_fcs value is  :  %s " %  ip_addr_fcs )
    
    logger.info("model_from_fcs value is  :  %s " %   model_from_fcs)
    
    
    logger.info("firmver_fcs value is  :  %s " %  firmver_fcs )
    logger.info("vf_id_from_fcs value is  :  %s " %  vf_id_from_fcs )
    logger.info("fabric_name_from_fcs  value is  :  %s " %  fabric_name_from_fcs )   
    logger.info("ag_mode_from_fcs from fcs  is   :  %s"  %  ag_mode_from_fcs )
    
    logger.info('END==='*20)
    logger.info('===END'*20)
 
 
 
###############################################################################
###############################################################################
####
####
####
###############################################################################
###############################################################################

    #switch_info_name  =  fc_switch_info("name" , pa.fid)
    
    
    
    
    port_number_list = sm.port_numbers(pa.fid)
    
    
    #fc_stat_leaf            =  sm.fc_stats_leaf("model" , pa.fid)
    
    port_err_counts =  sm.port_err_stats(0, 7,  pa.fid)
        
    print(port_err_counts)

    #r = requests.post("http://%s/rest/logout" % pa.ip , headers=Auth_send)
    #print(r.status_code)
        
    r = sm.rest_logout()
    print(r.status_code)
    
    #sys.exit()
    
    
   

if __name__ == '__main__':
    
    main()
