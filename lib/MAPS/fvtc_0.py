#!/usr/bin/env python3

###############################################################################
#### Home location is
####
###############################################################################

import anturlar
import liabhar
import cofra
import re
import random
import os,sys
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

def tc_01_01_01_01():
    """
    Test Case   25.01.01.01.02
    Title:      MAPS switch View via Web Tools
    Feature     MAPS availability in Web Tools
    Confirm MAPS switch view is available when a license is not installed
    
    Note: currently not automated
    
    """
    print("at this time there this test case is not automated")
    
    return(0)
###############################################################################

def tc_01_01_01_02():
    """
    Test Case   25.01.01.01.02
    Title:      MAPS commands available with a license
    Feature:    MAPS CLI
    Confirm MAPS CLI function correctly with and without a license installed
        
    """
    ###########################################################################
    ####  todo -
    ####
    ####   2.  man page output
    ####   3.  confirm the correct commands return the right data
    ####   4.  if a license requires to answer a question about removal
    ####            (encryption)
    ####
    ####   Complete
    ####   A.  pass / fail for each step of test case
    ####       make the test_result a list of list [ step_0 pass ][step_2 fail]
    ####   B. log file of the commands and response
    ####
    ####
    ###########################################################################
    ####
    #### Steps:
    ####
    #### 1. confirm license is not installed
    ####    a. this can be flow vision, APM or FW license
    ####    b. if license is installed remove license
    #### 2. send each MAPS command
    #### 3. confirm the message for each command
    #### 4. add all license back
    ####    a. dont need to confirm Flow Vision license since the
    ####        test will fail if it is not one of the license
    #### 5. send each MAPS command
    #### 6. confirm the message for each command
    ####
    #### 7. confirm help message for each command
    #### 8. confirm man page is available for each command
    ####    a. confirm first page of man page - the rest is visual
    ####
    ####  mapsConfig 	 mapsPolicy  	mapsconfig  	mapshelp
    ####  mapsrule 	 mapsHelp   	 mapsRule    	mapsdb      
    ####  mapspolicy  	mapssam 	relayconfig *	logicalgroup *
    ####  * commands will not have a MAPS message since they are used
    ####     in other features
    #### LPMDE3mKQQrtTYYrKAWEPfFGgZfm7X3JBAXFM
    ####   beRybSSdefSzc8     beRybSSdgfSzcA
    #### start the test
    #header = "**************************************************************************"
    test_numb = "25.01.01.01.02"
    test_summary = "%s       MAPS commands available with a license" % test_numb
    header = maps_tools.format_header(test_summary)
    test_result = ""
    
    p = anturlar.Maps()
    sut_ip = p.ipaddress()
    cmds_list = maps_tools.mapscommand_list()
    cmds_list_w_usage = maps_tools.mapscommand_list("usage")
    cmds_list_w_correct = maps_tools.mapscommand_list("all")
    #### set up the log file info
    f_path = '/home/run_from_here/logs/%s_%s' % ( test_numb, sut_ip )
    
    f = liabhar.FileStuff(f_path, 'w+b')
    f.write(header)
    
    #### get the list of license and remove them from the switch
    l_list = p.getLicense()
    print("license list \n\n%s "% l_list)
    f.write("license list \n\n%s "% l_list)
    for license in l_list:
        anturlar.fos_cmd("licenseremove %s " % license)
    #### no need to confirm the Flow Vision license
    ####  just remove all the license and test
    ####   if no license for flow vision the test case will fail
    
    for cmd in cmds_list:
        console_out = anturlar.fos_cmd("%s" % cmd)
        f.write(console_out + "\r\n")
        #if "license not present" not in console_out:  #### 7.3 and earlier message
        if ("MAPS is not Licensed" not in console_out) and ("Please install the license" not in console_out):
            test_result += cmd
            test_result += ' step1'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
            f.write("\nFail Fail Fail Fail\n\n")
            
    for license in l_list:
        anturlar.fos_cmd("licenseadd %s " % license)
        
    
    for cmd in cmds_list_w_usage:
        console_out = anturlar.fos_cmd("%s" % cmd)
        f.write(console_out + "\r\n")
        if "Usage:" in console_out:
            pass
        elif "MAPS not active." in console_out:
            pass
        else:
            test_result += cmd
            test_result += ' step2'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
            f.write("\nFail Fail Fail Fail\n\n")
    
    for cmd in cmds_list_w_correct:
        console_out = anturlar.fos_cmd("%s" % cmd)
        f.write(console_out + "\r\n")
        if "root>" not in console_out:
            test_result += cmd
            test_result += ' step3'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")       
    
    
    if test_result == "":
        test_result = "PASS"
    
    print("\n\nTEST RESULTS FOR Test Case   25.01.01.01.02 ")
    print(test_result)
    tc_result = maps_tools.format_results(test_summary, test_result)
    f.write(maps_tools.format_results(test_summary, test_result))
    
    return(test_result)


def tc_01_01_03_01():
    """
    Test Case   25.01.01.03.01
    Title:      MAPS Category Management Default thresholds
    Feature:    MAPS 
    Objective:  Confirm MAPS default thresholds are set correctly
        
    """
    ###########################################################################
    ####  todo -
    ####
    ####   1.  pass / fail for each step of test case
    ####       make the test_result a list of list [ step_0 pass ][step_2 fail]
    ####   2.  ignore chassis rules on a pizza box    
    ####   3.  if bottleneckmonitor is enable FPI monitor will fail the command
    ####
    ###########################################################################
    ####
    ####  steps
    ####
    ####  1. get a list of the rules from a switch
    ####  2. get the list of rules from 7.3.0  --  maps_default_rule()
    ####  3. compare the list
    ####  4. return any diffence as a failure
    ####
    ####
    ####
    #### start the test
    test_numb = "25.01.01.03.01"
    test_summary = "%s    MAPS Catergory Management Default thresholds" % test_numb
    header = maps_tools.format_header(test_summary)
    test_result = ""
    
    p = anturlar.Maps()
    sut_ip = p.ipaddress()
    sw_rules = p.get_rules()
    
    
    #### set up the log file info
    f_path = '/home/run_from_here/logs/%s_%s' % (test_numb, sut_ip)
    
    f = liabhar.FileStuff(f_path, 'w+b')
    f.write(header)
    
    #sw_rules = str(sw_rules)
    #sw_rules = sw_rules.replace("'", "") #### remove ' from string
    #sw_rules = sw_rules.replace("[", "") #### remove open bracket
    #sw_rules = sw_rules.replace("]", "") #### remove ending bracket
    df_rules = maps_tools.maps_default_rule()
    
    sw_rules = sw_rules.split()
    
    df_rules = df_rules.split()
   
   
    count_df = len(df_rules)
    count = len(sw_rules)
    if count < count_df:
        loop_count = count
    else:
        loop_count = count_df
    i =0
    rule_differ = 0
    while i < loop_count:
        print("\n\ncomparing switch rule with default rule ")
        print("%s      %s " % (sw_rules[i], i ))
        if sw_rules[i].rstrip() not in df_rules:
            rule_differ += 1
            test_result += sw_rules[i]
            test_result += ' step1'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
        
        i += 1
        
    print("The number of rules that differ are %s " % rule_differ)
    print("The number of additional rules on the switch %s " % ( count - count_df))
    print("Total number of switch rules    %s  \r\n" % len(sw_rules))
    print("Total number of default rules   %s  \r\n" % len(df_rules))
    print(len(sw_rules))
    print(len(df_rules))
    f.write("The number of rules that differ are %s \r\n" % rule_differ)
    f.write("The number of additional rules on the switch %s \r\n" % ( count - count_df))
    f.write("Total number of switch rules    %s  \r\n" % len(sw_rules))
    f.write("Total number of default rules   %s  \r\n" % len(df_rules))


    if test_result == "":
        test_result = "PASS"
    
    print("="*80)
    print("\n\nTEST RESULTS FOR Test Case   25.01.01.03.01 ")
    print(test_result)
    f.write(maps_tools.format_results(test_summary, test_result))
    
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    i =0
    rule_differ = 0
    while i < loop_count:
        print("\n\ncomparing switch rule with default rule ")
        #print("%s      %s " % (sw_rules[i], i ))
        print(df_rules[i])
        print("default rule       %s" % i )
        if df_rules[i] not in sw_rules:
            rule_differ += 1
            test_result += df_rules[i]
            test_result += ' step1'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
        
        i += 1
        
    print("The number of rules that differ are %s " % rule_differ)
    print("The number of additional rules on the switch %s " % ( count_df - count))
    print("Total number of switch rules    %s  \r\n" % len(sw_rules))
    print("Total number of default rules   %s  \r\n" % len(df_rules))
    print(test_result)
    print(len(sw_rules))
    print(len(df_rules))
    f.write("The number of rules that differ are %s \r\n" % rule_differ)
    f.write("The number of additional rules on the switch %s \r\n" % ( count_df - count))
    f.write("Total number of switch rules    %s  \r\n" % len(sw_rules))
    f.write("Total number of default rules   %s  \r\n" % len(df_rules))

    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    print("#"*80)
    
    #print(df_rules)
    
    print("#"*80)
    print("#"*80)
    print("#"*80)
    
    #print(sw_rules)
    
    print("#"*80)
    print("#"*80)
    print("#"*80)
    
    
    return(test_result)


def tc_01_01_03_02():
    """
        Test Case   25.01.01.03.02
        Title:
        Feature:    Predfined Group Management
        Verify the predefined groups including only the elements
        defined for each group 
    """
    ###########################################################################
    ####  todo -
    ####    0.   pizza box
    ####    1.   E-Port 
    ####    2.   QSFP
    ####    3.   check all other category in the group
    ####
    ###########################################################################
    ####
    #### Steps:
    ####
    #### 1. get each port type
    ####    a. all ports        d. E_ports ?     f. other_f_ports       
    ####    b. non_e_f_ports    e. F_ports      g. D_ports
    ####    c. Target_ports     f. Host_ports ?? portFlag ??
    ####
    #### 2. get each TS / FAN / PS / WWN
    ####    a. TS  - tempshow count the state of OK
    ####    b. FAN - fanshow count the Fan
    ####    c. PS  - psshow count the Power Supply #
    ####    d. WWN - ??
    ####
    #### 3. get each SFP type
    ####    a. sfpshow - count the id (sw) and Speed that are 16 / 10
    ####                 and not 16 / 10
    ####    b. Qsfp - count ??  maybe serial number ?
    ####
    #### 4. get each Blade type
    ####    a. slotshow - count the slots and blades
    ####
    #### 5. Compare to logicalgroup --show output
    ####
    #### 6. repeat for each FID
    ####
    ###########################################################################
    ####
    #### start the test
    ####
    #### get the info from the switch
    ####  Step 1
    ####
    pgm = anturlar.Maps()
    sut_ip = pgm.ipaddress()
    port_list = pgm.all_ports()
    port_list_no_ve = pgm.all_ports_fc_only()
    e_ports = pgm.e_ports()
    f_ports = pgm.f_ports()
    sim_ports = pgm.sim_ports()
    d_ports = pgm.d_ports()
    #other_f_ports = pgm.f_ports_other()
    #non_ef_port = pgm.ports - e_ports - f_ports
    #host_ports = pgm.host_ports()
    #target_ports = pgm.target_ports()
    fans_count = pgm.fan_count()
    blade_count = pgm.blades()
    temp_sensor = pgm.temp_sensors()
    temp_sensor_absent = pgm.temp_sensors("absent")
    fan_count_sensor_f = pgm.sensor_t_f_ps("f")
    fan_count_sensor_t = pgm.sensor_t_f_ps("t")
    fan_count_sensor_ps = pgm.sensor_t_f_ps("ps")
    sfp_list = pgm.sfp_info()
    sfp_summary = pgm.sfp_info("summary")
    total_f_ports = f_ports + sim_ports
    
    
    
    
    ###########################################################################
    #### get the data from the switch
    ####
    ####    
    ####   ALL_F_PORTS         ALL_OTHER_F_PORTS       ALL_HOST_PORTS    
    ####   ALL_TARGET_PORTS    ALL_TS                  ALL_FAN        
    ####   ALL_PS              ALL_WWN                 ALL_SFP        
    ####   ALL_10GSWL_SFP *     ALL_10GLWL_SFP *        ALL_16GSWL_SFP * 
    ####   ALL_16GLWL_SFP  *    ALL_QSFP                ALL_OTHER_SFP  *
    ####   ALL_SLOTS           ALL_SW_BLADES           ALL_CORE_BLADES
    ####   ALL_FLASH           ALL_CIRCUITS            SWITCH *     
    ####  CHASSIS *            ALL_D_PORTS
    
    if "not a director" in blade_count:
        t1 = -1
    else:
        t1 = len(blade_count)
    
    
    t_fports = (pgm.logicalgroup_count("ALL_PORTS"))
    print("ALL PORTS IS  %s  " % t_fports)
    
    t_ofports = int(pgm.logicalgroup_count("ALL_OTHER_F_PORTS"))
    t_hostports = int(pgm.logicalgroup_count("ALL_HOST_PORTS"))
    t_targetports = int(pgm.logicalgroup_count("ALL_TARGET_PORTS"))
    t_ts = int(pgm.logicalgroup_count("ALL_TS"))
    t_fan = int(pgm.logicalgroup_count("ALL_FAN"))
    t_ps  = int(pgm.logicalgroup_count("ALL_PS"))
    t_wwn = int(pgm.logicalgroup_count("ALL_WWN"))
    t_sfp = int(pgm.logicalgroup_count("ALL_SFP"))
    
    t_qsfp = int(pgm.logicalgroup_count("ALL_QSFP"))
    t_slots = int(pgm.logicalgroup_count("ALL_SLOTS"))
    t_swblade = int(pgm.logicalgroup_count("ALL_SW_BLADES"))
    t_coreblade = int(pgm.logicalgroup_count("ALL_CORE_BLADES"))
    t_flash = int(pgm.logicalgroup_count("ALL_FLASH"))
    t_circuits = int(pgm.logicalgroup_count("ALL_CIRCUITS"))
    
    t_dports = int(pgm.logicalgroup_count("ALL_D_PORTS"))
    
    t_error = int(pgm.logicalgroup_count("notinthelist"))
    
    ###########################################################################
    
    print("\n\nINFO FROM the SWITCH ITSELF")
    print("="*80)
    print("\nport list is            : %s" % len(port_list))
    print("port list no ve is       : %s " % len(port_list_no_ve))
    print("F ports   is             : %s" % len(total_f_ports))
    
    print("E ports   is             : %s" % len(e_ports))
    
    print("temp sensors is          : %s" % len(temp_sensor))
    print("temp sensors missing     : %s" % len(temp_sensor_absent))
    print("TEMP from sensor cmd     : %s" % len(fan_count_sensor_t))
    print("PS from sensor cmd       : %s" % len(fan_count_sensor_ps))
    
    print("fans      is             : %s" % len(fans_count))
   
    print("Fan from sensor cmd      : %s" % len(fan_count_sensor_f))
    
    print("SFP summary  less SIM    : %s" % sfp_summary)
    print("SFP list of speed  -     : %s" % sfp_list)

    #print("blade_count is           : %s" % len(blade_count))
    print("blade_count is           : %s" % t1)
    print("D ports   is             : %s" % len(d_ports))
    
    #print("Need the fan sensor output : %s " % port_list)
    print("="*80)
    print("INFO FROM LOGICAL GROUP COMMAND")
    print("="*80)
    print("\nALL Ports count          :  %s " % t_fports)
    print("ALL other F port count    :  %s " % t_ofports)
    print("ALL host port count       :  %s " % t_hostports)
    print("ALL target port count     :  %s " % t_targetports)
    print("ALL temp sensors count    :  %s " % t_ts)
    print("ALL POWER SUPPLY count    :  %s " % t_ps)
    print("ALL FAN count             :  %s " % t_fan)
    print("All WWN count             :  %s " % t_wwn)
    print("ALL SFP count             :  %s " % t_sfp)
    print("ALL QSFP count            :  %s " % t_qsfp)
    print("ALL slot count            :  %s " % t_slots)
    print("ALL blade count           :  %s " % t_swblade)
    print("ALL core blade count      :  %s " % t_coreblade)
    print("ALL flash count           :  %s " % t_flash)
    print("ALL circuit count         :  %s " % t_circuits)
    print("ALL D Port count          :  %s " % t_dports)
    print("="*80)
    
    
     
    test_result = ""
    if t1 != t_swblade:
        test_result += "ALL_SW_BLADES"
        test_result += ' step1'
        test_result += ' Fail\n'
        
    if int(t_fports) == len(port_list_no_ve):
        test_result += "ALL PORT LIST"
        test_result += ' step 1'
        test_result += ' Fail\n'
    
    
    if test_result == "":
        test_result = "PASS"
    
    print("debug all port list ")
    print(t_fports)
    print(len(port_list_no_ve))
    
    print("="*80)
    print("\n\nTEST RESULTS FOR Test Case   25.01.01.03.02 ")
    print(test_result)
    return(test_result)


def tc_01_01_05_01():
    """
        Test Case   25.01.01.05.01
        Title:
        Feature:    Environmental Events and alarms
        Objective:  Verify the Environmental events and alarms in Switch
                    Resource Category of MAPS
                    
    """
    ###########################################################################
    ####  todo -
    ####    1.   DNS configure
    ####    2.   SNMP configure   
    ####    3.   need to confirm the CPU message is only returned after two
    ####         polling cycles 
    ###########################################################################
    ####
    #### Steps:
    ####    1. create a policy for the rules that are created in the next step
    ####    2. create rules for flash usage, memory usage and CPU usage
    ####    3. enable the policy
    ####    4. confirm or set the actions in mapsconfig (raslog, email, snmp)
    ####    5. confirm DNS is configured and snmp is configured
    ####    6. get the current usage of the flash, cpu, memory, temp
    ####        - flash  confirm with df /
    ####        - cpu confirm with cat /proc/stat look for cpu grab
    ####          the idle time for calculation
    ####        - memory usage vmstat,  free,  top  cat /proc/meminfo
    ####        - tempshow     pgm.sensor_t_f_ps("t") 
    ####    7. confirm RAS log message
    ####    8. confirm MAPS entry
    ####
    ####    9. cleanup switch of the rules and policy
    ####
    ###########################################################################
    #### start the test
    ####
    ####  mapsrule --create sqa_switch_res_flash_usage_down  -group chassis
    ####  -monitor flash_usage -value 50 -action email,raslog,snmp,sw_marginal
    ####    -op ge -policy environ_test
    ####  mapsrule --create sqa_switch_res_cpu_usage_down -group chassis
    ####   -monitor cpu -value 100 -action email,raslog,snmp
    ####    -op le -policy policy_test_1
    ####
    ####  mapspolicy --create environ_test
    ####
    
    en = anturlar.Maps()
    #cofra.clear_stats()
    #liabhar.count_down(30)
    #### create a policy and rules
    ####
    flash_rule_name = "sqa_sw_res_flash_usage_down"
    cpu_rule_name   = "sqa_sw_res_cpu_usage_down"
    mem_rule_name   = "sqa_sw_res_memory_usage"
    temp_rule_out   = "sqa_sw_temp_out"
    temp_rule_in    = "sqa_sw_temp_in"
    
    
    cmd_flash    = "mapsrule --create "+ flash_rule_name +" -group chassis\
              -monitor flash_usage -value 30 -action email,raslog,snmp,sw_marginal\
              -op ge -policy environ_test" 
    
    cmd_cpu      = "mapsrule --create "+ cpu_rule_name +" -group chassis \
               -monitor cpu -value 100 -action email,raslog,snmp\
               -op le -policy environ_test"
    
    cmd_mem      = "mapsrule --create "+ mem_rule_name +"  -group chassis \
              -monitor memory_usage -value 100 -action email,raslog,snmp  \
              -op le -policy environ_test"
    
    cmd_temp     = "mapsrule --create "+ temp_rule_out +" -group ALL_ts \
               -monitor temp -timebase none -value out_of_range \
               -action snmp,raslog,email -op eq -policy environ_test"
    
    cmd_temp_in  = "mapsrule --create " + temp_rule_in + " -group ALL_ts \
                  -monitor temp -timebase none -value IN_range \
                  -action snmp,raslog,email -op eq -policy environ_test"
    
    
    cmd_flash_del   = "mapsrule --delete " + flash_rule_name  
    cmd_cpu_del     = "mapsrule --delete " + cpu_rule_name  
    cmd_mem_del     = "mapsrule --delete " + mem_rule_name 
    cmd_temp_del    = "mapsrule --delete " + temp_rule_out 
    cmd_temp_in_del = "mapsrule --delete " + temp_rule_in 
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create environ_test")
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    anturlar.fos_cmd(cmd_flash)
    anturlar.fos_cmd(cmd_cpu)
    anturlar.fos_cmd(cmd_mem)
    anturlar.fos_cmd(cmd_temp)
    anturlar.fos_cmd(cmd_temp_in)
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL")
    anturlar.fos_cmd("mapspolicy --enable environ_test")
    ####
    #### do some steps here
    ####
    print("\n\nwaiting for maps actions to be triggered. . .")
    #liabhar.JustSleep(600)
     
    liabhar.count_down(650)
    #back2prompt = anturlar.fos_cmd("\n",9)
    ####  see if there is a ras log message for each rule
    mem_ras_message   = en.ras_message_search(mem_rule_name)
    
    print("debug ")
    print(mem_ras_message)
    print("debug")
    
    flash_ras_message = en.ras_message_search(flash_rule_name)
    
    temp_ras_message  = en.ras_message_search(temp_rule_in)
    
    cpu_ras_message   = en.ras_message_search(cpu_rule_name)

    ####  see if there is a mapsdb entry for each r+= 1ule
    #mem_mapsdb_confirm = en.db_search(mem_rule_name)
    #mem_mapsdb_confirm = mem_mapsdb_confirm.replace("|","")
    #mem_confirm_final = mem_mapsdb_confirm.split(" ")
    mem_confirm       = en.db_search(mem_rule_name)
    
    flash_confirm     = en.db_search(flash_rule_name)
    
    cpu_confirm       = en.db_search(cpu_rule_name)
    
    temp_confirm      = en.db_search(temp_rule_in)
    
    #### get the raw data from the switch
    ####
    #### example from df command for Flash usage
    ####Filesystem           1k-blocks      Used Available Use% Mounted on
    #/dev/root               495016    210188    259276  45% /
    #/dev/hda1               494984    210716    258720  45% /mnt
    ####
    ####  no calculation needanturlar.fos_cmd(cmd_temp_in_del)ed since the use% is the correct number
    ####
    #back2prompt = anturlar.fos_cmd("\n",9)
    
    flash_df_command = anturlar.fos_cmd("df",9)
    if flash_df_command == None:
        print("did not find the flash df command output")
        exit()
        
    ras = re.compile('[\d]+(?=%)')
    flash_raw = ras.search(flash_df_command)
    
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)

    print(flash_raw)
    try:
        flash_usage = flash_raw.group()   
    except AttributeError:
        print("did not find df output")
        exit()
    liabhar.count_down(30)
    
    ### equation to confirm mem usage
    #### using the command free returns these values
    ####          total       used       free     shared    buffers     cached
    # Mem:       1024096     672768     351328          0      40884     379300
    # -/+ buffers/cache:     252584     771512
    # Swap:            0          0          0
    ####
    ####  use the calculation (total - free - buffers - cached)/ total
    ####    ( 1024096 - 351328 - 40884 - 379300 ) / 1024096 = = 25%
    ####
    mem_usage = en.mem_usage()
    
    if mem_usage == None:
        print("did not find the mem usage ")
        exit()
        
    liabhar.count_down(30)
    #### equation for cpu usage
    #### cat /proc/stat - in the line containing cpu, the 4th number 
    ####   is the idle time.  The CPU usage is calculated as
    ####  (100-(idle value at T1 - idle value at T2)*100/(sum of all number
    ####           at T1 - sum of all numbers at T2))
    ####
    ####    cat /proc/stat
    # cpu  1296327 9539 459156 22597828 163062 9894 61210 0
    # cpu0 1296327 9539 459156 22597828 163062 9894 61210 0
    # intr 44837986softirq 65577794 148267 24596931 0 38492796 0 2339800
    ####
    cpu_calc    = en.cpu_usage()
    
    if cpu_calc == None:
        print("CPU usage was not found")
        exit()
    temp_status = en.temp_status()
    
    if temp_status == None:
        print("Temp Status was not found")
        exit()
        
    
    
    
    ###########################################################################
    ###########################################################################
    ####  clean up
    ####
    policy_list = en.get_policies("s")
    policy_user_list = en.get_nondflt_policies()
    liabhar.count_down(5)
    
    maps_tools.cleanup_policy(policy_user_list)
    policy_user_list_final = en.get_policies("s")

    anturlar.fos_cmd(cmd_flash_del)
    anturlar.fos_cmd(cmd_cpu_del)
    anturlar.fos_cmd(cmd_mem_del)
    anturlar.fos_cmd(cmd_temp_del)
    anturlar.fos_cmd(cmd_temp_in_del)
     
    anturlar.fos_cmd("mapspolicy --enable dflt_moderate_policy")
    anturlar.fos_cmd("mapspolicy --delete environ_test")
     
    print("\n\n\n\n\n")
    print("="*80)
    print("="*80)
    print("Policy list")
    print(policy_list)
    print("\n")
    print("="*80)
    print("="*80)
    print("Policy list - User list")
    print(policy_user_list)
    print("\n\n\n\n\n")
    print("memory ras message is   :  %s  " % mem_ras_message)
    print("flash  ras message is   :  %s  " % flash_ras_message)
    print("cpu    ras message is   :  %s  " % cpu_ras_message)
    print("temp   ras message is   :  %s  " % temp_ras_message)
    print("="*80)
    print("memory db message is      :  %s  " % mem_confirm)
    print("flash  db message is      :  %s  " % flash_confirm)
    print("cpu    db message is      :  %s  " % cpu_confirm)
    print("temp   db message is      :  %s  " % temp_confirm)
    print("="*80)
    print("="*80)

    print("SWITCH VALUES")
    print("calculated memory usage           :  %s  " % mem_usage )
    print("calculated flash usage            :  %s  " % flash_usage)
    print("calculated switch CPU             :  %s  " % cpu_calc)
    print("Temp Sensor info high-low-avg     :  %s  " % temp_status)
    
    
    ###################################################################################################################
    ####
    ####  check for all messages are present
    ####   if not then the test case fails
    ####
    ###################################################################################################################
    if "no match" in mem_ras_message:
        print("TEST CASE FAILED")
        exit()
        return(False)
    
    
    return(True)


def tc_01_01_05_02():
    """
        Test Case   25.01.01.05_02
        Title:      MAPS Port Health
        Feature:    MAPS
        Objective:  Verify Port Related events / alarms
            at this time it is configuration for testing only. 
        
    """
    ###########################################################################
    ####  todo -
    ####    1.   finisar API
    ####    2.   DNS configure
    ####    3.   SNMP configure 
    ####
    ####
    ###########################################################################
    ####
    #### Steps:
    ####    1. Setup the rules and policy for this test
    ####
    ####    Link loss                      
    ####    Sync loss                      
    ####    Signal loss                    Port state change
    ####    Invalid Protocol               Link Reset
    ####    Invalid Word                   
    ####    CRC                            C3TX_TO
    ####
    ####    2. get the current values - or clear to zero and get them
    ####    3. trigger a rule - have the user trigger the rule 
    ####    4. confirm a ras log message
    ####    5. confirm an entry in MPAS
    ####    6. clean up the switch
    ###########################################################################
    #### start testing
    ####
    #### rule names and maps commands and maps policy
    ####
    
    port_health_policy = "port_health_policy"
    
    
    link_loss_rule         = "sqa_all_ports_LF_N_1"
    sync_loss_rule         = "sqa_all_ports_loss_sync_N_1"
    loss_signal_rule       = "sqa_all_ports_loss_sig_N_1"
    port_state_change_rule = "sqa_all_ports_state_change_N_0"
    invalid_proto_rule     = "sqa_all_ports_PE_N_1"
    link_reset_rule        = "sqa_all_ports_LR_N_1"
    invalid_word_rule      = "sqa_all_ports_ITW_N_1"
    crc_rule               = "sqa_all_ports_CRC_N_1"
    c3to_rule              = "sqa_all_ports_C3_TO_N_1"
    
    link_loss_cmd         = "mapsrule --create sqa_all_ports_LF_N_1 \
                            -group ALL_ports -monitor LF -timebase hour \
                            -value 2 -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    sync_loss_cmd         = "mapsrule --create sqa_all_ports_loss_sync_N_1 \
                            -group ALL_ports -monitor loss_sync -timebase min \
                            -value 2 -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    loss_signal_cmd       = "mapsrule --create sqa_all_ports_loss_sig_N_1 \
                            -group ALL_ports -monitor loss_signal \
                            -timebase hour -value 0 -action email,raslog,snmp \
                            -op g -policy port_health_policy"
    
    port_state_change_cmd = "mapsrule --create sqa_all_ports_state_change_N_0 \
                            -group ALL_ports -monitor State_CHG -timebase min \
                            -value 1 -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    invalid_proto_cmd     = "mapsrule --create sqa_all_ports_PE_N_1 \
                            -group ALL_ports -monitor PE -timebase hour \
                            -value 5 -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    lr_cmd                = "mapsrule --create sqa_all_ports_LR_N_1 \
                            -group ALL_ports -monitor LR -timebase min \
                            -value 0 -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    invalid_word_cmd      = "mapsrule --create sqa_all_ports_ITW_N_1 \
                            -group ALL_ports \
                            -monitor itw -timebase hour -value 5 \
                            -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    crc_cmd               = "mapsrule --create sqa_all_ports_CRC_N_1 \
                            -group ALL_ports \
                            -monitor crc -timebase min -value 6 \
                            -action email,raslog,snmp -op g -policy port_health_policy"
    
    c3tx_to_cmd           = "mapsrule --create sqa_all_ports_C3_TO_N_1 \
                            -group ALL_ports -monitor C3TXTO -timebase hour \
                            -value 1 -action email,raslog,snmp -op g \
                            -policy port_health_policy"
    
    
 
    ####  list of commands
    cmd_list = [link_loss_cmd, sync_loss_cmd, loss_signal_cmd,\
                port_state_change_cmd,\
                invalid_proto_cmd, lr_cmd, invalid_word_cmd,\
                crc_cmd, c3tx_to_cmd ]
    
    
    en = anturlar.Maps()
    cofra.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % port_health_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % port_health_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL")
    
    anturlar.fos_cmd("porterrshow")
    
    print("\n\n\n\n")
    print("***   THIS TEST CASE AUTOMATION IS CONFIGURATION ONLY   ***")
    print("\n\n")
    print("check for maps messages") 
    print("")
    
    print("use the port_health_policy = db command to poke for one test, \
           \nuse the finisar for confirmation")
    
    
    return()
###############################################################################

def tc_01_01_05_03():
    """
        Test Case   25.01.01.05.03
        Title:
        Feature:    FCIP 
        Objective:  verify the FCIP traffic events and alarms
        
    """
    ###########################################################################
    ####  todo -
    ####    1.   ??
    ####
    ###########################################################################
    ####
    #### Steps:
    ####    1. check if switch is fcip switch
    ####    2. confirm circuit and tunnel
    ####    3. 
    ####
    ###########################################################################
    #### start testing
    ####
    
    




    
    fcip_health_policy = "fcip_health_policy"
    
    
    circuit_change_rule  = "sqa_fcip_cir_STATE"
    circuit_util_rule    = "sqa_fcip_cir_UTIL"
    packet_loss_rule     = "sqa_fcip_cir_pktloss"
    
    qos_tunnel_rule      = " "
    
    rtt_rule             = "sqa_fcip_rtt"
    jitter_rule          = "sqa_fcip_jitter"
    
    state_change_rule    = "sqa_fcip_statechange"
    utilization_rule     = "sqa_fcip_utilization"
    packets_rule         = "sqa_fcip_packet_loss"
    slow_starts          = " "
    
    
    circuit_change_cmd    = "mapsrule --create sqa_fcip_cir_STATE \
                            -group ALL_CIRCUITS -monitor cir_state \
                            -timebase hour -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy fcip_health_policy"
    
    circuit_util_cmd     = "mapsrule --create sqa_fcip_cir_UTIL \
                            -group ALL_CIRCUITS -monitor cir_util \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy fcip_health_policy "
    
    packet_loss_cmd      = "mapsrule --create sqa_fcip_cir_pktloss \
                            -group ALL_CIRCUITS -monitor cir_pktloss \
                            -timebase hour -value 0 -action email,raslog,snmp \
                            -op g -policy fcip_health_policy "
    
    qos_tunnel_cmd      = " "
    
    ####  remove -timebase hour for sqa_fcip_rtt and jitter
    rtt_cmd             = "mapsrule --create sqa_fcip_rtt \
                            -group ALL_CIRCUITS -monitor rtt \
                            -value 0 -action email,raslog,snmp \
                            -op g -policy fcip_health_policy  "
    
    jitter_cmd          = "mapsrule --create sqa_fcip_jitter \
                            -group ALL_CIRCUITS -monitor jitter \
                            -value 0 -action email,raslog,snmp \
                            -op g -policy fcip_health_policy  "
    
    state_change_cmd    = "mapsrule --create sqa_fcip_statechange \
                            -group ALL_CIRCUITS -monitor state_chg \
                            -timebase hour -value 0 -action email,raslog,snmp \
                            -op g -policy fcip_health_policy "
    
    utilization_cmd     = "mapsrule --create sqa_fcip_utilization \
                            -group ALL_CIRCUITS -monitor util \
                            -timebase hour -value 0 -action email,raslog,snmp \
                            -op g -policy fcip_health_policy"
    
    packets_cmd         = "mapsrule --create sqa_fcip_packet_loss \
                            -group ALL_CIRCUITS -monitor pktloss \
                            -timebase hour -value 0 -action email,raslog,snmp \
                            -op g -policy fcip_health_policy"
    
    slow_starts_cmd     = " "
    
    ####  list of commands
    cmd_list = [ circuit_change_cmd, circuit_util_cmd, packet_loss_cmd, \
                 rtt_cmd, jitter_cmd ]
    
    ####
    en = anturlar.Maps()
    cofra.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % fcip_health_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % fcip_health_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")    
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL")
    
    anturlar.fos_cmd("portshow fciptunnel ")
    anturlar.fos_cmd("portshow fcipcircuit ")
    
    print("\n\n\n")
    print("***   THIS TEST CASE AUTOMATION IS CONFIGURATION ONLY   ***")
    print("\n\n")
    
    print("use Anue Systems Network test equipment to Trigger events")
    print("\n\n")
    
    
    
    
    
    return()
###############################################################################

def tc_01_01_05_04():
    """
        Test Case   25.01.01.05.04
        Title:      Traffic Performance Events
        Feature:    MAPS
        Objective:  Verify the Traffic performance events and alarms
        
    """
    ###########################################################################
    ####  todo -
    ####    1.   ??
    ####
    ###########################################################################
    ####
    #### Steps:
    ####    1. set up the rules and policies for the test
    ####    2. 
    ####
    ###########################################################################
    #### start testing
    ####

    perf_policy = "traffic_performance_policy"
    
    
    sqa_tf_rx_e_rule   = "sqa_trafperf_port_RX_E"
    sqa_tf_rx_f_rule   = "sqa_trafperf_port_RX_F"
     
    sqa_tf_tx_e_rule   = "sqa_trafperf_port_TX_E"
    sqa_tf_tx_f_rule   = "sqa_trafperf_port_TX_F"
    sqa_tf_util_e_rule = "sqa_trafperf_util_E"
    sqa_tf_util_f_rule = "sqa_trafperf_util_F"
    sqa_tf_rx_none     = "sqa_trafperf_rx_none"
    sqa_tf_tx_none     = "sqa_trafperf_tx_none"
    
    
    
    rx_e_cmd   = "mapsrule --create sqa_trafperf_port_RX_E -group ALL_E_ports \
                 -monitor RX  -timebase min -value 0 -action email,raslog,snmp\
                 -op g -policy traffic_performance_policy"

    rx_f_cmd   = "mapsrule --create sqa_trafperf_port_RX_F -group ALL_F_ports \
                 -monitor RX  -timebase min -value 0 -action email,raslog,snmp\
                 -op g -policy traffic_performance_policy"
    
    tx_e_cmd    = "mapsrule --create sqa_trafperf_port_TX_E -group ALL_E_ports\
                  -monitor TX -timebase min -value 0 -action email,raslog,snmp\
                  -op g -policy traffic_performance_policy"
    
    tx_f_cmd    = "mapsrule --create sqa_trafperf_port_TX_F -group ALL_F_ports\
                  -monitor TX -timebase min -value 0 -action email,raslog,snmp\
                  -op g -policy traffic_performance_policy"
    
    util_e_cmd  = "mapsrule --create sqa_trafperf_port_UTIL_E \
                  -group ALL_E_ports\
                  -monitor UTIL -timebase hour -value 0 \
                  -action email,raslog,snmp\
                  -op g -policy traffic_performance_policy"
    
    util_f_cmd  =  "mapsrule --create sqa_trafperf_port_UTIL_F \
                   -group ALL_F_ports\
                   -monitor UTIL -timebase hour -value 0 \
                   -action email,raslog,snmp\
                   -op g -policy traffic_performance_policy"
    
    rx_none_cmd =  "mapsrule --create sqa_trafperf_port_RX_Non \
                   -group NON_E_F_ports -monitor RX  -timebase min -value 0 \
                   -action email,raslog,snmp -op g \
                   -policy traffic_performance_policy"
    
    tx_none_cmd = "mapsrule --create sqa_trafperf_port_TX_Non \
                  -group NON_E_F_ports -monitor TX  -timebase min -value 0 \
                  -action email,raslog,snmp -op g \
                  -policy traffic_performance_policy"
    
    
    ####  list of commands
    cmd_list = [rx_e_cmd, rx_f_cmd, tx_e_cmd, tx_f_cmd, util_e_cmd, \
                util_f_cmd, rx_none_cmd, tx_none_cmd ]
    
    
    en = anturlar.Maps()
    cofra.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % perf_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % perf_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL")
    
    anturlar.fos_cmd("mapsdb --show")
    
    
    print("\n\n\n\n")
    print("***   THIS TEST CASE AUTOMATION IS CONFIGURATION ONLY   ***")
    print("\n\n")
    print("check for maps messages") 
    print("")
    
    print("Run Traffic and Confirm port usage \n\n\n")
    
    
    return()
################################################################################

def tc_01_01_05_05():
    """
        Test Case   25.01.01.05.05
        Title:      Fabric State Change
        Feature:    MAPS
        Objective:  Verify the Fabric State Change events and alarms
         
    """
    ###########################################################################
    ####  todo -
    ####    1.   create each event to trigger the rule
    ####    2.   FLOGI
    ####    3.   director test
    ####    4.   add different time base for the rules( hour and days)
    ####    5.   eport down section need to check for switch is enabled -
    ####           if no fail that part of the test
    #### 
    ###########################################################################
    ####
    #### Steps:
    ####    1. configure the rules and policy for Fabric State Change
    ####    2.
    ####    3. Create the events that will trigger each rule
    ####        - e_port_down    - bounce an eport on the switch
    ####        - fabric_rec     - bounce an adjacent switch
    ####                           switchdisable ; sleep ; switchenable
    ####        - domain_id      - same domain id and principle switch has
    ####                           to change another id - must be 2 times
    ####                           in less than 1 minute - use local switch
    ####              a. get the list of switch id in the fabric - fabricshow
    ####              b. disable the switch
    ####              c. use configure to change the id to the same as another
    ####                 switch in the fabric
    ####              d. enable the switch -  the switch ID will change
    ####              e. repeat since it must be done 2 times in a minute
    ####                 
    ####        - fab_segment    - add a switch to the fabric with an
    ####                           incorrect fid from the SUT
    ####        - zone_change    - change to a zone and save the zone
    ####                           note that the rule is set to trigger hour
    ####                           since the rule is 3 zone changes per day
    ####        - fabric_login   - FLOGI  
    ####
    ###########################################################################
    #### start testing
    ####

    fabric_state_policy = "fabric_state_policy"
    
    e_p_down_rule         = "sqa_fabric_state_EPORT_Down"
    fab_recon_rule        = "sqa_fabric_Fab_config"
    domian_change_rule    = "sqa_fabric_Domain_change"
    fab_segment_rule      = "sqa_fabric_segment"
    zone_change_rule      = "sqa_fabric_zone_chg"
    fabric_login_rule     = "sqa_fabric_FLOGI"
    
    e_port_down_cmd      = "mapsrule --create sqa_fabric_state_EPORT_Down \
                           -group switch -monitor eport_down -timebase min \
                           -value 0 -action email,raslog,snmp -op g \
                           -policy fabric_state_policy"
    fabric_reconfig_cmd  = "mapsrule --create sqa_fabric_Fab_config  \
                           -group switch -monitor FAB_CFG -timebase min \
                           -value 0 -action email,raslog,snmp -op g \
                           -policy fabric_state_policy"
    domain_id_change_cmd = "mapsrule --create sqa_fabric_Domain_change  \
                           -group switch -monitor DID_CHG -timebase min \
                           -value 0 -action email,raslog,snmp -op g \
                           -policy fabric_state_policy"
    fabric_segment_cmd   = "mapsrule --create sqa_fabric_segment  \
                           -group switch -monitor fab_seg -timebase min \
                           -value 0 -action email,raslog,snmp -op g \
                           -policy fabric_state_policy"
    zone_change_cmd      = "mapsrule --create sqa_fabric_zone_chg  \
                           -group switch -monitor zone_chg -timebase min \
                           -value 0 -action email,raslog,snmp -op g \
                           -policy fabric_state_policy"
    fabric_login_cmd     = "mapsrule --create sqa_fabric_FLOGI  -group switch \
                           -monitor FLOGI -timebase min -value 0 \
                           -action email,raslog,snmp -op g \
                           -policy fabric_state_policy"

    ###########################################################################
    ####  list of commands
    ###########################################################################
    cmd_list = [e_port_down_cmd, fabric_reconfig_cmd, domain_id_change_cmd,\
                fabric_segment_cmd, zone_change_cmd, fabric_login_cmd]
    
    #### create the object and clear stats
    en = anturlar.Maps()
    cofra.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ###########################################################################
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % fabric_state_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % fabric_state_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL")
    
    anturlar.fos_cmd("mapsdb --show")
    
    ###########################################################################
    ####  E-Port down event
    ####
    ###########################################################################
    eports = en.e_ports()
    print("\n\nMY E-PORTS  %s " % eports )
    if eports == []:
        print("No E-Ports found")
        ####  check if switch is enabled or fail this part of the test ?
        cmdrtn = anturlar.fos_cmd("switchenable")
        liabhar.JustSleep(30)
        cmdrtn = anturlar.fos_cmd("switchshow")
    else:
        print("use the first port found for now %s  " % eports[0][0])
    
    ###########################################################################
    #### for pizza box
    ####
    
        x = 0
        while x <= 1:
            for p in eports:
                x += 1
                cmdrtn = anturlar.fos_cmd("portdisable %s/%s" % (p[0],p[1]))
                cmdrtn = anturlar.fos_cmd("sleep 3")
                cmdrtn = anturlar.fos_cmd("portenable %s/%s " % (p[0],p[1]))
                cmdrtn = anturlar.fos_cmd("sleep 3")
                
    ############################################################################
    #### fabric config event
    ####  disable all the ports on the target switch
    ####  when the ports are enabled the fabric will reconfigure
    ############################################################################
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portdisable %s/%s " % (p[0],p[1]))
        cmdrtn = anturlar.fos_cmd("sleep 10")
        
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portenable %s/%s " % (p[0],p[1]))
    cmdrtn = anturlar.fos_cmd("sleep 60")
    
    
    
    ############################################################################
    ####  DID conflict
    ####
    ############################################################################

    fab_stuff = anturlar.FabricInfo(en.currentFID())
    fabmems = fab_stuff.fabric_members()
    myzone_info = fab_stuff.zone_info()
    myzone = myzone_info[0][1]
    my_swid = en.switch_id()
    print("\n\n")
    print("Fabric members and my switch ID")
    print(fabmems,  my_swid )
    
    ####  change the switch ID to one on the list in fabmems
    if my_swid == int(fabmems[0]):
        new_swid = fabmems[0]
    else:
        new_swid = fabmems[1]
    
    #usrn = "[\r\n]+[:_\w]+(root>)"
    #usrn = usrn.encode()
    ctrl_c = "\x03"  ### ctrl-c  
    ctrl_d = "\x04"  ### ctrl-d 
    reg_ex_list = [ b"(no])", b"(\d+])", b"(on])", b"root>", b"affected"]
    reg_ex_list = [ b"(no])", b"(\d+])", b"(on])", b"(off])", b":root> " ]
    cmdrtn = anturlar.fos_cmd("")
    cmdrtn = anturlar.fos_cmd("switchdisable")
    cmdrtn = anturlar.fos_cmd_regex("configure", reg_ex_list)
    cmdrtn = anturlar.fos_cmd_regex("y", reg_ex_list)
    cmdrtn = anturlar.fos_cmd_regex(new_swid, reg_ex_list)
    while 'root' not in cmdrtn:
        cmdrtn = anturlar.fos_cmd_regex("", reg_ex_list)
     
    
    #cmdrtn = anturlar.fos_cmd_regex('\x04', reg_ex_list,9) ### send ctrl-c  \003 or ctrl-d \004
    #### sending the ctrl-d command i believe is seen as EOF and does not continue
    #### with the fos_cmd_regex command
     
  
    cmdrtn = anturlar.fos_cmd("version",9)
    cmdrtn = anturlar.fos_cmd("switchenable",9)
    cmdrtn = anturlar.fos_cmd("sleep 30",9)
    cmdrtn = anturlar.fos_cmd("switchshow")
    ############################################################################
    #### fabric_segment
    ####   attach a switch to the fabric that has a different FID
    ####   - find the fabric member and confirm one is attached to the switch
    ####   - confirm there are at least 2 fid on the attached switch
    ####   - move one of the eports to another fid
    ####   - enable the port
    ####   - move the port back to original fid
    ############################################################################
    #moveport = eports[0][0]
    moveport = eports[0]
    ls_list = en.ls()
    fid_to_move_port = 88
    fid_now = en.currentFID()
    
    #reg_ex_list    = [ b".+no]", b".+\d+]", b".+n]?:", b"usrn" ]
    
    
    anturlar.fos_cmd_regex("lscfg --config %s -port %s " %(fid_to_move_port, moveport) , reg_ex_list)
    cmdrtn = anturlar.fos_cmd_regex("y", reg_ex_list)
    
    cmdrtn = anturlar.fos_cmd("setcontext %s " % fid_to_move_port)
    cmdrtn = anturlar.fos_cmd("portenable %s " % moveport)
    liabhar.JustSleep(10)
    
    anturlar.fos_cmd_regex("lscfg --config %s -port %s " %(fid_now, moveport), reg_ex_list)
    cmdrtn = anturlar.fos_cmd_regex("y", reg_ex_list)
    
    cmdrtn = anturlar.fos_cmd("setcontext %s " % fid_now)
    cmdrtn = anturlar.fos_cmd("portenable %s " % moveport)
    liabhar.JustSleep(10)
    cmdrtn = anturlar.fos_cmd("mapsdb --show")
    
    
    ############################################################################
    #### add and remove a zone
    ############################################################################
    z=0
    while z < 3:
        z += 1
        anturlar.fos_cmd('zonecreate test_maps, "124,52;86,31"')
        anturlar.fos_cmd("cfgadd %s, test_maps" % myzone)
        anturlar.fos_cmd("echo yes | cfgenable %s" % myzone)
        
        anturlar.fos_cmd("cfgshow")
        anturlar.fos_cmd("sleep 60")
        
        anturlar.fos_cmd("cfgremove %s, test_maps" % myzone)
        anturlar.fos_cmd("zonedelete test_maps")
        anturlar.fos_cmd("echo 'yes' | cfgenable %s " % myzone)
    
    print("\n\n")
    print("Fabric members")
    print(fabmems)
    print("zonestuff")
    print(myzone)
    
    
    anturlar.fos_cmd("sleep 600")
    
    anturlar.fos_cmd("mapsdb --show")
    
    
    print("\n\n\n\n")
    print("***   CONFIRM the MAPS OUTPUT in section 3.2   ***")
    print("***                                            ***")
    print("***   Domain Change                            ***")
    print("***   Fabric config                            ***")
    print("***   Zone Change                              ***")
    print("***   State Change                             ***")
    print("***   FLOGI                                    ***")
    print("\n\n\n") 
        
    
    return()
###############################################################################   

def tc_01_01_05_06():
    """
        Test Case   25.01.01.05.06
        Title:      Security Events
        Feature:    MAPS
        Objective:  Verify the Security Violations events and alarms
         
    """
    ###########################################################################
    ####
    ####  todo
    ####
    ###########################################################################
    ####
    ####  Steps
    ####   1. add security rules
    ####   2. trigger rules
    ####   3. confirm the rules show in MAPS
    ####
    ####
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    en = anturlar.Maps()
    ####
        
     
    fab_stuff = anturlar.FabricInfo(en.currentFID())
    fabmems = fab_stuff.fabric_members()
        
    ###########################################################################
    #### create security rules and policy
    ####
    security_policy      = "security_policy"
    #maps_tools.cleanup_policy(security_policy)

    telnet_violation     = "sqa_telnet_violation"
    http_violation       = "sqa_http_violaltion"
    scc_violation        = "sqa_scc_violation"
    dcc_violation        = "sqa_dcc_violation"
    login_violation      = "sqa_login_violation"
    invalid_cert         = "sqa_invalid_cert"
    ts_out_of_sync       = "sqa_ts_out_of_sync"
    auth_failure         = "sqa_auth_failure"
    no_fcs_failure       = "sqa_no_fcs_failure"
    incompat_security_db = "sqa_incompat_security_db"
    illegal_command      = "sqa_illegal_cmd"
    
    telnet_violation_cmd  = "mapsrule --create sqa_telnet_violation \
                            -group SWITCH -monitor sec_telnet \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    http_violation_cmd    = "mapsrule --create sqa_http_violation \
                            -group SWITCH -monitor sec_http \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    scc_violation_cmd     = "mapsrule --create sqa_scc_violation \
                            -group SWITCH -monitor sec_SCC \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    dcc_violation_cmd     = "mapsrule --create sqa_dcc_violation \
                            -group SWITCH -monitor sec_DCC \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                                
    login_violation_cmd   = "mapsrule --create sqa_login_violation \
                            -group SWITCH -monitor sec_LV \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    invalid_cert_cmd      = "mapsrule --create sqa_invalid_cert \
                            -group SWITCH -monitor sec_CERT \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    ts_out_of_sync_cmd    = "mapsrule --create sqa_ts_out_of_sync \
                            -group SWITCH -monitor sec_TS \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
         
    auth_failure_cmd    = "mapsrule --create sqa_auth_failure_cmd \
                            -group SWITCH -monitor sec_auth_fail \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"    
                             
    no_fcs_failure_cmd    = "mapsrule --create sqa_no_fcs_failure \
                            -group SWITCH -monitor sec_FCS \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    incompat_security_db_cmd = "mapsrule --create sqa_incompat_security_db \
                            -group SWITCH -monitor sec_IDB \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                             
    illegal_command_cmd   = "mapsrule --create sqa_illegal_cmd \
                            -group SWITCH -monitor sec_CMD \
                            -timebase min -value 0 \
                            -action email,raslog,snmp -op g \
                            -policy security_policy"
                                 
            
    
    ####  list of commands
    cmd_list = [ telnet_violation_cmd, http_violation_cmd, scc_violation_cmd,\
                 dcc_violation_cmd, login_violation_cmd, invalid_cert_cmd, \
                 ts_out_of_sync_cmd, auth_failure_cmd, no_fcs_failure_cmd, \
                 incompat_security_db_cmd, illegal_command_cmd ]
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % security_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % security_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")    
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL")
    
    
    
    
    
    
    anturlar.fos_cmd("mapsdb --show ")
        
    return()
###############################################################################

def tc_01_01_05_07(): 
    """
        Test Case   25.01.01.05.07
        Title:      MAPS SAM EVENTS
        Feature:    MAPS 
        Objective:  Verify the MAPS SAM output
         
    """
    ###########################################################################
    ####
    ####  todo
    ####
    ###########################################################################
    ####
    ####  Steps
    ####   1. MAPSSAM
    ####   2. 
    ####   3. 
    ####
    ####
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    en = anturlar.Maps()
    ####
    
    #### cpu usage  and mem usage
    ####   see test case 2.1.1.5.1 maps switch resource category
    ####   for how this was calculated
    cpu_calc    = en.cpu_usage()
    
    flash_df_command = anturlar.fos_cmd("df")
    ras = re.compile('[\d]+(?=%)')
    flash_raw = ras.search(flash_df_command)
    flash_usage = flash_raw.group()   

    mem_usage = en.mem_usage()
    
    liabhar.cls()
    
    capture_cmd = anturlar.fos_cmd("mapssam --show")
    
    capture_cmd = anturlar.fos_cmd("mapssam --show cpu")
    
    capture_cmd = anturlar.fos_cmd("mapssam --show memory")
    
    capture_cmd = anturlar.fos_cmd("mapssam --show flash")
    
    #capture_cmd = anturlar.fos_cmd("mapssam --clear")
    
    
    
    print("\n\n\n")
    print("***   THIS TEST CASE AUTOMATION                       ***")
    print("\n\n")
    
    print("***   Confirm CPU usage   MEM usage  and FLASH usage  ***")
    print("***   match the output in mapssam command             ***\n\n")
    print("CPU calculated   :   %s  " % cpu_calc)
    print("FLASH calculated :   %s  " % flash_usage)
    print("MEM calculated   :   %s  " % mem_usage)
          
    return()
###############################################################################
   
def tc_01_01_06_07():
    """
        Test Case   25.01.01.06_07
        Title:      MAPS Data Base Management
        Feature:    MAPS
        Objective:  Verify 
    """
    ###########################################################################
    ####  todo -
    ####    1.   check for pizza box or chassis now it fails for pizza line 1703??
    ####    2.  add the slot numbers - right now it is the default 0
    ####   
    ###
    ###########################################################################
    ####
    #### Steps:
    ####    1.
    ####    2.  add error counts to each rule in the historical data section
    ####    3.  
    ####
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    en = anturlar.Maps()
    statsclearcomplete = cofra.clear_stats()
    
    
    slot_list = en.blades(True)
    if "not a" in slot_list:
        slot_list = [0]
    print("slot list   %s " % slot_list )
    
    
    slot_list_len = (len(slot_list))
    
    slot_list_of_ports = [0 for i in range(12)]
    
    #for s in range(slot_list_len):
    #    
    #    print(s)
    #    slot_list_of_ports[s] = []
    #    print("slot list  %s  "  % slot_list_of_ports[s])        
    
    
    print("slot list length is   %s  " % slot_list_len)
    print("slot list  0   %s " % slot_list[0])
    print("slot list  1  %s " % slot_list[1])
    
    
    slot_core_list = en.blades(False,True)
    print("core blades    % s  " % slot_core_list)
    
    ####
    #fabmems = anturlar.fabric_members()
    cmdrtn = anturlar.fos_cmd("mapspolicy --enable dflt_aggressive_policy")
    #cmdrtn = anturlar.fos_cmd("mapspolicy --enable Nervio_test_1")
    cmdrtn = anturlar.fos_cmd("mapsdb --show all")
    #### 
    #### add the slot numbers here
    for s in range(slot_list_len):
        slot_numb = int(slot_list[s])
        
        bld_map = cofra.bladeportmap_Info(slot_numb)
        print("\n\n\nBLADEPORTMAP INFO \n")
        print(bld_map)
        print("@"*80)
        print("#"*80)
        #### create a list of only in_sync ports
        #count_in_synce = 0
        in_sync_ports = []
        
        for i in bld_map:
            if "In_Sync" in (i[12]):
                
                in_sync_ports.append(i)
        
        slot_list_of_ports[s] = in_sync_ports    
    
    
    print("#"*80)
    print("#"*80)
    print("#"*80)
    
    for s in range(slot_list_len):
        print("\n\n")
        print("slot list of ports %s  "  % slot_list_of_ports[s])  
    
    print("#"*80)
    print("#"*80)
    print("#"*80)
    
    ###########################################################################
    ###########################################################################
    cont = 0
    
    
    slotpicklist = []
    
    while cont <= 100000:
        cont +=1
        
        
        print("\n"*20)
        print("#"*80)
        print("#"*80)
        print("#"*80)
        
        slot_list_len = (len(slot_list))
        ####pick a FC blade
        print("SLOT LIST           %s  " % slot_list)
        print("LENGTH of SLOT LIST  %s " % slot_list_len)
        slot_to_add_err = ((liabhar.random_number_int(float(len(slot_list))))) -1
        
        if slot_to_add_err == -1 :
            slot_to_add_err = 0 
        
        print("random slot number  %s  " % slot_to_add_err)
        
        slot_numb_holder = int(slot_list[slot_to_add_err])
        print("slot number is      %s  " % slot_numb_holder)
        slotpicklist.append(slot_numb_holder)
        
        print("the list of slots  is  %s  " % slotpicklist)
        liabhar.JustSleep(10)
        
        
        print("#"*80)
        print("#"*80)
        print("#"*80)
    
        for s in range(slot_list_len):
            print("\n\n")
            print("slot list of ports %s  "  % slot_list_of_ports[s])  
    
    
    
        print("slot to add err value is  ")
        print(slot_to_add_err)
        print("slot list of ports value  ")
        print(slot_list_of_ports[slot_to_add_err])
        print(len(slot_list_of_ports[slot_to_add_err]))
        
        print("#"*80)
        print("#"*80)
        print("#"*80)
        
        #w = slot_list_of_ports[0]
        #print(type(w))
        #print(w)
        #print((len(w)))
        #
        #
        ####  if the list of ports in the slot is [] then skip
        
        ####  pick a port randomly 
        #### 
        #port_to_add_err = ((liabhar.random_number_int(float(len(in_sync_ports))))) - 1
    
        port_to_add_err = ((liabhar.random_number_int(float(len(slot_list_of_ports[slot_to_add_err]))))) - 1
        print("\n\nPORT NUMBER TO ADD  %s  \n\n" % port_to_add_err)
        print("THE LENGTH OF the PORT LIST  %s   \n\n" % len(slot_list_of_ports[slot_to_add_err]))
        #### pick and err type randomly
        multiplier = float(12) #### even though we are picking a number that is
        #### an integer the multiplier has to be a float 
        pck_rndm_err = ((liabhar.random_number_int(multiplier))) - 1
        #### from the list of in_sync ports get the port that cooresponds
        #### to the number    i = in_sync_port[port_to_add_err]
        #try:
        #    i = in_sync_ports[port_to_add_err]
        #except IndexError:
        #    i = 0
            
        try:
            i = slot_list_of_ports[slot_to_add_err][port_to_add_err]
            
        except IndexError:
            i = 0   
            print("could not capture the slot list of ports")
            sys.exit()
            
            
        chip_numb = i[8]
        chip_id = i[11]
        chip_port = i[4]
        port_in_sync = i[12]
        usr_port = i[1]
        #### some debug info
        print("\n\n\n")
        print("="*80)
        print("CHIP #   CHIP-ID    CHIP PORT   STATE ")
        print("%s         %s           %s         %s   " %( chip_numb, chip_id, chip_port, port_in_sync))
        print("@"*80)
        ####  get the port error list
        port_los_error = cofra.PortStats()
        coutr_to_incr_name = port_los_error[pck_rndm_err][0]
        #coutr_to_incr_count = int(port_los_error[pck_rndm_err][1])

        try:
            coutr_to_incr_count = int(port_los_error[pck_rndm_err][1])
            add_this = liabhar.random_number_int(25)
            #coutr_to_incr_count = coutr_to_incr_count + 3
            #coutr_to_incr_count += 21
            coutr_to_incr_count += add_this
        except ValueError:
            #ras_count = re.compile('([\.\d+])([gkmt])')
            #ras_count = ras_count.findall(coutr_to_incr_count)
        
            #print(ras_count)
            coutr_to_incr_count = port_los_error[pck_rndm_err][1]
            print("counter value is  %s  " % coutr_to_incr_count)
            ras_count = re.compile('([\.\d]+)([gkmt])')
            ras_count = ras_count.findall(coutr_to_incr_count)
            print("ras count is  %s  " % ras_count )
            print(type(ras_count))
            current_count = ras_count[0][0]
            current_multiplyer = ras_count[0][1]

            print("\n\nCURRENT_COUNT  %s   " % current_count)
            print(type(current_count))
            
            current_count = float(current_count)
            print("\n\nCURRENT_COUNT  %s   " % current_count)
            print(type(current_count))
            #coutr_to_incr_count = ((current_count * 1001) + 1000)
            #coutr_to_incr_count = (float(ras_count[0])*10.0)
            print("\n\nNEW COUNTER VALUE IS   %s    \n\n" % coutr_to_incr_count)
            
            if 'k' in current_multiplyer:
                print('K is the multiplyer ')
                coutr_to_incr_count = ((current_count * 1001) + 1000)
            
            elif 'm' in current_multiplyer:
                coutr_to_incr_count = ((current_count * 10001) + 10000 )
            
            else:
                coutr_to_incr_count = 1
                
            coutr_to_incr_count = int(coutr_to_incr_count)

        #### configure the db command
        ####   db [slot/chip] stats set [chipport] [counter] [value]
        db_cmd = "db %s/%s stats set %s %s %s" % (slot_numb, chip_numb, \
                                                  chip_port, coutr_to_incr_name, coutr_to_incr_count)
        
        cmdrtn = anturlar.fos_cmd(db_cmd)

    #### confirm if the port is still in_sync once errors are started
    ####  code goes here
        
    ##for i in bld_map:
    ##    if "In_Sync" in (i[12]):
    ##        chip_numb = i[8]
    ##        chip_id = i[11]
    ##        chip_port = i[4]
    ##        port_in_sync = i[12]
    ##        usr_port = i[1]
    ##        print("CHIP #   CHIP-ID    CHIP PORT   STATE ")
    ##        print("%s         %s           %s         %s   " %( chip_numb, chip_id, chip_port, port_in_sync))
           
   
        
        print("MY RANDOM NUMBER   %s " % port_to_add_err)
        print("ERR COUNTER TO INCRIMENT  %s  " % coutr_to_incr_name )
        print("ERR COUNTER TO INCRIMENT   %s " % coutr_to_incr_count)
    
    
        cmdrtn = anturlar.fos_cmd("mapsdb --show all")
        liabhar.JustSleep(10)
        
    return(0)
###############################################################################        
   
def tc_02_01_01_01():
    """
        Test Case   25.02.01.01.01 
        Title:      License of Flow Vision
        Feature:    Flow Vision
        Objective:  Verify Flow Vision requires a license
        
    """
    ###########################################################################
    ####  todo -
    ####    1.   ??
    ####
    ###########################################################################
    ####
    #### Steps:
    #### 1. confirm license is not installed
    ####    a. this can be flow vision, APM or FW license
    ####    b. if license is installed remove license
    #### 2. send each Flow Vision command
    #### 3. confirm the message for each command
    #### 4. add all license back
    ####    a. dont need to confirm Flow Vision license since the
    ####        test will fail if it is not one of the license
    #### 5. send each Flow Vision command
    #### 6. confirm the message for each command
    ####
    #### 7. confirm help message for each command
    #### 8. confirm man page is available for each command
    ####    a. confirm first page of man page - the rest is visual
    ####
    ####  Flow 
    ####  mapsConfig 	 mapsPolicy  	mapsconfig  	mapshelp
    ####  mapsrule 	 mapsHelp   	 mapsRule    	mapsdb      
    ####  mapspolicy  	mapssam 	relayconfig *	logicalgroup *
    ####  * commands will not have a MAPS message since they are used
    ####     in other features
    #### LPMDE3mKQQrtTYYrKAWEPfFGgZfm7X3JBAXFM
    ####     
    #### start the test
    ####
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    en = anturlar.Maps()
    ####
    cmds_list = maps_tools.mapscommand_list()
    cmds_list_w_usage = maps_tools.mapscommand_list("usage")
    cmds_list_w_correct = maps_tools.mapscommand_list("all")
    
    #### get the list of license and remove them from the switch
    l_list = p.getLicense()
    print("license list \n\n%s "% l_list)
    for license in l_list:
        anturlar.fos_cmd("licenseremove %s " % license)
    #### no need to confirm the Flow Vision license
    ####  just remove all the license and test
    ####   if no license for flow vision the test case will fail
    
    cmds_list = flow_tools.flow()
    cmds_list_w_usage = maps_tools.mapscommand_list("usage")
    cmds_list_w_correct = maps_tools.mapscommand_list("all")
    
    
    
    
    fab_stuff = anturlar.FabricInfo(en.currentFID())
    fabmems = fab_stuff.fabric_members()
    myzone = fab_stuff.zone_info()
    
    eports = en.e_ports()
    #print("\n\nMY E-PORTS  %s " % eports )
    #print("use the first port found for now %s  " % eports[0][0])
    #### for pizza box
    
    #fid_now = en.currentFID()
    
    f = cofra.DoSupportsave('10.38.243.102','ftp2','ftp','chassisname')
    
    x = 5555
    while x <= 3600:
        
        anturlar.fos_cmd("date") 
        anturlar.fos_cmd("mapsdb --show")
        cmdrtn = anturlar.fos_cmd("sleep 5")
        
        for p in eports:
            x += 1
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
            #cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            #cmdrtn = anturlar.fos_cmd("sleep 10")
        
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
    
    
        for p in eports:
            x += 1
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
    
    
    
    return()
###############################################################################   
    
 
 
def tc_07_01_06_01():
    """
        Test Case   25.07.01_06_01_supportsave_test
        Title:
        Feature:    MAPS
        Objective:  Verify during and after a supportsave there is no reporting
                    of CPU usage. also other monitoring issues.
                    
    """
    ###########################################################################
    ####  todo -
    ####    1.   supportsave
    ####    2.   check cpu usage
    ####
    ###########################################################################
    ####
    #### Steps:
    ####    1. supportsave
    ####    2. check cpu usage for the value
    ####    3. errdumpall look for MAPS messages
    ####    
    ####
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    print("get the maps info \n")
    en = anturlar.Maps()
    print("\n\nComplete with MAPS info")
    ####
    
    fab_stuff = anturlar.FabricInfo(en.currentFID())
    fabmems = fab_stuff.fabric_members()
    myzone = fab_stuff.zone_info(1)
    eports = en.e_ports()
   
    cpu_start   = en.cpu_usage()
    mem_start   = en.mem_usage()
    temp_start  = en.temp_status()
    
    print("@"*80)
    print("@"*80)
    print("CPU USAGE  = %s " % cpu_start)
    print("MEM USAGE  = %s " % mem_start)
    print("TEMP START = %s " % temp_start)
    print("@"*80)
    print("@"*80)
    
    
    x = 0
    while x <= 100:
    
        f = cofra.DoSupportsave('10.38.243.102','ftp2','ftp','supportsave/test_case_07_01_06_01')
        print("\nSupportsave Complete\n")
        liabhar.JustSleep(60)
        cpu_now   = en.cpu_usage()
        mem_now   = en.mem_usage()
        temp_now  = en.temp_status()
        x += 1
        
    print("@"*80)
    print("@"*80)
    print("CPU USAGE  = %s " % cpu_start)
    print("MEM USAGE  = %s " % mem_start)
    print("TEMP START = %s " % temp_start)
    print("#"*80)
    print("CPU USAGE  = %s " % cpu_now)
    print("MEM USAGE  = %s " % mem_now)
    print("TEMP START = %s " % temp_now)
    
    some_cpu_ras = anturlar.fos_cmd("errdumpall | grep CPU")
    some_mem_ras = anturlar.fos_cmd("errdumpall | grep MEMORY")
        
    print("@"*80)
    print("@"*80)
    print("#"*80)
    print(some_cpu_ras)
    print(some_mem_ras)
    
    
    
    x = 5555
    while x <= 3600:
        
        anturlar.fos_cmd("date") 
        anturlar.fos_cmd("mapsdb --show")
        cmdrtn = anturlar.fos_cmd("sleep 5")
        
        for p in eports:
            x += 1
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
            #cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            #cmdrtn = anturlar.fos_cmd("sleep 10")
        
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
    
    
        for p in eports:
            x += 1
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
    
    
    
    return()
###############################################################################  
   
    
def tc_01_01_template():
    """
        Test Case   25.01.01.template
        Title:
        Feature:    Predfined Group Management
        Objective:  Template - discription of the test case and the area that
                    is being tested in this test case
        
    """
    ###########################################################################
    ####  todo -
    ####    1.   ??
    ####
    ###########################################################################
    ####
    #### Steps:
    ####    1. 
    ####
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    en = anturlar.Maps()
    ####
    #fabmems = anturlar.fabric_members()
    

    fab_stuff = anturlar.FabricInfo(en.currentFID())
    fabmems = fab_stuff.fabric_members()
    myzone = fab_stuff.zone_info()
    
    eports = en.e_ports()
    #print("\n\nMY E-PORTS  %s " % eports )
    #print("use the first port found for now %s  " % eports[0][0])
    #### for pizza box
    
    #fid_now = en.currentFID()
    
    f = cofra.DoSupportsave('10.38.243.102','ftp2','ftp','chassisname')
    
    x = 0
    while x <= 3600:
        
        anturlar.fos_cmd("date") 
        anturlar.fos_cmd("mapsdb --show")
        cmdrtn = anturlar.fos_cmd("sleep 5")
        
        for p in eports:
            x += 1
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
            #cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            #cmdrtn = anturlar.fos_cmd("sleep 10")
        
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
    
    
        for p in eports:
            x += 1
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
            cmdrtn = anturlar.fos_cmd("sleep 10")
    
    
    
    return()
###############################################################################   
    
 
def mem_monitor_test():
    """
    excecute the mem_monitor test in cofra
    
    """
    
    cofra.mem_monitor(13,104)
###############################################################################

 
 
def firmwaredownload(frmdwn, frmup, email):
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
        f = cofra.DoFirmwaredownloadChoice(frmdwn,frmup, email)
        
        #
        #print("value of f is :  ")
        #print(f)
        #
        #if "failed" in f:
        #    sys.exit()
        
         
        liabhar.count_down(600)
        
        anturlar.connect_tel_noparse(myip, 'root', 'password')
        en = anturlar.SwitchInfo()
        capture_cmd = anturlar.fos_cmd("version")
        
        f = cofra.DoFirmwaredownloadChoice(frmdwn, frmup, email)
    
        anturlar.connect_tel_noparse(myip, 'root', 'password')
        en = anturlar.SwitchInfo()

    return(0)
###############################################################################
 
def credit_recovery():
    pass


def add_monitor_types():
    """
        add rules to a switch until the limit is reach
        
    """
    
    ###########################################################################
    #### start testing
    ####
    #### create the object and clear stats
    en = anturlar.Maps()
    ####
    maps_tools.add_rules_each_monitor_type(False,True,False)
    
    return()


def cleanup_rules():
    """
    
    """
    
    ###########################################################################
    ###########################################################################
    ####
    ####
    ####  start
    
    en = anturlar.Maps()
    ######
    maps_tools.cleanup_policy("Nervio_test_1")
    
    return()
    
def cleanup_non_def_rules():
    """
    
    """
    
    en = anturlar.Maps()
    
    maps_tools.cleanup_all_rules()
    
    
    return()
    
    
def add_RoR_rules():
    """
    
    """
    
    maps_tools.add_RoR_rules_on_each_rule()



    
    return(True)





def end():
    pass
        
    
