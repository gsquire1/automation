#!/usr/bin/env python


import datetime
import sys
import anturlar
import re

"""
cofra is cabinet
"""
 
def bladeportmap_Info(blade = 0):
    capture_cmd = anturlar.fos_cmd("bladeportmap %s " % blade)
 
    ras = re.compile('ENB\s(\d+)\s+([-\d]+)\s+([-\d]+)\s+(\d+)\s+(\d+)')
    ras = ras.findall(capture_cmd)
    
    
    return(ras)

 
 