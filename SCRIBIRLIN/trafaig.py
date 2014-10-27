#!/usr/bin/env python3

###############################################################################
####
####   Start Traffic
####
###############################################################################


###############################################################################
####   Import system modules here                                          ####
###############################################################################

import os,sys

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
#sys.path.append('/home/automation/lib/FCR')
#sys.path.append('/home/automation/APM')
#sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')


###############################################################################
####   Import user modules here and set system paths                       ####
###############################################################################
import liabhar
#import anturlar
#import cofra
###############################################################################
####   Import test case modules here                                       ####
###############################################################################

import traffic_tools

###############################################################################
####  Get the traffic info to start 
###############################################################################

def get_switch_info():
    
###############################################################################
#### read the csv file to get the switch info
####  return the ip, username and password 
###############################################################################
    
    pass




def main():
    
    my_ip = "10.38.39.43"
    user_name = "root"
    psswd = "pass"

    this_platform = liabhar.platform()

    print("PLATFORM IS  :  %s  " % this_platform)

    traffic_tools.traff_get_port_list(my_ip, user_name, psswd)

 
 

main()