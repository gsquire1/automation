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
import sys
import cofra

import flow_tools
import maps_tools

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
     

def ha_failover_check_frame_log(times=1):
    """
    
    """
    
    
    sw_info = anturlar.SwitchInfo()
    #fid_now = sw_info.ls_now()
    ip_addr = sw_info.ipaddress()
    go_or_not = sw_info.synchronized()
    cons_out = anturlar.fos_cmd(" ")
    username = 'root'
    pwrd = 'password'
    #counter = 1
    new_connect = True
  
    liabhar.count_down(10)
    
 
            
    while times > 0:
        cofra.ha_failover(1)
        
        print("\n\n\n")
        print("@"*60)
        print("HA Failovers remaining -- %s " % times)
        print("@"*60)
        anturlar.connect_tel_noparse(ip_addr,'root','password')

    
        times -= 1
    
        flog_status = maps_tools.frameview_status()
        print("$"*80)
        print("$"*80)
        print(flog_status)
        print("$"*80)
        print("$"*80)
        
        if 'Enabled' in flog_status:
            print("Framelog is Enabled")
        elif 'Disabled' in flog_status:
            print("Framelog is Disabled")
            sys.exit()
        else:
            print("Framelog State is UnKnown")
        
        
        
        
    
    return(flog_status)
    
     
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
    ff.write("#############################################################\r\n")
    ff.write("#############################################################\r\n")
    ff.write("\r\n")
    for ip in fab_ip_list:
        ff.write(ip)
        ff.write("\r\n")
    ff.write("#############################################################\r\n")
    ff.write("#############################################################\r\n")
    ff.write("#############################################################\r\n")
    ff.write("#############################################################\r\n\r\n\r\n")
    ff.close()
    
    
    fabric_data = []
    for ip in fab_ip_list:
        tnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
        
        m_info          = anturlar.Maps()
        f_info          = anturlar.FlowV()
        maps_config     = anturlar.fos_cmd("mapsconfig --show")
        firmware_ver    = check_version()
        s_name          = m_info.switch_name()
        s_type          = m_info.switch_type()
        ls_list         = m_info.ls()
        switch_id       = m_info.switch_id()
        ls_domain       = m_info.ls_and_domain()
        chass_name      = m_info.chassisname()
        vf_state        = m_info.vf_enabled()
        non_dflt_policy = m_info.get_nondflt_policies()
        flow_names      = f_info.flow_names()
        flow_cnfg       = f_info.flow_config()
        
        
        anturlar.close_tel()
####
####  leave as capturing data for only one FID at a time
####   
        ff = liabhar.FileStuff(fname, 'a+b')
        seperator(ff, ip)
        ff.write("Switch ipv4         :    %s \r\n" % ip)
        ff.write("Chassis Name        :    %s \r\n" % chass_name)
        ff.write("Firmware version    :    %s \r\n" % firmware_ver)
        ff.write("Switch Name         :    %s \r\n" % s_name)
        ff.write("Switch Type         :    %s \r\n" % s_type)
        ff.write("VF State            :    %s \r\n" % vf_state)
        ff.write("Logical Switches    :    %s \r\n" % ls_list)
        ff.write("Switch ID           :    %s \r\n" % switch_id)
        ff.write("ls and domain       :    %s \r\n" % ls_domain)
        ff.write("MAPS config         :    %s \r\n" % maps_config)
        ff.write("MAPS Policy         :    %s \r\n" % non_dflt_policy)
        ff.write("FLOW Names list     :    %s \r\n" % flow_names)
        ff.write("FLOW CONFIG         :    %s \r\n" % flow_cnfg)

        
        
        
    return(True)
    

def seperator(f, name = ""):
    """
       print a few lines of special characters to seperate field in the output
       
    """ 
    #f.write("\r\n\r\n")
    f.write("@"*120 + "\r\n\r\n")
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n@@@@@@@@@@@@@@@@@@@@@@@        STARTING SWITCH INFO FOR   %s  \r\n" % name )
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n\r\n")
    
    
    
    return()
    
    
def check_version():
         
    capture_cmd = anturlar.fos_cmd("version")
    capture_cmd_dir = capture_cmd
    
    
    ras = re.compile('Fabric OS:\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
    ras = re.compile('Fabric\s+OS:\s+([\.\\s_a-z0-9]{6,24})(?:\\r\\n)')
    
    
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
    try:
        f = ras[0]
    except:
        f= "FOS unknown in check_version in fos_gen_tc_0 "
    #try:
    #    if ras_dir.group(0) != "none":
    #        f=ras_dir.group(1)
    #except:
    #    pass
    #
    
    return(f)
    
    
    
    
    
    
    
    