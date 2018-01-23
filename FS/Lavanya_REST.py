#!/usr/bin/env python3
import requests
import argparse
import time
import sys

sys.path.append('/home/automation/lib/FOS')

import rest_cmd_lib as rest_cmd

# #Getting the user arguments
# parser = argparse.ArgumentParser(description = 'Getting the all arguments')
# parser.add_argument('-ip', '--switch_ip',  type=str, help = 'Please give the valid switch ip to login into the switch')
# parser.add_argument('-u', '--user_name', type=str, default = 'admin', help='Please give the user name to login into the switch')
# parser.add_argument('-p', '--pass_word', type=str, default = 'password', help='Please give the password to login into the switch')
# parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")

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
	return(args)

#def main(argv):
def main():
    
   pa = parse_args(sys.argv)
   #namespace = login_utils.parse_args(argv)
   #print('(((((((((((((((((PA PA PA PA PA PA PA PA)))))))))))))))))')
   print(pa)
   print ("Switch ip is " + pa.ip)
   print ("User name is " + pa.user)
   print ("Password is " + pa.pw)

   ##### Call in and initialize as object module res_cmd_lib, class rest_cfg
   ##### This rest_cmd_lib already does login and returns Auth header for future use
   sm = rest_cmd.rest_cfg(pa)
   wwn = sm.get_wwn(pa.fid)
   print('WWN WWN WWN WWN WWN WWN')
   print(wwn)

   ##### This is Auth Key used for all transactions till logout
   Auth  = sm.get_Auth() 
   #print(Auth)
   Auth_key = Auth['Authorization']
   #print('AUTH_KEY')
   #print(Auth_key)
   
   # ### REST LOGOUT (returns status code and successful logout message)
   # rlogout = (sm.rest_logout(Auth))
   # sys.exit()
   
   
   #Executing the basic GET uri

   status_flag = 1;
   while status_flag:
      #url_get = "http://"+ HOST +"/rest/running/switch/fibrechannel-switch"
      #url_get = "http://"+ HOST + "/rest/running/zoning/defined-configuration/cfg"
      uri_array = []
      uri_array = ["http://"+ pa.ip +"/rest/running/switch/fibrechannel-switch",
                                   #"http://"+ pa.ip + "/rest/running/zoning/defined-configuration/cfg",
                                   # "http://"+ HOST + "/rest/running/fabric/fabric-switch",
                                   # "http://"+ HOST + "/rest/running/brocade-interface/fibrechannel",
                                   # "http://"+ HOST + "/rest/running/brocade-interface/fibrechannel-statistics",
                                   # "http://"+ HOST + "/rest/running/zoning/effective-configuration",
                                   # "http://"+ HOST + "/rest/running/diagnostics/fibrechannel-diagnostics",
                                   # "http://"+ HOST + "/rest/running/brocade-nameserver/fibrechannel-nameserver",
                                   # "http://"+ HOST + "/rest/running/brocade-fdmi/hba",
                                   # "http://"+ HOST + "/rest/running/logical-switch/fibrechannel-logical-switch",
                                   # "http://"+ HOST + "/rest/running/logical-switch/fibrechannel-logical-swtich/fabric-id",
                                   # "http://"+ HOST + "/rest/running/brocade-access-gateway/policy/port-group-policy-enabled",
                                   # "http://"+ HOST + "/rest/running/brocade-access-gateway/policy/auto-policy-enabled",
                                   # "http://"+ HOST + "/rest/running/brocade-access-gateway/n-port-settings/reliability-counter",
                                   ]
      for url_in in uri_array:
         if pa.fid < 1 :
            url_2_use = url_in #"http://" + self.ip + "/rest/running/switch/fibrechannel-switch"
         else:
            url_2_use = url_in + "?vf-id=" + str(pa.fid)    #vf-://"/rest/running/switch/fibrechannel-switch" + "?vf-id=" + str(fid)
         print ("Executing the URI \n " + url_2_use)
         print(Auth)
         url_get = requests.get(url_2_use, headers=Auth)
         time.sleep(10)
         get_status_code = url_get.status_code;
         print ("Printing the URI response");
         print (url_get.text);
         print ("\n Printing the get status code for uri \n" + url_in );
         print (get_status_code);
         #checking for 200 response code
         if get_status_code == 200:
            print ("GET operation is successfull")
         else:
            print("Didn't work")
         # elif get_status_code == 401:
         #    #Invalid session key found so re-logging
         #    print ("Found invalid session key so re-logging")
         #    url_login = "http://"+ pa.ip +"/rest/login"
         #    print ("url login " + url_login);
         #    response = requests.post(url_login, auth=(user, pass_word))
         # 
         #    #printing the response code
         #    print (response.text);
         #    login_status_code = response.status_code;
         #    print (login_status_code);
         # 
         #    #checking for 200 response code
         #    if login_status_code == 200:
         #       print ("Rest login is successfull")
         #    else:
         #       print ("Rest login failed")
   
         #    #Getting the authorazation key
         #    Auth_key = response.headers['Authorization'];
         #    print ("Auth key " +Auth_key);
         #    header = {'Authorization':''+Auth_key+''}
         # elif get_status_code == 400:
         #    print ("The URI is repsonds is bad request with status code 400 \n");
         # else:
         #    status_flag = 0
         #    print ("Issues observed while performing the GET operaion")
      
      ### REST LOGOUT (returns status code and successful logout message)
      rlogout = (sm.rest_logout(Auth))
      sys.exit()
   
   
   # #REST logout
   # url_logout = "http://"+ HOST +"/rest/logout"
   # rest_logout = requests.post(url_logout, headers=header)
   # print(rest_logout);
   # #logout status code check
   # rest_logout_status = rest_logout.status_code;
   # if rest_logout_status == 204:
   #    print ("REST logout is successfull")
   # else:
   #    print ("Issues observed during REST logout")

if __name__ == "__main__":
   main()