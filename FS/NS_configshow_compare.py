#!/usr/bin/env python3


#######################################################################################################################
####
#### This template has the format to create a script that:
#### 1) connects to a switch and captures output of "configshow" first for comparison later
#### 2) send any FOS command (allows user to add different functions that will do operations on the switch)
#### 3) capture the output of "configshow" again 
#### 4) compare the two captures for differences, return True or False and if false disaply differences
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
import PortFlapper
#import time

#######################################################################################################################
####
####  Identify the path that a module resides in here
####
#######################################################################################################################
sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')
sys.path.append('/home/automation/APM')
#sys.path.append('/home/RunFromHere/logs')

#######################################################################################################################
####
####  Import user created Modules here
####
#######################################################################################################################
import sw_matrix_tools
import anturlar
import liabhar
import cofra
import Config_up_down_compare


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
    pp.add_argument("porttype", type=str, help="Choose the port type to operate on (eports/fports)")
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
    parser.add_argument('-i',   '--iterations', type=int, default=1, help="number of iterations")
    #parser.add_argument('-eports', '--eports', type=int, default=0, help="bounce all eports")
    #parser.add_argument('-fports', '--fports', type=int, default=0, help="bounce all fports")
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
        
    porttype = args.porttype
    if porttype != porttype.isalpha() and len(porttype) != 6:
        print("\nYOU MUST USE EITHER 'eports' or 'fports' in the CLI\n")
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
    print(pa.iterations)
    print(pa.porttype)
    print("@"*40)
    print("@"*40)
    #sys.exit()
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
 ####   connect via telnet:
 ####   if you want to connect to the console it is available in anturlar and an example is available below
 ####
 ####
 ######################################################################################################################
 ######################################################################################################################
 ####   Config_up_down_compare.main()

    #cons_out = anturlar.fos_cmd("firmwareshow")                          ####   send any command with anturlar.fos_cmd
    #print("\r\n")
    #liabhar.JustSleep(5)                                                ####   sleep without printing anything
    #print(cons_out)
    # print("now closing telnet session ") 
    # #anturlar.close_tel()                                                 ####  close the telnet session
#######################################################################################################################   
#######################################################################################################################
####
####   connect via console example and other "send command" commands
####    
####
#######################################################################################################################
#######################################################################################################################
    #tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)   ####  connect to console w/o parser info
    #cons_out = anturlar.fos_cmd("firmwareshow")
    #cons_out = anturlar.fos_cmd("setcontext %s " % pa.fid)                 ####  change to the fid given on the command  
    #tn = anturlar.connect_console(console_ip,console_port)                 ####  use the console ip and console port info
    #cons_out = anturlar.fos_cmd("switchshow")                              ####  send a command via the console
    #cons_out = cofra.power_cycle(power_pole_info)                          ####  powercycle switch via switchmatrix.csv file
    #liabhar.JustSleep(30)                                                  ####  wait for the switch to boot
    #cons_out = anturlar.send_cmd_console("\r\n")                           ####  send some commands to the console
    #cons_out = anturlar.send_cmd_console("setcontext %s " % pa.fid)        ####  send some commands to the console
    #cons_out = anturlar.send_cmd_console("firmwareshow")                   ####  send some commands to the console
    #capture = cofra.cfgupload("10.38.35.131", "ftp1", "ftp2")              ####  send a cfgupload file to a ftp server
    #liabhar.count_down(5)                                                  ####  set and observe a count down timer


#######################################################################################################################
#######################################################################################################################
####
####  This starts the template for configshow output comparison (after some type of switch operation).
####  First snippet of code simply opens a connection, changes to requested fid, sends output of configshow to a file.
####
#######################################################################################################################
#######################################################################################################################
    tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    cons_out = anturlar.fos_cmd("setcontext %s " % pa.fid)  
    dt = liabhar.dateTimeStuff()                                        #### create the object for date and time stuff
    date_is = dt.current_no_dash_at_end()                               #### get the current time for file naming purposes
    #print("\n\nDate is %s" % date_is)
    
    liabhar.count_down(3)                                               ####   count down to the next command 
    #configup_cmd = ("configupload -all -p ftp %s,%s,/configs/%s.txt,%s") % ("10.38.35.131","ftp1", ipaddr_switch, "ftp2")
    f = "%s%s%s%s"%("logs/NameServer_test_case_file","_"+ipaddr_switch+"_",date_is,".txt")
    f1 = "%s%s%s%s"%("logs/NameServer_test_case_file","_"+ipaddr_switch+"_",date_is,".txt")
    ff = liabhar.FileStuff(f, 'w+b')                                    #### open the log file for writing       
    #header = "%s%s%s%s" % ("\nNAMESERVER CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch,"\n==============================\n\n") #### write a header line at top of file
    header = "%s%s%s%s" % ("\nNAMESERVER CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch, "\n==============================\n\n")
    ff.write(header)
    ff.write(anturlar.fos_cmd("nsshow"))
    ff.write(anturlar.fos_cmd("nsallshow"))
    ff.close()
    g = open(f, "r")
    lines = g.readlines()
    g.close()
    ff = liabhar.FileStuff(f, 'w+b')
    for l in lines:
        if " date = " not in l:
            ff.write(l)
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

    # tn = cofra.clear_stats()
    # print(pa.porttype)
    # #sys.exit()
    # porttype = pa.porttype
    # print(porttype)
    # PortFlapper.main(porttype)
#############################################################################################
    si = anturlar.SwitchInfo()
    fi = anturlar.FabricInfo()
    fabric_check =  fi.fabric_members()
    f_ports = si.f_ports()
    e_ports = si.e_ports()
    print("\n\n\n\n")
    print(f_ports)
    print(e_ports)
    print("\n\n\n\n")
    if pa.porttype == "eports":
        ports = e_ports
    else:
        ports = f_ports
    i = ipaddr_switch
    
    # try: 
    #     tn = anturlar.connect_tel_noparse(i,user_name,usr_psswd)
    # except OSError:
    #     print("Switch %s not available" % i) 
    nos = si.nos_check()
    if not nos:
        for i in ports:
            slot = i[0]
            port = i[1]
            if slot:
                anturlar.fos_cmd("portdisable %s/%s" % (slot, port))
                liabhar.count_down(15)
                anturlar.fos_cmd("portenable %s/%s" % (slot, port))
                liabhar.count_down(15)
            else:
                anturlar.fos_cmd("portdisable %s" % (port))
                liabhar.count_down(15)
                anturlar.fos_cmd("portenable %s" % (port))
                liabhar.count_down(15)
        fabric_check1 =  fi.fabric_members()
        if fabric_check != fabric_check1:
            print ("WTF")
            #email_sender_html(you, me, subj, html_to_send, htmlfile_path = "" )
            liabhar.email_sender_html("gsquire@brocade.com","gsquire@brocade.com","NS_portflapper failed","NS_portflapper failed","")
            sys.exit()
        anturlar.close_tel()
        #return(True)         
    else:
        print("\n"+"@"*40)
        print('\nTHIS IS A NOS SWITCH> SKIPPING')
        print("\n"+"@"*40)
        pass
    #anturlar.close_tel()
####################################################################################################################
    #anturlar.fos_cmd("tsclockserver 10.38.2.80; tstimezone America/Denver")
    #tn = cofra.ha_failover(pa.iterations)
    #tn = cofra.power_cycle_iterations(power_pole_info, pa.iterations)
    
    
    tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    cons_out = anturlar.fos_cmd("setcontext %s " % pa.fid)
    date_is = dt.current_no_dash_at_end()
    f1 = "%s%s%s%s"%("logs/NameServer_test_case_file","_"+ipaddr_switch+"_",date_is,".txt")
    ff = liabhar.FileStuff(f1, 'w+b')  #### reset the log file
    #header = "%s%s%s%s" % ("\NAMESERVER CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch,"\n==============================\n\n")
    #header = "%s%s%s%s" % ("\nCONFIGUPLOAD CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch, "\n==============================\n\n")
    header = "%s%s%s%s" % ("\nNAMESERVER CAPTURE FILE \n", "  sw_info ipaddr  ",ipaddr_switch, "\n==============================\n\n")
    ff.write(header)
    ff.write(anturlar.fos_cmd("nsshow"))
    ff.write(anturlar.fos_cmd("nsallshow"))
    ff.close()
    g = open(f1,"r")
    lines = g.readlines()
    g.close()
    ff = liabhar.FileStuff(f1, 'w+b')
    for l in lines:
        if " date = " not in l:
            ff.write(l)            
    ff.close()
    
    diff_f  = liabhar.file_diff(f,f1)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("Result ")
    print(diff_f)
    liabhar.email_sender_html("gsquire@brocade.com","gsquire@brocade.com","NS_portflapper passed","NS_portflapper passed","")

    return(True)
    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

