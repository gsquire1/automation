#!/usr/bin/env python3

###############################################################################
#### Home location is /home/automation/lib/MAPS/
####
###############################################################################

  
def test_case_flow():
    """
        get the current flows on the SUT
        remove the flows
        create the same flows
        
    """
   
    pass

def test_case_config():
    """
        Get MAPS information from the switch so config can be
        put back to the switch
    """
    
    pass

#def genAll():
#    """
#    turn all ports to SIM ports and enable Flow genALL sys test
#    
#    """
#    #### send a fos command to configure
#    capture_cmd = anturlar.fos_cmd("flow --control -portidmode slotport ")
#    cons_out = anturlar.fos_cmd("flow --show")
#
#    si_maps = anturlar.maps()
#    si_maps_sim = si_maps.toggle_all("off")
#    
#    si_maps_gen = si_maps.genAll("on")
#    
#    cons_out = anturlar.fos_cmd("portcfgshow")
#    
#    si_maps_sim = si_maps.toggle_all("on")
#    
#    cons_out = anturlar.fos_cmd("portcfgshow")
#    cons_out = anturlar.fos_cmd("flow --show")
#
#    si_maps_gen = si_maps.genAll("on")
#    cons_out = anturlar.fos_cmd("flow --show")
#    


def ports_disable(portlist = "", t=1, wait=10):
    """
    port disable for the number of time passed in
    
    """
    ####is there a reason to do more than one time from this function
    ####
    if portlist == "":
        myp = anturlar.SwitchInfo()
        portlist = myp.all_ports()
    for x in range(1, t+1):
        for a in portlist:
            cons_out = anturlar.fos_cmd("portdisable %s"%a)
            
def ports_enable(portlist= "", t=1, wait=10):
    """
     port enable for the number of time passed in
     there should be no reason for time to be more than 1
     
    """
    
    if portlist == "":
        myp = anturlar.SwitchInfo()
        portlist = myp.all_ports()
    for x in range(1, t+1):
        for a in portlist:
            cons_out = anturlar.fos_cmd("portenable "+a)
            
def ports_toggle(portlist= "", t=2, wait=10):
    """
      port disable / port enable for the number of times passed in
      
    """
    ####  this is for pizza box
    ####   need to add chassis
    ####
    
    if portlist == "":
        myp = anturlar.SwitchInfo()
        portlist = myp.all_ports()
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
    

       
#def add_remove_flow(repeat, fname, scr, dst, ingrp, egrp, feat):
#    """
#        add and remove a flow from the current switch and FID
#        
#        --should add find one of the ports on the switch and add the flow to
#        that port -
#        --discover which port is the same as the scrdev or dstdev and add
#        -- since this is a add and remove the flow test case the lun, ftype and bidir
#        could be random
#        
#    """
#    ####cmd = "supportsave -n -u %s -p %s -h %s -l ftp -d %s" % (variables, variables)
#    cmd_create = "flow --create %s -fea %s -srcdev %s -dstdev %s" % ( fname,feat,scr,dst)
#    
#    if ingrp != "na":
#        cmd_create = "%s -ingrport %s" % ( cmd_create, ingrp )
#    
#    if egrp != "na":
#        cmd_create = "%s -egrport %s " % ( cmd_create, egrp )
#        
#    cmd_delete = "flow --delete %s " % (fname)
#    
#    cons_out = anturlar.fos_cmd(cmd_create)
#    
#    while repeat > 0:
#        #print(repeat,"\n")
#        cons_out = anturlar.fos_cmd(cmd_create)
#        cons_out = anturlar.fos_cmd("flow --show")
#        
#        liabhar.count_down(3600)
#        
#        cons_out = anturlar.fos_cmd(cmd_delete)
#        cons_out = anturlar.fos_cmd("flow --show")
#        
#        print("\n\n",cons_out)
#        liabhar.count_down(300)
#        
#        repeat = repeat - 1
#        
#    return 0 

#def add_flow(fname, scr, dst, ingrp, egrp, feat):
#    """
#        add a flow from the current switch and FID
#        this will add with the --noactivate option so that it is always added
#        
#        --should add find one of the ports on the switch and add the flow to
#        that port -
#        --discover which port is the same as the scrdev or dstdev and add
#        -- since this is a add and remove the flow test case the lun, ftype and bidir
#        could be random
#        
#    """
#    ####cmd = "supportsave -n -u %s -p %s -h %s -l ftp -d %s" % (variables, variables)
#    cmd_create = "flow --create %s -fea %s " % ( fname,feat)
#    
#    
#    if scr != "b":
#        if scr == "learn":
#            cmd_create = "%s -srcdev '*' " % (cmd_create)    
#        else:
#            cmd_create = "%s -srcdev %s " % (cmd_create, scr)
#        
#    if dst != "b":
#        if dst == "learn":
#            cmd_create = "%s -dstdev '*' " % (cmd_create)    
#        else:
#            cmd_create = "%s -dstdev %s " % (cmd_create, dst)
#        
#    if ingrp != "na":
#        cmd_create = "%s -ingrport %s " % ( cmd_create, ingrp )
#    
#    if egrp != "na":
#        cmd_create = "%s -egrport %s " % ( cmd_create, egrp )
#        
#    cmd_create = "%s -noactivate -%s " % (cmd_create, "bidir")
#    
#    
#    cons_out = anturlar.fos_cmd(cmd_create)
#    cons_out = anturlar.fos_cmd("")
#    
#    #while repeat > 0:
#    #    print("repeat\n")
#    #    repeat = repeat - 1 
#    
#    return 0 
       
#def add_flows_count(fname, scr, dst, ingrp, egrp, feat, cnt):
#    
#    count = 0
#    while count <= cnt:
#        fn = "%s_%s" % (fname,count)
#        add_flow(fn, scr, dst, ingrp, egrp, feat)
#        count += 1
#    
#    return 0
 
#def delete_flow( name ):
#    """
#        delete flow vision flows from a switch
#        
#    """
#    
#    if name == "all":
#        cons_out = anturlar.fos_cmd("echo Y | flow --delete all ")
#    else:
#        cons_out = anturlar.fos_cmd("flow --delete %s" % name)
#    
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
    
#def enable_flows( ones ):
#    """
#        enable all fea of flows of current switch
#        - get the flow names
#        - enable the flows with all features
#        
#    """
#    
#    f = anturlar.FlowV()
#    the_names = f.flow_names()
#    print(the_names)
#    
#    for k in the_names:
#        if "sys_gen_all_simports" in k:
#            print("not enabling this one" , k)
#        else:
#            cmd_create = ("flow --activate %s -fea all" % k )   
#            cons_out = anturlar.fos_cmd(cmd_create)
            
#def check_gen_all_stats():
#    """
#        start the gen_all SIM ports test and capture the number of runs
#        the percent of run, the frames generated brom IngrPort and frames
#        generated to EgrPort
#        
#    """
#    sw_info = anturlar.SwitchInfo()
#    sw_info_ls = sw_info.ls()
#    fid_now = sw_info.ls_now()
#    sw_ip = sw_info.ipaddress()
#    
#    fv = anturlar.FlowV()
#    fv.genAll("on")
#    
#    f = "%s%s%s"%("logs/Gen_all_stats_test_case_file",sw_ip,".txt")
#    clear = 0
#    if clear == 1 :
#        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
#    else:
#        ff = liabhar.FileStuff(f, 'a+b')  #### open for appending
#            
#    st = "Runs  Percent  Ingrport  Egrport \n"        
#    header = "%s%s%s%s" % ("\nGEN ALL CAPTURE FILE \n", "  sw_info ipaddr  ",sw_ip, "\n==============================\n\n")  
#    ff.write(header)
#    ff.write(st)
#    d=0
#    
#    while d <= 1000:
#        stats = fv.genAllStats()
#        print(stats)
#        print("run number  %s" % d)
#        ff.write(stats)
#        liabhar.count_down(60)
#        d += 1
#        
#    ff.close()
        
#def flow_to_each_SIM():
#    """
#        find all the SIM ports in the fabric and create a flow
#        from each SIM port to all the Other SIM ports
#          Since this test case finds all the switches in the
#          fabric it might not be good to run in fabric mode
#        steps
#         1. get the ip list of switches in the fabric
#         2. for each switch get a list of SIM ports
#         3. create a flow for each SIMport to all other SIM ports
#         4. start all of the flows if not started
#         5. if there are only 2 switches only send to the other switch
#            if there are more than 2 switches then send to a random port which
#            could also be on the same switch
#    """
#    
#    sw_info = anturlar.SwitchInfo()
#    fid_now = sw_info.ls_now()
#    cons_out = anturlar.fos_cmd(" ")
#    #sw_ip = sw_info.ipaddress()
#    f = anturlar.FabricInfo()
#    ip_list = f.ipv4_list()
#    ip_count = len(ip_list)
#    ip_c = ip_count
#    
#    combine_port_list = []
#    list_for_j = []
#    list_for_i = []
#    temp_list = []
#        
#    for ip in ip_list:
#        anturlar.connect_tel_noparse(ip,'root','password')
#        s = anturlar.SwitchInfo()
#        cons_out = anturlar.fos_cmd(" ")
#        cons_out = anturlar.fos_cmd("setcontext %s" % (fid_now))
#        ports = s.sim_ports(False)
#        #print("\n\n\n",ports, "\n\n\n")
#        #combine_port_list.append(ports)
#        combine_port_list = combine_port_list + ports
#        if ip_c == 2:
#            list_for_i = ports
#            #print("\n\n\nI list \n")
#            #print(list_for_i)
#            liabhar.count_down(10)
#            ip_c = 1
#        if ip_c == 1:
#            list_for_j = ports
#            #print("\n\n\nJ list \n")
#            #print(list_for_j)
#            liabhar.count_down(10)
#            
#    flow_name_base = "Send_to_each_"
#    count = 0
#     
#    #### need index address for simport 
#    #### now create a flow to each simport
#    #print(combine_port_list)
#    
#    for ip in ip_list:
#        anturlar.connect_tel_noparse(ip,'root','password')
#        s = anturlar.SwitchInfo()
#        cons_out = anturlar.fos_cmd(" ")
#        cons_out = anturlar.fos_cmd("setcontext %s " % (fid_now))
#        cons_out = anturlar.fos_cmd("flow --deact sys_gen_all_simports -fea all")  
#            
#            
#        #### randomize the list
#        combine_port_list = liabhar.randomList(combine_port_list)
#        j_port_list = combine_port_list
#        #print("\n\n\nPORT LIST RANDOMIZED  \n", combine_port_list)
#        #print("\n\n\nNEW LIST RANDOMIZED  \n", new_combine_port_list)
#        if len(ip_list) == 2:
#            #print("\n\n\nyes only two switches\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#            liabhar.count_down(10)
#            random.shuffle(list_for_i)
#            #print("start I list ")
#            for i in list_for_i:
#                random.shuffle(list_for_j)
#                generate_port = i[0]
#                generate_addr = i[1]
#                #print("\n\ngenerator port and address  %s  %s  \n\n" %(generate_port, generate_addr))
#                
#                #### this loops on the same list of combined port list
#                #### one idea was to select a random element from the list each time
#                ####  
#                for j in list_for_j: 
#                    target_port = j[0]
#                    target_addr = j[1]
#                    #print("\n\ntarget port and address  %s  %s \n\n" %( target_port, target_addr))
#                    
#                    if generate_port not in target_port:
#                        flow_name = ("%s%s" % (flow_name_base,count))
#                        count +=1
#                        #print(flow_name, "   " , generate_port," ", generate_addr, "to this port  " ,target_port," ", target_addr)
#                        cmd_create = "flow --create %s -srcdev %s -dstdev %s -ingrport %s -fea gen,mon" % (flow_name, generate_addr,target_addr, generate_port)
#                        cons_out = anturlar.fos_cmd(cmd_create)   
#                        if "maximum limit" in cons_out:
#                            count -= 1
#                            break
#                        if "Port does not" in cons_out:
#                            break
#                        if "PID or WWN do not" in cons_out:
#                            break
#                        if "Exceeds maximum flow limit" in cons_out:
#                            count -= 1
#                            break
#            temp_list = list_for_i
#            list_for_i = list_for_j
#            list_for_j = temp_list
#            
#        else:    
#            for i in combine_port_list:
#                random.shuffle(j_port_list)
#                generate_port = i[0]
#                generate_addr = i[1]
#                #### this loops on the same list of combined port list
#                #### one idea was to select a random element from the list each time
#                ####  
#                for j in j_port_list: 
#                    target_port = j[0]
#                    target_addr = j[1]
#                    if generate_port not in target_port:
#                        flow_name = ("%s%s" % (flow_name_base,count))
#                        count +=1
#                        print(flow_name, "   " , generate_port," ", generate_addr, "to this port  " ,target_port," ", target_addr)
#                        cmd_create = "flow --create %s -srcdev %s -dstdev %s -ingrport %s -fea gen,mon" % (flow_name, generate_addr,target_addr, generate_port)
#                        cons_out = anturlar.fos_cmd(cmd_create)   
#                        if "maximum limit" in cons_out:
#                            count -= 1
#                            break
#                        if "Port does not" in cons_out:
#                            break
#                        if "PID or WWN do not" in cons_out:
#                            break
#                        if "Exceeds maximum flow limit" in cons_out:
#                            count -= 1
#                            break
#    
def mapscommand_list(options="0"):
    """
        returns a list fo the maps commands
        send true to recieve the list of options for each command
        pass the options of 0 , usage or all
        0 - or blank will use the core commands only
        usage - will use commands that will return the help list
        all   - will use commands that will function correctly
        
    """
    l = ["mapsConfig", "mapsPolicy", "mapsHelp", "mapsRule", \
         "mapsconfig", "mapspolicy", "mapshelp", "mapsrule", \
         "mapsdb", "mapssam"]
    
    if options == "usage":
        #### these commands will return a usage message since they are
        ####  not in the correct format
        #### maybe add the next line to be the correct response
        ####
        l = ["mapsConfig -- ", \
             "mapsconfig --config pause -type NO_port -members 0", \
             "mapsconfig --config continue -type YES_port -members 0", \
             "mapsconfig --emailcfg smckie@brocade.com", \
             "mapsconfig --emailcfg ", \
             "mapsconfig --actions ", \
             "mapsconfig --import  ", \
             "mapsconfig --deimport ", \
             "mapsconfig --enablemaps ", \
             "mapsconfig --No_purge", \
             "mapsconfig -", \
             #"mapsconfig --enableFPImon", \   #### commented out because it
             #"mapsconfig --disableFPImon", \  #### is the correct command
             "mapsconfig --help", \
             "mapspolicy --create  ", \
             "mapspolicy --", \
             "mapspolicy --enable  ", \
             "mapspolicy --addrule test_policy -rulename ", \
             "mapspolicy --delrule test_policy -rulename ", \
             "mapspolicy --delete   ", \
             "mapsRule --create  ", \
             "mapsRule --config  ", \
             "mapsRule --delete  ", \
             "mapsRule --", \
             "mapsRule --help ", \
             "mapssam -- ", \
             "mapssam --show cpu", \
             "mapssam --show memory", \
             "mapssam --show flash", \
             "mapssam --help", \
             "mapsdb -- ", \
             "mapsdb --show everything", \
             "mapsdb --show abunchof28284204", \
             "mapsdb --clear  ", \
        ]
    
    if options == "all":
        #### these commands should complete without error
        ####
        
        sbj = "this is a test email from maps"
        msg = "this is the body of the email from maps"
        
        l = ["mapsConfig --show", \
             "mapsconfig --config pause -type port -members 0", \
             "mapsconfig --config continue -type port -members 0", \
             "mapsconfig --emailcfg -address smckie@brocade.com", \
             "mapsconfig --actions none", \
             "mapsconfig --testmail -subject $sbj -message $msg", \
             "mapsconfig --import someflowname ", \
             "mapsconfig --deimport someflowname", \
             "echo n | mapsconfig --enablemaps -policy dflt_conservative_policy", \
             "mapsconfig --", \
             "mapsconfig --show", \
             "mapsconfig --enableFPImon", \
             "mapsconfig --disableFPImon", \
             "mapsconfig --help", \
             "mapspolicy --create test_policy", \
             "mapspolicy --show -summary", \
             "mapspolicy --enable test_policy", \
             "mapspolicy --clone test_policy -name test_policy_clone", \
             "mapspolicy --addrule test_policy -rulename ", \
             "mapspolicy --delrule test_policy -rulename ", \
             "mapspolicy --delete test_policy ", \
             "mapspolicy --delete test_policy_clone",\
             "mapsRule --create rule_00 ", \
             "mapsRule --config rule_00", \
             "mapsRule --clone rule_00 -rulename rule_00_clone", \
             "mapsRule --delete rule_00", \
             "mapsrule --delete rule_00_clone", \
             "mapsRule --show <ruleName | -all>", \
             "mapsRule --help ", \
             "mapssam --show ", \
             "mapssam --show cpu", \
             "mapssam --show memory", \
             "mapssam --show flash", \
             "mapssam --clear", \
             "mapssam --help", \
             "mapsdb --show ", \
             "mapsdb --show all", \
             "mapsdb --show history ", \
             "mapsdb --show details ", \
             "echo n | mapsdb --clear summary ", \
             "echo n | mapsdb --clear history ", \
             "echo n | mapsdb --clear all ", \
        ]
        
    return(l)

def maps_default_rule():
    ####
    ####  list of all the rules including director only rules
    ####  
    l = "   defNON_E_F_PORTSCRC_0                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(CRC/MIN>0),\
            defNON_E_F_PORTSCRC_2                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(CRC/MIN>2),\
            defNON_E_F_PORTSCRC_10                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(CRC/MIN>10),\
            defNON_E_F_PORTSCRC_20                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(CRC/MIN>20),\
            defNON_E_F_PORTSCRC_21                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(CRC/MIN>21),\
            defNON_E_F_PORTSCRC_40                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(CRC/MIN>40),\
            defNON_E_F_PORTSITW_15                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(ITW/MIN>15),\
            defNON_E_F_PORTSITW_20                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(ITW/MIN>20),\
            defNON_E_F_PORTSITW_21                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(ITW/MIN>21),\
            defNON_E_F_PORTSITW_40                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(ITW/MIN>40),\
            defNON_E_F_PORTSITW_41                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(ITW/MIN>41),\
            defNON_E_F_PORTSITW_80                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(ITW/MIN>80),\
            defNON_E_F_PORTSLR_2                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LR/MIN>2),\
            defNON_E_F_PORTSLR_4                    |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(LR/MIN>4),\
            defNON_E_F_PORTSLR_5                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LR/MIN>5),\
            defNON_E_F_PORTSLR_10                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(LR/MIN>10),\
            defNON_E_F_PORTSLR_11                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LR/MIN>11),\
            defNON_E_F_PORTSLR_20                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(LR/MIN>20),\
            defNON_E_F_PORTSSTATE_CHG_2             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(STATE_CHG/MIN>2),\
            defNON_E_F_PORTSSTATE_CHG_4             |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(STATE_CHG/MIN>4),\
            defNON_E_F_PORTSSTATE_CHG_5             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(STATE_CHG/MIN>5),\
            defNON_E_F_PORTSSTATE_CHG_10            |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(STATE_CHG/MIN>10),\
            defNON_E_F_PORTSSTATE_CHG_11            |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(STATE_CHG/MIN>11),\
            defNON_E_F_PORTSSTATE_CHG_20            |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(STATE_CHG/MIN>20),\
            defNON_E_F_PORTSLOSS_SIGNAL_0           |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SIGNAL/MIN>0),\
            defNON_E_F_PORTSLOSS_SIGNAL_3           |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SIGNAL/MIN>3),\
            defNON_E_F_PORTSLOSS_SIGNAL_5           |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SIGNAL/MIN>5),\
            defNON_E_F_PORTSPE_0                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(PE/MIN>0),\
            defNON_E_F_PORTSPE_2                    |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(PE/MIN>2),\
            defNON_E_F_PORTSPE_3                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(PE/MIN>3),\
            defNON_E_F_PORTSPE_7                    |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(PE/MIN>7),\
            defNON_E_F_PORTSPE_5                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(PE/MIN>5),\
            defNON_E_F_PORTSPE_10                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(PE/MIN>10),\
            defNON_E_F_PORTSLF_0                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LF/MIN>0),\
            defNON_E_F_PORTSLF_3                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LF/MIN>3),\
            defNON_E_F_PORTSLF_5                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LF/MIN>5),\
            defNON_E_F_PORTSLOSS_SYNC_0             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SYNC/MIN>0),\
            defNON_E_F_PORTSLOSS_SYNC_3             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SYNC/MIN>3),\
            defNON_E_F_PORTSLOSS_SYNC_5             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SYNC/MIN>5),\
            defNON_E_F_PORTSRX_60                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(RX/HOUR>60),\
            defNON_E_F_PORTSRX_75                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(RX/HOUR>75),\
            defNON_E_F_PORTSRX_90                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(RX/HOUR>90),\
            defNON_E_F_PORTSTX_60                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(TX/HOUR>60),\
            defNON_E_F_PORTSTX_75                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(TX/HOUR>75),\
            defNON_E_F_PORTSTX_90                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(TX/HOUR>90),\
            defNON_E_F_PORTSUTIL_60                 |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(UTIL/HOUR>60),\
            defNON_E_F_PORTSUTIL_75                 |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(UTIL/HOUR>75),\
            defNON_E_F_PORTSUTIL_90                 |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(UTIL/HOUR>90),\
            defALL_HOST_PORTSCRC_0                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(CRC/MIN>0),\
            defALL_HOST_PORTSCRC_2                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(CRC/MIN>2),\
            defALL_HOST_PORTSCRC_10                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(CRC/MIN>10),\
            defALL_HOST_PORTSCRC_20                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(CRC/MIN>20),\
            defALL_HOST_PORTSCRC_21                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(CRC/MIN>21),\
            defALL_HOST_PORTSCRC_40                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(CRC/MIN>40),\
            defALL_HOST_PORTSITW_15                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(ITW/MIN>15),\
            defALL_HOST_PORTSITW_20                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(ITW/MIN>20),\
            defALL_HOST_PORTSITW_21                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(ITW/MIN>21),\
            defALL_HOST_PORTSITW_40                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(ITW/MIN>40),\
            defALL_HOST_PORTSITW_41                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(ITW/MIN>41),\
            defALL_HOST_PORTSITW_80                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(ITW/MIN>80),\
            defALL_HOST_PORTSLR_2                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LR/MIN>2),\
            defALL_HOST_PORTSLR_4                   |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(LR/MIN>4),\
            defALL_HOST_PORTSLR_5                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LR/MIN>5),\
            defALL_HOST_PORTSLR_10                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(LR/MIN>10),\
            defALL_HOST_PORTSLR_11                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LR/MIN>11),\
            defALL_HOST_PORTSLR_20                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(LR/MIN>20),\
            defALL_HOST_PORTSSTATE_CHG_2            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(STATE_CHG/MIN>2),\
            defALL_HOST_PORTSSTATE_CHG_4            |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(STATE_CHG/MIN>4),\
            defALL_HOST_PORTSSTATE_CHG_5            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(STATE_CHG/MIN>5),\
            defALL_HOST_PORTSSTATE_CHG_10           |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(STATE_CHG/MIN>10),\
            defALL_HOST_PORTSSTATE_CHG_11           |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(STATE_CHG/MIN>11),\
            defALL_HOST_PORTSSTATE_CHG_20           |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(STATE_CHG/MIN>20),\
            defALL_HOST_PORTSLOSS_SIGNAL_0          |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SIGNAL/MIN>0),\
            defALL_HOST_PORTSLOSS_SIGNAL_3          |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SIGNAL/MIN>3),\
            defALL_HOST_PORTSLOSS_SIGNAL_5          |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SIGNAL/MIN>5),\
            defALL_HOST_PORTSPE_0                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(PE/MIN>0),\
            defALL_HOST_PORTSPE_2                   |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(PE/MIN>2),\
            defALL_HOST_PORTSPE_3                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(PE/MIN>3),\
            defALL_HOST_PORTSPE_7                   |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(PE/MIN>7),\
            defALL_HOST_PORTSPE_5                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(PE/MIN>5),\
            defALL_HOST_PORTSPE_10                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(PE/MIN>10),\
            defALL_HOST_PORTSLF_0                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LF/MIN>0),\
            defALL_HOST_PORTSLF_3                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LF/MIN>3),\
            defALL_HOST_PORTSLF_5                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LF/MIN>5),\
            defALL_HOST_PORTSLOSS_SYNC_0            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SYNC/MIN>0),\
            defALL_HOST_PORTSLOSS_SYNC_3            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SYNC/MIN>3),\
            defALL_HOST_PORTSLOSS_SYNC_5            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SYNC/MIN>5),\
            defALL_HOST_PORTSRX_60                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(RX/HOUR>60),\
            defALL_HOST_PORTSRX_75                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(RX/HOUR>75),\
            defALL_HOST_PORTSRX_90                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(RX/HOUR>90),\
            defALL_HOST_PORTSTX_60                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(TX/HOUR>60),\
            defALL_HOST_PORTSTX_75                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(TX/HOUR>75),\
            defALL_HOST_PORTSTX_90                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(TX/HOUR>90),\
            defALL_HOST_PORTSUTIL_60                |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(UTIL/HOUR>60),\
            defALL_HOST_PORTSUTIL_75                |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(UTIL/HOUR>75),\
            defALL_HOST_PORTSUTIL_90                |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(UTIL/HOUR>90),\
            defALL_OTHER_F_PORTSCRC_0               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(CRC/MIN>0),\
            defALL_OTHER_F_PORTSCRC_2               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(CRC/MIN>2),\
            defALL_OTHER_F_PORTSCRC_10              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(CRC/MIN>10),\
            defALL_OTHER_F_PORTSCRC_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(CRC/MIN>20),\
            defALL_OTHER_F_PORTSCRC_21              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(CRC/MIN>21),\
            defALL_OTHER_F_PORTSCRC_40              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(CRC/MIN>40),\
            defALL_OTHER_F_PORTSITW_15              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(ITW/MIN>15),\
            defALL_OTHER_F_PORTSITW_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(ITW/MIN>20),\
            defALL_OTHER_F_PORTSITW_21              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(ITW/MIN>21),\
            defALL_OTHER_F_PORTSITW_40              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(ITW/MIN>40),\
            defALL_OTHER_F_PORTSITW_41              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(ITW/MIN>41),\
            defALL_OTHER_F_PORTSITW_80              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(ITW/MIN>80),\
            defALL_OTHER_F_PORTSLR_2                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LR/MIN>2),\
            defALL_OTHER_F_PORTSLR_4                |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(LR/MIN>4),\
            defALL_OTHER_F_PORTSLR_5                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LR/MIN>5),\
            defALL_OTHER_F_PORTSLR_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(LR/MIN>10),\
            defALL_OTHER_F_PORTSLR_11               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LR/MIN>11),\
            defALL_OTHER_F_PORTSLR_20               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(LR/MIN>20),\
            defALL_OTHER_F_PORTSSTATE_CHG_2         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(STATE_CHG/MIN>2),\
            defALL_OTHER_F_PORTSSTATE_CHG_4         |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(STATE_CHG/MIN>4),\
            defALL_OTHER_F_PORTSSTATE_CHG_5         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(STATE_CHG/MIN>5),\
            defALL_OTHER_F_PORTSSTATE_CHG_10        |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(STATE_CHG/MIN>10),\
            defALL_OTHER_F_PORTSSTATE_CHG_11        |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(STATE_CHG/MIN>11),\
            defALL_OTHER_F_PORTSSTATE_CHG_20        |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(STATE_CHG/MIN>20),\
            defALL_OTHER_F_PORTSLOSS_SIGNAL_0       |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>0),\
            defALL_OTHER_F_PORTSLOSS_SIGNAL_3       |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>3),\
            defALL_OTHER_F_PORTSLOSS_SIGNAL_5       |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>5),\
            defALL_OTHER_F_PORTSPE_0                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(PE/MIN>0),\
            defALL_OTHER_F_PORTSPE_2                |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(PE/MIN>2),\
            defALL_OTHER_F_PORTSPE_3                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(PE/MIN>3),\
            defALL_OTHER_F_PORTSPE_7                |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(PE/MIN>7),\
            defALL_OTHER_F_PORTSPE_5                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(PE/MIN>5),\
            defALL_OTHER_F_PORTSPE_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(PE/MIN>10),\
            defALL_OTHER_F_PORTSLF_0                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LF/MIN>0),\
            defALL_OTHER_F_PORTSLF_3                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LF/MIN>3),\
            defALL_OTHER_F_PORTSLF_5                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LF/MIN>5),\
            defALL_OTHER_F_PORTSLOSS_SYNC_0         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>0),\
            defALL_OTHER_F_PORTSLOSS_SYNC_3         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>3),\
            defALL_OTHER_F_PORTSLOSS_SYNC_5         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>5),\
            defALL_OTHER_F_PORTSRX_60               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(RX/HOUR>60),\
            defALL_OTHER_F_PORTSRX_75               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(RX/HOUR>75),\
            defALL_OTHER_F_PORTSRX_90               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(RX/HOUR>90),\
            defALL_OTHER_F_PORTSTX_60               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(TX/HOUR>60),\
            defALL_OTHER_F_PORTSTX_75               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(TX/HOUR>75),\
            defALL_OTHER_F_PORTSTX_90               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(TX/HOUR>90),\
            defALL_OTHER_F_PORTSUTIL_60             |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(UTIL/HOUR>60),\
            defALL_OTHER_F_PORTSUTIL_75             |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(UTIL/HOUR>75),\
            defALL_OTHER_F_PORTSUTIL_90             |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(UTIL/HOUR>90),\
            defALL_HOST_PORTSC3TXTO_2               |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(C3TXTO/MIN>2),\
            defALL_HOST_PORTSC3TXTO_4               |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(C3TXTO/MIN>4),\
            defALL_HOST_PORTSC3TXTO_3               |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(C3TXTO/MIN>3),\
            defALL_HOST_PORTSC3TXTO_10              |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(C3TXTO/MIN>10),\
            defALL_HOST_PORTSC3TXTO_11              |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(C3TXTO/MIN>11),\
            defALL_HOST_PORTSC3TXTO_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(C3TXTO/MIN>20),\
            defALL_OTHER_F_PORTSC3TXTO_2            |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(C3TXTO/MIN>2),\
            defALL_OTHER_F_PORTSC3TXTO_4            |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(C3TXTO/MIN>4),\
            defALL_OTHER_F_PORTSC3TXTO_3            |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(C3TXTO/MIN>3),\
            defALL_OTHER_F_PORTSC3TXTO_10           |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(C3TXTO/MIN>10),\
            defALL_OTHER_F_PORTSC3TXTO_11           |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(C3TXTO/MIN>11),\
            defALL_OTHER_F_PORTSC3TXTO_20           |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(C3TXTO/MIN>20),\
            defALL_E_PORTSCRC_0                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(CRC/MIN>0),\
            defALL_E_PORTSCRC_2                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(CRC/MIN>2),\
            defALL_E_PORTSCRC_10                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(CRC/MIN>10),\
            defALL_E_PORTSCRC_20                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(CRC/MIN>20),\
            defALL_E_PORTSCRC_21                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(CRC/MIN>21),\
            defALL_E_PORTSCRC_40                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(CRC/MIN>40),\
            defALL_E_PORTSITW_15                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(ITW/MIN>15),\
            defALL_E_PORTSITW_20                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(ITW/MIN>20),\
            defALL_E_PORTSITW_21                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(ITW/MIN>21),\
            defALL_E_PORTSITW_40                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(ITW/MIN>40),\
            defALL_E_PORTSITW_41                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(ITW/MIN>41),\
            defALL_E_PORTSITW_80                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(ITW/MIN>80),\
            defALL_E_PORTSLR_2                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LR/MIN>2),\
            defALL_E_PORTSLR_4                      |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(LR/MIN>4),\
            defALL_E_PORTSLR_5                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LR/MIN>5),\
            defALL_E_PORTSLR_10                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(LR/MIN>10),\
            defALL_E_PORTSLR_11                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LR/MIN>11),\
            defALL_E_PORTSLR_20                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(LR/MIN>20),\
            defALL_E_PORTSSTATE_CHG_2               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(STATE_CHG/MIN>2),\
            defALL_E_PORTSSTATE_CHG_4               |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(STATE_CHG/MIN>4),\
            defALL_E_PORTSSTATE_CHG_5               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(STATE_CHG/MIN>5),\
            defALL_E_PORTSSTATE_CHG_10              |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(STATE_CHG/MIN>10),\
            defALL_E_PORTSSTATE_CHG_11              |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(STATE_CHG/MIN>11),\
            defALL_E_PORTSSTATE_CHG_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(STATE_CHG/MIN>20),\
            defALL_E_PORTSLOSS_SIGNAL_0             |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SIGNAL/MIN>0),\
            defALL_E_PORTSLOSS_SIGNAL_3             |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SIGNAL/MIN>3),\
            defALL_E_PORTSLOSS_SIGNAL_5             |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SIGNAL/MIN>5),\
            defALL_E_PORTSPE_0                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(PE/MIN>0),\
            defALL_E_PORTSPE_2                      |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(PE/MIN>2),\
            defALL_E_PORTSPE_3                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(PE/MIN>3),\
            defALL_E_PORTSPE_7                      |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(PE/MIN>7),\
            defALL_E_PORTSPE_5                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(PE/MIN>5),\
            defALL_E_PORTSPE_10                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(PE/MIN>10),\
            defALL_E_PORTSLF_0                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LF/MIN>0),\
            defALL_E_PORTSLF_3                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LF/MIN>3),\
            defALL_E_PORTSLF_5                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LF/MIN>5),\
            defALL_E_PORTSLOSS_SYNC_0               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SYNC/MIN>0),\
            defALL_E_PORTSLOSS_SYNC_3               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SYNC/MIN>3),\
            defALL_E_PORTSLOSS_SYNC_5               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SYNC/MIN>5),\
            defALL_E_PORTSRX_60                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(RX/HOUR>60),\
            defALL_E_PORTSRX_75                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(RX/HOUR>75),\
            defALL_E_PORTSRX_90                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(RX/HOUR>90),\
            defALL_E_PORTSTX_60                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(TX/HOUR>60),\
            defALL_E_PORTSTX_75                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(TX/HOUR>75),\
            defALL_E_PORTSTX_90                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(TX/HOUR>90),\
            defALL_E_PORTSUTIL_60                   |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(UTIL/HOUR>60),\
            defALL_E_PORTSUTIL_75                   |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(UTIL/HOUR>75),\
            defALL_E_PORTSUTIL_90                   |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(UTIL/HOUR>90),\
            defALL_E_PORTSC3TXTO_5                  |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(C3TXTO/MIN>5),\
            defALL_E_PORTSC3TXTO_10                 |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(C3TXTO/MIN>10),\
            defALL_E_PORTSC3TXTO_20                 |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(C3TXTO/MIN>20),\
            defALL_TARGET_PORTSC3TXTO_0             |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(C3TXTO/MIN>0),\
            defALL_TARGET_PORTSC3TXTO_2             |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(C3TXTO/MIN>2),\
            defALL_TARGET_PORTSC3TXTO_3             |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(C3TXTO/MIN>3),\
            defALL_TARGET_PORTSC3TXTO_5             |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(C3TXTO/MIN>5),\
            defALL_TARGET_PORTSC3TXTO_6             |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(C3TXTO/MIN>6),\
            defALL_TARGET_PORTSC3TXTO_10            |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(C3TXTO/MIN>10),\
            defALL_TARGET_PORTSCRC_0                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(CRC/MIN>0),\
            defALL_TARGET_PORTSCRC_2                |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(CRC/MIN>2),\
            defALL_TARGET_PORTSCRC_5                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(CRC/MIN>5),\
            defALL_TARGET_PORTSCRC_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(CRC/MIN>10),\
            defALL_TARGET_PORTSCRC_11               |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(CRC/MIN>11),\
            defALL_TARGET_PORTSCRC_20               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(CRC/MIN>20),\
            defALL_TARGET_PORTSITW_5                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(ITW/MIN>5),\
            defALL_TARGET_PORTSITW_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(ITW/MIN>10),\
            defALL_TARGET_PORTSITW_11               |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(ITW/MIN>11),\
            defALL_TARGET_PORTSITW_20               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(ITW/MIN>20),\
            defALL_TARGET_PORTSITW_21               |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(ITW/MIN>21),\
            defALL_TARGET_PORTSITW_40               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(ITW/MIN>40),\
            defALL_TARGET_PORTSLR_0                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LR/MIN>0),\
            defALL_TARGET_PORTSLR_2                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(LR/MIN>2),\
            defALL_TARGET_PORTSLR_3                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LR/MIN>3),\
            defALL_TARGET_PORTSLR_5                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(LR/MIN>5),\
            defALL_TARGET_PORTSLR_6                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LR/MIN>6),\
            defALL_TARGET_PORTSLR_10                |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(LR/MIN>10),\
            defALL_TARGET_PORTSSTATE_CHG_0          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(STATE_CHG/MIN>0),\
            defALL_TARGET_PORTSSTATE_CHG_2          |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(STATE_CHG/MIN>2),\
            defALL_TARGET_PORTSSTATE_CHG_3          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(STATE_CHG/MIN>3),\
            defALL_TARGET_PORTSSTATE_CHG_7          |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(STATE_CHG/MIN>7),\
            defALL_TARGET_PORTSSTATE_CHG_8          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(STATE_CHG/MIN>8),\
            defALL_TARGET_PORTSSTATE_CHG_15         |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(STATE_CHG/MIN>15),\
            defALL_TARGET_PORTSLOSS_SIGNAL_0        |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>0),\
            defALL_TARGET_PORTSLOSS_SIGNAL_3        |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>3),\
            defALL_TARGET_PORTSLOSS_SIGNAL_5        |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>5),\
            defALL_TARGET_PORTSPE_0                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(PE/MIN>0),\
            defALL_TARGET_PORTSPE_2                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(PE/MIN>2),\
            defALL_TARGET_PORTSPE_3                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(PE/MIN>3),\
            defALL_TARGET_PORTSPE_4                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(PE/MIN>4),\
            defALL_TARGET_PORTSPE_5                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(PE/MIN>5),\
            defALL_TARGET_PORTSPE_6                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(PE/MIN>6),\
            defALL_TARGET_PORTSLF_0                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LF/MIN>0),\
            defALL_TARGET_PORTSLF_3                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LF/MIN>3),\
            defALL_TARGET_PORTSLF_5                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LF/MIN>5),\
            defALL_TARGET_PORTSLOSS_SYNC_0          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SYNC/MIN>0),\
            defALL_TARGET_PORTSLOSS_SYNC_3          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SYNC/MIN>3),\
            defALL_TARGET_PORTSLOSS_SYNC_5          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SYNC/MIN>5),\
            defALL_TARGET_PORTSRX_60                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(RX/HOUR>60),\
            defALL_TARGET_PORTSRX_75                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(RX/HOUR>75),\
            defALL_TARGET_PORTSRX_90                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(RX/HOUR>90),\
            defALL_TARGET_PORTSTX_60                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(TX/HOUR>60),\
            defALL_TARGET_PORTSTX_75                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(TX/HOUR>75),\
            defALL_TARGET_PORTSTX_90                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(TX/HOUR>90),\
            defALL_TARGET_PORTSUTIL_60              |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(UTIL/HOUR>60),\
            defALL_TARGET_PORTSUTIL_75              |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(UTIL/HOUR>75),\
            defALL_TARGET_PORTSUTIL_90              |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(UTIL/HOUR>90),\
            defALL_CIRCUITSCIR_STATE_0              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_STATE/MIN>0),\
            defALL_CIRCUITSCIR_STATE_3              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_STATE/MIN>3),\
            defALL_CIRCUITSCIR_STATE_5              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_STATE/MIN>5),\
            defALL_CIRCUITSCIR_UTIL_60              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_UTIL/MIN>60),\
            defALL_CIRCUITSCIR_UTIL_75              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_UTIL/MIN>75),\
            defALL_CIRCUITSCIR_UTIL_90              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_UTIL/MIN>90),\
            defALL_CIRCUITSCIR_PKTLOSS_PER_01       |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.01),\
            defALL_CIRCUITSCIR_PKTLOSS_PER_05       |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.05),\
            defALL_CIRCUITSCIR_PKTLOSS_PER_1        |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.1),\
            defSWITCHEPORT_DOWN_1                   |RASLOG,SNMP,EMAIL            |SWITCH(EPORT_DOWN/MIN>1),\
            defSWITCHEPORT_DOWN_2                   |RASLOG,SNMP,EMAIL            |SWITCH(EPORT_DOWN/MIN>2),\
            defSWITCHEPORT_DOWN_4                   |RASLOG,SNMP,EMAIL            |SWITCH(EPORT_DOWN/MIN>4),\
            defSWITCHFAB_CFG_1                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_CFG/MIN>1),\
            defSWITCHFAB_CFG_2                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_CFG/MIN>2),\
            defSWITCHFAB_CFG_4                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_CFG/MIN>4),\
            defSWITCHFAB_SEG_1                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_SEG/MIN>1),\
            defSWITCHFAB_SEG_2                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_SEG/MIN>2),\
            defSWITCHFAB_SEG_4                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_SEG/MIN>4),\
            defSWITCHFLOGI_4                        |RASLOG,SNMP,EMAIL            |SWITCH(FLOGI/MIN>4),\
            defSWITCHFLOGI_6                        |RASLOG,SNMP,EMAIL            |SWITCH(FLOGI/MIN>6),\
            defSWITCHFLOGI_8                        |RASLOG,SNMP,EMAIL            |SWITCH(FLOGI/MIN>8),\
            defSWITCHZONE_CHG_2                     |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CHG/DAY>2),\
            defSWITCHZONE_CHG_5                     |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CHG/DAY>5),\
            defSWITCHZONE_CHG_10                    |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CHG/DAY>10),\
            defSWITCHDID_CHG_1                      |RASLOG,SNMP,EMAIL            |SWITCH(DID_CHG/MIN>1),\
            defSWITCHL2_DEVCNT_PER_60               |RASLOG,SNMP,EMAIL            |SWITCH(L2_DEVCNT_PER/NONE>60),\
            defSWITCHL2_DEVCNT_PER_75               |RASLOG,SNMP,EMAIL            |SWITCH(L2_DEVCNT_PER/NONE>75),\
            defSWITCHL2_DEVCNT_PER_90               |RASLOG,SNMP,EMAIL            |SWITCH(L2_DEVCNT_PER/NONE>90),\
            defSWITCHLSAN_DEVCNT_PER_60             |RASLOG,SNMP,EMAIL            |SWITCH(LSAN_DEVCNT_PER/NONE>60),\
            defSWITCHLSAN_DEVCNT_PER_75             |RASLOG,SNMP,EMAIL            |SWITCH(LSAN_DEVCNT_PER/NONE>75),\
            defSWITCHLSAN_DEVCNT_PER_90             |RASLOG,SNMP,EMAIL            |SWITCH(LSAN_DEVCNT_PER/NONE>90),\
            defSWITCHZONE_CFGSZ_PER_70              |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CFGSZ_PER/NONE>70),\
            defSWITCHZONE_CFGSZ_PER_80              |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CFGSZ_PER/NONE>80),\
            defSWITCHZONE_CFGSZ_PER_90              |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CFGSZ_PER/NONE>90),\
            defSWITCHBB_FCR_CNT_12                  |RASLOG,SNMP,EMAIL            |SWITCH(BB_FCR_CNT/NONE>12),\
            defSWITCHSEC_TELNET_0                   |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TELNET/MIN>0),\
            defSWITCHSEC_TELNET_2                   |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TELNET/MIN>2),\
            defSWITCHSEC_TELNET_4                   |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TELNET/MIN>4),\
            defSWITCHSEC_HTTP_0                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_HTTP/MIN>0),\
            defSWITCHSEC_HTTP_2                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_HTTP/MIN>2),\
            defSWITCHSEC_HTTP_4                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_HTTP/MIN>4),\
            defSWITCHSEC_SCC_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_SCC/MIN>0),\
            defSWITCHSEC_SCC_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_SCC/MIN>2),\
            defSWITCHSEC_SCC_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_SCC/MIN>4),\
            defSWITCHSEC_DCC_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_DCC/MIN>0),\
            defSWITCHSEC_DCC_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_DCC/MIN>2),\
            defSWITCHSEC_DCC_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_DCC/MIN>4),\
            defSWITCHSEC_LV_0                       |RASLOG,SNMP,EMAIL            |SWITCH(SEC_LV/MIN>0),\
            defSWITCHSEC_LV_2                       |RASLOG,SNMP,EMAIL            |SWITCH(SEC_LV/MIN>2),\
            defSWITCHSEC_LV_4                       |RASLOG,SNMP,EMAIL            |SWITCH(SEC_LV/MIN>4),\
            defSWITCHSEC_CERT_0                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CERT/MIN>0),\
            defSWITCHSEC_CERT_2                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CERT/MIN>2),\
            defSWITCHSEC_CERT_4                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CERT/MIN>4),\
            defSWITCHSEC_AUTH_FAIL_0                |RASLOG,SNMP,EMAIL            |SWITCH(SEC_AUTH_FAIL/MIN>0),\
            defSWITCHSEC_AUTH_FAIL_2                |RASLOG,SNMP,EMAIL            |SWITCH(SEC_AUTH_FAIL/MIN>2),\
            defSWITCHSEC_AUTH_FAIL_4                |RASLOG,SNMP,EMAIL            |SWITCH(SEC_AUTH_FAIL/MIN>4),\
            defSWITCHSEC_FCS_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_FCS/MIN>0),\
            defSWITCHSEC_FCS_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_FCS/MIN>2),\
            defSWITCHSEC_FCS_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_FCS/MIN>4),\
            defSWITCHSEC_IDB_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_IDB/MIN>0),\
            defSWITCHSEC_IDB_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_IDB/MIN>2),\
            defSWITCHSEC_IDB_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_IDB/MIN>4),\
            defSWITCHSEC_CMD_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CMD/MIN>0),\
            defSWITCHSEC_CMD_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CMD/MIN>2),\
            defSWITCHSEC_CMD_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CMD/MIN>4),\
            defSWITCHSEC_TS_H1                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/HOUR>1),\
            defSWITCHSEC_TS_H2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/HOUR>2),\
            defSWITCHSEC_TS_H4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/HOUR>4),\
            defSWITCHSEC_TS_D2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/DAY>2),\
            defSWITCHSEC_TS_D4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/DAY>4),\
            defSWITCHSEC_TS_D10                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/DAY>10),\
            defALL_TSTEMP_OUT_OF_RANGE              |RASLOG,SNMP,EMAIL            |ALL_TS(TEMP/NONE==OUT_OF_RANGE),\
            defALL_OTHER_SFPCURRENT_50              |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(CURRENT/NONE>=50),\
            defALL_OTHER_SFPVOLTAGE_3630            |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(VOLTAGE/NONE>=3630),\
            defALL_OTHER_SFPRXP_5000                |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(RXP/NONE>=5000),\
            defALL_OTHER_SFPTXP_5000                |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(TXP/NONE>=5000),\
            defALL_OTHER_SFPSFP_TEMP_85             |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(SFP_TEMP/NONE>=85),\
            defALL_OTHER_SFPVOLTAGE_2960            |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(VOLTAGE/NONE<=2960),\
            defALL_OTHER_SFPSFP_TEMP_n13            |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(SFP_TEMP/NONE<=-13),\
            defALL_10GSWL_SFPCURRENT_10             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(CURRENT/NONE>=10),\
            defALL_10GSWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(VOLTAGE/NONE>=3600),\
            defALL_10GSWL_SFPRXP_1999               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(RXP/NONE>=1999),\
            defALL_10GSWL_SFPTXP_1999               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(TXP/NONE>=1999),\
            defALL_10GSWL_SFPSFP_TEMP_90            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(SFP_TEMP/NONE>=90),\
            defALL_10GSWL_SFPVOLTAGE_3000           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(VOLTAGE/NONE<=3000),\
            defALL_10GSWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(SFP_TEMP/NONE<=-5),\
            defALL_10GLWL_SFPCURRENT_95             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(CURRENT/NONE>=95),\
            defALL_10GLWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(VOLTAGE/NONE>=3600),\
            defALL_10GLWL_SFPRXP_2230               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(RXP/NONE>=2230),\
            defALL_10GLWL_SFPTXP_2230               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(TXP/NONE>=2230),\
            defALL_10GLWL_SFPSFP_TEMP_90            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(SFP_TEMP/NONE>=90),\
            defALL_10GLWL_SFPVOLTAGE_2970           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(VOLTAGE/NONE<=2970),\
            defALL_10GLWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(SFP_TEMP/NONE<=-5),\
            defALL_16GSWL_SFPCURRENT_12             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(CURRENT/NONE>=12),\
            defALL_16GSWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(VOLTAGE/NONE>=3600),\
            defALL_16GSWL_SFPRXP_1259               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(RXP/NONE>=1259),\
            defALL_16GSWL_SFPTXP_1259               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(TXP/NONE>=1259),\
            defALL_16GSWL_SFPSFP_TEMP_85            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(SFP_TEMP/NONE>=85),\
            defALL_16GSWL_SFPVOLTAGE_3000           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(VOLTAGE/NONE<=3000),\
            defALL_16GSWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(SFP_TEMP/NONE<=-5),\
            defALL_16GLWL_SFPCURRENT_70             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(CURRENT/NONE>=70),\
            defALL_16GLWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(VOLTAGE/NONE>=3600),\
            defALL_16GLWL_SFPRXP_1995               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(RXP/NONE>=1995),\
            defALL_16GLWL_SFPTXP_1995               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(TXP/NONE>=1995),\
            defALL_16GLWL_SFPSFP_TEMP_90            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(SFP_TEMP/NONE>=90),\
            defALL_16GLWL_SFPVOLTAGE_3000           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(VOLTAGE/NONE<=3000),\
            defALL_16GLWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(SFP_TEMP/NONE<=-5),\
            defALL_QSFPCURRENT_10                   |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(CURRENT/NONE>=10),\
            defALL_QSFPVOLTAGE_3600                 |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(VOLTAGE/NONE>=3600),\
            defALL_QSFPRXP_2180                     |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(RXP/NONE>=2180),\
            defALL_QSFPSFP_TEMP_85                  |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(SFP_TEMP/NONE>=85),\
            defALL_QSFPVOLTAGE_2940                 |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(VOLTAGE/NONE<=2940),\
            defALL_QSFPSFP_TEMP_n5                  |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(SFP_TEMP/NONE<=-5),\
            defCHASSISFLASH_USAGE_90                |RASLOG,SNMP,EMAIL            |CHASSIS(FLASH_USAGE/NONE>=90),\
            defCHASSISMEMORY_USAGE_75               |RASLOG,SNMP,EMAIL            |CHASSIS(MEMORY_USAGE/NONE>=75),\
            defCHASSISCPU_80                        |RASLOG,SNMP,EMAIL            |CHASSIS(CPU/NONE>=80),\
            defSWITCHMARG_PORTS_5                   |SW_CRITICAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=5),\
            defSWITCHMARG_PORTS_6                   |SW_MARGINAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=6),\
            defSWITCHMARG_PORTS_10                  |SW_CRITICAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=10),\
            defSWITCHMARG_PORTS_11                  |SW_MARGINAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=11),\
            defSWITCHMARG_PORTS_25                  |SW_CRITICAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=25),\
            defSWITCHFAULTY_PORTS_5                 |SW_CRITICAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=5),\
            defSWITCHFAULTY_PORTS_6                 |SW_MARGINAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=6),\
            defSWITCHFAULTY_PORTS_10                |SW_CRITICAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=10),\
            defSWITCHFAULTY_PORTS_11                |SW_MARGINAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=11),\
            defSWITCHFAULTY_PORTS_25                |SW_CRITICAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=25),\
            defCHASSISBAD_TEMP_MARG                 |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(BAD_TEMP/NONE>=1),\
            defCHASSISBAD_TEMP_CRIT                 |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_TEMP/NONE>=2),\
            defCHASSISBAD_PWR_CRIT                  |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_PWR/NONE>=3),\
            defCHASSISBAD_FAN_MARG                  |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(BAD_FAN/NONE>=1),\
            defCHASSISBAD_FAN_CRIT                  |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_FAN/NONE>=2),\
            defCHASSISDOWN_CORE_1                   |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(DOWN_CORE/NONE>=1),\
            defCHASSISDOWN_CORE_2                   |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(DOWN_CORE/NONE>=2),\
            defCHASSISWWN_DOWN_1                    |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(WWN_DOWN/NONE>=1),\
            defCHASSISHA_SYNC_0                     |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(HA_SYNC/NONE==0),\
            defCHASSISFAULTY_BLADE_1                |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(FAULTY_BLADE/NONE>=1),\
            defALL_PORTSSFP_STATE_FAULTY            |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==FAULTY),\
            defALL_PORTSSFP_STATE_IN                |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==IN),\
            defALL_PORTSSFP_STATE_OFF               |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==OFF),\
            defALL_PORTSSFP_STATE_OUT               |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==OUT),\
            defALL_PSPS_STATE_FAULTY                |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==FAULTY),\
            defALL_PSPS_STATE_IN                    |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==IN),\
            defALL_PSPS_STATE_OFF                   |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==OFF),\
            defALL_PSPS_STATE_OUT                   |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==OUT),\
            defALL_FANFAN_STATE_FAULTY              |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==FAULTY),\
            defALL_FANFAN_STATE_IN                  |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==IN),\
            defALL_FANFAN_STATE_OFF                 |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==OFF),\
            defALL_FANFAN_STATE_OUT                 |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==OUT),\
            defALL_WWNWWN_FAULTY                    |RASLOG,SNMP,EMAIL            |ALL_WWN(WWN/NONE==FAULTY),\
            defALL_WWNWWN_IN                        |RASLOG,SNMP,EMAIL,SNMP,EMAIL |ALL_WWN(WWN/NONE==IN),\
            defALL_WWNWWN_OFF                       |RASLOG,SNMP,EMAIL,SNMP,EMAIL |ALL_WWN(WWN/NONE==OFF),\
            defALL_WWNWWN_OUT                       |RASLOG,SNMP,EMAIL            |ALL_WWN(WWN/NONE==OUT),\
            defALL_SLOTSBLADE_STATE_FAULTY          |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==FAULTY),\
            defALL_SLOTSBLADE_STATE_IN              |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==IN),\
            defALL_SLOTSBLADE_STATE_OFF             |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==OFF),\
            defALL_SLOTSBLADE_STATE_OUT             |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==OUT),\
            defCHASSISETH_MGMT_PORT_STATE_DOWN      |RASLOG,SNMP,EMAIL            |CHASSIS(ETH_MGMT_PORT_STATE/NONE==DOWN),\
            defCHASSISETH_MGMT_PORT_STATE_UP        |RASLOG,SNMP,EMAIL            |CHASSIS(ETH_MGMT_PORT_STATE/NONE==UP),\
            defALL_D_PORTSCRC_1                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/MIN>1),\
            defALL_D_PORTSPE_1                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/MIN>1),\
            defALL_D_PORTSITW_1                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/MIN>1),\
            defALL_D_PORTSLF_1                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/MIN>1),\
            defALL_D_PORTSLOSS_SYNC_1               |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/MIN>1),\
            defALL_D_PORTSCRC_H30                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/HOUR>30),\
            defALL_D_PORTSPE_H30                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/HOUR>30),\
            defALL_D_PORTSITW_H30                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/HOUR>30),\
            defALL_D_PORTSLF_H30                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/HOUR>30),\
            defALL_D_PORTSLOSS_SYNC_H30             |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/HOUR>30),\
            defALL_D_PORTSCRC_D500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/DAY>500),\
            defALL_D_PORTSPE_D500                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/DAY>500),\
            defALL_D_PORTSITW_D500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/DAY>500),\
            defALL_D_PORTSLF_D500                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/DAY>500),\
            defALL_D_PORTSLOSS_SYNC_D500            |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/DAY>500),\
            defALL_D_PORTSCRC_2                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/MIN>2),\
            defALL_D_PORTSPE_2                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/MIN>2),\
            defALL_D_PORTSITW_2                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/MIN>2),\
            defALL_D_PORTSLF_2                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/MIN>2),\
            defALL_D_PORTSLOSS_SYNC_2               |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/MIN>2),\
            defALL_D_PORTSCRC_H60                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/HOUR>60),\
            defALL_D_PORTSPE_H60                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/HOUR>60),\
            defALL_D_PORTSITW_H60                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/HOUR>60),\
            defALL_D_PORTSLF_H60                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/HOUR>60),\
            defALL_D_PORTSLOSS_SYNC_H60             |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/HOUR>60),\
            defALL_D_PORTSCRC_D1000                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/DAY>1000),\
            defALL_D_PORTSPE_D1000                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/DAY>1000),\
            defALL_D_PORTSITW_D1000                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/DAY>1000),\
            defALL_D_PORTSLF_D1000                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/DAY>1000),\
            defALL_D_PORTSLOSS_SYNC_D1000           |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/DAY>1000),\
            defALL_D_PORTSCRC_3                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/MIN>3),\
            defALL_D_PORTSPE_3                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/MIN>3),\
            defALL_D_PORTSITW_3                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/MIN>3),\
            defALL_D_PORTSLF_3                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/MIN>3),\
            defALL_D_PORTSLOSS_SYNC_3               |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/MIN>3),\
            defALL_D_PORTSCRC_H90                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/HOUR>90),\
            defALL_D_PORTSPE_H90                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/HOUR>90),\
            defALL_D_PORTSITW_H90                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/HOUR>90),\
            defALL_D_PORTSLF_H90                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/HOUR>90),\
            defALL_D_PORTSLOSS_SYNC_H90             |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/HOUR>90),\
            defALL_D_PORTSCRC_D1500                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/DAY>1500),\
            defALL_D_PORTSPE_D1500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/DAY>1500),\
            defALL_D_PORTSITW_D1500                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/DAY>1500),\
            defALL_D_PORTSLF_D1500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/DAY>1500),\
            defALL_D_PORTSLOSS_SYNC_D1500           |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/DAY>1500),\
            defALL_F_PORTS_IO_PERF_IMPACT           |RASLOG,SNMP,EMAIL            |ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_PERF_IMPACT),\
            defALL_F_PORTS_IO_FRAME_LOSS            |RASLOG,SNMP,EMAIL            |ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_FRAME_LOSS),\
            defALL_F_PORTS_IO_FRAME_LOSS            |RASLOG,SNMP,EMAIL            |ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_FRAME_LOSS) ,\
            defCHASSISBAD_PWR_MARG                  |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(BAD_PWR/NONE>=1),\
            defCHASSISBAD_PWR_CRIT                  |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_PWR/NONE>=2),\
            defALL_2K_QSFPCURRENT_39                |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(CURRENT/NONE>=39),\
            defALL_2K_QSFPVOLTAGE_3600              |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(VOLTAGE/NONE>=3600),\
            defALL_2K_QSFPRXP_2000                  |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(RXP/NONE>=2000),\
            defALL_2K_QSFPSFP_TEMP_85               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(SFP_TEMP/NONE>=85),\
            defALL_2K_QSFPVOLTAGE_2900              |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(VOLTAGE/NONE<=2900),\
            defALL_2K_QSFPSFP_TEMP_n15              |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(SFP_TEMP/NONE<=-15),\
            defALL_100M_16GSWL_QSFPCURRENT_10       |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(CURRENT/NONE>=10),\
            defALL_100M_16GSWL_QSFPSFP_TEMP_85      |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(SFP_TEMP/NONE>=85),\
            defALL_100M_16GSWL_QSFPSFP_TEMP_n5      |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(SFP_TEMP/NONE<=-5),\
            defALL_100M_16GSWL_QSFPVOLTAGE_2970     |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(VOLTAGE/NONE<=2970),\
            defALL_100M_16GSWL_QSFPVOLTAGE_3630     |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(VOLTAGE/NONE>=3630),\
            defALL_100M_16GSWL_QSFPRXP_2187         |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(RXP/NONE>=2187) ,\
        "
    
    return(l) 
     
def cleanup_policy( policy_list):
    """
        cleanup any user added policies, rules
        remove rules from policies and delete the policy
    """
     
    capture_cmd = anturlar.fos_cmd("mapspolicy --enable dflt_moderate_policy")
     
    for p in policy_list:
        r = get_policy_rules(p)
        print("\n\n\n\n")
        print(r)
        print("\n\n")

        for s in r:
            #rn = s.split(" ")
            rn = " ".join(s.split())
            rn = rn.split(",")
            print("\n\n\n\n")
            print(rn)
            print("\n\n")
            
            capture_cmd = anturlar.fos_cmd("mapspolicy --delrule %s -rulename %s" % (p,rn[0]))
            capture_cmd = anturlar.fos_cmd("mapsrule --delete %s " % rn[0])
           
        capture_cmd = anturlar.fos_cmd("mapspolicy --delete %s" % p)
        
    return(0)
  
def get_policy_rules( p = "None"):
    """
       get the rules of a policy
       
    """
 
    capture_cmd = anturlar.fos_cmd("mapspolicy --show %s " % p)
    #ras = re.compile('([_ ,\//\(-=\.|<>A-Za-z0-9]+)(?=\))')
    ras = re.compile('([_A-Za-z]+)(?=\s+\w+,)')
    ras = ras.findall(capture_cmd)
    return(ras)
    
    
    
def format_header(testcase):
    
    a = "***************************************************************************\r\n"
    b = "****        %s   \r\n" % testcase
    c = "****        STARTING THE TEST \r\n"
    
    h = a + a + b + c + a + a
    
    return(h)
    
    
def format_results(testcase, testresult):
    
    a = "***************************************************************************\r\n"
    b = "****        TEST RESULTS      \r\n"
    c = "****        %s  \r\n" % testcase
    d = "****        %s  \r\n" % testresult
    
    h = a + a + b + c + d + a + a
    
    return(h)
    
    
def check_same_state():
    """
    """
    #### get maps stats for compare to previous
    ####
    ####
    
    pass
    
    
    
    
def end():
    pass
    
    

























