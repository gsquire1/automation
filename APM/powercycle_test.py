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


def user_start():
    go = False
    start = 'n'
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nSTART THE Power Cycle TEST ?  [y/n] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                sys.exit()
                
        if start == 'y':
            go = True
        else:
            sys.exit()
    return()
###############################################################################


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
    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    parser.add_argument("-d_on", "--delay_before_on", type=int, default=1800, help="the time delay after the power is turned off to the on command - default is 1800 seconds")
    parser.add_argument("-d_next", "--delay_before_next_off", type=int, default=1800, help="the time delay after the power is turned on to the next power off command - default is 1800 seconds")
    parser.add_argument("-n", "--count_power_cycles", type=int, default=50, help="the number of power cycles to perform - one cycle is off delay then turn on")
    
    args = parser.parse_args()
    print(args)
    
    if not args.chassis_name :
        print("Chassis Name is required")
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


def pwr_cycle(pwr_ip, pp, stage, db=10):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    
    anturlar.power_cmd("" ,10)
    anturlar.power_cmd("cli" ,10)
    anturlar.power_cmd("cd access/1\t/1\t%s" % pp ,10)
    #anturlar.power_cmd("show\r\n" ,10)
    
    anturlar.power_cmd(stage, 5)
    anturlar.power_cmd("yes", 5)
    
    #liabhar.JustSleep(10)
    anturlar.power_cmd("exit", 10)
     
    print("\r\n"*10)
    print("Just sent power pole  %s port %s   %s command " % (pp, stage,pwr_ip))
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
    reg_ex_list = [b"root> ", b"admin> "]
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
    #sw_set_pwd_timeout
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
 
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################   

 
    
def main():

    global tn
    
#######################################################################################################################
####
#### 
####
#######################################################################################################################
    pa = parse_args(sys.argv)
    #print(pa)
    print(pa.chassis_name)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    print(pa.delay_before_on)
    print(pa.delay_before_next_off)
    print(pa.count_power_cycles)

    print("@"*40)
 
###################################################################################################################
###################################################################################################################
####
#### get the info from the SwitchMatrix file using the Chassis Name
#### 
#### the only args required are  chassisname
####

    power_pole_info   = pwr_pole_info(pa.chassis_name)    

 
###################################################################################################################
###################################################################################################################
####
# #######################################################################################################################
# ####
# ####  
# ####
#######################################################################################################################
#######################################################################################################################
#### this step is the same for director or pizza box
####
####  turn each port off then turn each port on (otherwise the delay between did not power cycle the switch)
####
#######################################################################################################################
    
    liabhar.count_down(20)
    cycles = 0
    while cycles < pa.count_power_cycles:
        pass
    
        
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            #pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off" ,10)
            #time.sleep(4)
    
        try:
            for pp in range(0, len(power_pole_info), 2):
                print('POWERPOLE')
                print(power_pole_info[pp])
                print(power_pole_info[pp+1])
                pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off",10)
                time.sleep(4)
                liabhar.count_down(pa.delay_before_on)
                
            for pp in range(0, len(power_pole_info), 2):
                print('POWERPOLE')
                print(power_pole_info[pp])
                print(power_pole_info[pp+1])
                pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "on",10)
                time.sleep(4)
                
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
        
        cycles += 1
        print("power cycle    %s   of   %s" % (cycles, pa.count_power_cycles) )
        
        liabhar.JustSleep(6)
        liabhar.count_down(pa.delay_before_next_off)
#######################################################################################################################
#######################################################################################################################
#### 
####
####
#######################################################################################################################

     
    dt = liabhar.dateTimeStuff()
    date_is = dt.current()
    print(date_is)
    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

