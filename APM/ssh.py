#!/usr/bin/env python3

 
import paramiko
import sys
import time
import logging


ip = "10.38.34.192"
uname = "root"
pwd = "password"
yesSync = 0

def connect_ssh( ip, user, pwd):
	global ssh
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(ip, username=user, password=pwd)
		return True
	except Exception as e:
		print(e)
		return False



def ssh_send_cmd(cmd):
	 
	syncOutput = ''
	yesSync = 0
	connect = True
	
	if (connect == True):
		print ("inside ssh send command")
		stdin, stdout, stderr = ssh.exec_command(cmd)
		outlines = stdout.readlines()
		resp = ''.join(outlines)
		logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		for line in stdout:
			print ("####    %s " % (line.strip('\n')))
			logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
			logging.debug(line)
		
		logging.debug(resp)

		print("#"*80)
		print("#"*80)
		print("#"*80)
		print("\n\n")
		print(resp)
	
	return(True)



def main():

	connect = connect_ssh(ip, uname, pwd)
	resp = ssh_send_cmd("switchshow")
	print(resp)
	print("#"*80)
	print("\n\n")

	resp = ssh_send_cmd("fabricshow")
	print(resp)
	print("#"*80)
	print("\n\n")	
	ssh.close()

if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

