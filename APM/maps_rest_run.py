#!/usr/bin/env python3

import os,sys
sys.path.append('/home/automation/lib/FOS')


import pprint
import requests
import json

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
####    START LOGGER SECTION for multiple log files
####
###############################################################################
###############################################################################
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
###############################################################################

def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to setup as many loggers as needed. 
    """
    handler   =  logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger  = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return(logger)

logger = setup_logger('logs/rest_logs/first_logger', 'first_logfile.log')
logger.info('This is just info message')
# super_logger = setup_logger('second_logger', 'second_logfile.log')
# super_logger.error('This is an error message')
mapsrule_response_logger = setup_logger("mapsrule_output", "logs/rest_logs/maps_rule_output.log")
mapsrule_response_logger.info("mapsrule Rest output")
#### use this to record the response from http to the command
cmd_response_logger  = setup_logger("command_logger", "logs/rest_logs/cmd_logger.log")
cmd_response_logger.info("log http response of each command")

 
    

###############################################################################
###############################################################################
####    END of LOGGER SECTION 
###############################################################################
###############################################################################

###############################################################################
###############################################################################
####
####    START PARSER SECTION
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
    if args.fid == "":
        args.fid = -1
        
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
####  END OF PARSER SECTION
###############################################################################
###############################################################################


###############################################################################
###############################################################################
####
####     MAIN SECTION
####
###############################################################################
###############################################################################
def main():
    
    pa = parse_args(sys.argv)
    pa_print(pa)
###############################################################################
###############################################################################
####
####    create object  to be able to send rest commands
####     get the Autherization code
####     get  wwn for the fid to
####
###############################################################################
###############################################################################

    sm = rest_cmd_lib.rest_cfg(pa)
    wwn = sm.get_wwn(pa.fid)
    Auth_send = sm.get_Auth()
    
    cmd_response_logger.info("WWN  %s  "  % wwn)
    cmd_response_logger.info("AUTH  %s  "  % Auth_send)
    
###############################################################################
###############################################################################
####
####    do some testing here
####
###############################################################################
###############################################################################
 ####   Get the list of Domains on the switch
 ####     hold these for later
 ####
    domain_id_from_fcs = sm.fcs_leaf( "domain_id" ,  pa.fid)
    print("GET DOMAIN IDS")
    domain_id_list           = sm.get_domain_ids()
    print("END GET DOMAIN IDS ")
 
    #wwn_from_fabric_switch = sm.fs_leaf( "fcid" , pa.fid)
    # chass_friendly_name_from_fabric_switch = sm.fs_leaf("chassis-user-friendly-name" , wwn, pa.fid)
    # friendly_name_from_fabric_switch  = sm.fs_leaf(  "switch-user-friendly-name" , wwn, pa.fid) 
    # pricipal_from_fabric_switch = sm.fs_leaf( "principal" , wwn, pa.fid)
    # fcid_from_fabric_switch = sm.fs_leaf( "fcid" , wwn, pa.fid)
    # ipaddr_from_fabric_switch = sm.fs_leaf( "ip-address", wwn, pa.fid)
    # fcipaddr_from_fabric_switch = sm.fs_leaf( "fcip-address" , wwn, pa.fid)
    # ipv6addr_from_fabric_switch = sm.fs_leaf( "ipv6-address" , wwn, pa.fid)
    # firmrev_from_fabric_switch = sm.fs_leaf("firmware-version" , wwn, pa.fid) 
 

#     wwn_from_fabric_switch = sm.fs_leaf( "name" , pa.fid)
#     chass_wwn_fs                   = sm.fs_leaf("chassis_wwn", pa.fid)
#     domain_id_fs                    = sm.fs_leaf("domain_id", pa.fid)
#     fcid_fs                                =  sm.fs_leaf("fcid", pa.fid)
#     fcid_hex_fs                       =   sm.fs_leaf("fcid_hex", pa.fid)
#     switch_name_fs                =   sm.fs_leaf("switch_user_friendly_name", pa.fid)
#     chass_name_fs                =   sm.fs_leaf("chassis_user_friendly_name", pa.fid)
#     firmver_fs                        =   sm.fs_leaf("firmware_version", pa.fid)
#     ip_addr_fs                       =   sm.fs_leaf("ip_address", pa.fid)
#     fcip_addr_fs                     =   sm.fs_leaf("fcip_address", pa.fid)
#     ipv6_addr_fs                    =   sm.fs_leaf("ipv6_address", pa.fid)
#     principal_fs                      =   sm.fs_leaf("principal", pa.fid)
# #    
 
    
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################  
    # 
    # wwn_from_fcs                 =  sm.fcs_leaf("name", pa.fid)
    # domain_id_from_fcs = sm.fcs_leaf( "domain_id" , pa.fid)
    # fcid_fcs                               =  sm.fcs_leaf("fcid" , pa.fid)
    # fcid_hex_fcs                       =   sm.fcs_leaf("fcid_hex" , pa.fid)
    # user_friendly_name_fcs   =   sm.fcs_leaf("user_friendly_name", pa.fid)
    # enabled_state_from_fcs = sm.fcs_leaf( "enabled_state" , pa.fid)
    # uptime_fcs                        =  sm.fcs_leaf("up_time", pa.fid)
    # domain_name_from_fcs = sm.fcs_leaf( "domain_name" , pa.fid)    
    # principal_fcs                     =  sm.fcs_leaf("principal", pa.fid)
    # 
    # ip_addr_fcs                       =   sm.fcs_leaf("ip_address" , pa.fid)
    # model_from_fcs               =  sm.fcs_leaf("model" , pa.fid)
    # firmver_fcs                       =  sm.fcs_leaf("firmware_version", pa.fid)
    # vf_id_from_fcs                  =  sm.fcs_leaf("vf_id", pa.fid)
    # fabric_name_from_fcs    = sm.fcs_leaf( "fabric_user_friendly_name" ,  pa.fid)
    # ag_mode_from_fcs          = sm.fcs_leaf( "ag_mode" , pa.fid)
    # 
#  
#         
# 

###############################################################################
###############################################################################
####
####    hold for later testing in maps
####
###############################################################################
###############################################################################
    
    port_number_list = sm.port_numbers(pa.fid)
    
    port_err_counts =  sm.port_err_stats(0, 7,  pa.fid)
        
 
###############################################################################
###############################################################################
####
####    MAPS Commands
####
###############################################################################
###############################################################################
####    get the MAPS rules for each FID
####
    # # if -1 == domain_id_list:
    # #     maps_monitor_rules                   = sm.maps_rules()       
    # # else:
    # #     for vf in domain_id_list:
    # #         vf = int(vf)
    # #         maps_monitor_rules                   = sm.maps_rules(vf)
####
####     how do you want to handle the FIDS   all or what's  is on command line
####
    if str(pa.fid) in domain_id_list:
        maps_monitor_rules                   = sm.maps_rules(pa.fid)
    
    maps_monitor_policy                    =   sm.maps_policy()
    maps_monitor_config                   =  sm.maps_config()
    
 #   maps_monitor_rules                     = sm.maps_rules()
    maps_monitor_rules = "END"

    if 4 >= 9999:
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
    #cmd_response_logger.info("mapsrules    \n\n   %s  " %  maps_monitor_rules)
    
    
    
    # logger.info("maps monitor switch status policy    :  %s "  %  maps_monitor_sspr )
    # logger.info("maps monitor system Resource        :  %s "  %  maps_monitor_system_resource)    
    # logger.info("maps monitor system matrix    :  %s "  %  maps_monitor_pause)    
    # logger.info("maps monitor group                 :  %s "  %  maps_monitor_group)
    # logger.info("maps monitor Config                        :  %s "  %  maps_monitor_config )
    # logger.info("maps monitor dashboard rules          :  %s "  %  maps_monitor_dashboard_rule)
    # logger.info("maps monitor dashboard misc          :  %s "  %  maps_monitor_dashboard_misc)  
    # logger.info("maps monitor rules                          :  %s "  %  maps_monitor_rules )
    # logger.info("maps monitor policy                          :  %s "  %  maps_monitor_policy) 
    # logger.info("maps monitor system matrix            :  %s "  %  maps_monitor_sys_matrix )
    # 
    # 
    # logger.info('=== MAPS END  ==='*8) 
    # logger.info("\n\n\n\n")
    # logger.info("@"*80)
    #
    
###############################################################################
###############################################################################
####
####     GET top level leaf data for the 10 sections
####
###############################################################################
###############################################################################
    print("TOP LEVEL"*40)
    m_config = sm.get_top_level("maps-config")
    logging.info(m_config)
    print(m_config)
    
    ms_matrix = sm.get_top_level("monitoring-system-matrix")
    logging.info(ms_matrix)
    print(ms_matrix)
    
    mm_rules = sm.get_top_level("rule")
    logging.info(mm_rules)
    print(mm_rules)
    
    sspolicy = sm.get_top_level("switch-status-policy-report")
    logging.info(sspolicy)
    print(sspolicy)
    
    maps_monitor_sspr                      = sm.maps_sspr()
    logging.info(maps_monitor_sspr)
    print(maps_monitor_sspr)
    
    s_resource =  sm.get_top_level("system-resources")
    logging.info(s_resource)
    print(s_resource)
        
    maps_monitor_system_resource  = sm.maps_system_resource(pa.fid)
    logging.info(maps_monitor_system_resource)
    print(maps_monitor_system_resource)

    p_config = sm.get_top_level("paused-cfg")
    logging.info(p_config)
    print(p_config)
    
    maps_group  = sm.get_top_level("group")
    logging.info(maps_group)
    print(maps_group)
    
    d_rule =  sm.get_top_level("dashboard-rule")
    logging.info(d_rule)
    print(d_rule)
          
    d_misc = sm.get_top_level("dashboard-misc")
    logging.info(d_misc)
    print(d_misc)
    
    m_policy = sm.get_top_level("maps-policy")
    logging.info(m_policy)
    print(m_policy)
    
    
    #post_something =  sm.set_paused_cfg()
    #print(post_something.status)
    post_something = sm.set_maps_config()
    
   
    
    
###############################################################################
###############################################################################
####
####     END of Session    LOGOUT here
####
###############################################################################
###############################################################################

    r = sm.rest_logout()
    #print(r.status_code)
    print(m_config.text)
    #sys.exit()
    

    ####################################
    #####################################
    ####   make the group into a dictionary
    ####
    ####
    ####
    
    
    print(json.dumps(maps_monitor_rules, indent=2))
    print("&"*80)
    print("#"*80)
    print(json.dumps(maps_monitor_config))
    print("&"*80)
    print("#"*80)
    
    if 4 >= 999:
            
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
    
    print("#"*80)
    print(domain_id_list)
    print("@---"*30)
    print("port list  ")
    print(port_number_list)
    print("==---"*30)
    
    
    if 'Fail' in maps_monitor_rules :
        print("MAPS Monitor Rules                          %s  "  % maps_monitor_rules )
    else:
        print("MAPS Monitor Rules                          PASS")
 
 
    if 4 > 9999:
            
        
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
