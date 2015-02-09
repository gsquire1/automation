#!/usr/bin/env python3


###############################################################################
####
####  net install a switch of any 
####
###############################################################################

import os,sys

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')

import telnetlib
import getpass
import argparse
import re
import liabhar
import anturlar





def connect_console(HOST,usrname,password,port, *args):
    
    global tn
    var = 1
    reg_list = [b"aaaaa: ",  b"Login incorrect", b"option : ", b"root> ", b"login: ", b"r of users: "]   #### using b for byte string
    reg_list_r = [b".*\n", b":root> "]
    
    password = "pass"
    capture = ""
    option = 1
    #############################################################################
    #### parse the user name for console login
    ####
    port = str(port)
    usrname = parse_port(port)
    print("connecting via Telnet to  " + HOST + " on port " + port )
    print(HOST)
    print(usrname)
    print(password)
    print(port)
    
    tn = telnetlib.Telnet(HOST,port)
    print("tn value is  ", tn)
    
    tn.set_debuglevel(0)
    
    print("-------------------------------------------------ready to read lines")
    #############################################################################
    #### login 
    capture = tn.read_until(b"login: ")
    print(capture)
    tn.write(usrname.encode('ascii') + b"\r\n")
    #if password:
    capture = tn.read_until(b"assword: ")
    print(capture)
    tn.write(password.encode('ascii') + b"\r\n")
        
    
    #############################################################################
    #### login to the switch
    reg_list = [ b"Enter your option", b"login: ", b"assword: ", b"root> " ]  
    while var <= 4:
        #print("start of the loop var is equal to ")
        capture = tn.expect(reg_list)
        print(capture)
        
        if capture[0] == 0:
            tn.write(b"1\r\n\r\n")
                    
        if capture[0] == 1:
            tn.write(b"root\r\n")
                
        if capture[0] == 2:
            tn.write(b"password\r\n")
                    
        if capture[0] == 3:
            print(capture)
            break
        
        var += 1   
    
    
    return tn


def parse_port(port):
    print("port number " , port )
    print("\n\n")
    print("My type is %s"%type(port))
    print("\n\n\n\n")
    ras = re.compile('([0-9]{2})([0-9]{2})')
    ras_result = ras.search(port)
    print("port front  is  ",  ras_result.group(1))
    print("port back is    ",  ras_result.group(2))
    usrname = ras_result.group(2)
    if usrname < "10":
        ras = re.compile('([0]{1})([0-9]{1})')
        ras_result = ras.search(usrname)
        usrname = ras_result.group(2)
    usrname = "port" + usrname
    return usrname


def send_cmd(cmd, db=0):
    global tn
    
    tn.set_debuglevel(db)
    
    capture = ""
    reg_ex_list = [b'root>', b'.*\r\n']
    reg_ex_root = [b"root> "]
    #print(cmd)
    
    tn.write(cmd.encode('ascii') + b"\n")
    #capture_root = tn.expect(reg_ex_root, 30)
    capture = tn.expect(reg_ex_list, 3600)
    #capture = tn.expect(reg_ex_list, 30)
    #print(capture)
    
    
    capture = capture[2]
    
    #print(capture)
    
    
    capture = capture.decode()
    
    print(capture, end="")
    
    #print("SENDING COMMAND TO THE SWITCH")
    
    return(capture)



    
def main():

    global tn
    
    cons_ip = "10.38.32.156"
    cons_port = 3008
    my_ip = "10.38.37.50"
    user_name = "root"
    psswd = "password"
    
    
    #cons_out = anturlar.login()
    tn  = connect_console(cons_ip,user_name,psswd,cons_port)
    
    tn.set_debuglevel(9)
    
    

    cons_out = send_cmd("\n\n")
    #print(cons_out)
    
    cons_out = send_cmd("switchshow")
    
    #print(cons_out)
    
    cons_out = send_cmd("fabricshow")
    #print(cons_out)
    
    
    
    tn.write(b"exit\n")
    tn.close()
    
    
    
    
    
    
    
    
    
    
main()



