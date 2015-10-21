#!/usr/bin/env python3

 
###############################################################################
####  Flow Vision tool box
####    home location is /home/automation/lib/MAPS/
####
###############################################################################

import anturlar
import liabhar
import random


def flowcommand_list(options = "0"):
    """
        returns a list fo the flow Vision commands
        send true to recieve the list of options for each command
        pass the options of 0 , usage or all
        0 - or blank will use the core commands only
        usage - will use commands that will return the help list
        all   - will use commands that will function correctly
        
    """
    l = "flow"

    if options == "usage":
        
        l = ["flow --create , \
              flow --sh, \
              flow --create, \
              flow --delete,\
              flow --control, \
              flow --reset, \
              flow --activate, \
              flow --deactivate, \
              flow --show aa, \
              flow --help,\
             ",\
            ]

    if options == "all":

        l = ["flow --create test_flow -fea mon -ingrport 20 -srcdev '*' -dstdev '*' " ,\
             "flow --delete test_flow -fea mon" ,\
             "flow --control -deviceIdMode wwn" ,\
             "flow --control -deviceIdMode pid" ,\
             "flow --control -portIdMode slotport" ,\
             "flow --control -portIdMode index" ,\
             "flow --create test_flow -fea gen,mon -ingrport 20 -srcdev '*' -dstdev '*' " ,\
             "flow --control test_flow -feature gen -size 64 -pattern 'abcd'" ,\
             "flow --control -feature mir -disable_wrap" ,\
             "flow --control -feature mir -enable_wrap" ,\
             "flow --reset test_flow -fea gen" ,\
             "flow --reset test_flow -fea mon" ,\
             "flow --reset test_flow -fea all" ,\
             "flow --deact test_flow -fea all" ,\
             "flow --act test_flow -fea all" ,\
             "flow --show all " ,\
             "flow --show " ,\
             "flow --delete all" ,\
             "flow --show " ,\
             ]

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
    f = anturlar.FabricInfo(fid_now)
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
        #combine_port_list = liabhar.randomList(combine_port_list)
        random.shuffle(combine_port_list)
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
    
def delete_flow( name ):
    """
        delete flow vision flows from a switch
        
    """
    
    if name == "all":
        cons_out = anturlar.fos_cmd("echo Y | flow --delete all ")
    else:
        cons_out = anturlar.fos_cmd("flow --delete %s" % name)
    
    
def add_flows_count(fname, scr, dst, ingrp, egrp, feat, cnt):
    
    count = 0
    while count <= cnt:
        fn = "%s_%s" % (fname,count)
        add_flow(fn, scr, dst, ingrp, egrp, feat)
        count += 1
    
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
    


def flow_all_switch():
    """
        capture all the flow --show information
        this can go to in the FlowV class
        
    """
    
    
def remove_sim():
    """
    remove any SIM ports enabled on the switch
    
    """
    
    
    pass
    
    
def end():
    pass