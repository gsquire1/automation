#!/usr/bin/env python3


###############################################################################
#### Home location is
####
###############################################################################

import anturlar
import re


"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""


def traff_get_port_list(ip, user, pwd):
    
    
    #### add the variable pain_main in the command line
    ####  add option to be random traffic
    ####      random pattern    block size   etc
    ####      random drives    
    
    start_pain = "pain -t4 -r -b8k -o -u -n -l69 -q5 "
    start_pain = "pain -t8 -M60 -b8k -o -u -n -l69 -q5 "
    
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    print(type(ip))
    print(user)
    print(pwd)
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    db_level = 9
    remote_list = []
    
    anturlar.connect_tel_noparse(ip, user, pwd)
    cmdout = anturlar.traff_cmd("" , db_level )
    cmdout = anturlar.traff_cmd("cd /home/traffic" , db_level )
    
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
    
    cmdout = anturlar.fos_cmd_regex(start_pain_sd , "([\w\d]+)")
    
    cmdout = anturlar.traff_output()
    
    
    anturlar.close_tel()
    
    
    
    
    
    
    
    
