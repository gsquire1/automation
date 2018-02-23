#!/usr/bin/env python3

import sys, os
sys.path.append('/home/automation/lib/FOS')
#sys.path.append('/home/automation/lib/MAPS')
#sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')


import requests
import json
import re    
import time
import untangle
import logging
import argparse
import rest_cmd_lib
###############################################################################
###############################################################################
#sys.path.append('/home/automation/lib/FOS')

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
    #print(args)
    
    return(parser.parse_args())

#sys.path.append ("/opt/python/lib/python3.4/site-packages/")
###################################
###################################

#ip = '10.38.36.33'

# def _url(path):
#     """
#     """
#     #return('http:// ip  + path)
# 
# 
# def add_task(summary, description=""):
#     """
#     """
#     return(requests.post(_url('/rest/login')))
# 
# def get_tasks():
#     """
#     """
#     return(request.get(_url('')))
    
    
def main():
    
    pa = parse_args(sys.argv)
    # print(pa)
    # print(pa.ip)
    # print(pa.fid)
    # print(pa.user)
    # print(pa.pw)
    # print(pa.quiet)
    # print(pa.verbose)
    # print(pa.cmdprompt)
    # print("@"*40)
    # print("="*80)
    
    sm = rest_cmd_lib.rest_cfg(pa)

    Auth_send = sm.get_Auth()
    wwn = sm.get_wwn(pa.fid)
    
    #print(wwn)

    #r = requests.post("http://%s/rest/login" % ip, auth=('admin','password'))
    #print(r.text)
    #print(r.headers)
    # print('((((((((((((((((((AUTH HERE))))))))))))))))))')
    # Auth_send = sm.get_Auth()
    # 
    # print(Auth_send)
    # print('((((((((((((((((((WWN HERE))))))))))))))))))')
    # wwn = sm.get_wwn(pa.fid)
    # print(wwn)
    # Auth = r.headers.get('Authorization')
    # #print(r.status_code)
    # #print(Auth)
    # Auth_send={'Authorization':'%s'%Auth}
    # print(Auth_send)
    # # print(r.text)
    # # print(r.headers)
    # # print(r.cookies)
    
    ###########################################################################
    ###########################################################################
    ####
    ####   fibrechannel-switch
    ####     
    ####   GET WWN from 'fibrechannel-switch'
    ####

    print('((((((((((((((((((WWN STARTS HERE))))))))))))))))))')
    fs = requests.get("http://%s/rest/running/switch/fibrechannel-switch" % pa.ip , headers=Auth_send)
    print(fs.json)
    print(fs.text)
    print(fs.headers)
    ras = re.compile('name>([\:0-9a-f]+)</n')
    ras = ras.findall(fs.text)
    #print(type(ras))
    #print(ras)
    wwn = ras[0]
    print(wwn)
    print('((((((((((((((((((WWN ENDS HERE))))))))))))))))))')
    
    logger.info('Start of rest commands')

    r = requests.get("http://%s/rest/running/zoning/defined-configuration"  % ( pa.ip) , headers=Auth_send)
    #r = requests.get("http://%s/rest/running/zoning/defined-configuration"  % ( pa.ip) , headers=Auth_send)
    print("@"*80)
    print(r.text)
    print("@"*80)
    print("@"*80)
    a = r.text
    doc = untangle.parse(a)
    a = doc.Response.defined_configuration.cfg.cfg_name.cdata
    print(a)
    
    print('LOGOUT____HERE')
    r = requests.post("http://%s/rest/logout"% pa.ip, headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    if r.status_code == 204:
        print("successful logout\n\n")
    else:
        print("logout was not successful\n\n")
    sys.exit(0)

    #print("=H"*80)
    #print("=H"*80)

    logger.info('@'*120)
    logger.info('================ Start of Fabric Switch commands ===================')
    
    defined_configuration_from_fabric_switch = sm.zone_defined_leaf("defined-configuration" , pa.fid)
    logger.info("defined-configuration is  :  %s " %  defined_configuration_from_fabric_switch)
    
    alias_from_fabric_switch = sm.zone_defined_leaf("alias" , pa.fid)
    alias_names = sm.alias_names(pa.fid)
    print(alias_names)
    logger.info("defined-configuration is  :  %s " % alias_from_fabric_switch)
    
    # domain_id_from_fabric_switch = sm.fs_leaf( "domain-id" , wwn, pa.fid)
    # logger.info("domain id is  :  %s " %  domain_id_from_fabric_switch)
    
    logger.info('End of domain-id command =====================================')
    logger.info('@'*120)
    
                ####   LOGOUT   ####
    print('LOGOUT____HERE')
    r = requests.post("http://%s/rest/logout"% pa.ip, headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    if r.status_code == 204:
        print("successful logout\n\n")
    else:
        print("logout was not successful\n\n")
    sys.exit(0)
    
    print('\n\n\n')   
    print('(((((((((((((((((((((1111111 ZONING)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    print('(((((((((((((((((((((222222222 ALIAS LIST)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/alias/" % paip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    print('(((((((((((((((((((((3333333 LIST OF MEMBER(S)IN ALIAS)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/alias/alias-name/Z/" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('(((((((((((((((((((((4444444  MEMBERS ENTRY IN ALIAS)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/alias/alias-name/Z/member-entry" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('(((((((((((((((((((((5555555  ALIAS ENTRY NAME)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/alias/alias-name/Z/member-entry" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('(((((((((((((((((((((AAAAAA CFG LIST)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('(((((((((((((((((((((BBBBBB CFG LIST FID 10)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg/cfg-name/FID_10" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('(((((((((((((((((((((BBBBBB CFG MEMBER-ZONE FID 10)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg/cfg-name/FID_10/member-zone" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('((((((((((((((((((((( CCCCCC CFG ZONE NAME FID 10)))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg/cfg-name/FID_10/member-zone/zone-name" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    print('((((((((((((((((((((( 1111111 DEFINED-CONFIG ZONE ))))))))))))))))))))')
    r = requests.get("http://%s/rest/running/zoning/defined-configuration/zone" % pa.ip,  headers=Auth_send)
    print(r.json)
    print(r.text)
    
    # print('\n\n\n')   
    # print('(((((((((((((((((((((EFFECTIVE_CONFIGURATION)))))))))))))))))))))')
    # r = requests.get("http://10.38.36.33/rest/running/zoning/effective-configuration",  headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # #print(r.headers)
    
    # print('\n\n\n')
    # print('(((((((((((((((((((((DEFINED_CONFIGURATION)))))))))))))))))))))))')    
    # r = requests.get("http://%s/rest/running/zoning/defined-configuration" % ip,  headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # #print(r.headers)
    # 
    # print('\n\n\n')
    # print('(((((((((((((((((((((DEFINED_CONFIGURATION_TESTING)))))))))))))))))))))))')    
    # r = requests.get("http://%s/rest/running/zoning/defined-configuration/cfg/cfg-name/FID_10/member-zone/zone-name/" % ip,  headers=Auth_send)
    # print(r.json)
    # print(r.text)
    # print(r.headers)
    
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
    r = requests.post("http://%s/rest/logout"% pa.ip, headers=Auth_send)
    #print(r.json)
    print(r.status_code)
    if r.status_code == 204:
        print("successful logout\n\n")
    else:
        print("logout was not successful\n\n")
    sys.exit(0)
    

if __name__ == '__main__':
    
    main()
