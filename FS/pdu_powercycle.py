#!/usr/bin/env python

import paramiko
import sys
import time
import select

ip = "10.39.36.112"
uname = "user"
user = "user"
pwd = "pass"
#host = "10.38.36.24"
yesSync = 0
i = 1
def check_ssh(ip, user, pwd):
	global ssh
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(ip, username=user, password=pwd)
		return True
	except Exception as e:
		print (e)
		return False

# def haFailover():
# 	print ("Inside HAFailover function")
# 	connect = check_ssh(ip, uname, pwd)
# 	if (connect == True):
# 		stdin, stdout, stderr = ssh.exec_command('echo y|hafailover')
# 		print ("Executed hafailover")
# 		time.sleep(150)	
# 		ssh.close()
# 		return True
# 	else:
# 		print ("No connection")
# 		return False
 
# def haShow(yesSync):
# 	print ("Inside HAShow")
# 	syncOutput = ''
# 	connect = check_ssh(ip, uname, pwd)
# 	if (connect == True):
# 		print ("inside hashow connect")
# 		stdin, stdout, stderr = ssh.exec_command('hashow | grep synchronized')
# 		#print (stdout)
#         	for line in stdout:
#         		print ("hashow output %s" % (line.strip('\n')))
# 			syncOutput = line.strip('\n')
# 		ssh.close()
# 		if (syncOutput == 'HA enabled, Heartbeat Up, HA State synchronized'):
# 			print( "HA synchronized")
# 			return True
# 		else:
# 			print( "Not synchronized yet, Trying again")
# 			time.sleep(60)
# 			yesSync += 1
# 			if (yesSync < 5):
# 				return haShow(yesSync)
# 			else:
# 				print( "Tried max times of HAShow")
# 				return False
# 	else:
# 		print( "No connection")
# 		return False

#def slottoggle():
        
#         connect = check_ssh(ip, uname, pwd)
#         if (connect == True):
#         	print( "Inside slotshow")
#         	stdin, stdout, stderr = ssh.exec_command("slotshow | grep SW |  awk '{print $1}'")
#         	for line in stdout:
#                         print( line.strip('\n'))
#                         syncOutput = line.strip('\n')
# 			#cmd = "slotpoweroff %s;slotpoweron %s" % (syncOutput, syncOutput)
# 			cmd1 = "slotpoweroff %s" % (syncOutput)
# 		        	
# 			cmd2 = "slotpoweron %s" % (syncOutput)
# 			
# 			stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
#  			print( cmd1 )
# 			for line1 in stderr1:
#                                 print( line1.strip('\n'))
# 			time.sleep(150)
# 			stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
# 			print( cmd2 )
# 			for line2 in stderr2:
#                                 print( line2.strip('\n'))
# 		return True
#         else:
#                 print( "No connection" )
#                 return False

if __name__ == "__main__":


	# for i in range(0,1):
	# 	print( i )
	# 	status = check_ssh(ip,uname,pwd)
	# 	print( "ssh status %s" %status )
	# 	if (status):
	# 		print( "Inside PDU????")
	# 		stdin, stdout, stderr = ssh.exec_command("switchshow")
	# 		print("Starting While Loop")
	# 		while not stdout.channel.exit_status_ready():
	# 			if stdout.channel.recv_ready():
	# 				rl, wl, xl = select.select([stdout.channel], [],[], 0.0)
	# 				print(rl)
	# 				if len(rl) > 0:
	# 					print (stdout.channel.recv(1024),)		
	# 		for line in stdout:
	# 			print(line)
	# 			print ("out output %s" % (line.strip('\n')))
	# 		print("stdin status %s" % stdin)
	# 		print("stdout status %s" % stdout)
	# 		print("stderr status %s" % stderr)
	# 		#for line in stdout:
	# 			#print(line.strip('\n'))
	# 			#syncOutput = line.strip('\n')
	# 		ssh.close()
	# 		sys.exit()
	# 		ssh.close()
	# 		if not stat:
	# 			break
	# 		else:
	# 			slotstatus = slottoggle()
	# 			print( "Slot toggle status %s" % slotstatus )
	# 	else:
	# 		print( "No connection" )
	# 		break
		
	# for i in range(0,100):
	# 	print( i )
	# 	status = haFailover()
	# 	print( "Hafailover status %s" %status )
	# 	if (status):
	# 		stat = haShow(yesSync)
	# 		print( "Hashow status %s" % stat )
	# 		if not stat:
	# 			break
	# 		else:
	# 			slotstatus = slottoggle()
	# 			print( "Slot toggle status %s" % slotstatus )
	# 	else:
	# 		print( "No connection" )
	# 		break

#######################################
# Try to connect to the host.
# Retry a few times if it fails.
#
	while True:
		print ("Trying to connect to %s (%i/30)" % (ip, i))
	
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip, username=user, password=pwd)
			print ("Connected to %s" % ip)
			break
		except paramiko.AuthenticationException:
			print ("Authentication failed when connecting to %s" % ip)
			sys.exit(1)
		except:
			print ("Could not SSH to %s, waiting for it to start" % ip)
			i += 1
			time.sleep(2)
	
		# If we could not connect within time limit
		if i == 30:
			print ("Could not connect to %s. Giving up" % ip)
			sys.exit(1)
	
	# Send the command (non-blocking)
	time.sleep(5)
	stdin, stdout, stderr = ssh.exec_command("power outlets 10 cycle /y")
	
	# Wait for the command to terminate
	while not stdout.channel.exit_status_ready():
		# Only print data if there is data to read in the channel
		if stdout.channel.recv_ready():
			rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
			if len(rl) > 0:
				# Print data from stdout
				print (stdout.channel.recv(2048),)
	# Disconnect from Host
	print("Command done, closing ssh")
	ssh.close()
					   