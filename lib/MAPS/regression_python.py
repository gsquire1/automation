#!/usr/bin/env python3

###############################################################################
###############################################################################
####
####  test each class and function
####
###############################################################################


import anturlar
import re
import liabhar
import cofra
import sys

"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""


#### confirm anturlar
def chck_a():
    #global tn
    
    si = anturlar.SwitchInfo()
    does_allow_xisl   = si.allow_xisl()
    show_all_ports    = si.all_ports()
    show_all_ports_fc = si.all_ports_fc_only()    
    base_y_n          = si.base_check()
    blade_8G          = si.blade_search_8GB()
    blades            = si.blades()
    blade_blank       = si.blank_type()
    fid_now           = si.currentFID()
    chass_name        = si.chassisname()
    dport             = si.d_ports()
    dflt_switch       = si.default_switch()
    dir_y_n           = si.director()
    disbled_ports     = si.disabled_ports()
    eports            = si.e_ports()
    exports           = si.ex_ports()
    vexports          = si.vex_ports()
    fports            = si.f_ports()
    fans              = si.fan_count()
    fcr_y_n           = si.fcr_enabled()
    gports            = si.g_ports()
    lic_lst           = si.getLicense()
    sw_ip             = si.ipaddress()
    lport             = si.loopback()
    ls_lst            = si.ls()
    ls_crnt           = si.ls_now()
    nports            = si.n_ports()
    pdports           = si.persistent_disabled_ports()
    sensors_lst_t     = si.sensor_t_f_ps("t")
    sensors_lst_t     = si.sensor_t_f_ps("f")
    sensors_lst_t     = si.sensor_t_f_ps("ps")
    sfpinfo           = si.sfp_info()
    sports            = si.sim_ports()
    swstate           = si.switch_state()
    sw_id             = si.switch_id()
    sw_name           = si.switch_name()
    sw_status         = si.switch_status()  ### fcr info
    sw_type           = si.switch_type()
    sw_sync           = si.synchronized()
    sw_tmp            = si.temp_sensors()
    vf_y_n            = si.vf_enabled()
    
    ####  Fabric
    
    fi = anturlar.FabricInfo()
    sid_nums          = fi.sid_numbers()
    sw_cnt            = fi.switch_count()
    ipv4_lst          = fi.ipv4_list()
     
    print("$"*80)
    print(ipv4_lst)
    print("@"*80)
    
    ipv4_fcr          = fi.ipv4_plus_fcr_list('root','password')
    
    print("$"*80)
    print(ipv4_fcr)
    print("@"*80)
    
    
    fab_name          = fi.name()
    fab_all           = fi.all_info()
    fab_memb          = fi.fabric_members()
    fab_zone          = fi.zone_info()

    
    #####  FCIP info
    #
    fc = anturlar.FcipInfo()
    fc_ge_ports        = fc.all_online_ge_ports()
    fc_ge_ports_dble   = fc.all_ge_port_disabled()
    fc_vex_ports       = fc.vex_ports()
    fc_ex_ports        = fc.ex_ports()
    fc_ge_ports        = fc.ge_ports()
    
    
    ####  DATE TIME STUFF
    ####
    
    dt = liabhar.dateTimeStuff()
    crrnt_date         = dt.current()
    time_stamp         = dt.stamp()
    time_simple        = dt.simple()
 
    ####  other stuff
    
    
    
    print("\r\n"*5)
    print(crrnt_date)
    print(time_stamp)
    print(time_simple)
  
    
    liabhar.cls()
    liabhar.count_down(3)
    
    some_string_0 = "this is to compare different text strings"
    some_string_1 = "this is to compare diff erent text strings"
    some_string_2 = "this is to compare different text strings"
    
    case_1_diff  = liabhar.diff_compare(some_string_0, some_string_1)
    case_2_diff   = liabhar.diff_compare(some_string_0, some_string_2)
    
    print("result of case 1 diff test   %s   " % case_1_diff  )
    print("result of case 2 diff test   %s   " % case_2_diff  )

    this_pltfrm_is  = liabhar.platform()
    print("this platform is  %s  "  % this_pltfrm_is )
    
    print(liabhar.random_number())
    print(liabhar.random_number_int(23))
    


    #### COFRA
    
    bld_port_map_info   = cofra.bladeportmap_Info(3)
    port_stats_0        = cofra.PortStats()
    fid_to_check        = "24"
    fids_0              = cofra.fids_check(fid_to_check)
    print("THIS IS FID CHECK %s  is on the switch  %s  " % (fid_to_check, fids_0 ))
    print("Blade Port Map Info ")
    print(bld_port_map_info)
    print("PORT STATS  ")
    print(port_stats_0)
    
    
    clr_stats           = cofra.clear_stats()




def chck_fab():
    ###########################################################################
    ###########################################################################
    ####
    ####
    ####
    pass
    




























