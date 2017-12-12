import paramiko
import sys
import time
ip = "10.38.36.40"
uname = "root"
pwd = "password"

def check_ssh( ip, user, pwd):
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
                ssh.connect(ip, username=user, password=pwd)
                return True
        except Exception as e:
                print e
                return False

def switchtoggle():
	connect = check_ssh(ip, uname, pwd)
        if (connect == True):
		stdin, stdout, stderr = ssh.exec_command('switchdisable')
		print "switchdisabled"
		time.sleep(300)
		stdin1, stdout1, stderr1 = ssh.exec_command("switchshow | grep switchState | awk '{ print $2 }'")
		for line in stdout1:
			syncOutput = line.strip('\n')
		print syncOutput		
		if (syncOutput == 'Offline'):
			stdin, stdout, stderr = ssh.exec_command('switchenable')
			print "switchenabled"
			time.sleep(1500)
			stdin3, stdout3, stderr3 = ssh.exec_command("switchshow | grep switchState | awk '{ print $2 }'")
			for line in stdout3:
	                        syncOutput = line.strip('\n')
			print syncOutput

	else:
		print "no connection"
		
		

if __name__ == "__main__":
		
		for i in range(0,100):
			print i
			switchtoggle()
					
