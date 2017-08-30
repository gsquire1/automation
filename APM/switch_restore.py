#!/usr/bin/env python3


###############################################################################
####
####  net install a switch of any 
####
###############################################################################

import os,sys

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')

import getpass
import argparse

import liabhar
import anturlar


def main():


    my_ip = "10.38.37.50"
    user_name = "root"
    psswd = "pass"
    
    
    cons_out = anturlar.login()

    cons_out = anturlar.fos_cmd("")
    cons_out = anturlar.clear_stats()
    cons_out = anturlar.fos_cmd("switchshow")
    
    print(cons_out)
    
    
    

#################################################################################
#################################################################################
#### test the SWICH INFO CLASS
##

    si = anturlar.SwitchInfo()
        
    print(si)
    
    cons_out = anturlar.close_tel()
    
main()
