#!/usr/bin/env python3


import requests
import untangle
import sys
import logging

###############################################################################
###############################################################################
###############################################################################
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

####
####  file handler for logging
fh = logging.FileHandler('log_filename.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
####
####  console handler for logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

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

    def rest_logout(self, Auth_send):
        """
            logout of the current rest session
            
        """
        logoutpath = "http://" + self.ip + "/rest/logout"
        #r = requests.post("http://%s/rest/logout" % self.ip , headers=Auth_send)
        r = (requests.post(logoutpath, headers=Auth_send))
        print(r.status_code)    
        if r.status_code == 204:
            print("successful logout\n\n")
        else:
            print("logout was not successful\n\n")
        return(r)
    

    def fs_leaf(self, word, fid = -1):
        """
        return the info for a specified leaf in the module
            brocade-fabric-switch  yang file 
                #/rest/running/switch/fibrechannel-switch
        """
        logger.info('Start of function fs_leaf')
        done = "none"
        
        if fid < 1 :
            r = requests.get("http://%s/rest/running/fabric/fabric-switch" % (self.ip), headers=self.Auth)
        else:
            r = requests.get("http://%s/rest/running/fabric/fabric-switch?vf-id=%s"  % (self.ip, self.fid) , headers=self.Auth)
        
        
        #try:
            
      
        print("fs_leaf_ONE___"*10)
        print(r.text)
        print("fs_leaf_end_ONE____"*10)
        doc = untangle.parse(r.text)
        print("fs_leaf_debug TWO ___"*10)
        print(doc)
        print("fs_leaf_end___TWO___"*10)
        done = "none"
        if "vf-id" == word:
            done = doc.Response.fabric_switch.vf_id.cdata
        if "wwn" == word:
            done = doc.Response.fabric_switch.name.cdata
        if "switch-user-friendly-name"  == word:
            done = doc.Response.fabric_switch.switch_user_friendly_name.cdata
        if "chassis-wwn"  == word:
            done = doc.Response.fabric_switch.chassis_wwn.cdata
        if "chassis-user-friendly-name" == word:
            done = doc.Response.fabric_switch.chassis_user_friendly_name.cdata              
        if "domain-id" == word:
            done = doc.Response.fabric_switch.domain_id.cdata
        if "principal" == word:
            done = doc.Response.fabric_switch.principal.cdata
        if "fcid" == word:
            done = doc.Response.fabric_switch.fcid.cdata
        if "ip-address" == word:
            done = doc.Response.fabric_switch.ip_address.cdata
        if "fcip-address"  == word:
            done = doc.Response.fabric_switch.fcip_address.cdata
        if "ipv6-address" == word:
            done = doc.Response.fabric_switch.ipv6_address.cdata
        if "firmware-version" == word:
            done = doc.Response.fabric_switch.firmware_version.cdata
        
        if done == "none":
            
            print("\n\nError in fs_leaf the command requested is not one of the\
                  \ncommand requested was  %s    \
                  \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
                  \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
                  \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    
        try:
            pass
        
        except AttributeError:
            print("Error during untangle - None was returned")
            done = "Untangle Error"
        except:
            print("Error in untagle" , sys.exc_info()[0] )
            print("fs_leaf")
            done = "Untangle Error"
        logger.info('End of function get_wwn')
        return(done)
              
    def fcs_leaf(self, word, fid = -1):
        """return the info for a specified leaf in the module
            brocade-fibrecahnnel-switch  yang file 
      
            r = requests.get("http://%s/rest/running/switch/fibrechannel-switch?vf-id=%s"  % ( pa.ip, pa.fid) , headers=Auth_send)      
        """
        logger.info('Start of function fcs_leaf')
 
        if fid < 1:
            r = requests.get("http://%s/rest/running/switch/fibrechannel-switch"  % ( self.ip) , headers=self.Auth)
        else:
            r = requests.get("http://%s/rest/running/switch/fibrechannel-switch?vf-id=%s"  % ( self.ip, self.fid) , headers=self.Auth)     
        doc = untangle.parse(r.text)
 
        try:  
            if "vf-id" == word:
                done =  doc.Response.fibrechannel_switch.name.vf_id.cdata
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

            if done == "none":
                logger.info("ERROR====="*12)
                logger.info('Error in function fcs_leaf')
                logger.info("\n\nError in fcs_leaf the command requested is not one of the\
                    \ncommand requested was  %s    \
                    \n\nthe list of valid commands is \nvf-id, domain-id, fcid,\
                    \n user-freindly-name, enabled-state, up-time, model, firmware-version,\
                    \n ip-address, domain-name, fabric-user-friendly-name,\
                    \n ag-mode, principal\n\n"  %  word)    

            logger.info('END of function fcs_leaf')
        except AttributeError:
            print("Error during untangle - None was returned")
            done = "Untangle Error from fcs_leaf "
        except:
            print("Error in untagle" , sys.exc_info()[0] )
            done = "Untangle Error from fcs_leaf"
        return(done)
    
    def fc_stats_leaf(self, word, wwn, fid=-1):
        """
        
        """
        logger.info('Start of function fc_stats_leaf')
        
        s = self.get_tasks(word,self.ip, wwn,self.Auth, "fc_switch", fid )
        
        doc = untangle.parse(s.text)
        try:
                
            if "address_errors" == word:
                done =  doc.Response.fibrechannel_statistics.name.address_errors.cdata
            if " " == word:
                done =  doc.Response.fibrechannel_switch.domain_id.cdata
            if " "  == word:
                done =  doc.Response.fibrechannel_switch.fcid.cdata
            if " - - " == word:
                done =  doc.Response.fibrechannel_switch.user_friendly_name.cdata
            if " - " == word:
                done =  doc.Response.fibrechannel_switch.enabled_state.cdata
            if " - "  == word:
                done =  doc.Response.fibrechannel_switch.up_time.cdata
            if " " == word:
                done = doc.Response.fibrechannel_switch.model.cdata
            if " - "  == word:
                done =  doc.Response.fibrechannel_switch.firmware_version.cdata
            if " - "  == word:
                done =  doc.Response.fibrechannel_switch.ip_address.ip_address.cdata        
            if " - "  == word:
                done =  doc.Response.fibrechannel_switch.domain_name.cdata
            if " - - - "  == word:
                done =  doc.Response.fibrechannel_switch.fabric_user_friendly_name.cdata
            if " - "  == word:
                done =  doc.Response.fibrechannel_switch.ag_mode.cdata    
            if " "  == word:
                done =  doc.Response.fibrechannel_switch.principal.cdata 
        #    'domain-id', 'user-friendly-name', 'fcid', 'vf-id', 'principal', 'enabled-state',
        #    'up-time', 'model', 'firmware-version', 'ip-address', 'domain-name', 'fabric-user-friendly-name', 'ag-mode'
        
        
            if done == "none":
                logger.info("ERROR====="*12)
                logger.info('Error in function fs_leaf')
                logger.info("\n\nError in fs_leaf the command requested is not one of the\
                    \ncommand requested was  %s    \
                    \n\nthe list of valid commands is \ndomain-id\nchassis-wwn\
                    \nswitch-user-friendly-name\nprincipal\nfcid\nip-address\
                    \nfcip-address\nipv6-address\nfirmware-version\n\n"  %  word)    

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
            done = "Untangle Error"
        return(done)
        
    def zone_defined_leaf(self, word, fid = -1):
        """
        return the info for a specified leaf in the module
            brocade-zone  yang file 
        
        """
        logger.info('Start of function zone_leaf')
        try:
            
            s = self.get_tasks_zone(word, self.ip, self.Auth , "defined_configuration", fid )
            print("zone_leaf_debug___"*10)
            print(s.text)
            print("zone_leaf_end_____"*10)
            doc = untangle.parse(s.text)
            print("zone_leaf_dbg___"*10)
            print(doc)
            print("zone_leaf_ends_____"*10)
            done = "none"
            #if "defined-configuration" == word:
            if "alias" == word:
                done = doc.Response.defined_configuration.alias.cdata
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
        
        
  
     
    def port_numbers(self):
        done = dd.Response.fibrechannel[0].name.cdata
        print(done)
        print("END_3"*40)
        ll = len(dd.Response.fibrechannel)
        print("length  %s   " %  ll)
        
        port_list = []
        for x in range(ll):
            print(x)
            
            pl = dd.Response.fibrechannel[x].name.cdata
            print(pl)
            print(type(dd.Response.fibrechannel[x].name.cdata))
            port_list += [pl]
        print(port_list)
    

