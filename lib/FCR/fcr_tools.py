#!/opt/python3/bin/python3

###############################################################################
#### Home location is
####
###############################################################################
"""
FCR TOOLS - different functions to get information from switches and/or fabrics in regards to FCR configuration

"""

import anturlar
import liabhar
import cofra
import sys, os, csv, re

"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""

def bb_fabric_switch_status():
    """
        OBSOLETE????? Not sure if returned data is useable
        For all switches found in backbone fabric, returns a dictionary data structure for switch
        status for switch states:
        fcr_enabled (T or F); ip address; switch_name; vf_enabled (T or F); base (return base FID
        if T or False if not configured).
    """
    si = anturlar.FcrInfo()
    ips = si.all_switches_in_bb_ip()
    switch_dict = {}
    for i in ips:
        anturlar.connect_tel_noparse(i,'root','password')
        a = switch_status()
        switch_dict = switch_dict + a
        print(switch_dict)
    return(switch_dict)

def get_bb_ips():
    """
    Return ip addressses of all switches in backbone. ##Checked 02/03/2015
    """
    
    fcrcfg = anturlar.FcrInfo()
    fab_ip_list = list(fcrcfg.fcr_backbone_ip())
    return(fab_ip_list)

def get_fabwide_ip():
    """
    Get all IP addresses of backbone switches and edge switches ##Checked 02/03/2015
    """
    fcrcfg = anturlar.FcrInfo()
    fab_ip_list = list(fcrcfg.fcr_fab_wide_ip())
    print("\n\n\n\n\nFABLIST with NO DUPLICATES IS  :  ",fab_ip_list,"\n\n\n\n\n")
    return(fab_ip_list)


def fab_wide_proxy_device_numbers():
    """
    Retrieve number of proxy device on all backbone switches in fabric. Drop those numbers
    into a file for later retreival (e.g. say after reboot testing). Also return a
    dictionary (e.g {switch_ip: # of proxy devices})
    """
    
    fcrinfo = anturlar.FcrInfo()
    backbone_ip = fcrinfo.fcr_backbone_ip()
    bb_fab_num = (len(backbone_ip))
    proxy_dev_count = []
    for ip in backbone_ip:
        anturlar.connect_tel_noparse(ip,'root','password')
        base = fcrinfo.base_check() # get the base FID number
        if base is not False:
            anturlar.fos_cmd("setcontext " + base)
            get_proxy = fcrinfo.fcr_proxy_dev()
            proxy_dev_count.extend(get_proxy)

        else:
            get_proxy = fcrinfo.fcr_proxy_dev()
            proxy_dev_count.extend(get_proxy)
    switch_list_with_proxy_dev = dict(zip(backbone_ip, proxy_dev_count))
    proxy_dev_count = (str(proxy_dev_count))
    f = ('logs/ProxyDev_Count.txt')
    ff = liabhar.FileStuff(f,'w+b') ###open new file or clobber old
    ff.write(proxy_dev_count)
    ff.close()
    print('\n\n'+ '='*20)        
    print('Backbone Fabric consists of %s switches.' % bb_fab_num)
    print('IP addresses: Number of proxy devices found')
    print(switch_list_with_proxy_dev)
    print('='*20 + '\n\n')
    return(switch_list_with_proxy_dev)

    #switches = dict.fromkeys(['switch_name','switch_ip','form_factor'])
    #print(switches)
    #switches_found = (len(backbone_ip))
    #print (switches_found)
    #while switches_found > 0:
    #    for i in backbone_ip:
    #        print(i)
    #        switches_found = switches_found - 1
    #        switches['switch_ip'] = i
    #    #print(switches)
    #print(proxy_dev)
    #print(backbone_ip)
    #print(switches)
    #switchlist = [dict() for x in range(0,5)]
    #print (switchlist)
    #d={}
    #for x in range(1,5):
    #    d["string{1}".format(x)]="Hello"
    #    print(d)
    #return(proxy_dev, backbone_ip, switches)
    

def switch_status():
    """
        Retrieve FCR fabric and return info. Variable #'s:
        0) Switch name
        1) IP address
        1) Chassis or Pizza Box
        2) VF or not
        3) FCR Enabled
        4) Base Configured
        
        return dictionary with {switch_name, ipaddr, chassis, vf_enabled, base, fcr_enabled}}
    """
    fcrinfo = anturlar.FcrInfo()
    initial_checks = fcrinfo.sw_basic_info()
    print('\n\n'+ '='*20)
    print("Switch Name :  %s" % initial_checks[0])
    print("IP address :  %s" % initial_checks[1])
    print("Chassis :  %s" % initial_checks[2])
    print("VF enabled :  %s" % initial_checks[3])
    print("FCR enabled :  %s" % initial_checks[4])
    print("Base configured :  %s" % initial_checks[5])
    print('='*20 + '\n\n')
    switch_info = { 'switch_name' : initial_checks[0],'ipaddr' : initial_checks[1], 'chassis' : initial_checks[2],'vf_enabled' : initial_checks[3], 'fcr_enabled' : initial_checks[4], 'base' : initial_checks[5]}
    return (switch_info)

#def bb_fabric_switch_status():
#    ips = all_switches_in_bb_ip()
#    switch_dict = []
#    for i in ips:
#        anturlar.connect_tel_noparse(i,'root','password')
#        a = switch_status()
#        switch_dict.append(a)
#    s = (len(switch_dict))
#    #print(s)
#    return(switch_dict)

def ex_slots_find():
    """
    Find EX/VEX ports and return slot number/port number.
    """
    fcri = anturlar.FcrInfo()
    fcipi = anturlar.FcipInfo()
    vex_port_list = fcri.vex_ports()
    ex_port_list = fcri.ex_ports()
    disabled_port_list = fcri.disabled_ports()
    ge_port_list = fcipi.all_ge_ports()
    print("PORTLISTPORTLIST")
    print(vex_port_list)
    sys.exit(0)
    print(ex_port_list)
    print(disabled_port_list)

    #################################
    print(ex_port_list)
    print(disabled_port_list)
    if self.am_i_director:
       for i in portlist:
            slot = i[0]
            port = i[1]
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = fos_cmd("portcfgshow %a/%a" % (slot, port))
            ex = pattern.search(cmd)
            if ex:
                fos_cmd("portcfgexport %s/%s %s"%(slot,port,"-a2") )
    else: 
        for i in portlist:
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = fos_cmd("portcfgshow %a" % i)
            ex = pattern.search(cmd)
            if ex:
                fos_cmd("portcfgexport "+i+" -a2")
        cmd_cap = fos_cmd("switchenable")        
        return(cmd_cap)
    
def fcr_state_persist_enabled():
    #print(sys.argv)
    host = (sys.argv[1])
    user = sys.argv[2]
    password = sys.argv[7]
    test_file = '/home/RunFromHere/ini/SwitchMatrix.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is True:
        anturlar.fos_cmd("switchdisable")
        print('\n\nSleeping: 10')
        liabhar.JustSleep(10)
        enabled = switch_status()
        if enabled['fcr_enabled'] is True:
            anturlar.fos_cmd("switchenable")
            print('\n\nSleeping: 10')
            liabhar.JustSleep(10)
            print("\n\nENABLE/DISABLE TEST PASSED")
        else:
            pass
    else:
        print("\n\nENABLE/DISABLE TEST FAILED")
        print("Please enable fcr for this test and try again")
        sys.exit(0)
    print('\n\nSleeping: 10')
    liabhar.JustSleep(10)
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    a = cofra.switch_power_off_on(cn, 'off')
    print('\n\nSleeping: 20')
    liabhar.JustSleep(20)
    a = cofra.switch_power_off_on(cn, 'on')
    print('\n\nSleeping: 120')
    liabhar.JustSleep(120)
    anturlar.connect_tel_noparse(host, user, password)
    si = anturlar.SwitchInfo()
    print("GETTINGFCRSTATE")
    fcr_state = switch_status()
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
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is False: #the same to here disabled is false, enabled is true
        anturlar.fos_cmd("switchdisable")
        print('\n\nSleeping: 10')
        liabhar.JustSleep(10)
        enabled = switch_status()
        if enabled['fcr_enabled'] is False:
            anturlar.fos_cmd("switchenable")
            print('\n\nSleeping: 10')
            liabhar.JustSleep(10)
            print("\n\nENABLE/DISABLE TEST PASSED")
        else:
            pass
    else:
        print("\n\nENABLE/DISABLE TEST FAILED")
        print("Please disable fcr for this test and try again")
        sys.exit(0)
    print('\n\nSleeping: 10')
    liabhar.JustSleep(10)
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    a = cofra.switch_power_off_on(cn, 'off')
    print('\n\nSleeping: 20')
    liabhar.JustSleep(20)
    a = cofra.switch_power_off_on(cn, 'on')
    print('\n\nSleeping: 120')
    liabhar.JustSleep(120)
    anturlar.connect_tel_noparse(host, user, password)
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is False:
        print('Reboot Complete. FCR State remains consistent')
        print('TEST PASSED')
    else:
        print('FCR State changed.')
        print('TEST FAILED')

    sys.exit(0)#######################
    
def license_restore(): #### NEED TO ADD supportftp settings AND Timeserver
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[7]
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    test_file = '/home/RunFromHere/ini/SwitchLicenses.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    for line in csv_file:
        a = (type(line))
        switch_name = (line['Nickname'])
        if switch_name == cn[0]:
            del (line[''])
            del (line ['Nickname'])
            del (line['IP Address'])
            a = (list(line.values()))
            for i in a:
                if i != (''):
                    anturlar.fos_cmd("licenseadd %s" % i)
                    liabhar.JustSleep(5)
    anturlar.fos_cmd("echo y | reboot")
    print('\n\nSleeping: 150')
    liabhar.JustSleep(150)   
    anturlar.connect_tel_noparse(host, user, password)
    anturlar.fos_cmd('licenseshow')
    return(True)


    