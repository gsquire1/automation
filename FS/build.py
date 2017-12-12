import paramiko
import re
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
def fabric_ips():
	connect = check_ssh(ip, uname, pwd)
        if (connect == True):
		fabricIp = []
		print "Inside fabric ips function"
		stdin, stdout, stderr = ssh.exec_command("fabricshow | awk '{print $4}'")
		pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
		for line in stdout:
			status = pat.match(line.strip('\n'))
			if status:
				fabricIp.append(line.strip('\n'))
		print fabricIp
		ssh.close()
		return fabricIp
	else:
		print "No conection estabilished"
		return None	

def build(ip1):
	fwd = []
        statusfwd = 'Completed download of 110/110 packages (100%). Please wait...'
	connect = check_ssh(ip1, uname, pwd)
        if (connect == True):
        	stdin, stdout, stderr = ssh.exec_command('errdelimiterset -s "" -e "";coreshow -R; supportsave -R; errclear; fabriclog -c; tracedump -R; statsclear; slotstatsclear; fabstatsclear; fcrlogclear; echo y | historyclear; mp_util --bg_memtrace --enable')
        	for line in stdout:
                	print line.strip('\n')
                stdin1, stdout1, stderr1 = ssh.exec_command('echo y | firmwaredownload -p ftp 10.31.2.40,fvt,/buildsjc/sre/SQA/fos/v8.2.0/v8.2.0_bld41,pray4green')
                for line1 in stdout1:
                	fwd.append(line1.strip('\n'))
                if (statusfwd in fwd):
                        print "Firmware is being downloaded successfully in %s" % (ip1)
       		ssh.close()
	else:
                print "No connetion %s" % (ip1)


def buildstatus(ip2):
	connect = check_ssh(ip2, uname, pwd)
        if (connect == True):
        	stdin3, stdout3, stderr3 = ssh.exec_command('firmwaredownloadstatus')
        	for line2 in stdout3:
                	fwd_final_status = line2.strip('\n')
                if (fwd_final_status == 'Firmwaredownload command has completed successfully. Use firmwareshow to verify the firmware versions.'):
                	print "Firmwaredownload command has completed successfully in %s." % (ip2)
                else:
                 	print fwd_final_status
                ssh.close()
        else:
        	print "No connetion %s" % (ip2)

if __name__ == "__main__":
	fabricIps = fabric_ips()
	for ip1 in fabricIps:
		build(ip1)
	time.sleep(60*30)
	for ip2 in fabricIps:
		buildstatus(ip2)

