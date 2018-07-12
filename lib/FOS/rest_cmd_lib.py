#!/usr/bin/env python3


import requests
import untangle
import sys
import logging
import xmltodict
import json
import pprint

#from xml.etree import cElementTree as ET
from lxml import etree as ET
from copy import copy


##############################################################################
###############################################################################
####
####  enable logger 
####
###############################################################################
###############################################################################
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
###############################################################################
###############################################################################
####   END of configuring Logger     -  ii is before the first  function  to make it global
####
####    this can be setup for multiple logger locations
####
###############################################################################
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


def check_status( cs ):
    """
    """
    c = cs.status_code
    
    if c == 200:
        
        return(True)
  
  
  
    elif c == 400:
        return("Fail      400     Bad Request")
    elif c == 405:
        return("Fail      405     Method Not Allowed")
    else:
        return("unknown")
        


def  check_response_type(doc):
    """
    
    """
    

    return(True)


class rest_cfg:

    def __init__(self, pa):
        self.fid          = pa.fid
        self.user      = pa.user
        self.pwrd     = pa.pw
        self.ip           = pa.ip
        self.Auth    =  self.rest_login()
        self.verbose  = pa.verbose
        
    def get_Auth(self, ):
        return(self.Auth)
    
    def get_wwn(self,  fid = -1):
        """
        
        """
        #Auth_strng = {'Authorization':'%s'%auth_value}
        logger.info('Start of function get_wwn')
        if fid < 1 :
            path_to_wwn =  "http://" + self.ip + "/rest/running/switch/fibrechannel-switch"
        else:
            path_to_wwn =  "http://" + self.ip + "/rest/running/switch/fibrechannel-switch" + "?vf-id=" + str(fid)
        
        try: 
            s = requests.get(path_to_wwn, headers=self.Auth)            
            doc = untangle.parse(s.text)
            done = doc.Response.fibrechannel_switch.name.cdata
        except AttributeError:
            
            print("Error during untangle - None was returned")
            print("Please check that the correct FID is used    ")
            done = "Untangle Error"
        except:
            print("Error in untagle" , sys.exc_info()[0] )
            done = "Untangle Error"
        logger.info('End of function get_wwn')
        return(done)
            
    def rest_login(self, ):
        """
            login to the switch via rest and return the Autherization string
            
        """
        
        loginpath =  "http://" + self.ip + "/rest/login"
        r = (requests.post(loginpath, auth=(self.user , self.pwrd)))
        Auth = r.headers.get('Authorization')
        print(Auth)
        Auth_send={'Authorization':'%s'%Auth}
        print(Auth_send)
###############################################################################
###############################################################################
        if r.status_code == 403:    ####  max limit for REST sessions reached
            print(r.text)
            sys.exit()
        return(Auth_send)        

    def rest_logout(self, ):
        """
            logout of the current rest session
            
        """
        #r = requests.post("http://%s/rest/logout" % pa.ip , headers=Auth_send)
        r = requests.post("http://%s/rest/logout" % self.ip , headers=self.Auth)
        print(r.status_code)    
        if r.status_code == 204:
            print("successful logout\n\n")
        else:
            print("logout was not successful\n\n")
        return(r)
    
    
    def set_paused_cfg(self, fid = -1):
        """
       +--rw paused-cfg* [group-type]
       |  +--rw group-type    enumeration
       |  +--rw members
       |     +--rw member*   string
    
        """
        g_type = "fc-port"
        membs = "41"
        payload = {'paused-cfg' :  {"group-type" : g_type ,  'members' : {"member" : membs }}}
        data = json.dumps(payload)
        payload = "<paused-cfg><group-type>fc-port</group-type><members> \
                            <member>0%2f0</member></members></paused-cfg>"
        
        print("\n\n\nDATA")
        print(data)

        if fid < 1 :
            #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
            r = requests.post("http://%s/rest/running/brocade-maps/paused-cfg" % (self.ip), data=payload , headers=self.Auth)
        else:
            r = requests.post("http://%s/rest/running/brocade-maps/paused-cfg/?vf-id=%s"  % (self.ip, self.fid) , data= data, headers=self.Auth)
            
        print(r.status_code)
        print(r.text)
        print(r.headers)
        return(r)
            
            
    def set_maps_config(self, fid = -1):
        """
       +--rw paused-cfg* [group-type]
       |  +--rw group-type    enumeration
       |  +--rw members
       |     +--rw member*   string
    
        """
    
        membs = "raslog"
        #payload = {"actions"  :{ 'action' : [membs] }}
        payload =  { "maps-config": { "recipient-address-list": { "recipient-address": [ "scooby.doo@broadcom.net" ]  }, \
                                    "relay-ip-address": "192.1.1.1", "domain-name": "broadcom.net", "actions": { "action": [  "raslog",  \
                                    "email"  ]  },  "sender-address": "deputy.dog@brocade.com", "decommission-cfg": "impair"  } }

        payload =  { "recipient-address-list": { "recipient-address": [ "scooby.doo@broadcom.net" ]  }, \
                                     "relay-ip-address": "192.1.1.1", "domain-name": "broadcom.net", "actions": { "action": [  "raslog",  \
                                     "email"  ]  },  "sender-address": "deputy.dog@brocade.com", "decommission-cfg": "impair"  }
        
        
        data = json.dumps(payload)
        
        xml_body = """"<maps-config><recipient-address-list><recipient-address>steve.mckie@broadcom.com</recipient-address>
                        </recipient-address-list><relay-ip-address/><domain-name/><actions><action>raslog</action>
                        </actions><sender-address/><decommission-cfg></decommission-cfg></maps-config>"""
                        
        url = "http://%s/rest/running/brocade-maps/maps-config/recipient-address-list/recipient-address/steve.mckie@broadcom.com" % self.ip
        

        print("\n\n\nDATA")
        print(url)
        
        r = requests.post( url,  headers=self.Auth)
        #r = requests.post("http://%s/rest/running/brocade-maps" % (self.ip), params=data, headers=self.Auth)

        # if fid < 1 :
        #     #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
        #     #r = requests.post("http://%s/rest/running/brocade-maps/maps-config" % (self.ip), data=data , headers=self.Auth)
        #     r = requests.post("http://%s/rest/running" % (self.ip),  data=xml, headers=self.Auth)
        # else:
        #     r = requests.post("http://%s/rest/running/brocade-maps/maps-config/?vf-id=%s"  % (self.ip, self.fid) , data= data, headers=self.Auth)
        #     
        print(r.status_code)
        print(r.text)
        print(r.headers)
        print(r.json)
        print(r.url)
        print(r.encoding)
        print("END of MAPSCONFIG" * 10)
        return(r)
            
            
    def get_top_level(self, leaf = "none", fid = -1):
        """
               this function will return the leaf info for the value passed 
        
        """
        
    ##########################################################
    ##########################################################
    ### should be able to get all info from r since it is per name
    ####
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, leaf), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/%s/?vf-id=%s"  % (self.ip, leaf, self.fid) , headers=self.Auth)
                
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
 
    
        
        #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, leaf), headers=self.Auth)
     
        go = r.text
        go = go.replace("N/A", "NA")     
        return(r)
        data = xmltodict.parse(go)
        # pprint.pprint(data["Response"]['group'])
        # print("ABC "*80)
        if r.status_code == 200:
            cmd_response_logger.info("TOP LEVEL COMMAND  is  %s" % leaf)
            cmd_response_logger.info("STATUS CODE                 %s   " % r.status_code)
            cmd_response_logger.info("HEADERS     %s  " %  r.headers)
        else:
            cmd_response_logger.error("TOP LEVEL COMMAND is %s " % leaf)
            cmd_response_logger.error("STATUS CODE                 %s   " % r.status_code)
            cmd_response_logger.info("HEADERS     %s  " %  r.headers)
        logger.info("#"*80)
        logger.info('Start of Top Level function and getting  %s   '  % leaf )
        logger.info("#"*80)
        logger.info(r.status_code)
        logger.info(r.headers)
        logger.info(data)
        #logger.info(pprint.pprint(data))
        logger.info("@"*80)
        
        return(data)






    def fs_leaf(self, word, fid = -1):
        """
        return the info for a specified leaf in the module
            brocade-fabric-switch  yang file 
                #/rest/running/switch/fibrechannel-switch
        """
        logger.info('Start of function fs_leaf')
        done = "none"
        print("#"*88)
        print(fid)
        print("#"*88)
        
        try:
            if fid == -1 :
                r = requests.get("http://%s/rest/running/fabric/fabric-switch" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/fabric/fabric-switch?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
     
            doc = untangle.parse(r.text)
            done_list = []
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
        #######################################################################
        #######################################################################
        ####
        ####   check the status of the command
        ####
        #######################################################################
        #######################################################################
        print("#"*80)
        print("JSON"*40)
        print(r.text)
        print("@"*80)
        cs = check_status(r)
        if cs != True:
            logger.error("fs_leaf error")
            logger.error(cs)
            logger.error("#"*80)
            sys.exit()
            return(cs)  
        
        try:
                
            if type(doc.Response.fabric_switch) is list:
                for c in doc.Response.fabric_switch:
                    done_list.append(getattr(c, word).cdata)
                print("using the if part ")
                print(done_list)
                return(done_list)
            else:
                done_list = getattr(doc.Response.fabric_switch, word).cdata
                print("using the else part")
                print(done_list)
                return(done_list)
            
        except AttributeError:
            print("Error during untangle - None was returned")
            done = "Untangle Error"
        except:
            print("Error in untagle" , sys.exc_info()[0] )
            print("fs_leaf")
            done = "Untangle Error"
        logger.info('End of function fabric switch')
        return(done)
              
    def fcs_leaf(self, word, fid = -1):
        """return the info for a specified leaf in the module
            brocade-fibrecahnnel-switch  yang file 
      
            r = requests.get("http://%s/rest/running/switch/fibrechannel-switch?vf-id=%s"  % ( pa.ip, pa.fid) , headers=Auth_send)      
        """
        logger.info('Start of function fcs_leaf')
        logger.info("requesting data for  keyword      %s  " %  word)
        
        done = "none"
        done_list = []
        
        if fid < 1:
            r = requests.get("http://%s/rest/running/switch/fibrechannel-switch"  % ( self.ip) , headers=self.Auth)
        else:
            r = requests.get("http://%s/rest/running/switch/fibrechannel-switch?vf-id=%s"  % ( self.ip, self.fid) , headers=self.Auth)     
        doc = untangle.parse(r.text)
        print(r.text)
        print("\r\n"*10)
        
        
        try:

            if word == "ip_address" :
                print("try this one ")
                done_list  = getattr(doc.Response.fibrechannel_switch, word).ip_address.cdata 
            else:
                done_list = getattr(doc.Response.fibrechannel_switch, word).cdata
            print("using the else part")
            print(done_list)
            return(done_list)
        
        except AttributeError:
            print("Error during untangle - None was returned")
            done = "Untangle Error"
        except:
            print("Error in untagle" , sys.exc_info()[0] )
            print("fs_leaf")
            done = "Untangle Error"
        
        if done == "none":
            logger.info("ERROR====="*12)
            logger.info('Error in function fcs_leaf')
            logger.info("\n\nError in fcs_leaf the command requested is not one of the\
                \ncommand requested was  %s    \
                \n\nthe list of valid commands is \nvf-id, domain-id, fcid,\
                \n user-freindly-name, enabled-state, up-time, model, firmware-version,\
                \n ip-address, domain-name, fabric-user-friendly-name,\
                \n ag-mode, principal\n\n"  %  word)    

        logger.info('End of function fabric switch')
        return(done)
        

        
    def fc_stats_leaf(self, word, wwn, fid= -1):
        """
        
        """
        logger.info('Start of function fc_stats_leaf  or brocade-interface/fibrechannel  ')
        
        try:
            if fid < 1 :
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
     
            doc = untangle.parse(r.text)
            done_list = []
            print(r.text)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
            
        #s = self.get_tasks(word,self.ip, wwn,self.Auth, "fc_switch", fid )
 
        
        
        
        # try:
        #         
        #     pass
        # 
        #     if done == "none":
        #         logger.info("ERROR====="*12)
        #         logger.info('Error in function fs_leaf')
        #         logger.info("\n\nError in fs_leaf the command requested is not one of the\
        #             \ncommand requested was  %s    \
        #             \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
        #             \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
        #             \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    
        # 
        #         print("\n\nError in fs_leaf the command requested is not one of the\
        #             \ncommand requested was  %s    \
        #             \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
        #             \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
        #             \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    
        # 
        # 
        # except AttributeError:
        #     print("Error during untangle - None was returned")
        #     done = "Untangle Error"
        # except:
        #     print("Error in untagle" , sys.exc_info()[0] )
        #     done = "Untangle Error"
        return(done_list)
        
    def zone_defined_leaf(self, word, fid = -1):
        """
        return the info for a specified leaf in the module
            brocade-zone  yang file 
        
        """
        logger.info('Start of function zone_leaf')
        try:
            
            # s = self.get_tasks_zone(word, self.ip, self.Auth , "defined_configuration", fid )
            # print("zone_leaf_debug___"*10)
            # print(s.text)
            # print("zone_leaf_end_____"*10)
            # doc = untangle.parse(s.text)
            # print("zone_leaf_dbg___"*10)
            # print(doc)
            # print("zone_leaf_ends_____"*10)
            # done = "none"
            # #if "defined-configuration" == word:
            # if "alias" == word:
            #     done = doc.Response.defined_configuration.alias.cdata
            # if "vf-id" == word:
            #     done = doc.Response.fabric_switch.vf_id.cdata
            # if "wwn" == word:
            #     done = doc.Response.fabric_switch.name.cdata
            # if "switch-user-friendly-name"  == word:
            #     done = doc.Response.fabric_switch.switch_user_friendly_name.cdata
            # if "chassis-wwn"  == word:
            #     done = doc.Response.fabric_switch.chassis_wwn.cdata
            # if "chassis-user-friendly-name" == word:
            #     done = doc.Response.fabric_switch.chassis_user_friendly_name.cdata              
            # if "domain-id" == word:
            #     done = doc.Response.fabric_switch.domain_id.cdata
            # if "principal" == word:
            #     done = doc.Response.fabric_switch.principal.cdata
            # if "fcid" == word:
            #     done = doc.Response.fabric_switch.fcid.cdata
            # if "ip-address" == word:
            #     done = doc.Response.fabric_switch.ip_address.cdata
            # if "fcip-address"  == word:
            #     done = doc.Response.fabric_switch.fcip_address.cdata
            # if "ipv6-address" == word:
            #     done = doc.Response.fabric_switch.ipv6_address.cdata
            # if "firmware-version" == word:
            #     done = doc.Response.fabric_switch.firmware_version.cdata
            
            if done == "none":
                
                print("\n\nError in fs_leaf the command requested is not one of the\
                      \ncommand requested was  %s    \
                      \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
                      \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
                      \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    
 
        except AttributeError:
            print("Error during untangle - None was returned")
            done = "Untangle Error"
        except:
            print("Error in untagle" , sys.exc_info()[0] )
            print("fs_leaf")
            done = "Untangle Error"
        logger.info('End of function get_wwn')
        return(done)      
    
    def test(self, ):
        print("#"*80)
        print("\nTEST of rest_cfg")
        print(self.ip)
        print(self.fid)
        print(self.user)
        print(self.pwrd)
        return()
    
    
   

    
            
            
            
            
            
            
        if list_name == "fab_switch":
            top_level = "/rest/running/fabric/fabric-switch"
            cmplt_path = self._url(switch_ip, wwn, top_level, command , fid)
            r = requests.get(cmplt_path, headers=Auth_send)
            return(r)
        
    def maps_matrix(self, fid = -1 ):
        """
        
        """
        logger.info('Start of function maps commands   ')
        
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/monitoring-system-matrix" % (self.ip), headers=self.Auth)               
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/monitoring-system-matrix/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                
            doc = untangle.parse(r.text)
        
            print("#"*80)
            print("JSON"*40)
            print(r.text)
            print("@"*80)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
   
   
        logger.info("Monitoring Matrix ")
        logger.info(r.text)
        logger.info("Untangled doc")
        logger.info(r)
   
    
        go = r.text
        go = go.replace("N/A", "NA")     
        
        data = xmltodict.parse(go)
        pprint.pprint(data["Response"])
        print("ABC "*80)
 
        logger.info("Monitoring MAPS Group")
 
        logger.info(r.status_code)
        
        return(data)
   
   
  
    def maps_config(self,  fid = -1):
        """
                +--rw maps-config
                |  +--rw actions
                |  |  +--rw action*   maps-types:maps-generic-action-type
                |  +--rw decommission-cfg
                |  |  +--rw cfg?   enumeration
                |  +--rw receipient-address-list
                |  |  +--rw receipient-address*   string
                |  +--rw sender-address?            string
                |  +--rw domain-name?               string
                |  +--rw relay-ip-address?          inet:ip-address
                |  +--rw test-email
                |     +--rw subject?   string
                |     +--rw body?      string
        
        """
        logger.info('Start of function maps config commands   ')
        
        try:
            if fid < 1 :
                r = requests.get("http://%s/rest/running/brocade-maps/maps-config" % (self.ip), headers=self.Auth)               
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/maps-config/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
 
            go = r.text
            go = go.replace("N/A", "NA")     
            data = xmltodict.parse(go)
 
            logger.info("Monitoring MAPS Group")    
            logger.info(r.status_code)
            
            return(data)
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
   
        logger.info("Monitoring MAPS CONFIG")
 
        done_list = []
        return(data)
   
        

    def maps_rules(self, fid = -1):
        """
        
         +--rw rule* [name]
       |  +--rw name                          maps-types:maps-rule-name-type
       |  +--rw is-rule-on-rule?              maps-types:maps-rule-type
       |  +--rw monitoring-system?            maps-types:maps-monitoring-system-type
       |  +--rw time-base?                    maps-types:maps-time-base-type
       |  +--rw logical-operator?             maps-types:maps-logical-operator-type
       |  +--rw threshold-value?              maps-types:threshold-value-type
       |  +--rw group-name?                   maps-types:maps-group-name-type
       |  +--rw actions
       |  |  +--rw action*   maps-types:maps-generic-action-type
       |  +--ro is-predefined?                boolean
       |  +--rw event-severity?               maps-types:maps-event-severity-type
       |  +--rw toggle-time?                  uint32
       |  +--rw quiet-time?                   uint32
       |  +--rw quiet-time-unit?              maps-types:maps-quiet-time-unit-type
       |  +--rw quiet-time-clear?             boolean
       |  +--rw un-quarantine-timeout?        uint32
       |  +--rw un-quarantine-timeout-unit?   maps-types:maps-quiet-time-unit-type
       |  +--rw un-quarantine-clear?          boolean
        
        
        """
    ###################################################################################################
    ###################################################################################################
        r = ""
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/rule" % (self.ip), headers=self.Auth)
                cmd_response_logger.info("mapsrules                Sending command to default FID  ")
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/rule/?vf-id=%s"  % (self.ip, fid) , headers=self.Auth)
                cmd_response_logger.info("mapsrules                Sending command with FID   %s  "  % fid)
            
            cmd_response_logger.info("mapsrules                  %s  " % r)
            
            try:
                doc = untangle.parse(r.text)
                
                print("#"*80)
                print("JSON"*40)
                print(r.text)
                print("@"*80)
            except AttributeError:
                print("Error during untangle - None was returned")
                done = "Untangle Error"
                sys.exit()
            except:
                print("Error in untagle" , sys.exc_info()[0] )
                print("mapsrule")
                done = "Untangle Error"
                sys.exit()
                
                
        
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()

   
        go = r.text
        go = go.replace("N/A", "NA")     
        
        data = xmltodict.parse(go)
  
 ######################################################################################################
 ######################################################################################################
 ####
 ####  log the status code and response      
 ####
 ######################################################################################################
        cmd_response_logger.info("mapsrules                  %s  " %  r.status_code)
        mapsrule_response_logger.info(json.dumps(data, indent=2))
        
        
        return(data)
        # 
        # done_list = []
        # return(r)
        # 
        # 
        # try:
        #     logger.info("Creating list of data")
        #     logger.info(type(doc.Respnse.rule))
        #     
        #     if type(doc.Response.rule) is list:
        #         logger.info("check of location  3")
        #     
        #         for c in doc.Response.rule:
        #             logger.info(c)
        #         
        #             done_list.append(getattr(c, word).cdata)
        #         print("using the if part ")
        #         print(done_list)
        #         return(done_list)
        #     else:
        #         done_list = getattr(doc.Response.rule, word).cdata
        #         print("using the else part")
        #         print(done_list)
        #         return(done_list)
        #     
        # except AttributeError:
        #     print("Error during untangle - None was returned")
        #     done = "None was returned  Untangle Error"
        # except:
        #     print("Error in untagle" , sys.exc_info()[0] )
        #     print("maps")
        #     done_list = "Untangle Error see previous message for details"
        # logger.info('End of function   maps  config command  ')
        # return(done_list)
                       
    def maps_sspr(self, fid = -1):
        """
           Switch status policy  
        
            +--rw brocade-maps
                +--ro switch-status-policy-report       #### this should be allowed to return all of the health status below
                |  +--ro switch-health?                ssp-state-type
                |  +--ro power-supply-health?          ssp-state-type
                |  +--ro fan-health?                   ssp-state-type
                |  +--ro wwn-health?                   ssp-state-type {maps-types:chassis-platform}?
                |  +--ro temperature-sensor-health?    ssp-state-type
                |  +--ro ha-health?                    ssp-state-type {maps-types:chassis-platform}?
                |  +--ro control-processor-health?     ssp-state-type {maps-types:chassis-platform}?
                |  +--ro core-blade-health?            ssp-state-type {maps-types:chassis-platform}?
                |  +--ro blade-health?                 ssp-state-type {maps-types:chassis-platform}?
                |  +--ro flash-health?                 ssp-state-type
                |  +--ro marginal-port-health?         ssp-state-type
                |  +--ro faulty-port-health?           ssp-state-type
                |  +--ro missing-sfp-health?           ssp-state-type
                |  +--ro error-port-health?            ssp-state-type
                |  +--ro expired-certificate-health?   ssp-state-type
                |  +--ro airflow-mismatch-health?      ssp-state-type
        
        """
        logger.info('Start of function maps Switch status Policy commands   ')
        ssp_list = ['switch-health', 'power-supply-health', 'fan-health', 'wwn-health', 'temperature-sensor-health', 'ha-health', \
                    'control-processor-health', 'core-blade-health', 'blade-health', 'flash-health', 'marginal-port-health', \
                    'faulty-port-health', 'missing-sfp-health', 'error-port-health', 'expired-certificate-health', 'airflow-mismatch-health' ]
        
        
        try:
            
            xml_dict = {}
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                #r = requests.get("http://%s/rest/running/brocade-maps/switch-status-policy-report/switch-health" % (self.ip), headers=self.Auth)
                for h in ssp_list:   
                    r = requests.get("http://%s/rest/running/brocade-maps/switch-status-policy-report/%s" % (self.ip, h), headers=self.Auth)   
                    tree = ET.fromstring(r.text, )
                    sh3 = tree[0][0].text
                    if r.status_code == 200:
                        xml_dict[h]  =  sh3
                    else:
                        xml_dict[h]  = "status code returned was  %s " % r.status_code
                return(xml_dict)
            else:
                for h in ssp_list:
                    r = requests.get("http://%s/rest/running/brocade-maps/switch-status-policy-report/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                    tree = ET.fromstring(r.text, )
                    sh3 = tree[0][0].text
                    if r.status_code == 200:
                        xml_dict[h]  =  sh3
                    else:
                        xml_dict[h]  = "status code returned was  %s " % r.status_code
                return(xml_dict)
                          
            print(xml_dict)
            print("&& "*50)
            print("&& "*50)
             
            logger.info("Monitoring MAPS Switch Status Policy ")
            logger.info("SSP")
            logger.info( xml_dict)
            logger.info("@")
      
        except TypeError:
            logger.info("logout ")
            logger.info("Possible error with the command ")
            logger.info("you did not get logged out of the session")
            return("ERROR")
        
    def maps_system_resource(self, fid = -1):
        """
             +--ro system-resource
             |  +--ro cpu-usage?      decimal64
             |  +--ro memory-usage?   decimal64
             |  +--ro flash-usage?    decimal64
        
        """
        logger.info('Start of function maps system resource commands   ')
        ssp_list = ['cpu-usage', 'memory-usage', 'flash-usage']
                
        try:
            
            xml_dict = {}
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                #r = requests.get("http://%s/rest/running/brocade-maps/switch-status-policy-report/switch-health" % (self.ip), headers=self.Auth)
                for h in ssp_list:   
                    r = requests.get("http://%s/rest/running/brocade-maps/system-resources/%s" % (self.ip, h), headers=self.Auth)   
                    print(r.status_code)
                    tree = ET.fromstring(r.text, )
                    sh3 = tree[0][0].text
                    if r.status_code == 200:
                        xml_dict[h]  =  sh3
                    else:
                        xml_dict[h]  = "status code returned was  %s " % r.status_code
                return(xml_dict)
            else:
                for h in ssp_list:
                    r = requests.get("http://%s/rest/running/brocade-maps/system-resources/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                    tree = ET.fromstring(r.text, )
                    sh3 = tree[0][0].text
                    xml_dict[h]  =  sh3
                    if r.status_code == 200:
                        xml_dict[h]  =  sh3
                    else:
                        xml_dict[h]  =  "status code returned was  %s " % r.status_code
                return(xml_dict)
                          
            print(xml_dict)
            print("&& "*50)
            print("&& "*50)
             
            logger.info("Monitoring MAPS  System Resource Commands ")
            logger.info("SSP")
            logger.info( xml_dict)
            logger.info("@")
      
        except TypeError:
            logger.info("logout ")
            logger.info("Possible error with the command ")
            logger.info("you did not get logged out of the session")
            return("ERROR")
        

    def maps_pause_con(self, fid = -1):
        """
                   +--rw Puased-cfg* [group-type]
                    |  +--rw group-type    enumeration
                    |  +--rw operation?    enumeration
                    |  +--rw members
                    |     +--rw member*   string
        
        """
        logger.info('Start of function maps system resource commands   ')
        
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/paused-cfg" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/paused-cfg/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                
            doc = untangle.parse(r.text)
        
            print("#"*80)
            print("JSON"*40)
            print(r.text)
            print("@"*80)
            cs = check_status(r)
            if cs != True:
                return(cs)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
 
   
        logger.info("Monitoring MAPS CONFIG")
        logger.info(r.text)
        logger.info("Untangled doc")
        logger.info(r)
   
        go = r.text
        go = go.replace("N/A", "NA")     
        
        data = xmltodict.parse(go)
        pprint.pprint(data["Response"])
        print("ABC "*80)
 
        logger.info("Monitoring MAPS Group")
 
        logger.info(r.status_code)
        
        return(data)
  
    def maps_group(self, fid = -1):
        """
               +--rw group* [name]
                |  +--rw name              maps-types:maps-group-name-type
                |  +--rw group-type?       maps-types:maps-group-type-type
                |  +--rw group-feature?    maps-group-feature-type
                |  +--ro is-predefined?    boolean
                |  +--ro is-augmentable?   boolean
                |  +--rw members
                |     +--rw member*   string
        
        """
        logger.info('Start of function maps group commands   ')
        
        # try:
        #     if fid < 1 :
        #         #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
        #         r = requests.get("http://%s/rest/running/brocade-maps/group" % (self.ip), headers=self.Auth)
        #     else:
        #         r = requests.get("http://%s/rest/running/brocade-maps/group/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
        #         
        #     
        # except TypeError:
        #     pass
        #     print("logout ")
        #     print("Possible error with the command ")
        #     print("you did not get logged out of the session")
        #     sys.exit()
        # 
        # g_dict = []
        # port_list = []
        # go = r.text
        # go = go.replace("N/A", "NA")
        # tree = ET.fromstring(go)
        # g_dict_com = {}
        # g_type = {}
        # predefined = {}
        # port_dict = {}
        # h_dict = {}
        # 
        #######################################################################
        #######################################################################
        ####  get the list of all group names   
        ####    then loop through and get all the other info and create a dictionary
        ####     with the values that coorespond
        ####
        
        # for groups in  tree.findall(".//group/name"):
        #     print(groups.tag)
        #     print(groups.text)
        #     g_dict.append(groups.text)
        # 
        # 
        # for h in g_dict:
        #     r = requests.get("http://%s/rest/running/brocade-maps/group/name/%s" % (self.ip, h), headers=self.Auth)
        #     #gt = requests.get("http://%s/rest/#running/brocade-maps/group/name/%s/group-type" % (self.ip, h), headers=self.Auth)
        # 
        #     go = r.text
        #     go = go.replace("N/A", "NA")
        #     tree = ET.fromstring(go)
        #     port_list = []
        #     group_list = []
        #     for gt in tree.findall('.//members/member'):
        #      
        #         memb = requests.get("http://%s/rest/running/brocade-maps/group/name/%s/members" % (self.ip, h), headers=self.Auth)
        #     
        #         print("$"*800)
        #         print(h)
        #         print(gt.text)
        #         port_list.append(gt.text)
        #         print("PORT LIST ")
        #         print(port_list)
        # 
        #         print("0"*800 )
        #         print(memb.text)
        #         
        #     for group_type in tree.findall('.//group-type'):
        #         g_type['group_type'] = group_type.text
        #     
        #     for is_pre in tree.findall('.//is-predefined'):
        #         predefined['predefined'] = is_pre.text
        #     
        #     ###################################################################
        #     ###################################################################
        #     ####  add the types to a new list then add to dictionary
        #     ####
        #     #####
        #     print("@"*80)
        #     print(port_list)
        #     port_dict['ports']  =  port_list
        #     print("GROUP LIST")
        #     print(group_list)
        #     print("2 "*80)
        #     
        #     
        #     group_list.append(port_dict)
        #     group_list.append(g_type)
        #     group_list.append(predefined)
        #     h_dict[h] = group_list
        #     
        #     #g_dict_com [h] = group_list
        #     g_dict_com.update(h_dict)
        #     g_dict_com.update(port_dict)
        #     
        #     print("3 "*80)
        #     print(predefined)
        #     print(g_type)
        #     print(g_dict_com)
        #     print(port_list)
        #     print(r.text)
        #     print(group_list)
        #     print("4 "*80)
        #     # 
            #print(gt.text)
            #print(memb.text)
    ##########################################################
    ##########################################################
    ### should be able to get all info from r since it is per name
    ####
        r = requests.get("http://%s/rest/running/brocade-maps/group" % (self.ip), headers=self.Auth)
   
        go = r.text
        go = go.replace("N/A", "NA")     
        
        data = xmltodict.parse(go)
        pprint.pprint(data["Response"]['group'])
        print("ABC "*80)
 
        logger.info("Monitoring MAPS Group")
 
        logger.info(r.status_code)
        
        return(data)
  
    def maps_dashboard_rule(self, fid = -1):
        """
                +--ro dashboard-rule*
                |  +--ro category?           maps-types:maps-dashboard-category-type
                |  +--ro name?               maps-types:maps-rule-name-type
                |  +--ro triggered-count?    uint32
                |  +--ro time-stamp?         yang:date-and-time
                |  +--ro repetition-count?   uint32
                |  +--ro objects
                |     +--ro object*   string
        
        """
        logger.info('Start of function maps group commands   ')
        
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/dashboard-rule" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/dashbaord-rule/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                
            #doc = untangle.parse(r.text)
        
            print("#"*80)
            print("JSON"*40)
            print(r.text)
            print("@"*80)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
        
        go = r.text
        go = go.replace("N/A", "NA")     
        go = go.replace("Switch#0", "Switch0")
 
        data = xmltodict.parse(go)
        pprint.pprint(data["Response"])
        print("ABC "*80)
 
        
        logger.info("Monitoring MAPS Group")
 
        logger.info(r.status_code)
        

   
        logger.info("Monitoring MAPS Dashbaord Rule")
        logger.info(r.text)
        logger.info("Untangled doc")
        logger.info(r)
   
        return(data)
   
        #done_list = []
        #return(r)
   
        # 
        # try:
        #     logger.info("Creating list of data")
        #     logger.info(type(doc.Respnse.dashboard_rule))
        #     
        #     if type(doc.Response.dashboard_rule) is list:
        #         logger.info("check of location  3")
        #     
        #         for c in doc.Response.dashboard_rule:
        #             logger.info(c)
        #         
        #             done_list.append(getattr(c, word).cdata)
        #         print("using the if part ")
        #         print(done_list)
        #         return(done_list)
        #     else:
        #         done_list = getattr(doc.Response.dashbaord_rule, word).cdata
        #         print("using the else part")
        #         print(done_list)
        #         return(done_list)
        #     
        # except AttributeError:
        #     print("Error during untangle - None was returned")
        #     done = "None was returned  Untangle Error"
        # except:
        #     print("Error in untagle" , sys.exc_info()[0] )
        #     print("maps")
        #     done_list = "Untangle Error see previous message for details"
        # logger.info('End of function   maps  switch-status-policy-report  command  ')
        # return(done_list)
                           
         
         
    def maps_dashboard_misc(self, fid = -1):
        """
                +--rw dashboard-misc
               |  +--ro maps-start-time?   yang:date-and-time
               |  +--rw clear-operation?   boolean
        
        """
        logger.info('Start of function maps group commands   ')
        
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/dashboard-misc" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/dashbaord-misc/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                
            doc = untangle.parse(r.text)
        
            print("#"*80)
            print("JSON"*40)
            print(r.text)
            print("@"*80)
            cs = check_status(r)
            if cs != True:
                return(cs)
            
        except TypeError:
            print("logout ") 
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
   
   
        logger.info("Monitoring MAPS Dashbaord Rule")
        logger.info(r.text)
        logger.info("Untangled doc")
        logger.info(r)
   
   
        go = r.text
        go = go.replace("N/A", "NA")     
        
        data = xmltodict.parse(go)
        pprint.pprint(data["Response"])
        print("ABC "*80)
 
        logger.info("Monitoring MAPS Group")
 
        logger.info(r.status_code)
        
        return(data)
    
         
       
    def maps_policy(self, fid = -1):
        """
                +--rw maps-policy* [name]
                |  +--rw name                    maps-types:maps-policy-name-type
                |  +--rw rule-list
                |  |  +--rw rule*   maps-types:maps-rule-name-type
                |  +--rw is-active-policy?       boolean
                |  +--ro is-predefined-policy?   boolean
        
        """
        logger.info('Start of function maps Policy commands   ')
        
        try:
            if fid < 1 :
                #r = requests.get("http://%s/rest/running/brocade-maps/%s" % (self.ip, word), headers=self.Auth)
                r = requests.get("http://%s/rest/running/brocade-maps/maps-policy" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-maps/maps-policy/?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
                
            doc = untangle.parse(r.text)
        
            print("#"*80)
            print("JSON"*40)
            print(r.text)
            print("@"*80)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
   
   
        logger.info("Monitoring MAPS Dashbaord Rule")
        logger.info(r.text)
        logger.info("Untangled doc")
        logger.info(r)
   
        go = r.text
        go = go.replace("N/A", "NA")     
        
        data = xmltodict.parse(go)
        pprint.pprint(data["Response"])
        print("ABC "*80)
 
        logger.info("Monitoring MAPS Group")
 
        logger.info(r.status_code)
        
        return(data)
    
         
    def get_policy_list(self, predefined = 0, active = 0, fid = -1):
        """
        return the list of policys both default and user created
        
        """
        logger.info('Start of function get_policy_list')
        logger.info("requesting data  to get policy list  ")
          
        
        policy_data = self.maps_policy(fid)
        
        return(policy_data)

       
       
        
        
    def get_domain_ids(self, fid = -1):
        """
        get the VF ID ( Fabric ID )  list for the switch
        if VF is not enabled return    -1

        """
        logger.info('Start of function get_domain_ids')
        logger.info("requesting data  to get all domain ids  ")
                
        word = "fabric_id"
        done_list = []
        
        r = requests.get("http://%s/rest/running/logical-switch/fibrechannel-logical-switch"  % ( self.ip) , headers=self.Auth)
 
        doc = untangle.parse(r.text)
        print(r.text)
        print("\r\n"*10)
            
        try:
            if type(doc.Response.fibrechannel_logical_switch ) is list :
                for c in doc.Response.fibrechannel_logical_switch:
                    done_list.append(getattr(c, word).cdata)
                
                print("using the if part ")
                print(done_list)    
            #    return(done_list)
            else:
                done_list = getattr(doc.Response.fibrechannel_logical_switch, word).cdata
                print("using the else part")
                print(done_list)
        except AttributeError:
            print("Error during untangle - None was returned")
            done_list = "Untangle Error  hahahaha"
            done_list = getattr(doc.errors.error, "error_message").cdata
            if "not enabled" in done_list:
                #print("YES")
                done_list=[-1,]
 
        return(done_list)
            
                

        
              
        
        
     
    def port_numbers(self, fid = -1):
        """
        """
     
        logger.info('Start of function port_numbers   ')
        
        try:
            if fid < 1 :
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics" % (self.ip), headers=self.Auth)
            else:
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
     
            doc = untangle.parse(r.text)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
 
        print("#"*80)
        print(doc)
        print("@"*80)
        #print(r.text)
        print(type(doc))
        print(doc.cdata)
        
        if doc.cdata is None:
            print("NONE")
        print("&"*80)
        
        
        done_list = []
        word = "name"
        
        check_response_type(doc)
        
        try:
            if type(doc.Response.fibrechannel_statistics ) is list :
            
    
                for c in doc.Response.fibrechannel_statistics:
                    done_list.append(getattr(c, word).cdata)
                
                print("using the if part ")
                print(done_list)    
            #    return(done_list)
            else:
                done_list = getattr(doc.Response.fabric_switch, word).cdata
                print("using the else part")
                print(done_list)
        except AttributeError:
            print("Error during untangle - None was returned")
            done_list = "Untangle Error  "
            
            
        return(done_list)
            
    
    
    
    def port_err_stats(self, slot=0, port=0, fid = -1):
        """
        """
     
        logger.info('Start of function port_numbers   ')
        
        try:
                
            if fid < 1 :
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/0%s%s" % (self.ip, "%2f", port), headers=self.Auth)
            else:
                #r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics?vf-id=%s/name/0%s7"  % (self.ip, self.fid, "%2f" ) , headers=self.Auth )
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/0%s%s?vf-id=%s"  % (self.ip, "%2f" ,port, self.fid) , headers=self.Auth )
     
     
            doc = untangle.parse(r.text)
            
        except TypeError:
            print("logout ")
            print("Possible error with the command ")
            print("you did not get logged out of the session")
            sys.exit()
        
        print("&"*80)
        print(doc)
        print("%"*80)
        print(r.text)
        
        done_list = []
        word = "name"
        
        
        try:
            
            if type(doc.Response.fibrechannel_statistics is list ):
                
                for c in doc.Response.fibrechannel_statistics:
                    done_list.append(getattr(c, word).cdata)
                
                print("using the if part ")
                print(done_list)    
            #    return(done_list)
            else:
                done_list = getattr(doc.Response.fabric_switch, word).cdata
                print("using the else part")
                print(done_list)
     
        except AttributeError:
            print("Error during untangle - None was returned")
            done_list = "Untangle Error"
            
 
        return(done_list)
            
