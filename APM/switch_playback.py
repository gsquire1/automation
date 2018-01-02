#!/usr/bin/env python3

####
#  this is the old way of calling python3   
#!/opt/python3/bin/python3
#Graham

###############################################################################
####
####  net install a switch of any 
####
###############################################################################

import os,sys
import os.path

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')
sys.path.append('/home/automation/lib/SDK')

import telnetlib
import getpass

import struct

import argparse
import re
import csv
import time

###############################################################################
####
####  import user modules
####
###############################################################################
import anturlar
import liabhar
import cofra

###############################################################################
#
# SDK Modules
#
###############################################################################
from raritan.rpc import Agent, pdumodel, firmware, sensors


###############################################################################
####
####  switch types
####
####  62  DCX
####  64  5300
####  66  5100
####  67  Encryption switch
####  70  5410 - embedded switch
####  71  300
####  72  5480 - embedded switch
####  73  5470 - embedded switch
####  75  M5424 - embedded switch
####  77  DCX-4S
####  83  7800
####  86  5450 - embedded switch
####  87  5460 - embedded switch
####  92  VA-40FC
####  109  6510
####  117  6547  - embedded switch
####  118  6505
####  120  DCX 8510-8
####  121  DCX 8510-4
####  124  5430  - embedded switch
####  125  5431
####  129  6548  - embedded switch
####  130  M6505  - embedded switch
####  133  6520 - odin
####  134  5432  - embedded switch
####  
####  141  Yoda DCX
####  142  Yoda pluto
####  148  Skybolt
####
####  162.0  Wedge
####  165   X6-4 (Venator)
####  166   X6-8 (Allegience)
####  170   Chewbacca
####   173 TYR
#### 
###############################################################################


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    #pp.add_argument("--repeat", help="repeat repeat")
    pp.add_argument("firmware", help="firmware verison 8.1.0_bldxx")
    pp.add_argument("-fa", "--file_action", help="0 to stop after creating file                            \
                                                  1 to create new file and continue                        \
                                                  2 skip file create and use your own file                 \
                                                  3 rebuild the switch from previously saved file          ", \
                                                  type=int, default=0 )
 
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return(pp) 

def parse_args(args):
    
 
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    parser.add_argument('-cp',   '--cmdprompt', help="switch is already at command prompt", action="store_true")
    parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
    parser.add_argument('-f',    '--filename',   help="File name to use instead of the default file", default="for_playback")
    parser.add_argument('-d',    '--cust_date',      help=argparse.SUPPRESS, )
         
    args = parser.parse_args()
    print(args)
    
    if not args.chassis_name and not args.ipaddr:
        print("Chassis Name or IP address is required")
        sys.exit()
        
    if args.cmdprompt and not args.switchtype:
        print("To start at the command prompt the switch type is needed.")
        sys.exit()
        
    if not args.cmdprompt and args.switchtype:
        print('To start at the command prompt both switch type and command prompt is requried')
        sys.exit()
    
    if not args.firmware:
        print("0 to stop after creating file 1 to create new file and continue 2 skip file create and use your own file")
    
    if args.file_action >= 4:
        print("\n\nfa (file action ) is required to be 0,1,2,3    \n\n \
                       0 to stop after creating file  \n\
                        1 to create new file and execute the Netinstall and restore the switch \n\
                        2 skip file create and use your own file to restore the switch \n\
                        3 rebuild the switch from previously saved file \n\n\n")
        sys.exit()

    return(parser.parse_args())

def start_of_func_print(func_name):
    """
        print a message for reference about the start of a function
        
    """
    print("@"*120)
    print("#"*120)
    print("####")
    print("####\n\n")
    print("STARTING THE FUNCTION   \n\n")
    print(func_name)
    print("\n\n")
    print("####")
    print("####")
    print("#"*120)
    print("@"*120)
    
    return(True)

def info_help_OSError():
    """
    """
    print("\n  If the Switch is at the command prompt use the -cp and -t switch")
    print("\n  ./APM/switch_playback.py -cp -t <no> -c <chassisname> <firmware>")
    print("\n\n  Popular switch types are:\n")
    print("       Type      Model\n")
    print("\t62       DCX\n\t64       5300\n\t66       5100\n\t71       300 \n")
    print("\t77       DCX-4S\n\t83       7800\n\t109      6510\n\t118      6505\n")
    print("\t120      DCX 8510-8\n\t121      DCX 8510-4")
    print("\t133      6520/Odin\n\t148      Skybolt ")
    print("\t165      Venator\n\t166      Allegiance ")
    print("\n"*5)
    sys.exit()

def connect_console_enable_root(HOST,usrname,password,port,db=10, *args):
    
    global tn
    
    var = 1
    reg_list = [ b"Enter your option : ", \
                b"login: ", \
                b"assword: ", \
                b"root> ", \
                b".*?users: ", \
                b"Login incorrect", \
                b"=>" , \
                b"admin>", \
                b"key to proceed.", \
                b"Authentication failure" , \
                b" login: ", \
                b"no]" , \
                b"all':"            ]


    password = "pass"
    capture = ""
    option = 1
    #############################################################################
    #### parse the user name for console login
    ####
    port = str(port)
    usrname = parse_port(port)
    print("connecting via Telnet to  Console  " + HOST + " on port " + port )
    print(HOST)
    print(usrname)
    print(password)
    print(port)
    ###########################################################################
    ####
    #### connect to the console via telnet
    ####   this is connection to console before login 
    ####
    tn = telnetlib.Telnet(HOST,port)
    print("tn value is  ", tn)
    tn.set_debuglevel(db)
    print("@"*80)
    print("CONSOLE==="*8)
    print("CONNECTED VIA TELNET TO THE CONSOLE ")
    print("NEXT STEP IS TO LOGIN TO THE CONSOLE")
    print("\n"*4)
    
    ####liabhar.JustSleep(120)
    
    #############################################################################
    #### login console  
    ####  start the login procedure
    ####
    #############################################################################
    ####
    #### some consoles would not need to login steps so if the capture after the
    ####    telnet login are the words 'Enter your login: '  or reglist 0
    ####     if this is found we can move to the next step if not then login
    ####      to the console
    ####
    ####   steps for both types of consoles
    ####    1. console 1 displays a message "Welcome to Console Server Managment Server .....port SXXX
    ####       - look for this message
    ####          - login to the console
    ####
    ####    2. check for timeout of so many seconds
    ####       - if timeout send a \n and look for login
    ####
    ####    3. should be at switch login 
    ####
    ####
    tn = connect_console(HOST,usrname,password,port,db=10, *args)
  

    ###################################################################################################################
    ####
    ####  this sends number 1 when there are more than one user on the console
    ####
    ###################################################################################################################
    print("CONNECTED TO CONSOLE IN PLAYBACK and ENABLE ROOT ")
    #liabhar.JustSleep(60)
    
    #if capture[0] == 0:
    #    tn.write(struct.pack('!b', 49))   #### use the struct to send a integer
    #    #print("\n"*11)
    #    #tn.write(b"\n")
    #    capture = tn.expect(reg_list)
    #    print(capture)
    #    print("END CAPTURE PRINT OUT !!!!!!!!!!!!!!!!!!!!! ")
    #else:
    #    tn.write(b"\n")
    
    print("3___"*20)
    tn.write(b"password\n")
    capture = tn.expect(reg_list)
    
    #print("send password   and login as root ")
    #print(capture)
    #print("LOGIN CHANGE PASSWORDS  A"*3)
    ###################################################################################################################
    ####
    ####  find login or the user that is logged in. 
    ####
    ###################################################################################################################
    print("4___"*20)
    
    
    if capture[0] == 0:
        #tn.write(struct.pack('!b', 49))   #### use the struct to send a integer
        tn.write(struct.pack('!b', 52))   #### use the struct to send a integer  #### send a 4 to kill all sessions
        #print("\n"*11)
        #tn.write(b"\n")
        capture = tn.expect(reg_list)
        if capture[0] == 12:
            tn.write(b"all\n")
        print("send password   and login as root ")
        print(capture)
        print("LOGIN CHANGE PASSWORDS  A FOUND OPTION: "*3)
    else:
        tn.write(b"\n")
        capture = tn.expect(reg_list)
        print("send password   and login as root ")
        print(capture)
        print("LOGIN CHANGE PASSWORDS  A FOUND OPTION: but fell to ELSE"*3)
    
    if capture[0] == 4:          ####  found the users: after starting a regular session
        print("FOUND USER ")
        tn.write(b"\n")
        capture = tn.expect(reg_list)  ####  nothing to do execpt wait for the login or user prompt
        print("send password   and login as root ")
        print(capture)
        print("LOGIN CHANGE PASSWORDS  A EXIT FOUND USER "*3)
    if capture[0] == 2:#### if Password is found we did not enter the user name yet.
        print("FOUND PASSWORD  ")
        tn.write(b"\n")          ####  so send a \n so we can get the login prompt
        capture = tn.expect(reg_list)
        print("send password   and login as root ")
        print(capture)
        print("LOGIN CHANGE PASSWORDS  A EXIT FOUND PASSWORD "*3)
    if capture[0] == 3:           ##### if root is logged in should be able to continue from here
        print("FOUND ROOT : ")
             
    if capture[0] == 7:           #### if admin is found log out and see if passwords are changed and root is enabled
        print("FOUND ADMIN : ")   #### 
        tn.write(b"exit\n")
        capture = tn.expect(reg_list)
        print("send exit and and login as root ")
        print(capture)
        print("LOGIN CHANGE PASSWORDS  A"*3)
              
    if capture[0] == 1:            ####  found login login as Admin 
        print("FOUND LOGIN : ")    ####    change the root permissions for root then loggin as root
        tn.write(b"admin\n")
        capture = tn.expect(reg_list)
        print("send exit and login as root next ")
        print(capture)
        print("LOGIN CHANGE PASSWORDS  B LOGIN AS ADMIN"*3)
        
        if capture[0] == 2:                 ####  is password
            print("FIND 2  "*10 )
            tn.write(b"password\n")
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
        
        if capture[0] == 8:                 ####   old password for admin
            tn.write(b"password\n")
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"password1\n")         #### enter new password
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"password1\n")         #### enter new password
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"password\n")         #### enter new user password
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"password\n")         #### enter new user password
            capture = tn.expect(reg_list) 
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"userconfig --change root -e yes\n")         #### enable root
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"rootaccess --set all\n")         #### enable root
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"yes\n")         #### question Please confirm to proceed
            capture = tn.expect(reg_list)
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            
            tn.write(b"exit\n")         #### enable root
            capture = tn.expect(reg_list)   
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"root\n")         #### enable root
            capture = tn.expect(reg_list)   
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"fibranne\n")         #### enable root
            capture = tn.expect(reg_list) 
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"fibranne\n")         #### enable root
            capture = tn.expect(reg_list) 
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"password\n")         #### enable root
            capture = tn.expect(reg_list) 
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"password\n")         #### enable root
            capture = tn.expect(reg_list) 
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)
            tn.write(b"firmwareshow\n")         #### enable root
            capture = tn.expect(reg_list) 
            print("send password   and login as root ")
            print(capture)
            print("LOGIN CHANGE PASSWORDS  A"*3)

                        
    print("\n"*8)
    print("@"*30)
    print("@"*30)
    print("@"*30)
    print(capture)
    tn.write(b"timeout 0\n")
    capture = tn.expect(reg_list)
    print("\n"*10)
    print(capture)
    print("\n"*10)
    liabhar.JustSleep(10)

    return(tn)

def connect_console(HOST,usrname,password,port,db=0, *args):
    
    global tn
    
    
    var = 1
    reg_list = [b"aaaaa: ",  b"Login incorrect", b"option : ", b"root> ", b".*?login: ", b"r of users: ", b"admin> "]   #### using b for byte string
    reg_list_r = [b".*\n", b":root> ", b":admin> "]
    
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
    tn.set_debuglevel(db)
    print("\n\n")
    print("-"*80)
    print("-"*80)
    print("CONNECTING TO THE CONSOLE-------------------------------------------")
    print("-------------------------CONNECT CONSOLE FUNCTION-------------------")
    print("-------------------------------------------------ready to read lines")
    tn.write(b"\n")
    #############################################################################
    #### login
    capture = tn.expect(reg_list)
    #capture = tn.read_until(b".*?login: ")
    print(capture)
    if capture[0] == 4:        
        tn.write(usrname.encode('ascii') + b"\n")
        #if password:
        capture = tn.read_until(b"assword: ")
        print(capture)
        tn.write(password.encode('ascii') + b"\n")  
        print("\n\n\n\n\n\n\n\n")
    #tn.close()
    #sys.exit()
    
    #############################################################################
    ####
    #### login to the switch
    ####
    ####
    ####
    reg_list = [ b"Enter your option : ", b"login: ", b"assword: ", b"root> ", b"users: ", b"=>" , b"admin> ", b"sh-2.04#"]  
    while var <= 4:
        #print("start of the loop var is equal to ")
        capture = ""
        capture = tn.expect(reg_list,20)
        if capture == -1:
            print(capture)
            sys.exit()
        print(capture)
        
        if capture[0] == 0:
            
            tn.write(struct.pack('!b', 49))   #### use the struct to send a integer 
            ####
                    
        if capture[0] == 1:
            tn.write(b"root\n")
            capture = tn.expect(reg_list,20)
            tn.write(b"password\n")
            capture = tn.expect(reg_list,20)
            if capture[0] == 1:
                tn.write(b"admin\n")
                capture = tn.expect(reg_list,20)
                tn.write(b"password\n")
                if capture[0] == 1:
                    tn.write(b"admin\n")
                    capture = tn.expect(reg_list,20)
                    tn.write(b"fibranne\n")   
                
            
        if capture[0] == 2:
            tn.write(b"password\n")
                    
        if capture[0] == 3:
            #print(capture)
            print("this found root")
            tn.write(b"\n")
            break
        
        if capture[0] == 4:
            #print(capture)
            print("\n\n\n\n\n\nFOUND USERS: \n\n")
            #capture = ""
            
            tn.write(b"\n")
            #capture = tn.expect(reg_list)
            #break
        if capture[0] == 5:
            print(capture)
            tn.write(b"\n")
            var += 4
            break
        
        if capture[0] == 7:  #### at the bash prompt ready to power cycle
            print("\n\nswitch is at the BASH prompt\n\n")
            print("I was expecting the command prompt or FOS prompt\n\n")
            #tn.write(b"\n")
            #sys.exit()
            #break
        
        var += 1
    capture = ""  
    capture = tn.expect(reg_list, 20)
    print("Console "*10)
    print(capture)
    print("Console_"*10)    
    if capture[0] == 1 :
        #print("SENDINGROOT")
        tn.write(b"root\n")
        capture = tn.expect(reg_list, 20)
        tn.write(b"password\n")
        capture = tn.expect(reg_list, 20)
        

    #capture = tn.expect(reg_list, 20)
    
    return(tn)
    
def stop_at_cmd_prompt(db=0):
    global tn
    
    tn.set_debuglevel(db)
    print("\n\n\n\n\n\n\n\nlooking for stop autoboot\n\n")
    
    #cons_out = send_cmd("/sbin/reboot")
    #
    #
    reg_list = [ b"Hit ESC to stop autoboot: "]
 
    tn.write(b"/sbin/reboot\n")
    capture = tn.expect(reg_list, 3600)
    
    #tn.write( b"char(27)")  #### char(27) or \x1b are both ESC 
    tn.write(b"\x1b")
    reg_list = [b"Option?"]
    
    capture = tn.expect(reg_list)
    #tn.write(b"3\n")
    tn.write(b"3\r\n")
    
    reg_list = [ b"=>"]
    capture = tn.expect(reg_list, 300)
    
    return(capture)
       
def env_variables(swtype, gateway_ip, db=0): #put new gateway variable here

    #liabhar.count_down(10)
    
    pa = parse_args(sys.argv)
    if pa.verbose >=3:
        db=10
    tn.set_debuglevel(db)                                   #### set the telnet debug level                        ####   
    
    if pa.verbose >=3:
        start_of_func_print("  env_variables")
    
    capture = ""
    ras = re.compile('.\d{1,3}.\d{1,3}.(\d{1,3}).\d{1,3}')
    gw_octet = ras.findall(gateway_ip)
    gw_octet = int(gw_octet[0])

    #### set the temp ip address --it has to have some ip so add a temp one
    ####   if gw_octet is 128 it for the raised flow other wise the rest
    ####    of 3rd floor
    ####
    if gw_octet == 128:
        fake_ip = "10.38.134.2"
    else:
        fake_ip = "10.38.34.100"
    ###################################################################################################################
    #### define the reg expression list of what needs to be found
    ####
    ###################################################################################################################
    reg_list = [b"=>"]
    reg_list_done = [b"done",b"NVRAM..."]
    reg_alive     = [b"is alive\r\n=>"]
    reg_bash = [ b"bash-2.04"]
    #### check if the switch is at the boot prompt
    #### if it is at the switch prompt it is wrong    
    capture = tn.expect(reg_list,30)
    tn.write(b"date\n")

    capture = tn.expect(reg_list)
    if pa.verbose >=3 :
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("A"*80)
    
    tn.write(b"printenv\n")                                 #### print the environmental variables                 #### 
    capture = tn.expect(reg_list)                           #### caputure the output from printenv and look for => ####
    
    if pa.verbose >=3 :
        print("send printenv   and look for =>")
        print("\n\n")
        print(capture)
        print("B"*80)
    
    netmask   = "255.255.240.0"                             ####  set the netmask value                            ####
    #### for all switches except WEDGE (for now) need the bootargs ip=off setting                                  ####
    ###  the exceptions are below for skybolt and wedge                                                            ####
    bootargs  = "bootargs ip=off"                                                                                  ####
    
    if swtype == '162' or swtype == '166' or swtype == '165'  or swtype == '173':   #### HANDLE WEDGE and Allegiance bootargs here    ####
        bootargs  = "root=/dev/sda\$prt rootfstype=ext4 console=ttyS0,9600 quiet"
    if swtype == '170':   ####  CHEWBACCA
        bootargs  = "root=/dev/sda\$prt rootfstype=ext4 console=ttyS0,9600 quiet"
        
    ethrotate = "no"                                             ####  always set ethrotate to no                  ####
    server_ip = "10.38.2.40"                        #### Set the TFTP server                                       ####
                                                    #### So if server changes or multiple servers etc.             ####
    ####  ethact default is ENET0                                                                                  ####
    ####   for some switches is other values are needed and are set by switch type                                 ####
    ethact    = "ENET0"
    if swtype == '162' or swtype == '148' or swtype == '170' or swtype == '173':     #### set the wedge and skybolt values for ethact ####  
        ethact = "FM1@DTSEC2"
    
    if swtype == '166' or swtype == '165':                   ####   ethprime is a new env variable and             ####
        ethact = "FM2@DTSEC4"                                ####  "ethact =" between Allegiance                   ####
        a = ("setenv ethprime FM2@DTSEC4 \n")                ####  and Wedge are different                         ####
        tn.write(a.encode('ascii'))

        capture = tn.expect(reg_list)
        if pa.verbose >=3:
            print("send set the ethprime value    and look for =>")
            print("\n\n")
            print(capture)
            print("C"*80)
    ###################################################################################################################
    ###################################################################################################################
    ####                                                                                                           ####
    ####capture = tn.expect(reg_list, 10) ####  add this capture since the next two writes are running together.   ####
    ####                                                                                                           ####
    #### was hanging here until on the switch a newline was sent.                                                  ####
    #### the next two lines are to take care of the hang                                                           ####
    ###################################################################################################################
    ###################################################################################################################
    
    if swtype == '162' or swtype == '165' or swtype == '166' :              ####  wedge requires a Enter command or ####
        newline = "\n"                                                     ####  hangs at the prompt               ####
        tn.write(newline.encode('ascii'))                                  ####                                    ####
        capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("setting the environmental variables \n\n")
        print("   and look for =>")
        print("\n\n")
        print(capture)
        print("D"*80)
    
    ###################################################################################################################
    ###################################################################################################################
    ####
    ####
    ###################################################################################################################
    ###################################################################################################################
    a = ("setenv ethact %s \n" % ethact)     
    tn.write(a.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send ethatc command   and look for =>")
        print("\n\n")
        print(capture)
        print("E"*80)
    
    g = ("setenv gatewayip %s \n" % gateway_ip)
    tn.write(g.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send gateway ip    and look for =>")
        print("\n\n")
        print(capture)
        print("F"*80)
    
    n = ("setenv netmask %s\n"%netmask)
    tn.write(n.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send netmask   and look for =>")
        print("\n\n")
        print(capture)
        print("G"*80)
    b = ("setenv bootargs %s\n"%bootargs)
    tn.write(b.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send bootargs    and look for =>")
        print("\n\n")
        print(capture)
        print("H"*80)
    e = ("setenv ethrotate %s\n"%ethrotate)
    tn.write(e.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send ethrotate   and look for =>")
        print("\n\n")
        print(capture)
        print("I"*80)
    
    s = ("setenv serverip %s\n"%server_ip)
    tn.write(s.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send serverip    and look for =>")
        print("\n\n")
        print(capture)
        print("J"*80)

    i = ("setenv ipaddr %s\n" % fake_ip)
    tn.write(i.encode('ascii'))
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send setenv ipaddr    and look for =>")
        print("\n\n")
        print(capture)
        print("K"*80)
    
    tn.write(b"saveenv\n")
    capture = tn.expect(reg_list_done)
    if pa.verbose >=3:
        print("send Save env   and look for =>")
        print("\n\n")
        print(capture)
        print("L"*80)
    
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send second capture command   and look for =>")
        print("\n\n")
        print(capture)
        print("M"*80)
    
    tn.write(b"printenv\n")    
    capture = tn.expect(reg_list)
    if pa.verbose >=3:
        print("send printenv   and look for =>")
        print("\n\n")
        print(capture)
        print("N"*80)
    
    p = ("ping %s  \n" % gateway_ip)
    tn.write(p.encode('ascii'))
    tn.write(b"\n")
    capture = tn.expect(reg_alive)
    if pa.verbose >=3:
        print("send PING command   and look for  alive =>")
        print("\n\n")
        print(capture)
        print("O"*80)
        print("send send nothing just leaving   ")
        print("oh my \n")
        print("          leaving the env variable proc ")
        print("\n\nCOMPLETE with loading ENV VARIABLES\n\n")
    
    return(True)

def pwr_cycle(pwr_ip, pp, stage, db=0):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    
    anturlar.power_cmd("" ,10)
    anturlar.power_cmd("cli" ,10)
    anturlar.power_cmd("cd access/1\t/1\t%s" % pp ,10)
    #anturlar.power_cmd("show\n" ,10)
    
    anturlar.power_cmd(stage, 5)
    anturlar.power_cmd("yes", 5)
    
    #liabhar.JustSleep(10)
    anturlar.power_cmd("exit", 10)
     
    print("\n"*10)
    print("Just sent power pole  %s port %s   %s command " % (pp, stage,pwr_ip))
    print("\n"*5)
    
    return(0)

def raritan(port, status, ip="10.39.36.112", user="user", pw="pass"):
    
    agent = Agent("https", ip, user, pw, disable_certificate_verification=True)
    pdu = pdumodel.Pdu("/model/pdu/0", agent)
    firmware_proxy = firmware.Firmware("/firmware", agent)
    
    inlets = pdu.getInlets()
    ocps = pdu.getOverCurrentProtectors()
    outlets = pdu.getOutlets()
    
    print ("PDU: %s" % (ip))
    print ("Firmware version: %s" % (firmware_proxy.getVersion()))
    print ("Number of inlets: %d" % (len(inlets)))
    print ("Number of over current protectors: %d" % (len(ocps)))
    print ("Number of outlets: %d" % (len(outlets)))
    port = (int(port))
    port = (port-1)
    print(type(port))
    print(port)
    outlet = outlets[port]
    outlet_metadata = outlet.getMetaData()
    outlet_settings = outlet.getSettings()
    
    print ("Outlet %s:" % (format(outlet_metadata.label)))
    print ("  Name: %s" % (outlet_settings.name if outlet_settings.name != "" else "(none)"))
    print ("  Switchable: %s" % ("yes" if outlet_metadata.isSwitchable else "no"))
    
    
    if outlet_metadata.isSwitchable:
        outlet_state = outlet.getState()
        print("OUTLET_GET_STATE")
        print(outlet_state)
        if outlet_state.available:
            #print ("  Status :%s" % ("on" if outlet_state.value == outlet_state_sensor.OnOffState.ON.val else "off"))
            print ("  Status :%s" % ("on" if outlet_state.powerState == pdumodel.Outlet.PowerState.PS_ON else "off"))
        if status == "off":
            print ("  Turning outlet off...")
            outlet.setPowerState(outlet.PowerState.PS_OFF)
            print ("  Sleeping 4 seconds...")
            time.sleep(4)
        else:
            print ("  Turning outlet on...")
            outlet.setPowerState(outlet.PowerState.PS_ON)
            outlet_state = outlet.getState()
        #if outlet_state.available:
            #print ("  Status :%s" % ("on" if outlet_state.powerState == pdumodel.Outlet.PowerState.PS_ON else "off"))
    else:
        print("THIS PDU DOES NOT SUPPPORT CLI POWERCYCLING")
    
def load_kernel(switch_type, sw_ip, gateway_ip, frm_version): ###ADDED GATEWAY HERE
    
    #reg_list = [ b"^=> "]
    reg_list =  [b"=>"]
    reg_bash = [ b".*?bash-2.04#", b".*?=> ", b"bash-2.04#"]
    reg_bash = [ b"bash-2.04", b"=> "]
    reg_bash = [ b"bash-2.04"]
    reg_bash_only = [ b"bash-2.04" ]
    reg_linkup = [ b".*?ink is up"]
    
    #### set tftp command
    pa = parse_args(sys.argv)
    if pa.verbose >=3:
        start_of_func_print("  LOAD KERNEL ")
    #ras = re.compile('([\.a-z0-9]+)(?:_)?')
    ras = re.compile('([\.v0-9]+)(?:_)?')
    ras = ras.search(frm_version)
    frm_no_bld = ras.group(1)
    if 'amp' in frm_version:
        frm_no_bld = frm_no_bld + '_amp'
    
    
    if switch_type == '170':  ####  CHEWBACCA
        nbt = "makesinrec 0x1000000 \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  A "*8)
        ####
        nbt = "tftpboot 0x2000000 chewbacca/uImage \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  B "*8)
        ####
        nbt = "tftpboot 0x3000000 chewbacca/ramdisk_v1.0.img \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  C "*8)
        ####
        nbt = "tftpboot 0xc00000 chewbacca/silkworm.dtb \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  C "*8)
        ####
        nbt = "bootm 0x2000000 0x3000000 0xc00000 \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash_only)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  E "*8)
    
    
    if switch_type == '173':  ####  TYR
        nbt = "makesinrec 0x1000000 \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  A "*8)
        ####
        nbt = "tftpboot 0x2000000 tyr/uImage \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  B "*8)
        ####
        nbt = "tftpboot 0x3000000 tyr/ramdisk_v1.0.img \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  C "*8)
        ####
        nbt = "tftpboot 0xc00000 tyr/silkworm_bd173.dtb \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  C "*8)
        ####
        nbt = "bootm 0x2000000 0x3000000 0xc00000 \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash_only)
        print("send the date   and look for =>")
        print("\n\n")
        print(capture)
        print("Kernel  E "*8)
    
    
    if switch_type == '133':  ####  ODIN
        nbt = "tftpboot 0x1000000 net_install26_odin.img\n"
        tn.write(nbt.encode('ascii'))
        #capture = tn.expect(reg_list, 30)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x1000000\n")
        #capture = tn.expect(reg_bash_only, 30)
        capture = tn.expect(reg_bash_only)
        
    if (switch_type == '66' or switch_type == '71' or switch_type == '118' or switch_type == '109'):
        #### 5100  Stinger   tomahawk  tom_too
        nbt = "tftpboot 0x1000000 net_install_v7.2.img\n"
        tn.write(nbt.encode('ascii'))
        #capture = tn.expect(reg_list, 30)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x1000000\n")
        #capture = tn.expect(reg_bash_only, 30)
        capture = tn.expect(reg_bash_only)
        
    if (switch_type == '120' or switch_type == '121' or switch_type == '64' or switch_type == '83' or switch_type == '62' or switch_type == '77'):
        ####  DCX zentron  pluto zentron  thor  7800
        nbt = "tftpboot 0x1000000 net_install26_8548.img\n"
        tn.write(nbt.encode('ascii'))
        #capture = tn.expect(reg_list, 30)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x1000000\n")
        #capture = tn.expect(reg_bash_only, 30)
        capture = tn.expect(reg_bash)
        
        
    if switch_type == '148':  #### SKYBOLT
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_list,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x2000000 skybolt/uImage \n")
        #capture = tn.expect(reg_list,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x3000000 skybolt/ramdisk.skybolt \n")
        #capture = tn.expect(reg_list,30
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x4000000 skybolt/silkworm.dtb \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000 \n")
        #caputure = tn.expect(reg_bash_only,30)
        capture = tn.expect(reg_bash_only)
        
    if (switch_type == '141' or switch_type == '142'):  #### YODA 
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x2000000 yoda/uImage\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x3000000 yoda/ramdisk.yoda\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x4000000 yoda/silkworm_yoda.dtb\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\n")
        #caputure = tn.expect(reg_bash_only,30)
        capture = tn.expect(reg_bash)
        
        
        
    if (switch_type == '162'):  #### WEDGE
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x2000000 wedge/uImage.netinstall\n")
        #capture = tn.expect(reg_bash,10)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x3000000 wedge/ramdisk_v1.0.img\n")
        #capture = tn.expect(reg_bash,20)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x4000000 wedge/silkworm.dtb.netinstall\n")
        #capture = tn.expect(reg_bash,10)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\n")
        #caputure = tn.expect(reg_bash,60)
        capture = tn.expect(reg_bash)
        
    if (switch_type == '166' or switch_type == '165'):  #### Allegiance
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x2000000 rayg/uImage_165_9_24_1900\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0x3000000 lando/ramdisk_v1.0.img\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"tftpboot 0xc00000 rayg/silkworm_bd165.dtb\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_list)
        tn.write(b"bootm 0x2000000 0x3000000 0xc00000\n")
        #caputure = tn.expect(reg_bash,60)
        capture = tn.expect(reg_bash)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####
####  this section is common for all switches after the kernel is loaded
####
####
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
    tn.write(b"export PATH=/usr/sbin:/sbin:$PATH\n")
    #capture = tn.expect(reg_bash, 30)
    capture = tn.expect(reg_bash)
    print("send export PATH  and look for bash")
    print("\n\n")
    print(capture)
    print("Kernel  F "*8)
    i = "ifconfig eth0 %s netmask 255.255.240.0 up\n" % sw_ip 
    tn.write(i.encode('ascii'))
    #capture = tn.expect(reg_bash, 30)
    capture = tn.expect(reg_bash)
    print("send the ifconfig    and look for bash")
    print("\n\n")
    print(capture)
    print("Kernel  G "*8)
    gw = "route add default gw %s \n" % gateway_ip
    tn.write(gw.encode('ascii'))
    #capture = tn.expect(reg_linkup,30)
    capture = tn.expect(reg_bash)
    print("send the route add default  and look for bash")
    print("\n\n")
    print(capture)
    print("Kernel  H "*8)
    #tn.write(b"\n")
    #capture = tn.expect(reg_bash, 20)
    #capture = tn.expect(reg_bash)
    #print("send the date   and look for =>")
    #print("\n\n")
    #print(capture)
    #print("Kernel  I "*8)
    m = "mount -o tcp,nolock,rsize=32768,wsize=32768 10.38.2.20:/export/sre /load\n" ####CHANGE SERVER TO VARIABLE
    tn.write(m.encode('ascii'))
    #capture = tn.expect(reg_bash, 30)
    capture = tn.expect(reg_bash)
    print("send mount command   and look for bash")
    print("\n\n")
    print(capture)
    print("Kernel  J "*8)
    ### firmwarepath
    firmpath = "cd /load/SQA/fos/%s/%s\n" % (frm_no_bld, frm_version)
    tn.write(firmpath.encode('ascii'))
    #capture = tn.expect(reg_bash,160)
    capture = tn.expect(reg_bash)
    print("send the firmware path   and look for bash")
    print("\n\n")
    print(capture)
    print("Kernel  K "*8)
    print("\nRelax for a few minutes, this step takes a while  ")
    #### need to capture when this hangs anc was not able to connect to the server
    ####  this appears to timeout and the last recieve string was
    ####    \xco\xc0\x80  80 repeated 10 times
    tn.write(b"./install release\n")
    #capture = tn.expect(reg_bash,160)
    capture = tn.expect(reg_bash)
    ####  this does not capture the bash  and from the console the last recv b'30`\x00\x180\xf0
    print("send  install release   and look for bash")
    print("\n\n")
    print(capture)
    print("Kernel  L "*8)
    
    return(True)

def do_net_install(sw_info_filename):
    """
    
    """
    global tn
    pa = parse_args(sys.argv)
    pa.filename = sw_info_filename
    print(pa.filename)
    if pa.verbose >=3:
        start_of_func_print("do_net_install")
        
    if pa.ipaddr:
        print("do IP steps")
        pa.chassis_name = console_info_from_ip(pa.ipaddr)
    
    cons_info         = console_info(pa.chassis_name)
    console_ip        = cons_info[0]
    console_port      = cons_info[1]
    console_ip_bkup   = cons_info[2]
    console_port_bkup = cons_info[3]
    power_pole_info   = pwr_pole_info(pa.chassis_name)    
    usr_pass          = get_user_and_pass(pa.chassis_name)
    user_name         = usr_pass[0]
    usr_psswd         = usr_pass[1]
    ipaddr_switch     = get_ip_from_file(pa.chassis_name)
    print("IPADDR")
    print(ipaddr_switch)
    print("@"*80)
    ras = re.compile('.\d{1,3}.\d{1,3}.(\d{1,3}).\d{1,3}')
    gw_octet = ras.findall(ipaddr_switch)
    gw_octet = int(gw_octet[0])
    if gw_octet >= 129:
        gateway_ip = "10.38.128.1"
    else:
        gateway_ip = "10.38.32.1"
    print("@"*80)
    print(gateway_ip)
    print("\nuser name and password  \n\n")
    print(user_name)
    print(usr_psswd)
    print(usr_pass)
    print(pa.filename)
    
    if not pa.cmdprompt:
        try:
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
        except OSError:
            info_help_OSError()
            #### this will exit here
        
        sw_dict = cofra.get_info_from_the_switch(pa.filename, 128)
        
        anturlar.close_tel()
     
        my_ip                = sw_dict["switch_ip"]
        my_cp_ip_list        = sw_dict["cp_ip_list"]
        sw_name              = sw_dict["switch_name"]
        sw_chass_name        = sw_dict["chassis_name"]
        sw_director_or_pizza = sw_dict["director"]
        sw_domains           = sw_dict["domain_list"]
        sw_ls_list           = sw_dict["ls_list"]
        sw_base_fid          = sw_dict["base_sw"]
        sw_xisl              = sw_dict["xisl_state"]
        sw_type              = sw_dict["switch_type"]
        sw_license           = sw_dict["license_list"]
        sw_vf_setting        = sw_dict["vf_setting"]
        sw_fcr_enabled       = sw_dict["fcr_enabled"]
        sw_port_list         = sw_dict["port_list"]
        sw_ex_port_list      = sw_dict["ex_ports"]
    
    else:
        sw_director_or_pizza = False
        sw_type = pa.switchtype
        my_ip = ipaddr_switch
        print("SETTING THE DIRECTOR OR PIZZA BOX VARIABLE")

 
###################################################################################################################
###################################################################################################################
####
####  if I am Director then connect to console 1 and find the cmdprompt
####     then connect to console 2 and find the cmdprompt
####
####     switch IP now needs to be the CP0 and CP1 values
####
    tn_list = []
    print("\n\nCONNECT TO THE CONSOLE NOW\n\n")
    #if sw_director_or_pizza:
    tn_cp0 = connect_console(console_ip, user_name, usr_pass, console_port, 0)
    tn_list.append(tn_cp0)
    
    if sw_director_or_pizza:
        tn_cp1 = connect_console(console_ip_bkup, user_name,usr_pass,console_port_bkup,0)
        tn_list.append(tn_cp1)
    
    print("\n\nOUT OF CONNECTION TO CONSOLE\n\n")
#######################################################################################################################
####
####  reboot and find the command prompt 
####
    cnt = 1
    if not pa.cmdprompt:
        for tn in tn_list:
            cons_out = stop_at_cmd_prompt(0)
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("FIND THE COMMAND PROMPT  1  \n")
            print(cons_out)
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("NOW SET THE ENV VARIABLES  ")
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    
    for tn in tn_list:
        cons_out = env_variables(sw_type,gateway_ip, 0)
        print("\n"*4)
        print("P"*80)
        print("\n"*2)
        print("Q"*80) 
        print(cons_out)
        if sw_director_or_pizza:
            load_kernel(sw_type, my_cp_ip_list[cnt], gateway_ip, pa.firmware)
            cnt += 1
        else:
            load_kernel(sw_type, my_ip, gateway_ip, pa.firmware)
 
    
#######################################################################################################################
#######################################################################################################################
#### this step is the same for director or pizza box
####
####  turn each port off then turn each port on (otherwise the delay between did not power cycle the switch)
####
#######################################################################################################################
    reg_list_bash = [b"bash-2.04#"]
    print("H"*80)
    print("looking for bash forever")
 
    print("\n"*4)
    print("&"*80)
    print("\n"*4)
    print("&"*80) 
 
#try:
    
    for pp in range(0, len(power_pole_info), 2):
        print('POWERPOLE')
        if power_pole_info[pp] == "10.39.36.112":
            port = (power_pole_info[pp+1])
            print(port)
            raritan(port, "off")
        else:
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off",10)
            time.sleep(4)
        
    for pp in range(0, len(power_pole_info), 2):
        print('POWERPOLE')
        if power_pole_info[pp] == "10.39.36.112":
            port = (power_pole_info[pp+1])
            raritan(port, "on")
        else:
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "on",10)
            time.sleep(4)
#except:

    if  '' == power_pole_info[0]:
        print("\n"*20)
        print("NO POWER POLE INFO FOUND ")
        print("HA "*10)
        print("you have to walk to power cycle the switch")
        print("I will wait ")
        liabhar.JustSleep(30)
    else:
        print("POWER TOWER INFO")
        print(power_pole_info[0])
        print(power_pole_info)
        liabhar.JustSleep(30)
            
#######################################################################################################################
#######################################################################################################################
####
####
#######################################################################################################################
#######################################################################################################################
####
####
#######################################################################################################################

    print("\n"*6)
    print("@"*40)
    print("Close Console sessions and login via telnet")
    print("Sleep for a minute at line 1230")
    print("\n"*6)     

    reg_list_after_reboot = [b"is in sync", b"initialization completed."]
    cons_out = tn.expect(reg_list_after_reboot,900)
    print("\n"*4)
    print("&"*80)
    print(cons_out)
    print("\n"*4)
    print("&"*80)
 
    liabhar.count_down(60)
    
    for tn in tn_list:
        tn.close()
 
    tn_list = []
    print("\n\nCONNECT TO THE CONSOLE NOW\n\n")
 
    tn_cp0 = connect_console_enable_root(console_ip, user_name, usr_pass, console_port, 0)
    tn_list.append(tn_cp0)
    
    if sw_director_or_pizza:
        tn_cp1 = connect_console_enable_root(console_ip_bkup, user_name,usr_pass,console_port_bkup,0)
        tn_list.append(tn_cp1)
    
    for tn in tn_list:
        tn.close()
 
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
    """
    send a command to the console when connected
    
    """
    
    
    global tn
    
    tn.set_debuglevel(db)
    
    capture = ""
    cmd_look = cmd.encode()
    
    #reg_ex_list = [b".*:root> "]
    reg_ex_list = [b"root> ", b"admin> "]
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    capture = tn.expect(reg_ex_list,3600)
    #print(capture[0])
    #print(capture[1])
    #print(capture[2])
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    
    return(capture)

def console_info_from_ip(ipaddr):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    for line in csv_file:
        ip_address_from_file = (line['IP Address'])
        
        if ip_address_from_file == ipaddr:
            swtch_name = (line['Chassisname'])
         
        else:
            print("\n\nIPaddress was not found    please check the numbers and try again\n\n")
            print("@"*80)
            #sys.exit()
            
    return(swtch_name)
       
def console_info(chassis_name):
    """
    
    """
    
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        
        if chassis_name_from_file == chassis_name:
            
            cons_1_ip   = (line['Console1 IP'])
            cons_1_port = (line['Console1 Port']) 
            cons_2_ip   = (line['Console2 IP'])
            cons_2_port = (line['Console2 Port']) 
        
            a = []
            a = [cons_1_ip, cons_1_port]
            
            if cons_2_ip:

                a += [cons_2_ip]
                a += [cons_2_port]
            else:
                a += ["0"]
                a += ["0"]
        else:
            print("\n\n\nChassis Name unknown   please check the spelling and try again \n\n")
            print("@"*80)
            
            #sys.exit()
            
    return(a)

def pwr_pole_info(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    #print("@"*80)
    #print("@"*80)
    #print("@"*80)
    
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        
        #if chassis_name_from_file == chassis_name[0]:
        if chassis_name_from_file == chassis_name:
            #sn = (switch_name)
            
            pwer1_ip = (line['Power1 IP'])
            pwer2_ip = (line['Power2 IP'])
            pwer3_ip = (line['Power3 IP'])
            pwer4_ip = (line['Power4 IP'])
            
            pwer1_prt = (line['Power1 Port'])
            pwer2_prt = (line['Power2 Port'])
            pwer3_prt = (line['Power3 Port'])
            pwer4_prt = (line['Power4 Port'])
            
            p = []
            p =[pwer1_ip, pwer1_prt]
            if pwer2_ip:
                p += [pwer2_ip]
                p += [pwer2_prt]
            if pwer3_ip:
                p += [pwer3_ip]
                p += [pwer3_prt]
            if pwer4_ip:
                p += [pwer4_ip]
                p += [pwer4_prt]
            

    
    return(p)

def get_user_and_pass(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
     
    u_and_p = []
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            u = (line['Username'])
            p = (line['Password'])
            u_and_p += [u]
            u_and_p += [p]
            
    return(u_and_p)
 
def get_ip_from_file(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
     
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            ip = (line['IP Address'])
                        
    return(ip)

   
def user_start():
    go = False
    go = True
    start = 'n'
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/no] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                #sys.exit()
                
        if start == 'y' :
            go = True
        else:
            print("START VALUE is  %s" % start)
            if start == 'no':
                sys.exit()
            else:
                start = 'n'           
    return()

def load_config(ipaddr_switch, user_name,usr_psswd, filename):
    """
       read from config files and configure the switch
    
    """
    pa = parse_args(sys.argv)
    if pa.verbose >=3:
        start_of_func_print("  load_config   ")
        
    try:
        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"password")
        
        if tn == "":
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    
    except:
        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    

    #cons_out = sw_set_pwd_timeout(usr_psswd, tn)
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    #print("tn is   %s  " % tn )
    ##tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    #
    
    user_start()
    
    print("\n\nLICENSE ADD TO SWITCH \n\n")
    print(ipaddr_switch)
    
    ###################################################################################################################
    ####  
    ####  ask the user which file to use
    ####   prepopulate with the file from above
    ####    check the existience of the file
    ####    correct it or exit
    ####
    ###################################################################################################################
    print("USE USER INPUTED FILE NAME OR DEFAULT")
    
    #cc = cofra.SwitchUpdate("for_playback")
    cc = cofra.SwitchUpdate(filename)
                                                                ####   format of each playback feature             ####
    cons_out = cc.playback_licenses()                           ####   list of strings                             ####
    tn_maybe = cc.playback_ls()                                 ####   list of strings                             ####
    #print("\r\ngetting another tn\r\n")
    #print(tn)
    #print(tn_maybe)
    #sys.exit()
    cons_out = cc.playback_switch_names()                 ####   list     --  fid: switchname                      ####
    #cons_out = cc.playback_switch_domains()               ####   list     --  fid: domain                          ####
    cons_out = cc.playback_switchget_info_from_the_switch_domains()               ####   list     --  fid: domain                          ####
    cons_out = cc.playback_add_ports()                    ####   list    --   fid: list of ports                   ####
    cons_out = cc.playback_add_ports_ex()
    tn       = cc.reboot_reconnect()
    cons_out = anturlar.fos_cmd("switchshow")
    print(cons_out)
    cons_out = anturlar.fos_cmd("timeout 0")
    print(cons_out)
     
    anturlar.close_tel()
    #tn.write(b"exit\n")
    #tn.close()
    
    
    return(True)

def cant_find_file_message(complete_name,filename):
    """
    
    """
    print("\ncomplete file path")
    print(complete_name)
    print("\nparser  filename ")
    print(filename)
    print("\n\nNO FILE FOUND")
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("\n\nformat for filename is stinger for the info file\n\n   Switch_Info_10.20.30.40_stinger_for_playback.txt")
    print("                           ^^^^^^^\n")
    print("This part may be a time stamp of when the file was created unless you changed it...\nsince I know the rest of the info I only need the unique part :) \n\n")
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)
 
    sys.exit()
    
def enter_file_ext():
    go = False
    start = 'n'
    ###################################################################################################################
    ####
    ####  enter a file extension for the replay file instead of the default
    ####  otherwise use the defualt
    ####  stop if the user pushes esc 
    ####
    ###################################################################################################################

#######################################################################################################################
####
####  standard way to handle user input
####    - while loop looking for a valid 'go' variable
####       - while loop waiting for a string input
####       - if start variable is y set go to true and exit the procedure
####
#######################################################################################################################
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/no] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                #sys.exit()        
        if start == 'y' :
            go = True
        else:
            print("START VALUE is  %s" % start)
            if start == 'no':
                sys.exit()
            else:
                start = 'n'

def pb_action( pb, ipaddr_switch, user_name, usr_psswd, console_ip, usr_pass, console_port, console_port_bkup, console_ip_bkup ):
    """
        this will start the net install and playback steps depending on the input by the user
        of how the info file is created or which file to use
    
    """
    
    pa = parse_args(sys.argv)                              ####   set the command line arguments to a variable     ####
    db = 0



#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 0   --   create the user file and exit                                         ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################
    
    if pa.verbose >=3:
        start_of_func_print("   In MAIN   Check for file_action == 0  \n  if so then create the INFO File only \n\
                            then exit   pb = %s " % pb  )
    
    if pb == 0:
        print("CREATE USER FILE ONLY")
        #### for this section create the file name with Switch_Info + ipaddress + date_stamp + .txt
        ####   user can change the file name afterwords to shorten or make unique to remember
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.cust_date + pa.filename
    
        try:
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
        except OSError:
            info_help_OSError()
            #### this will exit here
        sw_dict = cofra.get_info_from_the_switch(pa.filename, 128)
        anturlar.close_tel()
        
        sys.exit()



#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 1   -- create the user file  and start Net Install                             ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################

    if pa.verbose >=3:
        start_of_func_print("   In MAIN   Check for file_action == 1 ")
    
    if pa.file_action == 1:
        print("NET INSTALL AND REPLAY ")
        ####   capture data from the switch
        ####   net install the switch
        ####   play back the configuration
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.cust_date + pa.filename
        sw_info_filename = pa.filename
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))
        do_net_install(sw_info_filename)
    
        if not os.path.isfile(complete_name):  #### this should be checked in parser
            cant_find_file_message(complete_name,pa.filename)
        
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,10)
        
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,10)
        
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
    
        return(True)


   

#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 2   --   create the user file and exit                                         ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################

    if pa.verbose >=3:
        start_of_func_print("   In MAIN   Check for file_action == 2  \n   if so then use a Previous captured \n\
                            INFO file to configure the switch after netinstall  \n   then exit   pb = %s  " % pb)
        
    if pb == 2:
        print("USER FILE and NETINSTALL")
        print("\n"*40)
        ####what is file name
        
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.filename + "_for_playback"
        pa.filename = pa.cust_date + pa.filename
        sw_info_filename = pa.filename
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))
        do_net_install(sw_info_filename)
        
        
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))  #### substitute this way
        pa.filename   = "%s"%(pa.filename)                                                  ####  or file might not be
        #### see note at the end of this line                                               ####   found
        if not os.path.isfile(complete_name):  #### this should be checked in parser
            cant_find_file_message(complete_name,pa.filename)
            
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,10)
           
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,10)
         
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
        
        return(True)
        

#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 3   -- restor with the user file and exit                                      ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################
    if pa.verbose >=3:
        start_of_func_print("   In MAIN   Check for file_action == 3   \n  if so then only restore from the file \n\
                            then exit  pb = %s " % pb)
        db = 10
        
    if pb == 3:
        print("USER FILE and NO NETINSTALL")
        ####   what is file name
        pa.filename = pa.filename + "_for_playback"
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))  #### substitute this way ##
        pa.filename   = "%s"%(pa.filename)                                                  ####  or file might not####
        #### see note at the end of this line                                               ####   be found        ####
        if not os.path.isfile(complete_name):                       #### this should be checked in parser          ####
            cant_find_file_message(complete_name,pa.filename)
        
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,db)
        
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,db)
        
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
        
        sys.exit()
    

 
    return(True)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################   

def main():

    global tn
#######################################################################################################################
####
####     display the parse arguments captured on the command line
####
#######################################################################################################################
    pa = parse_args(sys.argv)
    #print(pa)
    print(pa.chassis_name)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    print(pa.firmware)
    print(pa.cmdprompt)
    print(pa.file_action)
    print(pa.filename)
    print(pa.cust_date)
    print("@"*40)
    
#######################################################################################################################
####   TO DO
#######################################################################################################################
####
####  if pa.file_action
####        0  -  create the file ONLY             -- if option 0 or 1 then add the date to the filename
####        1  -  Default file and NET INSTALL     -- if option 0 or 1 then add the date to the filename
####        2  -  USER file and NET INSTALL        -- if option 2 we only need the extention from the end of
####                                                      the switch_ip_ to the _ before _playback ????   because the
####                                                      user could change the file or use a previous one and
####                                                      the cust_date would not match
####        3  -  USER FILE and NO net install     -- CONFIGURATION CHANGES ONLY                   < working 11/20/15 >
####
####  if pa.cmdprompt
####       Ignore pa.file_action ( shold be blocked in parser)
####  
####  
####  if pa.filename       is supplied then check for the files existence
####  if pa.type           is supplied then check for the correct type
####  if pa.chassis_name   then get the IP from the SwitchMatrix file
####   
####
    
#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
#### if user enter ip address then get the chassisname from the                                                    ####
####   SwitchMatrix file                                                                                           ####
#### then get the info from the SwitchMatrix file using the Chassis Name                                           ####
####                                                                                                               ####
####  then parse the arguments into variable names that are easier to identify                                     ####
####                                                                                                               ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################
    if pa.ipaddr:
        print("do IP steps")
        pa.chassis_name = console_info_from_ip(pa.ipaddr)
        
    cons_info         = console_info(pa.chassis_name)
    console_ip        = cons_info[0]
    console_port      = cons_info[1]
    console_ip_bkup   = cons_info[2]
    console_port_bkup = cons_info[3]
    power_pole_info   = pwr_pole_info(pa.chassis_name)    
    usr_pass          = get_user_and_pass(pa.chassis_name)
    user_name         = usr_pass[0]
    usr_psswd         = usr_pass[1]
    ipaddr_switch     = get_ip_from_file(pa.chassis_name)
 
    ras = re.compile('.\d{1,3}.\d{1,3}.(\d{1,3}).\d{1,3}')
    gw_octet = ras.findall(ipaddr_switch)
    gw_octet = int(gw_octet[0])
    if gw_octet >= 129:
        gateway_ip = "10.38.128.1"
    else:
        gateway_ip = "10.38.32.1"

#######################################################################################################################
 
#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the switch is at the command prompt                                                                      ####
####      start the net install from the command prompt                                                            ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################
    if pa.verbose >=3:
        start_of_func_print("   In MAIN   Check for cmdprompt then do_net_install ")

    if pa.cmdprompt:
        do_net_install(pa.filename)
    #### in the netinstall proc you need to check for the bash prompt
        print("EXIT since we started at the command prompt")
        print("if you want to configure the switch from the INFO file")
        print("run this again with option -fa 3 ")
        print("\n"*5)
        sys.exit()
    else:
        if pa.verbose >=3:
            start_of_func_print("   Did NOT find the command prompt switch from the arguments  ")



#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 0     -- Create the switch info file only                                      ####
    if pa.file_action == 0:
        pb_action(0, ipaddr_switch,user_name,usr_psswd, console_ip, usr_pass, console_port, console_port_bkup, console_ip_bkup)
        sys.exit() 
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 3   --  use a previously created user file to restore and exit                 ####
    if pa.file_action == 3:
        pb_action(3, ipaddr_switch,user_name,usr_psswd, console_ip, usr_pass,console_port, console_port_bkup, console_ip_bkup)
        sys.exit()
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################
 
#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 1     -- Create the switch info file only                                      ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################

    if pa.verbose >=3:
        start_of_func_print("   In MAIN   Check for file_action == 1 ")
    
    if pa.file_action == 1:
        print("NET INSTALL AND REPLAY ")
        ####   capture data from the switch
        ####   net install the switch
        ####   play back the configuration
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.cust_date + pa.filename
        sw_info_filename = pa.filename
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))
        do_net_install(sw_info_filename)
    
        if not os.path.isfile(complete_name):  #### this should be checked in parser
            cant_find_file_message(complete_name,pa.filename)
        
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,10)
        
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,10)
        
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
    
        sys.exit()    


    
#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
####   if the file action is set to 2     -- Create the switch info file only                                      ####
    if pa.file_action == 2:
        pb_action(2, ipaddr_switch,user_name,usr_psswd, console_ip, usr_pass, console_port, console_port_bkup, console_ip_bkup)
        sys.exit() 
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################
   

    print("#"*6000)
    sys.exit()


    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

