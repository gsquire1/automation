#!/usr/bin/env python3

import os,sys
sys.path.append('/home/automation/lib/FOS')
#sys.path.append('/home/automation/lib/MAPS')
#sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')

import pprint
import requests
import json
# import  re
# import os
# import sys     
# import time
import xmltodict
import untangle
import logging

import logging
import argparse
import rest_cmd_lib
from lxml import etree as ET



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
####
####   PARSER SECTION
####
###############################################################################
###############################################################################

def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    pp.add_argument("ip", help="IP address of SUT")
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
    
    args = parser.parse_args()
    print(args)
    
    if args.fid > 128 or args.fid < 1:
        print(args.fid)
        
        if args.fid == -1:
            pass
        else:
            print("\n\nFID must be between 1 and 128  or blank for pizza box\n\n")
            sys.exit()
    
    return(parser.parse_args())


def pa_print(pa):
        
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
        return(True)
    
###############################################################################
###############################################################################
####     END PARSER SECTION
###############################################################################
###############################################################################

def main():
    
    
    pa = parse_args(sys.argv)
    pa_print(pa)

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

    #wwn_from_fabric_switch = sm.fs_leaf( "fcid" , pa.fid)
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
 
    #SStest_error_message = sm.fs_leaf("jibberish" , 22) 
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
# #########################indent######################################################
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

    
    port_number_list = sm.port_numbers(pa.fid)
    
    port_err_counts =  sm.port_err_stats(0, 7,  pa.fid)
        
    #print(port_err_counts)

###############################################################################
###############################################################################
####
####    MAPS Commands
####
###############################################################################
###############################################################################
    logger.info('=== MAPS Start ==='*6)
    
    
    maps_monitor_rules                     = sm.maps_rules()
    maps_monitor_sspr                      = sm.maps_sspr()
    maps_monitor_system_resource  = sm.maps_system_resource(pa.fid)
    maps_monitor_config                   =  sm.maps_config()
    maps_monitor_policy                    =   sm.maps_policy()
    maps_monitor_sys_matrix            =  sm.maps_matrix()
    maps_monitor_pause                    = sm.maps_pause_con()
    maps_monitor_group                    = sm.maps_group()
    maps_monitor_dashboard_rule   =  sm.maps_dashboard_rule()
    maps_monitor_dashboard_misc   =   sm.maps_dashboard_misc()
    
    
    ####   this will be all of the allowed settings
    ####     
    
    logger.info("maps monitor switch status policy    :  %s "  %  maps_monitor_sspr )
    logger.info("maps monitor system Resource        :  %s "  %  maps_monitor_system_resource)    
    logger.info("maps monitor system matrix    :  %s "  %  maps_monitor_pause)    
    logger.info("maps monitor group                 :  %s "  %  maps_monitor_group)
    logger.info("maps monitor Config                        :  %s "  %  maps_monitor_config )
    logger.info("maps monitor dashboard rules          :  %s "  %  maps_monitor_dashboard_rule)
    logger.info("maps monitor dashboard misc          :  %s "  %  maps_monitor_dashboard_misc)  
    logger.info("maps monitor rules                          :  %s "  %  maps_monitor_rules )
    logger.info("maps monitor policy                          :  %s "  %  maps_monitor_policy) 
    logger.info("maps monitor system matrix            :  %s "  %  maps_monitor_sys_matrix )


    logger.info('=== MAPS END  ==='*8) 
    logger.info("\n\n\n\n")
    logger.info("@"*80)
            
###############################################################################
###############################################################################
####
####     END of Session    LOGOUT here
####
###############################################################################
###############################################################################

    r = sm.rest_logout()
    print(r.status_code)
    
    #sys.exit()
    
    
    ####################################
    #####################################
    ####   make the group into a dictionary
    ####
    ####
    ####

    print(maps_monitor_group)
     
    pprint.pprint(maps_monitor_group["Response"]['group'], indent=1)
  
    print(json.dumps(maps_monitor_group, indent=1))
   
   
    print("&"*80)
    print("#"*80)
    print("&"*80)
    print("#"*80)
    print("&"*80)
    print("#"*80)
   
 
    print(json.dumps(maps_monitor_rules, indent=2))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_sspr, indent=2))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_system_resource, indent=2))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_config, indent=2)) 
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_policy, indent=3 ))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_sys_matrix,  indent=2))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_pause , indent=2))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_group, indent=1))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_dashboard_rule, indent=2))  
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_dashboard_misc, indent=1))
    print("&"*80)
    print("#"*80)
    
    ###########################################################################
    ###########################################################################
    ####
    ####  Print a Summary of MAPS Rest  
    ####
    ###########################################################################
    ###########################################################################
    
    if 'Fail' in maps_monitor_rules :
        print("MAPS Monitor Rules                          %s  "  % maps_monitor_rules )
    else:
        print("MAPS Monitor Rules                          PASS")
 
 
    
    if 'Fail' in maps_monitor_sspr :
        print("MAPS Monitor Switch Status Policy           %s  " % maps_monitor_sspr )
    else:
        print("MAPS Monitor Switch Status Policy           PASS")
    
    if 'Fail' in maps_monitor_system_resource:
        print("MAPS Monitor System Resource                %s  " % maps_monitor_system_resource)
    else:
        print("MAPS Monitor System Resource                PASS")
    if 'Fail' in maps_monitor_config:
        print("MAPS Monitor Config                         %s " %  maps_monitor_config)
    else:
        print("MAPS Monitor Config                         PASS")
    
    if 'Fail' in maps_monitor_policy:
        print("MAPS Monitor Policy                         %s " % maps_monitor_policy)
    else:
        print("MAPS Monitor Policy                         PASS")
    
    if 'Fail' in maps_monitor_sys_matrix:
        print("MAPS Monitor SYS Matrix                     %s  "  % maps_monitor_sys_matrix)
    else:
        print("MAPS Monitor SYS Matrix                     PASS")
    if 'Fail' in maps_monitor_pause:
        print("MAPS Monitor Pause                          %s   "  % maps_monitor_pause )
    else:
        print("MAPS Monitor Pause                          PASS")
    
    if 'Fail' in maps_monitor_group:
        print("MAPS Monitor Group                          %s  "  %  maps_monitor_group)
    else:
        print("MAPS Monitor Group                          PASS")
    
    if 'Fail' in maps_monitor_dashboard_rule:
        print("MAPS Monitor Dashboard Rule                 %s  "  %  maps_monitor_dashboard_rule)
    else:
        print("MAPS Montior Dashboard Rule                 PASS")
    
    if 'Fail' in maps_monitor_dashboard_misc:
        print("MAPS Monitor Dashboard Misc                 %s   "   %  maps_monitor_dashboard_misc)
    else:
        print("MAPS Monitor Dashboard Misc                 PASS")
    
    
    #print(json.dumps(maps_monitor_dashboard_rule, indent=2))  
    #print(json.dumps(maps_monitor_dashboard_misc, indent=1))
    print("&"*80)
    print("#"*80)
    print("&"*80)
    print("#"*80)
    
###############################################################################
###############################################################################
###############################################################################
###############################################################################



if __name__ == '__main__':
    
    main()
