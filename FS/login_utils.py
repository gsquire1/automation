#!/usr/bin/env python3

"""
Login args
"""

import argparse


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

# def parent_parser(argv):
# 	pp = argparse.ArgumentParser(add_help=False)
# 	pp.add_argument("fid")
# 	#pp.add_argument('-f', '--fid', type=int, help="Choose the FID to operate on")
# 	#pp.add_argument("-ip",'--ipaddr', help="IP address of target switch" , default=0)
# 	return(pp)
# 
# def parse_args(argv):
# 	parent_p = parent_parser(argv)
# 	parser = argparse.ArgumentParser(description = 'PARSER', parents = [parent_p])
# 	parser.add_argument('-ip', '--ipaddr',  type=str, help = 'Please give the valid switch ip to login into the switch')
# 	parser.add_argument('-u', '--user_name', type=str, default = 'admin', help='Please give the user name to login into the switch')
# 	parser.add_argument('-p', '--pass_word', type=str, default = 'password', help='Please give the password to login into the switch')
# 	parser.add_argument('-c', '--chassis_name', type=str, help='Chassis Name in the SwitchMatrix file')
# 	args = parser.parse_args()
# 	return(args)
# 
# def post_header_handling(headers):
# 	print("(((((((((((((inside req_header_handling)))))))))))))")
# 	print(headers)
# 	Auth_key = headers['Authorization']
# 	print(Auth_key)
# 	return(headers)
# 	#header = {'Authorization':''+Auth_key+''}
# 	


