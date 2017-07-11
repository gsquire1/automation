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
import csv
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
    pp.add_argument("file", help="csv file that has info for the test \n Chassisname,FID ")
    #pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
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
    #parser.add_argument('-cp',   '--cmdprompt', help="switch is already at command prompt")
    #parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
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
    
    #if not args.chassis_name and not args.ipaddr:
    #    print("Chassis Name or IP address is required")
    #    sys.exit()
    #    
    #if args.cmdprompt and not args.switchtype:
    #    print("To start at the command prompt the switch type is needed.")
    #    sys.exit()
    #    
    #if not args.cmdprompt and args.switchtype:
    #    print('To start at the command prompt both switch type and command prompt is requried')
    #    sys.exit()
 
    return parser.parse_args()

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################  

def verb_list_print(show_list):
    """
       print a list member at a time
       
    """
    print("@"*80)
    print("#"*80)
    print(show_list)
    print("\n")
    for f in show_list:
        print(f)
        print("\r\n")
    print("#"*80)
    print("@"*80)

    return(True)


def look_for_zero(stats):
    """
      scan the output looking for zero in the stats
      if there is a zero flag it as a failure or should be investigated
      
      
    """
    
    con_out = anturlar.fos_cmd("version")
    ras = re.compile('\s+([0]\s+)')
    #ras_dir = re.compile('[ \\t0-9CPFOS]{19,21}')
    #ras = ras.search(capture_cmd)
    ras = ras.findall(stats)
    
    if ras == []:
        pass_fail = True
    else:
        pass_fail = False
    
    print("@"*80)
    print("#"*80)
    
    print("\n")
    print(ras)
    print("\n")
    
    print("#"*80)
    print("@"*80)
    
    return(pass_fail)
    

def get_info_from_flow_file(name):
    """
        get the information from the file given at the start of the script
        
        
    """
    
    flow_reg_file = "ini/%s" % name
    
    try:
        csv_file = csv.DictReader(open(flow_reg_file, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    chass_fid = []
    for line in csv_file:
        chassname = (line['Chassisname'])
        fid       = (line['FID'])    
    
        chass_fid.append(chassname)
        chass_fid.append(fid)
        
    return(chass_fid)

def write_to_results_file(what_to_write,ip,stamp):
    """
        write to the Flow File 
    
    """
    dt = liabhar.dateTimeStuff()                                        #### create the object for date and time stuff
    date_is = "%s" % (dt.current()) 

    f = "%s%s%s%s%s"%("logs/Flow_regression_result_",ip,"_",stamp,".txt")
    ff = liabhar.FileStuff(f, 'a+b')                                    #### open the log file for writing       
    ff.write(date_is)
    ff.write("\r\n")
    ff.write(what_to_write)
    ff.write("\r\n")
    
    ff.close()                                                          #### close this file 
    
    return(True)
    
def write_pass_fail_to_file(pass_or_not,ip,stamp):
    """
        write the results of looking for zero to the file 
    
    """
    dt = liabhar.dateTimeStuff()                                        #### create the object for date and time stuff
    date_is = "%s" % (dt.current()) 

    f = "%s%s%s%s%s"%("logs/Flow_regression_result_",ip,"_",stamp,".txt")
    ff = liabhar.FileStuff(f, 'a+b')                                    #### open the log file for writing       
    ff.write("\r\n")
    ff.write("@"*80)
    ff.write("\r\n")
    ff.write("#"*80)
    ff.write("\r\n")
    ff.write(date_is)
    ff.write("\r\n")
    if pass_or_not:
        ff.write("FOUND NO ZERO COUNTS")
    else:
        ff.write("ZERO WAS FOUND AT LEAST ONE TIME ")
        ff.write("FAIL  ??? ")
    ff.write(str(pass_or_not))
    ff.write("\r\n")
    ff.write("@"*80)
    ff.write("\r\n")
    ff.write("#"*80)
    ff.write("\r\n")
    
    ff.close()                                                          #### close this file 
    
    return(True)
    
def get_time_stamp():
    """
    
    """
    
    dt = liabhar.dateTimeStuff()                                        #### create the object for date and time stuff
    stamp = dt.stamp() 
    date_is = str(stamp)
    date_is = date_is[:-8]
    
    return(date_is)
    
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
    if pa.verbose:
        print("@"*40)
        print("#"*40)
        print(pa)
        print(pa.file)
        print(pa.quiet)
        print(pa.verbose)
        print("#"*40)
        print("@"*40)
#######################################################################################################################
#######################################################################################################################
####
#### if user enter ip address then get the chassisname from the
####   SwitchMatrix file
#### 
#### then get the info from the SwitchMatrix file using the Chassis Name
#### 
####  Type,Chassisname,IP Address,Username,Password,Console1 IP,Console1 Port,Console2 IP,Console2 Port,
####       Power1 IP,Power1 Port,Power2 IP,Power2 Port,Power3 IP,Power3 Port,Power4 IP,Power4 Port,
####            KVM IP,KVM Port,Web Username,Web Password,Admin Password
####
#######################################################################################################################
#######################################################################################################################

    reg_list = get_info_from_flow_file(pa.file)
    if pa.verbose:
        print("\n\ninfo from flow reg file\n\n")
        print(reg_list)
    
####  this is common steps to get the information from a csv file
####    for this test we only need the chassis name and fid
    for i in range(0,len(reg_list),2):
        chass_1     = reg_list[i]
        target_fid  = reg_list[i+1]
        print("chassname is  %s " % chass_1)
        print("target fid  is  %s " % target_fid)
        #chass_1     = reg_list[0]
        #target_fid  = reg_list[1]
        #cons_info         = sw_matrix_tools.console_info(chass_1)
        #console_ip        = cons_info[0]
        #console_port      = cons_info[1]
        #console_ip_bkup   = cons_info[2]
        #console_port_bkup = cons_info[3]
        power_pole_info   = sw_matrix_tools.pwr_pole_info(chass_1)    
        usr_pass          = sw_matrix_tools.get_user_and_pass(chass_1)
        user_name         = usr_pass[0]
        usr_psswd         = usr_pass[1]   
        ipaddr_switch     = sw_matrix_tools.get_ip_from_file(chass_1)
     
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
        cons_out = anturlar.fos_cmd("setcontext %s " % target_fid)               ####   change to the fid given on the command 
        firmware_ver = anturlar.fos_cmd("firmwareshow")                          ####   send any command with anturlar.fos_cmd
        flow = anturlar.FlowV()
        date_is = get_time_stamp()
        header = "%s" % ("\nFlow Regression Log \n")              #### write a header line at top of file
        seperator  = "%s" % ("="*80)
        write_to_results_file("\r\n\r\n",ipaddr_switch,date_is)
        write_to_results_file(header,ipaddr_switch,date_is)
        write_to_results_file(ipaddr_switch,ipaddr_switch,date_is)
        write_to_results_file(firmware_ver,ipaddr_switch,date_is)
        write_to_results_file(seperator,ipaddr_switch,date_is)
        write_to_results_file(seperator,ipaddr_switch,date_is)
        #### get the list of flows on the switch
        flow_all_fport = flow.get_flow_details()
        ####  change the list to a string
        a = str(flow_all_fport)
        write_to_results_file(a,ipaddr_switch,date_is)
        
        liabhar.cls()
#######################################################################################################################
#######################################################################################################################
####
####
#######################################################################################################################
        cons_out = anturlar.fos_cmd("fosexec --fid all -cmd 'flow --deact all'")
        cons_out = anturlar.fos_cmd("flow --deact all")
        cons_out = anturlar.fos_cmd("echo y | flow --delete all -force")   #### remove all flows
        
        cons_out = anturlar.fos_cmd("flow --act sys_mon_all_fports")
        liabhar.JustSleep(360) 
        stats = flow.get_egr_stats("sys_mon_all_fports")        
        liabhar.JustSleep(120) 
     
        write_to_results_file(stats,ipaddr_switch,date_is)
        
        result = look_for_zero(stats)
        #### print the result to a file
        ####
        write_pass_fail_to_file(result,ipaddr_switch,date_is)
        print("@"*80)
        print("#"*80)
        print(result)
        print("#"*80)
        print("@"*80)
            
        cons_out = anturlar.fos_cmd("flow --deact all")
        
        #### find the SID DID pairs and create each monitor
        ####
        
        ras = re.compile('\|([0-9a-f]{1,4})\s+\|([0-9a-f]{6})\|([0-9a-f]{6})')
        ingr_sid_did_list = ras.findall(stats)      
        
        if pa.verbose:
            print("LIST OF FLOWS \n")
            print(stats)
            print("regex ")
            print(ingr_sid_did_list)
        
        name_number = 0
        for ingr_p, sid, did in ingr_sid_did_list:
            print(ingr_p)
            print(sid)
            print(did)
            print("\n")
        
            cons_out = anturlar.fos_cmd("flow --create regress_flow_a%s -fea mon -ingrport %s -srcdev %s -dstdev %s -noact " % (name_number,ingr_p,sid,did))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_b%s -fea mon  -ingrport %s -dstdev %s -noact  "           % (name_number,ingr_p,did))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_c%s -fea mon  -ingrport %s -srcdev %s -noact  "          % (name_number,ingr_p,sid))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_d%s -fea mon  -ingrport %s -srcdev '*' -dstdev %s -noact " % (name_number,ingr_p,did))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_e%s -fea mon  -ingrport %s -srcdev %s -dstdev '*' -noact " % (name_number,ingr_p,sid))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_f%s -fea mon  -egrport %s -srcdev %s -dstdev %s -noact " % (name_number,ingr_p,did,sid))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_g%s -fea mon  -egrport %s -srcdev %s  -noact "           % (name_number,ingr_p,did))
            cons_out = anturlar.fos_cmd("flow --create regress_flow_h%s -fea mon  -egrport %s -dstdev %s  -noact "            % (name_number,ingr_p,sid))
            
            
            name_number += 1 
        flow_all = flow.get_nondflt_flows()
        
        if pa.verbose:
            verb_list_print(flow_all)
        
            
        
        for f in flow_all:
            cons_out = anturlar.fos_cmd("flow --act %s " % f)
        
    
            #### get the current flow 
            #egrp_flow = flow.get_active_flows()
            #e = egrp_flow[0]
            liabhar.JustSleep(120) 
            stats = flow.get_egr_stats(f)
        
            liabhar.JustSleep(120) 
     
            write_to_results_file(stats,ipaddr_switch,date_is)
        
            result = look_for_zero(stats)
            #### print the result to a file
            ####
            write_pass_fail_to_file(result,ipaddr_switch,date_is)
            print("@"*80)
            print("#"*80)
            print(result)
            print("#"*80)
            print("@"*80)
            cons_out = anturlar.fos_cmd("flow --deact all")
        
        #### close the telnet session
        #############################
        anturlar.close_tel()                                                 ####  close the telnet session
    
    #liabhar.JustSleep(30) 
    return(True)

if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

