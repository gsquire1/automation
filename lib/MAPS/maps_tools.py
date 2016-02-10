#!/usr/bin/env python3

###############################################################################
#### Home location is /home/automation/lib/MAPS/
####
###############################################################################
  
  
import anturlar
import liabhar
import re
  
  
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
    

       
def get_maps_config():
    """
        get the maps configuration to compare
        
    """
    capture_cmd = anturlar.fos_cmd("" )
    #ras = re.compile('([_ ,\//\(-=\.|<>A-Za-z0-9]+)(?=\))')
    ras = re.compile('Status:\s+([A-Za-z]+)(?=\\r\\n)')
    ras = ras.findall(capture_cmd)
    
    
    return(maps_config)
    
 
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
    
 
 
def add_rules_each_monitor_type(add_max=False, add_each_monitor=False, add_all=True, policy_is="Dolly" ):
    """
        create rules with each different combination of monitor for each type of logical group
        
        
        
    """
    
    sw_info = anturlar.SwitchInfo()
    fid_now = sw_info.ls_now()
    cons_out = anturlar.fos_cmd(" ")
    #sw_ip = sw_info.ipaddress()
    #f = anturlar.FabricInfo(fid_now)
    
    #### this list goes with FC Ports as the type of logical group
    #monitor_list_port_health_fc_port = ["CRC", "ITW", "LOSS_SYNC", "UTIL", "CRED_ZERO", "THPUT_DEGRADE", ]
    #### this list goes with FLOW as the type of logical group
    #monitor_list_perf_flow_port = ["TX_THPUT", "RX_THPUT", "RX_FCNT", "TX_FCNT"]
    #### this list goes wtth SFP as the type of logical groups
    monitor_list_for_ios  = ["RD_PENDING_IO_8K", "WR_PENDING_IO_8K", "RD_PENDING_IO_8_64K", "WR_PENDING_IO_8_64K", \
                             "RD_PENDING_IO_64_512K", "WR_PENDING_IO_64_512K", "RD_PENDING_IO_GE_512K", "WR_PENDING_IO_GE_512K", \
                             
                             "RD_STATUS_TIME_8K", "WR_STATUS_TIME_8K", "RD_STATUS_TIME_8_64K", "WR_STATUS_TIME_8_64K", \
                             "RD_STATUS_TIME_64_512K", "WR_STATUS_TIME_64_512K", "RD_STATUS_TIME_GE_512K", "WR_STATUS_TIME_GE_512K", \
                             
                             "RD_1stDATA_TIME_LE_8K", "WR_1stXFER_RDY_LE_8K", "RD_1stDATA_TIME_8_64K", "WR_1stXFER_RDY_8_64K", \
                             "RD_1stDATA_TIME_64_512K", "WR_1stXFER_RDY_64_512K", "RD_1stDATA_TIME_GE_512K", "WR_1stXFER_RDY_GE_512K" ]
    
    
    monitor_list_for_traffic_perf =  [ "TX_FCNT", "RX_FCNT", "TX_THPUT", "RX_THPUT", "IO_RD", "IO_WR", "IO_RD_BYTES", "IO_WR_BYTES" ]
    
    monitor_list_for_monitor_type =  [ "CRC","ITW","LOSS_SYNC","LF","LOSS_SIGNAL","PE","LR","C3TXTO","STATE_CHG", \
                                        "GE_CRC","GE_INV_LEN","GE_LOS_OF_SIG", \
                                        "BAD_OS","FRM_TRUNC"," FRM_LONG","CIR_STATE","CIR_UTIL","CIR_PKTLOSS", \
                                        "PKTLOSS","IP_UTIL","IP_PKTLOSS", \
                                        "SEC_DCC","SEC_HTTP","SEC_CMD","SEC_IDB","SEC_LV","SEC_CERT", \
                                        "SEC_FCS","SEC_SCC","SEC_AUTH_FAIL","SEC_TELNET","SEC_TS", \
                                        "DID_CHG","FLOGI","FAB_CFG","EPORT_DOWN","FAB_SEG","ZONE_CHG", \
                                        
                                        "RX","TX","UTIL", "FAN_AIR_FLOW_DIR", "ZONED_DEV_RATIO", "OVER_SUB_RATIO"]
    
    monitor_list_with_no_timebase =  [ "PWR_HRS", " RXP", "VOLTAGE", "CURRENT", "TXP", "SFP_TEMP", "VTAP_IOPS", "BE_LATENCY_IMPACT", \
                                       "DAYS_TO_EXPIRE", "IP_JITTER", "IP_RTT", "JITTER", "RTT", "BLADE_STATE", "DEV_LATENCY_IMPACT", \
                                       "DEV_NPIV_LOGINS", "FAN_STATE", "PS_STATE", "WWN", "TEMP", "BAD_FAN", "BAD_PWR", "BAD_TEMP", \
                                       "CPU", "DOWN_CORE", "ETH_MGMT_PORT_STATE", "EXPIRED_CERTS", "FAULTY_BLADE", "FLASH_USAGE", \
                                       "HA_SYNC", "MEMORY_USAGE", "WWN_DOWN", "BB_FCR_CNT", "ERR_PORTS", "FAULTY_PORTS", \
                                       "L2_DEVCNT_PER", "LSAN_DEVCNT_PER", "MARG_PORTS", "MISSING_SFP", "ZONE_CFGSZ_PER", \
                                       "SFP_STATE"  ]
    
    
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ####
    ####  GROUP LISTS
    ####
    ###################################################################################################################
    ###################################################################################################################
    
    flow_logical_group  = "sys_mon_all_fports" 
    fc_logical_group = "ALL_PORTS"
   
    fc_logical_group_list = [ "ALL_PORTS", "NON_E_F_PORTS", "ALL_E_PORTS", "ALL_F_PORTS", "ALL_OTHER_F_PORTS", \
                         "ALL_HOST_PORTS", "ALL_TARGET_PORTS" ]

    sfp_group_list  = [ "ALL_SFP", "ALL_10GSWL_SFP", "ALL_10GLWL_SFP", "ALL_16GSWL_SFP", "ALL_16GLWL_SFP", \
                   "ALL_QSFP", "ALL_OTHER_SFP", "ALL_2K_QSFP", "ALL_100M_16GSWL_QSFP", "ALL_32GSWL_SFP", \
                   "ALL_32GLWL_SFP", "ALL_32GSWL_QSFP", "ALL_25Km_16GLWL_SFP" ]

    circuit_group_list = [ "ALL_CIRCUITS", "ALL_CIRCUIT_F_QOS", "ALL_CIRCUIT_HIGH_QOS", "ALL_CIRCUIT_MED_QOS", "ALL_CIRCUIT_LOW_QOS" ]

    tunnel_group_list  = [ "ALL_cleanup_all_rulesTUNNELS", "ALL_TUNNEL_F_QOS", "ALL_TUNNEL_HIGH_QOS", "ALL_TUNNEL_MED_QOS", "ALL_TUNNEL_LOW_QOS" ]
    
    ip_logical_group_list = [ "ALL_TUNNEL_IP_HIGH_QOS", "ALL_TUNNEL_IP_MED_QOS", "ALL_TUNNEL_IP_LOW_QOS", \
                             "ALL_CIRCUIT_IP_HIGH_QOS", "ALL_CIRCUIT_IP_MED_QOS", "ALL_CIRCUIT_IP_LOW_QOS" ]

    ext_ge_group_list = [ "ALL_EXT_GE_PORTS"]

    ext_all_groups  = circuit_group_list + tunnel_group_list + ip_logical_group_list + ext_ge_group_list

    temp_sensor_group_list   = [ "ALL_TS" ]
    fan_group_list           = [ "ALL_FAN" ] 
    power_supply_group_list  = [ "ALL_PS" ]
    wwn_group_list           = [ "ALL_WWN" ]                            
    blade_group_list         = [ "ALL_SLOTS", "ALL_SW_BLADES", "ALL_CORE_BLADES" ]
    flash_group_list         = [ "ALL_FLASH" ] 
    switch_group_list        = [ "SWITCH" ]
    chassis_group_list       = [ "CHASSIS" ]
    d_group_list             = [ "ALL_D_PORTS" ]
    be_ports_group_list      = [ "ALL_BE_PORTS" ]
    quarantined_group_list   = [ "ALL_QUARANTINED_PORTS" ]
    asic_group_list          = [ "ALL_ASICS" ]
    certs_group_list         = [ "ALL_CERTS" ]
    
    all_other_groups_list   =  temp_sensor_group_list + fan_group_list + power_supply_group_list + wwn_group_list \
                        + blade_group_list + flash_group_list + switch_group_list + chassis_group_list + d_group_list \
                        + be_ports_group_list + quarantined_group_list + asic_group_list + certs_group_list
    
    monitor_list_combined  =  monitor_list_for_ios + monitor_list_for_traffic_perf + monitor_list_for_monitor_type + monitor_list_with_no_timebase
    monitor_list_quick_sfp =  monitor_list_with_no_timebase
    timebase_list = ["min", "hour", "day", "none"]
    
    operator_list = [ "l", "le", "g", "ge", "eq" ]
    
    actions_list = [ "raslog", "email", "snmp", "fence", "fence,decom", "fms", "none", "sfp_marginal", "sw_marginal", "sw_critical"]  #### do we need other actions here - sddq 
    
    cons_out = anturlar.fos_cmd("mapspolicy --create %s" % policy_is)
    rule_name = "monitor_test___"
    stopnow = 0
    stophere = 100000
    monitor_number = 0
    
    
 
    #if add_all:
    #    f = "%s" % ("logs/MAPS_RULES_SFP_GROUPS_quick_test.txt")
    #    ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
    #    for r in sfp_group_list:
    #        cleanup_all_rules()
    #        for p in monitor_list_quick_sfp:
    #            cleanup_all_rules()
    #            for t in timebase_list:
    #                for o in operator_list:
    #                    for a in actions_list:
    #                        rule_to_add  = rule_name + str(monitor_number)
    #                        cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy policy_is" \
    #                                        % (rule_to_add, r, p, t, o, a ))
    #                        if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
    #                            monitor_number += 1 
    #                            ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
    #    ff.close()
    
        
    if add_each_monitor:
        f = "%s" % ("logs/MAPS_RULES_EXT_GROUPS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        timebase_list = ["min","none" ]
        operator_list = [ "g", ]
        actions_list  = [ "raslog", ]
        for r in ext_all_groups:
           

            
            for p in monitor_list_combined:
               
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s " \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        f = "%s" % ("logs/MAPS_RULES_ALL_OTHERS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in all_other_groups_list:
          
            for p in monitor_list_combined:
            
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s " \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        f = "%s" % ("logs/MAPS_RULES_SFP_GROUPS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in sfp_group_list:
         
            for p in monitor_list_combined:
            
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s " \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        f = "%s" % ("logs/MAPS_RULES_PORT_GROUPS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in fc_logical_group_list:
         
            for p in monitor_list_combined:
            
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s " \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        #
#######################################################################################################################
#######################################################################################################################
####
#### this section will add each rule with each timebase and each operator and each action
####
#######################################################################################################################
#######################################################################################################################
    
    
    if add_all:
        f = "%s" % ("logs/MAPS_RULES_EXT_GROUPS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in ext_all_groups:
            cleanup_all_rules()

            
            for p in monitor_list_combined:
                cleanup_all_rules()
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s " \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        f = "%s" % ("logs/MAPS_RULES_ALL_OTHERS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in all_other_groups_list:
            cleanup_all_rules()
            for p in monitor_list_combined:
                cleanup_all_rules()
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s" \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        f = "%s" % ("logs/MAPS_RULES_SFP_GROUPS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in sfp_group_list:
            cleanup_all_rules()
            for p in monitor_list_combined:
                cleanup_all_rules()
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s" \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        f = "%s" % ("logs/MAPS_RULES_PORT_GROUPS.txt")
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        for r in fc_logical_group_list:
            cleanup_all_rules()
            for p in monitor_list_combined:
                cleanup_all_rules()
                for t in timebase_list:
                    for o in operator_list:
                        for a in actions_list:
                            rule_to_add  = rule_name + str(monitor_number)
                            cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action %s -policy %s" \
                                            % (rule_to_add, r, p, t, o, a, policy_is ))
                            if "Invalid Monitor" not in cons_out and "Timebase" not in cons_out and "Invalid action" not in cons_out:
                                monitor_number += 1 
                                ff.write("\n--  %s  --  %s  --  %s    -- %s   --   %s   --   %s   --END  "  %  (r, p, t, o, a, cons_out))
        ff.close()
        #
        #
    ###################################################################################################################
    ###################################################################################################################
    ####
    ####  this section adds rules to a switch until the max is reached.(it will continue after the max is reached)
    ####    this failed for 'unable to communicate with deamon'  mdd in 8.0.0  and should be fixed in 8.0.1
    ####    
    ####
    ###################################################################################################################
    ###################################################################################################################
    
    if add_max:
        while stopnow < stophere:
            
            for p in monitor_list_port_health_fc_port:
                rule_to_add = rule_name + str(stopnow)
                cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action raslog,email -policy %s " \
                                        % (rule_to_add, fc_logical_group, p ,timebase_list[0], operator_list[2], policy_is ))
                 
                stopnow += 1
             
            for p in monitor_list_perf_flow_port: 
                rule_to_add = rule_name + str(stopnow)
                cons_out = anturlar.fos_cmd("mapsrule --create %s -group %s -monitor %s -timebase %s -op %s -value 0 -action raslog,email -policy policy_is" \
                                        % (rule_to_add, flow_logical_group, p ,timebase_list[0], operator_list[2], policy_is ))
                 
                stopnow += 1
     
    return(True)
        
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
    
    #### starting with 8.0.0
    l = [ "mapsdb --show all",  "mapssam --show", "mapsconfig --config pause -type NO_port -members 0", \
         "mapsconfig --config continue -type YES_port -members 0 ", "mapsconfig --actions ", \
         "mapsconfig --import", "mapsconfig --deimport" , "mapsdb --show everything", \
         "mapsdb --show abunchof28284204 ", "mapsdb --clear "]
    
    if options == "usage":
        #### these commands will return a usage message since they are
        ####  not in the correct format
        #### maybe add the next line to be the correct response
        ####
        l = ["mapsConfig -- ", \
             #"mapsconfig --config pause -type NO_port -members 0", \
             #"mapsconfig --config continue -type YES_port -members 0", \
             "mapsconfig --emailcfg smckie@brocade.com", \
             "mapsconfig --emailcfg ", \
             #"mapsconfig --actions ", \
             #"mapsconfig --import  ", \
             #"mapsconfig --deimport ", \
             #"mapsconfig --enablemaps ", \
             #"mapsconfig --No_purge", \
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
             #"mapsdb --show everything", \
             #"mapsdb --show abunchof28284204", \
             #"mapsdb --clear  ", \
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
             #"echo n | mapsconfig --enablemaps -policy dflt_conservative_policy", \
             "mapsconfig --", \
             "mapsconfig --show", \
             #"mapsconfig --enableFPImon", \
             #"mapsconfig --disableFPImon", \
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
    l = "   defNON_E_F_PORTSCRC_0                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(CRC/MIN>0)     ,\
            defNON_E_F_PORTSCRC_2                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(CRC/MIN>2)    ,\
            defNON_E_F_PORTSCRC_10                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(CRC/MIN>10)  ,\
            defNON_E_F_PORTSCRC_20                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(CRC/MIN>20) ,\
            defNON_E_F_PORTSCRC_21                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(CRC/MIN>21) ,\
            defNON_E_F_PORTSCRC_40                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(CRC/MIN>40) ,\
            defNON_E_F_PORTSITW_15                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(ITW/MIN>15) ,\
            defNON_E_F_PORTSITW_20                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(ITW/MIN>20) ,\
            defNON_E_F_PORTSITW_21                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(ITW/MIN>21) ,\
            defNON_E_F_PORTSITW_40                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(ITW/MIN>40) ,\
            defNON_E_F_PORTSITW_41                  |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(ITW/MIN>41) ,\
            defNON_E_F_PORTSITW_80                  |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(ITW/MIN>80) ,\
            defNON_E_F_PORTSLR_2                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LR/MIN>2) ,\
            defNON_E_F_PORTSLR_4                    |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(LR/MIN>4) ,\
            defNON_E_F_PORTSLR_5                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LR/MIN>5) ,\
            defNON_E_F_PORTSLR_10                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(LR/MIN>10) ,\
            defNON_E_F_PORTSLR_11                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LR/MIN>11) ,\
            defNON_E_F_PORTSLR_20                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(LR/MIN>20) ,\
            defNON_E_F_PORTSSTATE_CHG_2             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(STATE_CHG/MIN>2) ,\
            defNON_E_F_PORTSSTATE_CHG_4             |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(STATE_CHG/MIN>4) ,\
            defNON_E_F_PORTSSTATE_CHG_5             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(STATE_CHG/MIN>5) ,\
            defNON_E_F_PORTSSTATE_CHG_10            |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(STATE_CHG/MIN>10) ,\
            defNON_E_F_PORTSSTATE_CHG_11            |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(STATE_CHG/MIN>11)  ,\
            defNON_E_F_PORTSSTATE_CHG_20            |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(STATE_CHG/MIN>20)  ,\
            defNON_E_F_PORTSLOSS_SIGNAL_0           |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SIGNAL/MIN>0)  ,\
            defNON_E_F_PORTSLOSS_SIGNAL_3           |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SIGNAL/MIN>3)  ,\
            defNON_E_F_PORTSLOSS_SIGNAL_5           |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SIGNAL/MIN>5)  ,\
            defNON_E_F_PORTSPE_0                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(PE/MIN>0)  ,\
            defNON_E_F_PORTSPE_2                    |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(PE/MIN>2)  ,\
            defNON_E_F_PORTSPE_3                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(PE/MIN>3)  ,\
            defNON_E_F_PORTSPE_7                    |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(PE/MIN>7)  ,\
            defNON_E_F_PORTSPE_5                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(PE/MIN>5)  ,\
            defNON_E_F_PORTSPE_10                   |FENCE,SNMP,EMAIL             |NON_E_F_PORTS(PE/MIN>10)  ,\
            defNON_E_F_PORTSLF_0                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LF/MIN>0)  ,\
            defNON_E_F_PORTSLF_3                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LF/MIN>3)  ,\
            defNON_E_F_PORTSLF_5                    |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LF/MIN>5)  ,\
            defNON_E_F_PORTSLOSS_SYNC_0             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SYNC/MIN>0)  ,\
            defNON_E_F_PORTSLOSS_SYNC_3             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SYNC/MIN>3)  ,\
            defNON_E_F_PORTSLOSS_SYNC_5             |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(LOSS_SYNC/MIN>5)  ,\
            defNON_E_F_PORTSRX_60                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(RX/HOUR>60)  ,\
            defNON_E_F_PORTSRX_75                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(RX/HOUR>75)  ,\
            defNON_E_F_PORTSRX_90                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(RX/HOUR>90)  ,\
            defNON_E_F_PORTSTX_60                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(TX/HOUR>60)  ,\
            defNON_E_F_PORTSTX_75                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(TX/HOUR>75)  ,\
            defNON_E_F_PORTSTX_90                   |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(TX/HOUR>90)  ,\
            defNON_E_F_PORTSUTIL_60                 |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(UTIL/HOUR>60)  ,\
            defNON_E_F_PORTSUTIL_75                 |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(UTIL/HOUR>75)  ,\
            defNON_E_F_PORTSUTIL_90                 |RASLOG,SNMP,EMAIL            |NON_E_F_PORTS(UTIL/HOUR>90)  ,\
            defALL_HOST_PORTSCRC_0                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(CRC/MIN>0)  ,\
            defALL_HOST_PORTSCRC_2                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(CRC/MIN>2)  ,\
            defALL_HOST_PORTSCRC_10                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(CRC/MIN>10)  ,\
            defALL_HOST_PORTSCRC_20                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(CRC/MIN>20)  ,\
            defALL_HOST_PORTSCRC_21                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(CRC/MIN>21)  ,\
            defALL_HOST_PORTSCRC_40                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(CRC/MIN>40)  ,\
            defALL_HOST_PORTSITW_15                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(ITW/MIN>15)  ,\
            defALL_HOST_PORTSITW_20                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(ITW/MIN>20)  ,\
            defALL_HOST_PORTSITW_21                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(ITW/MIN>21)  ,\
            defALL_HOST_PORTSITW_40                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(ITW/MIN>40)  ,\
            defALL_HOST_PORTSITW_41                 |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(ITW/MIN>41)  ,\
            defALL_HOST_PORTSITW_80                 |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(ITW/MIN>80)  ,\
            defALL_HOST_PORTSLR_2                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LR/MIN>2)  ,\
            defALL_HOST_PORTSLR_4                   |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(LR/MIN>4)  ,\
            defALL_HOST_PORTSLR_5                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LR/MIN>5)  ,\
            defALL_HOST_PORTSLR_10                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(LR/MIN>10)  ,\
            defALL_HOST_PORTSLR_11                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LR/MIN>11)  ,\
            defALL_HOST_PORTSLR_20                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(LR/MIN>20)  ,\
            defALL_HOST_PORTSSTATE_CHG_2            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(STATE_CHG/MIN>2)  ,\
            defALL_HOST_PORTSSTATE_CHG_4            |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(STATE_CHG/MIN>4)  ,\
            defALL_HOST_PORTSSTATE_CHG_5            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(STATE_CHG/MIN>5)  ,\
            defALL_HOST_PORTSSTATE_CHG_10           |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(STATE_CHG/MIN>10)  ,\
            defALL_HOST_PORTSSTATE_CHG_11           |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(STATE_CHG/MIN>11)  ,\
            defALL_HOST_PORTSSTATE_CHG_20           |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(STATE_CHG/MIN>20)  ,\
            defALL_HOST_PORTSLOSS_SIGNAL_0          |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SIGNAL/MIN>0)  ,\
            defALL_HOST_PORTSLOSS_SIGNAL_3          |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SIGNAL/MIN>3)  ,\
            defALL_HOST_PORTSLOSS_SIGNAL_5          |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SIGNAL/MIN>5)  ,\
            defALL_HOST_PORTSPE_0                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(PE/MIN>0)  ,\
            defALL_HOST_PORTSPE_2                   |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(PE/MIN>2)  ,\
            defALL_HOST_PORTSPE_3                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(PE/MIN>3)  ,\
            defALL_HOST_PORTSPE_7                   |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(PE/MIN>7)  ,\
            defALL_HOST_PORTSPE_5                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(PE/MIN>5)  ,\
            defALL_HOST_PORTSPE_10                  |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(PE/MIN>10)  ,\
            defALL_HOST_PORTSLF_0                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LF/MIN>0)  ,\
            defALL_HOST_PORTSLF_3                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LF/MIN>3)  ,\
            defALL_HOST_PORTSLF_5                   |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LF/MIN>5)  ,\
            defALL_HOST_PORTSLOSS_SYNC_0            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SYNC/MIN>0)  ,\
            defALL_HOST_PORTSLOSS_SYNC_3            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SYNC/MIN>3)  ,\
            defALL_HOST_PORTSLOSS_SYNC_5            |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(LOSS_SYNC/MIN>5)  ,\
            defALL_HOST_PORTSRX_60                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(RX/HOUR>60)  ,\
            defALL_HOST_PORTSRX_75                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(RX/HOUR>75)  ,\
            defALL_HOST_PORTSRX_90                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(RX/HOUR>90)  ,\
            defALL_HOST_PORTSTX_60                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(TX/HOUR>60)  ,\
            defALL_HOST_PORTSTX_75                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(TX/HOUR>75)  ,\
            defALL_HOST_PORTSTX_90                  |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(TX/HOUR>90)  ,\
            defALL_HOST_PORTSUTIL_60                |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(UTIL/HOUR>60)  ,\
            defALL_HOST_PORTSUTIL_75                |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(UTIL/HOUR>75)  ,\
            defALL_HOST_PORTSUTIL_90                |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(UTIL/HOUR>90)  ,\
            defALL_OTHER_F_PORTSCRC_0               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(CRC/MIN>0)  ,\
            defALL_OTHER_F_PORTSCRC_2               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(CRC/MIN>2)  ,\
            defALL_OTHER_F_PORTSCRC_10              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(CRC/MIN>10)  ,\
            defALL_OTHER_F_PORTSCRC_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(CRC/MIN>20)  ,\
            defALL_OTHER_F_PORTSCRC_21              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(CRC/MIN>21)  ,\
            defALL_OTHER_F_PORTSCRC_40              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(CRC/MIN>40)  ,\
            defALL_OTHER_F_PORTSITW_15              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(ITW/MIN>15)  ,\
            defALL_OTHER_F_PORTSITW_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(ITW/MIN>20)  ,\
            defALL_OTHER_F_PORTSITW_21              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(ITW/MIN>21)  ,\
            defALL_OTHER_F_PORTSITW_40              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(ITW/MIN>40)  ,\
            defALL_OTHER_F_PORTSITW_41              |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(ITW/MIN>41)  ,\
            defALL_OTHER_F_PORTSITW_80              |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(ITW/MIN>80)  ,\
            defALL_OTHER_F_PORTSLR_2                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LR/MIN>2)  ,\
            defALL_OTHER_F_PORTSLR_4                |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(LR/MIN>4)  ,\
            defALL_OTHER_F_PORTSLR_5                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LR/MIN>5)  ,\
            defALL_OTHER_F_PORTSLR_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(LR/MIN>10)  ,\
            defALL_OTHER_F_PORTSLR_11               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LR/MIN>11)  ,\
            defALL_OTHER_F_PORTSLR_20               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(LR/MIN>20)  ,\
            defALL_OTHER_F_PORTSSTATE_CHG_2         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(STATE_CHG/MIN>2)  ,\
            defALL_OTHER_F_PORTSSTATE_CHG_4         |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(STATE_CHG/MIN>4)  ,\
            defALL_OTHER_F_PORTSSTATE_CHG_5         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(STATE_CHG/MIN>5)  ,\
            defALL_OTHER_F_PORTSSTATE_CHG_10        |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(STATE_CHG/MIN>10)  ,\
            defALL_OTHER_F_PORTSSTATE_CHG_11        |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(STATE_CHG/MIN>11)  ,\
            defALL_OTHER_F_PORTSSTATE_CHG_20        |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(STATE_CHG/MIN>20)  ,\
            defALL_OTHER_F_PORTSLOSS_SIGNAL_0       |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>0)  ,\
            defALL_OTHER_F_PORTSLOSS_SIGNAL_3       |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>3)  ,\
            defALL_OTHER_F_PORTSLOSS_SIGNAL_5       |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>5)  ,\
            defALL_OTHER_F_PORTSPE_0                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(PE/MIN>0)  ,\
            defALL_OTHER_F_PORTSPE_2                |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(PE/MIN>2)  ,\
            defALL_OTHER_F_PORTSPE_3                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(PE/MIN>3)  ,\
            defALL_OTHER_F_PORTSPE_7                |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(PE/MIN>7)  ,\
            defALL_OTHER_F_PORTSPE_5                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(PE/MIN>5)  ,\
            defALL_OTHER_F_PORTSPE_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(PE/MIN>10)  ,\
            defALL_OTHER_F_PORTSLF_0                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LF/MIN>0)  ,\
            defALL_OTHER_F_PORTSLF_3                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LF/MIN>3)  ,\
            defALL_OTHER_F_PORTSLF_5                |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LF/MIN>5)  ,\
            defALL_OTHER_F_PORTSLOSS_SYNC_0         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>0)  ,\
            defALL_OTHER_F_PORTSLOSS_SYNC_3         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>3)  ,\
            defALL_OTHER_F_PORTSLOSS_SYNC_5         |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>5)  ,\
            defALL_OTHER_F_PORTSRX_60               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(RX/HOUR>60)  ,\
            defALL_OTHER_F_PORTSRX_75               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(RX/HOUR>75)  ,\
            defALL_OTHER_F_PORTSRX_90               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(RX/HOUR>90)  ,\
            defALL_OTHER_F_PORTSTX_60               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(TX/HOUR>60)  ,\
            defALL_OTHER_F_PORTSTX_75               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(TX/HOUR>75)  ,\
            defALL_OTHER_F_PORTSTX_90               |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(TX/HOUR>90)  ,\
            defALL_OTHER_F_PORTSUTIL_60             |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(UTIL/HOUR>60)  ,\
            defALL_OTHER_F_PORTSUTIL_75             |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(UTIL/HOUR>75)  ,\
            defALL_OTHER_F_PORTSUTIL_90             |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(UTIL/HOUR>90)  ,\
            defALL_HOST_PORTSC3TXTO_2               |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(C3TXTO/MIN>2)  ,\
            defALL_HOST_PORTSC3TXTO_4               |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(C3TXTO/MIN>4)  ,\
            defALL_HOST_PORTSC3TXTO_3               |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(C3TXTO/MIN>3)  ,\
            defALL_HOST_PORTSC3TXTO_10              |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(C3TXTO/MIN>10)  ,\
            defALL_HOST_PORTSC3TXTO_11              |RASLOG,SNMP,EMAIL            |ALL_HOST_PORTS(C3TXTO/MIN>11)  ,\
            defALL_HOST_PORTSC3TXTO_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_HOST_PORTS(C3TXTO/MIN>20)  ,\
            defALL_OTHER_F_PORTSC3TXTO_2            |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(C3TXTO/MIN>2)  ,\
            defALL_OTHER_F_PORTSC3TXTO_4            |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(C3TXTO/MIN>4)  ,\
            defALL_OTHER_F_PORTSC3TXTO_3            |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(C3TXTO/MIN>3)  ,\
            defALL_OTHER_F_PORTSC3TXTO_10           |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(C3TXTO/MIN>10)  ,\
            defALL_OTHER_F_PORTSC3TXTO_11           |RASLOG,SNMP,EMAIL            |ALL_OTHER_F_PORTS(C3TXTO/MIN>11)  ,\
            defALL_OTHER_F_PORTSC3TXTO_20           |FENCE,DECOM,SNMP,EMAIL       |ALL_OTHER_F_PORTS(C3TXTO/MIN>20)  ,\
            defALL_E_PORTSCRC_0                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(CRC/MIN>0)  ,\
            defALL_E_PORTSCRC_2                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(CRC/MIN>2)  ,\
            defALL_E_PORTSCRC_10                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(CRC/MIN>10)  ,\
            defALL_E_PORTSCRC_20                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(CRC/MIN>20)  ,\
            defALL_E_PORTSCRC_21                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(CRC/MIN>21)  ,\
            defALL_E_PORTSCRC_40                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(CRC/MIN>40)  ,\
            defALL_E_PORTSITW_15                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(ITW/MIN>15)  ,\
            defALL_E_PORTSITW_20                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(ITW/MIN>20)  ,\
            defALL_E_PORTSITW_21                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(ITW/MIN>21)  ,\
            defALL_E_PORTSITW_40                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(ITW/MIN>40)  ,\
            defALL_E_PORTSITW_41                    |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(ITW/MIN>41)  ,\
            defALL_E_PORTSITW_80                    |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(ITW/MIN>80)  ,\
            defALL_E_PORTSLR_2                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LR/MIN>2)  ,\
            defALL_E_PORTSLR_4                      |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(LR/MIN>4)  ,\
            defALL_E_PORTSLR_5                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LR/MIN>5)  ,\
            defALL_E_PORTSLR_10                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(LR/MIN>10)  ,\
            defALL_E_PORTSLR_11                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LR/MIN>11)  ,\
            defALL_E_PORTSLR_20                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(LR/MIN>20)  ,\
            defALL_E_PORTSSTATE_CHG_2               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(STATE_CHG/MIN>2)  ,\
            defALL_E_PORTSSTATE_CHG_4               |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(STATE_CHG/MIN>4)  ,\
            defALL_E_PORTSSTATE_CHG_5               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(STATE_CHG/MIN>5)  ,\
            defALL_E_PORTSSTATE_CHG_10              |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(STATE_CHG/MIN>10)  ,\
            defALL_E_PORTSSTATE_CHG_11              |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(STATE_CHG/MIN>11)  ,\
            defALL_E_PORTSSTATE_CHG_20              |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(STATE_CHG/MIN>20)  ,\
            defALL_E_PORTSLOSS_SIGNAL_0             |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SIGNAL/MIN>0)  ,\
            defALL_E_PORTSLOSS_SIGNAL_3             |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SIGNAL/MIN>3)  ,\
            defALL_E_PORTSLOSS_SIGNAL_5             |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SIGNAL/MIN>5)  ,\
            defALL_E_PORTSPE_0                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(PE/MIN>0)  ,\
            defALL_E_PORTSPE_2                      |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(PE/MIN>2)  ,\
            defALL_E_PORTSPE_3                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(PE/MIN>3)  ,\
            defALL_E_PORTSPE_7                      |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(PE/MIN>7)  ,\
            defALL_E_PORTSPE_5                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(PE/MIN>5)  ,\
            defALL_E_PORTSPE_10                     |FENCE,DECOM,SNMP,EMAIL       |ALL_E_PORTS(PE/MIN>10)  ,\
            defALL_E_PORTSLF_0                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LF/MIN>0)  ,\
            defALL_E_PORTSLF_3                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LF/MIN>3)  ,\
            defALL_E_PORTSLF_5                      |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LF/MIN>5)  ,\
            defALL_E_PORTSLOSS_SYNC_0               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SYNC/MIN>0)  ,\
            defALL_E_PORTSLOSS_SYNC_3               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SYNC/MIN>3)  ,\
            defALL_E_PORTSLOSS_SYNC_5               |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(LOSS_SYNC/MIN>5)  ,\
            defALL_E_PORTSRX_60                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(RX/HOUR>60)  ,\
            defALL_E_PORTSRX_75                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(RX/HOUR>75)  ,\
            defALL_E_PORTSRX_90                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(RX/HOUR>90)  ,\
            defALL_E_PORTSTX_60                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(TX/HOUR>60)  ,\
            defALL_E_PORTSTX_75                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(TX/HOUR>75)  ,\
            defALL_E_PORTSTX_90                     |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(TX/HOUR>90)  ,\
            defALL_E_PORTSUTIL_60                   |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(UTIL/HOUR>60)  ,\
            defALL_E_PORTSUTIL_75                   |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(UTIL/HOUR>75)  ,\
            defALL_E_PORTSUTIL_90                   |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(UTIL/HOUR>90)  ,\
            defALL_E_PORTSC3TXTO_5                  |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(C3TXTO/MIN>5)  ,\
            defALL_E_PORTSC3TXTO_10                 |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(C3TXTO/MIN>10)  ,\
            defALL_E_PORTSC3TXTO_20                 |RASLOG,SNMP,EMAIL            |ALL_E_PORTS(C3TXTO/MIN>20)  ,\
            defALL_TARGET_PORTSC3TXTO_0             |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(C3TXTO/MIN>0)  ,\
            defALL_TARGET_PORTSC3TXTO_2             |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(C3TXTO/MIN>2)  ,\
            defALL_TARGET_PORTSC3TXTO_3             |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(C3TXTO/MIN>3)  ,\
            defALL_TARGET_PORTSC3TXTO_5             |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(C3TXTO/MIN>5)  ,\
            defALL_TARGET_PORTSC3TXTO_6             |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(C3TXTO/MIN>6)  ,\
            defALL_TARGET_PORTSC3TXTO_10            |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(C3TXTO/MIN>10)  ,\
            defALL_TARGET_PORTSCRC_0                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(CRC/MIN>0)  ,\
            defALL_TARGET_PORTSCRC_2                |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(CRC/MIN>2)  ,\
            defALL_TARGET_PORTSCRC_5                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(CRC/MIN>5)  ,\
            defALL_TARGET_PORTSCRC_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(CRC/MIN>10)  ,\
            defALL_TARGET_PORTSCRC_11               |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(CRC/MIN>11)  ,\
            defALL_TARGET_PORTSCRC_20               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(CRC/MIN>20)  ,\
            defALL_TARGET_PORTSITW_5                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(ITW/MIN>5)  ,\
            defALL_TARGET_PORTSITW_10               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(ITW/MIN>10)  ,\
            defALL_TARGET_PORTSITW_11               |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(ITW/MIN>11)  ,\
            defALL_TARGET_PORTSITW_20               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(ITW/MIN>20)  ,\
            defALL_TARGET_PORTSITW_21               |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(ITW/MIN>21)  ,\
            defALL_TARGET_PORTSITW_40               |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(ITW/MIN>40)  ,\
            defALL_TARGET_PORTSLR_0                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LR/MIN>0)  ,\
            defALL_TARGET_PORTSLR_2                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(LR/MIN>2)  ,\
            defALL_TARGET_PORTSLR_3                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LR/MIN>3)  ,\
            defALL_TARGET_PORTSLR_5                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(LR/MIN>5)  ,\
            defALL_TARGET_PORTSLR_6                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LR/MIN>6)  ,\
            defALL_TARGET_PORTSLR_10                |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(LR/MIN>10)  ,\
            defALL_TARGET_PORTSSTATE_CHG_0          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(STATE_CHG/MIN>0)  ,\
            defALL_TARGET_PORTSSTATE_CHG_2          |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(STATE_CHG/MIN>2)  ,\
            defALL_TARGET_PORTSSTATE_CHG_3          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(STATE_CHG/MIN>3)  ,\
            defALL_TARGET_PORTSSTATE_CHG_7          |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(STATE_CHG/MIN>7)  ,\
            defALL_TARGET_PORTSSTATE_CHG_8          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(STATE_CHG/MIN>8)  ,\
            defALL_TARGET_PORTSSTATE_CHG_15         |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(STATE_CHG/MIN>15)  ,\
            defALL_TARGET_PORTSLOSS_SIGNAL_0        |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>0)  ,\
            defALL_TARGET_PORTSLOSS_SIGNAL_3        |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>3)  ,\
            defALL_TARGET_PORTSLOSS_SIGNAL_5        |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>5)  ,\
            defALL_TARGET_PORTSPE_0                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(PE/MIN>0)  ,\
            defALL_TARGET_PORTSPE_2                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(PE/MIN>2)  ,\
            defALL_TARGET_PORTSPE_3                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(PE/MIN>3)  ,\
            defALL_TARGET_PORTSPE_4                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(PE/MIN>4)  ,\
            defALL_TARGET_PORTSPE_5                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(PE/MIN>5)  ,\
            defALL_TARGET_PORTSPE_6                 |FENCE,DECOM,SNMP,EMAIL       |ALL_TARGET_PORTS(PE/MIN>6)  ,\
            defALL_TARGET_PORTSLF_0                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LF/MIN>0)  ,\
            defALL_TARGET_PORTSLF_3                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LF/MIN>3)  ,\
            defALL_TARGET_PORTSLF_5                 |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LF/MIN>5)  ,\
            defALL_TARGET_PORTSLOSS_SYNC_0          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SYNC/MIN>0)  ,\
            defALL_TARGET_PORTSLOSS_SYNC_3          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SYNC/MIN>3)  ,\
            defALL_TARGET_PORTSLOSS_SYNC_5          |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(LOSS_SYNC/MIN>5)  ,\
            defALL_TARGET_PORTSRX_60                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(RX/HOUR>60)  ,\
            defALL_TARGET_PORTSRX_75                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(RX/HOUR>75)  ,\
            defALL_TARGET_PORTSRX_90                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(RX/HOUR>90)  ,\
            defALL_TARGET_PORTSTX_60                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(TX/HOUR>60)  ,\
            defALL_TARGET_PORTSTX_75                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(TX/HOUR>75)  ,\
            defALL_TARGET_PORTSTX_90                |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(TX/HOUR>90)  ,\
            defALL_TARGET_PORTSUTIL_60              |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(UTIL/HOUR>60)  ,\
            defALL_TARGET_PORTSUTIL_75              |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(UTIL/HOUR>75)  ,\
            defALL_TARGET_PORTSUTIL_90              |RASLOG,SNMP,EMAIL            |ALL_TARGET_PORTS(UTIL/HOUR>90)  ,\
            defALL_CIRCUITSCIR_STATE_0              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_STATE/MIN>0)  ,\
            defALL_CIRCUITSCIR_STATE_3              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_STATE/MIN>3)  ,\
            defALL_CIRCUITSCIR_STATE_5              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_STATE/MIN>5)  ,\
            defALL_CIRCUITSCIR_UTIL_60              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_UTIL/MIN>60)  ,\
            defALL_CIRCUITSCIR_UTIL_75              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_UTIL/MIN>75)  ,\
            defALL_CIRCUITSCIR_UTIL_90              |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_UTIL/MIN>90)  ,\
            defALL_CIRCUITSCIR_PKTLOSS_PER_01       |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.01)  ,\
            defALL_CIRCUITSCIR_PKTLOSS_PER_05       |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.05)  ,\
            defALL_CIRCUITSCIR_PKTLOSS_PER_1        |RASLOG,SNMP,EMAIL            |ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.1)  ,\
            defSWITCHEPORT_DOWN_1                   |RASLOG,SNMP,EMAIL            |SWITCH(EPORT_DOWN/MIN>1)  ,\
            defSWITCHEPORT_DOWN_2                   |RASLOG,SNMP,EMAIL            |SWITCH(EPORT_DOWN/MIN>2)  ,\
            defSWITCHEPORT_DOWN_4                   |RASLOG,SNMP,EMAIL            |SWITCH(EPORT_DOWN/MIN>4)  ,\
            defSWITCHFAB_CFG_1                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_CFG/MIN>1)  ,\
            defSWITCHFAB_CFG_2                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_CFG/MIN>2)  ,\
            defSWITCHFAB_CFG_4                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_CFG/MIN>4)  ,\
            defSWITCHFAB_SEG_1                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_SEG/MIN>1)  ,\
            defSWITCHFAB_SEG_2                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_SEG/MIN>2)  ,\
            defSWITCHFAB_SEG_4                      |RASLOG,SNMP,EMAIL            |SWITCH(FAB_SEG/MIN>4)  ,\
            defSWITCHFLOGI_4                        |RASLOG,SNMP,EMAIL            |SWITCH(FLOGI/MIN>4)  ,\
            defSWITCHFLOGI_6                        |RASLOG,SNMP,EMAIL            |SWITCH(FLOGI/MIN>6)  ,\
            defSWITCHFLOGI_8                        |RASLOG,SNMP,EMAIL            |SWITCH(FLOGI/MIN>8)  ,\
            defSWITCHZONE_CHG_2                     |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CHG/DAY>2)  ,\
            defSWITCHZONE_CHG_5                     |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CHG/DAY>5)  ,\
            defSWITCHZONE_CHG_10                    |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CHG/DAY>10)  ,\
            defSWITCHDID_CHG_1                      |RASLOG,SNMP,EMAIL            |SWITCH(DID_CHG/MIN>1)  ,\
            defSWITCHL2_DEVCNT_PER_60               |RASLOG,SNMP,EMAIL            |SWITCH(L2_DEVCNT_PER/NONE>60)  ,\
            defSWITCHL2_DEVCNT_PER_75               |RASLOG,SNMP,EMAIL            |SWITCH(L2_DEVCNT_PER/NONE>75)  ,\
            defSWITCHL2_DEVCNT_PER_90               |RASLOG,SNMP,EMAIL            |SWITCH(L2_DEVCNT_PER/NONE>90)  ,\
            defSWITCHLSAN_DEVCNT_PER_60             |RASLOG,SNMP,EMAIL            |SWITCH(LSAN_DEVCNT_PER/NONE>60)  ,\
            defSWITCHLSAN_DEVCNT_PER_75             |RASLOG,SNMP,EMAIL            |SWITCH(LSAN_DEVCNT_PER/NONE>75)  ,\
            defSWITCHLSAN_DEVCNT_PER_90             |RASLOG,SNMP,EMAIL            |SWITCH(LSAN_DEVCNT_PER/NONE>90)  ,\
            defSWITCHZONE_CFGSZ_PER_70              |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CFGSZ_PER/NONE>70)  ,\
            defSWITCHZONE_CFGSZ_PER_80              |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CFGSZ_PER/NONE>80)  ,\
            defSWITCHZONE_CFGSZ_PER_90              |RASLOG,SNMP,EMAIL            |SWITCH(ZONE_CFGSZ_PER/NONE>90)  ,\
            defSWITCHBB_FCR_CNT_12                  |RASLOG,SNMP,EMAIL            |SWITCH(BB_FCR_CNT/NONE>12)  ,\
            defSWITCHSEC_TELNET_0                   |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TELNET/MIN>0)  ,\
            defSWITCHSEC_TELNET_2                   |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TELNET/MIN>2)  ,\
            defSWITCHSEC_TELNET_4                   |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TELNET/MIN>4)  ,\
            defSWITCHSEC_HTTP_0                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_HTTP/MIN>0)  ,\
            defSWITCHSEC_HTTP_2                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_HTTP/MIN>2)  ,\
            defSWITCHSEC_HTTP_4                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_HTTP/MIN>4)  ,\
            defSWITCHSEC_SCC_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_SCC/MIN>0)  ,\
            defSWITCHSEC_SCC_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_SCC/MIN>2)  ,\
            defSWITCHSEC_SCC_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_SCC/MIN>4)  ,\
            defSWITCHSEC_DCC_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_DCC/MIN>0)  ,\
            defSWITCHSEC_DCC_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_DCC/MIN>2)  ,\
            defSWITCHSEC_DCC_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_DCC/MIN>4)  ,\
            defSWITCHSEC_LV_0                       |RASLOG,SNMP,EMAIL            |SWITCH(SEC_LV/MIN>0)  ,\
            defSWITCHSEC_LV_2                       |RASLOG,SNMP,EMAIL            |SWITCH(SEC_LV/MIN>2)  ,\
            defSWITCHSEC_LV_4                       |RASLOG,SNMP,EMAIL            |SWITCH(SEC_LV/MIN>4)  ,\
            defSWITCHSEC_CERT_0                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CERT/MIN>0)  ,\
            defSWITCHSEC_CERT_2                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CERT/MIN>2)  ,\
            defSWITCHSEC_CERT_4                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CERT/MIN>4)  ,\
            defSWITCHSEC_AUTH_FAIL_0                |RASLOG,SNMP,EMAIL            |SWITCH(SEC_AUTH_FAIL/MIN>0)  ,\
            defSWITCHSEC_AUTH_FAIL_2                |RASLOG,SNMP,EMAIL            |SWITCH(SEC_AUTH_FAIL/MIN>2)  ,\
            defSWITCHSEC_AUTH_FAIL_4                |RASLOG,SNMP,EMAIL            |SWITCH(SEC_AUTH_FAIL/MIN>4)  ,\
            defSWITCHSEC_FCS_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_FCS/MIN>0)  ,\
            defSWITCHSEC_FCS_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_FCS/MIN>2)  ,\
            defSWITCHSEC_FCS_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_FCS/MIN>4)  ,\
            defSWITCHSEC_IDB_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_IDB/MIN>0)  ,\
            defSWITCHSEC_IDB_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_IDB/MIN>2)  ,\
            defSWITCHSEC_IDB_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_IDB/MIN>4)  ,\
            defSWITCHSEC_CMD_0                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CMD/MIN>0)  ,\
            defSWITCHSEC_CMD_2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CMD/MIN>2)  ,\
            defSWITCHSEC_CMD_4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_CMD/MIN>4)  ,\
            defSWITCHSEC_TS_H1                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/HOUR>1)  ,\
            defSWITCHSEC_TS_H2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/HOUR>2)  ,\
            defSWITCHSEC_TS_H4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/HOUR>4)  ,\
            defSWITCHSEC_TS_D2                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/DAY>2)  ,\
            defSWITCHSEC_TS_D4                      |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/DAY>4)  ,\
            defSWITCHSEC_TS_D10                     |RASLOG,SNMP,EMAIL            |SWITCH(SEC_TS/DAY>10)  ,\
            defALL_TSTEMP_OUT_OF_RANGE              |RASLOG,SNMP,EMAIL            |ALL_TS(TEMP/NONE==OUT_OF_RANGE)  ,\
            defALL_OTHER_SFPCURRENT_50              |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(CURRENT/NONE>=50)  ,\
            defALL_OTHER_SFPVOLTAGE_3630            |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(VOLTAGE/NONE>=3630)  ,\
            defALL_OTHER_SFPRXP_5000                |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(RXP/NONE>=5000)  ,\
            defALL_OTHER_SFPTXP_5000                |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(TXP/NONE>=5000)  ,\
            defALL_OTHER_SFPSFP_TEMP_85             |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(SFP_TEMP/NONE>=85)  ,\
            defALL_OTHER_SFPVOLTAGE_2960            |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(VOLTAGE/NONE<=2960)  ,\
            defALL_OTHER_SFPSFP_TEMP_n13            |RASLOG,SNMP,EMAIL            |ALL_OTHER_SFP(SFP_TEMP/NONE<=-13)  ,\
            defALL_10GSWL_SFPCURRENT_10             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(CURRENT/NONE>=10)  ,\
            defALL_10GSWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(VOLTAGE/NONE>=3600)  ,\
            defALL_10GSWL_SFPRXP_1999               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(RXP/NONE>=1999)  ,\
            defALL_10GSWL_SFPTXP_1999               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(TXP/NONE>=1999)  ,\
            defALL_10GSWL_SFPSFP_TEMP_90            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(SFP_TEMP/NONE>=90)  ,\
            defALL_10GSWL_SFPVOLTAGE_3000           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(VOLTAGE/NONE<=3000)  ,\
            defALL_10GSWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GSWL_SFP(SFP_TEMP/NONE<=-5)  ,\
            defALL_10GLWL_SFPCURRENT_95             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(CURRENT/NONE>=95)  ,\
            defALL_10GLWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(VOLTAGE/NONE>=3600)  ,\
            defALL_10GLWL_SFPRXP_2230               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(RXP/NONE>=2230)  ,\
            defALL_10GLWL_SFPTXP_2230               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(TXP/NONE>=2230)  ,\
            defALL_10GLWL_SFPSFP_TEMP_90            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(SFP_TEMP/NONE>=90)  ,\
            defALL_10GLWL_SFPVOLTAGE_2970           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(VOLTAGE/NONE<=2970)  ,\
            defALL_10GLWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_10GLWL_SFP(SFP_TEMP/NONE<=-5)  ,\
            defALL_16GSWL_SFPCURRENT_12             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(CURRENT/NONE>=12)  ,\
            defALL_16GSWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(VOLTAGE/NONE>=3600)  ,\
            defALL_16GSWL_SFPRXP_1259               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(RXP/NONE>=1259)  ,\
            defALL_16GSWL_SFPTXP_1259               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(TXP/NONE>=1259)  ,\
            defALL_16GSWL_SFPSFP_TEMP_85            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(SFP_TEMP/NONE>=85)  ,\
            defALL_16GSWL_SFPVOLTAGE_3000           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(VOLTAGE/NONE<=3000)  ,\
            defALL_16GSWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GSWL_SFP(SFP_TEMP/NONE<=-5)  ,\
            defALL_16GLWL_SFPCURRENT_70             |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(CURRENT/NONE>=70)  ,\
            defALL_16GLWL_SFPVOLTAGE_3600           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(VOLTAGE/NONE>=3600)  ,\
            defALL_16GLWL_SFPRXP_1995               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(RXP/NONE>=1995)  ,\
            defALL_16GLWL_SFPTXP_1995               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(TXP/NONE>=1995)  ,\
            defALL_16GLWL_SFPSFP_TEMP_90            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(SFP_TEMP/NONE>=90)  ,\
            defALL_16GLWL_SFPVOLTAGE_3000           |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(VOLTAGE/NONE<=3000)  ,\
            defALL_16GLWL_SFPSFP_TEMP_n5            |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_16GLWL_SFP(SFP_TEMP/NONE<=-5)  ,\
            defALL_QSFPCURRENT_10                   |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(CURRENT/NONE>=10)  ,\
            defALL_QSFPVOLTAGE_3600                 |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(VOLTAGE/NONE>=3600)  ,\
            defALL_QSFPRXP_2180                     |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(RXP/NONE>=2180)  ,\
            defALL_QSFPSFP_TEMP_85                  |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(SFP_TEMP/NONE>=85)  ,\
            defALL_QSFPVOLTAGE_2940                 |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(VOLTAGE/NONE<=2940)  ,\
            defALL_QSFPSFP_TEMP_n5                  |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_QSFP(SFP_TEMP/NONE<=-5)  ,\
            defCHASSISFLASH_USAGE_90                |RASLOG,SNMP,EMAIL            |CHASSIS(FLASH_USAGE/NONE>=90)  ,\
            defCHASSISMEMORY_USAGE_75               |RASLOG,SNMP,EMAIL            |CHASSIS(MEMORY_USAGE/NONE>=75)  ,\
            defCHASSISCPU_80                        |RASLOG,SNMP,EMAIL            |CHASSIS(CPU/NONE>=80)  ,\
            defSWITCHMARG_PORTS_5                   |SW_CRITICAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=5)  ,\
            defSWITCHMARG_PORTS_6                   |SW_MARGINAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=6)  ,\
            defSWITCHMARG_PORTS_10                  |SW_CRITICAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=10)  ,\
            defSWITCHMARG_PORTS_11                  |SW_MARGINAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=11)  ,\
            defSWITCHMARG_PORTS_25                  |SW_CRITICAL,SNMP,EMAIL       |SWITCH(MARG_PORTS/NONE>=25)  ,\
            defSWITCHFAULTY_PORTS_5                 |SW_CRITICAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=5)  ,\
            defSWITCHFAULTY_PORTS_6                 |SW_MARGINAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=6)  ,\
            defSWITCHFAULTY_PORTS_10                |SW_CRITICAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=10)  ,\
            defSWITCHFAULTY_PORTS_11                |SW_MARGINAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=11)  ,\
            defSWITCHFAULTY_PORTS_25                |SW_CRITICAL,SNMP,EMAIL       |SWITCH(FAULTY_PORTS/NONE>=25)  ,\
            defCHASSISBAD_TEMP_MARG                 |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(BAD_TEMP/NONE>=1)  ,\
            defCHASSISBAD_TEMP_CRIT                 |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_TEMP/NONE>=2)  ,\
            defCHASSISBAD_PWR_CRIT                  |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_PWR/NONE>=3)  ,\
            defCHASSISBAD_FAN_MARG                  |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(BAD_FAN/NONE>=1)  ,\
            defCHASSISBAD_FAN_CRIT                  |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_FAN/NONE>=2)  ,\
            defCHASSISDOWN_CORE_1                   |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(DOWN_CORE/NONE>=1)  ,\
            defCHASSISDOWN_CORE_2                   |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(DOWN_CORE/NONE>=2)  ,\
            defCHASSISWWN_DOWN_1                    |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(WWN_DOWN/NONE>=1)  ,\
            defCHASSISHA_SYNC_0                     |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(HA_SYNC/NONE==0)  ,\
            defCHASSISFAULTY_BLADE_1                |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(FAULTY_BLADE/NONE>=1)  ,\
            defALL_PORTSSFP_STATE_FAULTY            |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==FAULTY)  ,\
            defALL_PORTSSFP_STATE_IN                |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==IN)  ,\
            defALL_PORTSSFP_STATE_OFF               |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==OFF)  ,\
            defALL_PORTSSFP_STATE_OUT               |RASLOG,SNMP,EMAIL            |ALL_PORTS(SFP_STATE/NONE==OUT)  ,\
            defALL_PSPS_STATE_FAULTY                |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==FAULTY)  ,\
            defALL_PSPS_STATE_IN                    |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==IN)  ,\
            defALL_PSPS_STATE_OFF                   |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==OFF)  ,\
            defALL_PSPS_STATE_OUT                   |RASLOG,SNMP,EMAIL            |ALL_PS(PS_STATE/NONE==OUT)  ,\
            defALL_FANFAN_STATE_FAULTY              |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==FAULTY)  ,\
            defALL_FANFAN_STATE_IN                  |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==IN)  ,\
            defALL_FANFAN_STATE_OFF                 |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==OFF)  ,\
            defALL_FANFAN_STATE_OUT                 |RASLOG,SNMP,EMAIL            |ALL_FAN(FAN_STATE/NONE==OUT)  ,\
            defALL_WWNWWN_FAULTY                    |RASLOG,SNMP,EMAIL            |ALL_WWN(WWN/NONE==FAULTY)  ,\
            defALL_WWNWWN_ON                        |RASLOG,SNMP,EMAIL,SNMP,EMAIL |ALL_WWN(WWN/NONE==ON)  ,\
            defALL_WWNWWN_IN                        |RASLOG,SNMP,EMAIL,SNMP,EMAIL |ALL_WWN(WWN/NONE==IN)  ,\
            defALL_WWNWWN_OFF                       |RASLOG,SNMP,EMAIL,SNMP,EMAIL |ALL_WWN(WWN/NONE==OFF)  ,\
            defALL_WWNWWN_OUT                       |RASLOG,SNMP,EMAIL            |ALL_WWN(WWN/NONE==OUT)  ,\
            defALL_SLOTSBLADE_STATE_FAULTY          |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==FAULTY)  ,\
            defALL_SLOTSBLADE_STATE_IN              |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==IN)  ,\
            defALL_SLOTSBLADE_STATE_OFF             |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==OFF)  ,\
            defALL_SLOTSBLADE_STATE_OUT             |RASLOG,SNMP,EMAIL            |ALL_SLOTS(BLADE_STATE/NONE==OUT)  ,\
            defCHASSISETH_MGMT_PORT_STATE_DOWN      |RASLOG,SNMP,EMAIL            |CHASSIS(ETH_MGMT_PORT_STATE/NONE==DOWN)  ,\
            defCHASSISETH_MGMT_PORT_STATE_UP        |RASLOG,SNMP,EMAIL            |CHASSIS(ETH_MGMT_PORT_STATE/NONE==UP)  ,\
            defALL_D_PORTSCRC_1                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/MIN>1)  ,\
            defALL_D_PORTSPE_1                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/MIN>1)  ,\
            defALL_D_PORTSITW_1                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/MIN>1)  ,\
            defALL_D_PORTSLF_1                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/MIN>1)  ,\
            defALL_D_PORTSLOSS_SYNC_1               |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/MIN>1)  ,\
            defALL_D_PORTSCRC_H30                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/HOUR>30)  ,\
            defALL_D_PORTSPE_H30                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/HOUR>30)  ,\
            defALL_D_PORTSITW_H30                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/HOUR>30)  ,\
            defALL_D_PORTSLF_H30                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/HOUR>30)  ,\
            defALL_D_PORTSLOSS_SYNC_H30             |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/HOUR>30)  ,\
            defALL_D_PORTSCRC_D500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/DAY>500)  ,\
            defALL_D_PORTSPE_D500                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/DAY>500)  ,\
            defALL_D_PORTSITW_D500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/DAY>500)  ,\
            defALL_D_PORTSLF_D500                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/DAY>500)  ,\
            defALL_D_PORTSLOSS_SYNC_D500            |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/DAY>500)  ,\
            defALL_D_PORTSCRC_2                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/MIN>2)  ,\
            defALL_D_PORTSPE_2                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/MIN>2)  ,\
            defALL_D_PORTSITW_2                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/MIN>2)  ,\
            defALL_D_PORTSLF_2                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/MIN>2)  ,\
            defALL_D_PORTSLOSS_SYNC_2               |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/MIN>2)  ,\
            defALL_D_PORTSCRC_H60                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/HOUR>60)  ,\
            defALL_D_PORTSPE_H60                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/HOUR>60)  ,\
            defALL_D_PORTSITW_H60                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/HOUR>60)  ,\
            defALL_D_PORTSLF_H60                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/HOUR>60)  ,\
            defALL_D_PORTSLOSS_SYNC_H60             |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/HOUR>60)  ,\
            defALL_D_PORTSCRC_D1000                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/DAY>1000)  ,\
            defALL_D_PORTSPE_D1000                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/DAY>1000)  ,\
            defALL_D_PORTSITW_D1000                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/DAY>1000)  ,\
            defALL_D_PORTSLF_D1000                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/DAY>1000)  ,\
            defALL_D_PORTSLOSS_SYNC_D1000           |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/DAY>1000)  ,\
            defALL_D_PORTSCRC_3                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/MIN>3)  ,\
            defALL_D_PORTSPE_3                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/MIN>3)  ,\
            defALL_D_PORTSITW_3                     |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/MIN>3)  ,\
            defALL_D_PORTSLF_3                      |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/MIN>3)  ,\
            defALL_D_PORTSLOSS_SYNC_3               |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/MIN>3)  ,\
            defALL_D_PORTSCRC_H90                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/HOUR>90)  ,\
            defALL_D_PORTSPE_H90                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/HOUR>90)  ,\
            defALL_D_PORTSITW_H90                   |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/HOUR>90)  ,\
            defALL_D_PORTSLF_H90                    |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/HOUR>90)  ,\
            defALL_D_PORTSLOSS_SYNC_H90             |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/HOUR>90)  ,\
            defALL_D_PORTSCRC_D1500                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(CRC/DAY>1500)  ,\
            defALL_D_PORTSPE_D1500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(PE/DAY>1500)  ,\
            defALL_D_PORTSITW_D1500                 |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(ITW/DAY>1500)  ,\
            defALL_D_PORTSLF_D1500                  |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LF/DAY>1500)  ,\
            defALL_D_PORTSLOSS_SYNC_D1500           |RASLOG,SNMP,EMAIL            |ALL_D_PORTS(LOSS_SYNC/DAY>1500)  ,\
            defALL_F_PORTS_IO_PERF_IMPACT           |RASLOG,SNMP,EMAIL            |ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_PERF_IMPACT)  ,\
            defALL_F_PORTS_IO_FRAME_LOSS            |RASLOG,SNMP,EMAIL            |ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_FRAME_LOSS)  ,\
            defALL_F_PORTS_IO_FRAME_LOSS            |RASLOG,SNMP,EMAIL            |ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_FRAME_LOSS) ,\
            defCHASSISBAD_PWR_MARG                  |SW_MARGINAL,SNMP,EMAIL       |CHASSIS(BAD_PWR/NONE>=1)  ,\
            defCHASSISBAD_PWR_CRIT                  |SW_CRITICAL,SNMP,EMAIL       |CHASSIS(BAD_PWR/NONE>=2)  ,\
            defALL_2K_QSFPCURRENT_39                |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(CURRENT/NONE>=39)  ,\
            defALL_2K_QSFPVOLTAGE_3600              |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(VOLTAGE/NONE>=3600)  ,\
            defALL_2K_QSFPRXP_2000                  |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(RXP/NONE>=2000)  ,\
            defALL_2K_QSFPSFP_TEMP_85               |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(SFP_TEMP/NONE>=85)  ,\
            defALL_2K_QSFPVOLTAGE_2900              |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(VOLTAGE/NONE<=2900)  ,\
            defALL_2K_QSFPSFP_TEMP_n15              |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_2K_QSFP(SFP_TEMP/NONE<=-15)  ,\
            defALL_100M_16GSWL_QSFPCURRENT_10       |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(CURRENT/NONE>=10)  ,\
            defALL_100M_16GSWL_QSFPSFP_TEMP_85      |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(SFP_TEMP/NONE>=85)  ,\
            defALL_100M_16GSWL_QSFPSFP_TEMP_n5      |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(SFP_TEMP/NONE<=-5)  ,\
            defALL_100M_16GSWL_QSFPVOLTAGE_2970     |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(VOLTAGE/NONE<=2970)  ,\
            defALL_100M_16GSWL_QSFPVOLTAGE_3630     |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(VOLTAGE/NONE>=3630)  ,\
            defALL_100M_16GSWL_QSFPRXP_2187         |SFP_MARGINAL,RASLOG,SNMP,EMAIL|ALL_100M_16GSWL_QSFP(RXP/NONE>=2187) ,\
        "
    
    ####################################################################################################################
    ####
    ####  rules starting with 8.0.1
    ####
    ###################################################################################################################
    
    l = "defNON_E_F_PORTSCRC_0	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(CRC/MIN>0)	,\
        defNON_E_F_PORTSCRC_2	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(CRC/MIN>2)	,\
        defNON_E_F_PORTSCRC_10	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(CRC/MIN>10)	,\
        defNON_E_F_PORTSCRC_20	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(CRC/MIN>20)	,\
        defNON_E_F_PORTSCRC_21	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(CRC/MIN>21)	,\
        defNON_E_F_PORTSCRC_40	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(CRC/MIN>40)	,\
        defNON_E_F_PORTSITW_15	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(ITW/MIN>15)	,\
        defNON_E_F_PORTSITW_20	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(ITW/MIN>20)	,\
        defNON_E_F_PORTSITW_21	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(ITW/MIN>21)	,\
        defNON_E_F_PORTSITW_40	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(ITW/MIN>40)	,\
        defNON_E_F_PORTSITW_41	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(ITW/MIN>41)	,\
        defNON_E_F_PORTSITW_80	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(ITW/MIN>80)	,\
        defNON_E_F_PORTSLR_2	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LR/MIN>2)	,\
        defNON_E_F_PORTSLR_4	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(LR/MIN>4)	,\
        defNON_E_F_PORTSLR_5	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LR/MIN>5)	,\
        defNON_E_F_PORTSLR_10	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(LR/MIN>10)	,\
        defNON_E_F_PORTSLR_11	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LR/MIN>11)	,\
        defNON_E_F_PORTSLR_20	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(LR/MIN>20)	,\
        defNON_E_F_PORTSSTATE_CHG_2	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(STATE_CHG/MIN>2)	,\
        defNON_E_F_PORTSSTATE_CHG_4	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(STATE_CHG/MIN>4)	,\
        defNON_E_F_PORTSSTATE_CHG_5	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(STATE_CHG/MIN>5)	,\
        defNON_E_F_PORTSSTATE_CHG_10	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(STATE_CHG/MIN>10)	,\
        defNON_E_F_PORTSSTATE_CHG_11	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(STATE_CHG/MIN>11)	,\
        defNON_E_F_PORTSSTATE_CHG_20	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(STATE_CHG/MIN>20)	,\
        defNON_E_F_PORTSLOSS_SIGNAL_0	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LOSS_SIGNAL/MIN>0)	,\
        defNON_E_F_PORTSLOSS_SIGNAL_3	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LOSS_SIGNAL/MIN>3)	,\
        defNON_E_F_PORTSLOSS_SIGNAL_5	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LOSS_SIGNAL/MIN>5)	,\
        defNON_E_F_PORTSPE_0	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(PE/MIN>0)	,\
        defNON_E_F_PORTSPE_2	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(PE/MIN>2)	,\
        defNON_E_F_PORTSPE_3	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(PE/MIN>3)	,\
        defNON_E_F_PORTSPE_7	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(PE/MIN>7)	,\
        defNON_E_F_PORTSPE_5	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(PE/MIN>5)	,\
        defNON_E_F_PORTSPE_10	|FENCE,SNMP,EMAIL	|NON_E_F_PORTS(PE/MIN>10)	,\
        defNON_E_F_PORTSLF_0	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LF/MIN>0)	,\
        defNON_E_F_PORTSLF_3	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LF/MIN>3)	,\
        defNON_E_F_PORTSLF_5	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LF/MIN>5)	,\
        defNON_E_F_PORTSLOSS_SYNC_0	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LOSS_SYNC/MIN>0)	,\
        defNON_E_F_PORTSLOSS_SYNC_3	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LOSS_SYNC/MIN>3)	,\
        defNON_E_F_PORTSLOSS_SYNC_5	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(LOSS_SYNC/MIN>5)	,\
        defNON_E_F_PORTSRX_60	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(RX/HOUR>60)	,\
        defNON_E_F_PORTSRX_75	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(RX/HOUR>75)	,\
        defNON_E_F_PORTSRX_90	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(RX/HOUR>90)	,\
        defNON_E_F_PORTSTX_60	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(TX/HOUR>60)	,\
        defNON_E_F_PORTSTX_75	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(TX/HOUR>75)	,\
        defNON_E_F_PORTSTX_90	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(TX/HOUR>90)	,\
        defNON_E_F_PORTSUTIL_60	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(UTIL/HOUR>60)	,\
        defNON_E_F_PORTSUTIL_75	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(UTIL/HOUR>75)	,\
        defNON_E_F_PORTSUTIL_90	|RASLOG,SNMP,EMAIL	|NON_E_F_PORTS(UTIL/HOUR>90)	,\
        defALL_HOST_PORTSCRC_0	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(CRC/MIN>0)	,\
        defALL_HOST_PORTSCRC_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(CRC/MIN>2)	,\
        defALL_HOST_PORTSCRC_10	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(CRC/MIN>10)	,\
        defALL_HOST_PORTSCRC_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(CRC/MIN>20)	,\
        defALL_HOST_PORTSCRC_21	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(CRC/MIN>21)	,\
        defALL_HOST_PORTSCRC_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(CRC/MIN>40)	,\
        defALL_HOST_PORTSITW_15	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(ITW/MIN>15)	,\
        defALL_HOST_PORTSITW_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(ITW/MIN>20)	,\
        defALL_HOST_PORTSITW_21	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(ITW/MIN>21)	,\
        defALL_HOST_PORTSITW_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(ITW/MIN>40)	,\
        defALL_HOST_PORTSITW_41	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(ITW/MIN>41)	,\
        defALL_HOST_PORTSITW_80	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(ITW/MIN>80)	,\
        defALL_HOST_PORTSLR_2	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LR/MIN>2)	,\
        defALL_HOST_PORTSLR_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(LR/MIN>4)	,\
        defALL_HOST_PORTSLR_5	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LR/MIN>5)	,\
        defALL_HOST_PORTSLR_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(LR/MIN>10)	,\
        defALL_HOST_PORTSLR_11	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LR/MIN>11)	,\
        defALL_HOST_PORTSLR_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(LR/MIN>20)	,\
        defALL_HOST_PORTSSTATE_CHG_2	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(STATE_CHG/MIN>2)	,\
        defALL_HOST_PORTSSTATE_CHG_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(STATE_CHG/MIN>4)	,\
        defALL_HOST_PORTSSTATE_CHG_5	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(STATE_CHG/MIN>5)	,\
        defALL_HOST_PORTSSTATE_CHG_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(STATE_CHG/MIN>10)	,\
        defALL_HOST_PORTSSTATE_CHG_11	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(STATE_CHG/MIN>11)	,\
        defALL_HOST_PORTSSTATE_CHG_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(STATE_CHG/MIN>20)	,\
        defALL_HOST_PORTSLOSS_SIGNAL_0	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LOSS_SIGNAL/MIN>0)	,\
        defALL_HOST_PORTSLOSS_SIGNAL_3	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LOSS_SIGNAL/MIN>3)	,\
        defALL_HOST_PORTSLOSS_SIGNAL_5	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LOSS_SIGNAL/MIN>5)	,\
        defALL_HOST_PORTSPE_0	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(PE/MIN>0)	,\
        defALL_HOST_PORTSPE_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(PE/MIN>2)	,\
        defALL_HOST_PORTSPE_3	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(PE/MIN>3)	,\
        defALL_HOST_PORTSPE_7	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(PE/MIN>7)	,\
        defALL_HOST_PORTSPE_5	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(PE/MIN>5)	,\
        defALL_HOST_PORTSPE_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_HOST_PORTS(PE/MIN>10)	,\
        defALL_HOST_PORTSLF_0	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LF/MIN>0)	,\
        defALL_HOST_PORTSLF_3	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LF/MIN>3)	,\
        defALL_HOST_PORTSLF_5	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LF/MIN>5)	,\
        defALL_HOST_PORTSLOSS_SYNC_0	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LOSS_SYNC/MIN>0)	,\
        defALL_HOST_PORTSLOSS_SYNC_3	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LOSS_SYNC/MIN>3)	,\
        defALL_HOST_PORTSLOSS_SYNC_5	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(LOSS_SYNC/MIN>5)	,\
        defALL_HOST_PORTSRX_60	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(RX/HOUR>60)	,\
        defALL_HOST_PORTSRX_75	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(RX/HOUR>75)	,\
        defALL_HOST_PORTSRX_90	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(RX/HOUR>90)	,\
        defALL_HOST_PORTSTX_60	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(TX/HOUR>60)	,\
        defALL_HOST_PORTSTX_75	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(TX/HOUR>75)	,\
        defALL_HOST_PORTSTX_90	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(TX/HOUR>90)	,\
        defALL_HOST_PORTSUTIL_60	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(UTIL/HOUR>60)	,\
        defALL_HOST_PORTSUTIL_75	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(UTIL/HOUR>75)	,\
        defALL_HOST_PORTSUTIL_90	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(UTIL/HOUR>90)	,\
        defALL_OTHER_F_PORTSCRC_0	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(CRC/MIN>0)	,\
        defALL_OTHER_F_PORTSCRC_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(CRC/MIN>2)	,\
        defALL_OTHER_F_PORTSCRC_10	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(CRC/MIN>10)	,\
        defALL_OTHER_F_PORTSCRC_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(CRC/MIN>20)	,\
        defALL_OTHER_F_PORTSCRC_21	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(CRC/MIN>21)	,\
        defALL_OTHER_F_PORTSCRC_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(CRC/MIN>40)	,\
        defALL_OTHER_F_PORTSITW_15	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(ITW/MIN>15)	,\
        defALL_OTHER_F_PORTSITW_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(ITW/MIN>20)	,\
        defALL_OTHER_F_PORTSITW_21	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(ITW/MIN>21)	,\
        defALL_OTHER_F_PORTSITW_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(ITW/MIN>40)	,\
        defALL_OTHER_F_PORTSITW_41	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(ITW/MIN>41)	,\
        defALL_OTHER_F_PORTSITW_80	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(ITW/MIN>80)	,\
        defALL_OTHER_F_PORTSLR_2	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LR/MIN>2)	,\
        defALL_OTHER_F_PORTSLR_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LR/MIN>4)	,\
        defALL_OTHER_F_PORTSLR_5	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LR/MIN>5)	,\
        defALL_OTHER_F_PORTSLR_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LR/MIN>10)	,\
        defALL_OTHER_F_PORTSLR_11	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LR/MIN>11)	,\
        defALL_OTHER_F_PORTSLR_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LR/MIN>20)	,\
        defALL_OTHER_F_PORTSSTATE_CHG_2	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(STATE_CHG/MIN>2)	,\
        defALL_OTHER_F_PORTSSTATE_CHG_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(STATE_CHG/MIN>4)	,\
        defALL_OTHER_F_PORTSSTATE_CHG_5	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(STATE_CHG/MIN>5)	,\
        defALL_OTHER_F_PORTSSTATE_CHG_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(STATE_CHG/MIN>10)	,\
        defALL_OTHER_F_PORTSSTATE_CHG_11	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(STATE_CHG/MIN>11)	,\
        defALL_OTHER_F_PORTSSTATE_CHG_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(STATE_CHG/MIN>20)	,\
        defALL_OTHER_F_PORTSLOSS_SIGNAL_0	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>0)	,\
        defALL_OTHER_F_PORTSLOSS_SIGNAL_3	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>3)	,\
        defALL_OTHER_F_PORTSLOSS_SIGNAL_5	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LOSS_SIGNAL/MIN>5)	,\
        defALL_OTHER_F_PORTSPE_0	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(PE/MIN>0)	,\
        defALL_OTHER_F_PORTSPE_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(PE/MIN>2)	,\
        defALL_OTHER_F_PORTSPE_3	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(PE/MIN>3)	,\
        defALL_OTHER_F_PORTSPE_7	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(PE/MIN>7)	,\
        defALL_OTHER_F_PORTSPE_5	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(PE/MIN>5)	,\
        defALL_OTHER_F_PORTSPE_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_OTHER_F_PORTS(PE/MIN>10)	,\
        defALL_OTHER_F_PORTSLF_0	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LF/MIN>0)	,\
        defALL_OTHER_F_PORTSLF_3	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LF/MIN>3)	,\
        defALL_OTHER_F_PORTSLF_5	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LF/MIN>5)	,\
        defALL_OTHER_F_PORTSLOSS_SYNC_0	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>0)	,\
        defALL_OTHER_F_PORTSLOSS_SYNC_3	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>3)	,\
        defALL_OTHER_F_PORTSLOSS_SYNC_5	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(LOSS_SYNC/MIN>5)	,\
        defALL_OTHER_F_PORTSRX_60	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(RX/HOUR>60)	,\
        defALL_OTHER_F_PORTSRX_75	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(RX/HOUR>75)	,\
        defALL_OTHER_F_PORTSRX_90	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(RX/HOUR>90)	,\
        defALL_OTHER_F_PORTSTX_60	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(TX/HOUR>60)	,\
        defALL_OTHER_F_PORTSTX_75	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(TX/HOUR>75)	,\
        defALL_OTHER_F_PORTSTX_90	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(TX/HOUR>90)	,\
        defALL_OTHER_F_PORTSUTIL_60	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(UTIL/HOUR>60)	,\
        defALL_OTHER_F_PORTSUTIL_75	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(UTIL/HOUR>75)	,\
        defALL_OTHER_F_PORTSUTIL_90	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(UTIL/HOUR>90)	,\
        defALL_HOST_PORTSC3TXTO_2	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(C3TXTO/MIN>2)	,\
        defALL_HOST_PORTSC3TXTO_4	|FENCE,DECOM,SNMP,EMAIL,FMS	|ALL_HOST_PORTS(C3TXTO/MIN>4)	,\
        defALL_HOST_PORTSC3TXTO_3	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(C3TXTO/MIN>3)	,\
        defALL_HOST_PORTSC3TXTO_10	|FENCE,DECOM,SNMP,EMAIL,FMS	|ALL_HOST_PORTS(C3TXTO/MIN>10)	,\
        defALL_HOST_PORTSC3TXTO_11	|RASLOG,SNMP,EMAIL	|ALL_HOST_PORTS(C3TXTO/MIN>11)	,\
        defALL_HOST_PORTSC3TXTO_20	|FENCE,DECOM,SNMP,EMAIL,FMS	|ALL_HOST_PORTS(C3TXTO/MIN>20)	,\
        defALL_OTHER_F_PORTSC3TXTO_2	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(C3TXTO/MIN>2)	,\
        defALL_OTHER_F_PORTSC3TXTO_4	|FENCE,DECOM,SNMP,EMAIL,FMS	|ALL_OTHER_F_PORTS(C3TXTO/MIN>4)	,\
        defALL_OTHER_F_PORTSC3TXTO_3	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(C3TXTO/MIN>3)	,\
        defALL_OTHER_F_PORTSC3TXTO_10	|FENCE,DECOM,SNMP,EMAIL,FMS	|ALL_OTHER_F_PORTS(C3TXTO/MIN>10)	,\
        defALL_OTHER_F_PORTSC3TXTO_11	|RASLOG,SNMP,EMAIL	|ALL_OTHER_F_PORTS(C3TXTO/MIN>11)	,\
        defALL_OTHER_F_PORTSC3TXTO_20	|FENCE,DECOM,SNMP,EMAIL,FMS	|ALL_OTHER_F_PORTS(C3TXTO/MIN>20)	,\
        defALL_E_PORTSCRC_0	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(CRC/MIN>0)	,\
        defALL_E_PORTSCRC_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(CRC/MIN>2)	,\
        defALL_E_PORTSCRC_10	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(CRC/MIN>10)	,\
        defALL_E_PORTSCRC_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(CRC/MIN>20)	,\
        defALL_E_PORTSCRC_21	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(CRC/MIN>21)	,\
        defALL_E_PORTSCRC_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(CRC/MIN>40)	,\
        defALL_E_PORTSITW_15	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(ITW/MIN>15)	,\
        defALL_E_PORTSITW_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(ITW/MIN>20)	,\
        defALL_E_PORTSITW_21	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(ITW/MIN>21)	,\
        defALL_E_PORTSITW_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(ITW/MIN>40)	,\
        defALL_E_PORTSITW_41	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(ITW/MIN>41)	,\
        defALL_E_PORTSITW_80	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(ITW/MIN>80)	,\
        defALL_E_PORTSLR_2	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LR/MIN>2)	,\
        defALL_E_PORTSLR_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(LR/MIN>4)	,\
        defALL_E_PORTSLR_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LR/MIN>5)	,\
        defALL_E_PORTSLR_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(LR/MIN>10)	,\
        defALL_E_PORTSLR_11	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LR/MIN>11)	,\
        defALL_E_PORTSLR_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(LR/MIN>20)	,\
        defALL_E_PORTSSTATE_CHG_2	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(STATE_CHG/MIN>2)	,\
        defALL_E_PORTSSTATE_CHG_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(STATE_CHG/MIN>4)	,\
        defALL_E_PORTSSTATE_CHG_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(STATE_CHG/MIN>5)	,\
        defALL_E_PORTSSTATE_CHG_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(STATE_CHG/MIN>10)	,\
        defALL_E_PORTSSTATE_CHG_11	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(STATE_CHG/MIN>11)	,\
        defALL_E_PORTSSTATE_CHG_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(STATE_CHG/MIN>20)	,\
        defALL_E_PORTSLOSS_SIGNAL_0	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LOSS_SIGNAL/MIN>0)	,\
        defALL_E_PORTSLOSS_SIGNAL_3	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LOSS_SIGNAL/MIN>3)	,\
        defALL_E_PORTSLOSS_SIGNAL_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LOSS_SIGNAL/MIN>5)	,\
        defALL_E_PORTSPE_0	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(PE/MIN>0)	,\
        defALL_E_PORTSPE_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(PE/MIN>2)	,\
        defALL_E_PORTSPE_3	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(PE/MIN>3)	,\
        defALL_E_PORTSPE_7	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(PE/MIN>7)	,\
        defALL_E_PORTSPE_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(PE/MIN>5)	,\
        defALL_E_PORTSPE_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_E_PORTS(PE/MIN>10)	,\
        defALL_E_PORTSLF_0	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LF/MIN>0)	,\
        defALL_E_PORTSLF_3	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LF/MIN>3)	,\
        defALL_E_PORTSLF_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LF/MIN>5)	,\
        defALL_E_PORTSLOSS_SYNC_0	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LOSS_SYNC/MIN>0)	,\
        defALL_E_PORTSLOSS_SYNC_3	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LOSS_SYNC/MIN>3)	,\
        defALL_E_PORTSLOSS_SYNC_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(LOSS_SYNC/MIN>5)	,\
        defALL_E_PORTSRX_60	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(RX/HOUR>60)	,\
        defALL_E_PORTSRX_75	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(RX/HOUR>75)	,\
        defALL_E_PORTSRX_90	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(RX/HOUR>90)	,\
        defALL_E_PORTSTX_60	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(TX/HOUR>60)	,\
        defALL_E_PORTSTX_75	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(TX/HOUR>75)	,\
        defALL_E_PORTSTX_90	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(TX/HOUR>90)	,\
        defALL_E_PORTSUTIL_60	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(UTIL/HOUR>60)	,\
        defALL_E_PORTSUTIL_75	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(UTIL/HOUR>75)	,\
        defALL_E_PORTSUTIL_90	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(UTIL/HOUR>90)	,\
        defALL_E_PORTSC3TXTO_5	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(C3TXTO/MIN>5)	,\
        defALL_E_PORTSC3TXTO_10	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(C3TXTO/MIN>10)	,\
        defALL_E_PORTSC3TXTO_20	|RASLOG,SNMP,EMAIL	|ALL_E_PORTS(C3TXTO/MIN>20)	,\
        defALL_TARGET_PORTSC3TXTO_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(C3TXTO/MIN>0)	,\
        defALL_TARGET_PORTSC3TXTO_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(C3TXTO/MIN>2)	,\
        defALL_TARGET_PORTSC3TXTO_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(C3TXTO/MIN>3)	,\
        defALL_TARGET_PORTSC3TXTO_5	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(C3TXTO/MIN>5)	,\
        defALL_TARGET_PORTSC3TXTO_6	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(C3TXTO/MIN>6)	,\
        defALL_TARGET_PORTSC3TXTO_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(C3TXTO/MIN>10)	,\
        defALL_TARGET_PORTSCRC_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(CRC/MIN>0)	,\
        defALL_TARGET_PORTSCRC_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(CRC/MIN>2)	,\
        defALL_TARGET_PORTSCRC_5	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(CRC/MIN>5)	,\
        defALL_TARGET_PORTSCRC_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(CRC/MIN>10)	,\
        defALL_TARGET_PORTSCRC_11	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(CRC/MIN>11)	,\
        defALL_TARGET_PORTSCRC_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(CRC/MIN>20)	,\
        defALL_TARGET_PORTSITW_5	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(ITW/MIN>5)	,\
        defALL_TARGET_PORTSITW_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(ITW/MIN>10)	,\
        defALL_TARGET_PORTSITW_11	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(ITW/MIN>11)	,\
        defALL_TARGET_PORTSITW_20	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(ITW/MIN>20)	,\
        defALL_TARGET_PORTSITW_21	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(ITW/MIN>21)	,\
        defALL_TARGET_PORTSITW_40	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(ITW/MIN>40)	,\
        defALL_TARGET_PORTSLR_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LR/MIN>0)	,\
        defALL_TARGET_PORTSLR_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(LR/MIN>2)	,\
        defALL_TARGET_PORTSLR_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LR/MIN>3)	,\
        defALL_TARGET_PORTSLR_5	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(LR/MIN>5)	,\
        defALL_TARGET_PORTSLR_6	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LR/MIN>6)	,\
        defALL_TARGET_PORTSLR_10	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(LR/MIN>10)	,\
        defALL_TARGET_PORTSSTATE_CHG_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(STATE_CHG/MIN>0)	,\
        defALL_TARGET_PORTSSTATE_CHG_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(STATE_CHG/MIN>2)	,\
        defALL_TARGET_PORTSSTATE_CHG_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(STATE_CHG/MIN>3)	,\
        defALL_TARGET_PORTSSTATE_CHG_7	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(STATE_CHG/MIN>7)	,\
        defALL_TARGET_PORTSSTATE_CHG_8	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(STATE_CHG/MIN>8)	,\
        defALL_TARGET_PORTSSTATE_CHG_15	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(STATE_CHG/MIN>15)	,\
        defALL_TARGET_PORTSLOSS_SIGNAL_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>0)	,\
        defALL_TARGET_PORTSLOSS_SIGNAL_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>3)	,\
        defALL_TARGET_PORTSLOSS_SIGNAL_5	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LOSS_SIGNAL/MIN>5)	,\
        defALL_TARGET_PORTSPE_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(PE/MIN>0)	,\
        defALL_TARGET_PORTSPE_2	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(PE/MIN>2)	,\
        defALL_TARGET_PORTSPE_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(PE/MIN>3)	,\
        defALL_TARGET_PORTSPE_4	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(PE/MIN>4)	,\
        defALL_TARGET_PORTSPE_5	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(PE/MIN>5)	,\
        defALL_TARGET_PORTSPE_6	|FENCE,DECOM,SNMP,EMAIL	|ALL_TARGET_PORTS(PE/MIN>6)	,\
        defALL_TARGET_PORTSLF_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LF/MIN>0)	,\
        defALL_TARGET_PORTSLF_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LF/MIN>3)	,\
        defALL_TARGET_PORTSLF_5	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LF/MIN>5)	,\
        defALL_TARGET_PORTSLOSS_SYNC_0	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LOSS_SYNC/MIN>0)	,\
        defALL_TARGET_PORTSLOSS_SYNC_3	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LOSS_SYNC/MIN>3)	,\
        defALL_TARGET_PORTSLOSS_SYNC_5	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(LOSS_SYNC/MIN>5)	,\
        defALL_TARGET_PORTSRX_60	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(RX/HOUR>60)	,\
        defALL_TARGET_PORTSRX_75	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(RX/HOUR>75)	,\
        defALL_TARGET_PORTSRX_90	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(RX/HOUR>90)	,\
        defALL_TARGET_PORTSTX_60	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(TX/HOUR>60)	,\
        defALL_TARGET_PORTSTX_75	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(TX/HOUR>75)	,\
        defALL_TARGET_PORTSTX_90	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(TX/HOUR>90)	,\
        defALL_TARGET_PORTSUTIL_60	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(UTIL/HOUR>60)	,\
        defALL_TARGET_PORTSUTIL_75	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(UTIL/HOUR>75)	,\
        defALL_TARGET_PORTSUTIL_90	|RASLOG,SNMP,EMAIL	|ALL_TARGET_PORTS(UTIL/HOUR>90)	,\
        defALL_CIRCUITSCIR_STATE_0	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_STATE/MIN>0)	,\
        defALL_CIRCUITSCIR_STATE_3	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_STATE/MIN>3)	,\
        defALL_CIRCUITSCIR_STATE_5	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_STATE/MIN>5)	,\
        defALL_CIRCUITSCIR_UTIL_60	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_UTIL/MIN>60)	,\
        defALL_CIRCUITSCIR_UTIL_75	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_UTIL/MIN>75)	,\
        defALL_CIRCUITSCIR_UTIL_90	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_UTIL/MIN>90)	,\
        defALL_CIRCUITSCIR_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.05)	,\
        defALL_CIRCUITSCIR_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.1)	,\
        defALL_CIRCUITSCIR_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(CIR_PKTLOSS/MIN>0.5)	,\
        defALL_CIRCUITS_RTT_250	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(RTT/NONE>250)	,\
        defALL_CIRCUITS_JITTER_PER_05	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(JITTER/NONE>5)	,\
        defALL_CIRCUITS_JITTER_PER_15	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(JITTER/NONE>15)	,\
        defALL_CIRCUITS_JITTER_PER_20	|RASLOG,SNMP,EMAIL	|ALL_CIRCUITS(JITTER/NONE>20)	,\
        defALL_CIRCUIT_F_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_F_QOS(UTIL/HOUR>50)	,\
        defALL_CIRCUIT_F_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_F_QOS(UTIL/HOUR>75)	,\
        defALL_CIRCUIT_F_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_F_QOS(UTIL/HOUR>90)	,\
        defALL_CIRCUIT_HIGH_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_HIGH_QOS(UTIL/HOUR>50)	,\
        defALL_CIRCUIT_HIGH_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_HIGH_QOS(UTIL/HOUR>75)	,\
        defALL_CIRCUIT_HIGH_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_HIGH_QOS(UTIL/HOUR>90)	,\
        defALL_CIRCUIT_MED_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_MED_QOS(UTIL/HOUR>50)	,\
        defALL_CIRCUIT_MED_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_MED_QOS(UTIL/HOUR>75)	,\
        defALL_CIRCUIT_MED_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_MED_QOS(UTIL/HOUR>90)	,\
        defALL_CIRCUIT_LOW_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_LOW_QOS(UTIL/HOUR>50)	,\
        defALL_CIRCUIT_LOW_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_LOW_QOS(UTIL/HOUR>75)	,\
        defALL_CIRCUIT_LOW_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_LOW_QOS(UTIL/HOUR>90)	,\
        defALL_CIRCUIT_F_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_F_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_CIRCUIT_F_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_F_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_CIRCUIT_F_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_F_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_CIRCUIT_HIGH_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_HIGH_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_CIRCUIT_HIGH_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_HIGH_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_CIRCUIT_HIGH_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_HIGH_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_CIRCUIT_MED_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_MED_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_CIRCUIT_MED_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_MED_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_CIRCUIT_MED_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_MED_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_CIRCUIT_LOW_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_LOW_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_CIRCUIT_LOW_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_LOW_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_CIRCUIT_LOW_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_CIRCUIT_LOW_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_TUNNELSSTATE_CHG_0	|RASLOG,SNMP,EMAIL	|ALL_TUNNELS(STATE_CHG/MIN>0)	,\
        defALL_TUNNELSSTATE_CHG_1	|RASLOG,SNMP,EMAIL	|ALL_TUNNELS(STATE_CHG/MIN>1)	,\
        defALL_TUNNELSSTATE_CHG_3	|RASLOG,SNMP,EMAIL	|ALL_TUNNELS(STATE_CHG/MIN>3)	,\
        defALL_TUNNELSUTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_TUNNELS(UTIL/HOUR>50)	,\
        defALL_TUNNELSUTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_TUNNELS(UTIL/HOUR>75)	,\
        defALL_TUNNELSUTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_TUNNELS(UTIL/HOUR>90)	,\
        defALL_TUNNEL_F_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_F_QOS(UTIL/HOUR>50)	,\
        defALL_TUNNEL_F_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_F_QOS(UTIL/HOUR>75)	,\
        defALL_TUNNEL_F_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_F_QOS(UTIL/HOUR>90)	,\
        defALL_TUNNEL_HIGH_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_HIGH_QOS(UTIL/HOUR>50)	,\
        defALL_TUNNEL_HIGH_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_HIGH_QOS(UTIL/HOUR>75)	,\
        defALL_TUNNEL_HIGH_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_HIGH_QOS(UTIL/HOUR>90)	,\
        defALL_TUNNEL_MED_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_MED_QOS(UTIL/HOUR>50)	,\
        defALL_TUNNEL_MED_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_MED_QOS(UTIL/HOUR>75)	,\
        defALL_TUNNEL_MED_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_MED_QOS(UTIL/HOUR>90)	,\
        defALL_TUNNEL_LOW_QOS_UTIL_PER_50	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_LOW_QOS(UTIL/HOUR>50)	,\
        defALL_TUNNEL_LOW_QOS_UTIL_PER_75	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_LOW_QOS(UTIL/HOUR>75)	,\
        defALL_TUNNEL_LOW_QOS_UTIL_PER_90	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_LOW_QOS(UTIL/HOUR>90)	,\
        defALL_TUNNEL_F_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_F_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_TUNNEL_F_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_F_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_TUNNEL_F_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_F_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_TUNNEL_HIGH_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_HIGH_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_TUNNEL_HIGH_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_HIGH_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_TUNNEL_HIGH_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_HIGH_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_TUNNEL_MED_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_MED_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_TUNNEL_MED_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_MED_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_TUNNEL_MED_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_MED_QOS(PKTLOSS/MIN>0.5)	,\
        defALL_TUNNEL_LOW_QOS_PKTLOSS_PER_05	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_LOW_QOS(PKTLOSS/MIN>0.05)	,\
        defALL_TUNNEL_LOW_QOS_PKTLOSS_PER_1	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_LOW_QOS(PKTLOSS/MIN>0.1)	,\
        defALL_TUNNEL_LOW_QOS_PKTLOSS_PER_5	|RASLOG,SNMP,EMAIL	|ALL_TUNNEL_LOW_QOS(PKTLOSS/MIN>0.5)	,\
        defSWITCHEPORT_DOWN_1	|RASLOG,SNMP,EMAIL	|SWITCH(EPORT_DOWN/MIN>1)	,\
        defSWITCHEPORT_DOWN_2	|RASLOG,SNMP,EMAIL	|SWITCH(EPORT_DOWN/MIN>2)	,\
        defSWITCHEPORT_DOWN_4	|RASLOG,SNMP,EMAIL	|SWITCH(EPORT_DOWN/MIN>4)	,\
        defSWITCHFAB_CFG_1	|RASLOG,SNMP,EMAIL	|SWITCH(FAB_CFG/MIN>1)	,\
        defSWITCHFAB_CFG_2	|RASLOG,SNMP,EMAIL	|SWITCH(FAB_CFG/MIN>2)	,\
        defSWITCHFAB_CFG_4	|RASLOG,SNMP,EMAIL	|SWITCH(FAB_CFG/MIN>4)	,\
        defSWITCHFAB_SEG_1	|RASLOG,SNMP,EMAIL	|SWITCH(FAB_SEG/MIN>1)	,\
        defSWITCHFAB_SEG_2	|RASLOG,SNMP,EMAIL	|SWITCH(FAB_SEG/MIN>2)	,\
        defSWITCHFAB_SEG_4	|RASLOG,SNMP,EMAIL	|SWITCH(FAB_SEG/MIN>4)	,\
        defSWITCHFLOGI_4	|RASLOG,SNMP,EMAIL	|SWITCH(FLOGI/MIN>4)	,\
        defSWITCHFLOGI_6	|RASLOG,SNMP,EMAIL	|SWITCH(FLOGI/MIN>6)	,\
        defSWITCHFLOGI_8	|RASLOG,SNMP,EMAIL	|SWITCH(FLOGI/MIN>8)	,\
        defSWITCHZONE_CHG_2	|RASLOG,SNMP,EMAIL	|SWITCH(ZONE_CHG/DAY>2)	,\
        defSWITCHZONE_CHG_5	|RASLOG,SNMP,EMAIL	|SWITCH(ZONE_CHG/DAY>5)	,\
        defSWITCHZONE_CHG_10	|RASLOG,SNMP,EMAIL	|SWITCH(ZONE_CHG/DAY>10)	,\
        defSWITCHDID_CHG_1	|RASLOG,SNMP,EMAIL	|SWITCH(DID_CHG/MIN>1)	,\
        defSWITCHL2_DEVCNT_PER_60	|RASLOG,SNMP,EMAIL	|SWITCH(L2_DEVCNT_PER/NONE>60)	,\
        defSWITCHL2_DEVCNT_PER_75	|RASLOG,SNMP,EMAIL	|SWITCH(L2_DEVCNT_PER/NONE>75)	,\
        defSWITCHL2_DEVCNT_PER_90	|RASLOG,SNMP,EMAIL	|SWITCH(L2_DEVCNT_PER/NONE>90)	,\
        defSWITCHLSAN_DEVCNT_PER_60	|RASLOG,SNMP,EMAIL	|SWITCH(LSAN_DEVCNT_PER/NONE>60)	,\
        defSWITCHLSAN_DEVCNT_PER_75	|RASLOG,SNMP,EMAIL	|SWITCH(LSAN_DEVCNT_PER/NONE>75)	,\
        defSWITCHLSAN_DEVCNT_PER_90	|RASLOG,SNMP,EMAIL	|SWITCH(LSAN_DEVCNT_PER/NONE>90)	,\
        defSWITCHZONE_CFGSZ_PER_70	|RASLOG,SNMP,EMAIL	|SWITCH(ZONE_CFGSZ_PER/NONE>70)	,\
        defSWITCHZONE_CFGSZ_PER_80	|RASLOG,SNMP,EMAIL	|SWITCH(ZONE_CFGSZ_PER/NONE>80)	,\
        defSWITCHZONE_CFGSZ_PER_90	|RASLOG,SNMP,EMAIL	|SWITCH(ZONE_CFGSZ_PER/NONE>90)	,\
        defSWITCHBB_FCR_CNT_12	|RASLOG,SNMP,EMAIL	|SWITCH(BB_FCR_CNT/NONE>12)	,\
        defSWITCHSEC_TELNET_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TELNET/MIN>0)	,\
        defSWITCHSEC_TELNET_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TELNET/MIN>2)	,\
        defSWITCHSEC_TELNET_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TELNET/MIN>4)	,\
        defSWITCHSEC_HTTP_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_HTTP/MIN>0)	,\
        defSWITCHSEC_HTTP_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_HTTP/MIN>2)	,\
        defSWITCHSEC_HTTP_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_HTTP/MIN>4)	,\
        defSWITCHSEC_SCC_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_SCC/MIN>0)	,\
        defSWITCHSEC_SCC_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_SCC/MIN>2)	,\
        defSWITCHSEC_SCC_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_SCC/MIN>4)	,\
        defSWITCHSEC_DCC_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_DCC/MIN>0)	,\
        defSWITCHSEC_DCC_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_DCC/MIN>2)	,\
        defSWITCHSEC_DCC_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_DCC/MIN>4)	,\
        defSWITCHSEC_LV_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_LV/MIN>0)	,\
        defSWITCHSEC_LV_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_LV/MIN>2)	,\
        defSWITCHSEC_LV_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_LV/MIN>4)	,\
        defSWITCHSEC_CERT_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_CERT/MIN>0)	,\
        defSWITCHSEC_CERT_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_CERT/MIN>2)	,\
        defSWITCHSEC_CERT_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_CERT/MIN>4)	,\
        defSWITCHSEC_AUTH_FAIL_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_AUTH_FAIL/MIN>0)	,\
        defSWITCHSEC_AUTH_FAIL_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_AUTH_FAIL/MIN>2)	,\
        defSWITCHSEC_AUTH_FAIL_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_AUTH_FAIL/MIN>4)	,\
        defSWITCHSEC_FCS_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_FCS/MIN>0)	,\
        defSWITCHSEC_FCS_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_FCS/MIN>2)	,\
        defSWITCHSEC_FCS_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_FCS/MIN>4)	,\
        defSWITCHSEC_IDB_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_IDB/MIN>0)	,\
        defSWITCHSEC_IDB_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_IDB/MIN>2)	,\
        defSWITCHSEC_IDB_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_IDB/MIN>4)	,\
        defSWITCHSEC_CMD_0	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_CMD/MIN>0)	,\
        defSWITCHSEC_CMD_2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_CMD/MIN>2)	,\
        defSWITCHSEC_CMD_4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_CMD/MIN>4)	,\
        defSWITCHSEC_TS_H1	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TS/HOUR>1)	,\
        defSWITCHSEC_TS_H2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TS/HOUR>2)	,\
        defSWITCHSEC_TS_H4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TS/HOUR>4)	,\
        defSWITCHSEC_TS_D2	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TS/DAY>2)	,\
        defSWITCHSEC_TS_D4	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TS/DAY>4)	,\
        defSWITCHSEC_TS_D10	|RASLOG,SNMP,EMAIL	|SWITCH(SEC_TS/DAY>10)	,\
        defALL_TSTEMP_OUT_OF_RANGE	|RASLOG,SNMP,EMAIL	|ALL_TS(TEMP/NONE==OUT_OF_RANGE)	,\
        defALL_OTHER_SFPCURRENT_50	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(CURRENT/NONE>=50)	,\
        defALL_OTHER_SFPVOLTAGE_3630	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(VOLTAGE/NONE>=3630)	,\
        defALL_OTHER_SFPRXP_5000	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(RXP/NONE>=5000)	,\
        defALL_OTHER_SFPTXP_5000	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(TXP/NONE>=5000)	,\
        defALL_OTHER_SFPSFP_TEMP_85	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(SFP_TEMP/NONE>=85)	,\
        defALL_OTHER_SFPVOLTAGE_2960	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(VOLTAGE/NONE<=2960)	,\
        defALL_OTHER_SFPSFP_TEMP_n13	|RASLOG,SNMP,EMAIL	|ALL_OTHER_SFP(SFP_TEMP/NONE<=-13)	,\
        defALL_10GSWL_SFPCURRENT_10	|SFP_MARGINAL,RASLOG,SNMP,EMAIL |ALL_10GSWL_SFP(CURRENT/NONE>=10)	|ALL_10GSWL_SFP(CURRENT/NONE>=10)	,\
        defALL_10GSWL_SFPVOLTAGE_3600	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GSWL_SFP(VOLTAGE/NONE>=3600)	,\
        defALL_10GSWL_SFPRXP_1999	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GSWL_SFP(RXP/NONE>=1999)	,\
        defALL_10GSWL_SFPTXP_1999	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GSWL_SFP(TXP/NONE>=1999)	,\
        defALL_10GSWL_SFPSFP_TEMP_90	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GSWL_SFP(SFP_TEMP/NONE>=90)	,\
        defALL_10GSWL_SFPVOLTAGE_3000	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GSWL_SFP(VOLTAGE/NONE<=3000)	,\
        defALL_10GSWL_SFPSFP_TEMP_n5	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GSWL_SFP(SFP_TEMP/NONE<=-5)	,\
        defALL_10GLWL_SFPCURRENT_95	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(CURRENT/NONE>=95)	,\
        defALL_10GLWL_SFPVOLTAGE_3600	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(VOLTAGE/NONE>=3600)	,\
        defALL_10GLWL_SFPRXP_2230	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(RXP/NONE>=2230)	,\
        defALL_10GLWL_SFPTXP_2230	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(TXP/NONE>=2230)	,\
        defALL_10GLWL_SFPSFP_TEMP_90	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(SFP_TEMP/NONE>=90)	,\
        defALL_10GLWL_SFPVOLTAGE_2970	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(VOLTAGE/NONE<=2970)	,\
        defALL_10GLWL_SFPSFP_TEMP_n5	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_10GLWL_SFP(SFP_TEMP/NONE<=-5)	,\
        defALL_16GSWL_SFPCURRENT_12	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(CURRENT/NONE>=12)	,\
        defALL_16GSWL_SFPVOLTAGE_3600	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(VOLTAGE/NONE>=3600)	,\
        defALL_16GSWL_SFPRXP_1259	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(RXP/NONE>=1259)	,\
        defALL_16GSWL_SFPTXP_1259	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(TXP/NONE>=1259)	,\
        defALL_16GSWL_SFPSFP_TEMP_85	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(SFP_TEMP/NONE>=85)	,\
        defALL_16GSWL_SFPVOLTAGE_3000	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(VOLTAGE/NONE<=3000)	,\
        defALL_16GSWL_SFPSFP_TEMP_n5	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GSWL_SFP(SFP_TEMP/NONE<=-5)	,\
        defALL_16GLWL_SFPCURRENT_70	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(CURRENT/NONE>=70)	,\
        defALL_16GLWL_SFPVOLTAGE_3600	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(VOLTAGE/NONE>=3600)	,\
        defALL_16GLWL_SFPRXP_1995	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(RXP/NONE>=1995)	,\
        defALL_16GLWL_SFPTXP_1995	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(TXP/NONE>=1995)	,\
        defALL_16GLWL_SFPSFP_TEMP_90	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(SFP_TEMP/NONE>=90)	,\
        defALL_16GLWL_SFPVOLTAGE_3000	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(VOLTAGE/NONE<=3000)	,\
        defALL_16GLWL_SFPSFP_TEMP_n5	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_16GLWL_SFP(SFP_TEMP/NONE<=-5)	,\
        defALL_QSFPCURRENT_10	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_QSFP(CURRENT/NONE>=10)	,\
        defALL_QSFPVOLTAGE_3600	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_QSFP(VOLTAGE/NONE>=3600)	,\
        defALL_QSFPRXP_2180	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_QSFP(RXP/NONE>=2180)	,\
        defALL_QSFPSFP_TEMP_85	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_QSFP(SFP_TEMP/NONE>=85)	,\
        defALL_QSFPVOLTAGE_2940	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_QSFP(VOLTAGE/NONE<=2940)	,\
        defALL_QSFPSFP_TEMP_n5	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_QSFP(SFP_TEMP/NONE<=-5)	,\
        defCHASSISFLASH_USAGE_90	|RASLOG,SNMP,EMAIL	|CHASSIS(FLASH_USAGE/NONE>=90)	,\
        defCHASSISMEMORY_USAGE_75	|RASLOG,SNMP,EMAIL	|CHASSIS(MEMORY_USAGE/NONE>=75)	,\
        defCHASSISCPU_80	|RASLOG,SNMP,EMAIL	|CHASSIS(CPU/NONE>=80)	,\
        defSWITCHMARG_PORTS_5	|SW_CRITICAL,SNMP,EMAIL	|SWITCH(MARG_PORTS/NONE>=5)	,\
        defSWITCHMARG_PORTS_6	|SW_MARGINAL,SNMP,EMAIL	|SWITCH(MARG_PORTS/NONE>=6)	,\
        defSWITCHMARG_PORTS_10	|SW_CRITICAL,SNMP,EMAIL	|SWITCH(MARG_PORTS/NONE>=10)	,\
        defSWITCHMARG_PORTS_11	|SW_MARGINAL,SNMP,EMAIL	|SWITCH(MARG_PORTS/NONE>=11)	,\
        defSWITCHMARG_PORTS_25	|SW_CRITICAL,SNMP,EMAIL	|SWITCH(MARG_PORTS/NONE>=25)	,\
        defSWITCHFAULTY_PORTS_5	|SW_CRITICAL,SNMP,EMAIL	|SWITCH(FAULTY_PORTS/NONE>=5)	,\
        defSWITCHFAULTY_PORTS_6	|SW_MARGINAL,SNMP,EMAIL	|SWITCH(FAULTY_PORTS/NONE>=6)	,\
        defSWITCHFAULTY_PORTS_10	|SW_CRITICAL,SNMP,EMAIL	|SWITCH(FAULTY_PORTS/NONE>=10)	,\
        defSWITCHFAULTY_PORTS_11	|SW_MARGINAL,SNMP,EMAIL	|SWITCH(FAULTY_PORTS/NONE>=11)	,\
        defSWITCHFAULTY_PORTS_25	|SW_CRITICAL,SNMP,EMAIL	|SWITCH(FAULTY_PORTS/NONE>=25)	,\
        defCHASSISBAD_TEMP_MARG	|SW_MARGINAL,SNMP,EMAIL	|CHASSIS(BAD_TEMP/NONE>=1)	,\
        defCHASSISBAD_TEMP_CRIT	|SW_CRITICAL,SNMP,EMAIL	|CHASSIS(BAD_TEMP/NONE>=2)	,\
        defCHASSISBAD_PWR_CRIT	|SW_CRITICAL,SNMP,EMAIL	|CHASSIS(BAD_PWR/NONE>=3)	,\
        defCHASSISBAD_FAN_MARG	|SW_MARGINAL,SNMP,EMAIL	|CHASSIS(BAD_FAN/NONE>=1)	,\
        defCHASSISBAD_FAN_CRIT	|SW_CRITICAL,SNMP,EMAIL	|CHASSIS(BAD_FAN/NONE>=2)	,\
        defCHASSISDOWN_CORE_1	|SW_MARGINAL,SNMP,EMAIL	|CHASSIS(DOWN_CORE/NONE>=1)	,\
        defCHASSISDOWN_CORE_2	|SW_CRITICAL,SNMP,EMAIL	|CHASSIS(DOWN_CORE/NONE>=2)	,\
        defCHASSISWWN_DOWN_1	|SW_CRITICAL,SNMP,EMAIL	|CHASSIS(WWN_DOWN/NONE>=1)	,\
        defCHASSISHA_SYNC_0	|SW_MARGINAL,SNMP,EMAIL	|CHASSIS(HA_SYNC/NONE==0)	,\
        defCHASSISFAULTY_BLADE_1	|SW_MARGINAL,SNMP,EMAIL	|CHASSIS(FAULTY_BLADE/NONE>=1)	,\
        defALL_PORTSSFP_STATE_FAULTY	|RASLOG,SNMP,EMAIL	|ALL_PORTS(SFP_STATE/NONE==FAULTY)	,\
        defALL_PORTSSFP_STATE_IN	|RASLOG,SNMP,EMAIL	|ALL_PORTS(SFP_STATE/NONE==IN)	,\
        defALL_PORTSSFP_STATE_OUT	|RASLOG,SNMP,EMAIL	|ALL_PORTS(SFP_STATE/NONE==OUT)	,\
        defALL_PSPS_STATE_FAULTY	|RASLOG,SNMP,EMAIL	|ALL_PS(PS_STATE/NONE==FAULTY)	,\
        defALL_PSPS_STATE_ON	|RASLOG,SNMP,EMAIL	|ALL_PS(PS_STATE/NONE==ON)	,\
        defALL_PSPS_STATE_OUT	|RASLOG,SNMP,EMAIL	|ALL_PS(PS_STATE/NONE==OUT)	,\
        defALL_FANFAN_STATE_FAULTY	|RASLOG,SNMP,EMAIL	|ALL_FAN(FAN_STATE/NONE==FAULTY)	,\
        defALL_FANFAN_STATE_ON	|RASLOG,SNMP,EMAIL	|ALL_FAN(FAN_STATE/NONE==ON)	,\
        defALL_FANFAN_STATE_OUT	|RASLOG,SNMP,EMAIL	|ALL_FAN(FAN_STATE/NONE==OUT)	,\
        defALL_WWNWWN_FAULTY	|RASLOG,SNMP,EMAIL	|ALL_WWN(WWN/NONE==FAULTY)	,\
        defALL_WWNWWN_ON	|RASLOG,SNMP,EMAIL,SNMP,EMAI	|ALL_WWN(WWN/NONE==ON)	,\
        defALL_WWNWWN_OUT	|RASLOG,SNMP,EMAIL	|ALL_WWN(WWN/NONE==OUT)	,\
        defALL_SLOTSBLADE_STATE_FAULTY	|RASLOG,SNMP,EMAIL	|ALL_SLOTS(BLADE_STATE/NONE==FAULTY)	,\
        defALL_SLOTSBLADE_STATE_ON	|RASLOG,SNMP,EMAIL	|ALL_SLOTS(BLADE_STATE/NONE==ON)	,\
        defALL_SLOTSBLADE_STATE_OFF	|RASLOG,SNMP,EMAIL	|ALL_SLOTS(BLADE_STATE/NONE==OFF)	,\
        defALL_SLOTSBLADE_STATE_OUT	|RASLOG,SNMP,EMAIL	|ALL_SLOTS(BLADE_STATE/NONE==OUT)	,\
        defCHASSISETH_MGMT_PORT_STATE_DOWN	|RASLOG,SNMP,EMAIL	|CHASSIS(ETH_MGMT_PORT_STATE/NONE==DOWN)	,\
        defCHASSISETH_MGMT_PORT_STATE_UP	|RASLOG,SNMP,EMAIL	|CHASSIS(ETH_MGMT_PORT_STATE/NONE==UP)	,\
        defALL_D_PORTSCRC_1	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/MIN>1)     ,\
        defALL_D_PORTSITW_1	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/MIN>1)	,\
        defALL_D_PORTSLF_1	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/MIN>1)	,\
        defALL_D_PORTSLOSS_SYNC_1	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/MIN>1)	,\
        defALL_D_PORTSCRC_H30	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/HOUR>30)	,\
        defALL_D_PORTSITW_H30	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/HOUR>30)	,\
        defALL_D_PORTSLF_H30	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/HOUR>30)	,\
        defALL_D_PORTSLOSS_SYNC_H30	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/HOUR>30)	,\
        defALL_D_PORTSCRC_D500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/DAY>500)	,\
        defALL_D_PORTSITW_D500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/DAY>500)	,\
        defALL_D_PORTSLF_D500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/DAY>500)	,\
        defALL_D_PORTSLOSS_SYNC_D500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/DAY>500)	,\
        defALL_D_PORTSCRC_2	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/MIN>2)	    ,\
        defALL_D_PORTSITW_2	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/MIN>2)	,\
        defALL_D_PORTSLF_2	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/MIN>2)	,\
        defALL_D_PORTSLOSS_SYNC_2	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/MIN>2)	,\
        defALL_D_PORTSCRC_H60	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/HOUR>60)	,\
        defALL_D_PORTSITW_H60	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/HOUR>60)	,\
        defALL_D_PORTSLF_H60	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/HOUR>60)	,\
        defALL_D_PORTSLOSS_SYNC_H60	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/HOUR>60)	,\
        defALL_D_PORTSCRC_D1000	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/DAY>1000)	,\
        defALL_D_PORTSITW_D1000	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/DAY>1000)	,\
        defALL_D_PORTSLF_D1000	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/DAY>1000)	,\
        defALL_D_PORTSLOSS_SYNC_D1000	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/DAY>1000)	,\
        defALL_D_PORTSCRC_3	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/MIN>3)	    ,\
        defALL_D_PORTSITW_3	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/MIN>3) 	,\
        defALL_D_PORTSLF_3	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/MIN>3)	,\
        defALL_D_PORTSLOSS_SYNC_3	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/MIN>3)	,\
        defALL_D_PORTSCRC_H90	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/HOUR>90)	,\
        defALL_D_PORTSITW_H90	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/HOUR>90)	,\
        defALL_D_PORTSLF_H90	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/HOUR>90)	,\
        defALL_D_PORTSLOSS_SYNC_H90	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/HOUR>90)	,\
        defALL_D_PORTSCRC_D1500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(CRC/DAY>1500)	,\
        defALL_D_PORTSITW_D1500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(ITW/DAY>1500)	,\
        defALL_D_PORTSLF_D1500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LF/DAY>1500)	,\
        defALL_D_PORTSLOSS_SYNC_D1500	|RASLOG,SNMP,EMAIL	|ALL_D_PORTS(LOSS_SYNC/DAY>1500)	,\
        defALL_PORTS_IO_PERF_IMPACT	|RASLOG,SNMP,EMAIL,SDDQ,TOGG	|ALL_PORTS(DEV_LATENCY_IMPACT/NONE==IO_PERF_IMPACT)|RASLOG,SNMP,EMAIL,SDDQ,TOGG  ,\
        defALL_PORTS_IO_FRAME_LOSS	|RASLOG,SNMP,EMAIL,SDDQ,TOGG	|ALL_PORTS(DEV_LATENCY_IMPACT/NONE==IO_FRAME_LOSS) 	,\
        defALL_PORTS_IO_LATENCY_CLEAR	|RASLOG,SNMP,EMAIL	|ALL_PORTS(DEV_LATENCY_IMPACT/NONE==IO_LATENCY_CLEA|RASLOG,SNMP,EMAIL   ,\
        defALL_F_PORTS_IO_PERF_IMPACT	|RASLOG,SNMP,EMAIL	|ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_PERF_IMPAC|RASLOG,SNMP,EMAIL   ,\
        defALL_F_PORTS_IO_FRAME_LOSS	|RASLOG,SNMP,EMAIL	|ALL_F_PORTS(DEV_LATENCY_IMPACT/NONE==IO_FRAME_LOSS|RASLOG,SNMP,EMAIL	,\
        defALL_2K_QSFPCURRENT_39	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_2K_QSFP(CURRENT/NONE>=39)	,\
        defALL_2K_QSFPVOLTAGE_3600	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_2K_QSFP(VOLTAGE/NONE>=3600)	,\
        defALL_2K_QSFPRXP_2000	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_2K_QSFP(RXP/NONE>=2000)	,\
        defALL_2K_QSFPSFP_TEMP_85	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_2K_QSFP(SFP_TEMP/NONE>=85)	,\
        defALL_2K_QSFPVOLTAGE_2900	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_2K_QSFP(VOLTAGE/NONE<=2900)	,\
        defALL_2K_QSFPSFP_TEMP_n15	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_2K_QSFP(SFP_TEMP/NONE<=-15)	,\
        defALL_100M_16GSWL_QSFPCURRENT_10	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_100M_16GSWL_QSFP(CURRENT/NONE>=10)	,\
        defALL_100M_16GSWL_QSFPSFP_TEMP_85	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_100M_16GSWL_QSFP(SFP_TEMP/NONE>=85)	,\
        defALL_100M_16GSWL_QSFPSFP_TEMP_n5	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_100M_16GSWL_QSFP(SFP_TEMP/NONE<=-5)	,\
        defALL_100M_16GSWL_QSFPVOLTAGE_2970	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_100M_16GSWL_QSFP(VOLTAGE/NONE<=2970)	,\
        defALL_100M_16GSWL_QSFPVOLTAGE_3630	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_100M_16GSWL_QSFP(VOLTAGE/NONE>=3630)	,\
        defALL_100M_16GSWL_QSFPRXP_2187	|SFP_MARGINAL,RASLOG,SNMP,EM	|ALL_100M_16GSWL_QSFP(RXP/NONE>=2187)	,\
        defALL_BE_PORTSCRC_5M_10	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(CRC/5MIN>10)	,\
        defALL_BE_PORTSCRC_D_100	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(CRC/DAY>100)	,\
        defALL_BE_PORTSITW_5M_10	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(ITW/5MIN>10)	,\
        defALL_BE_PORTSITW_D_100	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(ITW/DAY>100)	,\
        defALL_BE_PORTSLR_5M_10	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(LR/5MIN>10)	,\
        defALL_BE_PORTSLR_D_100	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(LR/DAY>100)	,\
        defALL_BE_PORTSBAD_OS_5M_10	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(BAD_OS/5MIN>10)	,\
        defALL_BE_PORTSBAD_OS_D_100	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(BAD_OS/DAY>100)	,\
        defALL_BE_PORTSFRM_LONG_5M_10	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(FRM_LONG/5MIN>10)	,\
        defALL_BE_PORTSFRM_LONG_D_100	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(FRM_LONG/DAY>100)	,\
        defALL_BE_PORTSFRM_TRUNC_5M_10	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(FRM_TRUNC/5MIN>10)	,\
        defALL_BE_PORTSFRM_TRUNC_D_100	|RASLOG,SNMP,EMAIL,FMS	|ALL_BE_PORTS(FRM_TRUNC/DAY>100)	,\
        defALL_F_PORTSDEV_NPIV_LOGINS_PER_75	|RASLOG,SNMP,EMAIL	|ALL_F_PORTS(DEV_NPIV_LOGINS/NONE>75)	,\
        defALL_F_PORTSDEV_NPIV_LOGINS_PER_60	|RASLOG,SNMP,EMAIL	|ALL_F_PORTS(DEV_NPIV_LOGINS/NONE>60)	,\
        defALL_F_PORTSDEV_NPIV_LOGINS_PER_90	|RASLOG,SNMP,EMAIL	|ALL_F_PORTS(DEV_NPIV_LOGINS/NONE>90)	,\
        defALL_ASICS_VTAP_IOPS_250K	|RASLOG,SNMP,EMAIL	|ALL_ASICS(VTAP_IOPS/SEC>250000)	,\
        defALL_BE_PORTS_LATENCY_IMPACT	|RASLOG,SNMP,EMAIL	|ALL_BE_PORTS(BE_LATENCY_IMPACT/NONE==IO_PERF_IMPAC|RASLOG,SNMP,EMAIL	,\
        defALL_BE_PORTS_LATENCY_CLEAR	|RASLOG,SNMP,EMAIL	|ALL_BE_PORTS(BE_LATENCY_IMPACT/NONE==IO_LATENCY_CL|RASLOG,SNMP,EMAIL	,\
        | ,\
    "
    
    return(l) 
     
def cleanup_policy( policy_list):
    """
        cleanup any user added policies, rules
        remove rules from policies and delete the policy
    """
     
    capture_cmd = anturlar.fos_cmd("mapspolicy --enable dflt_moderate_policy")
     
    for p in policy_list:
        r = get_policy_rules(policy_list)
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
            
            capture_cmd = anturlar.fos_cmd("mapspolicy --delrule %s -rulename %s" % (policy_list,rn[0]))
            capture_cmd = anturlar.fos_cmd("mapsrule --delete %s " % rn[0])
           
        capture_cmd = anturlar.fos_cmd("mapspolicy --delete %s" % p)

    return(0)
  
def get_policy_rules( p = "None"):
    """
       get the rules of a policy
       
    """
 
    capture_cmd = anturlar.fos_cmd("mapspolicy --show %s " % p)
    #ras = re.compile('([_ ,\//\(-=\.|<>A-Za-z0-9]+)(?=\))')
    ras = re.compile('([A-Za-z0-9_]{1,40})\\s+\|[a-zA-Z]')
    #ras = re.compile('([monitor]+)')
    ras = ras.findall(capture_cmd)
    
    
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print(ras)
    print("@"*80)
    print("@"*80)
    print("@"*80)
    
    return(ras)

def cleanup_all_rules():
    """
    """
    capture_cmd = anturlar.fos_cmd("mapspolicy --enable dflt_moderate_policy")
    
    r = get_non_default_rules()
 
    for s in r:
    
        rn = " ".join(s.split())
        rn = rn.split(",")
        if "def" not in rn[0]:
            capture_cmd = anturlar.fos_cmd("mapsrule --delete %s -f " % rn[0])
    
    return()
    

def get_non_default_rules():
    """
    
    """
    
    capture_cmd = anturlar.fos_cmd("mapsrule --show -all")
    ras = re.compile('([a-zA-Z0-9_]{1,40})\\s+\|[a-zA-Z]')
    
    ras = ras.findall(capture_cmd)
    
    return(ras)
    
    
def frameview_status():
    """
    
    """
    
    capture_cmd = anturlar.fos_cmd("framelog --status" )
    #ras = re.compile('([_ ,\//\(-=\.|<>A-Za-z0-9]+)(?=\))')
    ras = re.compile('Status:\s+([A-Za-z]+)(?=\\r\\n)')
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
    capture_cmd = anturlar.fos_cmd('mapsdb --show all')
    
    print(capture_cmd)
    
    
    
    
    
    
    
    
def end():
    pass
    
    

























