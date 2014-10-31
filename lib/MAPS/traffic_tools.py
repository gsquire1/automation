#!/usr/bin/env python3


###############################################################################
#### Home location is
####
###############################################################################

import anturlar
import re
import liabhar

"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""

def bcu_version():
    
    ###########################################################################
    ####
    ####
    ####
    db_level = 9
    ras = re.compile('\s\d\s+\d\s+([:\d\w]{5,10})')
    
    cmdout = anturlar.traff_cmd("bcu adapter --list", db_level)
    ad = ras.findall(cmdout)
    ad_one = ad[0]
    print("\n\n\n\n\n\n\n\n\n\n")
    print(ad_one)
    
    
    ras = re.compile('\s+fw version:\s+([\.\d\w]{7})')
    cmdout = anturlar.traff_cmd("bcu adapter --query %s " % ad_one)
    ras = ras.findall(cmdout)
    
    return(ras)
    
    
    
    

def traff_get_port_list(ip, user, pwd, start_command, os_ver):
    
    
    #### add the variable pain_main in the command line
    ####  add option to be random traffic
    ####      random pattern    block size   etc
    ####      random drives    
    
    start_pain = "pain -t4 -r -b8k -o -u -n -l69 -q5 "
    start_pain = "pain -t8 -M60 -b8k -o -u -n -l69 -q5 "
    start_pain = start_command
    
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    print(type(ip))
    print(user)
    print(pwd)
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    db_level = 9
    remote_list = []
    
    anturlar.connect_tel_noparse_traffic(ip, user, pwd)
    cmdout = anturlar.traff_cmd("" , db_level )
    cmdout = anturlar.traff_cmd("cd /home/traffic" , db_level )
    
    this_platform = os_ver
    #this_platform = liabhar.platform()
    this_bcu_version = bcu_version()
    
    print("\n\nPLATFORM IS        :   %s  " % this_platform)
    print("ADAPTER HW-PATH    :   %s  " % this_bcu_version)
    
    
    sys.exit()
    ####  windows style
    ####  windows with 3.2 driver
    ####
    #### linux style
    #### linux style with 3.2 driver
    ####
    #### add the other type of os version to the remote os ver function
    
    
    for i in [1,2,3,4]:
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/0" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu rport --osname %s/0" % i , db_level )
        ras = re.compile('/dev/sd([a-z]+)')
        ras = ras.findall(cmdout)
        remote_list = remote_list + ras
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/1" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu rport --osname %s/1" % i , db_level )
        ras = re.compile('/dev/sd([a-z]+)')
        ras = ras.findall(cmdout)
        remote_list = remote_list + ras
    
    print("remote port list  :  %s  " % remote_list )
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    ####  put the list is the correct syntax
    new_list = ",".join(remote_list)
        
    print("NEW LIST IS   :   %s " % new_list)
    
    #### combine the command with the drive list
    start_pain_sd = start_pain + ' -f"/dev/sd;%s"' % new_list
    print("NEWEST COMMAND  %s   " % start_pain_sd)
    reg_list = [b'([\w\d]+)']
    cmdout = anturlar.fos_cmd_regex(start_pain_sd , reg_list)
    
    cmdout = anturlar.traff_output()
    
    
    anturlar.close_tel()
    
    
    
    
    
    
    
    
