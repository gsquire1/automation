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
###############################################################################
####  file handler for logging
###############################################################################
fh = logging.FileHandler('rest_cmd_lib_log_.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
###############################################################################
####  console handler for logging
###############################################################################
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
###############################################################################
###############################################################################
###############################################################################
###############################################################################

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
        
        try:
            if fid < 1 :
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
        

        
    def fc_stats_leaf(self, word, wwn, fid=-1):
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

        # 
        # done = doc.Response.fibrechannel-statistics[0].name.cdata
        # print(done)
        # print("END_3"*40)
        # ll = len(doc.Response.fibrechannel-statistics)
        # print("length  %s   " %  ll)
        # 
        # port_list = []
        # for x in range(ll):
        #     print(x)
        #     
        #     pl = dd.Response.fibrechannel[x].name.cdata
        #     print(pl)
        #     print(type(dd.Response.fibrechannel[x].name.cdata))
        #     port_list += [pl]
        print("#"*80)
        print(doc)
        print("@"*80)
        print(r.text)
        
        done_list = []
        word = "name"
        
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
 
        return(done_list)
            
    
    
    
    def port_err_stats(self, slot=0, port=0, fid = -1):
        """
        """
     
        logger.info('Start of function port_numbers   ')
        
        try:
                
            if fid < 1 :
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/0%s36" % (self.ip, "%2f"), headers=self.Auth)
            else:
                #r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics?vf-id=%s/name/0%s7"  % (self.ip, self.fid, "%2f" ) , headers=self.Auth )
                r = requests.get("http://%s/rest/running/brocade-interface/fibrechannel-statistics/name/0%s36?vf-id=%s"  % (self.ip, "%2f" ,self.fid) , headers=self.Auth )
     
     
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
 
        return(done_list)
            
