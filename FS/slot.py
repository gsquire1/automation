import paramiko
import sys
import time
ip = "10.38.36.230"
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

def slottoggle():
        
        connect = check_ssh(ip, uname, pwd)
        if (connect == True):
        	print "Inside slotshow"
        	stdin, stdout, stderr = ssh.exec_command("slotshow | grep SW |  awk '{print $1}'")
        	for line in stdout:
                        print line.strip('\n')
                        syncOutput = line.strip('\n')
			#cmd = "slotpoweroff %s;slotpoweron %s" % (syncOutput, syncOutput)
			cmd1 = "slotpoweroff %s" % (syncOutput)
		        	
			cmd2 = "slotpoweron %s" % (syncOutput)
			
			stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
 			print cmd1
			for line1 in stderr1:
                                print line1.strip('\n')
			time.sleep(150)
			stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
			print cmd2
			for line2 in stderr2:
                                print line2.strip('\n')
		return True
        else:
                print "No connection"
                return False

if __name__ == "__main__":

	for i in range(0,100):
		print i       
		status = slottoggle()
		print status
        	ssh.close()
