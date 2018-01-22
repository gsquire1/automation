#!/usr/bin/env python3
import requests
import argparse
import time
import sys
import login_utils as login_utils

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
    pp.add_argument("pwrd", help="password of user")
    
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
   print(pa)
   ip = pa.ip
   print(ip)
   print ("Switch ip is " + ip)
   user = pa.user
   print ("User name is " + user)
   pwrd = pa.pwrd
   print ("Password is " + pwrd)

   #Rest login
   rl = rest_cmd.rest_cfg.rest_login(pa)
   print("((((((((((this is rl)))))))))))")
   print(rl)
   Auth_key = rl['Authorization']
   print(Auth_key)
   #Rest Logout
   rl = rest_cmd.rest_cfg.rest_logout(pa)
   sys.exit()
   response = requests.post(url_login, auth=(user, pwrd))
   rh = response.headers
  # print(rh)
   login_utils.post_header_handling(Auth_key)
   
   # #REST logout
   # Auth_key = response.headers['Authorization']
   # header = {'Authorization':''+Auth_key+''}
   # url_logout = "http://"+ host +"/rest/logout"
   # rest_logout = requests.post(url_logout, headers=header)
   # print(rest_logout);
   # #logout status code check
   # rest_logout_status = rest_logout.status_code;
   # if rest_logout_status == 204:
   #    print ("REST logout is successfull")
   # else:
   #    print ("Issues observed during REST logout")
   # sys.exit()
   
   
   #Auth = response.headers.get('Authorization')
   #print(Auth)
   #printing the response code
   #print ("Printing the response of logging URI\n");
   #print (response.text);
   login_status_code = response.status_code;
   print ("Printing the login status code \n");
   print (login_status_code);
   
   #checking for 200 response code
   if login_status_code == 200:
      print ("Rest login is successfull\n")
   else:
      print ("Rest login failed\n")
   
   #Getting the authorazation key
   Auth_key = response.headers['Authorization'];
   print ("REST Authorization key is %s \n " % Auth_key);
   #header = (''Authorization:' %s' % Auth_key)
   header = {'Authorization':''+Auth_key+''}
   
   #Executing the basic GET uri
   status_flag = 1;
   while status_flag:
      #url_get = "http://"+ HOST +"/rest/running/switch/fibrechannel-switch"
      #url_get = "http://"+ HOST + "/rest/running/zoning/defined-configuration/cfg"
      uri_array = []
      uri_array = ["http://"+ HOST +"/rest/running/switch/fibrechannel-switch",
                                   "http://"+ HOST + "/rest/running/zoning/defined-configuration/cfg",
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
         print ("Executing the URI \n " + url_in)
         url_get = requests.get(url_in, headers=header)
         time.sleep(10)
         get_status_code = url_get.status_code;
         print ("Printing the URI response");
         print (url_get.text);
         print ("\n Printing the get status code for uri \n" + url_in );
         print (get_status_code);
         #checking for 200 response code
         if get_status_code == 200:
            print ("GET operation is successfull")
         elif get_status_code == 401:
            #Invalid session key found so re-logging
            print ("Found invalid session key so re-logging")
            url_login = "http://"+ HOST +"/rest/login"
            print ("url login " + url_login);
            response = requests.post(url_login, auth=(user, pass_word))
   
            #printing the response code
            print (response.text);
            login_status_code = response.status_code;
            print (login_status_code);
   
            #checking for 200 response code
            if login_status_code == 200:
               print ("Rest login is successfull")
            else:
               print ("Rest login failed")
   
            #Getting the authorazation key
            Auth_key = response.headers['Authorization'];
            print ("Auth key " +Auth_key);
            header = {'Authorization':''+Auth_key+''}
         elif get_status_code == 400:
            print ("The URI is repsonds is bad request with status code 400 \n");
         else:
            status_flag = 0
            print ("Issues observed while performing the GET operaion")
   
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