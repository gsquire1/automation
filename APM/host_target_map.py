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
    #parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    #parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    #parser.add_argument('-cp',   '--cmdprompt', help="switch is already at command prompt")
    #parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
    ##parser.add_argument('-s', '--suite', type=str, help="Suite file name")
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
    print("@"*40)
    print("@"*40)
#######################################################################################################################
#######################################################################################################################
####
#######################################################################################################################
########################################################################################################################
    ####
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    ####
    print("\n\n  ip address     chassisname        username       password   " )
    for line in csv_file:
        ipaddr_switch         = (line['IP Address'])
        swtch_name            = (line['Chassisname'])
        user_name             = (line['Username'])
        usr_psswd             = (line['Password'])
        print("   %s        %s        %s        %s " % (ipaddr_switch, swtch_name,user_name, usr_psswd) )
 
        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
        cons_out = anturlar.fos_cmd("firmwareshow")                       ####   send any command with anturlar.fos_cmd
        ht = anturlar.SwitchInfo()
        ls_numbs  =  ht.ls()
        ####
        str1 = ''.join(ls_numbs)
        ls_numbs_str  = ' '.join(str(e) for e in ls_numbs)
        dt = liabhar.dateTimeStuff()                                  #### create the object for date and time stuff
        port_list = []
        date_is = dt.current_no_dash_at_end()  
        f = "%s%s%s"%("logs/Host_target_file",ipaddr_switch,".txt")
        ff = liabhar.FileStuff(f, 'a+b')                                    #### open the log file for writing       
        header = "%s%s%s%s%s%s%s" % ("\n HOST  TARGET  CAPTURE FILE \n"," ",date_is,"\n ipaddress:  ",\
                                     " ",ipaddr_switch,"\n ==================================\n")
        #### write a header line at top of file
        ff.write(header)
        ff.write("\n")
        ff.write("LS NUMBERS   ")
        ff.write(ls_numbs_str)

        for l in ls_numbs:
            port_list_str = ""
            nsoutput = anturlar.fos_cmd("setcontext %s " % l)
            reg_wwn = [b'.?;([:0-9a-f]{23,23})']
            nsoutput = anturlar.fos_cmd("nsshow")
            ras = re.compile('Permanent Port Name: ([:0-9a-f]{23,23})')
            port_list = ras.findall(nsoutput)

            #port_list_str  = ' '.join(str(e) for e in port_list)
            #cons_out = anturlar.fos_cmd("setcontext %s " % pa.fid)  
            ff.write("\n")
            ff.write("LS   %s   PORTS \n" % l)
            ff.write("PORT WWN   \n")
            for p in port_list:
                wwn_zone  = anturlar.fos_cmd("nszoneshow -wwn %s " % p , 0)
                ras = re.compile('\s{2}([-_a-zA-Z0-9]+)(?=\r\n)')
                zones = ras.findall(wwn_zone)
                
                print("\n")
                print("$"*80)
                print("$"*80)
                
                print(zones)
                for z in zones:
                    print(z)
                    zone_cfg_members  = anturlar.fos_cmd("zoneshow %s " % z , 0)
                    ras = re.compile('([:0-9a-f]{23})')
                    wwn_zoned_with  = ras.findall(zone_cfg_members)
                    print(wwn_zoned_with)
                    
                print("$"*80)
                print("$"*80)
                print("$"*80)
                ff.write(p)
                ff.write("\n=============================")
                ff.write("\n\t\t\t")
                
                for z in zones:
                    ff.write(z)
                    ff.write("; ")
                    zone_cfg_members  = anturlar.fos_cmd("zoneshow %s " % z , 0)
                    ras = re.compile('([:0-9a-f]{23})')
                    wwn_zoned_with  = ras.findall(zone_cfg_members)
                    ff.write("(")
                    do_semi = False
                    for w in wwn_zoned_with:
                        if p != w:
                            ff.write(w)
                            if do_semi:
                                ff.write("; ")
                            else:
                                do_semi = True
                            
                    ff.write(")")
                    ff.write("\n\t\t\t")
                ff.write("\n")
            #ff.write(port_list_str)
            ff.write("\n")
        
        ff.close()                                                          #### close this file for comparison later
        
        anturlar.close_tel()                                                 ####  close the telnet session



if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

