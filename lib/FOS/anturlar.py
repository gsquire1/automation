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
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""



class FabricInfo:
    """
        a class to return iformations about a Fabric including
        The FID is required make the class specific to the FID
        
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
        self.__change_fid__()
        capture_cmd = fos_cmd("fabricshow")
        #### the next two lines would return each item from the fabricshow command
        #ras = re.compile('\s?([0-9]{1,3}):\s+([\d\w]{6})\s+([:\d\w]{23})\s+([.\d]{7,15})\s+([.\d]{7,15})\s+(["_\w\d]+)')
        #ras_result = ras.search(capture_cmd)
        #### the above two lines not used here
        
        ### if used with the above line the next regex would return all the ipv4
        ####  addresses  but with FCR there are 00.00.00.00 addresses these are not
        ####   included with the current regex
        #ras = re.compile('\s+([.\d]{7,15})\s+')
        ras = re.compile('(?:\s?[0-9]{1,3}:\s+[\d\w]{6}\s+[:\d\w]{23}\s+)([1-9][0-90-9].\d{1,3}.\d{1,3}.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd)
            
        
        if not ras_result_all:
            ras_result_all = "none"
           
        return ras_result_all
    
    
    def ipv4_plus_fcr_list(self, pa,pw):
        """
            Return a string of the ipv4 plus switches attached via FCR
            Return none if nothing is matched with ipv4_list
            
        """
        fablist = self.ipv4_list()
        fablist_extended = []
        fablist_nodup = []
        #print("\n\n\n\n\nFABLIST IS AT THE START  ", fablist, "\n\n\n\n\n")
        fablist_base = fablist
        #for f in fablist_base:
        #print("\n\n\n\n\nFCR FAB BASE LIST   ", fablist_base, "\n\n\n\n")
        conn_value = connect_tel(pa,pw)
        capture_cmd = fos_cmd("")
        capture_cmd = fos_cmd("fcrfabricshow")
        ras = re.compile('(?:\d{1,3}\s+\d{1,3}\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd)
        #print("\n\n\n\n\nFCR FAB SHOW LIST   ", ras_result_all, "\n\n\n\n")
        print("\n\n\n\n\nFABLIST IS  :  ", fablist, "\n\n\n\n\n")
        
        if ras_result_all:
            for ip in ras_result_all:
                #print("\n\n\n\n\nCURRENTLY ON IP ", ip , "\n\n\n\n")
                orig_ip = pa.ip
                pa.ip = ip
                conn_value = connect_tel(pa,pw)
                fablist_extended = self.ipv4_list()
                #close_tel()
                for n in fablist_extended:
                    if n not in fablist:
                        fablist.append(n)
                pa.ip = orig_ip
                 
        print("\n\n\n\n\nFABLIST with No DUPLICATES IS  :  ", fablist, "\n\n\n\n\n")
        liabhar.count_down(10)
        
        return fablist
    
    
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
            ras_result = "no fabric"
            return("no fabric")
            
        return(ras_result)


    def zone_info(self):
        """
           return info all about the zones
            
        """
        #### need to add zone names
        
        capture_cmd = fos_cmd("cfgshow")
        #### find the effective config
        #### cfgshow
        ####   The Fabric is busy, try again later.
        #ras = re.compile('Effective configuration:\s+cfg:([_0-9A-Za-z])')
        ras = re.compile('(Effective configuration):\s+\\n\s+cfg:\s([_A-Za-z0-9]+)(?=\\t)')
        ras_result = ras.search(capture_cmd)
        
        result = [ ras_result.group(1), ras_result.group(2)]
        r_list = [result]
        return(r_list)
    
    
    
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
            ras = re.compile('\s?([0-9]{1,3})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
        else:
            #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
            ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9a-f]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+((FC)\s*(?=\\n))')
        ras = ras.findall(capture_cmd)
        self.online_ports = ras
        
    def __sw_show_info_all_ports__(self):
        """
            capture switchshow info and each column with regex
            return the index list of ports
        """
        capture_cmd = fos_cmd("switchshow")
        #### this regex will catch all online ports except base port
        #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+(\d+)\s+([0-9abcdef]{6})\s+([-id]{2})\s+([UNG12486]{2,3})\s+(Online)\s+(FC)\s+([-\w]{6,8})\s+([()-:\"_\w\s\d]*?(?=\\n))')
        #### this regex will catch all online ports including base port and loopback
        #print("\n\nDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        #print(self.am_i_director)
        #print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP\n\n")
        if self.am_i_director :
            #ras = re.compile('\s?([0-9]{1,3})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+(Online)\s+(FC)\s+([->\w]{6,8})\s+([()-:\"_\w\s\d]*?(?=\\n))')
            ras = re.compile('\s?([0-9]{1,3})\s+([-\d]+)\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+(FC)\s*([->\w]{6,8})([()-:\"_\w\s\d]*?(?=\\n))')
        else:
            #ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+(Online)\s+(FC)\s+([->\w]{6,14})\s+([()-:\"_\w\s\d]*?(?=\\n))')  
            ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+(FC)\s+([->\w]{6,14})\s+([()-:\"_\w\s\d]*?(?=\\n))')
            ras = re.compile('\s?([0-9]{1,3})\s+(\d+)\s+([-0-9abcdef]{6})\s+([-id]{2})\s+([-UNG12486]{2,3})\s+([_\w]{5,9})\s+(FC)\s*([->\w]{6,14})([()-:\"_\w\s\d]*?(?=\\n))')
        ras = ras.findall(capture_cmd)
        self.online_ports = ras
    
    def __director__(self):
        """
            determine if the switch is director or pizza box
            True = director
            False = pizza box
        """
        capture_cmd = fos_cmd("hashow")
        self.am_i_director = True
        if "hashow: Not supported" in capture_cmd:
            self.am_i_director = False
    
    def __myIPaddr__(self):
        """
            determine the current switch IP
            Return the ipv4 address
            Return 0 if no match found
        """
        capture_cmd = fos_cmd("ipaddrshow", 0)
        #match = re.search('(?P<ipaddress>[\s+\S+]+:([\d\.]){7,15}(?=\\r\\n))', capture_cmd)
        match = re.search('(?P<pre>([\s+\w+]+):\s?(?P<ip>[0-9\.]{1,15}))', capture_cmd)
        if match:
            myip = (match.group('ip'))
            return(myip)
        else:
            print("\n\n NO IP FOUND \n\n")
            return (0)
         
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
                slot_port_list = []
                slot_port_list.append(int(i[1]))
                if self.am_i_director:
                    slot_port_list.append(int(i[2]))
                port_list.append(slot_port_list)
                 
            if porttype == "Persistent":
                try:
                    if "rsistent" in i[persist_local]:
                        ####port_list.append(i[0])
                        slot_port_list = []
                        slot_port_list.append(int(i[1]))
                        if self.am_i_director:
                            slot_port_list.append(int(i[2]))
                        port_list.append(slot_port_list)
                except UnboundLocalError:
                    print("unboundlocalerror - moving on  ")
                    pass

        if not ras_result:
            ras_result = "no port found"
        return port_list
    
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
                prt = []
                prt.append(int(i))
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
            ras = re.compile('(?:\d{1,4}\s{3,4})(?P<slotnumber>\d{1,2})\s+?(?P<port>\d{1,2})\s+[-0-9a-f]{6}\s+[-idcu]{2}\s+[-AN24816G]{2,3}\s+\w+\s+[FC]{2}') 
            ras = ras.findall(capture_cmd)
            for i in ras:
                ras_list.append(list(i))
            for i in ras_list:
                i[0] = int(i[0])
                i[1] = int(i[1])
            return(ras_list)
        else:
            ras = re.compile('\s?\d{1,2}\s+(\d{1,2})\s+[-0-9a-f]{6}\s+[-idcu]{2}\s+[-AN24816G]{2,3}\s+\w+\s+[FC]{2}') 
            ras = ras.findall(capture_cmd)
            for i in ras:
                prt = []
                prt.append(int(i))
                ras_list.append(prt)
                 
            return(ras)
        
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
           return (False)
    
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
    
    def blades(self):
        """
            return the list of SW blades in the switch
            includes SW BLADES and AP BLADES
        """
        if self.am_i_director:
            capture_cmd = fos_cmd("slotshow -m")
            ras = re.compile('(\d+)\s+(SW BLADE|AP BLADE)\s+(\d+)\s+([-FCOEX1032468]+)\s+(\w+)')
            ras = ras.findall(capture_cmd)
            return(ras)
        else:
            return("not a director")
            
    
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
        fid = int(ras[0])
        return(fid)
        
    def d_ports(self):
        """
            this does not work because the getportlist requires the port
        """ 
        return(self.__getportlist__("D-Port"))
     
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
            return (0)

    def director(self):
        """
            return a 1 if this switch is a director
        """
        return(self.am_i_director)
    
    def disabled_ports(self):
        """
            Return a list of disabled ports including Persistent disabled ports
        """
        return(self.__getportlist__("Disabled"))
    
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
        capture_cmd = fos_cmd("licenseshow")
        ras = re.compile('([\w\d]{16,37})(?=:\\r\\n)')
        ras = ras.findall(capture_cmd)
        return(ras)
    
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
        for i in all_ports:
            #ras = ""
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
                print("\n\nSETTING THE SDFINFO info  \n")
                print("with slot port speed %s  %s   %s : " % (slot, port, sfp_speed))
                sfp_speed = int(ras[0])
                sfp_combine = [slot,port,sfp_speed]
                sfpinfo.append(sfp_combine)
                   
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
            
        sfpinfo_summary = ["total", sfp_count, 16, count16, 8, count8, 4, count4, 10, count10, "other", count_other]
        
        
        
        
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
        capture_cmd = fos_cmd("switchshow")
        ras = re.compile('switchState:\s+(\w{6,7})') 
        ras = ras.findall(capture_cmd)
        ss = str(ras[0])
        return(ss)     
    
    def switch_id(self ):
        """
           get the current switch
           does not work on AG switch
           
        """
        #### need a check for AG switch 
        capture_cmd = fos_cmd("switchshow")
        ras = re.compile('switchDomain:\s+(\d{1,3})') 
        ras = ras.findall(capture_cmd)
        sid = [int(i) for i in ras]
        sid = int(ras[0])
        return(sid)     
    
    def switch_name(self ):
        """
           get the current switch Name from switchshow
           return the current switchname
        """
        capture_cmd = fos_cmd("switchshow")
        ras = re.compile('switchName:\s+([_\d\w]{1,30})') 
        ras = ras.findall(capture_cmd)
        sn = str(ras[0])
        return(sn)
    
    def synchronized(self):
        """
            determine if a switch CP blades are in sync
        """
        
        capture_cmd = fos_cmd("hashow")
        if "HA State synchronized" in capture_cmd:
            return True
        else:
            return False
    
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
            return (False)
        else:
            #print("\n\n\nVF is enabled on this switch\n\n\n")
            return (True)
   
   


    
   
class DoSupportsave():
    """
        start a supportsave on the current switch
        the ip user 
    """
    def __init__(self, ip, user, passw, chas_name, tr = 'yes'):
        self.tr = tr
        self.ip = ip
        self.user = user
        self.passw = passw
        self.chas_name = chas_name
        self.dirname = ""
        self.createdir()
        self.start()
        
    def start(self):
        """
         doc here
        """
        
        self.tracedump()
        
        capture = ""
        reg_ex_list = [b'root> ', b'.*\r\n']
        reg_ex_list = [b'root>', b'please retry later', b'SupportSave complete', b'Supportsave failed.']
        cmd = "supportsave -n -u %s -p %s -h %s -l ftp -d %s" % (self.user, self.passw, self.ip, self.dirname)
        reg_ex_list_only_root = [b'(.*\d\\r\\n )']
        reg_ex_list_only_cmd = [ cmd.encode()]
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        capture = tn.expect(reg_ex_list_only_cmd, 10)
        capture = tn.expect(reg_ex_list, 3600)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end=' ')
    
    def tracedump(self):
        if self.tr == "yes":
            capture_cmd = fos_cmd("tracedump -n")
            capture_cmd = fos_cmd("")
         
    def createdir(self):
        global tn
        i = str(datetime.datetime.today())  #### ISO format 2013-02-21 06:35:45.707450
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
        print(i)
        d = [" ", "-", ":", "."]
        for k in d:
            print(k)
            i = i.replace(k, "_")
         
        print("\niiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
        print(i)
        self.dirname = self.chas_name
        self.dirname += "__"
        self.dirname += i
        print("new directory name\n")
        print(self.dirname)
        print("\niiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
            
        reg_ex_list_ftp = [b'root\):', b'none\)\):']
        cmd = "ftp "
        cmd += self.ip
        tn.write(cmd.encode('ascii') + b"\n")
        capture = tn.expect(reg_ex_list_ftp, 10)
        print(capture)
        reg_ex_list_ftp = [b'assword:']
        cmd = self.user
        tn.write(cmd.encode('ascii') + b"\n")
        capture = tn.expect(reg_ex_list_ftp, 10)
        print(capture)
        
        reg_ex_list_ftp = [b'ftp> ']
        cmd = self.passw
        tn.write(cmd.encode('ascii') + b"\n")
        capture = tn.expect(reg_ex_list_ftp, 10)
        print(capture)
     
        reg_ex_list_ftp = [b'ftp', b'denied ', b'timeout']
        cmd = "mkdir "
        cmd += self.dirname
        tn.write(cmd.encode('ascii') + b"\n")
        capture = tn.expect(reg_ex_list_ftp, 10)
        print(capture)
        
        reg_ex_list_ftp = [b'ftp', b'denied ', b'timeout']
        cmd = "exit"
        tn.write(cmd.encode('ascii') + b"\n")
        capture = tn.expect(reg_ex_list_ftp, 10)
        print(capture)
        
        return 0
   
class DoFirmwaredownloadChoice():
    """
        do a firmware download to 7.3.x or 7.2.x builds depending on what
        is already on the switch
        
    """
    def __init__(self, firmdown, firmup):
        self.firmdown = firmdown
        self.firmup = firmup
        #self.check_version()
        self.start()
        
    def check_status(self):
        capture_cmd = fos_cmd("firmwaredownloadstatus")
        if "firmware versions" in capture_cmd:
            return("1")
        else:
            liabhar.count_down(30)
            self.check_status()
               
         
    def check_version(self):
         
        capture_cmd = fos_cmd("firmwareshow") 
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = ras.search(capture_cmd)
        ras_dir = ras_dir.search(capture_cmd)
        #print(ras.group(0))
        #print(ras_dir.group(0))
        #print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        f=""
        try:
            if ras.group(0) != "none":
                f= ras.group(1)
        except:
            pass
        try:
            if ras_dir(0) != "none":
                f=ras_dir.group(1)
        except:
            pass
         
         
        #liabhar.JustSleep(20)
        #self.check_version()
            
        #print("found the firmware version\n")
        #print(f)
        #print(capture_cmd)
        return(f)
         
         
    def start(self):
        ras = self.check_version()
        print("FIRMUP IS %s\n"%(self.firmup))
        print("RAS IS     %s\n"%(ras))
        if ras != self.firmup:
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
        else:
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.']
        capture_own_regex = fos_cmd_regex(firmware_cmd, reg_ex_list)
        if "the same firmware" in capture_own_regex:
            return(capture_own_regex)
        if "server is inaccessible" in capture_own_regex:
            return(capture_own_regex)
        
        capture_cmd = fos_cmd("Y")
        close_tel()
        liabhar.email_sender_html("smckie@brocade.com", "smckie@brocade.com", "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
        liabhar.count_down(1200) 
        return(capture_cmd)
        
    
class doFirmwareDownload():
    """
        do a firmware download to 7.3.0 build of  firmware
        then close the telnet connection and
        wait 1200 seconds before closing ending the function
        Return could be
                1. a message that firmware version are the same
                2. server is inaccessible
                3. the user prompt after firmware download is started
    """
    def __init__(self, firmvrsn ):
        self.firmvrsn = firmvrsn
        self.start()
    
    def check_status(self):
        capture_cmd = fos_cmd("firmwaredownloadstatus")
        if "firmware versions" in capture_cmd:
            return("1")
        else:
            liabhar.count_down(30)
            self.check_status()
            
    def check_version(self):
         
        capture_cmd = fos_cmd("firmwareshow") 
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = ras.search(capture_cmd)
        ras_dir = ras_dir.search(capture_cmd)
        f=""
        try:
            if ras.group(0) != "none":
                f= ras.group(1)
        except:
            pass
        try:
            if ras_dir(0) != "none":
                f=ras_dir.group(1)
        except:
            pass
        
        return(f)

    def start(self):
        ras = self.check_version()
        #print("FIRMUP IS %s\n"%(self.firmup))
        #print("RAS IS     %s\n"%(ras))
        if ras != self.firmvrsn:
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmvrsn)
        else:
            return "fail to perform Firmwaredownload since versions were the same"
            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.']
        capture_own_regex = fos_cmd_regex(firmware_cmd, reg_ex_list)
        if "the same firmware" in capture_own_regex:
            return(capture_own_regex)
        if "server is inaccessible" in capture_own_regex:
            return(capture_own_regex)
        
        capture_cmd = fos_cmd("Y")
        close_tel()
        liabhar.email_sender_html("smckie@brocade.com", "smckie@brocade.com", "Started Firmware Download ", "%s"%(self.firmvrsn))
        liabhar.count_down(1200) 
        return(capture_cmd)
    
    
class configSwitch(SwitchInfo):
    
    
    
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
                
            
                
            
                
             
    
class FcrConfig(SwitchInfo, FabricInfo):
    
    def __init__(self):
        SwitchInfo.__init__(self)
        FabricInfo.__init__(self)
    
    def ex_cleanup(self):
        """
            
        """
        fos_cmd("switchdisable")
        portlist =  self.all_ports()
        if self.am_i_director:
           for i in portlist:
                slot = i[0]
                port = i[1]
                pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
                cmd = fos_cmd("portcfgshow %a/%a" % (slot, port))
                ex = pattern.search(cmd)
                if ex:
                    fos_cmd("portcfgexport %s/%s %s"%(slot,port,"-a2") )
        else: 
            for i in portlist:
                pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
                cmd = fos_cmd("portcfgshow %a" % i)
                ex = pattern.search(cmd)
                if ex:
                    fos_cmd("portcfgexport "+i+" -a2")
        cmd_cap = fos_cmd("switchenable")        
        return(cmd_cap)
    
    def fcr_backbone_ip(self):
        """
            Runs fabricshow against backbone switches in a fabric to determine all IPs 
        """
         
        fcrcfg = FcrConfig()
        fcrstatus = self.initial_checks()
        if fcrstatus[3] is not False:  # Test if base config'd and if so
            base = fcrcfg.base_check() # get the base FID number
            f = FabricInfo(base) ###########NEW OBJECT FOR BASE FID
            get_fabric_ip = f.ipv4_list() ###########NEW OBJECT FOR BASE FID
        else:
            get_fabric_ip = fcrcfg.ipv4_list()
        return(get_fabric_ip)

    def fcr_fab_wide_ip(self):
        """
            Runs fcrfabricshow and fabricshow against switches in a fabric to determine all IPs then
            removes any duplicate entries.
            This includes both backbone and edge switches and any switches in edge fabrics.
            Return is a set of IPs (set function doesn't allow duplicates).
        """
         
        fcrcfg = FcrConfig()
        fcrstatus = self.initial_checks()
        if fcrstatus[3] is not False:  # Test if base config'd and if so
            base = fcrcfg.base_check() # get the base FID number
            f = FabricInfo(base) ###########NEW OBJECT FOR BASE FID
            get_fabric_ip = f.ipv4_list() ###########NEW OBJECT FOR BASE FID
        else:
            get_fabric_ip = fcrcfg.ipv4_list()
        get_fcr_fabric = self.ipv4_fcr()
        fcr_fab_ip_list = (set(get_fabric_ip + get_fcr_fabric))
        
        all_ips = []
        get_fabric_ip = []
        for ip in fcr_fab_ip_list:
            connect_tel_noparse(ip,'root','password')
            base = fcrcfg.base_check() # get the base FID number
            if base is not False:
                f = FabricInfo(base) ###########NEW OBJECT FOR BASE FID
                get_fabric_ip = f.ipv4_list() ###########NEW OBJECT FOR BASE FID
            else:
                get_fabric_ip = fcrcfg.ipv4_list()
                all_ips.extend(get_fabric_ip)
        all_ips_no_dups = (set(all_ips))
        return(all_ips_no_dups)


    def fcr_proxy_dev(self):
        """
        Get number of proxy devices reported by switch
        """
        cmd_capture = fos_cmd("fcrproxydevshow | grep device")
        print(cmd_capture)
        device_number = re.findall(':\s([0-9]{1,4})', cmd_capture)
        #print('DEVICEDEVICEDEVICE')
        #print(device_number)
        return(device_number)


    def get_licenses(self):
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


    def initial_checks(self):
        """
            Retrieve FCR fabric and return info. Variable #'s:
            0) FCR Enabled
            1) Chassis or Pizza Box
            2) VF or not
            3) Base Configured

        """
        fcr = self.fcr_enabled()
        director = self.director()
        vf = self.vf_enabled()
        base = self.base_check()
        #print('\n\n'+ '='*20)
        #print('FCR Enabled: %s\n' % fcr)
        #print('Chassis or Pizzabox: %s\n' % director)
        #print('VF enabled: %s\n' % vf)
        #print('Base configured: %s\n' % base)
        #print('='*20)
        return [fcr, director, vf, base]

    def ipv4_fcr(self):
        """
            Return a string (list) ipv4 address of switch\switches connected
            to FCR Router thru EX-Port
        """
        #self.__change_fid__()
        capture_cmd = fos_cmd("fcrfabricshow")
        
        ras = re.compile('(?:\d{1,3}\s+\d{1,3}\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ras_result_all = ras.findall(capture_cmd)
            
        if not ras_result_all:
            ras_result_all = None 
        return ras_result_all


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
        return ras_result_all 
    
    
    def name1(self, ):
        pass
    
    def portcfgfillword(self, cfgvalue):
        """
            Applies user chosen setting (0-4) for portcfgfillword command.
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
                fos_cmd("portcfgfillword "+slot+"/"+port+" "+ cfgvalue )
                fos_cmd("\r")
        else: 
            for i in portlist:
                fos_cmd("\r")
                fos_cmd("portcfgfillword "+i+" "+ cfgvalue )
                fos_cmd("\r")
        cmd_cap = fos_cmd("switchenable")
        return(cmd_cap)
     
     
     


class Maps(SwitchInfo):
    
    def enable(self, policy ):
        return(fos_cmd("echo Y | mapsconfig --enable -policy %s " % policy))
                
    def actions(self, action_list ):
        return(fos_cmd("mapsconfig --actions %s " % action_list))

    def email_cfg(self, email_list ):
        return(fos_cmd("mapsconfig --emailcfg -address %s " % email_list))

    def get_rules(self):
        capture_cmd = fos_cmd("mapsrule --show -all")
        ras = re.compile('(def[_ ,\/\()-=\.|<>A-Za-z0-9]+)')
        ras = ras.findall(capture_cmd)
        ras = str(ras)
        ras = ras.replace("'","")
        ras = ras.replace("[","")
        ras = ras.replace("]","")
        return(ras)
        

        
        
    def get_policies(self, p = 's' ):
        #### ruturn the policy rules list for p
        ####  a = aggresive policy
        ####  c = conservative policy
        ####  m = moderate policy
        ####  s or none = summary of policy
        
        if p == "s":
            return(fos_cmd("mapspolicy --show -summary"))
        elif p == "a":
            return(fos_cmd("mapspolicy --show -dflt_aggressive_policy"))
        elif p == "c":
            return(fos_cmd("mapspolicy --show -dflt_conservative_policy"))
        elif p == "m":
            return(fos_cmd("mapspolicy --show -dflt_moderate_policy"))
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
        i = 0
        while i <=2:
            ras.pop(0)
            i +=1
        ras_str = str(ras)
        ras_str = ras_str.replace("'","")
        ras_str = ras_str.replace("[","")
        ras_str = ras_str.replace("]","")
        ras_str = ras_str.replace(",","")
        ras_final = ras_str.split(" ")
        
        return(ras_final)
        
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
        ras = ras.search(capture_cmd)
        
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
        capture_cmd = fos_cmd("errdumpall")
        ras = re.compile("(%s)" % pattern)
        ras = ras.search(capture_cmd)
        print("\n\n\nRAS PATTERN is  :  %s " % pattern)
        print("\n\n %s " % ras)
         
        if ras:
            return(ras.group())
        else:
            return("no match found")
    
        return(0)
    
        
    def logicalgroup_count(self, group):
        """
            return the count for the line group passed for any of the following
            
            ALL_F_PORTS         ALL_OTHER_F_PORTS       ALL_HOST_PORTS    
            ALL_TARGET_PORTS    ALL_TS                  ALL_FAN        
            ALL_PS              ALL_WWN                 ALL_SFP        
            ALL_10GSWL_SFP      ALL_10GLWL_SFP          ALL_16GSWL_SFP 
            ALL_16GLWL_SFP      ALL_QSFP                ALL_OTHER_SFP  
            ALL_SLOTS           ALL_SW_BLADES           ALL_CORE_BLADES 
            ALL_FLASH           ALL_CIRCUITS            SWITCH     
            CHASSIS             ALL_D_PORTS
            
        """
        #### return a list of all the values ?
        capture_cmd = fos_cmd("logicalgroup --show")
            
        #ras = re.compile("(ALL_SW_BLADES)\s+(?:\|)(Yes)\s+\|(Blade)\s+(?:\|)([0-9])\s+(?:\|)([,0-9])")
        ras = re.compile("(%s)\s+\|Yes\s+\|[ \w]+\|([0-9]+)" % group)    
        ras = ras.search(capture_cmd)
        
        if not ras:
            value = "-1"
        else:
            print(ras)
            print(ras.group())
        
            value = ras.group()
        return(value)

    def cpu_usage(self):
        """
           calculate the cpu usage from the data
           in /proc/stat
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
        liabhar.JustSleep(6)
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
        
        print("@"*80)
        print("@"*80)
        cpu_use_d = (sumt1 - sumt2)
        cpu_use  = (round(100-( cpu_use_n / cpu_use_d),2) ) 
        
        print("cpu top     %s  " % cpu_use_n)
        print("cpu demon   %s  " % cpu_use_d)
        print("values")
        print(sumt1)
        print(sumt2)
        print(cpu_calc[4])
        print(cpu_calcT2[4])
        print(cpu_calc[1])
        print(cpu_calc[3])
        print(cpu_calc[5])
        print(cpu_calc[6])
        print(cpu_calc[7])
        
        print("@"*80)
        print("@"*80)
        
        return(cpu_use)
    
    def temp_status(self):
        """
           scan all the temp sensors and return the high temp, low temp
           and average temp of the switch using the tempshow command
           
        """
        capture_cmd = fos_cmd("tempshow")
        
        ras = re.compile("\d+\s+\w+\s+\d+\s+\d+")
        ras = ras.findall(capture_cmd)
        ras_str = str(ras)
        ras_str = ras_str.replace("\\t"," ")
        ras_str = ras_str.replace("'", "")
        ras_str = ras_str.replace("[", "")
        ras_str = ras_str.replace("]", "")
        #ras_str = ras_str.replace(" ", "")
        ras_final = " ".join(ras_str.split())
        
        ras_final = ras_final.split()
        return(ras_final[2])
    
        
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
        
        print("\n\n\n",cmd_out , "\n\n\n\n")
        #ras = re.compile('([_-a-z0-9A-z]{1,20})[ \|]+[\*,-|a-zA-Z0-9]+(?=\n)')
        ras = re.compile('\n([_a-z0-9A-Z]{1,20})(?= |)')
        ras = ras.findall(cmd_out)
        
        print(ras)
        return(ras)
    
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
        if self.am_i_director:
            for i in portlist:
                slot = i[0]
                port = i[1]
                #pattern = re.compile(r'(?:\Sim\sPort\s+)(?P<state> ON)')
                #cmd = fos_cmd("portcfgshow %a/%a" % (slot, port))
                #ex = pattern.search(cmd)
                #if ex:
                fos_cmd("flow --control -simport "+slot+"/"+port+" %s"%(state))
              
        else: 
            for i in portlist:
                #pattern = re.compile(r'(?:\Sim\sPort\s+)(?P<state> ON)')
                #cmd = fos_cmd("portcfgshow %a" % i)
                #ex = pattern.search(cmd)
                #if ex:
                fos_cmd("flow --control -simport "+i+" %s"%(state))
              
        return(portlist)


def clear_stats():
    """
        clear the following stats on a switch
        fcrlogclear     errclear    diagclearerror -all     tracedump -R
        supportsave -R  statsclear  portlogclear        coreshow -R
        slotstatsclear    fabstatsclear   history clear
        
    """
    switch_info = fos_cmd("")
    switch_info = fos_cmd("fcrlogclear")
    switch_info = fos_cmd("supportsave -R")
    switch_info = fos_cmd("errclear")
    switch_info = fos_cmd("statsclear")
    switch_info = fos_cmd("portlogclear")
    switch_info = fos_cmd("diagclearerror -all")
    switch_info = fos_cmd("tracedump -R")
    switch_info = fos_cmd("coreshow -R")
    switch_info = fos_cmd("slotstatsclear")
    switch_info = fos_cmd("fabstatsclear")
    switch_info = fos_cmd("history -c")
   

def login(pw=""):
    pa = liabhar.parse_args(sys.argv)
    if pw == "":
        pw = getpass.getpass()
    conn_value = connect_tel(pa,pw)
    return conn_value


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
        reg_ex_list = [b"login: ", b"Password: ", b"option :", b"root>", usrn, telnet_closed, bad_login ]
        #print(HOST)
        #print(usrname)
        #print(password)
        tn = telnetlib.Telnet(HOST)
        #tn.set_debuglevel(9)
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
            sys.exit()
            
        
        print(capture)
        con_out = fos_cmd("")
        con_out = fos_cmd("setcontext %s"%(fid))
        print(con_out)
        
        return capture      
    
    except EOFError:
        print("========================")
        print("handle the EOF case here")
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
        reg_ex_list = [b"login: ", b"Password: ", b"option :", b"root>", usrn, telnet_closed, bad_login ]
        #print(HOST)
        #print(usrname)
        #print(password)
        tn = telnetlib.Telnet(HOST)
        #tn.set_debuglevel(9)
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
            sys.exit()
            
        print(capture)
        return capture      
    
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")
        pass
    
def fos_cmd_regex(cmd, reg, dblevel=0):
    global tn
    try: 
        usrn = var.sw_user + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        
        tn.set_debuglevel(dblevel)
        #reg_ex_list = [b"login: ", b"Password: ", b"option :", b"root>", usrn, telnet_closed ]
        reg_ex_list = reg
        reg_ex_list.append(usrn)
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        
        capture = tn.expect(reg_ex_list, 60)
        capture = capture[2]
        capture = capture.decode()
        print(capture, end="")
        tn.set_debuglevel(0)
        return capture
 
    except EOFError:
        print("========================")
        print("handle the EOF case here")
        print("========================")


def fos_cmd(cmd, dl=0):
    global tn
    try: 
        usrn = var.sw_user + '> '
        usrn = usrn.encode()
        telnet_closed = "telnet connection closed"
        telnet_closed = telnet_closed.encode()
        
        tn.set_debuglevel(dl)
        reg_ex_list = [b"login: ", b"Password: ", b"option :", b"root>", b"Forcing Failover ...", usrn, telnet_closed ]
        capture = ""
        print(cmd)
        tn.write(cmd.encode('ascii') + b"\n")
        
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


def waitForOnline(si):
    """
        what for a switch to return to online state
        si = switch object from SwitchInfo
        
    """
    print("\n\n\n\n")
    s_state = si.switch_state()
    while "Offline" in s_state:
        s_state = si.switch_state()
        sleeping = liabhar.count_down(15)
        print("\n\nswitch is Offline ")
        print(s_state)
    sleeping = liabhar.count_down(10)
    return 1



def mem_usage():
    """
        Returns the top memory users on the switch
    """
    
    capture = fos_cmd("ps axu")
    return capture
 
def mem_usage_top20():
    """
        Returns the top 20 memory users on the switch
    """
    capture = fos_cmd("ps -eo vsz,rss,comm,pid | sort | tail -20")
    return capture
    

    
    
    
def fids_check(self, fid, lscfgshow): 
        """
            Check if FID given is resident on switch.
        """
        self.fid = fid
        self.lscfgshow = lscfgshow
        #print("\n\n\nChecking if FID %s is a valid FID on switch.\n\n\n " % fid)
        fids = re.findall('(\d{1,3})\(', lscfgshow)
        #print("==================")
        #print("Below is list of available FIDs: ")
        #print(fids)
        #print("==================")
        b = (str(fid))
        if b in fids:
            #print("\n")
            #print("="*20)
            #print("%s is a valid FID on this switch " % fid)
            #print("="*20)
            return(1)
        else:
            print("\n")
            print("="*20)
            print("%s is a NOT valid FID on this switch " % fid)
            print("="*20)
            return(0)

    
