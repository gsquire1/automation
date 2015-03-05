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


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    pp.add_argument("--repeat", help="repeat repeat")
    #pp.add_argument("ip", help="IP address of SUT")
    #pp.add_argument("user", help="username for SUT")
    #pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp 

def parse_args(args):
    
    #global tn,sw_user
    verb_value = "99"
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    #parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    #parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c', '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip', '--ipaddr', help="IP address of SUT")
    #parser.add_argument('-s', '--suite', type=str, help="Suite file name")
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
    #print("Connecting to IP :  " + args.ip)
    #print("user             :  " + args.user)
    #verbose    = args.verbose
     
     

    return parser.parse_args()

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
    
    tn.set_debuglevel(10)
    
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
    reg_list = [ b"Enter your option", b"login: ", b"assword: ", b"root> ", b"users: " ]  
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
    
    cons_out = send_cmd("/sbin/reboot")
    
    reg_list = [ b"Hit ESC to stop autoboot: "]
    
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
    
    tn.set_debuglevel(db)
    tn.write(b"printenv\r\n")
    reg_list = [b"=>"]
    capture = tn.expect(reg_list, 300)
    
    gateway = "10.38.32.1"
    netmask = "255.255.240.0"
    bootargs = "ip=off"
    ethrotate = "no"
    server_ip = "10.38.2.40"
    
    if swtype == 133:
        print("ODIN")
        g = ("setenv ethact ENETO \r\n")
        tn.write(g.encode('ascii'))
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
    
    return(capture)

def pwr_cycle(pwr_ip, pp, db=0):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    anturlar.power_cmd("cd access/1\t/1\t%s" % pp )
     
    anturlar.power_cmd("show\r\n" )
    
    anturlar.power_cmd("cycle")
    anturlar.power_cmd("yes")
    
    
    liabhar.JustSleep(10)
    anturlar.power_cmd("exit")
     
    return(0) 
    
def load_kernel(switch_type, sw_ip, frm_version):
    
    #### set tftp command
    if switch_type == 133: ###  ODIN
        nbt = "tftpboot 0x1000000 net_install26_odin.img"
    if switch_type == "STINGER":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
    if switch_type == "TOMTOO":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
    if switch_type == "5100":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
    if switch_type == "TOMAHAWK":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
       
    ####set type true for skybolt and yoda
    ####
    if switch_type == 133:
        type = True
    
    ####   do these step sfor ODIN, STINGER, TOMTOO, 5100, 300 
    reg_list = [ b"=>"]
    reg_bash = [ b"bash-2.04#"]
    
    tn.write(b"%s\r\n" % nbt)
    capture = tn.expect(reg_list, 300)
    tn.write(b"bootm 0x1000000\r\n")
    capture = tn.expect(reg_bash, 300)
    
    
    if type:
    ####  do these for SKYBOLT  and YODA  ONLY
        tn.write(b"makesinrec 0x1000000 \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x2000000  skybolt/uImage \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x3000000 skybolt/ramdisk.skybolt \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x4000000 skybolt/silkworm.dtb \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000 \r\n")
        caputure = tn.expect(reg_bash,300)
    
    
    else:
    #### do these steps for ALL switch types
        pass
    
    tn.write(b"export PATH=/usr/sbin:/sbin:$PATH\r\n")
    capture = tn.expect(reg_bash, 300)
    tn.write(b"ifconfig eth0 %s netmask 255.255.240.0 \r\n" % sw_ip )
    capture = tn.expect(reg_bash, 300)
    tn.write(b"route add default gw 10.38.32.1 \r\n")
    capture = tn.expect(reg_bash, 300)
    tn.write(b"mount -o tcp,nolock,rsize=32768,wsize=32768 10.38.2.20:/export/sre /load\r\n")
    capture = tn.expect(reg_bash, 300)
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
    
    print("@"*80)
    print("@"*80)
    print("looking for %s  " % chassis_name)
    print(type(chassis_name))
    print("@"*80)
    
    for line in csv_file:
        chassis_name_from_file = (line['Nickname'])
        print("@"*80)
        print(chassis_name_from_file)
        print(type(chassis_name_from_file))
        print("@"*80)
        
        if chassis_name_from_file == chassis_name:
            #sn = (switch_name)
            
            cons_1_ip   = (line['Console1 IP'])
            cons_1_port = (line['Console1 Port']) 
            cons_2_ip   = (line['Console2 IP'])
            cons_2_port = (line['Console2 Port']) 
        
            a = []
            a = [cons_1_ip, cons_1_port]
            print("@"*80)
            print(chassis_name)
            print("&"*80)
            print(cons_2_ip)
            
            if cons_2_ip:
                print("&"*80)
                print("checked for true cons_2_ip")
                print(cons_2_ip)
                
                a += [cons_2_ip]
                a += [cons_2_port]
         
        else:
            print("NO MATCH")
            
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
    
    print("@"*80)
    print("@"*80)
    print("@"*80)
    
    for line in csv_file:
        chassis_name_from_file = (line['Nickname'])
        
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
        chassis_name_from_file = (line['Nickname'])
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
        chassis_name_from_file = (line['Nickname'])
        if chassis_name_from_file == chassis_name:
            ip = (line['IP Address'])
                        
    return(ip)
   
###############################################################################
###############################################################################
###############################################################################
###############################################################################    

 
    
def main():

    global tn
    
###############################################################################
####
#### variable required for netinstall
####
###############################################################################
   
    #cons_ip = "10.38.32.152"
    #cons_port = 3019
    ##my_ip = "10.38.37.83"
    #user_name = "root"
    #psswd = "password"
    #gateway = "10.38.32.1"
    #netmask = "255.255.240.0"
    #bootargs = "ip=off"
    #ethrotate = "no"
    #server_ip = "10.38.2.40"
    #pwr_ip= "10.38.32.119"
    #power_port = 12
    #
    
    
    
    pa = parse_args(sys.argv)
    print(pa)
    print(pa.chassis_name)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    print("@"*40)
    ###########################################################################
    ###########################################################################
    ####
    #### hold the ip address from the command line
    ####  
    ipaddr = pa.ipaddr
    #print("IP FROM COMMAND LINE  %s " % ipaddr)
    
    cons_info         = console_info(pa.chassis_name)
    #print("console"*7)
    #print(cons_info)
    console_ip = cons_info[0]
    console_port = cons_info[1]
    #print("Console IP and Port are  %s   %s  " %  (console_ip, console_port))
    #print("console"*7)
    
    power_pole_info   = pwr_pole_info(pa.chassis_name)    
    #print("PowerPole"*6)
    #print(power_pole_info)
        
    #print("PowerPole"*6)
    
    usr_pass = get_user_and_pass(pa.chassis_name)
    #print("USER PASSWORD  %s  " % usr_pass)
    #print("USER NAME is %s    " % usr_pass[0])
    #print("USER PASS is %s    " % usr_pass[1])
    #print("USER__PASSWORD_"*5)
    
    user_name = usr_pass[0]
    usr_psswd = usr_pass[1]
    
    
    ipaddr_switch = get_ip_from_file(pa.chassis_name)
    #print("IP ADDRESS is %s  " % ipaddr_switch)
    
    
    
    
    
    
    #### need to get the ipaddress from the file
    #### pass to login procedure
    #### already have username password
    
    cons_out = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    
    sw_dict = cofra.get_info_from_the_switch()
    #print("\n\n\nGET IP")
    my_ip                = sw_dict["switch_ip"]
    #print("\n\n\nGET NAME")
    sw_name              = sw_dict["switch_name"]
    #print("\n\n\nGET CHASSIS_NAME")
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

    print("\n"*20)
    print("SWITHC IP            : %s   " % my_ip)
    print("SWITCH NAME          : %s   " % sw_name)
    print("CHASSIS NAME         : %s   " % sw_chass_name)
    print("DIRECTOR             : %s   " % sw_director_or_pizza)
    print("SWITCH DOMAINS       : %s   " % sw_domains)
    print("LOGICAL SWITCH LIST  : %s   " % sw_ls_list)
    print("BASE FID             : %s   " % sw_base_fid)
    print("XISL STATE           : %s   " % sw_xisl)
    print("SWITCH TYPE          : %s   " % sw_type)
    print("LICENSE LIST         : %s   " % sw_license)
    print("VF SETTING           : %s   " % sw_vf_setting)
    print("FCR SETTING          : %s   " % sw_fcr_enabled)
    print("PORT LIST            : %s   " % sw_port_list)
    print("@"*40)
    print("CONSOLE INFO         : %s   " % cons_info)
    print("@"*40)
    print("POWER POLE INFO      : %s   " % power_pole_info)
    
    
     
###############################################################################
####
####  close telnet connection and 
####  connect to the console
####
###############################################################################
     
    anturlar.close_tel()
    connect_console(console_ip, user_name, usr_pass, console_port)
    cons_out = send_cmd("switchshow")
    #print("**************************************************************")
    #print("\n\n\n\n\n\n\n\n\n\n")
    cmd_list = ["switchshow", "fabricshow", "mapsdb --show"]
    for c in cmd_list:
        cons_out = send_cmd(c)

###############################################################################
####
####  reboot and find the command prompt
####
    
    #cons_out = stop_at_cmd_prompt(9)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(cons_out)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    cons_out = env_variables(sw_type, 9)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print(cons_out)
    #pwr_cycle(pwr_ip, power_port)
    
    for pp in range(0, len(power_pole_info), 2):
        print('POWERPOLE')
        print(power_pole_info[pp])
        print(power_pole_info[pp+1])
        
        
        #pwr_cycle(power_pole_info[pp],power_pole_info[pp+1])
    
    tn.write(b"exit\n")
    tn.close()
    
    
    
    
if __name__ == '__main__':
    
    main()


###############################################################################
####
####
####
####
#
#  Constant variables
#       gateway_ip    10.38.32.1
#       bootargs      =ip=off
#       server_ip     10.38.2.40
#       subnetmask    255.255.240.0
#       


#=> printenv
#AutoLoad=yes
#InitTest=MEM()
#LoadIdentifiers=Fabric Operating System;Fabric Operating System
#OSLoadOptions=quiet;quiet
#OSLoader=ATA()0x1f1c48;ATA()0x1404f
#OSRootPartition=hda2;hda1
#SkipWatchdog=yes
#baudrate=9600
#bootargs=ip=off
#bootcmd=setenv bootargs mem=${mem} ${OSLoadOptions};ataboot;bootm 0x400000
#bootdelay=5
#ethact=ENET0
#ethaddr=00:05:33:7A:0F:88
#gateway=10.38.32.1
#gatewayip=10.38.32.1
#hostname=sequoia
#initrd_high=0x20000000
#ipaddr=10.38.37.50
#loads_echo=1
#mem=1044480k
#netmask=255.255.240.0
#preboot=echo;echo Type "run flash_nfs" to mount root filesystem over NFS;echo
#netdev=eth0
#consoledev=ttyS1
#ramdiskaddr=400000
#ramdiskfile=your.ramdisk.u-boot
#serverip=10.38.2.40
#stderr=serial
#stdin=serial
#stdout=serial
#submask=255.255.240.0
#ver=U-Boot 1.1.3 (Feb  5 2015 - 14:19:55)
#
#Environment size: 784/4080 bytes

