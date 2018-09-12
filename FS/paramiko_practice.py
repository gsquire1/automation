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
import os
import sys
import argparse
import csv
import sys
import time
import logging
import paramiko
import re
import threading

host = "10.39.36.112"
port = (int(22))
username = 'root'
password = 'password'
command = "show pdu"
bufsize = -1
# key_filename=''
timeout = 30
pkey = None
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


class SSH:
    shell = None
    client = None
    transport = None

    # def __init__(self, host, username, password):
        # self.connection = self.connect(host, username, password)

    # def __init__(self, host, username, password):
    def __init__(self, host, username, password):
        print("Connecting to server on ip", str(host) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        # self.client.connect(host, username, password, look_for_keys=False)
        # self.client.connect(host, username=username, password=password, look_for_keys=False)
        # self.client.connect(host, username, password, look_for_keys=False)
        # self.transport = paramiko.Transport((host, 22))
        # self.transport.connect(username, password)
        # self.transport.connect(username=username, password=password)

        # starts the output checking thread
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def openShell(self):
        self.shell = self.client.invoke_shell()

    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                print(strdata, end = "")
                if(strdata.endswith("$ ")):
                    print("\n$ ", end = "")







ssh = SSH(host,username,password)
ssh = ssh.openShell()
# f = channel.process()
info = ssh.sendShell('date')
print(info)
SSH.closeConnection()


# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('10.38.36.112', port=22, username='root', password='password')
# channel = ssh.invoke_shell()
# # channel.send() # Send a string to the shell session
# # channel.recv(9999) # Receive data from shell session. (9999) amount of bytes
# # channel.recv_ready() # If there is data to be read then read it.
# channel_data = str()
# host = str()
# srcfile = str()
#
#
# while True:
#     if channel.recv_ready():
#         channel_data += str(channel.recv(1024))  # If data read it and append to channel_data
#         # os.system('cls')
#         print('##### Device Output #####')
#         print(type(channel_data))
#         print(channel_data.strip('\r\n'))
#         # sync = (channel_data.strip('\r\n'))
#         # print(sync)
#         print('#########################')
#         host = input('\n\nEnter Date: ')
#         channel.send(host)
#         channel.send('\n')
#
#     else:
#         continue  # If no data continue

    # if channel_data.endswith('root>:'):
    # if channel_data.endswith("disclaimer.\r\n\r\n'"):
    #     channel.send('\r')
    # break
    # elif 'Ethernet' in channel_data:
    #     host = raw_input('\n\nEnter the IP Address: ')
    #     channel.send(host)
    #     channel.send('\n')
    # else:
    #     channel.send('\n')
    # if channel_data.endswith('root>:'):
    #     break
    # else:
    #     channel.send('\n')
    # if '(Timed out)' in channel_data:
    #     print('\nError: Connection to switch timed out'.format(host))
    #     channel_data = ''
    #     channel.send('\n')



# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# client.connect(hostname=host, port=port,
# username=user, key_filename=key_filename, banner_timeout=10)
# client.connect(hostname=host, port=port,
#                username=user, password='pass', pkey=None, banner_timeout=None)
# chan = client.get_transport().open_session()
# chan.settimeout(timeout)
# chan.set_combine_stderr(True)
# chan.get_pty()
# chan.exec_command(command)
# stdout = chan.makefile('r', bufsize)
# stdout_text = stdout.read()
# status = int(chan.recv_exit_status())
# client.close()
# return stdout_text, status
