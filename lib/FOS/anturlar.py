#!/usr/bin/env python3

####
####  old method of  calling python3 
#!/opt/python3/bin/python3

import telnetlib
import getpass
import os,sys
#import argparse
import re
import var
import datetime
import liabhar
from socket import error as SocketError
import errno
"""
Note: Naming conventions follow the typical Python convention

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name                                
"""

class FabricInfo:
    """
        A class to return information about a Fabric.
        The FID is required make the class specific to the FID.
        
    """
    
    def __init__(self, fid=128):
        self.fid = fid
        print("\n\ninitializing Fabric Info class  ", self.fid, "\n\n\n")
        
    def __change_fid__(self):
        capture_cmd = fos_cmd("setcontext " + str(self.fid))
        
    def sid_numbers(self):
        """
            Return a string of the members of the current fabric
            Return none if no switches are found
        """
        self.__change_fid__()
        capture_cmd = fos_cmd("fabricshow")
        
        #### the next two lines would return each item from the fabricshow command
        ras = re.compile('\s?([0-9]{1,3}):\s+([\d\w]{6})\s+([:\d\w]{23})\s+([.\d]{7,15})\s+([.\d]{7,15})\s+(["_\w\d]+)')
        ras_result = ras.search(capture_cmd)
        #### the above two lines not used here
        
        ras = re.compile('\s?([0-9]{1,3}):\s+')
        ras_result_all = ras.findall(capture_cmd)
            
        #print("\n\n\n\n", ras_result_all, "ras_result_all\n\n\n")
        if not ras_result_all:
            ras_result_all = "none"
           
        return ras_result_all
    
    def switch_count(self):
        """
            Return the number of switches in the FID
            Return 0 if no match is found
        """
        self.__change_fid__()
        capture_cmd = fos_cmd("fabricshow")
        
        #### the next two lines would return each item from the fabricshow command
        #ras = re.compile('\s?([0-9]{1,3}):\s+([\d\w]{6})\s+([:\d\w]{23})\s+([.\d]{7,15})\s+([.\d]{7,15})\s+(["_\w\d]+)')
        #ras_result = ras.search(capture_cmd)
        #### the above two lines not used here
        
        ras = re.compile('Fabric has\s?([0-9]{1,3})')
        #ras = re.compile('Fabric has')
        ras_result_all = ras.search(capture_cmd)
        
        if not ras_result_all:
            ras_result = "0"
        else:
            ras_result = ras_result_all.group(1)
            print(ras_result_all.group(1))
        return ras_result
    
    
    def ipv4_list(self):
        """
            Return a string of the ipv4 address of the switches in
            the current fabric
            Return none if nothing is matched
        """
        #self.__change_fid__()
        capture_cmd = fos_cmd("fabricshow")
        ras = re.compile('(?:\s?[0-9]{1,3}:\s+[\d\w]{6}\s+[:\d\w]{23}\s+)([1-9][0-90-9].\d{1,3}.\d{1,3}.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd)
        #print(ras_result_all)
        if not ras_result_all:
            ras_result_all = None
            
        return(ras_result_all)
    
    
    def ipv4_plus_fcr_list(self,usr,pw):
        """
            Return a string of the ipv4 plus switches attached via FCR
            Return none if nothing is matched with ipv4_list
            
        """
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print(usr)
        print(pw)
        #sys.exit()
        bb_fablist = self.ipv4_list()
        #host = sys.argv[1]
        #user = sys.argv[2]
        #pw = sys.argv[7]
        capture_cmd = fos_cmd("fcrfabricshow")
        ras = re.compile('(?:\d{1,3}\s+\d{1,3}\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd)
        fablist_nodup = (list(set(ras_result_all)))
        #tn.set_debuglevel(9)
        try:
            if fablist_nodup:
                for ip in fablist_nodup:
                    #print("\n\n\n\n\nCURRENTLY ON IP ", ip , "\n\n\n\n")
                    conn_value = connect_tel_noparse(ip, usr, pw)
                    fablist_extended = self.ipv4_list()
                    for n in fablist_extended:
                        if n not in fablist_nodup:
                            fablist_nodup.append(n)
        except:
            #return(False)
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^')
            print('connection failed')
            sys.exit()
        return(fablist_nodup)
    
    
    def name(self):
        """
            Return a string of the names of the members in the current fabric
            Return none if no match is found
            
        """
        
        self.__change_fid__()
        capture_cmd = fos_cmd("fabricshow")
        
        #### the next two lines would return each item from the fabricshow command
        ras = re.compile('\s?([0-9]{1,3}):\s+([\d\w]{6})\s+([:\d\w]{23})\s+([.\d]{7,15})\s+([.\d]{7,15})\s+(["_\w\d]+)')
        ras_result = ras.search(capture_cmd)
        #### the above two lines not used here
        
        ras = re.compile('[.\d]{7,15}\s+[.\d]{7,15}\s+>?(["_\w\d]+)')
        ras_result_all = ras.findall(capture_cmd)
            
        if not ras_result_all:
            sw_names = "none"
            
        sw_names = [str(i.replace('"', '')) for i in ras_result_all]
        
        return sw_names
     
     
    def all_info(self):
        """
            Does nothing at this time
        """
        pass
    
    def fabric_members(self):
        """
            Return a string of the members of the current fabric
        """
        capture_cmd = fos_cmd("fabricshow")
        
        #15})\\s+(FC)\\s+([\(\)\":_ \-a-zA-Z0-9]+)')
        ras = re.compile('\s?([0-9]{1,3}):\s+([\d\w]{6})\s+([:\d\w]{23})\s+([.\d]{7,15})\s+([.\d]{7,15})\s+(["_\w\d]+)')
        ras_result = ras.search(capture_cmd)
        
        ras = re.compile('\s?([0-9]{1,3}):\s+')
        ras_result_all = ras.findall(capture_cmd)
         
        #if ras_result:
            #print("\n\nFabric show output\n")
            #print("Match found group 0: ",ras_result.group())
            #print("Match found group 1: ",ras_result.group(1))
            #print("Match found group 2: ",ras_result.group(2))
            #print("Match found group 3: ",ras_result.group(3))
            #print("Match found group 4: ",ras_result.group(4))
            #print("Match found group 5: ",ras_result.group(5))
            #print("Match found group 6: ",ras_result.group(6))
            #print("Match found group 7: ",ras_result.group(7))
        
            #print("\n\nFabric show output end\n")
        #else:
            #ras_result = "no fabric"
            #print("no fabric")
            
        if ras_result_all:
            #print("\n\nFabric show output find ALL\n")
            #print("Match for find all :" , ras_result_all)
            #swtch_one = ras_result_all[0]
            #print("First in the list is : ", swtch_one)
            #how_many = len(ras_result_all)
            #print("Last in the list is  : ", ras_result_all[how_many -1])
            
            #print("\n\nFabric show find all output end\n")
            return(ras_result_all)
            
        else:
            print("NOOOOOOOOOOOOO!!!!!!!!!!")
            ras_result = "no fabric"
            return("no fabric")
            
        return(ras_result)


    def zone_info(self, zone_capture):
        """
           return info all about the zones
           zone_capture needs to be a 1,2 or 3
           1 = Entire cfgshow output
           2 = Defined only
           3 = Effective only
        """
        #### need to add zone names
        capture_cmd = fos_cmd("cfgshow")
        entire = ('Defined configuration:\r\n\s[ 0-9a-zA-Z:;_,\r\n\t]+\r\n')
        defined = ('Defined configuration:\r\n\s[ 0-9a-zA-Z:;_,\r\n\t]+(?=Effective)')
        effective = ('Effective configuration:\r\n\s[0-9a-zA-Z:;_, \r\n\t]+')
        #effective = ('Effective configuration:\r\n\s[0-9a-zA-Z:;_, \n\t]+')
        global tn
        tn.set_debuglevel(9)
        if zone_capture == 1:
            ras = re.compile(entire)
            a = ras.findall(capture_cmd)
            zone = (str(a[0]))
            return(zone)
        elif zone_capture == 2:
            ras = re.compile(defined)
            wtf = ras.findall(capture_cmd)
            define = (str(wtf[0]))
            return(define)
        elif zone_capture == 3:
            ras = re.compile(effective)
            wtf = ras.findall(capture_cmd)
            eff = (str(wtf[0]))
            return(eff)
        else:
            print ("No Zone match or a number other than 1,2,3 passed in. Exiting Script")
            sys.exit()

    def zone_cfgtransshow(self, dblevel=0):
        capture_cmd = fos_cmd("cfgtransshow --opentrans", dblevel)
        ras = re.compile('(?<=-)\r\n\s?(\d{1,3})')
        digit = ras.findall(capture_cmd)
        return(digit)
        
class SwitchInfo:
    """
        A class to return information about a switch
    """
    global tn
    
    def __init__(self):
        #my_ipaddr = ipaddr
        self.__director__()
        self.online_ports = ""
        self.ipaddr =  self.__myIPaddr__()
        
    
    
    def __sw_show_info_no_port_type__(self):
        """
            capture the switch info and each column with regexs
            if the port type is not included in switchshow output
            then add the port to the list
        """
        #tn.set_debuglevel(9)
        capture_cmd = fos_cmd("switchshow")
        if self.am_i_director:
            ras = re.compile('\s?([0-9]{1,4})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG123486]{2,4})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
        else:
            #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
            ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9a-f]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
        ras = ras.findall(capture_cmd)
        self.online_ports = ras
        
    def __sw_show_info_all_ports__(self):
        """
            capture switchshow info for ports (port types: F,E,EX,VEX and Disabled) and each column with regex
            return the index list of ports
        """
        capture_cmd = fos_cmd("switchshow")
        if self.am_i_director :
            #ras = re.compile('\s?([0-9]{1,3})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+(Online)\s+(FC)\s+([->\w]{6,8})\s+([()-:\"_\w\s\d]*?(?=\\n))')
            ras = re.compile('\s?([0-9]{1,4})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG123486]{2,4})\s+([_\w]{5,9})\s+([FCVE]+)\s*([->\w]{6,8})([()-:\"_=\w\s\d]*?(?=\\n))')
        else:
            #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+(Online)\s+[FCVE]\s+([->\w]{6,14})\s+([()-:\"_\w\s\d]*?(?=\\n))')  
            #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+(FC)\s+([->\w]{6,14})\s+([()-:\"_\w\s\d]*?(?=\\n))')
            ras = re.compile('\s?([0-9]{1,4})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG123486]{2,4})\s+([_\w]{5,9})\s+([FCVE]+)\s*([->\w]{6,14})([()-:\"_=\w\s\d]*?(?=\\n))')
        ras = ras.findall(capture_cmd)
        self.online_ports = ras
        return(ras)
        
    def __sw_basic_info__(self):
        """
            Retrieve FCR fabric and return info. Variable #'s:
            0) Switch name
            1) IP address
            2) Chassis or Pizza Box
            3) VF or not
            4) FCR Enabled
            5) Base Configured
    
        """
        switchname = self.switch_name()
        ip_addr = self.ipaddress()
        director = self.director()
        vf = self.vf_enabled()
        fcr = self.fcr_enabled()
        base = self.base_check()
        
        return[switchname, ip_addr, director, vf, fcr, base]
        
        #Example on how to print Human readable results:
        #print('\n\n'+ '='*20)
        #print("Switch Name :  %s" % initial_checks[0])
        #print("IP address :  %s" % initial_checks[1])
        #print("Chassis :  %s" % initial_checks[2])
        #print("VF enabled :  %s" % initial_checks[3])
        #print("FCR enabled :  %s" % initial_checks[4])
        #print("Base configured :  %s" % initial_checks[5])
        #print('='*20 + '\n\n')
        

    def __director__(self):
        """
            determine if the switch is director or pizza box
            True = director
            False = pizza box
        """
  
        capture_cmd = fos_cmd("hashow",0)
        #print('ZZZZZZZZZZZ')
        #print(capture_cmd)
        self.am_i_director = True
        try:
            if "hashow: Not supported" in capture_cmd:
                self.am_i_director = False
        except:
            #self.am_i_director = False
            return("COULD NOT DETERMINE IF SWITCH IS A DIRECTOR")
        
            
    def __myIPaddr__(self):
        """
            determine the current switch IP
            Return the ipv4 address
            Return 0 if no match found
        """
        capture_cmd = fos_cmd("ipaddrshow", 0)
        try:
            #match = re.search('(?P<ipaddress>[\s+\S+]+:([\d\.]){7,15}(?=\\r\\n))', capture_cmd)
            match = re.search('(?P<sre>([\s+\w+]+):\s?(?P<ip>[0-9\.]{1,15}))', capture_cmd)
        
            if match:
                myip = (match.group('ip'))
                return(myip)
            else:
                print("\n\n NO IP FOUND \n\n")
                return(0)
        except:
            return("COULD NOT MATCH IP ADDRESS")
    

    def __getblanklist__(self):
        """
            Find the ports that are blank 
            Return a list of port or slot / port for directors            
        """
        #### this still needs tested for no port in the list
        ####  in other words with all ports populated
        #### it could be tested with all SIM ports
        ####
        port_list = []
        self.__sw_show_info_no_port_type__()
        capture_cmd_split = self.online_ports
        for i in capture_cmd_split:
            slot_port_list = []
            slot_port_list.append(int(i[1]))
            if self.am_i_director:
                slot_port_list.append(int(i[2]))
            port_list.append(slot_port_list)
         
        return(port_list)

    def __getportlist__(self, porttype):
        """
        `   Return a list of the porttype passed in - in the current FID
            
        """
        port_list = []
        self.__sw_show_info_all_ports__()
        capture_cmd_split = self.online_ports
        ras_result = capture_cmd_split.count(porttype)
        if self.am_i_director:
            location = 8
        else:
            location = 7
            
        persist_local = location
        persist_local += 1
            
        for i in capture_cmd_split:
            if i[location] == porttype:
                #### port_list.append(i[0])
                #slot_port_list = []
                #slot_port_list.append(int(i[1]))
                if self.am_i_director:
                    #slot_port_list.append(int(i[2]))
                    slot_port_list = [int(i[1]), int(i[2])]
                #port_list.append(s_p)
                else:
                    slot_port_list = [0, int(i[1])]
                port_list.append(slot_port_list)
                 
                 
            if porttype == "Persistent":
                try:
                    if "rsistent" in i[persist_local]:
                        ####port_list.append(i[0])
                        #slot_port_list = []
                        #slot_port_list.append(int(i[1]))
                        if self.am_i_director:
                            #slot_port_list.append(int(i[2]))
                            slot_port_list = [int(i[1]), int(i[2])]
                        else:
                            slot_port_list = [0, int(i[1])]
                        port_list.append(slot_port_list)
                        
                except UnboundLocalError:
                    print("unboundlocalerror - moving on  ")
                    pass

        if not ras_result:
            ras_result = "no port found"
        return(port_list)

    def ae_ports(self):
        """
           Return a list of the AMP AE-ports in the current FID
        """
        return(self.__getportlist__("AE-Port"))
    
    def allow_xisl(self):
        """
            Return whether XISL Use is: 'ON or OFF'
            
        """
        capture_cmd = fos_cmd("switchshow")
        try:
            ras = re.compile('Allow XISL Use:\s+(\w{2,3})') 
            ras = ras.findall(capture_cmd)
            ss = str(ras[0])
        except IndexError: ##Base switch does not have "allow xisl" condition
            return("OFF")
        else:
            return(ss)

    def all_ports(self):
        """
            Queuries switch for number of ports.
            return the port list or none if no ports in the FID
            The list will include FC and VE ports
        """
        
        ras_list = []
        capture_cmd = fos_cmd("switchshow")
        if self.am_i_director:
            ras = re.compile('(?:\d{1,4}\s{3,4})(?P<slotnumber>\d{1,2})\s+?(?P<port>\d{1,2})') 
            ras = ras.findall(capture_cmd)
            for i in ras:
                ras_list.append(list(i))
            for i in ras_list:
                i[0] = int(i[0])
                i[1] = int(i[1])
            return(ras_list)
        else:
            ras = re.compile('(?:\n\s+?\d+\s{0,3})(\d{0,3})')
            ras = ras.findall(capture_cmd)
            for i in ras:
                prt = [0, int(i)]
                #prt.append(int(i))
                ras_list.append(prt)
                 
            return(ras_list)
        
        return("none")
    
    def all_ports_fc_only(self):
        """
            Queuries switch for number of ports.
            return the port list or none if no ports in the FID
            the list will include FC ports only
        """
        ras_list = []
        
        capture_cmd = fos_cmd("switchshow")
        if self.am_i_director:
            ras = re.compile('(?:\d{1,4}\s{3,4})(?P<slotnumber>\d{1,2})\s+?(?P<port>\d{1,2})\s+[-0-9a-f]{6}\s+[-idcu]{2}\s+[-ANU234816G]{2,3}\s+\w+\s+[FC]{2}') 
            ras = ras.findall(capture_cmd)
            for i in ras:
                ras_list.append(list(i))
            for i in ras_list:
                i[0] = int(i[0])
                i[1] = int(i[1])
            return(ras_list)
        else:
            ras = re.compile('\s?\d{1,2}\s+(\d{1,2})\s+[-0-9a-f]{6}\s+[-idcu]{2}\s+[-AN234816G]{2,3}\s+\w+\s+[FC]{2}') 
            ras = ras.findall(capture_cmd)
            for i in ras:
                prt = [0, int(i)]
                #prt.append(int(i))
                ras_list.append(prt)
                 
            return(ras_list)
        
        return("none")
    
    def base_check(self):
        """
            Return Base FID if found
            Return False if no base is found
        """
        capture_cmd = fos_cmd("lscfg --show")
        match = re.search('(?P<default>\d{0,3})\(ds\)(?:.+?)(?P<base>\d{0,3})\(bs\)', capture_cmd)
        if match:
           base = (match.group('base'))
           return(base)
        else:
           return(False)
    
    def blade_search_8GB(self):
        """
            Parse out 8GB Blades.
            This is used against non-VF switches.
            Return 0 if none are found
        """
        #global tn
        slotshow_8GB = fos_cmd("slotshow -m | grep F.8")
        pattern = re.compile("BLADE")
        matchObj = pattern.search(slotshow_8GB)
        if matchObj:
            #print("\n\n\nGathering Blade Info\n\n\n")
            return(slotshow_8GB)
        else:
            return(0)
    
    def blades(self, L=False, C=False):
        """
            return the list of SW blades in the switch
            includes SW BLADES and AP BLADES
            L option will return a list of the blade port numbers if set to true
               if set to false it will return the port, type, ID and model
               
        """
        
        
        if self.am_i_director:
            capture_cmd = fos_cmd("slotshow -m")
            if L:
                ras = re.compile('(\d+)\s+[SWAP]')
            elif C:
                #ras = re.compile('(\d+)\s+(CORE BLADE)\s+(\d+)\s+([-CRFCOSEX1032468]+)\s+(\w+)')
                print("&"*80)
                ras = re.compile('(\d+)\s+[CO]{2}')
            else:
                ras = re.compile('(\d+)\s+(SW BLADE|AP BLADE|CP BLADE|CORE BLADE)\s+(\d+)\s+([-FCOSEX1032468]+)\s+(\w+)')
            
            ras = ras.findall(capture_cmd)
            return(ras)
        else:
            if not self.am_i_director:
                return("not a director")
            else:
                return("unknown")
            

    def blank_type(self):
        """
            Return a list of ports that do not have a port type
            
        """
        return(self.__getblanklist__())
    
    def currentFID(self):
        """
            Return the current FID number
            
        """
        capture_cmd = fos_cmd("switchshow")
        ras = re.compile('[.\s]+LS Attributes:\s+\[FID:\s+(\d+)') 
        ras = ras.findall(capture_cmd)
        print("\n\n\n")
        print("CURRENT FID")
        print(ras)
        if not ras:
            fid = "AG MODE ?"
        else:
            fid = int(ras[0])
        return(fid)
    
    def chassisname(self):
        capture_cmd = fos_cmd("chassisname")
        cn = capture_cmd.replace(" ", '')
        ras = re.compile('([\w\d_]+)(?:\\r\\n)')
        ras = ras.findall(cn)
        return(ras)
    
    #def d_ports(self):
    #    """
    #        this does not work because the getportlist requires the port
    #    """ 
    #    return(self.__getportlist__("D-Port"))
    
    def cp_ipaddrs_get(self):
        """
            determine the current switch IP
            Return the ipv4 address
            Return 0 if no match found
        """
        capture_cmd = fos_cmd("ipaddrshow", 0)
        try:
            #match = re.search('(?P<ipaddress>[\s+\S+]+:([\d\.]){7,15}(?=\\r\\n))', capture_cmd)
            ras = re.compile('Ethernet\s+IP\s+Address:\s+([0-9\.]{7,15})')
            ras = ras.findall(capture_cmd)
            return(ras)

        except:
            print("COULD NOT MATCH IP ADDRESS")
            sys.exit()
            return("COULD NOT MATCH IP ADDRESS")
            
        return(ras)
    
    def credit_recovery(self):
        """
            returns the configuration setting for credit recovery
            captures each line the has a line return at the end
            
        """
        
        capture_cmd = fos_cmd("creditrecovmode --show")
        #cn = capture_cmd.replace(" ", '')
        ras = re.compile('([ \'\w\d_]+)(?:\\r\\n)')
        ras = ras.findall(capture_cmd)
        return(ras)
        
    
    
    
    def default_switch(self):
        """
            Return default FID if found
            Return 0 if no match
        """
        capture_cmd = fos_cmd("lscfg --show")
        match = re.search('(?P<default>\d{0,3})\(ds\)(?:.+?)(?P<base>\d{0,3})\(bs\)', capture_cmd)
        if match:
            default = (match.group('default'))
            return(default)
        else:
            return(0)

    def director(self):
        """
            return a True if this switch is a director
        """
        return(self.am_i_director)
    
    def disabled_ports(self):
        """
            Return a list of disabled ports including Persistent disabled ports
        """
        return(self.__getportlist__("Disabled"))
    
    def dns_config_info(self):
        """
                 Domain Name Server Configuration Information 
         ____________________________________________ 

         Domain Name            = englab.brocade.com
         Name Server IP Address = 10.38.2.1
         Name Server IP Address = 10.38.2.2
        """
        
        reg_ex = [ b"4]"]
        reg_ex_option = [ b"Enter option" ]
        
        capture_cmd = fos_cmd_regex("dnsconfig", reg_ex, 9)
        
        #cn = capture_cmd.replace(" ", '')
        capture_cmd = fos_cmd_regex("1", reg_ex)
        
        ras_dname = re.compile('(Domain Name\s+=\s+[\.a-zA-z0-9]+)(?:\r\n)')
        ras_ip = re.compile('(Name Server IP Address\s+=\s+[\.0-9:]+)(?:\r\n)')
        ras_dname = ras_dname.findall(capture_cmd)
        ras_ip = ras_ip.findall(capture_cmd)
        
        dns_info = str(ras_dname) + str(ras_ip)
        
        capture_cmd = fos_cmd("4")
        
        return(dns_info)
        
        
        
    def e_ports(self):
        """
        `   Return a list of the E-ports in the current FID
        """
        doit = False
        e = self.__getportlist__("E-Port")
        dex = -1
        try:
            dex = [y[0] for y in e].index(-1)
            e.pop(dex)
        except ValueError:
            pass
        #if dex != -1:
            #e.pop(dex)
        
        return(e)
    
    def ex_ports(self):
        """
        `   Return a list of the EX-ports in the current FID
        """
        return(self.__getportlist__("EX-Port"))
    
    def vex_ports(self):
        """
        `   Return a list of the VEX-ports in the current FID
        """
        return(self.__getportlist__("VEX-Port"))
      
    def d_ports(self):
        """
            Return a list of the D-Ports in the current FID
        """
        return(self.__getportlist__("D-Port"))
        
    def f_ports(self):
        """
        `   Return a list of the F-ports in the current FID
        """
        return(self.__getportlist__("F-Port"))
    
    def fan_count(self):
        """
            count the list of fans returned in fanshow command
        """
        capture_cmd = fos_cmd("fanshow")
        ras = re.compile('(Fan)\s(\d)([, \w\d]{9,25})')
        ras = ras.findall(capture_cmd)
        return(ras)
    
    def fcr_enabled(self):
        """
            Determine if FCR is enabled on the switch
            1 - yes
            0 - no
        """
        fos_cfg = fos_cmd("fosconfig --show")
        foscfg = re.search( r'(FC Routing service:).*(enabled)', fos_cfg, re.M|re.I)
        if foscfg:
            return(True)
        else:
            return(False)    
     
    def g_ports(self):
        """
            Return a list of the G-ports in the current FID
        """
        return(self.__getportlist__("G-Port"))
    
    def getLicense(self):
        """
            get a list of the license on the switch
        """
        try:
            capture_cmd = fos_cmd("licenseshow")
            #ras = re.compile('([\w\d]{16,37})(?=:\\r\\n)')
            ras = re.compile('([\w\d]*[A-Z,a-z,0-9])(?=:\s)')
            ras = ras.findall(capture_cmd)
            return(ras)
        except:
            return("COULD NOT DETERMINE LICENSE")
        
        
    def ipaddress(self):
        return(self.__myIPaddr__())
    
    def loopback(self):
        """
            Return a list of the Loopback-ports in the current FID
        """
        return(self.__getportlist__("Loopback->Port"))
    
    def ls(self):
        """
            find the logical switch numbers and return them in a list 
        """
        capture_cmd = fos_cmd("lscfg --show")
        ras = re.compile('(\d{1,3})(?=\()')  
        ras = ras.findall(capture_cmd)
        return(ras)
    
    def ls_now(self):
        """
            find the logical switch numbers that is currently logged in 
        """
        capture_cmd = fos_cmd(" ")
        ras = re.compile('[-_A-Za-z0-9]{1,30}:FID(\d{1,3})')  
        ras = ras.findall(capture_cmd)
        try:
            ras = int(ras[0])
            return(ras)
        except:
            return(0)

    def ls_and_domain(self):
        """
            find the logical switch numbers and the domains
        """
        capture_cmd = fos_cmd("lscfg --show")
        #ras = re.compile('IDs\):\s+([\( 0-9bsd)]+)(?=\\r\\n)')
        ras = re.compile('([\(0-9bsd)]{4,12})')
        
        ras = ras.findall(capture_cmd)
        
        return(ras)
    

    def nos_check(self):
        """
            Looks at switchshow output and if "Rbridge" is found, it is a NOS switch.
        """
        capture_cmd = fos_cmd("switchshow | grep Rbridge")
        ras = re.search(r'Rbridge', capture_cmd)
        if ras:
            return(True)
        else:
            return(False)
            
    def n_ports(self):
        """
            Return a list of N-Ports in the current FID
            
        """
        return(self.__getportlist__("N-Port"))
    
    def persistent_disabled_ports(self):
        """
            Return a list of disabled ports including Persistent disabled ports
            
        """
        return(self.__getportlist__("Persistent"))

    def sensor_t_f_ps(self,sensor_type):
        """
            Return a list of temp sensors, Fan or Power Supply from
            sensorshow commmand that report Ok
            type can be f = Fan    t = Temperature Sensor   ps = Power Supply
            
        """
        
        if sensor_type == "t":
            capture_cmd = fos_cmd("sensorshow")
            ras = re.compile('(sensor)\s+(\d+):\s+\((Temperature)\)\s+is\s+([Ok]{2}), value is (\d+)') 
            ras = ras.findall(capture_cmd)
         
        if sensor_type == "f":
            capture_cmd = fos_cmd("sensorshow")
            ras = re.compile('(sensor)\s+(\d+):\s+\((Fan        )\)\s+is\s+([OkFaulty]{2,6})(?=,speed is (\d+))*') 
            ras = ras.findall(capture_cmd)
         
        if sensor_type == "ps":
            capture_cmd = fos_cmd("sensorshow")
            ras = re.compile('(sensor)\s+(\d+):\s+\((Power Supply)\)\s+is\s+([Ok]{2})') 
            ras = ras.findall(capture_cmd)
            
        return(ras)

    def sfp_info(self,info_type="info"):
        """
            Return a list of sfp and the optic speed
            speed or a summary
            pass summary
        """
        
        #### director data
        sfpinfo = []
        sfp_combine = []
        all_ports = self.all_ports_fc_only()
        sfp_count = 0
        count16 = 0
        count8 = 0
        count4 = 0
        count10 = 0
        count_other = 0
        #print("\n\n\n\n")
        #print(all_ports)
        #print("@"*80)
        
        for i in all_ports:
            
            slot = i[0]
            port = i[1]
                
            capture_cmd = fos_cmd("sfpshow %s/%s " % (slot,port))
            ras = re.compile('(\d{1,2}(?=_G))')
            #ras = re.compile('Transceiver:\s+[\d\w]{16}\s+[,\d]?(\d{1,2}(?=_))')
            ras = ras.findall(capture_cmd)
            sfp_speed = -1
            
            #print("\n\n\n")
            #print(ras)
            #if ras != []:
            #    print("EMPTYSET")
            #print("\n\n\n\n")
            
            if ras != []:
                #print("\n\nSETTING THE SDFINFO info  \n")
                #print("with slot port speed %s  %s   %s : " % (slot, port, sfp_speed))
                sfp_speed = int(ras[0])
                sfp_combine = [slot,port,sfp_speed]
                sfpinfo.append(sfp_combine)
                #print("\n\nSETTING THE SDFINFO info  \n")
                #print("with slot port speed %s  %s   %s : " % (slot, port, sfp_speed))
                   
        sfp_combine = ""
        for i in sfpinfo:
            sfp_count += 1            
            if i[2] == 16:
                count16 += 1
            elif i[2] == 8:
                count8 += 1
            elif i[2] == 4:
                count4 += 1
            elif i[2] == 10:
                count10 +=1
            else:
                count_other +=1
            
        sfpinfo_summary = ["total sfp count = ", sfp_count, 16, count16, 8, count8, 4, count4, 10, count10, "other", count_other]
        
        
        
        
        #### return list or summary or details
        #### sfpinfo is list    sfp_summary
        if info_type == "summary":
            return(sfpinfo_summary)
        elif info_type == "detail":
            return(sfpinfo_detail)
        else:
            return(sfpinfo)

    def sim_ports(self, extended = True):
        """
            Return a list of the SIM ports in the current FID
            
        """
        extend_list = []
        index_address = []
        if extended :
            return(self.__getportlist__("SIM-Port"))
        else:
            self.__sw_show_info_all_ports__()
            
            location = 2
            if self.am_i_director:
                location = 3
                
            for i in self.online_ports:
               
                if 'SIM-Port' in i:
                    index_address.append(i[0])
                    index_address.append(i[location])
                    extend_list.append(index_address)
                    index_address = []
            return(extend_list)
    
    def switch_state(self):
        """
            Return the switch state 'Offline or Online'
            
        """
        while True:
            capture_cmd = fos_cmd("switchshow")
            ras = re.compile('switchState:\s+(\w{6,7})') 
            ras = ras.findall(capture_cmd)
            #print(ras)
            #print('TRYING TRY STATEMENT IN switch_state')
            #sys.exit()
            try:
                ss = str(ras[0])
                return(ss)
            except IndexError:
                liabhar.JustSleep(30)
               
    
    def switch_id(self ):
        """
           get the current switch
           does not work on AG switch
           
        """
        #### need a check for AG switch 
        try:
            capture_cmd = fos_cmd("switchshow")
            ras = re.compile('switchDomain:\s+(\d{1,3})') 
            ras = ras.findall(capture_cmd)
            sid = [int(i) for i in ras]
            sid = int(ras[0])
            return(sid)     
        except IndexError:
            return("AG")
    
    
    def switch_name(self ):
        """
           get the current switch Name from switchshow
           return the current switchname
        """
        capture_cmd = fos_cmd("switchshow")
        #ras = re.compile('switchName:\s+([_\d\wA-Za-z]{1,30})')
        ras = re.compile('switchName:\s+([_\-\d\wA-Za-z]{1,30})')###added "\-" to capture hyphen
        ras = ras.findall(capture_cmd)
        print(ras)
        sn = str(ras[0])
        return(sn)
    
    def switch_status(self):
        """
            Retrieve FCR fabric and return info. Variable #'s:
            0) Switch name
            1) IP address
            1) Chassis or Pizza Box
            2) VF or not
            3) FCR Enabled
            4) Base Configured
            
            return dictionary with {switch_name, ipaddr, chassis, vf_enabled, base, fcr_enabled}}
        """
        #fcrinfo = FcrInfo()
        initial_checks = self.__sw_basic_info__()
        #print("Switch Name :  %s" % initial_checks[0])
        #print("IP address :  %s" % initial_checks[1])
        #print("Chassis :  %s" % initial_checks[2])
        #print("VF enabled :  %s" % initial_checks[3])
        #print("FCR enabled :  %s" % initial_checks[4])
        #print("Base configured :  %s" % initial_checks[5])
        #print('='*20 + '\n\n')
        #switch_info = { 'switch_name' : initial_checks[0],'ipaddr' : initial_checks[1], 'chassis' : initial_checks[2],'vf_enabled' : initial_checks[3], 'fcr_enabled' : initial_checks[4], 'base' : initial_checks[5]}
        return(initial_checks)
    
    def switch_type(self):
        """
           get the current switch type number from switchshow
           return the type number
        """
        capture_cmd = fos_cmd("switchshow")
        ras = re.compile('switchType:\s+(\d{1,3})')
        ras = ras.findall(capture_cmd)
        try:
            sn = str(ras[0])
        except IndexError:
            
            sysexit()
        
        
        return(sn)
    
    
    def synchronized(self):
        """
            determine if a switch CP blades are in sync
        """
        
        capture_cmd = fos_cmd("hashow")
        
        if "Not supported" in capture_cmd:
            ss = self.switch_state()
            if ss == "Online":
             
                return(True)
            else:
                return(False)
            
        if "HA State synchronized" in capture_cmd:
            return(True)
        else:
            return(False)
    
    
    
    def temp_sensors(self, absent='no'):
        """
            find the tempsensors with OK state
        """
        if self.am_i_director:
            capture_cmd = fos_cmd("tempshow")
            ras = re.compile('\s?(\d+)\s+(\d+)\s+(Ok)\s+(\d+)\s+(\d+)') 
            ras = ras.findall(capture_cmd)
            
            if absent != "no":
                capture_cmd = fos_cmd("tempshow")
                ras = re.compile('\s?(\d+)\s+(\d+)\s+(Absent)\s+(\d+)\s+(\d+)') 
                ras = ras.findall(capture_cmd)
        else:
            capture_cmd = fos_cmd("tempshow")
            ras = re.compile('\s?(\d+)\s+(Ok)\s+(\d+)\s+(\d+)') 
            ras = ras.findall(capture_cmd)
            
            if absent != "no":
                capture_cmd = fos_cmd("tempshow")
                ras = re.compile('\s?(\d+)\s+(Absent)\s+(\d+)\s+(\d+)') 
                ras = ras.findall(capture_cmd)
            
            
        return(ras)
    
    def vf_enabled(self):
        """
            See if switch has vf enabled
            Return VF or noVF
            
        """
        #self.__change_fid__()
        #self.lscfgshow = lscfgshow
        capture_cmd = fos_cmd("lscfg --show" )
        foscfg = re.search( '(requires)', capture_cmd, re.M|re.I)
        if foscfg:
            #print("\n\n\nVF not enabled on this switch\n\n\n")
            return(False)
        else:
            #print("\n\n\nVF is enabled on this switch\n\n\n")
            return(True)

class FcrInfo(FabricInfo, SwitchInfo):
    """
    Class for FCR functions and information. Doc strings need to be added for some of the functions.
    """
    
    def __init__(self):
        SwitchInfo.__init__(self)
        FabricInfo.__init__(self) 

    def all_ex_ports(self):
        """
            Capture all ex ports for both Chassis and Pizza Box using "switchshow" command, 
        """
        fos_cmd("setcontext %s" % self.base_check()) ###################NEW
        capture_cmd = self.__getportlist__("EX-Port")
        return(capture_cmd)
    
    def all_ex_ports_with_edge_fid(self):
        """
            Capture all ex ports for both Chassis and Pizza Box using "switchshow" command. Returns
            slot # ("0" for pizzabox), port number, edge_fid.
        """
        if self.am_i_director:
            fos_cmd("setcontext %s" % self.base_check())
            capture_cmd = self.__getportlist__("EX-Port")
            ex = []
            for i in capture_cmd:
                slot = i[0]
                port = i[1]
                a = fos_cmd("portcfgexport %s/%s" % (slot, port))
                fid = (re.findall('Edge Fabric ID:\s+(\d{1,3})', a))
                fid = int(fid[0])
                ex_list = [slot, port, fid]
                ex.append(ex_list)
            return(ex)
        else:
            fos_cmd("setcontext %s" % self.base_check())
            capture_cmd = self.__getportlist__("EX-Port")
            ex = []
            for i in capture_cmd:
                a = fos_cmd("portcfgexport %s" % (i[1]))
                fid = (re.findall('Edge Fabric ID:\s+(\d{1,3})', a))
                fid = int(fid[0])
                ex_list = [int("0"), i[1], fid]
                ex.append(ex_list)
            return(ex)
    
    def all_switches_in_bb_ip(self):
        """
            Returns ip addresses of all switches in backbone fabric. Does not get edge switches.
        """
    
        backbone_ip = self.fcr_backbone_ip()
        return(backbone_ip)
    
    def fcr_backbone_ip(self):
        """
        Runs fabricshow against backbone switches in a fabric to determine all IPs
        02/10/15 checked
        #print('\n\n'+ '='*20)
        #print("Switch Name :  %s" % initial_checks[0])
        #print("IP address :  %s" % initial_checks[1])
        #print("Chassis :  %s" % initial_checks[2])
        #print("VF enabled :  %s" % initial_checks[3])
        #print("FCR enabled :  %s" % initial_checks[4])
        #print("Base configured :  %s" % initial_checks[5])
        #print('='*20 + '\n\n')
        """
        fcrcfg = FcrInfo()
        fcrstatus = self.__sw_basic_info__()
        if fcrstatus[5] is not False:  # Test if base config'd and if so
            base = fcrstatus[5] ###fcrcfg.base_check() # get the base FID number
            f = FabricInfo(base) ###########NEW OBJECT FOR BASE FID
            get_fabric_ip = f.ipv4_list() ###########NEW OBJECT FOR BASE FID
        else:
            get_fabric_ip = fcrcfg.ipv4_list()
        return(get_fabric_ip)
    
    def fcr_fab_wide_ip(self):
        """
            ******************MUST BE RUN IN BASE IF VF IS USED *******************************
            Runs fcrfabricshow and fabricshow against switches in a backbone fabric to determine all IPs then
            removes any duplicate entries.
            This includes both backbone and edge switches and any additional switches resident in edge fabrics.
            Return is a list of IPs.
        """
         
        fci = FcrInfo()
        fcrstatus = self.__sw_basic_info__()
        if fcrstatus[3] is not False:  # Test if base config'd and if so
            base = fci.base_check() # get the base FID number
            f = FabricInfo(base) ###########NEW OBJECT FOR BASE FID
            # print(f)
            # sys.exit()
            get_fabric_ip = f.ipv4_list() ###########NEW OBJECT FOR BASE FID
        else:
            get_fabric_ip = fci.ipv4_list()
        get_fcr_fabric = self.ipv4_fcr()
        #try:
        fcr_fab_ip_list = (get_fabric_ip + get_fcr_fabric)
        # except TypeError:
        #     print("\n############################")
        #     print("Either fcrfabricshow and/or fabricshow are coming up as not available or not there.")
        #     print("Or this script must be run from a base switch if VF is set")
        #     print("############################\n")
        #     sys.exit()
        all_ips = []
        for ip in fcr_fab_ip_list:
            connect_tel_noparse(ip,'root','password')
            get_fabric_ip = fci.ipv4_list()
        entire_fcr_fab_ip_list = (get_fabric_ip + fcr_fab_ip_list)
        all_ips = (set(entire_fcr_fab_ip_list))
        final_ip_list = (list(all_ips))
        return(final_ip_list)

    def fcr_proxy_dev(self):
        """
        Get number of proxy devices reported by a switch
        
        """
        fos_cmd("setcontext %s" % self.base_check())
        cmd_capture = fos_cmd("fcrproxydevshow -a | grep device")
        print(cmd_capture)
        device_number = re.findall(':\s([0-9]{1,4})', cmd_capture)
        return(device_number)
    
    def get_licenses(self):
        """
        Query all switches in both bacakbone and edges, capture "licenseshow" command
        and write licenses to a file in /home/RunFromHere/logs/Switch_Licenses/<switchname>
        """
        ip_list = self.fcr_fab_wide_ip()
        for ip in ip_list:
            connect_tel_noparse(ip,'root','password')
            sw_info = SwitchInfo()
            sw_name = sw_info.switch_name()
            f = "%s%s%s"%("logs/Switch_Licenses/License_File_", sw_name ,".txt")
            ff = liabhar.FileStuff(f,'a+b') ###open new file or clobber old
            header = "%s%s%s%s" % ("\nLICENSE FILE \n", ip+"\n" , sw_name, "\n==============================\n\n")
            cons_out = fos_cmd("licenseshow")
            ff.write(header)
            ff.write(cons_out+"\n")
            ff.close()
        return(True)

    def ipv4_fcr(self):
        """
            Return a string (list) ipv4 address of switch\switches connected
            to FCR Router thru EX-Port
        """
        #self.__change_fid__()
        fos_cmd("setcontext %s" % self.base_check())
        capture_cmd = fos_cmd("fcrfabricshow")
        
        ras = re.compile('(?:\d{1,3}\s+\d{1,3}\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd)
            
        if not ras_result_all:
            ras_result_all = None 
        return(ras_result_all)

    def ipv4_fid_export_fcr(self):
        """
            Return a string (list) containing EX-Port number, FID and ipv4 address of switch\switches connected
            to FCR Router thru EX-Port
        """
        #self.__change_fid__()
        capture_cmd = fos_cmd("fcrfabricshow")
        ras = re.compile('(\d{1,3})\s+(\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd) 
        if not ras_result_all:
            ras_result_all = None
        return(ras_result_all) 

    def portcfgfillword(self, cfgvalue):
        """
            NEED TO TEST DIRECTOR. PIZZA BOX WORKING
            applies OPTION "3" TO portcfgfillword command. Suggested cfgvalue = 3
            Will try against all ports in given fid/switch with FOS rejecting
            all but C2 (8GB) ports.
        """
        fos_cmd("switchdisable")
        portlist =  self.all_ports()
        if self.am_i_director:
           for i in portlist:
                slot = i[0]
                port = i[1]
                fos_cmd("\r")
                #fos_cmd("portcfgfillword "+slot+"/"+port+" "+ cfgvalue )
                fos_cmd("portcfgfillword %s"/"%s %s %" (slot, port, cfgvalue))
                fos_cmd("\r")
        else: 
            for i in portlist:
                port = str(i[1])
                fos_cmd("\r")
                fos_cmd("portcfgfillword %s %s" % (port, cfgvalue))
        cmd_cap = fos_cmd("switchenable")
        return(cmd_cap)
    
    def playback_fosconfig_fcr(self):
        """
        Enable/Disable FCR functionality per "logs/Switch_Info_for_playback_",self.switch_ip,".txt"
        This function lives in cofra.switch_update()
        """
    
        f = ("logs/Switch_Info_for_playback_10.38.134.30.txt")
        try:
            with open(f, 'r') as file:
                a = file.read()
        except IOError:
            print("\n\nThere was a problem opening the file:" , f)
            sys.exit()        
        ras_fcr = re.findall('FCR ENABLED\s+:\s+([True0-9]+)', a)
        #ras_base = re.findall('BASE SWITCH\s+:\s+([TrueFals0-9]+)', a)
        #ras_vf_enabled = re.findall('VF SETTING\s+:\s([TrueFals0-9]+)', a)

        print("@"*44)
        print(type(ras_fcr))
        print(ras_fcr)
        print("@"*44)
        
        if ras_fcr:
            fos_cmd("fosconfig --enable fcr")
        else:
            fos_cmd("fosconfig --disable fcr")
        return(True)
        
class FcipInfo(FcrInfo, FabricInfo, SwitchInfo):
    """
        A class to return information about a switch
    Class for FCIP functions and information.
    """
    #global tn
    
    def __init__(self):
        FcrInfo.__init__(self)
        FabricInfo.__init__(self)
        SwitchInfo.__init__(self)

        
    def __sw_show_info_ge_port_type__(self):
        """
            capture the switch info and each column with regexs
            if the port type is not included in switchshow output
            then add the port to the list
        """
        #tn.set_debuglevel(9)
        capture_cmd = fos_cmd("switchshow")
        if self.am_i_director:
            ras = re.compile('\s?([0-9]{1,3})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
        else:
            #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
            ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9a-f]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
        ras = ras.findall(capture_cmd)
        self.online_ports = ras
 
    def all_online_ge_ports(self):
        """
        02/09/2015 checked
            Capture all online ge and xge ports.
            On chassis and pizzaboxes only catches ge ports in base(if base configured).
        """
        base = self.base_check()
        #initial_checks = self.__sw_basic_info__()
        #print('\n\n'+ '='*20)
        #print("Switch Name :  %s" % initial_checks[0])
        #print("IP address :  %s" % initial_checks[1])
        #print("Chassis :  %s" % initial_checks[2])
        #print("VF enabled :  %s" % initial_checks[3])
        #print("FCR enabled :  %s" % initial_checks[4])
        #print("Base configured :  %s" % initial_checks[5])
        #print('='*20 + '\n\n')
        #switch_info = { 'switch_name' : initial_checks[0],'ipaddr' : initial_checks[1], 'chassis' : initial_checks[2],'vf_enabled' : initial_checks[3], 'fcr_enabled' : initial_checks[4], 'base' : initial_checks[5]}
        online_ports = []
        if self.am_i_director:
            if base:
                fos_cmd("setcontext " + base)
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            else:
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            ras = re.compile('(?:\s+([0-9]{1,2})\s{1,2})([xge]{1,3}\d{1,2})\s+id\s+([0-4]{1,2}G)\s+([_\w]{5,9})\s+.{3,4}')
            ras = ras.findall(capture_cmd)
            for i in ras:
                if "Online" in i:
                    print(i)
                    online_ports.append(i)
            #print(online_ports)    
            return(online_ports)
        else:
            if base:
                fos_cmd("setcontext " + base)
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            else:
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            ras = re.compile('(?:\s+)([xge]{1,3}\d{1,2})\s+[id-]{1,2}\s+([0-4]{1,2}G)\s+([_\w]{5,9})\s+.{3,4}')
            ras = ras.findall(capture_cmd)
            #print(ras)
            for i in ras:
                if "Online" in i:
                    print(i)
                    online_ports.append(i)
            #print(online_ports)    
            return(online_ports)
    
    def all_ge_port_disabled(self):
        """
            Capture all disabled ge and xge ports.
            On chassis and pizzaboxes only catches ge ports in base(if base configured).
        """
        base = self.base_check()
        disabled_ports = []
        if self.am_i_director:
            if base:
                fos_cmd("setcontext " + base)
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            else:
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            print(capture_cmd)
            ras = re.compile('(?:\s+)([xge]{1,3}\d{1,2})\s+[id-]{1,2}\s+([0-4]{1,2}G)\s+([_\w]{3,9})\s+.{3,4}\s+(Disabled)')
            ras = ras.findall(capture_cmd)
            for i in ras:
                if "Disabled" in i:
                    print(i)
                    disabled_ports.append(i)
            #print(online_ports)    
            return(disabled_ports)
        else:
            if base:
                fos_cmd("setcontext " + base)
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            else:
                capture_cmd = fos_cmd("switchshow | grep -i ge")
            ras = re.compile('(?:\s+)([xge]{1,3}\d{1,2})\s+[id-]{1,2}\s+([0-4]{1,2}G)\s+([_\w]{3,9})\s+.{3,4}\s+(Disabled)')
            #ras = re.compile('(?:\s+([0-9]{1,2})\s{1,2})([xge]{1,3}\d{1,2})\s+id\s+([0-4]{1,2}G)\s+([_\w]{5,9})\s+.{3,4}\s+Disabled')
            ras = ras.findall(capture_cmd)
            #print(ras)
            #for i in ras:
            #    print(i)
            #sys.exit()
            #    if "Disabled" in i:
            #        print(i)
            #        disabled_ports.append(i)
            ##print(online_ports)    
            return(disabled_ports)
        
    def vex_ports(self):
        """
            Return a list of the VEX-Ports in the current FID
        """
        return(self.__getportlist__("VEX-Port"))
    
    def ex_ports(self):
        """
            Return a list of the EX-Ports in the current FID
        """
        return(self.__getportlist__("EX-Port"))
    
    def all_ge_ports(self):
        """
            Return a list of the ge-Ports in the current FID
        """
        return(self.__getportlist__("ge-Port"))
        
class ConfigSwitch(SwitchInfo):
    
    
    
    def cfgupload(self):
        fos_cmd("configupload")
    
    
    def getLsPorts(self):
        rasfile = "configofswitch"
        rasfile = "%s%s%s" % ("logs/configofswitch", self.ipaddr,".txt")  #### %s string  %d number
     
        sw_license = str(self.getLicense())
        sw_license = sw_license.replace("'", '')
        sw_ls_list = self.ls()
        sw_ls = str(sw_ls_list)
        sw_ls = sw_ls.replace("'", '')
            
        ras_log_file = liabhar.FileStuff(rasfile, 'w+b')  #### reset the log file
        ras_log_file.close()
        
        ras_log_file = liabhar.FileStuff(rasfile, 'a+b')  #### open the log file for writing
        ras_log_header = "%s%s%s" % ("RASLOG CAPTURE FILE \n", self.ipaddr, "\n==========================\n\n")
        
        ras_log_file.write(ras_log_header)
        ras_log_file.write("\nLOGICAL SWITCHES::\n")
        ras_log_file.write(sw_ls+"\nEND\n")
        ras_log_file.write("\nLOGICAL SWITCH PORTS::\n")
        
        print("\n\nget the list of ports\n\n")
        for ls in sw_ls_list:
            print("\n\nin the for loop "+ls+" \n\n")
            capture_cmd = fos_cmd("setcontext %s"% ls)
            p = self.all_ports()
            p = str(p)
            p = p.replace("'", '')
            ras_log_file.write("%s : %s\n"%(ls, p))
        #ras_log_file.write("\n")
        ras_log_file.write("END\n")
        ras_log_file.write("\nLICENSE::\n")
        ras_log_file.write(sw_license)
        ras_log_file.write("END\n")
        ras_log_file.close()
        
        self.saveSwitchInfo()
        
    def getSwitchID(self):
        return(self.switch_id())
        
     
    def saveSwitchInfo(self):
        """
            get license info
            get ls info and base info
            get switchname info
            get switch id info
            
            save to config file logs/sqa_test_config.txt
            
            NOT WORKING. OBSOLETE?????
            
        """
        cw_config_file_name = "%s%s%s" %("logs/configofswitch", self.ipaddr,".txt")
        #rl = [] 
        fileIN = open( cw_config_file_name, 'rb')
        keepnext = 0
        for line in fileIN:
            print("0000000000000000000000000000000000000000000000")
            print(line)
            print("11111111111111111111111111111111111111111111111")
            liabhar. count_down(1)
            line_str = str(line)
            remains_line = str(line.strip(), encoding='utf8')
            remains_line = remains_line.replace("[", '')
            remains_line = remains_line.replace("]", '')
            remains_line = remains_line.replace("(", '')
            remains_line = remains_line.replace(")", '')
            
            if "END" in line_str:
                keepnext = 0   
                 
            if keepnext:
                rl = []
                print("2222222222222222222222222222222222222222222222")
                print("do some setup here\n")
                print("split on , and print a digit")
                 
                fid2 = remains_line
                fid2 = fid2.split(":") 
                fid3 = fid2[0]
                
                print("FID3 IS  ")
                print(fid3)
                print("FID2 IS  ")
                print(fid2)
                print("\n\n")
                fid4 = fid2[1]
                fid4 = str(fid4)
                fid4 = fid4.split(",")
                #remains_line = remains_line.split(",")
                
                for i in fid4:
                    print(i)
                    rl.append(i)
                print("==============================================")
                for r in rl:
                    print(r)
                print("2222222222222222222222222222222222222222222222")
                ########'Are you sure you want to fail over to the standby '

                #### create slot port pair from the list 
                if len(rl) >= 2:
                    for index in range(0,len(rl),2):
                        slot = rl[index]
                        port = rl[index +1]
                        print("slot,port ", end="" )
                        print(slot+","+port)
                
                print("2222222222222222222222222222222222222222222222")
                print("2222222222222222222222222222222222222222222222")
                
                
            if "LOGICAL SWITCH PORTS" in line_str:
                keepnext = 1
                print("change keepnext to 1")
                
    def config_default(self):
        """
        Do switchconfigdefault on FID used in CLI only.
        Switch needs to be offline, rebooted and brought back online.
        """
        
        host = sys.argv[1]
        user = sys.argv[2]
        password = sys.argv[7]
        state = SwitchInfo.switch_state(self)
        if state == "Online":
            fos_cmd("switchdisable")
        else:
            pass
        fos_cmd("echo Y | configdefault")
        fos_cmd("echo Y | reboot")
        liabhar.count_down(120)
        connect_tel_noparse(host, user, password)
        fos_cmd("switchenable")
        liabhar.count_down(10)
        state = SwitchInfo.switch_state(self)
        return(state)

class Maps(SwitchInfo):
    
    def enable(self, policy ):
        return(fos_cmd("echo Y | mapsconfig --enable -policy %s " % policy))
                
    def actions(self, action_list ):
        return(fos_cmd("mapsconfig --actions %s " % action_list))

    def email_cfg(self, email_list ):
        return(fos_cmd("mapsconfig --emailcfg -address %s " % email_list))

    def get_email_cfg(self):
        """
        
        """
        
        capture_cmd = fos_cmd("mapsconfig --show")
        ras = re.compile('Mail Recipient:\s+([\._@0-9a-zA-Z]+)')
        ras = ras.findall(capture_cmd)
        
        return(ras)
    
    def get_actions(self):
        """
        """
        
        capture_cmd = fos_cmd("mapsconfig --show")
        ras = re.compile('Notifications:\s+([\._@0-9a-zA-Z ,]+)')
        ras = ras.findall(capture_cmd)
        
        return(ras)
        
    def get_rules(self):
        capture_cmd = fos_cmd("mapsrule --show -all")
        ras = re.compile('(def[ A-Z0-9nm_]{0,40}(?:|[_A_Z]+\())')
        ras = ras.findall(capture_cmd)
        ras = str(ras)
        ras = ras.replace("'","")
        ras = ras.replace("[","")
        ras = ras.replace("]","")
        ras = ras.replace(",","")
        ras = ras.replace("|,", "")
        
        return(ras)

         
        
    def get_policies(self, p = 's' ):
        #### ruturn the policy rules list for p
        ####  a = aggresive policy
        ####  c = conservative policy
        ####  m = moderate policy
        ####  s or none = summary of policy
        
        if p == "s":
            capture_cmd = fos_cmd("mapspolicy --show -summary")
            ras = re.compile('([_\w\d]+)\s+(?=:)')
            ras = ras.findall(capture_cmd)
            
            return(ras)
        
        elif p == "a":
            return(fos_cmd("mapspolicy --show -dflt_aggressive_policy"))
        elif p == "c":
            return(fos_cmd("mapspolicy --show -dflt_conservative_policy"))
        elif p == "m":
            return(fos_cmd("mapspolicy --show -dflt_moderate_policy"))
        elif p == "b":
            return(fos_cmd("mapspolicy --show -dflt_base_policy"))
        else:
            return("Could not determine the type of policy")
    
    def get_nondflt_policies(self):
        """
            get the policies in a list of the non default policies
            need to remove the default policies
        """
        capture_cmd = fos_cmd("mapspolicy --show -summary")
        ras = re.compile('([_\w\d]+)\s+(?=:)')
        
        ras = ras.findall(capture_cmd)
        
        dp = [ "dflt_aggressive_policy", "dflt_moderate_policy", "dflt_conservative_policy", "dflt_base_policy" ]
        for p in dp :
            try:
                ras.remove(p)
            except ValueError:
                pass
 
        return(ras)
    
    def get_active_policy(self):
        """
        get the active policy of MAPS
        
        Active Policy is 'dflt_aggressive_policy'.
        
        """
        
        capture_cmd = fos_cmd("mapspolicy --show -summary")
        ras = re.compile("Active Policy is '([_\w\d]+)'")
        
        ras = ras.findall(capture_cmd)
        
        return(ras)
        
    
    
    def get_relay_server_info(self):
        """
            Relay Host: 
            Relay Domain Name: 
        """
        
        capture_cmd = fos_cmd("relayconfig --show")
        ras_host = re.compile('Relay Host:\s+([\.0-9:]+)')
        ras_domain = re.compile('Relay Domain Name:\s+([\.A-Za-z]+)')
        ras_host = ras_host.findall(capture_cmd)
        ras_domain = ras_domain.findall(capture_cmd)
        
        relay_info = str(ras_host) + " " + str(ras_domain)
        
        
        return(relay_info)
        
    
        
    def db_search(self, pattern ):
        """
            send the mapsdb command and return search string line
            for a Rule_name and returns the info on the
            rest of the line
            
        """
        capture_cmd = fos_cmd("mapsdb --show details")
        #### %s=Rule Name |Execution time|Object             | triggered value
        repattern = "(%s)([ |/:\d]+(?=|))([ \w\d\s\\t]+)(?=|)([ \w\d\s\\t%s]+(?=|))" % (pattern, "%")
        repattern = "(%s)([ |/:\d]+(?=|))([ \w\d\s\\t]+)(?=|)(.+)" % (pattern)
        
        
        #ras = re.compile('(%s)[ |/:\d]+(?=|)([ \w\d\s|%]+)(?=\\n)' % pattern)
        print("R"*80)
        print("R"*80)
        print(repattern)
        print("U"*80)
        print("U"*80)
        ras = re.compile(repattern)
        ras = ras.search(str(capture_cmd))
        
        #output = ras.replace("|","")
        #output = output.split(" ")
        
        if ras:
            return(ras.group())
            #return(output)
        else:
            return("no match found")
        
        
    def ras_message_search(self, pattern):
        """
           search the errlog for a specific pattern
           
        """
        cap = fos_cmd("tempshow", 9 )
        print("TEMP"*20)
        print("TEMP"*20)
        print("TEMP"*20)
        print(cap)
        
        
        capture_cmd = fos_cmd("errdumpall", 9 )
        
        print("SHOW"*20)
        print("SHOW"*20)
        print("SHOW"*20)
        print("SHOW"*20)
        
        
        ras = re.compile("(%s)" % pattern)
         
        ras = ras.search(str(capture_cmd))
                 
        if ras:
            return(ras.group())
        else:
            return("no match found")
    
        return(0)
    
        
    def logicalgroup_count(self, group="ALL"):
        """
            return the count for the line group passed for any of the following
            
            ALL_PORTS
            ALL_F_PORTS         ALL_OTHER_F_PORTS       ALL_HOST_PORTS    
            ALL_TARGET_PORTS    ALL_TS                  ALL_FAN        
            ALL_PS              ALL_WWN                 ALL_SFP        
            ALL_10GSWL_SFP      ALL_10GLWL_SFP          ALL_16GSWL_SFP 
            ALL_16GLWL_SFP      ALL_QSFP                ALL_OTHER_SFP  
            ALL_SLOTS           ALL_SW_BLADES           ALL_CORE_BLADES 
            ALL_FLASH           ALL_CIRCUITS            SWITCH     
            CHASSIS             ALL_D_PORTS
            
        """
        ###############################################################################################################
        ###############################################################################################################
        ####
        #### return a list of all the values
        ####
        ###############################################################################################################
         
         
        if group == "ALL":
            capture_cmd = fos_cmd("logicalgroup --show")
            #ras = re.compile("(ALL_SW_BLADES)\s+(?:\|)(Yes)\s+\|(Blade)\s+(?:\|)([0-9])\s+(?:\|)([,0-9])")
            ras = re.compile("([_A-Z0-9]+)\s+\|Yes\s+\|[ \w]+\|([0-9]+)")    
            #ras = ras.search(capture_cmd)
            ras = ras.findall(capture_cmd)
            if not ras:
                value = "-1"
            else:
                print("\nTHIS IS RAS  \n")
                print(ras)
             
            #liabhar.JustSleep(110)
             
            return(ras)
        
        else:
            capture_cmd = fos_cmd("logicalgroup --show")
                
            #ras = re.compile("(ALL_SW_BLADES)\s+(?:\|)(Yes)\s+\|(Blade)\s+(?:\|)([0-9])\s+(?:\|)([,0-9])")
            ras = re.compile("(%s)\s+\|Yes\s+\|[ \w]+\|([0-9]+)" % group)    
            #ras = ras.search(capture_cmd)
            ras = ras.findall(capture_cmd)
            if not ras:
                value = "-1"
            else:
                print("\nTHIS IS RAS  \n")
                print(ras)
                print("\nTHIS IS RAS GROUP \n")
                print(ras[0][1])
                       
                value = ras[0][1]
                #liabhar.JustSleep(10)
            return(value)

    def cpu_usage(self):
        """
           calculate the cpu usage from the data
           in /proc/stat
           the numbers are captured in /proc/stat
           wait 2 minutes and capture the numbers again
           make the calculation
           
        """
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
        capture_cmd = fos_cmd("cat /proc/stat")
        ras = re.compile("^[ cpu]+([ \s\d]+)")
        ras = ras.match(capture_cmd)
        
        cpu_calc = (ras.group()).split()
        sumt1 = ( float(cpu_calc[1]) + float(cpu_calc[2]) + float(cpu_calc[3]) \
                 + float(cpu_calc[4]) + float(cpu_calc[5]) + float(cpu_calc[6])\
                 + float(cpu_calc[7]))
        liabhar.JustSleep(120)
        capture_cmd = fos_cmd("cat /proc/stat")
        ras = re.compile("^[ cpu]+([ \s\d]+)")
        ras = ras.match(capture_cmd)
        
        cpu_calcT2 = (ras.group()).split()
        sumt2 = ( float(cpu_calcT2[1]) + float(cpu_calcT2[2])  \
                 + float(cpu_calcT2[3]) + float(cpu_calcT2[4]) \
                 + float(cpu_calcT2[5]) + float(cpu_calcT2[6]) \
                 + float(cpu_calcT2[7]))
        
        #cpu_use = (100 - (((float(cpu_calc[4]) - float(cpu_calcT2[4]))*100)/(sumt1 - sumt2)))
        cpu_use_n = ((float(cpu_calc[4]) - float(cpu_calcT2[4])) *100)
        cpu_use_d = (sumt1 - sumt2)
        cpu_use  = (round(100-( cpu_use_n / cpu_use_d),2) ) 
    
        return(cpu_use)
    
    
    
    def temp_status(self):
        """
           scan all the temp sensors and return the high temp, low temp
           and average temp of the switch using the tempshow command
           
        """
        #capture_cmd = fos_cmd("tempshow")
        #
        #ras = re.compile("\d+\s+\w+\s+\d+\s+\d+")
        #ras = ras.findall(capture_cmd)
        #ras_str = str(ras)
        #ras_str = ras_str.replace("\\t"," ")
        #ras_str = ras_str.replace("'", "")
        #ras_str = ras_str.replace("[", "")
        #ras_str = ras_str.replace("]", "")
        ##ras_str = ras_str.replace(" ", "")
        #ras_final = " ".join(ras_str.split())
        #
        #ras_final = ras_final.split()
        
        tempsensor_list = self.temp_sensors()
        
        highside = -1
        lowside = 999
        average = -1
        count = 0
        total = 0
        
        if self.am_i_director:
            for i in tempsensor_list:
                if int(i[3]) > highside:
                    highside = int(i[3]) 
                if int(i[3]) < lowside:
                    lowside = int(i[3])
                count = count + 1
                total = total + int(i[3])
        else:
            for i in tempsensor_list:
                if int(i[2]) > highside:
                    highside = int(i[2]) 
                if int(i[2]) < lowside:
                    lowside = int(i[2])
                count = count + 1
                total = total + int(i[3])
             
        average = total / count
        high_low_average = [ highside, lowside, average]
        
        return(high_low_average)
    
        
    def mem_usage(self):
        """
            calculate the memory usage from the data
            returned in the command free
        """
        capture_cmd = fos_cmd("free")
        ras = re.compile("[Mem:]{4}([ \s\d]+)")
        ras = ras.search(capture_cmd)
        ####  use the calculation (total - free - buffers - cached)/ total
        ####    ( 1024096 - 351328 - 40884 - 379300 ) / 1024096 = 25%
        ####
        mem_calc = (ras.group()).split()
        mem_use = float( float(mem_calc[1]) - float(mem_calc[3]) - float(mem_calc[5]) - float(mem_calc[6]) )
        mem_use = (100 * round( mem_use / float(mem_calc[1]), 2))
        
        return(mem_use)
    
class FlowV(SwitchInfo):
    
    def genAll(self, on_off = "on"):
        if on_off == "on":
            fos_cmd("flow --activate sys_gen_all_simports -fea gen")
        elif on_off == "off":
            fos_cmd("flow --deactivate sys_gen_all_simports -fea gen")
        else:
            pass
        
    def genAllStats(self):
        cmd_out = fos_cmd("flow --show sys_gen_all_simports")
        ras = re.compile('(?<=[:\s+])(\d+\.?\d+[GMTPk]?)')
        ras = re.compile('(?<=[:\s+])(\d+[\.\dGMTPk]+)')
        ras = ras.findall(cmd_out)
        st = ""
        for s in ras:
            st = st + s
            st = st + "\t\t"
        st = st + "\n"
        return(st)
        
    def flow_names(self):
        """
            get all the flow names return in a list
            
        """
        cmd_out = fos_cmd("flow --show ")
        
        #print("\n\n\n",cmd_out , "\n\n\n\n")
        #ras = re.compile('([_-a-z0-9A-z]{1,20})[ \|]+[\*,-|a-zA-Z0-9]+(?=\n)')
        ras = re.compile('\n([_a-z0-9A-Z]{1,20})\s+(?=|)')
        ras = ras.findall(cmd_out)
        
        #print(ras)
        return(ras)
    
    def get_nondflt_flows(self):
        """
        
        """
        cmd_out = fos_cmd("flow --show ")
        
        #print("\n\n\n",cmd_out , "\n\n\n\n")
        #ras = re.compile('([_-a-z0-9A-z]{1,20})[ \|]+[\*,-|a-zA-Z0-9]+(?=\n)')
        ras = re.compile('\n([_a-z0-9A-Z]{1,20})\s+(?=|)')
        ras = ras.findall(cmd_out)
        
        df = [ "sys_gen_all_simports", "sys_analytics_vtap", "sys_mon_all_fports", "sys_mon_all_vms" ]
        for d in df:
            try:
                ras.remove(d)
            except ValueError:
                pass
        
        return(ras)
        
    def get_active_flows(self):
        """
         get the active flows only
         
            mon_eport_38        |mon+
        
        
        """
        cmd_out = fos_cmd("flow --show ")

        ras = re.compile('\n([_a-z0-9A-Z]{1,20})\s*\|[mongeir]{3,3}\+')
        ras = ras.findall(cmd_out)
        
        return(ras)
        
    def get_flow_details(self):
        """
        
        """
        cmd_out = fos_cmd("flow --show ")

        ras = re.compile('\n([_a-z0-9A-Z]{1,20})\s*\|[+mongeir]{3,4}\s+\|([-*0-9a-f]{1,6})\s+\|([-*0-9a-f]{1,6})\s+\|([-*0-9]{1,4})\s+\|([-*0-9]{1,4})\s+\|([a-z]{1,5})\s+\|([-0-9]{1,5})\s+\|([-_A-Za-z0-9]{1,16})\s*\|([-A-Za-z0-9]{1,4})\s*\|([-A-Za-z0-9]{1,4})\s*\|([ -_A-Za-z0-9]{1,47})\s*\|([-,0-9]{1,6})')
        ras = ras.findall(cmd_out)
        
        return(ras)
    
    def get_egr_stats(self, act_flow):
        """
        
        
        """
        
        cmd_out = fos_cmd("flow --show %s "% act_flow)
        
        
        return(cmd_out)
        
    
    def flow_config(self):
        """
          the flow configuration
          
        """
        
        cmd_out = fos_cmd("flow --show")
        
        return(cmd_out)
    
    def simPorts(self):
        
        return 0 
    
    
    def toggle_all(self, on_off = "on"):
        """
            simport enable or disable
            default is to turn all ports to simports
            
        """
        state = "-enable"
        if on_off == "off":
            state = "-disable"
            
        portlist =  self.all_ports()
        print(portlist)
         
        
        if self.am_i_director:
            for i in portlist:
                slot = i[0]
                port = i[1]
                #pattern = re.compile(r'(?:\Sim\sPort\s+)(?P<state> ON)')
                #cmd = fos_cmd("portcfgshow %a/%a" % (slot, port))
                #ex = pattern.search(cmd)
                #if ex:
                fos_cmd("flow --control -simport %s/%s %s" %(slot, port, state))
                #fos_cmd("flow --control -simport "+slot+"/"+port+" %s"%(state))
                
                
        else: 
            for i in portlist:
                #pattern = re.compile(r'(?:\Sim\sPort\s+)(?P<state> ON)')
                #cmd = fos_cmd("portcfgshow %a" % i)
                #ex = pattern.search(cmd)
                #if ex:
                fos_cmd("flow --control -simport %s %s " %(i, state))
                #fos_cmd("flow --control -simport "+i+" %s"%(state))
              
        return(portlist)

def login(pw=""):
    pa = liabhar.parse_args(sys.argv)
    if pw == "":
        pw = getpass.getpass()
    conn_value = connect_tel(pa,pw)
    return(conn_value)

def close_tel():
    global tn
    tn.write(b"exit\n")
    tn.close()
    return 0
   
def connect_tel(pa, pw):
    global tn
    try:
        fid = pa.fid
        verbose = pa.verbose
        HOST = pa.ip
        usrname = pa.user
        password = pw
        
        usrn = usrname + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        bad_login = "Login incorrect"
        bad_login = bad_login.encode()
        reg_ex_list = [b"hlogin: ", b"Password: ", b"option :", b"root>", usrn, telnet_closed, bad_login ]
        #print(HOST)
        #print(usrname)
        #print(password)
        tn = telnetlib.Telnet(HOST)
        tn.set_debuglevel(0)
        tn.read_until(b"login: ")
        tn.write(usrname.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
            capture = tn.expect(reg_ex_list, 10)
            capture_t = capture
            capture = capture[2]
            badlog0 = capture_t[0]
            capture = capture.decode()
        if badlog0 == 6:
            print("Could not connect at this time")
            print("Try again with a correct username / password combination")
            print("\n========================================================\n\n\n")
            tn.write(usrname.encode('ascii') + b"\n")
            
            if password:
                tn.read_until(b"assword: ")
                p_fibranne = "fibranne" 
                tn.write(p_fibranne.encode('ascii') + b"\n")
                capture = tn.expect(reg_ex_list, 10)
                capture_t = capture
                capture = capture[2]
                badlog0 = capture_t[0]
                capture = capture.decode()
                #sys.exit()
            
        
        print(capture)
        con_out = fos_cmd("")
        con_out = fos_cmd("setcontext %s"%(fid))
        print(con_out)
        
        return(tn)      
    
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print(" anturlar  connect_tel  ")
        print("========================")
        pass
        
def connect_tel_noparse(HOST,usrname,password, *args):
    global tn
    try:
        
        usrn = usrname + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        bad_login = "Login incorrect"
        bad_login = bad_login.encode()
        traff_server = " ~]# "
        #traff_prompt = "----------"
        traff_prompt = " ~]# "
        traff_server = traff_server.encode()
        
        reg_ex_list = [b"hlogin: ", b"assword: ", b"option :", b"root>", usrn, telnet_closed, bad_login, traff_server, b"key to proceed"]
        #print(HOST)
        #print(usrname)
        #print(password)
        tn = telnetlib.Telnet(HOST)
        tn.set_debuglevel(0)
        tn.read_until(b"login: ")
        tn.write(usrname.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
            capture = tn.expect(reg_ex_list, 10)
            capture_t = capture
             
            capture = capture[2]
            
            badlog0 = capture_t[0]
            capture = capture.decode()
        if badlog0 == 6:
            print("Could not connect at this time")
            print("Try again with a correct username / password combination")
            print("\n========================================================\n\n\n")
            tn.write(usrname.encode('ascii') + b"\n")
            
            if password:
                tn.read_until(b"assword: ")
                p_fibranne = "fibranne" 
                tn.write(p_fibranne.encode('ascii') + b"\n")
                capture = tn.expect(reg_ex_list, 10)
                capture_t = capture
                capture_k = capture
                capture = capture[2]
                badlog0 = capture_t[0]
                capture = capture.decode()
            #sys.exit()
            #print("\n"*35)
            #print("\n========================================================\n"*20)
            #print("\nIN ANTURLAR  TELNET NOPARE login with fibranne  ")
            #print("\n========================================================\n"*20)
            #print(capture)
            #print(type(capture))
            #capture_k = capture_k[0]
            #print("CAPTURE K   \n\n")
            #print(capture_k)
            #print("CAPTURE K   \n\n\n\n\n\n")
            
            if capture_k == 8:
                print("FOUND THE key to proceed WORDS")
                print(capture_k)
             
            #if str("key to proceed") in capture:
                tn.write(b"\n")
                capture = tn.expect(reg_ex_list, 10)
                print("\n=================== found the key ==========================="*10)
                print(capture)
                tn.write(b"fibranne\n")
                capture = tn.expect(reg_ex_list, 10)
                while capture[0] == 1:
                    tn.write(password.encode('ascii') + b"\n")
                    capture = tn.expect(reg_ex_list, 10)
            else:
                print("DID NOT       FIND Key to proceed")
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"*20)
                sys.exit()
             
        #print("\nLEAVING LOGIN PROCEDURE             "*20)    
        print(capture)
        return(tn)      
    
    except EOFError:
        print("==================================")
        print("  handle the EOF case here        ")
        print("   anturlar  connect_tel_no_parse ")
        print("==================================")
        sys.exit()
        
    
def connect_tel_noparse_power(HOST,usrname,password, *args):
    global tn
    try:
        
        usrn = usrname + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        bad_login = "Login incorrect"
        bad_login = bad_login.encode()
        reg_ex_list = [b"cli->", b"\$ " ]# b"Password: ", b"option :", b"root>", usrn, telnet_closed, bad_login, b"cli->" ]
        #print(HOST)
        #print(usrname)
        #print(password)
        tn = telnetlib.Telnet(HOST)
        tn.set_debuglevel(0)
        tn.read_until(b"login: ")
        tn.write(usrname.encode('ascii') + b"\r\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\r\n")
            capture = tn.expect(reg_ex_list)
            capture_t = capture
            capture = capture[2]
            badlog0 = capture_t[0]
            #print("@"*80)
            #print(capture)
            #print("$"*80)
            capture = capture.decode('ascii', 'ignore')
        if badlog0 == 6:
            print("Could not connect at this time")
            print("Try again with a correct username / password combination")
            print("\n========================================================\n\n\n")
            sys.exit()
            
        print(capture)
        return(capture)      
    
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")
        sys.exit()
        pass
 
def connect_tel_noparse_traffic(HOST,usrname,password, *args):
    global tn
    tn.set_debuglevel(0)
    try:
         
        usrn = usrname + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        bad_login = "Login incorrect"
        bad_login = bad_login.encode()
        traff_server = " ~]# "
        #traff_prompt = "----------"
        traff_prompt = " ~]# "
        traff_server = traff_server.encode()
        
        reg_ex_list = [b"hlogin: ", b"inistrator", b"assword: ", b"option :", b"root>", usrn, telnet_closed, bad_login, traff_server ]
        #print(HOST)
        #print(usrname)
        #print(password)
        tn = telnetlib.Telnet(HOST)
        tn.set_debuglevel(0)
        tn.read_until(b"login: ")
        tn.write(usrname.encode('ascii') + b"\r\n")
        
        if password:
            #print("looking for password here ::")
            #tn.expect(reg_ex_list,10)
            tn.read_until(b"assword:")
            tn.write(password.encode('ascii') + b"\r\n")
            capture = tn.expect(reg_ex_list, 10)
            capture_t = capture
            capture = capture[2]
            badlog0 = capture_t[0]
            capture = capture.decode()
        if badlog0 == 6:
            print("Could not connect at this time")
            print("Try again with a correct username / password combination")
            print("\n========================================================\n\n\n")
            sys.exit()
            
        print(capture)
        return(capture)      
    
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")
        pass
    

def power_cmd(cmd, dl=0):
    global tn
    try: 
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        #traff_prompt = "\(yes, no\)  : "
        #traff_prompt = traff_prompt.encode()
        
        tn.set_debuglevel(dl)
        reg_ex_list = [b"cli->", b"\(yes, no\)  : ", b"seconds.", b"\$ ", telnet_closed] # b"Password: ", b"option :", b"root>", b"Forcing Failover ...", usrn, telnet_closed ]
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\r\n")
        capture = tn.expect(reg_ex_list)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        return capture
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")
        
def power_cmd_raritan(cmd, dl=0):
    global tn
    try: 
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        #traff_prompt = "\(yes, no\)  : "
        #traff_prompt = traff_prompt.encode()
        
        tn.set_debuglevel(dl)
        reg_ex_list = [b">", b"\[y/n]" , telnet_closed] # b"Password: ", b"option :", b"root>", b"Forcing Failover ...", usrn, telnet_closed ]
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\r\n")
        capture = tn.expect(reg_ex_list)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        return capture
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")

def fos_cmd_regex(cmd, reg,dblevel=0):
    ###########################################################################
    ####   
    ####   to pass the reg make it a list and b style
    ####    reg_list = [b'[my reg expression]', b'second expression' ]
    ####
    ####
    ###########################################################################
 
    global tn
    try: 
        usrn = var.sw_user + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        
        tn.set_debuglevel(dblevel)
        
        #reg = reg.encode()
        reg_ex_list = [reg, b"login: ", b"Password: ", b"option :", b"root>", usrn, telnet_closed ]
        reg_ex_list = reg
        reg_ex_list.append(usrn)
        
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        
        capture = tn.expect(reg_ex_list, 3600)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        tn.set_debuglevel(0)
        return(capture)
 
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print(" in  fos_cmd_regex()    ")
        print("========================")

def fos_cmd(cmd, dl=0):
    global tn
    try: 
        usrn = var.sw_user + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        #traff_prompt = " ~]# "
        #traff_prompt = "----------"
        #traff_prompt = "]# "
        #traff_prompt = traff_prompt.encode()
        
        tn.set_debuglevel(10)
        reg_ex_list = [b"login: ", b"Password: ", b"option :", b"root>", b"Forcing Failover ...", usrn, telnet_closed ]
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        
        #capture = tn.expect(reg_ex_list, 60)
        capture = tn.expect(reg_ex_list)
        capture = capture[2]
        capture = capture.decode('ascii', 'ignore')
        #print("@@"*40)
        #print("CAPTURE\n\n")
        print(capture, end="")
        return(capture)
 
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("    in fos_cmd func     ")
        print("========================")
        
    except SocketError as e:
            if e.errno != errno.ECONNRESET:
                print("\n\n\nCONNECTION ERROR TRYING TO RECONNECT\n\n\n")
                raise 
            print("========================")
            print("handle the EOF case here")
            print("   in  fos_cmd  func    ")
            print("========================")           
    except:
        print("===============================================")
        print("\n\nTHERE WAS AN ERROR WITH THE CAPTURE IN \n")
        print("fos_cmd in anturlar.py    \n\n")
        print("===============================================")       

        sys.exit()


def traff_cmd(cmd, dl=0):
    global tn
    try: 
         
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
   
        traff_prompt = "]# "
        traff_prompt = traff_prompt.encode()
      
        #
        tn.set_debuglevel(dl)
        #reg_ex_list = [b"hlogin: ", b"Password: ", b"option :", b"root>", b"Forcing Failover ...", usrn, telnet_closed, traff_prompt ]
        reg_ex_list = [ telnet_closed, traff_prompt, b"Administrator", b"admin"]
        
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\r\n")
        
        #capture = tn.expect(reg_ex_list, 60)
        capture = tn.expect(reg_ex_list)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        
        
        return capture
 
    #except EOFError:
        #print("========================")
        #print("handle the EOF case here")
        #print("========================")
    #except SocketError as e:
    #        if e.errno != errno.ECONNRESET:
    #            print("\n\n\nCONNECTION ERROR TRYING TO RECONNECT\n\n\n")
    #            raise 
    #        print("========================")
    #        print("handle the EOF case here")
    #        print("========================")           
    except:
        print("========================")
        print("\n\nTELNET ERROR\n\n")
        print("========================")       

    
    
def traff_output(dl= 0):
    global tn
    try:
        while True:
            telnet_closed = "telnet connection closed"
            telnet_closed = telnet_closed.encode()
            traff_prompt = "]# "
            traff_prompt = traff_prompt.encode()
            traff_cpu = ".*CPU \d+"
            traff_err = ".*Read:\d+"
            traff_wrt = ".*Write:\d+"
            
            traff_cpu = traff_cpu.encode()
            traff_err = traff_err.encode()
            traff_wrt = traff_wrt.encode()
            
            tn.set_debuglevel(dl)
            reg_ex_list = [ telnet_closed, traff_prompt, traff_cpu, traff_err, traff_wrt]
            capture = ""
            capture = tn.expect(reg_ex_list)
            capture = capture[2]
            capture = capture.decode()
            print(capture, end="")
            
            if "]# " in capture:
                return capture
            else:
                pass
        
    except:
        
        print("error in anturlar traff_ouput ")
        pass

  
def fos_cmd_regex_gen(cmd, reg,dblevel=0):
     ###########################################################################
    ####   
    ####   to pass the reg make it a list and b style
    ####    reg_list = [b'[my reg expression]', b'second expression' ]
    ####
    ####    gen since teh user name is not needed
    ###########################################################################
 
    global tn
    try: 
        #usrn = var.sw_user + '> '
        #usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        
        tn.set_debuglevel(dblevel)
        reg = reg.encode()
        #reg = reg.encode()
        reg_ex_list = [reg, b"login: ", b"Password: ", b"option :", b"root>", telnet_closed ]
        #reg_ex_list = reg
        #reg_ex_list.append(usrn)
        
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        
        capture = tn.expect(reg_ex_list, 3600)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        tn.set_debuglevel(0)
        return(capture)
 
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")
        

def fos_cmd_regex_only(cmd, reg,dblevel=0):
     ###########################################################################
    ####   
    ####   to pass the reg make it a list and b style
    ####    reg_list = [b'[my reg expression]', b'second expression' ]
    ####
    ####    gen since teh user name is not needed
    ###########################################################################
 
    global tn
    try: 
        #usrn = var.sw_user + '> '
        #usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        
        tn.set_debuglevel(dblevel)
        reg = reg.encode()
        #reg = reg.encode()
        reg_ex_list = [reg ]
        #reg_ex_list = reg
        #reg_ex_list.append(usrn)
        
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        
        capture = tn.expect(reg_ex_list, 3600)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        tn.set_debuglevel(0)
        return(capture)
 
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")
        

def remote_os_ver(ip="127.0.0.1", dl=0):
    
    ###########################################################################
    ####  find the os type of remote switch
    ####    if the ip is not passed it will find the version of local switch
    ####
    ###########################################################################
    
    db_level = dl
    ras = re.compile('ttl=([\d]{1,3})')
    this_command = "ping -c 1 " + ip + "\r\n"
    reg = "]#"
    connect_tel_noparse("127.0.0.1","root", "pass")
    
    cmdout = fos_cmd_regex_gen(this_command,reg, 9)
    
    os_ver = ras.findall(cmdout)
    print("\n"*33)
    print(os_ver)
    os_is = ""
    if os_ver[0] == '128':
        os_is = "windows"
    if os_ver[0] == '64':
        os_is = "linux"
    
    
    close_tel()
    

    return(os_is)



def connect_console(HOST,port,db=0, *args):
    """
      connect to the console
      
      HOST         =    the ip address of console 
      usrname      =    will be created from the port number    example  port17
      password     =    pass
      port         =    console port number -- example  3017
      
      db           =    set the telnet debug level  default is 0 / off  can be set up to 10 
      other args   =    none at this time 
    
    
    """
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
    tn.set_debuglevel(db)
    
    
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
    reg_list = [ b"Enter your option", b"login: ", b"assword: ", b"root> ", b"users: ", b"=>" ]  
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
        if capture[0] == 5:
            print(capture)
            var += 4
            break
        
        var += 1
      
    capture = tn.expect(reg_list, 20)
    if capture[0] == 1 :
        tn.write(b"root\r\n")
        capture = tn.expect(reg_list, 20)
        tn.write(b"password\r\n")
        capture = tn.expect(reg_list, 20)
        

    capture = tn.expect(reg_list, 20)
    
    return(tn)






def parse_port(port):
    """
        pass the port number of the console 
        return the port number that can be used in the connect_console procedure
    
        example port is 3017 and the return value will be port17
        
    """
    
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





def send_cmd_console(cmd, db=10):
    """
        send a command to the console when connected
    
    """
    
    
    global tn
    
    tn.set_debuglevel(db)
    
    capture = ""
    cmd_look = cmd.encode()
    
    #reg_ex_list = [b".*:root> "]
    reg_ex_list = [b"root> ", b"admin> ", b"ogin:", b"assword:"]
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    capture = tn.expect(reg_ex_list,3600)
    #print(capture[0])
    #print(capture[1])
    #print(capture[2])
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    
    return(capture)

