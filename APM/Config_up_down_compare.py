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
    parser.add_argument('-ftp_ip', '--ftp_ipaddress', help="ftp address of server to upload the config file")
    parser.add_argument('-ftp_n', '--ftp_username', help="ftp username of server to upload the config file")
    parser.add_argument('-ftp_p', '--ftp_password', help="ftp password of server to upload the config file")
    
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
    if not args.ftp_ipaddress or not args.ftp_username or not args.ftp_password:
        print("ftp information is required")
        sys.exit()
     

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

 
def slot_pwr_cycle(slot_list):
    """
    
    """
    
    
    for s in slot_list:
    
        capture_cmd = anturlar.fos_cmd("slotpoweroff %s " % s)
        
        liabhar.JustSleep(30)
        
    for s in slot_list:
        capture_cmd = anturlar.fos_cmd("slotpoweron %s " % s)
        liabhar.JustSleep(60)
    liabhar.JustSleep(300)
    return(True)
    
    

def capture_switch_info(extend_name="", fid=128):
    """
    
    
    """
    
    si = anturlar.SwitchInfo()
    mi = anturlar.Maps()
    fi = anturlar.FlowV()
    fcr = anturlar.FcrInfo()
    
    vdx                  = si.nos_check()
    switch_ip            = si.ipaddress()
    switch_cp_ips        = si.cp_ipaddrs_get()
    license_list         = si.getLicense()
    ls_list              = si.ls()
    first_ls             = si.ls_now()
    switch_id            = si.switch_id()
    fid_now              = si.currentFID()
    try:
        theswitch_name   = si.switch_name()
    except IndexError:
        theswitch_name   = "unknown"
        pass
    chassis_name         = si.chassisname()
    director_pizza       = si.director()
    vf_enabled           = si.vf_enabled()
    sw_type              = si.switch_type()
    base_sw              = si.base_check()
    sim_ports            = si.sim_ports()
    ex_ports             = fcr.all_ex_ports() 
    fcr_state            = si.fcr_enabled()
    ports_and_ls         = si.all_ports_fc_only()
    psw_reset_value      = "YES"
    xisl_st_per_ls       = si.allow_xisl()
    maps_policy_sum      = mi.get_policies()
    maps_non_dflt_policy = mi.get_nondflt_policies()
    
    flow_per_ls          = fi.flow_names()
    blades               = si.blades()
    deflt_switch         = si.default_switch()
    #sfp_info             = si.sfp_info()
    maps_email_cfg       = mi.get_email_cfg()
    maps_actions         = mi.get_actions()
    logical_groups       = mi.logicalgroup_count()
    relay_server_info    = mi.get_relay_server_info()
    credit_recov_info    = mi.credit_recovery()
    dns_info             = mi.dns_config_info()
    sfpinfo              = si.sfp_info()
    
    
    
    
        
    ###################################################################################################################
    ###################################################################################################################
    ####
    #### print the variables for review
    ####
    ###################################################################################################################
    ###################################################################################################################
    
    print("\n\n\n")
    print("SWITCH IP         :  %s  " % switch_ip)
    print("SWITCH NAME       :  %s  " % theswitch_name)
    #print("SWITCH DOMAIN     :  %s  " % domain_list)
    print("LS LIST           :  %s  " % ls_list)
    print("DEFAULT SWITCH    :  %s  " % deflt_switch)
    print("BASE SWITCH       :  %s  " % base_sw)
    print("EX_PORTS          :  %s  " % ex_ports)######################NEW
    print("VF SETTING        :  %s  " % vf_enabled)
    print("SWITCH TYPE       :  %s  " % sw_type)
    print("TIMEOUT VALUE     :  0   " )
    print("RESET PASSWORD    :  %s " % psw_reset_value)
    print("FCR ENABLED       :  %s " % fcr_state)
    print("BLADES            :  %s " % blades)
    print("LICENSE LIST      :  %s  " % license_list)
    
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####
####  Write to the file
####
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
    
    f = "%s%s%s"%("logs/Switch_Info_cudc",switch_ip,"_%s.txt" % extend_name)
    header = "%s%s%s%s" % ("\nSwitch_info_for_playback CAPTURE FILE \n",\
                           "","", "==============================\n")  
    ff = liabhar.FileStuff(f, 'w+b')  #### open the log file for writing
    ff.write(header)
    ###################################################################################################################
    ff.write("SWITCH IP                :  %s  \n" % switch_ip)
    ff.write("LS LIST                  :  %s  \n" % ls_list)
    ff.write("DEFAULT SWITCH           :  %s  \n" % deflt_switch)
    ff.write("BASE SWITCH              :  %s  \n" % base_sw)
    ff.write("EX_PORTS                 :  %s  \n" % ex_ports)
    ff.write("SWITCH NAME              :  %s  \n" % theswitch_name)
    ff.write("CHASSIS NAME             :  %s  \n" % chassis_name)
    ff.write("DIRECTOR STATUS          :  %s  \n" % director_pizza)
    ff.write("VF SETTING               :  %s  \n" % vf_enabled)
    ff.write("SWITCH TYPE              :  %s  \n" % sw_type)
    ff.write("TIMEOUT VALUE            :  0   \n" )
    ff.write("RESET PASSWORD           :  %s  \n" % psw_reset_value)
    ff.write("FCR ENABLED              :  %s  \n" % fcr_state)
    ff.write("Ports                    :  %s  \n" % ports_and_ls)
    ff.write("SIM PORTS                :  %s  \n" % sim_ports)
    ff.write("Blades                   :  %s  \n" % blades)
    
    ff.write("LICENSE LIST             :  %s  \n" % license_list)
    ff.write("SFP  INFO                :  %s  \n" % sfpinfo)
    ff.write("="*80)
    ff.write("\n")
    ff.write("MAPS POLICIES            :  %s  \n" % maps_policy_sum )
    ff.write("MAPS NON DFLT POLICIES   :  %s  \n" % maps_non_dflt_policy)
    ff.write("EMAIL CFG                :  %s  \n" % maps_email_cfg)
    ff.write("MAPS ACTIONS             :  %s  \n" % maps_actions)
    ff.write("LOGICAL GROUPS           :  %s  \n" % logical_groups)
    ff.write("RELAY SERVER HOST IP     :  %s  \n" % relay_server_info)
    ff.write("CREDIT RECOVERY INFO     :  %s  \n" % credit_recov_info)
    ff.write("DNS CONFIG INFO          :  %s  \n" % dns_info)
    ff.write("="*80)
    ff.write("\n")
    ff.write("FLOW CONFIGURATION       :  %s  \n" % flow_per_ls)
    ff.write("\n"*2)
    ff.close()
    
    #cons_out             = anturlar.fos_cmd("setcontext %s " % fid_now)
    
    
    return(True)
    
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
    
    ###################################################################################################################
    ####
    ####   configure some settings that are not defualt to confirm they remain after disruptions
    ####
    cons_out = send_cmd("creditrecovmode --cfg onLrThresh")
    cons_out = send_cmd("creditrecovmode --cfg onLrThresh -lrtthreshold 7")
    cons_out = send_cmd("creditrecovmode --fe_crdloss off")
    cons_out = send_cmd("creditrecovmode --be_crdloss off")
    cons_out = send_cmd("creditrecovmode --be_losync off")
    cons_out = send_cmd("creditrecovmode --fault edgeblade")
    
    
    
    ###################################################################################################################
    ####
    ####   capture teh configuration file  if the user selected 1 or 3
    ####
    
    if steps_to_run == 1 or steps_to_run == 3:
        
        #cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_base_policy")
        #cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_aggressive_policy")
        switch_info = capture_switch_info("compare_orig", fid_to_compare)
        

    ###################################################################################################################
    #### path to the first file to compare
    #switch_data_0 = "logs/Switch_Info_cudc%s_compare_orig.txt" % pa.ipaddr
    
    switch_data_0 = "logs/Switch_Info_cudc%s_compare_orig.txt" % ipaddr_switch
    
    liabhar.JustSleep(10)
    
    ###################################################################################################################
    #### this is how to reconnect with telnet
    #
    #print("reconnect via telnet")
    #tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    #
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ####
    #### do configupload  or other test steps here
    ####  make other changes here before configupload or other commands 
    ####
    ###################################################################################################################
    ####
    ####   
    ####
    pp = cofra.SwitchUpdate()
    
    ###################################################################################################################
    ####
    #### hafailover or hareboot on pizza box
    ####  call the failover function from cofra and send the number of failovers
    ####
    cd = cofra.cfgupload(pa.ftp_ipaddress, pa.ftp_username,pa.ftp_password)
    
    #tn = cofra.ha_failover(1)
    
    liabhar.count_down(120)
    cons_out = anturlar.fos_cmd("echo Y | maspconfig --purge ")
    
    cd = cofra.cfgdownload(pa.ftp_ipaddress, pa.ftp_username,pa.ftp_password)
    liabhar.count_down(120)
    ###################################################################################################################
    ####
    #### 
    ####
    ####
    ####
    #### 
    ####  other actions here
    ####
    ####
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    
    if steps_to_run == 2 or steps_to_run == 3:
      #  liabhar.JustSleep(10)
        liabhar.count_down(60)
        #cons_out = anturlar.fos_cmd("setcontext 128")
        #cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_base_policy")
        #cons_out = anturlar.fos_cmd("mapspolicy --enable dflt_aggressive_policy")
        
        switch_info = capture_switch_info("compare", fid_to_compare)
    ###################################################################################################################
    #### path to the second file to compare
        switch_data_1 = "logs/Switch_Info_cudc%s_compare.txt" % ipaddr_switch
        
        liabhar.cls()
        #### compare the two files
        print("#"*80)
        print("#"*80)
        print("#######")
        print("#######     @@@@@   @@@@@   @@@@@  @   @   @      @@@@@   @  ")
        print("#######     @  @    @       @      @   @   @        @     @  ")
        print("#######     @@@     @@@@    @@@@   @   @   @        @     @  ")
        print("#######     @  @    @           @  @   @   @        @        ")
        print("#######     @   @   @@@@@   @@@@@   @@@    @@@@@    @     @ ")
        print("#"*80)
        print("#"*80)
        
        
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

    anturlar.close_tel()
#   dt = liabhar.dateTimeStuff()
#  date_is = dt.current()
#  print(date_is)
#    print(type(steps_to_run))
#    print(steps_to_run)
    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

