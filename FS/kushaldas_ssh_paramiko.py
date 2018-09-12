#!/usr/bin/env python

# def run(host='127.0.0.1', port=22, user='root',
#                   command='/bin/true', bufsize=-1, key_filename='',
#                   timeout=120, pkey=None):
"""
Excecutes a command using paramiko and returns the result.
:param host: Host to connect
:param port: The port number
:param user: The username of the system
:param command: The command to run
:param key_filename: SSH private key file.
:param pkey: RSAKey if we want to login with a in-memory key
:return:
"""

import paramiko
import logging
import

host = "10.39.36.112"
port = (int(22))
user = 'user'
password = 'pass'
command = "show pdu"
bufsize=-1
#key_filename=''
timeout=30
pkey=None
#### ATTEMPT AT LOGGING
# #create logger for paramiko and set level
# logger = logging.getLogger('paramiko')
# logger.setLevel(logging.DEBUG)
# #create file handler which logs even debug messages
# fh = logging.FileHandler('paramiko.log')
# fh.setLevel(logging.DEBUG)
# #creat console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# #create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# #add the handlers to the logger
# logger.addHandler(fh)
# logger.addHandler(ch)


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#client.connect(hostname=host, port=port,
		#username=user, key_filename=key_filename, banner_timeout=10)
client.connect(hostname=host, port=port,
		username=user, password='pass', pkey=None, banner_timeout=None)
chan = client.get_transport().open_session()
chan.settimeout(timeout)
chan.set_combine_stderr(True)
#chan.get_pty()
chan.exec_command(command)
stdout = chan.makefile('r', bufsize)
stdout_text = stdout.read()
status = int(chan.recv_exit_status())
client.close()
#return stdout_text, status

