#!/opt/python3/bin/python3



###############################################################################
####
####  Get switch config info and place in a file that
####  can be used later to rebuild the switch to the same configuration.
####  Options are single switch, entire fabric, entire fcr fabric and everything in
####  switch matrix file
####
###############################################################################

import os,sys

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')

import telnetlib
import getpass
import ipaddress
import argparse
import re
import anturlar
import liabhar
import cofra
import csv
import time

###############################################################################
####
####  switch types
####
####  62  DCX
####  64  5300
####  66  5100
####  67  Encryption switch
####  70  5410 - embedded switch
####  71  300
####  72  5480 - embedded switch
####  73  5470 - embedded switch
####  75  M5424 - embedded switch
####  77  DCX-4S
####  83  7800
####  86  5450 - embedded switch
####  87  5460 - embedded switch
####  92  VA-40FC
####  109  6510
####  117  6547  - embedded switch
####  118  6505
####  120  DCX 8510-8
####  121  DCX 8510-4
####  124  5430  - embedded switch
####  125  5431
####  129  6548  - embedded switch
####  130  M6505  - embedded switch
####  133  6520 - odin
####  134  5432  - embedded switch
####  
####  141  Yoda DCX
####  142  Yoda pluto
####  148  Skybolt
####
###############################################################################


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    #pp.add_argument("--repeat", help="repeat repeat")
    #pp.add_argument('ip', help="IP address of SUT")
    #pp.add_argument("user", help="username for SUT")
    #pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
    #pp.add_argument('-iter', '--iterations', type=int, default = 1, help="Number of iterations to run")

    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp 

def parse_args(args):
    
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    parser.add_argument('ip', help="IP address of target switch")   
    #parser.add_argument('firmware', help='firmware verison 8.1.0_bldxx')
    parser.add_argument('frmup', help='firmware to go to 8.1.0_bldxx')
    parser.add_argument('frmdwn', help='firmware to come from 8.1.0_bldxx')
    parser.add_argument('-t', '--time', type=int, default=None, help="Time between interations in seconds")
    parser.add_argument('-csv', '--csvall', action="store_true", help="Gets all Switch IPs from SwitchMatrix file")    
    #parser.add_argument('-a', '--all', action="store_true", help="Gets all Switch IPs from SwitchMatrix file")
    parser.add_argument('-fab', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c', '--chassis_name', help="Chassis Name in the SwitchMatrix file")
    #parser.add_argument('-ip', '--ipaddr', type=list, help="IP address of target switch")
    parser.add_argument('-fcr', '--fcrwide', action="store_true", help="Execute fabric wide incluiding edge switches")
    #parser.add_argument('-to', '--tofirmvrsn', type=str, default=None, help="firmware Revision to go to")
    #parser.add_argument('-to', '--tofirmvrsn', action="store_true", help="firmware Revision to go to")
    #parser.add_argument('-s', '--suite', type=str, help="Suite file name")
    #parser.add_argument('-p', '--password', help="password")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    #group.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")
    
    
    args = parser.parse_args()
    print(args)
    #sys.exit()
    
    if not args.chassis_name and not args.ip:
        print("Chassis Name or IP address is required")
        sys.exit()
        
            
    #if args.cmdprompt and not args.switchtype:
    #    print("To start at the command prompt the switch type is needed.")
    #    sys.exit()
    #    
    #if not args.cmdprompt and args.switchtype:
    #    print('To start at the command prompt both switch type and command prompt is requried')
    #    sys.exit()


    return parser.parse_args()

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
        #capture_cmd = anturlar.fos_cmd("version")
        #f = cofra.DoFirmwaredownloadChoice(frmdwn,frmup, email)
        #print("value of f is :  ")
        #print(f)
        #
        #if "failed" in f:
        #    sys.exit()
        
         
        #liabhar.count_down(600)
        
        anturlar.connect_tel_noparse(myip, 'root', 'password')
        #en = anturlar.SwitchInfo()
        capture_cmd = anturlar.fos_cmd("version")
        
        f = DoFirmwaredownloadChoice(frmdwn, frmup, email)
        #liabhar.count_down(600)    
        anturlar.connect_tel_noparse(myip, 'root', 'password')
        #en = anturlar.SwitchInfo( )
        print ("++++++++++++++++++++ OUT OF firmwaredownload +++++++++++++++++++++++++++")

    return(0)

class DoFirmwaredownloadChoice():
    """
        do a firmware download to one of the builds in the ini file
        depending on what is already on the switch
        
    """
    
    def __init__(self, firmdown, firmup, email):
        self.firmdown = firmdown
        self.firmup = firmup
        self.email = email
        #ras = re.compile('([\.a-z0-9]+)(?:_)')
        ras = re.compile('([\.a-z0-9]{6})')
        ras = ras.search(firmdown)
        frm_no_bld_down = ras.group(1)
        
        #ras_up = re.compile('([\.a-z0-9]+)(?:_)')
        ras_up = re.compile('([\.a-z0-9]{6})')
        ras_up = ras_up.search(firmup)
        frm_no_bld_up   = ras_up.group(1)
        
        if 'amp' in firmdown:
            frm_no_bld_down = frm_no_bld_down + '_amp'
        self.firmdown_folder = frm_no_bld_down   
        if 'amp' in firmup:
            frm_no_bld_up = frm_no_bld_up + '_amp'
        self.firmup_folder = frm_no_bld_up
        
        #self.check_version()
        
        self.start()
        
    
    def check_status(self):
        capture_cmd = anturlar.fos_cmd("firmwaredownloadstatus")
        if "firmware versions" in capture_cmd:
            return(True)
        else:
            liabhar.count_down(30)
            self.check_status()
               
    def check_version(self):
         
        capture_cmd = anturlar.fos_cmd("firmwareshow") 
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+[\\r\\n]*\s+([\._a-z0-9]{6,18})')
        ras = ras.search(capture_cmd)
        ras_dir = ras_dir.search(capture_cmd)
        
        f=""
        capture_cmd = anturlar.fos_cmd("hashow")
        print(capture_cmd)
        if "hashow: Not supported" in capture_cmd:
            f = ras.group(1)
        else:
            f = ras_dir.group(1)
        
        
        #print("switch RAS is :  %s  " % ras.group(1))
        #print("director RAS is  : %s " % ras_dir.group(1))
        
        #try:
        #    if ras_dir(0) != "none":
        #        f=ras_dir.group(1)
        #except:
        #    pass
  
        return(f)
          
    def eml_mssg(self):
        """
        """
        ss = anturlar.SwitchInfo()
        my_ip    = ss.ipaddress()
        my_name  = ss.chassisname()
        my_name  = str(my_name[0])
        
        msg_html = """\
        <p>
        Firmwaredownload has Started      
        ================================================================
        Switch IP Address                   :      replace_ip  
        Switch Name                         :      replace_name 
        Firmware Version downloading        :      replace_firm_up 
        Firmware Version Next               :      replace_firm_next 
       </p>
        
        """
        
        msg_html = msg_html.replace("replace_ip", my_ip)
        msg_html = msg_html.replace("replace_name", my_name)
        msg_html = msg_html.replace("replace_firm_up", self.firmdown)
        msg_html = msg_html.replace("replace_firm_next", self.firmup)
        
        
        return(msg_html)
        
        
        
    def start(self):
        ras = self.check_version()
        email = self.email
        download_success = False
        print("\n\nFIRMUP IS %s\n"%(self.firmup))
        print("RAS IS     %s\n"%(ras))
        
        #ss = anturlar.SwitchInfo()
        #my_ip    = ss.ipaddress()
        #my_name  = ss.chassisname()
        mmsg = self.eml_mssg()
        #mmsg = "Firmwaredownload has started on \n%s  \n%s  \n\n\n" % (my_ip, my_name)
        
        if ras != self.firmup:
            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/%s/%s,fwdlacct"%(self.firmup_folder, self.firmup)
        else:
            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/%s/%s,fwdlacct"%(self.firmdown_folder, self.firmdown)
        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.', \
                       b'with new firmware', b'Firmware has been downloaded']
        
        #capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
        print("\n\nstart firmwaredownload")
        capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list, 9)
        
        if "Y]:" in capture_own_regex:
            
            print("\n\n\nsending yes \n\n\n\n")
            capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list, 9)
            download_success = True
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            #print(capture_cmd)
            print("END OF SEND Y \n\n\n\n\n\n")
            anturlar.close_tel()
            

            ####liabhar.email_sender_html("smckie@brocade.com,gsquire@brocade.com", "smckie@brocade.com", "Started Firmware Download ", "%s  to  %s"%(self.firmdown, self.firmup))        
            
            liabhar.email_sender_html(email, email, "Started Firmware Download ", mmsg)        
            
            #liabhar.count_down(1800)
            liabhar.count_down(700)
            return(capture_cmd)
        
        #### does  capture_cmd include ha rebooting ???
        #if "HA Rebooting" in capture_cmd:
        #    print("\n\n\n")
        #    return(capture_cmd)
        #
        #if "with new firmware" in capture_cmd:
        #    return(capture_cmd)
        #
        #if "Firmware has been downloaded" in capture_cmd:
        #    return(capture_cmd)

        #######################################################################   
        #######################################################################
        ####
        #### port decommission  -- need to delete decom action in all FIDS
        ####         -- mapsconfig --actions raslog,email
        #### FPI monitor        -- need to disable FPI monitor in all FIDS
        ####         -- mapsconfig --disableFPImon
        #### discard frame logging --
        ####         -- framelog --disable -type du  and -type unroute
        #### SIM ports configured --
        ####         -- flow --control -simport [port] -disable 
        ####
        
        ####
        ####  if "root>" in capture_cmd_regex:
        ####
        capture_cmd = anturlar.fos_cmd("lscfg --show", 9)
        ras = re.compile('(\d{1,3})(?=\()')  
        ls_all = ras.findall(capture_cmd)
        
        message_check = ""
        if "the same firmware" in capture_own_regex:
            message_check = "Firmwaredownload failed"
        if "server is inaccessible" in capture_own_regex:
            message_check = "Firmwaredownload failed"
        
        if "Downgrade is not allowed" in capture_own_regex:
            pass
            #message_check = "failed"
        if "Firmwaredownload is already running" in capture_own_regex:
            pass
        if "Sanity check failed because system is non-redundant" in capture_own_regex:
            pass
        
        
        if "port decommission" in capture_own_regex:
            for l in ls_all:
                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
                capture_cmd = anturlar.fos_cmd("mapsconfig --actions raslog,email")
        
        if "FPI Monitor" in capture_own_regex:
            for l in ls_all:
                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
                capture_cmd = anturlar.fos_cmd("mapsconfig --disableFPImon")
            
        if "discard frame logging" in capture_own_regex:
            for l in ls_all:
                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
                capture_cmd = anturlar.fos_cmd("framelog --disable -type du")
                capture_cmd = anturlar.fos_cmd("framelog --disable -type unroute")
             
        if "SIM ports configured" in capture_own_regex:
            en = anturlar.SwitchInfo()
            #port_list = en.sim_ports()
            
            for l in ls_all:
                anturlar.fos_cmd("setcontext %s " % l)
                port_list = en.sim_ports()
                anturlar.fos_cmd("flow --control -portIdMode slotport")
                print("port list is \n")
                print(port_list)
                
                for p in port_list:
                    capture_cmd = anturlar.fos_cmd("flow --control -simport %s/%s -disable" % (p[0],p[1]) )
            
                anturlar.fos_cmd("flow --control -portIdMode index")
            #capture_cmd = anturlar.fos_cmd_regex("N", reg_ex_list)
            #message_check = "Firmwaredownload failed"
        
        ##if "SIM ports configured" in capture_own_regex:
        ##    message_check = "Firmwaredownload failed"
        
        if "Brocade FC16-64 blades" in capture_own_regex:
            message_check = "failed"
        
        mmsg = "%s "% (capture_own_regex)
        #liabhar.email_sender_html(email, "smckie@brocade.com", "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
        liabhar.email_sender_html(email, email, "Firmware Download Failed ", " %s  %s <br><br> \
                                  Console capture at time of Failure   <br><hr> %s "%(self.firmup, self.firmdown, mmsg))
        
        if "failed" in message_check:
            print("\n\ndo you want to stop the test ?")
            print(message_check)
            print("STOP"*20)
            print("STOP"*20)
            sys.exit()
            #return(message_check)
        if "failed" in capture_own_regex:
            print("\n\ndo you want to stop the test ?")
            print(capture_own_regex)
            print("\n"*4)
            print("STOP"*20)
            print("STOP"*20)
            sys.exit()
            #return(message_check)
        print("\n"*4)
        print("FAIL____"*10)
        print(message_check)
        print("FAIL____"*10)
        print(capture_own_regex)
        print("FAIL____"*10)
        
        liabhar.count_down(20)
        capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list)
        #anturlar.close_tel()
        mmsg = "%s "% (capture_own_regex)
        liabhar.email_sender_html(email, email, "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
        liabhar.email_sender_html(email, email, "Started Firmware Download ", " %s "%(mmsg))
        print("exit now")
        sys.exit()
        
        liabhar.count_down(1800) 
        return(capture_cmd)
###############################################################################

#class doFirmwareDownload():
#    """
#        do a firmware download to 7.3.0 build of  firmware
#        then close the telnet connection and
#        wait 1200 seconds before closing ending the function
#        Return could be
#                1. a message that firmware version are the same
#                2. server is inaccessible
#                3. the user prompt after firmware download is started
#    """
#    def __init__(self, firmvrsn, firmdown, firmup ):
#        self.firmdown = firmdown
#        self.firmup = firmup
#        self.firmvrsn = firmvrsn
#        self.start()
#    
#    def check_status(self):
#        capture_cmd = anturlar.fos_cmd("firmwaredownloadstatus")
#        if "firmware versions" in capture_cmd:
#            return(True)
#        else:
#            liabhar.count_down(30)
#            self.check_status()
#            
#    def check_version(self):
#         
#        capture_cmd = anturlar.fos_cmd("firmwareshow") 
#        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
#        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
#        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+\\r\\n\s+([\._a-z0-9]{6,18})')
#        ras = ras.search(capture_cmd)
#        ras_dir = ras_dir.search(capture_cmd)
#        f=""
#        try:
#            if ras.group(0) != "none":
#                f= ras.group(1)
#        except:
#            pass
#        try:
#            if ras_dir(0) != "none":
#                f=ras_dir.group(1)
#        except:
#            pass
#        
#        return(f)
#
#    #def start(self):
#    #    ras = self.check_version()
#    #    #print("FIRMUP IS %s\n"%(self.firmup))
#    #    #print("RAS IS     %s\n"%(ras))
#    #    if ras != self.firmvrsn:
#    #        #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.4.0/%s,fwdlacct"%(self.firmvrsn)
#    #        firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.4.0/%s,fwdlacct"%(self.firmvrsn)
#    #    else:
#    #        return "fail to perform Firmwaredownload since versions were the same"
#    #        #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
#    #    reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.']
#    #    capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
#    #    if "the same firmware" in capture_own_regex:
#    #        return(capture_own_regex)
#    #    if "server is inaccessible" in capture_own_regex:
#    #        return(capture_own_regex)
#    #    
#    #    capture_cmd = anturlar.fos_cmd("Y")
#    #    anturlar.close_tel()
#    #    liabhar.email_sender_html("smckie@brocade.com", "gsquire@brocade.com", "Started Firmware Download ", "%s"%(self.firmvrsn))
#    #    liabhar.count_down(360) 
#    #    return(capture_cmd)
#    
#    def start(self):
#        ras = self.check_version()
#        download_success = False
#        print("\n\nFIRMUP IS %s\n"%(self.firmup))
#        print("RAS IS     %s\n"%(ras))
#        if ras != self.firmup:
#            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
#            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/%s/%s,fwdlacct"%(self.firmup_folder, self.firmup)
#        else:
#            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
#            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/%s/%s,fwdlacct"%(self.firmdown_folder, self.firmdown)
#        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.', \
#                       b'with new firmware', b'Firmware has been downloaded']
#        
#        #capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
#        print("\n\nstart firmwaredownload")
#        capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list, 9)
#        
#        if "Y]:" in capture_own_regex:
#            
#            print("\n\n\nsending yes \n\n\n\n")
#            capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list, 9)
#            download_success = True
#            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#            #print(capture_cmd)
#            print("END OF SEND Y \n\n\n\n\n\n")
#            anturlar.close_tel()
#            liabhar.count_down(1800) 
#            return(capture_cmd)
#        
#        #### does  capture_cmd include ha rebooting ???
#        #if "HA Rebooting" in capture_cmd:
#        #    print("\n\n\n")
#        #    return(capture_cmd)
#        #
#        #if "with new firmware" in capture_cmd:
#        #    return(capture_cmd)
#        #
#        #if "Firmware has been downloaded" in capture_cmd:
#        #    return(capture_cmd)
#
#        #######################################################################   
#        #######################################################################
#        ####
#        #### port decommission  -- need to delete decom action in all FIDS
#        ####         -- mapsconfig --actions raslog,email
#        #### FPI monitor        -- need to disable FPI monitor in all FIDS
#        ####         -- mapsconfig --disableFPImon
#        #### discard frame logging --
#        ####         -- framelog --disable -type du  and -type unroute
#        #### SIM ports configured --
#        ####         -- flow --control -simport [port] -disable 
#        ####
#        
#        ####
#        ####  if "root>" in capture_cmd_regex:
#        ####
#        capture_cmd = anturlar.fos_cmd("lscfg --show", 9)
#        ras = re.compile('(\d{1,3})(?=\()')  
#        ls_all = ras.findall(capture_cmd)
#        
#        message_check = ""
#        if "the same firmware" in capture_own_regex:
#            message_check = "Firmwaredownload failed"
#        if "server is inaccessible" in capture_own_regex:
#            message_check = "Firmwaredownload failed"
#        
#        if "Downgrade is not allowed" in capture_own_regex:
#            pass
#            #message_check = "failed"
#        if "Firmwaredownload is already running" in capture_own_regex:
#            pass
#        if "Sanity check failed because system is non-redundant" in capture_own_regex:
#            pass
#        
#        
#        if "port decommission" in capture_own_regex:
#            for l in ls_all:
#                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
#                capture_cmd = anturlar.fos_cmd("mapsconfig --actions raslog,email")
#        
#        if "FPI Monitor" in capture_own_regex:
#            for l in ls_all:
#                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
#                capture_cmd = anturlar.fos_cmd("mapsconfig --disableFPImon")
#            
#        if "discard frame logging" in capture_own_regex:
#            for l in ls_all:
#                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
#                capture_cmd = anturlar.fos_cmd("framelog --disable -type du")
#                capture_cmd = anturlar.fos_cmd("framelog --disable -type unroute")
#             
#        if "SIM ports configured" in capture_own_regex:
#            en = anturlar.SwitchInfo()
#            #port_list = en.sim_ports()
#            
#            for l in ls_all:
#                anturlar.fos_cmd("setcontext %s " % l)
#                port_list = en.sim_ports()
#                anturlar.fos_cmd("flow --control -portIdMode slotport")
#                print("port list is \n")
#                print(port_list)
#                
#                for p in port_list:
#                    capture_cmd = anturlar.fos_cmd("flow --control -simport %s/%s -disable" % (p[0],p[1]) )
#            
#                anturlar.fos_cmd("flow --control -portIdMode index")
#            #capture_cmd = anturlar.fos_cmd_regex("N", reg_ex_list)
#            #message_check = "Firmwaredownload failed"
#        
#        ##if "SIM ports configured" in capture_own_regex:
#        ##    message_check = "Firmwaredownload failed"
#        
#        if "Brocade FC16-64 blades" in capture_own_regex:
#            message_check = "failed"
#        
#        
#        
#        if "failed" in message_check:
#            print("\n\ndo you want to stop the test ?")
#            print(message_check)
#            sys.exit()
#            #return(message_check)
#        
#        liabhar.count_down(20)
#        capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list)
#        #anturlar.close_tel()
#        
#        liabhar.email_sender_html("gsquire@brocade.com", "gsquire@brocade.com", "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
#        liabhar.count_down(1800) 
#        return(capture_cmd)
################################################################################
#
#class DoFirmwaredownloadChoice():
#    """
#        do a firmware download to 7.4.x or 7.3.1 builds depending on what
#        is already on the switch
#        
#    """
#    def __init__(self, firmdown, firmup, email):
#        self.firmdown = firmdown
#        self.firmup = firmup
#        #ras = re.compile('([\.a-z0-9]+)(?:_)')
#        ras = re.compile('([\.a-z0-9]{6})')
#        ras = ras.search(firmdown)
#        frm_no_bld_down = ras.group(1)
#        
#        #ras_up = re.compile('([\.a-z0-9]+)(?:_)')
#        ras_up = re.compile('([\.a-z0-9]{6})')
#        ras_up = ras_up.search(firmup)
#        frm_no_bld_up   = ras_up.group(1)
#        
#        if 'amp' in firmdown:
#            frm_no_bld_down = frm_no_bld_down + '_amp'
#        self.firmdown_folder = frm_no_bld_down   
#        if 'amp' in firmup:
#            frm_no_bld_up = frm_no_bld_up + '_amp'
#        self.firmup_folder = frm_no_bld_up
#        
#        #self.check_version()
#        
#        self.start()
#        
#    
#    def check_status(self):
#        capture_cmd = anturlar.fos_cmd("firmwaredownloadstatus")
#        if "firmware versions" in capture_cmd:
#            return(True)
#        else:
#            liabhar.count_down(30)
#            self.check_status()
#               
#    def check_version(self):
#         
#        capture_cmd = anturlar.fos_cmd("firmwareshow") 
#        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
#        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
#        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+[\\r\\n]*\s+([\._a-z0-9]{6,18})')
#        ras = ras.search(capture_cmd)
#        ras_dir = ras_dir.search(capture_cmd)
#        
#        f=""
#        capture_cmd = anturlar.fos_cmd("hashow")
#        if "hashow: Not supported" in capture_cmd:
#            f = ras.group(1)
#        else:
#            f = ras_dir.group(1)
#        
#        
#        #print("switch RAS is :  %s  " % ras.group(1))
#        #print("director RAS is  : %s " % ras_dir.group(1))
#        
#        #try:
#        #    if ras_dir(0) != "none":
#        #        f=ras_dir.group(1)
#        #except:
#        #    pass
#  
#        return(f)
#          
#    def start(self):
#        ras = self.check_version()
#        download_success = False
#        print("\n\nFIRMUP IS %s\n"%(self.firmup))
#        print("RAS IS     %s\n"%(ras))
#        if ras != self.firmup:
#            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
#            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/%s/%s,fwdlacct"%(self.firmup_folder, self.firmup)
#        else:
#            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
#            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/%s/%s,fwdlacct"%(self.firmdown_folder, self.firmdown)
#        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.', \
#                       b'with new firmware', b'Firmware has been downloaded']
#        
#        #capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
#        print("\n\nstart firmwaredownload")
#        capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list, 9)
#        
#        if "Y]:" in capture_own_regex:
#            
#            print("\n\n\nsending yes \n\n\n\n")
#            capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list, 9)
#            download_success = True
#            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#            #print(capture_cmd)
#            print("END OF SEND Y \n\n\n\n\n\n")
#            anturlar.close_tel()
#            #liabhar.count_down(1800)
#            liabhar.count_down(700)
#            return(capture_cmd)
#        
#        #### does  capture_cmd include ha rebooting ???
#        #if "HA Rebooting" in capture_cmd:
#        #    print("\n\n\n")
#        #    return(capture_cmd)
#        #
#        #if "with new firmware" in capture_cmd:
#        #    return(capture_cmd)
#        #
#        #if "Firmware has been downloaded" in capture_cmd:
#        #    return(capture_cmd)
#
#        #######################################################################   
#        #######################################################################
#        ####
#        #### port decommission  -- need to delete decom action in all FIDS
#        ####         -- mapsconfig --actions raslog,email
#        #### FPI monitor        -- need to disable FPI monitor in all FIDS
#        ####         -- mapsconfig --disableFPImon
#        #### discard frame logging --
#        ####         -- framelog --disable -type du  and -type unroute
#        #### SIM ports configured --
#        ####         -- flow --control -simport [port] -disable 
#        ####
#        
#        ####
#        ####  if "root>" in capture_cmd_regex:
#        ####
#        capture_cmd = anturlar.fos_cmd("lscfg --show", 9)
#        ras = re.compile('(\d{1,3})(?=\()')  
#        ls_all = ras.findall(capture_cmd)
#        
#        message_check = ""
#        if "the same firmware" in capture_own_regex:
#            message_check = "Firmwaredownload failed"
#        if "server is inaccessible" in capture_own_regex:
#            message_check = "Firmwaredownload failed"
#        
#        if "Downgrade is not allowed" in capture_own_regex:
#            pass
#            #message_check = "failed"
#        if "Firmwaredownload is already running" in capture_own_regex:
#            pass
#        if "Sanity check failed because system is non-redundant" in capture_own_regex:
#            pass
#        
#        
#        if "port decommission" in capture_own_regex:
#            for l in ls_all:
#                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
#                capture_cmd = anturlar.fos_cmd("mapsconfig --actions raslog,email")
#        
#        if "FPI Monitor" in capture_own_regex:
#            for l in ls_all:
#                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
#                capture_cmd = anturlar.fos_cmd("mapsconfig --disableFPImon")
#            
#        if "discard frame logging" in capture_own_regex:
#            for l in ls_all:
#                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
#                capture_cmd = anturlar.fos_cmd("framelog --disable -type du")
#                capture_cmd = anturlar.fos_cmd("framelog --disable -type unroute")
#             
#        if "SIM ports configured" in capture_own_regex:
#            en = anturlar.SwitchInfo()
#            #port_list = en.sim_ports()
#            
#            for l in ls_all:
#                anturlar.fos_cmd("setcontext %s " % l)
#                port_list = en.sim_ports()
#                anturlar.fos_cmd("flow --control -portIdMode slotport")
#                print("port list is \n")
#                print(port_list)
#                
#                for p in port_list:
#                    capture_cmd = anturlar.fos_cmd("flow --control -simport %s/%s -disable" % (p[0],p[1]) )
#            
#                anturlar.fos_cmd("flow --control -portIdMode index")
#            #capture_cmd = anturlar.fos_cmd_regex("N", reg_ex_list)
#            #message_check = "Firmwaredownload failed"
#        
#        ##if "SIM ports configured" in capture_own_regex:
#        ##    message_check = "Firmwaredownload failed"
#        
#        if "Brocade FC16-64 blades" in capture_own_regex:
#            message_check = "failed"
#        
#        
#        
#        if "failed" in message_check:
#            print("\n\ndo you want to stop the test ?")
#            print(message_check)
#            sys.exit()
#            #return(message_check)
#        
#        liabhar.count_down(20)
#        capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list)
#        #anturlar.close_tel()
#        
#        liabhar.email_sender_html(email, email, "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
#        liabhar.count_down(1800) 
#        return(capture_cmd)
################################################################################

def connect_console(HOST,usrname,password,port, *args):
    
    global tn
    var = 1
    reg_list = [b"aaaaa: ",  b"Login incorrect", b"option : ", b"root> ", b"login: ", b"r of users: "]   #### using b for byte string
    reg_list_r = [b".*\n", b":root> "]
    
    password = "pass"
    capture = ""
    option = 1
    #############################################################################
    #### parse the user name for console login
    ####
    port = str(port)
    usrname = parse_port(port)
    print("connecting via Telnet to  " + HOST + " on port " + port )
    print(HOST)
    print(usrname)
    print(password)
    print(port)
    
    tn = telnetlib.Telnet(HOST,port)
    print("tn value is  ", tn)
    
    tn.set_debuglevel(0)
    
    print("-------------------------------------------------ready to read lines")
    #############################################################################
    #### login 
    capture = tn.read_until(b"login: ")
    print(capture)
    tn.write(usrname.encode('ascii') + b"\r\n")
    #if password:
    capture = tn.read_until(b"assword: ")
    print(capture)
    tn.write(password.encode('ascii') + b"\r\n")
        
    print("\n\n\n\n\n\n\n\n")
    
    #############################################################################
    #### login to the switch
    reg_list = [ b"Enter your option", b"login: ", b"assword: ", b"root> ", b"users: " ]  
    while var <= 4:
        #print("start of the loop var is equal to ")
        capture = ""
        capture = tn.expect(reg_list)
        print(capture)
        
        if capture[0] == 0:
            tn.write(b"1")
                    
        if capture[0] == 1:
            tn.write(b"root\r\n")
                
        if capture[0] == 2:
            tn.write(b"assword\r\n")
                    
        if capture[0] == 3:
            print(capture)
            print("this found root")
            break
        
        if capture[0] == 4:
            print(capture)
            print("\n\n\n\n\n\nFOUND USERS: \n\n")
            tn.write(b"\r\n")
            #capture = tn.expect(reg_list)
            #break
            
        
        var += 1
      
    capture = tn.expect(reg_list, 20)
    if capture[0] == 1 :
        tn.write(b"root\r\n")
        capture = tn.expect(reg_list, 20)
        tn.write(b"password\r\n")
        capture = tn.expect(reg_list, 20)
        

    capture = tn.expect(reg_list, 20)
    
    return(tn)

def stop_at_cmd_prompt(db=0):
    global tn
    
    tn.set_debuglevel(db)
    print("\n\n\n\n\n\n\n\nlooking for stop autoboot\n\n")
    
    #cons_out = send_cmd("/sbin/reboot")
    #
    #
    reg_list = [ b"Hit ESC to stop autoboot: "]
    
    tn.write(b"/sbin/reboot\r\n")
    capture = tn.expect(reg_list, 3600)
    
    #tn.write( b"char(27)")  #### char(27) or \x1b are both ESC 
    tn.write(b"\x1b")
    reg_list = [b"Option"]
    
    capture = tn.expect(reg_list)
    tn.write(b"3\r\n")
    
    reg_list = [ b"=>"]
    capture = tn.expect(reg_list, 300)
    
    return()
       
def env_variables(swtype, db=0):
    
    tn.set_debuglevel(db)
    tn.write(b"printenv\r\n")
    reg_list = [b"=>"]
    capture = tn.expect(reg_list, 300)
    
    gateway   = "10.38.32.1"
    netmask   = "255.255.240.0"
    bootargs  = "ip=off"
    ethrotate = "no"
    server_ip = "10.38.2.40"
    ethact    = "ENET0"
    
    if swtype == 148:
        print("SKYBOLT")
        ethact = "FM1@DTSEC2"
    #if (swtype == 141 or swtype == 142):
    #    print("YODA")
    #    ethact = "FM2@DTSEC4"
        
    a = ("setenv ethact %s \r\n" % ethact)
    tn.write(a.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    
    g = ("setenv gateway %s \r\n" % gateway)
    tn.write(g.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    n = ("setenv netmask %s\r\n"%netmask)
    tn.write(n.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    b = ("setenv bootargs %s\r\n"%bootargs)
    tn.write(b.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    e = ("setenv ethrotate %s\r\n"%ethrotate)
    tn.write(e.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    s = ("setenv serverip %s\r\n"%server_ip)
    tn.write(s.encode('ascii'))
    capture = tn.expect(reg_list, 300)
    
    tn.write(b"saveenv\r\n")
    capture = tn.expect(reg_list, 300)
    tn.write(b"printenv\r\n")    
    capture = tn.expect(reg_list, 300)
    
    return(capture)

def pwr_cycle(pwr_ip, pp, stage, db=0):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    anturlar.power_cmd("cd access/1\t/1\t%s" % pp ,10)
    anturlar.power_cmd("show\r\n" ,10)
    
    anturlar.power_cmd(stage, 5)
    anturlar.power_cmd("yes", 5)
    
    #liabhar.JustSleep(10)
    anturlar.power_cmd("exit", 10)
     
    print("\r\n"*10)
    print("Waiting for the switch to boot")
    print("\r\n"*5)
    
    return(0) 
    
def load_kernel(switch_type, sw_ip, frm_version):
    
    reg_list = [ b"=>"]
    reg_bash = [ b"bash-2.04#", b"=>"]
    reg_linkup = [ b"link is up"]
    
    #### set tftp command
    
    ras = re.compile('([\.a-z0-9]+)(?:_)')
    ras = ras.search(frm_version)
    frm_no_bld = ras.group(1)
    if 'amp' in frm_version:
        frm_no_bld = frm_no_bld + '_amp'
    
    
    if switch_type == '133':  ####  ODIN
        nbt = "tftpboot 0x1000000 net_install26_odin.img\r\n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list, 300)
        tn.write(b"bootm 0x1000000\r\n")
        capture = tn.expect(reg_bash, 300)
        
    if (switch_type == '66' or switch_type == '71' or switch_type == '118' or switch_type == '109'):
        #### 5100  Stinger   tomahawk  tom_too
        nbt = "tftpboot 0x1000000 net_install_v7.2.img\r\n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list, 300)
        tn.write(b"bootm 0x1000000\r\n")
        capture = tn.expect(reg_bash, 300)
        
    if (switch_type == '120' or switch_type == '121' or switch_type == '64' or switch_type == '83'):
        ####  DCX zentron  pluto zentron  thor  7800
        nbt = "tftpboot 0x1000000 net_install26_8548.img\r\n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_list, 300)
        tn.write(b"bootm 0x1000000\r\n")
        capture = tn.expect(reg_bash, 300)
        
        
    if switch_type == '148':  #### SKYBOLT
        tn.write(b"makesinrec 0x1000000 \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x2000000  skybolt/uImage\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x3000000 skybolt/ramdisk.skybolt\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x4000000 skybolt/silkworm.dtb\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\r\n")
        caputure = tn.expect(reg_bash,300)
        
    if (switch_type == '141' or switch_type == '142'):  #### YODA 
        tn.write(b"makesinrec 0x1000000 \r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x2000000 yoda/uImage\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x3000000 yoda/ramdisk.yoda\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"tftpboot 0x4000000 yoda/silkworm_yoda.dtb\r\n")
        capture = tn.expect(reg_bash,300)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\r\n")
        caputure = tn.expect(reg_bash,300)
        
        
    tn.write(b"export PATH=/usr/sbin:/sbin:$PATH\r\n")
    capture = tn.expect(reg_bash, 300)
    i = "ifconfig eth0 %s netmask 255.255.240.0\r\n" % sw_ip 
    tn.write(i.encode('ascii'))
    capture = tn.expect(reg_bash, 300)
    tn.write(b"route add default gw 10.38.32.1\r\n")
    capture = tn.expect(reg_linkup,10)
    #tn.write(b"\r\n")
    capture = tn.expect(reg_bash, 10)
    m = "mount -o tcp,nolock,rsize=32768,wsize=32768 10.38.2.20:/export/sre /load\r\n"
    tn.write(m.encode('ascii'))
    capture = tn.expect(reg_bash, 300)
    ### firmwarepath
    firmpath = "cd /load/SQA/fos/%s/%s\r\n" % (frm_no_bld, frm_version)
    tn.write(firmpath.encode('ascii'))
    capture = tn.expect(reg_bash,600)
    #### need to capture when this hangs anc was not able to connect to the server  
    tn.write(b"./install release\r\n")
    capture = tn.expect(reg_bash,600)

    return(0)

def parse_port(port):
    print("port number " , port )
    print("\n\n")
    print("My type is %s"%type(port))
    print("\n\n\n\n")
    ras = re.compile('([0-9]{2})([0-9]{2})')
    ras_result = ras.search(port)
    print("port front  is  ",  ras_result.group(1))
    print("port back is    ",  ras_result.group(2))
    usrname = ras_result.group(2)
    if usrname < "10":
        ras = re.compile('([0]{1})([0-9]{1})')
        ras_result = ras.search(usrname)
        usrname = ras_result.group(2)
    usrname = "port" + usrname
    return usrname

def send_cmd(cmd, db=0):
    global tn
    
    tn.set_debuglevel(db)
    
    capture = ""
    cmd_look = cmd.encode()
    
    #reg_ex_list = [b".*:root> "]
    reg_ex_list = [b"root> "]
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\r\n")
    capture = tn.expect(reg_ex_list,3600)
    #print(capture[0])
    #print(capture[1])
    #print(capture[2])
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    
    return(capture)

def console_info_from_ip(ipaddr, chassis_name):
    """
    
    """
    #####################################
    # Check if file is available
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    #####################################
    #Check if IP is in valid format
    a = cofra.check_ip_format(ipaddr)
    if a == True:
        pass
    else:
        print("\nPLEASE CHECK YOUR IP ADDRESS AND TRY AGAIN")
        sys.exit()
        
    #####################################
    #Check if IP is in SwitchMatrix file
    ipaddr_switch   = get_ip_from_file(chassis_name)
    if ipaddr in ipaddr_switch:
        print('IP ADDRESS FOUND IN SwitchMatrix file')
    else:
        print('\nIP ADDRESS NOT FOUND IN SwitchMatrix file.')
        print('Are you sure this is your switch??\n')
        sys.exit()
        
    for line in csv_file:
        ip_address_from_file = (line['IP Address'])
        
        if ip_address_from_file == ipaddr:
            swtch_name = (line['Chassisname'])
         
        else:
            print("\r\n")
    return(swtch_name)

def console_info(chassis_name):
    """
    
    """
    
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    #print("@"*80)
    #print("@"*80)
    #print("looking for %s  " % chassis_name)
    #print(type(chassis_name))
    #print("@"*80)
    
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        #print("@"*80)
        #print(chassis_name_from_file)
        #print(type(chassis_name_from_file))
        #print("@"*80)
        
        if chassis_name_from_file == chassis_name:
            #sn = (switch_name)
            
            cons_1_ip   = (line['Console1 IP'])
            cons_1_port = (line['Console1 Port']) 
            cons_2_ip   = (line['Console2 IP'])
            cons_2_port = (line['Console2 Port']) 
        
            a = []
            a = [cons_1_ip, cons_1_port]
            #print("@"*80)
            #print(chassis_name)
            #print("&"*80)
            #print(cons_2_ip)
            
            if cons_2_ip:
                #print("&"*80)
                #print("checked for true cons_2_ip")
                #print(cons_2_ip)
                
                a += [cons_2_ip]
                a += [cons_2_port]
         
        else:
            print("\r\n")
            
    return(a)

def pwr_pole_info(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    #print("@"*80)
    #print("@"*80)
    #print("@"*80)
    
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        
        #if chassis_name_from_file == chassis_name[0]:
        if chassis_name_from_file == chassis_name:
            #sn = (switch_name)
            
            pwer1_ip = (line['Power1 IP'])
            pwer2_ip = (line['Power2 IP'])
            pwer3_ip = (line['Power3 IP'])
            pwer4_ip = (line['Power4 IP'])
            
            pwer1_prt = (line['Power1 Port'])
            pwer2_prt = (line['Power2 Port'])
            pwer3_prt = (line['Power3 Port'])
            pwer4_prt = (line['Power4 Port'])
            
            p = []
            p =[pwer1_ip, pwer1_prt]
            if pwer2_ip:
                p += [pwer2_ip]
                p += [pwer2_prt]
            if pwer3_ip:
                p += [pwer3_ip]
                p += [pwer3_prt]
            if pwer4_ip:
                p += [pwer4_ip]
                p += [pwer4_prt]
            

    
    return(p)

def get_user_and_pass(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
     
    u_and_p = []
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            u = (line['Username'])
            p = (line['Password'])
            u_and_p += [u]
            u_and_p += [p]
            
    return(u_and_p)
 
def get_ip_from_file(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    ips = [] 
    for line in csv_file:
        #chassis_name_from_file = (line['Chassisname'])
        #if chassis_name_from_file == chassis_name:
        ip = (line['IP Address'])
        if ip not in ips:
            ips.append(ip)
    print(ips)
    #sys.exit()
    return(ips)
    sys.exit()

def sw_set_pwd_timeout(pswrd):
   
    reg_list = [ b"Enter your option", b"login: ", b"Password: ", b"root> ", b"users: " ]
    reg_login = [ b"login:"]
    reg_assword = [ b"assword: ", b"root> "]
    reg_change_pass = [ b"key to proceed", b"incorrect" ]
    reg_complete   = [ b"zation completed"]
    reg_linertn    = [ b"\\r\\n" ]
    
    capture = tn.expect(reg_complete, 1000)
    tn.write(b"\r\n")
        #capture = tn.expect(reg_linertn)
    capture = tn.expect(reg_login, 60)
    
    tn.write(b"root\r\n")
    capture = tn.expect(reg_assword, 20)
    tn.write(b"fibranne\r\n")
    capture = tn.expect(reg_change_pass, 20)
    tn.write(b"\r\n")
    capture = tn.expect(reg_linertn)

    
    while True:    
        capture = tn.expect(reg_assword, 20)  #### looking for Enter new password
        #### if root is found break out 
        if capture[0] == 1:
            print(capture)
            print("this found root")
            break
        tn.write(b"password\r\n")
  
    capture = tn.expect(reg_list, 20)
    tn.write(b"root\r\n")
    capture = tn.expect(reg_list, 20)
    tn.write(b"password\r\n")
    capture = tn.expect(reg_list, 20)
    tn.write(b"timeout 0 \r\n")
    capture = tn.expect(reg_list, 20)
    
    return(tn)
   
def replay_from_file(switch_ip, lic=False, ls=False, base=False, sn=False, vf=False, fcr=False ):
    """
        open the log file for reading and add the following
        1. license
        2. create fids and base switch is previously set
        3. put ports into the FIDS
        4. update domains
        5. update switch name
        6. enable fcr
        7.
    """
    
    ff = ""
    f = ("%s%s%s"%("logs/Switch_Info_for_playback_",switch_ip,".txt"))
    print(f)
    
    try:
        with open(f, 'r') as file:
            ff = file.read()
    except IOError:
        print("\n\nThere was a problem opening the file" , f)
        sys.exit()
        
    print("look for the info\r\n")
    print(ff)
    ras_license     = re.findall('LICENSE LIST\s+:\s+\[(.+)\]', ff)
    
    print(ras_license)
    ras_ls_list     = re.findall('LS LIST\s+:\s+\[(.+)\]', ff)
    ras_base        = re.findall('BASE SWITCH\s+:\s+\[(.+)\]', ff)
    ras_switchname  = re.findall('SWITCH NAME\s+:\s+\[(.+)\]', ff)
    ras_vf          = re.findall('VF SETTING\s+:\s+\[(.+)\]', ff)
    ras_fcr         = re.findall('FCR ENABLED\s+:\s+\[(.+)\]', ff)
    ras_xisl        = re.findall('ALLOW XISL\s+:\s+\[(.+)\]', ff)
    ras_ports       = re.findall('Ports\s+:\s+\[(.+)\]', ff)
    
    ll = ras_license[0]
    ll.replace("'","")        #### remove the comma with string command  
    lic_list = ll.split(",")  #### change the data from string to list

    all_list = []
    all_list += [lic_list]
    all_list += [ras_ls_list]
    all_list += [ras_base]
    all_list += [ras_switchname]
        
    
    return(all_list)

    
###############################################################################
###############################################################################
###############################################################################
###############################################################################    

 
    
def main():

    global tn
    
###############################################################################
####
#### 
####
###############################################################################
    pa = parse_args(sys.argv)
    #print(pa)
    #print(pa.chassis_name)
    #print(pa.ip)
    #print(pa.quiet)
    #print(pa.verbose)
    #print(pa.firmware)
    #print("@"*40)
    #print(pa.frmup)
    #print(pa.frmdwn)
    #sys.exit()

   
    ##########################################################################
    ##########################################################################
    ###
    ### hold the ip address from the command line
    ###

    if pa.ip:
        pa.chassis_name = console_info_from_ip(pa.ip, pa.chassis_name)
    cons_info           = console_info(pa.chassis_name)
    console_ip          = cons_info[0]
    console_port        = cons_info[1]
    
    power_pole_info     = pwr_pole_info(pa.chassis_name)    
    usr_pass            = get_user_and_pass(pa.chassis_name)
    user_name           = usr_pass[0]
    usr_psswd           = usr_pass[1]
    frmup               = pa.frmup
    frmdwn              = pa.frmdwn
    
    tn = anturlar.connect_tel_noparse(pa.ip,user_name,usr_psswd)
    fi = anturlar.FabricInfo()
    si = anturlar.SwitchInfo()
    fcr = anturlar.FcrInfo()
    
    if pa.fabwide:
        ipaddr_switch   = fi.ipv4_list()
        #print(ipaddr_switch)
    elif pa.csvall:
        ipaddr_switch   = get_ip_from_file(pa.chassis_name)
    elif pa.fcrwide:
        anturlar.fos_cmd("setcontext %s" % fcr.base_check())
        ipaddr_switch   = fcr.fcr_fab_wide_ip()     
    else:
        ipaddr_switch       = [pa.ip]
    
    fwdl = firmwaredownload(frmdwn, frmup,"gsquire@brocade.com")    
    ##fwdl = cofra.DoFirmwaredownloadChoice('v7.4.0','v7.4.0a_rc1_bld10')
    #if pa.tofirmvrsn == False:
    #    print("none")
    #else:
    #    pass
    ##sys.exit()
    #fwdl = doFirmwareDownload(pa.firmware)
    #a = fwdl.start()
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #print(a)
    #print(c)
    anturlar.close_tel()
    sys.exit()
    
    #### pass ip(s)to login procedure
    #### and write the file

    for i in ipaddr_switch:
        tn = anturlar.connect_tel_noparse(i,user_name,usr_psswd)
        nos = si.nos_check()
        if not nos:
            sw_dict              = cofra.get_info_from_the_switch()
            switch_ip            = sw_dict["switch_ip"]
            sw_name              = sw_dict["switch_name"]
            sw_chass_name        = sw_dict["chassis_name"]
            sw_director_or_pizza = sw_dict["director"]
            sw_domains           = sw_dict["domain_list"]
            sw_ls_list           = sw_dict["ls_list"]
            sw_base_fid          = sw_dict["base_sw"]
            sw_xisl              = sw_dict["xisl_state"]
            sw_type              = sw_dict["switch_type"]
            sw_license           = sw_dict["license_list"]
            sw_vf_setting        = sw_dict["vf_setting"]
            sw_fcr_enabled       = sw_dict["fcr_enabled"]
            sw_port_list         = sw_dict["port_list"]

            print("\n"*20)
            print("SWITCH IP            : %s   " % switch_ip)
            print("SWITCH NAME          : %s   " % sw_name)
            print("CHASSIS NAME         : %s   " % sw_chass_name)
            print("DIRECTOR             : %s   " % sw_director_or_pizza)
            print("SWITCH DOMAINS       : %s   " % sw_domains)
            print("LOGICAL SWITCH LIST  : %s   " % sw_ls_list)
            print("BASE FID             : %s   " % sw_base_fid)
            print("XISL STATE           : %s   " % sw_xisl)
            print("SWITCH TYPE          : %s   " % sw_type)
            print("LICENSE LIST         : %s   " % sw_license)
            print("VF SETTING           : %s   " % sw_vf_setting)
            print("FCR SETTING          : %s   " % sw_fcr_enabled)
            print("PORT LIST            : %s   " % sw_port_list)
            print("@"*40)
            print("CONSOLE INFO         : %s   " % cons_info)
            print("@"*40)
            print("POWER POLE INFO      : %s   " % power_pole_info)
            print("@"*40)        
            print("\nSwitch_Info has been written this file in logs/Switch_Info_for_playback_%s.txt\n" % switch_ip)
            print("@"*40)
        else:
            print("\n"+"@"*40)
            print('\nTHIS IS A NOS SWITCH> SKIPPING')
            print("\n"+"@"*40)
            pass
    anturlar.close_tel()
    sys.exit()
     
###############################################################################
####
####  close telnet connection and 
####  connect to the console
####
###############################################################################

    cc = cofra.SwitchUpdate()
    
    cons_out = cc.playback_licenses()
    cons_out = cc.playback_ls()
    cons_out = cc.playback_switch_names()
    cons_out = cc.playback_switch_domains()
    cons_out = cc.playback_add_ports()
    tn       = cc.reboot_reconnect()
    cons_out = anturlar.fos_cmd("switchshow")
    print(cons_out)
    anturlar.close_tel()

    #connect_console(console_ip, user_name, usr_pass, console_port)
    #cons_out = send_cmd("switchshow")
    
 
    
 
        
###############################################################################
####
####  reboot and find the command prompt
####
     
    
    
    #cons_out = stop_at_cmd_prompt(9)
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print(cons_out)
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #cons_out = env_variables(sw_type, 9)
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    #print(cons_out)
    #load_kernel(sw_type, my_ip, pa.firmware)
    #
    #for pp in range(0, len(power_pole_info), 2):
    #    print('POWERPOLE')
    #    print(power_pole_info[pp])
    #    print(power_pole_info[pp+1])
    #    pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off")
    #    time.sleep(2)
    #    
    #for pp in range(0, len(power_pole_info), 2):
    #    print('POWERPOLE')
    #    print(power_pole_info[pp])
    #    print(power_pole_info[pp+1])
    #    pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "on")
    #    time.sleep(2)
    ##### is there another way to tell if switch is ready ??
    ##### instead of waiting
    #print("\r\n"*6)
    #print("@"*40)
    #print("wait here to login and change passwords")
    #print("\r\n"*6)     
    ##liabhar.count_down(300)
    ##time.sleep(360)
    #cons_out = sw_set_pwd_timeout(usr_psswd)
    #
    #tn.close()
    #
    #tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    #
    #print("\r\n\r\nLICENSE ADD TO SWITCH \r\n\r\n")
    #
    #print(my_ip)
    #
    #c = cofra.SwitchUpdate(switch_ip)
    #cons_out = cc.playback_licenses_to_switch()
    #
    #print(cons_out)
    #
    #anturlar.close_tel()
    ##tn.write(b"exit\n")
    ##tn.close()
    # 
    #dt = liabhar.dateTimeStuff()
    #date_is = dt.current()
    #print(date_is)
    
if __name__ == '__main__':
    
    main()


###############################################################################
#### END
###############################################################################


