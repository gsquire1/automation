#!/usr/bin/env python3

###############################################################################
####
####   Start Traffic
####
###############################################################################


###############################################################################
####   Import system modules here                                          ####
###############################################################################

import os,sys
import csv
import time
from multiprocessing import Process
sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
#sys.path.append('/home/automation/lib/FCR')
#sys.path.append('/home/automation/APM')
#sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')


###############################################################################
####   Import user modules here and set system paths                       ####
###############################################################################
import liabhar
import anturlar
#import cofra
###############################################################################
####   Import test case modules here                                       ####
###############################################################################

import traffic_tools

###############################################################################
####  Get the traffic info to start 
###############################################################################

def get_switch_info():
    
###############################################################################
#### read the csv file to get the switch info
####  return the ip, username and password 
###############################################################################
    server_list = []
    
    with open('ini/traffic.csv', newline='') as csvfile:
        traff_options = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        
        for row in traff_options:
            
            #print(i)
            #print("\nLine %s " % i)
            #print(', '.join(row))
            i += 1
            
            server_list.append(', '.join(row))
    return(server_list)
            
    




def main():
    
    
    
    #my_ip = "10.38.39.43"
    #user_name = "root"
    #psswd = "pass"

    this_platform = liabhar.platform()

    print("PLATFORM IS  :  %s  " % this_platform)

    traff_to_start = get_switch_info()
    print(traff_to_start)
    for s in traff_to_start:
        print("SERVER COMMANDS ")
        print(s)
        print(type(s))    
        t = s.split(',')
        print(t)
        serv_ip   = t[2]
        serv_usr  = t[3]
        serv_pwd  = t[4] 
        maim_pain = t[6]
        size      = t[7]
        cmd_options = ""
        if t[8]:  cmd_options = cmd_options + " -A" + t[8]
        if t[9]:  cmd_options = cmd_options + " -b" + t[9]
        if t[10]: cmd_options = cmd_options + " -B" + t[10]
        if t[11]: cmd_options = cmd_options + " -c" + t[11]
        if t[12]: cmd_options = cmd_options + " -C" + t[12]
        if t[13]: cmd_options = cmd_options + " -d" + t[13]
        if t[14]: cmd_options = cmd_options + " -D" + t[14]
        if t[15]: cmd_options = cmd_options + " -E" + t[15]
        if t[16]: cmd_options = cmd_options + " -g" + t[16]
        if t[17]: cmd_options = cmd_options + " -G" + t[17]
        if t[18]: cmd_options = cmd_options + " -i" + t[18]
        if t[19]: cmd_options = cmd_options + " -I" + t[19]
        if t[20]: cmd_options = cmd_options + " -j" + t[20]
        if t[21]: cmd_options = cmd_options + " -J" + t[21]
        if t[22]: cmd_options = cmd_options + " -l" + t[22]
        if t[23]: cmd_options = cmd_options + " -L" + t[23]
        if t[24]: cmd_options = cmd_options + " -m" + t[24]
        if t[25]: cmd_options = cmd_options + " -M" + t[25]
        if t[26]: cmd_options = cmd_options + " -n" 
        if t[27]: cmd_options = cmd_options + " -N" + t[27]
        if t[28]: cmd_options = cmd_options + " -o"
        if t[29]: cmd_options = cmd_options + " -O" + t[29]
        if t[30]: cmd_options = cmd_options + " -P" + t[30]
        if t[31]: cmd_options = cmd_options + " -q" + t[31]
        if t[32]: cmd_options = cmd_options + " -Q" + t[32]
        if t[33]: cmd_options = cmd_options + " --scsi" + t[33]
        if t[34]: cmd_options = cmd_options + " -r" + t[34]
        if t[35]: cmd_options = cmd_options + " -R" + t[35]
        if t[36]: cmd_options = cmd_options + " -s" + t[36]
        if t[37]: cmd_options = cmd_options + " -S" + t[37]
        if t[38]: cmd_options = cmd_options + " -t" + t[38]
        if t[39]: cmd_options = cmd_options + " -T" + t[39]
        if t[40]: cmd_options = cmd_options + " -u"
        if t[41]: cmd_options = cmd_options + " -U" + t[41]
        if t[42]: cmd_options = cmd_options + " -v" + t[42]
        if t[43]: cmd_options = cmd_options + " -V" + t[43]
        if t[44]: cmd_options = cmd_options + " -w" + t[44]
        if t[45]: cmd_options = cmd_options + " -W" + t[45]
        if t[46]: cmd_options = cmd_options + " -y" + t[46]
        if t[47]: cmd_options = cmd_options + " -Y" + t[47]
        if t[48]: cmd_options = cmd_options + " -%T" + t[48]
        
        strt_cmd = maim_pain + " " + size + cmd_options
    
        print("server info to connect with \n")
        print("IP address        :   %s " % serv_ip )
        print("User Name         :   %s " % serv_usr)
        print("Password          :   %s " % serv_pwd)
        print("MEDUSA Command    :   %s " % maim_pain) 
        print("Size              :   %s " % size)
        print("command Options   :   %s " % cmd_options)
        print("start command is  :   %s " % strt_cmd)
          
          

    ######################
    #### commenting out for debug purpose
    ####
    ####
        #if t[2] != "Username":
        #  traffic_tools.traff_get_port_list(serv_ip, serv_usr, serv_pwd, strt_cmd)
        
        print("\n\n\n\n\n\n\n\n\n\n")
        print(t[2])
        
        if t[2] != "Username":
            os_ver = anturlar.remote_os_ver(serv_ip,9)
    
            print("\n"*44)
            print(os_ver)
          
            
            p = Process(target=traffic_tools.traff_get_port_list, args=(serv_ip, serv_usr, serv_pwd, strt_cmd, os_ver))
            p.daemon = True
            p.start()
            #p.join()
            
            time.sleep(5.2)


    liabhar.count_down(300)



main()