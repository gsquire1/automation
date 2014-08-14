#!/opt/python3/bin/python3

###############################################################################
#### Home location is
####
###############################################################################

import anturlar
import liabhar
import re
import random
import os,sys
"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""


def tc_01_01_01_02():
    """
        Test Case   25.01.01.01.02
        Title:      MAPS commands available with a license
        Feature:    MAPS CLI
        Confirm MAPS CLI function correctly with and without a license
        installed
        
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
    ####   1.  pass / fail for each step of test case
    ####       make the test_result a list of list [ step_0 pass ][step_2 fail]
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
    test_result = ""
    
    p = anturlar.Maps()
    cmds_list = mapscommand_list()
    cmds_list_w_usage = mapscommand_list("usage")
    cmds_list_w_correct = mapscommand_list("all")
    #### get the list of license and remove them from the switch
    l_list = p.getLicense()
    print("license list \n\n%s "% l_list)
    for license in l_list:
        anturlar.fos_cmd("licenseremove %s " % license)
    #### no need to confirm the Flow Vision license
    ####  just remove all the license and test
    ####   if no license for flow vision the test case will fail
    
    for cmd in cmds_list:
        console_out = anturlar.fos_cmd("%s" % cmd)
        if "license not present" not in console_out:
            test_result += cmd
            test_result += ' step1'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")

    for license in l_list:
        anturlar.fos_cmd("licenseadd %s " % license)
        
    
    for cmd in cmds_list_w_usage:
        console_out = anturlar.fos_cmd("%s" % cmd)
        if "Usage:" in console_out:
            pass
        elif "MAPS not active." in console_out:
            pass
        else:
            test_result += cmd
            test_result += ' step2'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
            
    
    for cmd in cmds_list_w_correct:
        console_out = anturlar.fos_cmd("%s" % cmd)
        if "root>" not in console_out:
            test_result += cmd
            test_result += ' step3'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")       
    
    
    if test_result == "":
        test_result = "PASS"
    
    print("\n\nTEST RESULTS FOR Test Case   25.01.01.01.02 ")
    print(test_result)
    return(test_result)

def tc_01_01_03_01():
    """
        Test Case   25.01.01.03.01
        Title:      MAPS Category Management Default thresholds
        Feature:    MAPS 
        Confirm MAPS default thresholds are set correctly
        
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
    
    #### start the test
    test_result = ""
    
    p = anturlar.Maps()
    sw_rules = p.get_rules()
    #sw_rules = str(sw_rules)
    #sw_rules = sw_rules.replace("'", "") #### remove ' from string
    #sw_rules = sw_rules.replace("[", "") #### remove open bracket
    #sw_rules = sw_rules.replace("]", "") #### remove ending bracket
    df_rules = maps_default_rule()
    
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
        #print("%s      %s " % (sw_rules[i], df_rules[i]))
        if sw_rules[i] not in df_rules:
            rule_differ += 1
            test_result += sw_rules[i]
            test_result += ' step1'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
        
        i += 1
        
    print("The number of rules that differ are %s " % rule_differ)
    print("The number of additional rules on the switch %s " % ( count - count_df))
    print(len(sw_rules))
    print(len(df_rules))

    if test_result == "":
        test_result = "PASS"
    
    print("="*80)
    print("\n\nTEST RESULTS FOR Test Case   25.01.01.01.02 ")
    print(test_result)
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
    ####    a. sfpshow - count the id (sw) and Speed that are 16 / 10 and not 16 / 10
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
    
    t1 = len(blade_count)
    
    
    t_fports = int(pgm.logicalgroup_count("ALL_PORTS"))
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

    print("blade_count is           : %s" % len(blade_count))
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
    
    if test_result == "":
        test_result = "PASS"
    
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
    anturlar.clear_stats()
    
    #### create a policy and rules
    ####
    flash_rule_name = "sqa_sw_res_flash_usage_down"
    cpu_rule_name   = "sqa_sw_res_cpu_usage_down"
    mem_rule_name   = "sqa_sw_res_memory_usage"
    temp_rule_out   = "sqa_sw_temp_out"
    temp_rule_in    = "sqa_sw_temp_in"
    
    
    cmd_flash = "mapsrule --create "+ flash_rule_name +" -group chassis\
              -monitor flash_usage -value 30 -action email,raslog,snmp,sw_marginal\
              -op ge -policy environ_test" 
    
    cmd_cpu= "mapsrule --create "+ cpu_rule_name +" -group chassis \
               -monitor cpu -value 100 -action email,raslog,snmp\
               -op le -policy environ_test"
    
    cmd_mem = "mapsrule --create "+ mem_rule_name +"  -group chassis \
              -monitor memory_usage -value 100 -action email,raslog,snmp  \
              -op le -policy environ_test"
    
    cmd_temp = "mapsrule --create "+ temp_rule_out +" -group ALL_ts \
               -monitor temp -timebase none -value out_of_range \
               -action snmp,raslog,email -op eq -policy environ_test"
    
    cmd_temp_in = "mapsrule --create " + temp_rule_in + " -group ALL_ts \
                  -monitor temp -timebase none -value IN_range \
                  -action snmp,raslog,email -op eq -policy environ_test" 
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
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL,SW_CRITICAL,SW_MARGINAL")
    anturlar.fos_cmd("mapspolicy --enable environ_test")
    ####
    #### do some steps here
    ####
    print("\n\nwaiting for maps actions to be triggered. . .")
    liabhar.JustSleep(600)
    ####  see if there is a ras log message for each rule
    mem_ras_message   = en.ras_message_search(mem_rule_name)
    flash_ras_message = en.ras_message_search(flash_rule_name)
    temp_ras_message  = en.ras_message_search(temp_rule_in)
    cpu_ras_message   = en.ras_message_search(cpu_rule_name)
    
    ####  see if there is a mapsdb entry for each rule
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
    ####  no calculation needed since the use% is the correct number
    ####
    flash_df_command = anturlar.fos_cmd("df")
    ras = re.compile('[\d]+(?=%)')
    flash_raw = ras.search(flash_df_command)
    flash_usage = flash_raw.group()   
    
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
    temp_status = en.temp_status()
    
    ###########################################################################
    ###########################################################################
    ####  clean up
    ####
    policy_list = en.get_policies("s")
    policy_user_list = en.get_nondflt_policies()
    liabhar.count_down(5)
    
    cleanup_policy(policy_user_list)
    policy_user_list_final = en.get_policies("s")
     
     
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
    print("memory db message is      :  %s  " % mem_confirm)
    print("flash  db message is      :  %s  " % flash_confirm)
    print("cpu    db message is      :  %s  " % cpu_confirm)
    print("temp   db message is      :  %s  " % temp_confirm)
    print("="*80)
    print("SWITCH VALUES")
    print("calculated memory usage   :  %s  " % mem_usage )
    print("calculated flash usage    :  %s  " % flash_usage)
    print("calculated switch CPU     :  %s  " % cpu_calc)
    print("calculated Temp info      :  %s  " % temp_status)
    
    return()

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
    anturlar.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % port_health_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % port_health_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL,\
                     SW_CRITICAL,SW_MARGINAL")
    
    anturlar.fos_cmd("porterrshow")
    
    print("check for maps messages") 
    print("wait here for the user to finish")
    
    print("use the db command to poke for one test, \
          use the finisar for confirmation")
    
    
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
    anturlar.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % fcip_health_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % fcip_health_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL,SW_CRITICAL,SW_MARGINAL")
    
    anturlar.fos_cmd("portshow fciptunnel ")
    anturlar.fos_cmd("portshow fcipcircuit ")
    
    print("check for maps messages") 
    print("wait here for the user to finish")
    
    print("use the db command to poke for one test, use the finisar for confirmation")
    
    
    
    
    
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
    anturlar.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ####
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % perf_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % perf_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL,\
                     SW_CRITICAL,SW_MARGINAL")
    
    anturlar.fos_cmd("mapsdb --show")
    
    print("check for maps messages") 
    print("wait here for the user to finish")
    
    print("use the db command to poke for one test, \
          use the finisar for confirmation")
    
    
    
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
    anturlar.clear_stats()
    
    ###########################################################################
    #### setup the rules and policy for this test
    ###########################################################################
    cmdrtn = anturlar.fos_cmd("mapspolicy --create %s " % fabric_state_policy)
    cmdrtn = anturlar.fos_cmd("mapspolicy --show -summary")
    for cmd in cmd_list:
        anturlar.fos_cmd(cmd)
    anturlar.fos_cmd("mapspolicy --enable %s " % fabric_state_policy)
        
    #### setup the actions
    anturlar.fos_cmd("mapsconfig --actions RASLOG,SNMP,EMAIL,\
                     SW_CRITICAL,SW_MARGINAL")
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
    
    
    #### for pizza box
    
        x = 0
        while x <= 1:
            for p in eports:
                x += 1
                cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
                cmdrtn = anturlar.fos_cmd("sleep 3")
                cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
                cmdrtn = anturlar.fos_cmd("sleep 3")
                
    ############################################################################
    #### fabric config event
    ####  disable all the ports on the target switch
    ####  when the ports are enabled the fabric will reconfigure
    ############################################################################
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portdisable %s " % p[0])
        cmdrtn = anturlar.fos_cmd("sleep 10")
        
        for p in eports:
            cmdrtn = anturlar.fos_cmd("portenable %s " % p[0])
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
    while z < 1:
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
    
    
    anturlar.fos_cmd("sleep 60")
    
    anturlar.fos_cmd("mapsdb --show")
    print("\n\ncheck for maps messages") 
    print("wait here for the user to finish")
    
    print("use the db command to poke for one test, \
          use the finisar for confirmation")
    
    
    
    
    
    
    
    
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
    ####    1.   ??
    ####
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
    ####
    #fabmems = anturlar.fabric_members()
    cmdrtn = anturlar.fos_cmd("mapspolicy --enable dflt_aggressive_policy")
    cmdrtn = anturlar.fos_cmd("mapsdb --show all")
    #### 
    
    

   
   
    
def tc_01_01_template():
    """
        Test Case   25.01.01.template
        Title:
        Feature:    Predfined Group Management
        Objective:  Verify the predefined groups including only the elements
        defined for each group 
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
    print("\n\nMY E-PORTS  %s " % eports )
    print("use the first port found for now %s  " % eports[0][0])
    #### for pizza box
    
    fid_now = en.currentFID()
    
    
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
    cons_out = anturlar.fos_cmd("flow --show")

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
        this can go to anturlar in the FlowV class
        
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
        
    cmd_delete = "flow --delete %s " % (fname)
    
    cons_out = anturlar.fos_cmd(cmd_create)
    
    while repeat > 0:
        #print(repeat,"\n")
        cons_out = anturlar.fos_cmd(cmd_create)
        cons_out = anturlar.fos_cmd("flow --show")
        
        liabhar.count_down(3600)
        
        cons_out = anturlar.fos_cmd(cmd_delete)
        cons_out = anturlar.fos_cmd("flow --show")
        
        print("\n\n",cons_out)
        liabhar.count_down(300)
        
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
        
    cmd_create = "%s -noactivate -%s " % (cmd_create, "bidir")
    
    
    cons_out = anturlar.fos_cmd(cmd_create)
    cons_out = anturlar.fos_cmd("")
    
    #while repeat > 0:
    #    print("repeat\n")
    #    repeat = repeat - 1 
    
    return 0 
    
    
def add_flows_count(fname, scr, dst, ingrp, egrp, feat, cnt):
    
    count = 0
    while count <= cnt:
        fn = "%s_%s" % (fname,count)
        add_flow(fn, scr, dst, ingrp, egrp, feat)
        count += 1
    
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
            
    
def check_gen_all_stats():
    """
        start the gen_all SIM ports test and capture the number of runs
        the percent of run, the frames generated brom IngrPort and frames
        generated to EgrPort
        
    """
    sw_info = anturlar.SwitchInfo()
    sw_info_ls = sw_info.ls()
    fid_now = sw_info.ls_now()
    sw_ip = sw_info.ipaddress()
    
    fv = anturlar.FlowV()
    fv.genAll("on")
    
    f = "%s%s%s"%("logs/Gen_all_stats_test_case_file",sw_ip,".txt")
    clear = 0
    if clear == 1 :
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
    else:
        ff = liabhar.FileStuff(f, 'a+b')  #### open for appending
            
    st = "Runs  Percent  Ingrport  Egrport \n"        
    header = "%s%s%s%s" % ("\nGEN ALL CAPTURE FILE \n", "  sw_info ipaddr  ",sw_ip, "\n==============================\n\n")  
    ff.write(header)
    ff.write(st)
    d=0
    
    while d <= 1000:
        stats = fv.genAllStats()
        print(stats)
        print("run number  %s" % d)
        ff.write(stats)
        liabhar.count_down(60)
        d += 1
        
    ff.close()
        
 
def randomList(a):
    b = []
    for i in range(len(a)):
        element = random.choice(a)
        a.remove(element)
        b.append(element)
    
    return b
    
def flow_to_each_SIM():
    """
        find all the SIM ports in the fabric and create a flow
        from each SIM port to all the Other SIM ports
          Since this test case finds all the switches in the
          fabric it might not be good to run in fabric mode
        steps
         1. get the ip list of switches in the fabric
         2. for each switch get a list of SIM ports
         3. create a flow for each SIMport to all other SIM ports
         4. start all of the flows if not started
         5. if there are only 2 switches only send to the other switch
            if there are more than 2 switches then send to a random port which
            could also be on the same switch
    """
    
    sw_info = anturlar.SwitchInfo()
    fid_now = sw_info.ls_now()
    cons_out = anturlar.fos_cmd(" ")
    #sw_ip = sw_info.ipaddress()
    f = anturlar.FabricInfo()
    ip_list = f.ipv4_list()
    ip_count = len(ip_list)
    ip_c = ip_count
    
    combine_port_list = []
    list_for_j = []
    list_for_i = []
    temp_list = []
        
    for ip in ip_list:
        anturlar.connect_tel_noparse(ip,'root','password')
        s = anturlar.SwitchInfo()
        cons_out = anturlar.fos_cmd(" ")
        cons_out = anturlar.fos_cmd("setcontext %s" % (fid_now))
        ports = s.sim_ports(False)
        #print("\n\n\n",ports, "\n\n\n")
        #combine_port_list.append(ports)
        combine_port_list = combine_port_list + ports
        if ip_c == 2:
            list_for_i = ports
            #print("\n\n\nI list \n")
            #print(list_for_i)
            liabhar.count_down(10)
            ip_c = 1
        if ip_c == 1:
            list_for_j = ports
            #print("\n\n\nJ list \n")
            #print(list_for_j)
            liabhar.count_down(10)
            
    flow_name_base = "Send_to_each_"
    count = 0
     
    #### need index address for simport 
    #### now create a flow to each simport
    #print(combine_port_list)
    
    for ip in ip_list:
        anturlar.connect_tel_noparse(ip,'root','password')
        s = anturlar.SwitchInfo()
        cons_out = anturlar.fos_cmd(" ")
        cons_out = anturlar.fos_cmd("setcontext %s " % (fid_now))
        cons_out = anturlar.fos_cmd("flow --deact sys_gen_all_simports -fea all")  
            
            
        #### randomize the list
        combine_port_list = randomList(combine_port_list)
        j_port_list = combine_port_list
        #print("\n\n\nPORT LIST RANDOMIZED  \n", combine_port_list)
        #print("\n\n\nNEW LIST RANDOMIZED  \n", new_combine_port_list)
        if len(ip_list) == 2:
            #print("\n\n\nyes only two switches\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            liabhar.count_down(10)
            random.shuffle(list_for_i)
            #print("start I list ")
            for i in list_for_i:
                random.shuffle(list_for_j)
                generate_port = i[0]
                generate_addr = i[1]
                #print("\n\ngenerator port and address  %s  %s  \n\n" %(generate_port, generate_addr))
                
                #### this loops on the same list of combined port list
                #### one idea was to select a random element from the list each time
                ####  
                for j in list_for_j: 
                    target_port = j[0]
                    target_addr = j[1]
                    #print("\n\ntarget port and address  %s  %s \n\n" %( target_port, target_addr))
                    
                    if generate_port not in target_port:
                        flow_name = ("%s%s" % (flow_name_base,count))
                        count +=1
                        #print(flow_name, "   " , generate_port," ", generate_addr, "to this port  " ,target_port," ", target_addr)
                        cmd_create = "flow --create %s -srcdev %s -dstdev %s -ingrport %s -fea gen,mon" % (flow_name, generate_addr,target_addr, generate_port)
                        cons_out = anturlar.fos_cmd(cmd_create)   
                        if "maximum limit" in cons_out:
                            count -= 1
                            break
                        if "Port does not" in cons_out:
                            break
                        if "PID or WWN do not" in cons_out:
                            break
                        if "Exceeds maximum flow limit" in cons_out:
                            count -= 1
                            break
            temp_list = list_for_i
            list_for_i = list_for_j
            list_for_j = temp_list
            
        else:    
            for i in combine_port_list:
                random.shuffle(j_port_list)
                generate_port = i[0]
                generate_addr = i[1]
                #### this loops on the same list of combined port list
                #### one idea was to select a random element from the list each time
                ####  
                for j in j_port_list: 
                    target_port = j[0]
                    target_addr = j[1]
                    if generate_port not in target_port:
                        flow_name = ("%s%s" % (flow_name_base,count))
                        count +=1
                        print(flow_name, "   " , generate_port," ", generate_addr, "to this port  " ,target_port," ", target_addr)
                        cmd_create = "flow --create %s -srcdev %s -dstdev %s -ingrport %s -fea gen,mon" % (flow_name, generate_addr,target_addr, generate_port)
                        cons_out = anturlar.fos_cmd(cmd_create)   
                        if "maximum limit" in cons_out:
                            count -= 1
                            break
                        if "Port does not" in cons_out:
                            break
                        if "PID or WWN do not" in cons_out:
                            break
                        if "Exceeds maximum flow limit" in cons_out:
                            count -= 1
                            break
    
    
def ha_failover( times=2):
    """
        do HA failover on directors
        do hareboot on pizza box
    """
    #### steps
    ####  1. Determine Pizza box or Director
    ####  2. save username and password
    ####  3. HA Failover 
    ####  4. wait some time
    ####  5. reconnect
    ####  6. 
    ####   
    sw_info = anturlar.SwitchInfo()
    fid_now = sw_info.ls_now()
    ip_addr = sw_info.ipaddress()
    go_or_not = sw_info.synchronized()
    cons_out = anturlar.fos_cmd(" ")
    username = 'root'
    pwrd = 'password'
    counter = 1
    new_connect = True
    ####  add error checking here
    ####   the first step is to get original data before starting the test
    #print("\n\noutside the while loop the go or not is equal to %s  " % go_or_not)
    liabhar.count_down(10)
    
    
    
    while new_connect:
        print("@"*40)
        print("Starting Failover number %s "%counter)
        print("@"*40)
        
        try:
            
            while times > 0:
                anturlar.connect_tel_noparse(ip_addr,'root','password')
                sw_info = anturlar.SwitchInfo()
                while sw_info.synchronized() is False:
                    liabhar.count_down(30)
                    #print("\n\n")
                    #print("@"*30)
                    #print("\nwaiting for CPs to sync\n")
                    #print("not in sync\n")
                    #print("@"*30)
                    #print("@"*30)
                    liabhar.count_down(60)
                                
                sw_info = anturlar.fos_cmd("echo Y | hafailover")
                ####  add error checking here
                ####   get the same data as before the while loop and compare
                #print("\n\ninside the while loop the go or not is equal to %s  " % go_or_not)
                times -= 1
                #print("\n\nwait here  %s\n\n" % times)
                liabhar.count_down(30)
        
        except:
        #except SocketError as e:
            #if e.errno != errno.ECONNRESET:
                #print("\n\n\nCONNECTION ERROR TRYING TO RECONNECT\n\n\n")
                #raise 
            print("========================")
            print("Telnet was disconnected ")
            print("Attempting to reconnect shortly \n")
            print("========================")
            #pass
            liabhar.count_down(60)
        if times == 0:
            new_connect = False   
     
     
    
def ha_failover_check_adjacent( adjacent_ipaddr, times=2, wait=300):
    """
        do HA failover on directors
        do hareboot on pizza box
    """
    #### steps
    ####  1. Determine Pizza box or Director
    ####  2. save username and password
    ####  3. HA Failover 
    ####  4. wait some time
    ####  5. reconnect
    ####  6. 
    ####   
    sw_info = anturlar.SwitchInfo()
    fid_now = sw_info.ls_now()
    ip_addr = sw_info.ipaddress()
    go_or_not = sw_info.synchronized()
    cons_out = anturlar.fos_cmd(" ")
    username = 'root'
    pwrd = 'fibranne'
    counter = 1
    new_connect = True
    ####  add error checking here
    ####   the first step is to get original data before starting the test
    #print("\n\noutside the while loop the go or not is equal to %s  " % go_or_not)
    liabhar.count_down(10)
    
    
    
    while new_connect:
        print("@"*40)
        print("Starting Failover number %s "%counter)
        print("@"*40)
        
        try:
            
            while times > 0:
                anturlar.connect_tel_noparse(ip_addr,'root','fibranne')
                sw_info = anturlar.SwitchInfo()
                #while sw_info.synchronized() is False:
                #    liabhar.count_down(30)
                #    #print("\n\n")
                #    #print("@"*30)
                #    #print("\nwaiting for CPs to sync\n")
                #    #print("not in sync\n")
                #    #print("@"*30)
                #    #print("@"*30)
                #    liabhar.count_down(60)
                                
                sw_info = anturlar.fos_cmd("echo Y | hareboot")
                ####  add error checking here
                ####   get the same data as before the while loop and compare
                #print("\n\ninside the while loop the go or not is equal to %s  " % go_or_not)
                times -= 1
                #print("\n\nwait here  %s\n\n" % times)
                liabhar.count_down(wait)
        
        except:
        #except SocketError as e:
            #if e.errno != errno.ECONNRESET:
                #print("\n\n\nCONNECTION ERROR TRYING TO RECONNECT\n\n\n")
                #raise 
            print("========================")
            print("Telnet was disconnected ")
            print("Attempting to reconnect shortly \n")
            print("========================")
            #pass
            #liabhar.count_down(10)
        if times == 0:
            new_connect = False   
     
     
        anturlar.connect_tel_noparse(adjacent_ipaddr,'root','fibranne')
        sw_info = anturlar.SwitchInfo()
        sw_info = anturlar.fos_cmd("switchshow")
        sw_info = anturlar.fos_cmd("coreshow")
        if "panic" in sw_info:
            sys.exit()
        anturlar.close_tel()


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
             "mapsconfig --testmail -subject -message ", \
             "mapsconfig --import  ", \
             "mapsconfig --deimport ", \
             "mapsconfig --enablemaps ", \
             "mapsconfig --No_purge", \
             "mapsconfig -", \
             "mapsconfig --enableFPImon", \
             "mapsconfig --disableFPImon", \
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
           
   
def end():
    pass
        
    
