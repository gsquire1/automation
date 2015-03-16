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
    #show_all_ports    = si.all_ports()
    #show_all_ports_fc = si.all_ports_fc_only()
    #base_y_n          = si.base_check()
    #blade_8G          = si.blade_search_8GB()
    #blades            = si.blades()
    #blade_blank       = si.blank_type()
    #fid_now           = si.currentFID()
    #chass_name        = si.chassisname()
    #dport             = si.d_ports()
    #dflt_switch       = si.default_switch()
    #dir_y_n           = si.director()
    #disbled_ports     = si.disabled_ports()
    #eports            = si.e_ports()
    #exports           = si.ex_ports()
    #vexports          = si.vex_ports()
    #fports            = si.f_ports()
    #fans              = si.fan_count()
    #fcr_y_n           = si.fcr_enabled()
    #gports            = si.g_ports()
    #lic_lst           = si.getLicense()
    #sw_ip             = si.ipaddress()
    #lport             = si.loopback()
    #ls_lst            = si.ls()
    #ls_crnt           = si.ls_now()
    #nports            = si.n_ports()
    #pdports           = si.persistent_disabled_ports()
    #sensors_lst_t     = si.sensor_t_f_ps("t")
    #sensors_lst_t     = si.sensor_t_f_ps("f")
    #sensors_lst_t     = si.sensor_t_f_ps("ps")
    #sfpinfo           = si.sfp_info()
    #sports            = si.sim_ports()
    #swstate           = si.switch_state()
    #sw_id             = si.switch_id()
    #sw_name           = si.switch_name()
    ##sw_status         = si.switch_status()  ### fcr info
    #sw_type           = si.switch_type()
    #sw_sync           = si.synchronized()
    #sw_tmp            = si.temp_sensors()
    #vf_y_n            = si.vf_enabled()
    
    ####  Fabric
    
    fi = anturlar.FabricInfo()
    sid_nums          = fi.sid_numbers()
    sw_cnt            = fi.switch_count()
    ipv4_lst          = fi.ipv4_list()
    #ipv4_fcr          = fi.ipv4_plus_fcr_list('root','password')  
    fab_name          = fi.name()
    fab_all           = fi.all_info()
    fab_memb          = fi.fabric_members()
    fab_zone          = fi.zone_info()
    

    ####  FCIP info
    
    fc = anturlar.FcipInfo()
    fc_ge_ports        = fc.all_online_ge_ports()
    fc_ge_ports_dble   = fc.all_ge_port_disabled()
    fc_vex_ports       = fc.vex_ports()
    fc_ex_ports        = fc.ex_ports()
    fc_ge_ports        = fc.ge_ports()
    
    










































