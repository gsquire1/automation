#!/usr/bin/env python3

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
import switch_playback
import sys, os, csv, re, filecmp, difflib

"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""

def test_anturlar_functions():
    #a = ex_port_list()
    fcri = anturlar.FcrInfo()
    si = anturlar.SwitchInfo()
    #su = cofra.SwitchUpdate()
    #a = fcri.__getportlist__("EX-Port")
    b = fcri.all_ex_ports_with_edge_fid()
    print("3333333333333333333333333333333")
    print(b)
    sys.exit()
    
def playback_add_ports():
#def playback_add_ports(self):
    """
    
    """
    
    reg_ex_yes_no_root = [b"no\]\\s+", b":\s+[\[ofn\]]+", b"[0-9]+\]\\s+", b"root> "]
    reg_ex_yes_no = [b"n\]\?:\\s+", b":\s+[\[ofn\]]+", b"[0-9]+\]\\s+"]
    #switch_ip = self.si.ipaddress()

    #f = ("%s%s%s"%("logs/Switch_Info_for_playback_",self.switch_ip,".bak.txt"))
    #f = "%s%s%s"%("logs/Switch_Info_",self.switch_ip,"_%s.txt" % self.extend_name)
    f = ("logs/Switch_Info_10.38.134.65_2015_11_11_13_40_19_875006_65_VF_Wedge.txt")
    try:
        with open(f, 'r') as file:
            a = file.read()
            print(a)
    except IOError:
        print("\n\nThere was a problem opening the file:" , f)
        sys.exit()
    ras = re.findall('EX_PORTS\s+:\s+\{(.+)(?:})', a)
    print(ras)
    sys.exit()
    sn = ras[0]
    sn = sn.split("'")
    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
    print(sn)
    sys.exit()
    for i in range(2,len(sn),2):
        
        fid_for_ports = sn[i-1]
        fid_ports = sn[i]
        
        fid_ports = fid_ports.replace(": [","")
        fid_ports = fid_ports.replace("[","")
        fid_ports = fid_ports.replace("]],","")
        fid_ports = fid_ports.replace(" ","")
        fid_ports = fid_ports.replace("]","")
        fid_ports = fid_ports.split(",")
        print("@"*30)
        print(fid_ports)
        print("$"*44)
        for s in range(0,len(fid_ports),2):
            try:
                slot = fid_ports[s]
                port = fid_ports[s+1]
                #print("SLOT PORT_____%s_____%s___ " % (slot,port))
                #### add pizza box vs director
                #am_director = si.director()
                if self.direct:
                    cons_out = anturlar.fos_cmd_regex("lscfg --config %s -slot %s -port %s" % (fid_for_ports, slot,port) , reg_ex_yes_no, 0)
                    cons_out = anturlar.fos_cmd("y",0)
                else:
                    cons_out = anturlar.fos_cmd_regex("lscfg --config %s -port %s" % (fid_for_ports, port) , reg_ex_yes_no, 0)
                    cons_out = anturlar.fos_cmd("y",0)
             
            except IndexError:
                print("No ports in this FID")
                
    return(True)
    
def enter_file_ext():
    go = False
    start = 'n'
    ###################################################################################################################
    ####
    ####  enter a file extension for the replay file instead of the default
    ####  otherwise use the defualt
    ####  stop if the user pushes esc 
    ####
    ###################################################################################################################
    
    
    
#######################################################################################################################
####
####  standard way to handle user input
####    - while loop looking for a valid 'go' variable
####       - while loop waiting for a string input
####       - if start variable is y set go to true and exit the procedure
####
#######################################################################################################################
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/no] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                sys.exit()        
        if start == 'y' :
            go = True
        else:
            print("START VALUE is  %s" % start)
            if start == 'no':
                sys.exit()
            else:
                start = 'n'

def user_start():
    temperature = 115  
    while temperature > 112: # first while loop code
        print(temperature)
        temperature = temperature - 1
    print('The tea is cool enough.')
    start = 'n'
    go = False
    while go == False : ##Not False
        print("go is equal to FALSE")
        try:
            start = str(input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/n] : "))
            print(start)
        except:
            print("SOMETHING WRONG WITH INPUT")
        go = True
    print("OUT OF LOOP")
    sys.exit()


    
def csv_functions_ip():
    user_start()
    sys.exit()
    start = (input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/n] : "))
    print(start)
    sys.exit()
    test_file = '/home/RunFromHere/ini/TBC_SwitchMatrix.csv'
    ips = []
    #name = str(input("What's your name?  "))
    #print(name)
    #sys.exit()
    try:
        with open(test_file) as switch_matrix:
            my_dict = csv.DictReader(switch_matrix)
            for row in my_dict:
                #print(row)
                #sys.exit()
                chassisname = (row['Chassisname'])      # Resource_type
                ip = (row['IP Address'])                # IP
                password = (row['Password'])            # Password
                console_1 = (row['Console1 IP'])        # CP_0 Console IP
                console_1_port = (row['Console1 Port']) # CP_0 Console Port
                console_2 = (row['Console2 IP'])        # CP_1 Console IP
                console_2_port = (row['Console2 Port']) # CP_1 Console Port
                cp0_ip = (row['CP0 IP'])                # CP_0 IP
                cp1_ip = (row['CP1 IP'])                # CP_1 IP
                fabric_name = ("Need to get user input here")   #Fabric name
                admin_pwd = ['password']                # Admin Password
                root_pwd = ['password']                 # Root Password
                pwr_1 = (row['Power1 IP'])              # Power_1
                pwr_1_port = (row['Power1 Port'])       # Power_1_Port
                pwr_2 = (row['Power2 IP'])              # Power_2
                pwr_2_port = (row['Power2 Port'])       # Power_2_Port

                print ('\n\n')
                #sys.exit()
                chassis_name = ("%s_resource_type       fos" % chassisname)
                ip = "%s_ip                             %s" % (chassisname, ip)
                console_1 = "%s_cp0_console             %s %s" % (chassisname, console_1, console_1_port)
                cp0ip = "%s_cp0_ip    %s" % (chassisname, cp0_ip)
                cp1ip = "%s_cp0_ip    %s" % (chassisname, cp1_ip)
                if (console_2):
                    console_2 = "%s_cp1_console         %s %s" % (chassisname, console_2, console_2_port)
                    cp0ip = "%s_cp0_ip    %s" % (chassisname, cp0_ip)
                    cp1ip = "%s_cp0_ip    %s" % (chassisname, cp1_ip)

                else:
                    pass
                #if (console_2) #############CP IPS NEED TO GO IN THIS LOOP
                #print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
                #print(cp0_ip)
                #print(cp1_ip)
                #cp0ip = "%s_cp0_ip    %s" % (chassisname, cp0_ip)
                #cp1ip = "%s_cp0_ip    %s" % (chassisname, cp1_ip)

##############################################################
                print (chassis_name)
                print (ip)
                print(console_1)
                if (console_2):
                    print (console_2)
                    #print (console_2_port)
                    print(cp0ip)
                    print(cp1ip)
                #print(console_2)
                #print(cp0ip)
                #print(cp1ip)
            print("THEEND")
            sys.exit()
            if console_2 != '':
                    #console_2 = (row['Console2 IP'])
                    #console_2_port= (row['Console2 Port'])
                    print("PPPPPPPPPPP")
                    print(console_2)
                    print(console_2_port)
            else:
                    #print("MUST BE A PIZZA BOX")
                    pass
            
            #value = None
            #keys = my_dict.keys()
            #print (keys)
            #keys_sorted = keys.sorted()
            #print (keys_sorted)
            #for row in my_dict:
                #print
                #if row in reader:
                #    value = reader[key]
                #    print("PPPPPPPPPPPPPPPPPPPPP")
                #    print(value)
                #chassisname = (row['Chassisname'])
                #print(chassisname)
                #if chassisname in row:
                #    print("True")
                #    #chassisname = (row['Chassisname'])
                #    #print(chassisname)
                #else:
                #    print("NOT THERE")
                #sys.exit()
                #
                #if ip:
                #    if ip not in ips:
                #        ips.append(ip)
            #print("\n\n%s" % ips)
            #print("\n\n%s" % row)
            #return(ips)
            #for ip in ips:
                #get_info_from_the_switch(ip)
            #return(ips)
            return()


    except FileNotFoundError:
        print('\n\nFile Not Found (Line 158 in fcr_tools.py)')
        return(False)
    
def file_diff(a,b,c=""):
    """
    Compare two files for differences, print to console and put in a file in logs directory
    """

    difference = ("/home/RunFromHere/logs/difference_%s.txt" % c)
    z = filecmp.cmp(a,b)
    if z == True:
        print("\n\nThe files are the same")
        return(True)
    else:
        with open (a) as File1:
            c = File1.readlines() 
        with open (b) as File2:
            d = File2.readlines()
    print('\n')
    for line in difflib.context_diff(c,d, fromfile=(a), tofile=(b), n=0):
        print((line))
    with open (difference, 'w') as differ:
        for line in difflib.context_diff(c,d, fromfile=(a), tofile=(b), n=0):
            differ.write(line)    
    sys.exit()
       

def portcfgfillword():
    fcr = anturlar.FcrInfo()
    portcfg = fcr.portcfgfillword(3)
    
    
def bb_fabric_switch_status():
    """
        OBSOLETE##############
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

def cfgupload(ftp_ip, ftp_user, ftp_pass, clear = 0):
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
    sw_info = anturlar.SwitchInfo()
    sw_info_ls = sw_info.ls()
    fid_now = sw_info.ls_now()
    
    cons_out = anturlar.fos_cmd(" ")
    sw_ip = sw_info.ipaddress()
    
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
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    #cons_out = anturlar.fos_cmd(" ")
    configdown_cmd = ("configupload -all -p ftp %s,%s,/configs/%s.txt,%s") % (ftp_ip, ftp_user, sw_ip, ftp_pass)
    ftp_ip, ftp_user, ftp_pass
    cons_out = anturlar.fos_cmd (configdown_cmd)

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
    fid_now = sw_info.ls_now()
    
    cons_out = anturlar.fos_cmd(" ")
    sw_ip = sw_info.ipaddress()
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    #cons_out = anturlar.fos_cmd(" ")
    configdown_cmd = ("configdownload -all -p ftp 10.38.35.131,ftp1,/configs/%s.txt,ftp2") % (sw_ip)
    cons_out = anturlar.fos_cmd (configdown_cmd)
    

def fab_wide_proxy_device_numbers():
    """
    Retrieve number of proxy device on all backbone switches in fabric. Drop those numbers
    into a file for later retreival (e.g. say after reboot testing). Also return a
    dictionary (e.g {switch_ip: # of proxy devices})
    """
    
    fcrinfo = anturlar.FcrInfo()
    backbone_ip = fcrinfo.fcr_backbone_ip()
    print(backbone_ip)
    sys.exit()
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
    print('Backbone Fabric consists of %s switches.' % (len(bb_fab_num)))
    print('IP addresses: Number of proxy devices found')
    print(switch_list_with_proxy_dev)
    print('='*20 + '\n\n')
    return(switch_list_with_proxy_dev)


    

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
    si = anturlar.SwitchInfo()
    initial_checks = si.switch_status()
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

#def ex_deconfig(): 
#    fcri = anturlar.FcrInfo()
#    test = fcri.ex_deconfig()
#    print('\n\nAll EX_ports found are now deconfigured.')

def ex_port_list():
    """
    Grabs only ONLINE EX-Ports. Parses "switchshow" for EX-Ports.
    """
    si = anturlar.SwitchInfo()
    ex_list = si.ex_ports()
    #print('*************')
    #print(ex_list)
    
   
def ex_deconfig():
    """
    Find all EX-Ports AND VEX-Ports on either director or pizzabox and deconfigure.
    This parses "portcfgshow" command for any EX-Port, online or not, and deconfigures. This includes
    VEX ports as well.
    """
    si = anturlar.SwitchInfo()
    anturlar.fos_cmd("switchdisable")
    portlist =  si.all_ports()
    if si.am_i_director:
        for i in portlist:
            slot = i[0]
            port = i[1]
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = anturlar.fos_cmd("portcfgshow %a/%a" % (slot, port))
            ex = pattern.search(cmd)
            if ex:
                anturlar.fos_cmd("portcfgexport %s/%s %s"%(slot,port,"-a 2"))
                anturlar.fos_cmd("portcfgvexport %s/%s %s"%(slot,port,"-a 2"))
    else: 
        for i in portlist:
            print(i)
            port = i[1]
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = anturlar.fos_cmd("portcfgshow %a" % port)
            ex = pattern.search(cmd)
            if ex:
                anturlar.fos_cmd("portcfgexport %s %s"%(port,"-a 2"))
                anturlar.fos_cmd("portcfgvexport %s %s"%(port,"-a 2"))
    cmd_cap = anturlar.fos_cmd("switchenable")
    print('\n\nAll EX_ports found are now deconfigured.')
    return(cmd_cap)

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
    print("VEX_PORTS: %s" % vex_port_list)
    print("EX_PORTS: %s" % ex_port_list)
    print("DISABLED_PORTS: %s" % disabled_port_list)
    sys.exit(0)
#################################

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
    

    
def firmwaredownload(frmdwn, frmup):
    """
        uses cofra firmwaredownload to do testing for update to
        newest code
        
        the test will load first firmware and return to the other on a second
        download command
    """
    
    capture_cmd = anturlar.fos_cmd("ipaddrshow")
    #match = re.search('(?P<ipaddress>[\s+\S+]+:([\d\.]){7,15}(?=\\r\\n))', capture_cmd)
    match = re.search('(?P<pre>([\s+\w+]+):\s?(?P<ip>[0-9\.]{1,15}))', capture_cmd)
    if match:
        myip = (match.group('ip'))
        #return(myip)
    else:
        print("\n\n NO IP FOUND \n\n")
        #return (0)
    
    while True:
    #f = cofra.doFirmwareDownload(frmdwn)
        capture_cmd = anturlar.fos_cmd("version")
        f = cofra.DoFirmwaredownloadChoice(frmdwn,frmup)

        liabhar.count_down(600)
        
        anturlar.connect_tel_noparse(myip, 'root', 'password')
        #en = anturlar.SwitchInfo()
        capture_cmd = anturlar.fos_cmd("version")
        
        f = cofra.DoFirmwaredownloadChoice(frmdwn, frmup)
    
        anturlar.connect_tel_noparse(myip, 'root', 'password')
        #en = anturlar.SwitchInfo()

    return(0)
    
def license_restore(): #### NEED TO ADD supportftp settings AND Timeserver
    """
    Ned to replace sys.argv statements as the order can change on the cli input by user
    """
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[7]
    print(password)
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
    anturlar.connect_tel_noparse(host, user, "password")
    anturlar.fos_cmd('licenseshow')
    return(True)

def reboot_sequence(iterations, ip):
    """
    iterations and IP are passed in via the .txt file referred to in initial CLI.
    """
    try:
        while True:
            number = (int(input('Enter the number of iterations you would ike to run: ')))
            print(number)
    except EOFError:
        pass
    print("The End")
    sys.exit(0)
    #print("WTF!!")
    cs = cofra.SwitchUpdate(ip)
    iteration = iterations
    while iterations >= 1:
        cs.reboot_reconnect()
        iterations -= 1
        cons_out = anturlar.fos_cmd("lsanzoneshow -s | grep Invalid")
        print(cons_out)
        print("NUMBER OF ITERATIONS LEFT: %s" % iterations)
    print("Numer of iterations run without error is %s" % iteration)
    sys.exit(0)
        
def switch_command_loop(iterations):
    while iterations >= 1:
        cmd = anturlar.fos_cmd("lsanzoneshow -s | grep 50:06:01:69:3e:a0:5a:be")
        print(cmd)
        print("ITERATIONS LEFT TO PERFORM: %s" % iterations)
        liabhar.JustSleep(2)
        iterations -= 1   
    print('DONEDONEDONEDONEDONE')
    sys.exit()
    
def timeserversetup():
    cmd = anturlar.fos_cmd("tsclockserver 10.38.2.80; tstimezone America/Denver")
    print(cmd)
    return (cmd)

def autoftpsetup():
    cmd = anturlar.fos_cmd(supportftp -S)
    print(cmd)
        
    
    


    