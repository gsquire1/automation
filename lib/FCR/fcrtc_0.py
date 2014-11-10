#!/opt/python3/bin/python3

###############################################################################
#### Home location is
####
###############################################################################
"""
FCR 1st Test Case Module
"""

import anturlar, liabhar, cofra
import re, sys, os, csv
import fcr_tools

"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""
def fcr_state_persist_enabled():
    #print(sys.argv)
    host = (sys.argv[1])
    user = sys.argv[2]
    password = sys.argv[7]
    test_file = '/home/RunFromHere/ini/SwitchMatrix.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    fcr_state = fcr_tools.switch_status()
    state = fcr_state['fcr_enabled']
    if state is True:
        anturlar.fos_cmd("switchdisable")
        liabhar.JustSleep(10)
        enabled = fcr_tools.switch_status()
        if enabled['fcr_enabled'] is True:
            anturlar.fos_cmd("switchenable")
            liabhar.JustSleep(10)
            print("\n\nENABLE/DISABLE TEST PASSED")
        else:
            pass
    else:
        print("\n\nENABLE/DISABLE TEST FAILED")
        print("Please enable fcr for this test and try again")
        sys.exit(0)
    print('Sleeping: 10')
    liabhar.JustSleep(10)
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    a = cofra.switch_power_off_on(cn, 'off')
    print('Sleeping: 20')
    liabhar.JustSleep(20)
    a = cofra.switch_power_off_on(cn, 'on')
    print('Sleeping: 120')
    liabhar.JustSleep(120)
    anturlar.connect_tel_noparse(host, user, password)
    si = anturlar.SwitchInfo()
    print("GETTINGFCRSTATE")
    fcr_state = fcr_tools.switch_status()
    state = fcr_state['fcr_enabled']
    if state is True:
        print('Reboot Complete. FCR State remains consistent')
        print('TEST PASSED')
    else:
        print('FCR State changed.')
        print('TEST FAILED')
        
def fcr_state_persist_disabled():
    host = (sys.argv[1])
    user = sys.argv[2]
    password = sys.argv[7]
    test_file = '/home/RunFromHere/ini/SwitchMatrix.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    fcr_state = fcr_tools.switch_status()
    state = fcr_state['fcr_enabled']
    if state is False: #the same to here disabled is false, enabled is true
        anturlar.fos_cmd("switchdisable")
        liabhar.JustSleep(10)
        enabled = fcr_tools.switch_status()
        if enabled['fcr_enabled'] is False:
            anturlar.fos_cmd("switchenable")
            liabhar.JustSleep(10)
            print("\n\nENABLE/DISABLE TEST PASSED")
        else:
            pass
    else:
        print("\n\nENABLE/DISABLE TEST FAILED")
        print("Please disable fcr for this test and try again")
        sys.exit(0)
    print('Sleeping: 10')
    liabhar.JustSleep(10)
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    a = cofra.switch_power_off_on(cn, 'off')
    print('Sleeping: 20')
    liabhar.JustSleep(20)
    a = cofra.switch_power_off_on(cn, 'on')
    print('Sleeping: 120')
    liabhar.JustSleep(120)
    anturlar.connect_tel_noparse(host, user, password)
    fcr_state = fcr_tools.switch_status()
    state = fcr_state['fcr_enabled']
    if state is False:
        print('Reboot Complete. FCR State remains consistent')
        print('TEST PASSED')
    else:
        print('FCR State changed.')
        print('TEST FAILED')

    sys.exit(0)#######################

def ex_deconfig():
    fcri = anturlar.FcrInfo()
    test = fcri.ex_deconfig()
    print('\n\nAll EX_ports found are now deconfigured.')
  
def test_anturlar_functions():
    fcri = anturlar.FcipInfo()
    a = fcri.all_ge_ports()
    print(a)
    sys.exit(0)

def slotpower_off_on_check_devices():
    si = anturlar.SwitchInfo()
    fcrc = anturlar.FcrInfo()
    fi = anturlar.FcipInfo()
    
    ip_address = fcr_tools.all_switches_in_bb_ip()
    switch_info = fcr_tools.bb_fabric_switch_status()
    #blades = si.blades()
    #ex_ports = si.ex_ports()
    b = (len(switch_info))
    print("The number of switches in backbone is:", b)
    print('\n\n\n')
    print('IP addresses of all switches in Backbone:')
    print(ip_address)
    print('\n\n\n')
    for i in ip_address:
        print(i)
        anturlar.connect_tel_noparse(i,'root','password')
        a = si.ex_ports()
        print(a)
        sys.exit(0)
        ex_port = a.append(a)
        print('EXPORTSEXPORTS')
        print(ex_port)
    #print(switch_info) ##### Status on switches in BB fabric (ip, name, vf_enabled, fcr_enabled, base, chassis).
    #print('\n\n\n')

def Dictionary_Example():
    switch_info = fcr_tools.bb_fabric_switch_status()
    b = (len(switch_info))
    print("The number of switches in backbone is:", b)
    print(switch_info)
    #switch_dict = switch_info[3]
    #print(switch_dict)
    sys.exit(0)#################
    z = switch_dict['switch_name']
    #print(type(z))
    print(z)
    sortedkeys = switch_dict.keys()
    print(sortedkeys)
    #for key, value in sorted(switch_dict.items()):
    for value in sorted(switch_dict.items()):
        print(value)

    sys.exit(0)###############
    
    for i in switch_info:
        items = i.items()
        print('ITEMS')
        print(items)
    print("*"*20)
    for i in switch_info:
        keys = (i.keys())
        print('KEYS')
        print(keys)
    print("*"*20)
    for i in switch_info:
        values = i.values()
        print('VALUES')
        print(values)
              
def change_fid(fid):
    """
        change a fid on a switch
    """
    cons_out = anturlar.fos_cmd("setcontext %s" % fid)
    
def test_case_flow():
    """
        get the current flows on the SUT
        remove the flows
        create the same flows
        
    """
    pass

def test_case_config():
    """
        Get some information from the switch so config can be
        put back to the switch
    """
    
    pass

def genAll():
    """
    turn all ports to SIM ports and enable Flow genALL sys test
    
    """
    #### send a fos command to configure
    capture_cmd = anturlar.fos_cmd("flow --control -portidmode slotport ")
    cons_out = anturlar.fos_cmd("flow --show")

    si_maps = anturlar.maps()
    si_maps_sim = si_maps.toggle_all("off")
    
    si_maps_gen = si_maps.genAll("on")
    
    cons_out = anturlar.fos_cmd("portcfgshow")
    
    si_maps_sim = si_maps.toggle_all("on")
    
    cons_out = anturlar.fos_cmd("portcfgshow")
    cons_out = _anturlar.fos_cmd("flow --show")

    si_maps_gen = si_maps.genAll("on")
    cons_out = anturlar.fos_cmd("flow --show")

def remove_sim():
    """
    remove any SIM ports enabled on the switch
    
    """
    
    
    pass

def ports_disable(portlist = "", t=1, wait=10):
    """
     port disable for the number of time passed in
     should be no reason to do more than one time
    """
    if portlist == "":
        si = anturlar.SwitchInfo()
        portlist = si.all_ports()
    for x in range(1, t+1):
        for a in portlist:
            cons_out = anturlar.fos_cmd("portdisable %s" % a)
            
def ge_ports():
    """
        Return a list of the ge-ports in the current FID
    """
    si = anturlar.SwitchInfo()
    capture_cmd = anturlar.fos_cmd("switchshow")
    if si.am_i_director:
        ras = re.compile('\s([0-9]{1,2})\s+([a-z]{1,3}[0-9])')
        ge_ports = ras.findall(capture_cmd)
        return(ge_ports)
    else:
        ras = re.compile('\s?(ge[0-9]{1,2})')
        ge_ports = ras.findall(capture_cmd)
        return(ge_ports)
    
def ve_ports():
    """
        Return a list of the VE-ports in the current FID
    """
    si = anturlar.SwitchInfo()
    capture_cmd = anturlar.fos_cmd("switchshow")
    if si.am_i_director:
        ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+(?:[-0-9a-f]{6})\s+(?:[-id]{2})\s+(?:[-UNG12486]{2,3})\s+(?:[_\w]{5,9})(?:\s+VE)')
        ve_ports = ras.findall(capture_cmd)
        print('$$$$$$$$$$$$$$$$$$$$')
        #print(ve_ports)
        return(ve_ports)
    else:
        ras = re.compile('\s?([0-9]{1,3})\s+(?:\d+)\s+(?:[-0-9a-f]{6})\s+(?:[-id]{2})\s+(?:[-UNG12486]{2,3})\s+(?:[_\w]{5,9})(?:\s+VE)')
        ve_ports = ras.findall(capture_cmd)
        #print(ve_ports)
        return(ve_ports)
            
def enable_disabled_ports():
    si = anturlar.SwitchInfo()
    portlist = si.disabled_ports()
    print(type(portlist))
    print(portlist)
    if si.am_i_director:
        for i in portlist:
            slot = i[0]
            port = i[1]
            cons_out = anturlar.fos_cmd("portenable %a/%a" % (slot, port))  
    else:
        for i in portlist:
            pt = i[0]
            #port = (int(pt))
        cons_out = anturlar.fos_cmd("portenable %s" % pt)

def ports_enable(portlist= "", t=1, wait=10):
    """
     port enable for the number of time passed in
     there should be no reason for time to be more than 1
     
    """
    
    if portlist == "":
        si = anturlar.SwitchInfo()
        portlist = si.all_ports()
        print('$$$$$$$$$$$$$$$$$$$$')
        print(type(portlist))
        print (portlist)
        if si.am_i_director == (True):
            for x in range(1, t+1):
                for i in portlist:
                    slot = i[0]
                    print('$$$$$$$$$$$$$$$$$$$$')
                    print(slot)
                    port = i[1]
                    print(port)
                    cons_out = anturlar.fos_cmd("portenable %a/%a" % (slot, port))  
        else:
            for x in range(1, t+1):
                for i in portlist:
                    cons_out = anturlar.fos_cmd("portenable %i" % i)
                    
    else:  
        if si.am_i_director == "1":
            for x in range(1, t+1):
                for i in portlist:
                    slot = i[0]
                    port = i[1]
                    cons_out = anturlar.fos_cmd("portenable %a/%a" % (slot, port))
        else:
            for x in range(1, t+1):
                for a in portlist:
                    cons_out = anturlar.fos_cmd("portenable "+a)
        
        
def ports_toggle(portlist="", t=2, wait=10):
    """
      port disable / port enable for the number of times passed in
      
    """
    ####  this is for pizza box
    ####   need to add chassis
    ####
    
    if portlist == "":
        si = anturlar.SwitchInfo()
        portlist = si.all_ports()
    for x in range(1, t):
        for a in portlist:
            cons_out = anturlar.fos_cmd("portdisable %s"%a)
            
        liabhar.count_down(wait)
         
        for a in portlist:
            cons_out = anturlar.fos_cmd("portenable %s"%a)
            liabhar.count_down(10)
            
        liabhar.count_down(wait)
    
    
def configdl(clear = 0):
    """
        capture any information for testing of the configdownload 
        - including mapspolicy --show
                    mapsconfig --show
                    flow --show
                    flow --show -ctrlcfg
                    relayconfig --show
                    bottleneckmon --status
                    
        then perform configupload
        
        config upload 
        
        Nimbus_______________Odin_86__:FID25:root> configupload
        Protocol (scp, ftp, sftp, local) [ftp]: ftp 
        Server Name or IP Address [host]: 10.38.38.138
        User Name [user]: ftp2
        Path/Filename [<home dir>/config.txt]: Odin_configupload.txt
        Section (all|chassis|FID# [all]): all
        Password:
        
        or
        
        configdownload [- all ] [-p ftp | -ftp] ["host","user","path"[,"passwd"]]
        configdownload [- all ] [-p scp | -scp ] ["host","user","path"]
        
    """
    #### capture maps config all FIDS
    #### capture flow config all FIDS
    ####
    
    sw_info = anturlar.SwitchInfo()
    sw_info_ls = sw_info.ls()
    #print('$$$$$$$$$$$$$$$$$$$')
    #print(sw_info_ls)
    fid_now = sw_info.ls_now()
    
    cons_out = anturlar.fos_cmd(" ")
    sw_ip = sw_info.ipaddr
     
    
    f = "%s%s%s"%("logs/Configupload_test_case_file",sw_ip,".txt")
    
    if clear == 1 :
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
    else:
        ff = liabhar.FileStuff(f, 'a+b')  #### open for appending
        
    header = "%s%s%s%s" % ("\nCONFIGUPLOAD CAPTURE FILE \n", "  sw_info ipaddr  ",sw_ip, "\n==============================\n\n")  
    ff.write(header)
    ff.close()
    
    ff = liabhar.FileStuff(f, 'a+b')  #### open the log file for writing
    ff.write(str(sw_info_ls))
    ff.write("\n"*2)
    
    for i in sw_info_ls:
        cons_out = anturlar.fos_cmd("setcontext "+i)   
        cons_out = anturlar.fos_cmd("mapsconfig --show")
        ff.write("="*80+"\n")
        ff.write("="*80+"\n")
        ff.write("LOGICAL SWITCH :: " +i+"\n")
        ff.write("="*80+"\n")
        ff.write("\nMAPS CONFIG::"+i+"\n")
        ff.write(cons_out+"\n\n")
        ff.write("#"*80+"\n")
        ff.write("#"*80+"\n")
        
        cons_out = anturlar.fos_cmd("mapspolicy --show -summary")
        ff.write("="*80+"\n")
        ff.write(cons_out+"\n\n")
        ff.write("#"*80+"\n")
        ff.write("#"*80+"\n")
        
        cons_out = anturlar.fos_cmd("flow --show")
        ff.write("="*80+"\n")
        ff.write(cons_out+"\n\n")
        ff.write("#"*80+"\n")
        ff.write("#"*80+"\n")
        
        cons_out = anturlar.fos_cmd("flow --show -ctrlcfg")
        ff.write("="*80+"\n")
        ff.write(cons_out+"\n\n")
        ff.write("#"*80+"\n")
        ff.write("#"*80+"\n")
        
        cons_out = anturlar.fos_cmd("relayconfig --show")
        ff.write("="*80+"\n")
        ff.write(cons_out+"\n\n")
        ff.write("#"*80+"\n")
        ff.write("#"*80+"\n")
        
        cons_out = anturlar.fos_cmd("bottleneckmon --status")
        ff.write("="*80+"\n")
        ff.write(cons_out+"\n\n")
        ff.write("#"*80+"\n")
        ff.write("#"*80+"\n")
        
    ff.write("="*80+"\n")
    ff.write("\n"*10)
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    cons_out = anturlar.fos_cmd(" ")
    configdown_cmd = "configupload -all -p ftp 10.38.38.138,ftp2,configupload_test.txt,ftp"
    cons_out = anturlar.fos_cmd (configdown_cmd)
    
 
def firmwaredownload(frmdwn ):
    """
        use anturlar firmwaredownload to do testing for update to
        newest code
        
    """
    f = anturlar.doFirmwareDownload(frmdwn)
    
def clearstats():
    """
        clear all stats using the clear stats procedure in anturlar.py
    """
    cs = anturlar.clear_stats()
    
def flow_all_switch():
    """
        capture all the flow --show information 
    """
    
def add_remove_flow(repeat, fname, scr, dst, ingrp, egrp, feat):
    """
        add and remove a flow from the current switch and FID
        
        --should add find one of the ports on the switch and add the flow to
        that port -
        --discover which port is the same as the scrdev or dstdev and add
        -- since this is a add and remove the flow test case the lun, ftype and bidir
        could be random
        
    """
    ####cmd = "supportsave -n -u %s -p %s -h %s -l ftp -d %s" % (variables, variables)
    cmd_create = "flow --create %s -fea %s -srcdev %s -dstdev %s" % ( fname,feat,scr,dst)
    
    if ingrp != "na":
        cmd_create = "%s -ingrport %s" % ( cmd_create, ingrp )
    
    if egrp != "na":
        cmd_create = "%s -egrport %s " % ( cmd_create, egrp )
        
    
    cons_out = anturlar.fos_cmd(cmd_create)
    
    while repeat > 0:
        print(repeat,"\n")
        cons_out = anturlar.fos_cmd("flow --show")
        
        repeat = repeat - 1 
    
    return 0 

    
def add_flow(fname, scr, dst, ingrp, egrp, feat):
    """
        add a flow from the current switch and FID
        this will add with the --noactivate option so that it is always added
        
        --should add find one of the ports on the switch and add the flow to
        that port -
        --discover which port is the same as the scrdev or dstdev and add
        -- since this is a add and remove the flow test case the lun, ftype and bidir
        could be random
        
    """
    ####cmd = "supportsave -n -u %s -p %s -h %s -l ftp -d %s" % (variables, variables)
    cmd_create = "flow --create %s -fea %s " % ( fname,feat)
    
    
    if scr != "b":
        if scr == "learn":
            cmd_create = "%s -srcdev '*' " % (cmd_create)    
        else:
            cmd_create = "%s -srcdev %s " % (cmd_create, scr)
        
    if dst != "b":
        if dst == "learn":
            cmd_create = "%s -dstdev '*' " % (cmd_create)    
        else:
            cmd_create = "%s -dstdev %s " % (cmd_create, dst)
        
    if ingrp != "na":
        cmd_create = "%s -ingrport %s " % ( cmd_create, ingrp )
    
    if egrp != "na":
        cmd_create = "%s -egrport %s " % ( cmd_create, egrp )
        
    cmd_create = "%s -noactivate " % (cmd_create)
    
    cons_out = anturlar.fos_cmd(cmd_create)
    cons_out = anturlar.fos_cmd("")
    
    #while repeat > 0:
    #    print("repeat\n")
    #    repeat = repeat - 1 
    
    return 0 
    
    
    
def delete_flow( name ):
    """
        delete flow vision flows from a switch
        
    """
    
    if name == "all":
        cons_out = anturlar.fos_cmd("echo Y | flow --delete all ")
    else:
        cons_out = anturlar.fos_cmd("flow --delete %s" % name)
    
    
def mapsenable( pol, al, ml ):
    """
        enable MAPS with policy         pol
                         actions list   al
                         email list     ml
                         
        -- this function will enable MAPS only if you want to
        change the policy use mapspolicy()
        
    """
    
    m = anturlar.Maps()
    m.enable(pol)
    m.actions(al)
    m.email_cfg(ml)
    
    return 0
    

def enable_flows( ones ):
    """
        enable all fea of flows of current switch
        - get the flow names
        - enable the flows with all features
        
    """
    
    f = anturlar.FlowV()
    the_names = f.flow_names()
    print(the_names)
    
    for k in the_names:
        if "sys_gen_all_simports" in k:
            print("not enabling this one" , k)
        else:
            cmd_create = ("flow --activate %s -fea all" % k )   
            cons_out = anturlar.fos_cmd(cmd_create)
            
def cfgsave():
    """
        save switch config to \logs\config
    """
    
    config = anturlar.configSwitch()
    configsave = config.saveSwitchInfo
    
#def get_fcr_ipv4():
#    fcrinfo = anturlar.FcrInfo()
#    #switchinfo = anturlar.SwitchInfo
#    #fabricinfo = anturlar.FabricInfo
#    fcr_list = fcrinfo.ipv4_fcr()
#    print('$$$$$$$$$$$printing fcr_list from fcrtc_o.py$$$$$$$$$$$$$$$$$$$')
#    print(fcr_list)
#    return(fcr_list)

#def ipv4_fcr():
#    """
#        Return a string (list) ipv4 address of switch\switches connected
#        to FCR Router thru EX-Port
#    """
#    capture_cmd = fos_cmd("fcrfabricshow")
#        if capture_cmd = ("fcrfabricshow should be executed only in base switch"):
#            print('this is from ipv4_fcr in fcrtc_0.py')    
#    
#    ras = re.compile('(?:\d{1,3}\s+\d{1,3}\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
#    ras_result_all = ras.findall(capture_cmd)
#        
#    if not ras_result_all:
#        ras_result_all = "NO EX_PORTS FOUND" 
#    return ras_result_all

def get_licenses(ip):
    anturlar.connect_tel_noparse(ip,'root','password')
    sw_info = anturlar.SwitchInfo()
    #sw_ip = sw_info.ipaddr
    sw_name = sw_info.switch_name()
    f = "%s%s%s"%("logs/Switch_Licenses/License_File_", sw_name ,".txt")
    ff = liabhar.FileStuff(f,'a+b') ###open new file or clobber old
    header = "%s%s%s%s" % ("\nLICENSE FILE \n", ip+"\n" , sw_name, "\n==============================\n\n")
    cons_out = anturlar.fos_cmd("licenseshow")
    ff.write(header)
    ff.write(cons_out+"\n")
    ff.close()
    
def send_cmds(filename , loops = 1):
    """
        function to read cmds from a file and send them to the switch
        
    """
    print('$$$$$$$$$$$$$$$$$$$$$')
    file = "LicenseShow1" ####Change this as needed
    fullpath = "%s%s%s" % ("logs/configs/", file ,".txt")
    print(fullpath)
    g = liabhar.FileStuff(fullpath, 'a+b')
    cons_out = anturlar.fos_cmd("")
        
    with open(filename) as fileio:
        info = fileio.readlines()
        print(info)
    
    while loops >=1 :    
        for line in info:
            line = line.rstrip('\n')
            cons_out = anturlar.fos_cmd(line)
            g.write(cons_out)
            g.write(" ")
            
        loops -= 1
     
    g.close()
    return 0

    
    
    
    
    
    
    



