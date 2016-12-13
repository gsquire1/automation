#!/usr/bin/env python3


#######################################################################################################################
####
####  This template has the format to create a script that connects to a
####     switch and send any FOS command, capture the output 
####
#######################################################################################################################

#######################################################################################################################
####
####   Import Standard Library Modules here
####
#######################################################################################################################

import os,sys
import telnetlib
import getpass
import argparse
import re
#import csv
#import time

#######################################################################################################################
####
####  Identify the path that a module resides in here
####
#######################################################################################################################
sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')

#######################################################################################################################
####
####  Import user created Modules here
####
#######################################################################################################################
import sw_matrix_tools
import anturlar
import liabhar
import cofra


#######################################################################################################################
####  list of switch types 
####  --------------------
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
####  162   Wedge
####  165   X6-4 (Venator)
####  166   X6-8 (Allegience)
####  170   Chewbacca
####
####
####
####
#######################################################################################################################



def parent_parser():
    """
       the parent parser to handle the main arguements 
       
    """
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
    """
        the agrument parser for options unique to the new script
        
    """

    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    #parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    #parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    parser.add_argument('-cp',   '--cmdprompt', help="switch is already at command prompt")
    parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
    #parser.add_argument('-s', '--suite', type=str, help="Suite file name")
    #parser.add_argument('-p', '--password', help="password")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    #group.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")
    
    
    ###################################################################################################################
    ####
    ####  handle how the args interact together here
    ####    the first example requires the Chassis name or IP address with the command 
    ####
    ###################################################################################################################
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
 
    return parser.parse_args()



#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################  

 
    
def main():

    global tn
#######################################################################################################################
####
####   start with parsing the command line
#### 
####    use  the procedures  parent_parser and parse_args
####     to determine the command line switches 
####
#######################################################################################################################
    pa = parse_args(sys.argv)
    print(pa)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    print(pa.cmdprompt)
    print("@"*40)
    print("@"*40)
#######################################################################################################################
#######################################################################################################################
####
#### if user enter ip address then get the chassisname from the
####   SwitchMatrix file
#### 
#### then get the info from the SwitchMatrix file using the Chassis Name
#### 
#### 
####  Type,Chassisname,IP Address,Username,Password,Console1 IP,Console1 Port,Console2 IP,Console2 Port,
####       Power1 IP,Power1 Port,Power2 IP,Power2 Port,Power3 IP,Power3 Port,Power4 IP,Power4 Port,
####            KVM IP,KVM Port,Web Username,Web Password,Admin Password
####
#######################################################################################################################
#######################################################################################################################
    if pa.ipaddr:
        print("do IP steps")
        pa.chassis_name = sw_matrix_tools.console_info_from_ip(pa.ipaddr)
        
    cons_info         = sw_matrix_tools.console_info(pa.chassis_name)
    console_ip        = cons_info[0]
    console_port      = cons_info[1]
    console_ip_bkup   = cons_info[2]
    console_port_bkup = cons_info[3]
    
    power_pole_info   = sw_matrix_tools.pwr_pole_info(pa.chassis_name)    
    usr_pass          = sw_matrix_tools.get_user_and_pass(pa.chassis_name)
    user_name         = usr_pass[0]
    usr_psswd         = usr_pass[1]
    
    ipaddr_switch     = sw_matrix_tools.get_ip_from_file(pa.chassis_name)
 
 ######################################################################################################################
 ######################################################################################################################
 ####
 ####   connect via telnet
 ####                            if you want to connect to the console it is available in anturlar and an example below
 ####
 ####
 ######################################################################################################################
 ######################################################################################################################
    tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    cons_out = anturlar.fos_cmd("setcontext %s " % pa.fid)               ####   change to the fid given on the command 
    cons_out = anturlar.fos_cmd("firmwareshow")                          ####   send any command with anturlar.fos_cmd
    print("\r\n")
    liabhar.JustSleep(30)                                                ####   sleep without printing anything
    print("now closing telnet session ") 
    anturlar.close_tel()                                                 ####  close the telnet session
    liabhar.JustSleep(30)
#######################################################################################################################   
#######################################################################################################################
####
####   connect via console example
####    
####
#######################################################################################################################
#######################################################################################################################
 
    #tn = anturlar.connect_console(console_ip,console_port)          ####  use the console ip and console port info
    #cons_out = anturlar.fos_cmd("switchshow")                       ####  send a command via the console
    #
    ##cons_out = cofra.power_cycle(power_pole_info)                  #### power cycle the switch  using the
    #                                                                ####   Switch Matrix info
    #liabhar.JustSleep(30)                                           ####  wait for the switch to boot
    #
    #
    #cons_out = anturlar.send_cmd_console("\r\n")                        ####  send some commands to the console
    #                                                                    ####
    #cons_out = anturlar.send_cmd_console("setcontext %s " % pa.fid)     ####
    #cons_out = anturlar.send_cmd_console("firmwareshow")                ####


#######################################################################################################################
#######################################################################################################################
####
####  do anything else you want to try
####
####
#######################################################################################################################
#######################################################################################################################
    dt = liabhar.dateTimeStuff()                         #### create the object for date and time stuff
    date_is = dt.current()                               #### get the current time
    print(date_is)
    
    print("Leaving the script\r\n\r\n")
    liabhar.count_down(30)                               ####   count down to the next command 
    
#######################################################################################################################
#######################################################################################################################
####
####  This starts the template section for configshow output comparison (after some type of switch operation).
####  First snippet of code simply opens a connection, changes to requested fid, sends output of configshow to a file.
####
#######################################################################################################################
#######################################################################################################################
    tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    cons_out = anturlar.fos_cmd("setcontext %s " % pa.fid)  
    dt = liabhar.dateTimeStuff()                                        #### create the object for date and time stuff
    date_is = dt.current_no_dash_at_end()                               #### get the current time for file naming purposes
    #print("\n\nDate is %s" % date_is)
    
    liabhar.count_down(5)                                               ####   count down to the next command 
    #configup_cmd = ("configupload -all -p ftp %s,%s,/configs/%s.txt,%s") % ("10.38.35.131","ftp1", ipaddr_switch, "ftp2")
    f = "%s%s%s%s"%("logs/Configupload_test_case_file",ipaddr_switch,date_is,".txt")
    ff = liabhar.FileStuff(f, 'w+b')                                    #### open the log file for writing       
    header = "%s%s%s%s" % ("\nCONFIGUPLOAD CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch,"\n==============================\n\n")                                 #### write a header line at top of file
    ff.write(header)
    #cons_out = anturlar.fos_cmd (configup_cmd)
    ff.write(anturlar.fos_cmd("configshow"))
    ff.close()                                                          #### close this file for comparison later
#######################################################################################################################
#######################################################################################################################
####
####  do anything else you want to try (small sample of examples):
####  anturlar.fos_cmd("tsclockserver 10.38.2.80; tstimezone America/Denver")
####  anturlar.fos_cmd("cfgenable")
####  anturlar.fos_cmd("switchdisable")
####  anturlar.fos_cmd("switchenable")
####
####  In the below snippet we run tsclockerver: anturlar.fos_cmd("tsclockserver 10.38.2.80; tstimezone America/Denver")
####  Then grab output of configshow, drop into a file and compare that with original
####
#######################################################################################################################
#######################################################################################################################

    
    anturlar.fos_cmd("tsclockserver 10.38.2.80; tstimezone America/Denver")
    date_is = dt.current_no_dash_at_end()
    f1 = "%s%s%s%s"%("logs/Configupload_test_case_file",ipaddr_switch,date_is,".txt")
    ff = liabhar.FileStuff(f1, 'w+b')  #### reset the log file        
    header = "%s%s%s%s" % ("\nCONFIGUPLOAD CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch, "\n==============================\n\n")  
    ff.write(header)
    #cons_out = anturlar.fos_cmd (configup_cmd)
    ff.write(anturlar.fos_cmd("configshow"))
    ff.close()
    
    diff_f  = liabhar.file_diff(f,f1)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("Result ")
    print(diff_f)

    #return(cons_out)
    return(True)

if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

