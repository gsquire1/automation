#!/usr/bin/env python3


import datetime
import sys
import anturlar
import re

"""
cofra is cabinet
"""
 
def bladeportmap_Info(blade = 0):
    """
    bladeportmap_Info
    
    """
    capture_cmd = anturlar.fos_cmd("bladeportmap %s " % blade)
 
    ras = re.compile('ENB\s(\d+)\s+([-\d]+)\s+([-\d]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-\d]+)\s+(\d+)\s+([CONDOR324]+)\s+([:_/A-Za-z0-9]+)')
    ras = ras.findall(capture_cmd)
    
    
    return(ras)
###############################################################################


def PortStats(counter="all", port_list = "all"):
    """
    PortStats Values
        los         --  Loss of Sync 
        lol         --  Link Failure
        losig       --  Loss of Signal
        swtxto      --  switch tx timeout
        swrxto      --  switch rx timeout
        proto       --  protocal error
        crc         --  crc with g_eof
        lrout       --  link reset out
        lrin        --  link reset in
        encout      --  encoding out error
        encin       --  encoding in error
        c3to        --  c3 timeout discard
        pcserr      --  pcs error ( ITW errors )
        statechange --  statechange
        txcrd_zero  --  Port TX credit zero
        
        A list of all the Port Stats Values will be return by default
        or the counter value can be passed from the list above
        the port_list will return all ports unless pass 
        
    """
    
    #### set the list of counters to get for each port
    if "all" in counter:
        counter_list = ['los', 'lol', 'losig', 'swtxto', 'swrxto', 'proto',\
                        'crc', 'lrout', 'lrin', 'encout', 'encin',\
                        'c3to', 'pcserr', 'statechange' ]
    else:
        counter_list = counter
        
    port_list = 2
    counter_list_capture = []
    
    los_count        = ["los"]
    lol_count        = ["lol"]
    losig_count      = ["losig"]
    c3to_tx_count    = ['swtxto']
    c3to_rx_count    = ['swrxto']
    c3_discard_count = ['c3to']
    proto_count      = ['proto']
    crc_geof_count   = ['crc']
    lr_out_count     = ['lrout']
    lr_in_count      = ['lrin']
    enc_out_count    = ['encout']
    enc_in_count     = ['encin']
    pcserr_count     = ['pcserr']
    st_change_count  = ['statechange']

    #### send the command portshow and capture the data for each counter
    ####
    capture_cmd = anturlar.fos_cmd("portshow %s " % port_list)
    
    ras_intr_link_fail    = re.compile('Interrupts:\s+(\d+)\s+Link_failure:\s+(\d+)')
    ras_intr_link_fail    = ras_intr_link_fail.findall(capture_cmd)
    ras_unknown_loss_sync = re.compile('Unknown:\s+(\d+)\s+Loss_of_sync:\s+(\d+)')
    ras_unknown_loss_sync = ras_unknown_loss_sync.findall(capture_cmd)
    ras_Lli_loss_signal   = re.compile('Lli:\s+(\d+)\s+Loss_of_sig:\s+(\d+)')
    ras_Lli_loss_signal   = ras_Lli_loss_signal.findall(capture_cmd)
    ras_proc_protoc_err   = re.compile('Proc_rqrd:\s+(\d+)\s+Protocol_err:\s+(\d+)')
    ras_proc_protoc_err   = ras_proc_protoc_err.findall(capture_cmd)
    ras_Suspend_lr_out    = re.compile('Suspended:\s+(\d+)\s+Lr_out:\s+(\d+)')
    ras_Suspend_lr_out    = ras_Suspend_lr_out.findall(capture_cmd)
    ras_Overrun_lr_in     = re.compile('Overrun:\s+(\d+)\s+Lr_in:\s+(\d+)')
    ras_Overrun_lr_in     = ras_Overrun_lr_in.findall(capture_cmd)
    ras_state_change      = re.compile('state transition count:\s+(\d+)')
    ras_state_change      = ras_state_change.findall(capture_cmd)
    
    
    #### send the command porterrshow and capture the data for each counter
    #### 
    caputre_porterrshow = anturlar.fos_cmd("porterrshow %s | grep :" % port_list)
    ras_porterrshow = re.compile('\s*\d+:\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)')
    ras_porterrshow = ras_porterrshow.findall(caputre_porterrshow)
        
    
    for i in counter_list:
        
        print("\nvalue of i is  %s " % i)      
        #### start of portshow command 
        
        if i == 'lol' :
            los_count.append(ras_intr_link_fail[0][1])
            counter_list_capture.append(los_count)

        elif i == 'los':
            lol_count.append(ras_unknown_loss_sync[0][1])
            counter_list_capture.append(lol_count)

        elif i == 'losig':
            losig_count.append(ras_Lli_loss_signal[0][1])
            counter_list_capture.append(losig_count)
                
        elif i in 'proto':
            proto_count.append(ras_proc_protoc_err[0][1])
            counter_list_capture.append(proto_count)           
            
        elif i in "lrout":
            lr_out_count.append(ras_Suspend_lr_out[0][1])
            counter_list_capture.append(lr_out_count)
            
        elif i in "lrin":
            lr_in_count.append(ras_Overrun_lr_in[0][1])
            counter_list_capture.append(lr_in_count)
            
        elif i =='statechange':
            st_change_count.append(ras_state_change[0])
            counter_list_capture.append(st_change_count)
        
        ####  start of porterrshow command
        
        elif i == 'crc':
            crc_geof_count.append(ras_porterrshow[0][4])
            counter_list_capture.append(crc_geof_count)
        
        elif i == 'swtxto':
            c3to_tx_count.append(ras_porterrshow[0][15])
            counter_list_capture.append(c3to_tx_count)
        
        elif i == 'swrxto':
            c3to_rx_count.append(ras_porterrshow[0][16])
            counter_list_capture.append(c3to_rx_count)
            
        elif i == 'c3to':
            c3_discard_count.append(ras_porterrshow[0][9])
            counter_list_capture.append(c3_discard_count)
        
        elif i in 'encin':
            enc_in_count.append(ras_porterrshow[0][2])
            counter_list_capture.append(enc_in_count)
            
        elif i in 'encout':
            enc_out_count.append(ras_porterrshow[0][8])
            counter_list_capture.append(enc_out_count)
        
        elif i in 'pcserr':
            pcserr_count.append(ras_porterrshow[0][17])
            counter_list_capture.append(pcserr_count)
        
        else:
            pass
            
    return(counter_list_capture)
###############################################################################

