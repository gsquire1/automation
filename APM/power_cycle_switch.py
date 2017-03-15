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

def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp 

def parse_args(args):
    
    verb_value = "99"
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    
    args = parser.parse_args()
    print(args)
    
    if not args.chassis_name and not args.ipaddr:
        print("Chassis Name or IP address is required")
        sys.exit()

    return parser.parse_args()
    
#    return(capture)

def pwr_cycle(pwr_ip, pp, stage, db=0):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    anturlar.power_cmd("cli", 10)
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
#    return usrname

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
     
 
def pwr_cycle_fabric():
    """
         Power Cycle each switch that is listed in the SwitchMatrix.csv file
         this is done sequencially from top to bottom of the file
         
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
             
        power_pole_info   = pwr_pole_info(chassis_name_from_file)    
        
        print("@"*30)
        print("power cycle    with  power pole info  ")
        print(chassis_name_from_file)
        print(power_pole_info)
        print("\r\n"*2)
        cons_out = power_cycle(power_pole_info)
        
    return()
   
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################   

 
    
def main():

    global tn
    
#######################################################################################################################
####
####   Parse the command line indo
####
#######################################################################################################################
    pa = parse_args(sys.argv)
    print(pa)
    #print(pa.chassis_name)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    #print(pa.firmware)
    #print(pa.cmdprompt)
    print("@"*40)
    
#######################################################################################################################
#######################################################################################################################
####                                                                                                               ####
#### if user enter ip address then get the chassisname from the   SwitchMatrix file                                ####
####     then get the info from the SwitchMatrix file using the Chassis Name                                       ####
####                                                                                                               ####
#### If the fabric is selected power cycle all of the switches in the SwitchMatrix.csv file                        ####
####                                                                                                               ####
#######################################################################################################################
#######################################################################################################################

    if pa.fabwide:
        print("power cycle all of the switches in SwitchMatrix File")
        pwr_cycle_fabric()
          
    else:
        if pa.ipaddr:
            print("do IP steps")
            pa.chassis_name = console_info_from_ip(pa.ipaddr)
        cons_info         = console_info(pa.chassis_name)
        power_pole_info   = pwr_pole_info(pa.chassis_name)    
        cons_out = power_cycle(power_pole_info)
        
    dt = liabhar.dateTimeStuff()
    date_is = dt.current()
    print(date_is)
    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

