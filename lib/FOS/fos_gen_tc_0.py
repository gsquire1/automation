#!/usr/bin/env python3


###############################################################################
###############################################################################
####
#### HOME location is home/automation/lib/FOS/fos_gen_tc.py
####
####  this file holds the test cases that are not necessarily specific to
####   one area of FOS - ie mostly generic test cases
####
###############################################################################

import anturlar
import liabhar
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



def show_vc(slot, port ):
    """
        function to show which VC is in use
                
    """
    cons_out = anturlar.fos_cmd("")
    cmd_create = ("portregshow %s/%s | grep trc" %(slot, port))   
    
    cons_out = anturlar.fos_cmd(cmd_create)
         
    ras = re.compile('(\d)(?= )') 
    ras = ras.findall(cons_out)
    ras = [int(i) for i in ras]
    ras_previous = ras
    vc_list = []
    while True:
        
        cons_out = anturlar.fos_cmd(cmd_create)
         
        ras = re.compile('(\d)(?= )') 
        ras = ras.findall(cons_out)
        ras = [int(i) for i in ras]
        #### 
        pairwise = zip(ras, ras_previous)
        vc_list = [i for i, pair in enumerate(pairwise) if pair[0] != pair[1]]
               
        print("\n"*5,"=======","\nVC LIST")
        print(vc_list)
        ras_previous = ras
        vc_list = []
        liabhar.JustSleep(3)
        
    
    
def send_cmds(filename , loops = 1):
    """
        function to read cmds from a file and send them to the switch
        
    """
    
    fullpath = "%s%s" % ("logs/configs/cmdset/", "send_cmd_output.txt")
    g = liabhar.FileStuff(fullpath, 'w+b')
    #f = liabhar.FileStuff(filename, 'r+b')
    cons_out = anturlar.fos_cmd("")
        
    with open(filename) as fileio:
        info = fileio.readlines()
    
    while loops >=1 :    
        for line in info:
            line = line.rstrip('\n')
            cons_out = anturlar.fos_cmd(line)
            g.write(cons_out)
            g.write(" ")
            
        loops -= 1
    
    
    g.close()
    return 0
     

     
def ha_failover_check_maps_flow_ras_porterrs(times=1):
    """
        ha failover
        
        
    """
    ####    use cofra.hafailover to do the failover
    ####       pass the number of times to repeat before checking stats
    ####        
    ####
    ####
    cofra.ha_failover(times)
    maps_tools.
    
    
     
     
     
