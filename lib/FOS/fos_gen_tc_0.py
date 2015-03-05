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

import flow_tools
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
    pass
    
    
     
     
     
def start_all_SIM_flows():
    
    """
        document how this works here
    
    """
    
    flow_tools.flow_to_each_SIM()
    
    
def fabric_switch_config_show():
    
    """
       document how this works here
    
    """
    
    cons_out = anturlar.fos_cmd("")
    fab = anturlar.FabricInfo()
    fab_ip_list = fab.ipv4_list()
    fname = "%s%s" % ("logs/fabric_info_switch" ,".txt")  #### %s string  %d number
    ff = liabhar.FileStuff(fname, 'w+b')
    ff.close()
    
    
    fabric_data = []
    for ip in fab_ip_list:
        tnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
        
        m_info = anturlar.Maps()
        f_info = anturlar.FlowV()
        maps_config = anturlar.fos_cmd("mapsconfig --show")
        firmware_ver = check_version()
        s_name = m_info.switch_name()
        s_type = m_info.switch_type()
        
        
        anturlar.close_tel()

        ff = liabhar.FileStuff(fname, 'a+b')
        ff.write("+"*80)
        ff.write("+"*80)
        ff.write("\r\n")
        ff.write("Switch ipv4         :    %s \r\n" % ip)
        ff.write("Firmware version    :    %s \r\n" % firmware_ver)
        ff.write("Switch Name         :    %s \r\n" % s_name)
        ff.write("Switch Type         :    %s \r\n" % s_type)
    
    
    
    
def check_version():
         
    capture_cmd = anturlar.fos_cmd("version")
    capture_cmd_dir = capture_cmd
    
    
    ras = re.compile('Fabric OS:\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
    ras = re.compile('Fabric\s+OS:\s+([\.\\s_a-z0-9]{6,18})(?:\\r\\n)')
    
    
    #ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
    #ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
    #ras_dir = re.compile('[\s\t0-9CPFOS]{19,21}\s+([\._a-z0-9]{6,18})\s+\w+\\r\\n\s+([\._a-z0-9]{6,18})')
    #ras_dir = re.compile('[ \\t0-9CPFOS]{19,21}')
    #ras = ras.search(capture_cmd)
    ras = ras.findall(capture_cmd)
    #ras_dir = ras_dir.search(capture_cmd_dir)
    #
    f=""
    
    try:
        if ras.group(0) != "none":
            f= ras.group(1)
    except:
        pass
    
    f = ras[0]
    #try:
    #    if ras_dir.group(0) != "none":
    #        f=ras_dir.group(1)
    #except:
    #    pass
    #
    
    return(f)
    
    
    
    
    
    
    
    