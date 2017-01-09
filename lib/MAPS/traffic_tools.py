#!/usr/bin/env python3


###############################################################################
#### Home location is
####
###############################################################################
import sys
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

def bcu_version():
    
    ###########################################################################
    ####
    ####
    ####
    db_level = 9
    ras = re.compile('\s\d\s+\d\s+([:\d\w]{5,10})')
    
    cmdout = anturlar.traff_cmd("bcu adapter --list", db_level)
    ad = ras.findall(cmdout)
    ad_one = ad[0]
    print("\n\n\n\n\n\n\n\n\n\n")
    print(ad_one)
    
    
    ras = re.compile('\s+fw version:\s+([\.\d\w]{7})')
    cmdout = anturlar.traff_cmd("bcu adapter --query %s " % ad_one)
    ras = ras.findall(cmdout)
    
    return(ras)
  

    
def start_linux_pre_3_2(h, start_cmd):
    """
       the command is passed into this procedure and the drive letters are added to the command
       if there are Clariion devices the LUNZ devices are skipped
       
    
    """
    
    db_level = 9
    remote_list = []
    start_pain = start_cmd
    ###################################################################################################################
    #### use catapult to capture the  drives and and Volumn ID  -- use this if they are Clariion to not add
    ####     the drives with LUNZ Volumn ID  since they are not target IDs
    ####
    cmdout = anturlar.traff_cmd("catapult -p")
    ras = re.compile('[ \d]+/dev/sd([a-z]+)\s+[:0-9]+\s+[A-Z]+\s+([A-Z]+)')
    remove_lunz = ras.findall(cmdout)
        
    for i in [4,2,3,1]:
        
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/0" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu rport --osname %s/0" % i , db_level )
        ras = re.compile('/dev/sd([a-z]+)')
        ras = ras.findall(cmdout)
        
        print("ras"*30)
        print(ras)
        print(remove_lunz)
        print(remote_list)
        
        print("ras"*30)
        
        for r in ras:
            for lunz in remove_lunz:
                print(r)
                print(lunz[0])
                print(lunz[1])  
                
                if lunz[0] == r and lunz[1] != "LUNZ":
     
                    if r not in remote_list:
                        remote_list += [r] 
                  
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/1" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu rport --osname %s/1" % i , db_level )
        ras = re.compile('/dev/sd([a-z]+)')
        ras = ras.findall(cmdout)
        
        for r in ras:
            for lunz in remove_lunz:
        
            
                if lunz[0] == r and lunz[1] != "LUNZ":
             
                    if r not in remote_list:
                        remote_list += [r] 
 
    
    print("remote port list  :  %s  " % remote_list )
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    ####  put the list is the correct syntax by adding comma
    new_list = ",".join(remote_list)
        
    print("NEW LIST IS   :   %s " % new_list)
    print("#"*80)
    
    #### combine the command with the drive list
    start_pain_sd = start_pain + ' -f"/dev/sd;%s"' % new_list
    print("NEWEST COMMAND  %s   " % start_pain_sd)
    reg_list = [b'([\w\d]+)']
    cmdout = anturlar.fos_cmd_regex(start_pain_sd , reg_list,9)
    cmdout = anturlar.traff_output(9)
    
    anturlar.close_tel()    


def start_linux_post_3_2(h, start_cmd):
    
    db_level = 9
    remote_list = []
    start_pain = start_cmd
         ###################################################################################################################
    #### use catapult to capture the  drives and and Volumn ID  -- use this if they are Clariion to not add
    ####     the drives with LUNZ Volumn ID  since they are not target IDs
    ####
    cmdout = anturlar.traff_cmd("catapult -p")
    ras = re.compile('[ \d]+/dev/sd([a-z]+)\s+[:0-9]+\s+[A-Z]+\s+([A-Z]+)')
    remove_lunz = ras.findall(cmdout)
    
    for i in [1,2,3,4]:
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/0" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu fcpim --lunlist %s/0" % i , db_level )
        ras = re.compile('/dev/sd([a-z]+)')
        ras = ras.findall(cmdout)
    
        print("ras"*30)
        print(ras)
        print(remove_lunz)
        print(remote_list)
        
        print("ras"*30)
        
        for r in ras:
            for lunz in remove_lunz:
                print(r)
                print(lunz[0])
                print(lunz[1])  
                
                if lunz[0] == r and lunz[1] != "LUNZ":
     
                    if r not in remote_list:
                        remote_list += [r]    
        
        
        
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/1" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu fcpim --lunlist %s/1" % i , db_level )
        ras = re.compile('/dev/sd([a-z]+)')
        ras = ras.findall(cmdout)
        remote_list = remote_list + ras
    
    
        for r in ras:
            for lunz in remove_lunz:
        
            
                if lunz[0] == r and lunz[1] != "LUNZ":
             
                    if r not in remote_list:
                        remote_list += [r] 
     
    print("remote port list  :  %s  " % remote_list )
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    ####  put the list is the correct syntax
    new_list = ",".join(remote_list)
        
    print("NEW LIST IS   :   %s " % new_list)
    
    #### combine the command with the drive list
    start_pain_sd = start_pain + ' -f"/dev/sd;%s"' % new_list
    print("NEWEST COMMAND  %s   " % start_pain_sd)
    reg_list = [b'([\w\d]+)']
    cmdout = anturlar.fos_cmd_regex(start_pain_sd , reg_list)
    cmdout = anturlar.traff_output()
    
    anturlar.close_tel()
    
  
  
def start_windows_pre_3_2(h, start_cmd):
    
    db_level = 9
    remote_list = []
    start_pain = start_cmd
    
    for i in [1,2,3,4]:
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/0" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu rport --osname %s/0" % i , db_level )
        ras = re.compile('rive([0-9]+)')
        ras = ras.findall(cmdout)
        
        print("ras"*30)
        print(ras)
        print(remove_lunz)
        print(remote_list)
        
        print("ras"*30)
        
        for r in ras:
            for lunz in remove_lunz:
                print(r)
                print(lunz[0])
                print(lunz[1])  
                
                if lunz[0] == r and lunz[1] != "LUNZ":
     
                    if r not in remote_list:
                        remote_list += [r] 
        
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/1" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu rport --osname %s/1" % i , db_level )
        ras = re.compile('rive([0-9]+)')
        ras = ras.findall(cmdout)
      
        for r in ras:
            for lunz in remove_lunz:
        
            
                if lunz[0] == r and lunz[1] != "LUNZ":
             
                    if r not in remote_list:
                        remote_list += [r] 
 
    
    print("remote port list  :  %s  " % remote_list )
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    ####  put the list is the correct syntax
    new_list = ",".join(remote_list)
        
    print("NEW LIST IS   :   %s " % new_list)
    
    #### combine the command with the drive list
    start_pain_sd = start_pain + ' -f"\\\.\PhysicalDrive;%s"' % new_list
    print("NEWEST COMMAND  %s   " % start_pain_sd)
    reg_list = [b'([\w\d]+)']
    cmdout = anturlar.fos_cmd_regex(start_pain_sd , reg_list)
    cmdout = anturlar.traff_output()
    
    anturlar.close_tel()    
    
  
    
def start_windows_post_3_2(h, start_cmd):
    
    db_level = 9
    remote_list = []
    start_pain = start_cmd
    
    
    for i in [1,2,3,4]:
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/0" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu fcpim --lunlist %s/0" % i , db_level )
        ras = re.compile('rive([0-9]+)')
        ras = ras.findall(cmdout)

        print("ras"*30)
        print(ras)
        print(remove_lunz)
        print(remote_list)
        
        print("ras"*30)
        
        for r in ras:
            for lunz in remove_lunz:
                print(r)
                print(lunz[0])
                print(lunz[1])  
                
                if lunz[0] == r and lunz[1] != "LUNZ":
     
                    if r not in remote_list:
                        remote_list += [r]  
        
        
        cmdout = anturlar.traff_cmd("bcu port --statsclr %s/1" % i, db_level)
        cmdout = anturlar.traff_cmd("bcu fcpim --lunlist %s/1" % i , db_level )
        ras = re.compile('rive([0-9]{1,3})')
        ras = ras.findall(cmdout)

    
        for r in ras:
            for lunz in remove_lunz:
        
            
                if lunz[0] == r and lunz[1] != "LUNZ":
             
                    if r not in remote_list:
                        remote_list += [r] 
 
    
    
    
    
    print("remote port list  :  %s  " % remote_list )
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    ####  put the list is the correct syntax
    new_list = ",".join(remote_list)
        
    print("NEW LIST IS   :   %s " % new_list)
    
    #### combine the command with the drive list
    start_pain_sd = start_pain + ' -f"\\\.\PhysicalDrive;%s"\r\n' % new_list
    print("NEWEST COMMAND  %s   " % start_pain_sd)
    reg_list = [b'([.\w\d]+)']
    cmdout = anturlar.fos_cmd_regex(start_pain_sd , reg_list)
    cmdout = anturlar.traff_output()
    
    anturlar.close_tel()
    
    
    

def traff_get_port_list(ip, user, pwd, start_command, os_ver):
    
    
    #### add the variable pain_main in the command line
    ####  add option to be random traffic
    ####      random pattern    block size   etc
    ####      random drives    
    
    #start_pain = "pain -t4 -r -b8k -o -u -n -l69 -q5 "
    #start_pain = "pain -t8 -M60 -b8k -o -u -n -l69 -q5 "
    #start_pain = start_command
    
    #print("aaaaaaaaaaaaaaaaaaaaaaaa")
    #print(type(ip))
    #print(user)
    #print(pwd)
    #print("aaaaaaaaaaaaaaaaaaaaaaaa")
    db_level = 9
    #remote_list = []
    
    h = anturlar.connect_tel_noparse_traffic(ip, user, pwd)
    cmdout = anturlar.traff_cmd("" , db_level )
    cmdout = anturlar.traff_cmd("cd c:\traffic" , db_level )
    
    this_platform = os_ver
    #this_platform = liabhar.platform()
    this_bcu_version = bcu_version()
    
    print("\n\nPLATFORM IS        :   %s  " % this_platform)
    print("ADAPTER HW-PATH    :   %s  " % this_bcu_version)
    
    
    if "windows" in this_platform:
        if "3.2" in this_bcu_version[0] :
            print("START POST windows  ")
            #cmdout = anturlar.traff_cmd("catapult -p -t" , db_level )
            #cmdout = anturlar.traff_cmd("cd sqa\t" , db_level )
            
            start_windows_post_3_2(h, start_command)
        else:
            print("START PRe windows")
            #sys.exit()
            start_windows_pre_3_2(h, start_command)
        
    elif "linux" in this_platform:
        if "3.2" in this_bcu_version[0]:
            print("START POST linux ")
            #sys.exit()
            start_linux_post_3_2(h, start_command)
        else:
            print("START PRE linux")
            #sys.exit()
            start_linux_pre_3_2(h, start_command)
        
    else:
        print("not sure of the platform") 
    
    
    
    ####  windows style
    ####  windows with 3.2 driver
    ####
    #### linux style
    #### linux style with 3.2 driver
    ####
    #### add the other type of os version to the remote os ver function
     
    
    
    
    
    
    
    
    
    
    
    
    
    
