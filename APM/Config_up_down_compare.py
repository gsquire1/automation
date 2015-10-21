#!/usr/bin/env python3


###############################################################################
####
####  net install a switch of any 
####
###############################################################################

import os,sys

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')

import telnetlib
import getpass
 
import argparse
import re
import anturlar
import liabhar
import cofra
import csv
import time

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
###############################################################################


def user_start():
    go = False
    start = 'n'
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                print("This test can run 3 steps  ")
                print("   1. capture the switch info and write to file")
                print("   2. configdownload, capture the switch info and perform diff on orig file")
                print("   3. do all steps ")
                print("   4. exit")
                
                start = int(input("\n\n\n\nEnter your choice 1-4   "))
                
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input\n\n")
                sys.exit()
                
        if start > 0 and start <=3:
            go = True
            return(start)
        else:
            sys.exit()


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    #pp.add_argument("--repeat", help="repeat repeat")
    #pp.add_argument("firmware", help="firmware verison 8.1.0_bldxx")
    #pp.add_argument("ip", help="IP address of SUT")
    #pp.add_argument("user", help="username for SUT")
    pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp 

def parse_args(args):
    
    verb_value = "99"
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    #parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    #parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    parser.add_argument('-cp',  '--cmdprompt', help="switch is already at command prompt")
    parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
    parser.add_argument('-r',   '--steps', type=int, help="Steps that will be executed")
    #parser.add_argument('-p', '--password', help="password")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    #group.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")
    
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
    #print("Connecting to IP :  " + args.ip)
    #print("user             :  " + args.user)
    #verbose    = args.verbose
     
     

    return parser.parse_args()

def connect_console(HOST,usrname,password,port,db=0, *args):
    
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
    tn.set_debuglevel(db)
    
    
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
        
    print("\n\n\n\n\n\n\n\n")
    
    #############################################################################
    #### login to the switch
    reg_list = [ b"Enter your option", b"login: ", b"assword: ", b"root> ", b"users: ", b"=>" ]  
    while var <= 4:
        #print("start of the loop var is equal to ")
        capture = ""
        capture = tn.expect(reg_list)
        print(capture)
        
        if capture[0] == 0:
            tn.write(b"1")
                    
        if capture[0] == 1:
            tn.write(b"root\r\n")
                
        if capture[0] == 2:
            tn.write(b"assword\r\n")
                    
        if capture[0] == 3:
            print(capture)
            print("this found root")
            break
        
        if capture[0] == 4:
            print(capture)
            print("\n\n\n\n\n\nFOUND USERS: \n\n")
            tn.write(b"\r\n")
            #capture = tn.expect(reg_list)
            #break
        if capture[0] == 5:
            print(capture)
            var += 4
            break
        
        var += 1
      
    capture = tn.expect(reg_list, 20)
    if capture[0] == 1 :
        tn.write(b"root\r\n")
        capture = tn.expect(reg_list, 20)
        tn.write(b"password\r\n")
        capture = tn.expect(reg_list, 20)
        

    capture = tn.expect(reg_list, 20)
    
    return(tn)

def stop_at_cmd_prompt(db=0):
    global tn
    
    tn.set_debuglevel(db)
    print("\n\n\n\n\n\n\n\nlooking for stop autoboot\n\n")
    
    #cons_out = send_cmd("/sbin/reboot")
    #
    #
    reg_list = [ b"Hit ESC to stop autoboot: "]
    
    tn.write(b"/sbin/reboot\r\n")
    capture = tn.expect(reg_list, 3600)
    
    #tn.write( b"char(27)")  #### char(27) or \x1b are both ESC 
    tn.write(b"\x1b")
    reg_list = [b"Option"]
    
    capture = tn.expect(reg_list)
    tn.write(b"3\r\n")
    
    reg_list = [ b"=>"]
    capture = tn.expect(reg_list, 300)
    
    return()
       
def env_variables(swtype, db=0):
    
    liabhar.JustSleep(60)
    
    tn.set_debuglevel(db)
    tn.write(b"printenv\r\n")
    reg_list = [b"=>"]
    capture = tn.expect(reg_list, 300)
    
    gateway   = "10.38.32.1"
    netmask   = "255.255.240.0"
    bootargs  = "ip=off"
    ethrotate = "no"
    server_ip = "10.38.2.40"
    ethact    = "ENET0"
    
    if swtype == 148:
        print("SKYBOLT")
        ethact = "FM1@DTSEC2"
    #if (swtype == 141 or swtype == 142):
    #    print("YODA")
    #    ethact = "FM2@DTSEC4"
        
    a = ("setenv ethact %s \r\n" % ethact)
    tn.write(a.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    
    g = ("setenv gateway %s \r\n" % gateway)
    tn.write(g.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    n = ("setenv netmask %s\r\n"%netmask)
    tn.write(n.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    b = ("setenv bootargs %s\r\n"%bootargs)
    tn.write(b.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    e = ("setenv ethrotate %s\r\n"%ethrotate)
    tn.write(e.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    s = ("setenv serverip %s\r\n"%server_ip)
    tn.write(s.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    
    tn.write(b"saveenv\r\n")
    capture = tn.expect(reg_list, 300)
    tn.write(b"printenv\r\n")    
    capture = tn.expect(reg_list, 300)
    
    liabhar.JustSleep(60)
    
    p = ("ping %s  \r\n" % gateway)
    tn.write(p.encode('ascii'))
    tn.write(b"\r\n")
    capture = tn.expect(reg_list, 300)
    
    return(capture)

def pwr_cycle(pwr_ip, pp, stage, db=0):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    anturlar.power_cmd("cd access/1\t/1\t%s" % pp ,10)
    anturlar.power_cmd("show\r\n" ,10)
    
    anturlar.power_cmd(stage, 5)
    anturlar.power_cmd("yes", 5)
    
    #liabhar.JustSleep(10)
    anturlar.power_cmd("exit", 10)
     
    print("\r\n"*10)
    print("Waiting for the switch to boot")
    print("\r\n"*5)
    
    return(0) 
    
def load_kernel(switch_type, sw_ip, frm_version):
    
    reg_list = [ b"=>"]
    reg_bash = [ b"bash-2.04", b"=>"]
    reg_linkup = [ b"link is up"]
    
    #### set tftp command
    
    ras = re.compile('([\.a-z0-9]+)(?:_)?')
    ras = ras.search(frm_version)
    frm_no_bld = ras.group(1)
    if 'amp' in frm_version:
        frm_no_bld = frm_no_bld + '_amp'
    
    
    if switch_type == '133':  ####  ODIN
        nbt = "tftpboot 0x1000000 net_install26_odin.img\r\n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list, 300)
        tn.write(b"bootm 0x1000000\r\n")
        capture = tn.expect(reg_bash, 300)
        
    if (switch_type == '66' or switch_type == '71' or switch_type == '118' or switch_type == '109'):
        #### 5100  Stinger   tomahawk  tom_too
        nbt = "tftpboot 0x1000000 net_install_v7.2.img\r\n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list, 300)
        tn.write(b"bootm 0x1000000\r\n")
        capture = tn.expect(reg_bash, 300)
        
    if (switch_type == '120' or switch_type == '121' or switch_type == '64' or switch_type == '83'):
        ####  DCX zentron  pluto zentron  thor  7800
        nbt = "tftpboot 0x1000000 net_install26_8548.img\r\n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list, 300)
        tn.write(b"bootm 0x1000000\r\n")
        capture = tn.expect(reg_bash, 300)
        
        
    if switch_type == '148':  #### SKYBOLT
        tn.write(b"makesinrec 0x1000000 \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x2000000  skybolt/uImage\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x3000000 skybolt/ramdisk.skybolt\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x4000000 skybolt/silkworm.dtb\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\r\n")
        caputure = tn.expect(reg_bash,300)
        
    if (switch_type == '141' or switch_type == '142'):  #### YODA 
        tn.write(b"makesinrec 0x1000000 \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x2000000 yoda/uImage\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x3000000 yoda/ramdisk.yoda\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x4000000 yoda/silkworm_yoda.dtb\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\r\n")
        caputure = tn.expect(reg_bash,300)
        
        
    tn.write(b"export PATH=/usr/sbin:/sbin:$PATH\r\n")
    capture = tn.expect(reg_bash, 300)
    i = "ifconfig eth0 %s netmask 255.255.240.0\r\n" % sw_ip 
    tn.write(i.encode('ascii'))
    capture = tn.expect(reg_bash, 300)
    tn.write(b"route add default gw 10.38.32.1\r\n")
    capture = tn.expect(reg_linkup,10)
    #tn.write(b"\r\n")
    capture = tn.expect(reg_bash, 10)
    m = "mount -o tcp,nolock,rsize=32768,wsize=32768 10.38.2.20:/export/sre /load\r\n"
    tn.write(m.encode('ascii'))
    capture = tn.expect(reg_bash, 30)
    ### firmwarepath
    firmpath = "cd /load/SQA/fos/%s/%s\r\n" % (frm_no_bld, frm_version)
    tn.write(firmpath.encode('ascii'))
    capture = tn.expect(reg_bash,600)
    #### need to capture when this hangs anc was not able to connect to the server  
    tn.write(b"./install release\r\n")
    capture = tn.expect(reg_bash,600)

    return(0)

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
    cmd_look = cmd.encode()
    
    #reg_ex_list = [b".*:root> "]
    reg_ex_list = [b"root> "]
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\r\n")
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
            print("\r\n")
            
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
            print("\r\n")
            
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

def power_cycle(power_pole_info):
    
    try:
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off")
            time.sleep(2)
            
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "on")
            time.sleep(2)
    except:
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

def sw_set_pwd_timeout(pswrd,tn):
   
    reg_list = [ b"Enter your option", b"login: ", b"Password: ", b"root> ", b"users: " ]
    reg_login = [ b"login:"]
    reg_assword = [ b"assword: ", b"root> "]
    reg_change_pass = [ b"key to proceed", b"incorrect" ]
    reg_complete   = [ b"zation completed"]
    reg_linertn    = [ b"\\r\\n" ]
    
    print("\n\nlooking for completed task\n\n")
    capture = tn.expect(reg_complete, 10)
    tn.write(b"\r\n")
    print("\n\nwrite to tn a newline \n\n")
    print("\n\nlooking for login and send root\n\n")
        #capture = tn.expect(reg_linertn)
    capture = tn.expect(reg_login, 60)
    
    tn.write(b"root\r\n")
    capture = tn.expect(reg_assword, 20)
    print("\n\nlooking for password and send fibranne\n\n")
    tn.write(b"fibranne\r\n")
    capture = tn.expect(reg_change_pass, 20)
    tn.write(b"\r\n")
    capture = tn.expect(reg_linertn)

    
    while True:    
        capture = tn.expect(reg_assword, 20)  #### looking for Enter new password
        #### if root is found break out
        print("CAPTURE is  ")
        print(capture)
        
        if capture[0] == 1:
            print(capture)
            print("this found root")
            break
        tn.write(b"password\r\n")
  
    capture = tn.expect(reg_list, 20)
    tn.write(b"root\r\n")
    capture = tn.expect(reg_list, 20)
    tn.write(b"password\r\n")
    capture = tn.expect(reg_list, 20)
    tn.write(b"timeout 0 \r\n")
    capture = tn.expect(reg_list, 20)
    
    return(True)
    


 
 
 
   
def replay_from_file(switch_ip, lic=False, ls=False, base=False, sn=False, vf=False, fcr=False ):
    """
        open the log file for reading and add the following
        1. license
        2. create fids and base switch is previously set
        3. put ports into the FIDS
        4. update domains
        5. update switch name
        6. enable fcr
        7.
    """
    
    ff = ""
    f = ("%s%s%s"%("logs/Switch_Info_for_playback_",switch_ip,".txt"))
    print(f)
    
    try:
        with open(f, 'r') as file:
            ff = file.read()
    except IOError:
        print("\n\nThere was a problem opening the file" , f)
        sys.exit()
        
    print("look for the info\r\n")
    print(ff)
    ras_license     = re.findall('LICENSE LIST\s+:\s+\[(.+)\]', ff)
    
    print(ras_license)
    ras_ls_list     = re.findall('LS LIST\s+:\s+\[(.+)\]', ff)
    ras_base        = re.findall('BASE SWITCH\s+:\s+\[(.+)\]', ff)
    ras_switchname  = re.findall('SWITCH NAME\s+:\s+\[(.+)\]', ff)
    ras_vf          = re.findall('VF SETTING\s+:\s+\[(.+)\]', ff)
    ras_fcr         = re.findall('FCR ENABLED\s+:\s+\[(.+)\]', ff)
    ras_xisl        = re.findall('ALLOW XISL\s+:\s+\[(.+)\]', ff)
    ras_ports       = re.findall('Ports\s+:\s+\[(.+)\]', ff)
    
    ll = ras_license[0]
    ll.replace("'","")        #### remove the comma with string command  
    lic_list = ll.split(",")  #### change the data from string to list

    all_list = []
    all_list += [lic_list]
    all_list += [ras_ls_list]
    all_list += [ras_base]
    all_list += [ras_switchname]
        
    
    return(all_list)

    
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################   

 
    
def main():

    global tn   #### varable for telnet session
#######################################################################################################################
####
#### 
####
#######################################################################################################################
    pa = parse_args(sys.argv)
    print(pa)
    #print(pa.chassis_name)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    #print(pa.firmware)
    print(pa.cmdprompt)
    print("@"*40)
    
###################################################################################################################
###################################################################################################################
####
#### if user enter ip address then get the chassisname from the
####   SwitchMatrix file
#### then get the info from the SwitchMatrix file using the Chassis Name
#### 
#### 
####
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
    steps_to_run      = pa.steps
 
    fid_to_compare    = 128
    
    ###################################################################################################################
    #### if the user does not enter a value for which steps to run prompt for user input value
    ####
    if not steps_to_run:
        #pa.start = user_start()
        steps_to_run = pa.start = user_start()
        
    tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    
    if steps_to_run == 1 or steps_to_run == 3:
        
        cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_base_policy")
        switch_info = cofra.get_info_from_the_switch(fid_to_compare, "compare_orig")
    #switch_data_0 = "logs/Switch_Info_for_playback_",pa.ipaddr,".orig.txt" # this failed the compare
                                                                            #  the because it sees it
                                                                            #  as a tuple
    ###################################################################################################################
    #### path to the first file to compare
    switch_data_0 = "logs/Switch_Info_%s_compare_orig.txt" % pa.ipaddr
    
    liabhar.JustSleep(10)
    
    ###################################################################################################################
    #### this is how to reconnect with telnet
    #print("reconnect via telnet")
    #tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")


    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ####
    #### do configupload  or other test steps here
    ###########################################################################
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    
    
    
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ####
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    
    if steps_to_run == 2 or steps_to_run == 3:
        liabhar.JustSleep(10)
        cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_base_policy")
        cons_out = anturlar.fos_cmd("mapspolicy --enable test_policy")
        switch_info = cofra.get_info_from_the_switch(fid_to_compare, "compare")
    ###################################################################################################################
    #### path to the second file to compare
        switch_data_1 = "logs/Switch_Info_%s_compare.txt" % pa.ipaddr
        
        liabhar.cls()
        #### compare the two files
    
        diff_f  = liabhar.file_diff(switch_data_0,switch_data_1)
        print("#"*80)
        print("#"*80)
        print("#"*80)
        print("#"*80)
        print("Result ")
        print(diff_f)
    
    
    ###################################################################################################################
    ####  put additional commands here before disconnecting from telnet
    ####
    #cons_out = anturlar.fos_cmd("mapsdb --show all")
    #print(cons_out)
    cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_base_policy")
    
    anturlar.close_tel()
    dt = liabhar.dateTimeStuff()
    date_is = dt.current()
    print(date_is)
    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

