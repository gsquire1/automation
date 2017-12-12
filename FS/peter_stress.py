import paramiko
import sys
import time
ip = "172.26.26.189"
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
def lscreate(fid):
	syncOutput = []
	connect = check_ssh(ip, uname, pwd)
        if (connect == True):
		print "Inside lscreate"
		cmd = "lscfg --create %s -force" % (fid)
		print cmd
		stdin, stdout, stderr = ssh.exec_command(cmd)
		for line in stdout:
                        #print line.strip('\n')
                        syncOutput.append(line.strip('\n'))
		print syncOutput				
		successMsg = "Logical Switch with FID (%s) has been successfully created." %(fid)
		if (successMsg in syncOutput):
                       	print "Logical switch %s is created successfully" % (fid)
			ssh.close()
			return True
		else:
			print "Logical switch %s is not created" % (fid)
			ssh.close()
			return False
		
        else:
                print "No connection"
                return False
def lsdelete(fid):
	syncOutput = []
	connect = check_ssh(ip, uname, pwd)
	if (connect == True):
		print "Inside lsdelete"
		cmd = "lscfg --delete %s -force" % (fid)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		for line in stdout:
                        print line.strip('\n')
                        syncOutput.append(line.strip('\n'))
		if ("Switch successfully deleted." in syncOutput):
			print  "Switch %s successfully deleted" % (fid)
			ssh.close()
			return True
				
		else:
			print  "Switch %s not deleted" % (fid)
			ssh.close()
			return False
		
	else:
		print "No connection"
		return False

if __name__ == "__main__":
	for i in range(0,100):
		print i
		for fid in range(85,95):
               		print fid
                	status = lscreate(fid)
                	print status
		
			if (status == True):
				time.sleep(15)
				connect = check_ssh(ip, uname, pwd)
        			if (connect == True):
					cmd = "setcontext %s" % (fid)
					print "logged into ls %s" % (fid)
					stdin, stdout, stderr = ssh.exec_command(cmd)
					cmd1 = "lscfg --config %s -slot 2 -port 0-47 -force" % (fid)
					stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
					time.sleep(60)
					syncOutput = []
					for line in stdout1:
			                        print line.strip('\n')
                			        syncOutput.append(line.strip('\n'))
                			if ("Configuration change successful." in syncOutput):
						print "ports moved to newfid %s" % (fid)
					else:
						print syncOutput
						print "ports aren't moved"
						break
			
                			ssh.exec_command("switchdisable;switchenable")
					print "switch toggled"
					time.sleep(900)
				ssh.close()		

		connect = check_ssh(ip, uname, pwd)
        	if (connect == True):
			print "Inside deffaultmove"
			stdin2, stdout2, stderr2 = ssh.exec_command("lscfg --config 128 -slot 2 -port 0-47 -force")
			time.sleep(10)
			syncOutput = []
	                for line in stdout2:
        	        	print line.strip('\n')
                	        syncOutput.append(line.strip('\n'))
	                if ("Configuration change successful." in syncOutput):
        	        	print "ports moved to default fid 128"
				time.sleep(900)
                	else:
                		print syncOutput
	                        print "ports aren't moved"                      
		ssh.close()

	        for fid in range(85,95):         
			print fid
			stat = lsdelete(fid)
			time.sleep(60)
