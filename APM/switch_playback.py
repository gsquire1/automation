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
import anturlar
import liabhar

###############################################################################

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
        capture = tn.expect(reg_list)
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
    
   
def env_variables(db=0):
    
    tn.set_debuglevel(db)
    tn.write(b"printenv\r\n")
    reg_list = [b"=>"]
    
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
    
def load_kernel(switch_type, sw_ip):
    
    #### set tftp command
    if switch_type == "ODIN":
        nbt = "tftpboot 0x1000000 net_install26_odin.img"
    if switch_type == "STINGER":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
    if switch_type == "TOMTOO":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
    if switch_type == "5100":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
    if switch_type == "TOMAHAWK":
        nbt = "tftpboot 0x1000000 net_install_v7.2.img"
        
    
    
    
    ####   do these step sfor ODIN, STINGER, TOMTOO, 5100, 300 
    reg_list = [ b"=>"]
    reg_bash = [ b"bash-2.04#"]
    tn.write(b"%s" % nbt)
    capture = tn.expect(reg_list, 300)
    tn.write(b"bootm 0x1000000\r\n")
    capture = tn.expect(reg_bash, 300)
    
    
    
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
    
    
    
    #### do these steps for ALL switch types
    
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


def get_info_from_the_switch():
    cons_out = anturlar.login()
    
    si = anturlar.SwitchInfo()
    
    switch_ip = si.ipaddress()
    license_list = si.getLicense()
    ls_list = si.ls()
    first_ls = si.ls_now()
    switch_id = si.switch_id()
    theswitch_name = si.switch_name()
    vf_enabled = si.vf_enabled()
    sw_type = si.switch_type()
    
    ports_and_ls = si.all_ports_fc_only()
    psw_reset_value = "YES"
       
        
    
    
    #############################################################
    #### create a dict for ls and ports in the ls
    ####
    k = first_ls  #### craete a key with the command name
                               #### and pid added together
    v = ports_and_ls   #### create the value as a list otherwise the first one
                      #### is a string and extend command later on will fail
    #print("K AND V ARE : %s   %s " % (k,v))
    d = {k:v}     #### create the first dictionary entry ras[0]
    print(d)
    print("@"*600)
    print("@"*600)
    print("@"*600)
    for kk, vv in d.items():
        print(kk,vv)    #### print to the crt
        print("@"*60)
    print("*"*80)
    print("\n\n\n")
    
    for ls in ls_list:
        cons_out = anturlar.fos_cmd("setcontext %s " % ls)
        ports_and_ls = si.all_ports_fc_only()
        key = ls
        print(key)
        print("@"*600)
        if key not in d:
            print("@"*600)
            print("KEY IS NOT IN D   *************************")
            print("looking for %s in d" % key)
            print("ls value is  %s  " % ls)
            print(key)
            print("@"*600)
            
        if ls in d:
            print("@"*600)
            print("LS IS IN D   DD ******************************")
            print("looking for %s in d" % key)
            print("ls value is  %s  " % ls)
            print(key)
            print("@"*600)  
            
            
            
        
        if key in d:
            #value = d[key]
            print("@"*600)
            #print("\n\n\nvalue of d key is :  %s " % value )
        else:
            value = []
            #ras_value = [ras[y][3]]
            #value.extend(ras_value)
            value = ports_and_ls 
            d[key] = value            #### add the value to the key
                       
    
    print("\n\n\n")
    print("SWITCH IP         :  %s  " % switch_ip)
    print("LICENSE LIST      :  %s  " % license_list)
    print("SWITCH DOMAIN     :  %s  " % switch_id)
    print("LS LIST           :  %s  " % ls_list)
    #print("Ports             :  %s  " % ports_and_ls)
    print("SWITCH NAME       :  %s  " % theswitch_name)
    print("VF SETTING        :  %s  " % vf_enabled)
    print("SWITCH TYPE       :  %s  " % sw_type)
    print("TIMEOUT VALUE     :  0   " )
    print("RESET PASSWORD    :  %s " % psw_reset_value)
    
    
    for kk, vv in d.items():
        print(kk,vv)    #### print to the crt
        print("@"*60)
    print("*"*80)
    print("\n\n\n")
    
    
    switch_dict = ""
    
    
    sys.exit()
    
    return(switch_dict)

    
def main():

    global tn
    
###############################################################################
####
#### variable required for netinstall
####
###############################################################################
    cons_ip = "10.38.32.152"
    cons_port = 3019
    my_ip = "10.38.37.83"
    user_name = "root"
    psswd = "password"
    gateway = "10.38.32.1"
    netmask = "255.255.240.0"
    bootargs = "ip=off"
    ethrotate = "no"
    server_ip = "10.38.2.40"
    pwr_ip= "10.38.32.119"
    power_port = 12
    
    
    sw_dict = get_info_from_the_switch()
    
    
    
###############################################################################
#### 
###############################################################################
    tn  = connect_console(cons_ip,user_name,psswd,cons_port)
    
    print("**************************************************************")
    print("\n\n\n\n\n\n\n\n\n\n")
    
    cmd_list = ["switchshow", "fabricshow", "mapsdb --show"]
    
    for c in cmd_list:
        cons_out = send_cmd(c)
    
    
    
    cons_out = send_cmd("switchshow")
    
    #print(cons_out)
    
    cons_out = send_cmd("fabricshow")
    #print(cons_out)
    
    
    
    cons_out = stop_at_cmd_prompt(9)
    
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    
    print(cons_out)
    
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    cons_out = env_variables(9)
   
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print(cons_out)
    
    
    
    
    pwr_cycle(pwr_ip, power_port)
    
    
    
    
    tn.write(b"exit\n")
    tn.close()
    
    
    
    
    
    
    
    
    
    
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

