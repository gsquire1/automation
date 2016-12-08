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
    
def switch_config_show():
    """
      get information for a switch for each FID
      
      
      
    """
    
    cons_out = anturlar.fos_cmd("")
    swtch = anturlar.SwitchInfo()
    fab = anturlar.FabricInfo()
    #fab_ip_list = fab.ipv4_list()
    ip = swtch.ipaddress()
    this_fid = swtch.currentFID()
    
    fname = "%s%s" % ("logs/Switch_info_per_FID_" ,".txt")  #### %s string  %d number
    ff = liabhar.FileStuff(fname, 'w+b')
    ff.write("#############################################################\r\n")
    ff.close()
    
    tnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
    ff = liabhar.FileStuff(fname, 'a+b')
    
    ls_list_fids = swtch.ls()
    m_info              = anturlar.Maps()
    f_info              = anturlar.FlowV()
    firmware_ver        = check_version()
    
    s_type              = m_info.switch_type()
    ls_list             = m_info.ls()
    switch_id           = m_info.switch_id()
    ls_domain           = m_info.ls_and_domain()
    chass_name          = m_info.chassisname()
    vf_state            = m_info.vf_enabled()
    
    ff.write("Switch ipv4              :    %s \r\n" % ip)
    ff.write("Chassis Name             :    %s \r\n" % chass_name)
    ff.write("Firmware version         :    %s \r\n" % firmware_ver)
    #ff.write("Switch Name              :    %s \r\n" % s_name)
    ff.write("Switch Type              :    %s \r\n" % s_type)
    ff.write("VF State                 :    %s \r\n" % vf_state)
    ff.write("Logical Switches         :    %s \r\n" % ls_list)
    ff.write("Switch ID                :    %s \r\n" % switch_id)
    ff.write("ls and domain            :    %s \r\n" % ls_domain)
    
    print(ls_list_fids)
    for i in ls_list_fids:
        print(i)
 
    
    
    print("\n"*10)
    for ls in ls_list_fids:

        cons_out = anturlar.fos_cmd("setcontext %s " % ls)
        s_name              = m_info.switch_name()
        maps_policy_list    = m_info.get_policies()
        maps_active_policy  = m_info.get_active_policy()
        non_dflt_policy     = m_info.get_nondflt_policies()
        flow_names          = f_info.flow_names()
        flows_nondflt       = f_info.get_nondflt_flows()
        flows_active        = f_info.get_active_flows()
        #flow_cnfg           = f_info.flow_config()
        maps_config         = anturlar.fos_cmd("mapsconfig --show")          
        #######
        #######  remove line switchname FID ?? root> 
        #######
        print("\n"*4)
        print(maps_config)
        print("\n"*4)
        m_no_root = s_name + ":FID" + str(ls) + ":root>"
        #m_no_name = maps_config.replace(s_name ,'')
        #m_no_fid = m_no_name.replace(str(this_fid), '')
        m = maps_config.replace(m_no_root, '')
        print("\n"*4)
        print(m)
        print("\n"*4)
        #######
        #######  remove line switchname FID ?? root> 
        #######

        seperator_switch(ff, ls)
        ff.write("Switch Name              :    %s \r\n" % s_name)
        ff.write("---------------------------------------------------------------------\r\n")
        #ff.write("MAPS config         :    %s \r\n" % maps_config)
        ff.write("MAPS config              :   \r\n\r\n  %s \r\n" % m)   ## maps config
        ff.write("---------------------------------------------------------------------\r\n")       
        ff.write("MAPS Policy List         :    %s \r\n" % maps_policy_list)
        ff.write("MAPS Active Policy       :    %s \r\n" % maps_active_policy)
        ff.write("MAPS Non Default Policy  :    %s \r\n" % non_dflt_policy)
        ff.write("---------------------------------------------------------------------\r\n")
        ff.write("FLOW Names list          :    %s \r\n" % flow_names)
        ff.write("FLOW non dflt Flows      :    %s \r\n" % flows_nondflt)
        ff.write("FLOWs Active             :    %s \r\n" % flows_active)
        ff.write("---------------------------------------------------------------------\r\n")
        
    ff.close()
    anturlar.close_tel()
            

    
    
def fabric_switch_config_show():
    
    """
       document how this works here 
       
       1. Retreive a list of all of the switches in the FID passed during start
       2. get Flow and MAPS basic setup information
       
       
       
    """
    
    cons_out = anturlar.fos_cmd("")
    swtch = anturlar.SwitchInfo()
    fab = anturlar.FabricInfo()
    fab_ip_list = fab.ipv4_list()
    this_fid = swtch.currentFID()
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
    
    #ff = liabhar.FileStuff(fname, 'a+b')
    #for ip in fab_ip_list:
    #    tnnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
    #    firmware_ver = check_version()
    #    
    #    ip_firm_ver_pair = "%s      %s" % ( ip,firmware_ver)
    # 
    #    ff.write("\r\n")
    #    ff.write(ip_firm_ver_pair)
    #
    #ff.write("\r\n")
    #ff.write("#############################################################\r\n")
    #ff.write("#############################################################\r\n")
    #ff.write("#############################################################\r\n")
    #ff.write("#############################################################\r\n")
    #ff.write("#############################################################\r\n")
    #ff.close()
    m_info              = anturlar.Maps()
    f_info              = anturlar.FlowV()
    maps_config         = anturlar.fos_cmd("mapsconfig --show")
    firmware_ver        = check_version()
    s_name              = m_info.switch_name()
    s_type              = m_info.switch_type()
    ls_list             = m_info.ls()
    switch_id           = m_info.switch_id()
    ls_domain           = m_info.ls_and_domain()
    chass_name          = m_info.chassisname()
    vf_state            = m_info.vf_enabled()
    
    ff = liabhar.FileStuff(fname, 'a+b')
    ff.write("Switch ipv4              :    %s \r\n" % ip)
    ff.write("Chassis Name             :    %s \r\n" % chass_name)
    ff.write("Firmware version         :    %s \r\n" % firmware_ver)
    ff.write("Switch Name              :    %s \r\n" % s_name)
    ff.write("Switch Type              :    %s \r\n" % s_type)
    ff.write("VF State                 :    %s \r\n" % vf_state)
    ff.write("Logical Switches         :    %s \r\n" % ls_list)
    ff.write("Switch ID                :    %s \r\n" % switch_id)
    ff.write("ls and domain            :    %s \r\n" % ls_domain)
    
    
    for ip in fab_ip_list:
        tnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
        cons_out = anturlar.fos_cmd("setcontext %s " % this_fid)
        maps_policy_list    = m_info.get_policies()
        maps_active_policy  = m_info.get_active_policy()
        non_dflt_policy     = m_info.get_nondflt_policies()
        flow_names          = f_info.flow_names()
        flows_nondflt       = f_info.get_nondflt_flows()
        flows_active        = f_info.get_active_flows()
        #flow_cnfg           = f_info.flow_config()
        
        
        anturlar.close_tel()
        
        
        
                
        #######
        #######  remove line switchname FID ?? root> 
        #######
        print("\n"*4)
        print(maps_config)
        print("\n"*4)
        m_no_root = s_name + ":FID" + str(this_fid) + ":root>"
        #m_no_name = maps_config.replace(s_name ,'')
        #m_no_fid = m_no_name.replace(str(this_fid), '')
        m = maps_config.replace(m_no_root, '')
        print("\n"*4)
        print(m)
        print("\n"*4)
        #######
        #######  remove line switchname FID ?? root> 
        #######
        
####
####  leave as capturing data for only one FID at a time
####  have a switch for all fid data
####
####

        seperator(ff, ip)

        ff.write("---------------------------------------------------------------------\r\n")
        #ff.write("MAPS config         :    %s \r\n" % maps_config)
        ff.write("MAPS config              :   \r\n  %s \r\n" % m)   ## maps config
        ff.write("---------------------------------------------------------------------\r\n")       
        ff.write("MAPS Policy List         :    %s \r\n" % maps_policy_list)
        ff.write("MAPS Active Policy       :    %s \r\n" % maps_active_policy)
        ff.write("MAPS Non Default Policy  :    %s \r\n" % non_dflt_policy)
        ff.write("---------------------------------------------------------------------\r\n")
        ff.write("FLOW Names list          :    %s \r\n" % flow_names)
        ff.write("FLOW non dflt Flows      :    %s \r\n" % flows_nondflt)
        ff.write("FLOWs Active             :    %s \r\n" % flows_active)
        ff.write("---------------------------------------------------------------------\r\n")
        
        #ff.write("FLOW CONFIG         :   \r\n   %s \r\n" % flow_cnfg)
  
    
    ff = liabhar.FileStuff(fname, 'a+b')
    ff.write("#####################################################################\r\n")
    ff.write("#####################################################################\r\n")
    ff.write("##########\r\n")
    ff.write("##########     FABRIC SWITCHES INFO                        ##########\r\n")
    ff.write("##########\r\n")
    ff.write("#####################################################################\r\n")
    #for ip in fab_ip_list:
    #    tnnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
    #    firmware_ver = check_version()
    #    m_info          = anturlar.Maps()
    #    chass_name      = m_info.chassisname()
    #    
    #    ip_firm_ver_pair = "%s\t\t%s\t\t%s " % ( ip,chass_name,firmware_ver)
    # 
    #    ff.write("\r\n")
    #    ff.write(ip_firm_ver_pair)
    #
    #ff.write("\n"*5)
        
    for ip in fab_ip_list:
        tnnn = anturlar.connect_tel_noparse(ip, 'root', 'password')
        firmware_ver = check_version()
        m_info          = anturlar.Maps()
        chass_name      = m_info.chassisname()
        sf = "{0:18}   {1:25}   {2:25}"
        print(sf.format( str(ip), str(chass_name), str(firmware_ver) ), file=ff)
        
    ff.write("\r\n")
    ff.write("#####################################################################\r\n")
    ff.write("#####################################################################\r\n")
    ff.write("#####################################################################\r\n")
    ff.write("#####################################################################\r\n")
    ff.write("#####################################################################\r\n")
    ff.close()
    
    return(True)
    

def seperator(f, name = ""):
    """
       print a few lines of special characters to seperate field in the output
       
    """ 
    #f.write("\r\n\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*25)
    f.write("\r\n@@@@@@@@@@@@@@@@@@@@@@@@@        STARTING SWITCH INFO FOR   %s  \r\n" % name )
    f.write("@"*25)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n\r\n")
    
    
    
    return()
    
    
def seperator_switch(f, name = ""):
    """
       print a few lines of special characters to seperate field in the output
       
    """ 
    #f.write("\r\n\r\n")
     
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*120)
    f.write("\r\n")
    f.write("@"*25)
    f.write("\r\n@@@@@@@@@@@@@@@@@@@@@@@@@        STARTING SWITCH INFO FOR FID  %s  \r\n" % name )
    f.write("@"*25)
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
    ras = re.compile('[Fabric OS|FOS AMPOS]:\s+([\.\\s_a-zA-Z0-9]{6,24})(?:\\r\\n)')
    
    
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
    
    
    
    
    
    
    
    