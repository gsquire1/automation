#!/usr/bin/env python3

 #!/usr/bin/python 
 
 
 # All SSH libraries for Python are junk (2011-10-13). 
 # Too low-level (libssh2), too buggy (paramiko), too complicated 
 # (both), too poor in features (no use of the agent, for instance) 
 
 
 # Here is the right solution today: 
 
 
import subprocess 
import sys 
 
 
HOST="10.39.36.112"
USER="user"
PASSWORD="pass"
 # Ports are handled in ~/.ssh/config since we use OpenSSH 
COMMAND="uname -a" 
proc = subprocess.Popen(PASSWORD)
ssh = proc.communicate(["ssh", "%s" % HOST, COMMAND],
#ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND], 
#ssh = subprocess.Popen(["ssh", HOST, USER, PASS, COMMAND], 
                        shell=False, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE) 
result = ssh.stdout.readlines() 
if result == []: 
    error = ssh.stderr.readlines() 
    print(sys.stderr, "ERROR: %s" % error) 
else: 
    print(result) 
