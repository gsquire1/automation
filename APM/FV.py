#!/usr/bin/env python3

 
# -*- coding: iso-8859-1 -*-

from tkinter import *
from multiprocessing import Process,Queue
import sys
import time
import datetime
import telnetlib
import shelve
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#################################################################################
#### user modules
#################################################################################
 
#################################################################################
##### import my_module
#################################################################################

#################################################################################
##### variables
#################################################################################
tn =""
cw_config_file_name = "logs\\FV_Monitor.txt"
shelvename = "class-switchinfo"
fieldnames = ('name', 'ipaddr', 'port')  #### 
numerical_fieldnames = ( 'port' )
#entries = {}                       #### moved to class conwatch_tk

class FV(Tk):
    
    entries = {}
    global ras_switch_dictionary 
    ras_switch_dictionary = {}
    
    def __init__(self,parent, work_queue):
        Tk.__init__(self,parent)
        self.parent = parent
        self.queue = work_queue
        self.initialize()
        self.processIncomingQ()
        print("the queue is ", self.queue)
        self.queue.put("this is on the queue")
        self.qTest()
        
    def quit_gui(self):
        #self.parent.destroy
        try:
            if self.p.is_alive():
                self.p.terminate()
        except AttributeError:  #### if the process is not running no need to terminate
            pass                ####  just pass through
        time.sleep(0.1)
        cw.destroy()
        
    def initialize(self):
         
        
        self.grid()
        self.form0 = Frame(self.parent)
        self.form0.grid(column=0,row=0, sticky='EWNS')
       
        self.resizable(width=TRUE,height=TRUE)
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        
        menubar = MenuBar(self.form0)
        self.config(menu=menubar)
        
        self.frame_1()
        self.frame_3()
        self.frame_2()
        self.frame_4() 
        
        
        
          
        
    def frame_1(self):    #### top left frame for entry of records
        global entries
        self.form1 = Frame(self.form0, borderwidth=2, relief="groove")
        self.form1.grid(column=0,row=1)
        entries = {}
        #for (ix, label) in enumerate(('key',) + fieldnames):
        for (ix, label) in enumerate(('ID',) + fieldnames):  
            lab = Label(self.form1, text=label)
            ent = Entry(self.form1)
            lab.grid(row=ix, column=0)
            ent.grid(row=ix, column=1)
            entries[label] = ent
        
    
    def frame_2(self):   #### frame to hold text box
        
        self.form2 =Frame(self.form0, borderwidth=2, relief="groove")
        self.form2.grid(column=1,row=2,columnspan=2,sticky='EWNS')
                                 
        self.labelVariable = StringVar()
        label = Label(self.form2,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=2,row=1,columnspan=2,sticky='EWNS')
        self.labelVariable.set("Console Summary")
         
        text = Text(self.form2, relief=SUNKEN)
        sbar = Scrollbar(self.form2)
        sbar.config(command=text.yview) # xlink sbar and text
        text.config(yscrollcommand=sbar.set) # move one moves other
        sbar.grid(column=3, row=2,sticky='EWNS')
        text.grid(column=2, row=2,columnspan=2,sticky='EWNS') 
        self.text = text
        self.text.insert("end", "\nClick Connect All to start monitoring \n")
        self.text.insert("end", "\nEnter ID and Retrieve to monitor one switch\n")
        self.text.insert("end", "Or Enter all data to monitor a new switch")
        #self.grid_columnconfigure(1,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       
        #self.entry.focus_set()
        
         
    def frame_3(self):   #### frame to hold list of switches
        #self.form3 = Frame(self.form0,bg="yellow", borderwidth=2, relief="groove")
        self.form3 = Frame(self.form0, borderwidth=2, relief="groove")
        self.form3.grid(column=0,row=2, ipadx=20, ipady=15, sticky="NWES")
        #label3 = Label(self.form3,text="  Connected Consoles  ", borderwidth=5, anchor="s",fg="white",bg="blue")
        label3 = Label(self.form3,text="  Connected Consoles  ", borderwidth=2, anchor="center",fg="black" , relief="ridge")
        #label3.grid(column=0,row=21,sticky="WE")
        label3.grid(row=21,sticky='we')
    
    def frame_4(self):    #### frame to hold the buttons
        
        self.form4 = Frame(self.form0, borderwidth=2, relief="groove")
        self.form4.grid(column=1,row=1)
        
        button_fetch = Button(self.form4, text="Retrieve Record", command=self.fetchRecord)
        button_fetch.grid(row=1, column=1,sticky='EW')
        button_save_rec = Button(self.form4, text="Save record", command=self.updateRecord)
        button_save_rec.grid(row =2, column=1,sticky='EW')
        button_del_record = Button(self.form4, text="Delete Record", command=self.delRecord)
        button_del_record.grid(row=3, column=1,sticky='EW')
         
        button_list_keys = Button(self.form4, text="   list IDs   ", command=self.listKeys)
        button_list_keys.grid(row=2, column=2,sticky='EW') 
        
        button_connect = Button(self.form4, text="Connect", command=self.cwStart)
        button_connect.grid(row=1, column=4,sticky='EW')  
        button_connect_all = Button(self.form4, text=" Connect All ", command=self.cwStartAll)
        button_connect_all.grid(row=3, column=4,sticky='EW')
        
        button_quit = Button(self.form4, text="    Quit    ", command=self.quit_gui)
        button_quit.grid(row=2,column=5,sticky='EW')
        
    
    
    def processIncomingQ(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        global ras_switch_dictionary
         
        while True:
            try:
                m = self.queue.get(timeout = 0.1)
                if m == 'exit':
                    print ('cleaning up worker...')
                    # add here your cleaning up code
                    break
                else:
                    if m:
                        print(m)
            except:
                break
            if m: 
                if isinstance(m,str) | isinstance(m,int):
                    self.upDateTextBox(m)
                else:
                    m_dict = dict(m)
                    ip = m_dict["ip_address"]
                    
                    ras_switch_dictionary[ip] = m 
                    #self.upDateTextBox(ras_switch_dictionary)
                    self.upDateTextBox_clearfirst(ras_switch_dictionary)
                    print("\n888888888888888888888888888888888888888888888888888888888\n\n")
                    print(ras_switch_dictionary)
                    #try:
                    #    for key in ras_switch_dictionary:
                    #        print("KEY value is :    ")
                    #        print(key)
                    #        print("value is  :       ")
                    #        print(ras_switch_dictionary(key))
                    #except:
                    #    print("\noooops there was an error\n=========================")
                    #
                    print("\n999999999999999999999999999999999999999999999999999999999\n\n")
        #####################################################################
        #### 
        self.after(100, self.processIncomingQ)
        ### 
            #except KeyboardInterrupt:
            #   print ('ignore CTRL-C from worker')
            
    def qTest(self):
        m = self.queue.get()
        print(m)
    
    def OnButtonClick(self):
        self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
        self.entry.focus_set()
        self.entry.selection_range(0, END)
    
    def upDateTextBox(self, text):
        #print("\nin the Updatingtextbox procedure\n\n")
        self.text.insert("end", text )
        #self.text.insert("end", "\r\n-------------\r\n")
        self.text.see(END)
        
    
    def upDateTextBox_clearfirst(self, text):
        self.text.delete(1.0, END)
        rs = {}
        ip = ""
        cn = ""
        ras_Items = text.items()
        for key, value in ras_Items:
            kv = [key,value]            #### make a list of the key and value
            value_list = list(value)    #### lets work on only the value part
            #self.text.insert("end", value)
            #self.text.insert("end", value)
            for v,w in value_list:      #### everything is stored in pairs
                #### chassis_name-real_name ipaddr-10.20.30.40
                if v == "chassis_name":
                    cn = w
                elif v == "ip_address":
                    ip = w
                else:
                    rs[v] = w
                    
            self.text.insert("end", "CHASSIS NAME   ")
            self.text.insert("end", cn)
            self.text.insert("end", "\n")
            self.text.insert("end", "IP ADDRESS     ")
            self.text.insert("end", ip)
            self.text.insert("end", "\n\n")
            
            ras = ""
            value2 = ""
            rs_I = rs.items()
            for ras, value2 in rs_I:
                self.text.insert("end", value2)
                self.text.insert("end", "\t\t")
                self.text.insert("end", ras)
                self.text.insert("end", "\n")
            
            self.text.insert("end", "\n\n")
            #self.text.insert("end", kv)
        #self.text.insert("end", "\r\n-------------\r\n")
        self.text.see(END)
    
    
    def cwStart(self):
        try:
            print("connect to the console\n")
            self.queue.put("\n\nCONNECTING TO THE CONSOLES\n\n")
            
            ip = entries['ipaddr'].get()
            cport = entries['port'].get()
            
            self.p = Process(target=testproc, args=(self.queue, ip, cport))
            self.p.start()
            
            
        except ValueError:
            pass
    
    def cwStartAll(self):
        
        print("connect to all consoles in the data base")
        self.queue.put("\n\nCONNECTING TO ALL OF THE CONSOLES\n\n")
        
        db = shelve.open(shelvename)
        
        for ind, key in enumerate(db.keys()):
            print(key)
            console_info = db[key]
            print(console_info.ipaddr)
            print(console_info.port)
            
            ip = console_info.ipaddr
            cport = console_info.port
            #cport = int(cport)
            #self.queue.put(ip)
            #self.queue.put(cport)
            
            
            self.p = Process(target=testproc, args=(self.queue, ip, cport))
            self.p.daemon = True
            self.p.start()
            
            print("\n\n", self.p.pid)
            #self.queue.put("\n\nmy process id is ")
            #self.queue.put(self.p.pid)
            #self.queue.put("\n===========================")
            #print("\nI don't know Mr. Hand\n\n" ) 
        db.close()
        return 0          
         
    
    
    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, END)

    def fetchRecord(self):
        db = shelve.open(shelvename)
        
        key = entries['ID'].get()
        try:
            record = db[key] # fetch by key, show in GUI
        except:
            showerror(title='Error', message='No such key!')
            
        else:
            for field in fieldnames:
                entries[field].delete(0, END)
                entries[field].insert(0, repr(getattr(record, field)))
                
        db.close()
        return 0
            
    def updateRecord(self):
        
        db = shelve.open(shelvename)
        key = entries['ID'].get()
        if key in db:
            record = db[key] # update existing record
            return 0
            #del db[key]
            
        else:
            record = ConsoleData(name='?', ipaddr='?', port='?') 
        for field in fieldnames:
            currval = getattr(record, field)
            newtext = str(entries[field].get())
            
            newtext = int(newtext) if field in numerical_fieldnames else newtext
            if newtext:
                setattr(record, field, newtext)
                
        db[key] = record
        
        db.close()
     

    def delRecord(self):
    
        db = shelve.open(shelvename)
        key = entries['ID'].get()
        del db[key]

    def listKeys(self):
        db = shelve.open(shelvename)
        print("\n\n the shelve keys\n")
        print(db.keys())
        print("--------------")
        for ind, key in enumerate(db.keys()):
            print(key)
            console_info = db[key]
            print(console_info.ipaddr)
            print(console_info.port)
            labelc = Label(cw.form3,text=key, borderwidth=5,anchor="w",bg="blue", fg="white")
            
            labelc.grid(column=0,row=ind,columnspan=2, sticky='ew')
        db.close()

class MenuBar(Menu):
        def __init__(self,parent):
            Menu.__init__(self, parent)
                 
            filemenu = Menu(self, tearoff=0)
            
            filemenu.add_command(label="Save", command=self.donothing)
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.donothing)
            
            cnfgmenu = Menu(self, tearoff=0)
            cnfgmenu.add_command(label="email", command=self.cnfgWin)
            
            helpmenu = Menu(self, tearoff=0)
            helpmenu.add_command(label="about", command=self.helpAbout)
            self.add_cascade(label="File", underline=0, menu=filemenu)
            self.add_cascade(label="Config", underline=0, menu=cnfgmenu)
            self.add_cascade(label="Help", underline=0, menu=helpmenu)
            
        def helpAbout(self):
            aboutwin = Toplevel(master=None,width=555)
            aboutwin.title("About SQA Console Watch")
            aboutwin.geometry('400x200+25+40')
            aboutmsg="           SQA TEST\n        Brocade 2014\
                     \n\nSQA CONSOLE WATCH \n\n"
             
            msg = Message(aboutwin, text=aboutmsg)
            msg.pack()
            
            lbl = Label(aboutwin, text="------------------------------\n\n\n")
            lbl.pack()
            
            button = Button(aboutwin, text="close", command=aboutwin.destroy)
            button.pack()
           
        def saveCnfg(self): 
            s = fileStuff(cw_config_file_name, 'wb')
            eml = "EMLIST: "
            doss = "SS: "
            ftpip = "FTP: "
            
            #el = email_list.get()
            eml += email_list.get()
            doss += str(v.get())
            ftpip += ftpipaddr.get()
            ftpip += " "
            ftpip += ftpuser.get()
            ftpip += " "
            ftpip += ftppass.get()
            
            s.write(eml + "\n")
            s.write(doss + "\n")
            s.write(ftpip)
            s.close
             
        def readCnfg(self):
            #s = fileStuff(cw_config_file_name, 'rb')
            #el = s.read()
            #print(el)
            #email_list.set(el)
            #s.close
            #is_email = ""
            
            for line in open(cw_config_file_name,'rb').readlines():
                remains_line = str(line.strip(), encoding='utf8')
                #print("\n\n====================\n")
                #print(remains_line)
                #print("\n====================\n")
                is_cfg_data = remains_line.split(": ")
                #print("ooooooooooooooooooooooooooooooooooooooooooo")
                #print("is email ")
                #print(is_cfg_data)
                #print("tttttttttttttttttttttttttttttttttttttttttttt")
                if is_cfg_data[0] == "EMLIST":
                    eml = is_cfg_data[1]
                    #print("eml\n")
                    #print(eml)
                    #print("END elist\n")
                    
                if is_cfg_data[0] == "SS":
                    doss = is_cfg_data[1]
                    #print("supportsave config \n")
                    #print(doss)
                    #print("END supportsave config\n")
                    
                if is_cfg_data[0] == "FTP":
                    ftp_data = is_cfg_data[1]
                    ftp_data = ftp_data.split(" ")
                    ftpip = ftp_data[0]
                    ftpu = ftp_data[1]
                    ftpp = ftp_data[2]
                    #print("FTP data for config \n")
                    #print("\nall the data    :   ")
                    #print(ftp_data)
                    #print("\nftp IP address  :   ")
                    #print(ftpipaddr)
                    #print("\nftp user name   :   ")
                    #print(ftpuser)
                    #print("\nftp password    :   ")
                    #print(ftppass)
                    #print("END FTP config DATA\n")
           
            email_list.set(eml)
            v.set(doss)
            ftpipaddr.set(ftpip)
            ftpuser.set(ftpu)
            ftppass.set(ftpp)
            
            
    
        def quit(self):
            sys.exit(0)
             
        
        def cnfgWin(self):
            global email_list, v, ftpipaddr, ftpuser, ftppass
            email_list = StringVar()
            ftpipaddr = StringVar()
            ftpuser = StringVar()
            ftppass = StringVar()
            v = IntVar()
            
            c = Toplevel()
            self.form0 = Frame(c, borderwidth=2, relief="groove")
            self.form1 = Frame(c, borderwidth=2, relief="groove")
            self.form2 = Frame(c, borderwidth=2, relief="groove")
            self.form3 = Frame(c, borderwidth=2, relief="groove")
            self.form0.grid(column=0,row=0)
            self.form1.grid(column=0,row=1,sticky=E+W)
            self.form2.grid(column=0,row=2)
            self.form3.grid(column=0,row=3)
             
            eftp = Entry(self.form1, textvariable=ftpipaddr)
            eftpuser = Entry(self.form1, textvariable=ftpuser)
            eftppass = Entry(self.form1, textvariable=ftppass)
             
            ftplabel = Label(self.form1, text="ftp Configuration")
            ftplabelspace = Label(self.form1, text="             ")
            ftpiplabel = Label(self.form1,    text="ip address")
            ftpuserlabel = Label(self.form1,  text="username")
            ftppasslabel = Label(self.form1,  text="password")
             
            b1 = Button(self.form3, text="Save", command=self.saveCnfg)
            b2 = Button(self.form3, text="Close", command=c.destroy)
            b3 = Button(self.form3, text="Retrieve",command=self.readCnfg)
            #####################################################################
            ####  email label and entry box in frame 0
            elabel = Label(self.form0, text="Email list")
            #l = Label(self.form0, text= "Saved to Config file log\CW_config.txt")
            l = Label(self.form0, text= "       ")
            l2 = Label(self.form0, text="    comma seperate mutli addresses   ")
            e = Entry(self.form0, textvariable=email_list, width=50)
            elabel.grid(row=0,column=0)
            e.grid(row=0,column=1, columnspan=1)
            l.grid(row=2,column=0, columnspan=2)
            l2.grid(row=3,column=0, columnspan=2)
            #####################################################################
            ####  ftp info in frame 1
            
            ftplabel.grid(row=0,column=0, columnspan=2)
            ftplabelspace.grid(row=1,column=1)
            ftpiplabel.grid(row=1, column=0)
            eftp.grid(row=1,column=2)
            ftpuserlabel.grid(row=2,column=0)
            eftpuser.grid(row=2,column=2)
            ftppasslabel.grid(row=3,column=0)
            eftppass.grid(row=3,column=2)
            
            #####################################################################
            ####  checkbox in frame 2
            cbox = Checkbutton(self.form2, text="Enable Auto SupportSave", variable=v)
            cbox.var = v
            cbox.grid(row=0,column=0)
            #####################################################################
            ####  buttons in frame 3
            b1.grid(row=0,column=0)
            b2.grid(row=0,column=1)
            b3.grid(row=0,column=2)
          
            
            
        def donothing(self):
            filewin = Toplevel()
            button = Button(filewin, text="Do Nothing Button")
            button.pack()


class ConsoleData:
    def __init__(self, name, ipaddr, port ):
        self.name = name
        self.ipaddr = ipaddr
        self.port = port
  
class fileStuff:
    
    def __init__(self, name, mode = 'r'):
        self.name = name
        self.mode = mode
        self._f = open(name, mode,0)
    
    def __del__(self):
        self._f.close()
        
    def __iter__(self):
        return self
    
    def write(self, some_text):
        self._f.write(some_text.encode('utf-8'))
        
    def clear(self, mode= 'w'):
        self._f.write("FV MONITOR".encode('utf-8'))
    
    def close(self):
        self._f.close()
    
    def read(self):
        
        self._f.read()
        
        ####    with open("myfile.txt") as fileio:
        ####    info = fileio.readlines() 
       
  
class DoSupportsave():
    
    def __init__(self, ip, user, passw, chas_name ):
        self.ip = ip
        self.user = user
        self.passw = passw
        self.chas_name = chas_name
        self.dirname = ""
        self.createdir()
        self.start()
        
        
    def start(self):
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
        print(capture, end="")
         
    def createdir(self):
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
    
    
     
def email_sender_html(you, me, subj, html_to_send, htmlfile_path = "" ):
    """
    #############################################################################
        send an email from your script as an HTML message
        
        useage is email_sender(senders_email, recipients_email, \
                                subject, message , or text_file)
     
        This is a simple one time send script - - for a client with
        user interface features other choices are available including
        PyMailGUI, pymail, and PyMailCGI
        also see popmail.py for a script that can retrieve mail
    ############################################################################# 
    """
    #### add this inside the <p> paragraph markers to include a link to python
    ####      Here is the <a href="http://www.python.org">link</a> you wanted.
    
    msg = ""
    localhostname = "mail.brocade.com"
   
    print("sending the message via email")
    
    text = "the plain part of the email "
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hello!<br>
           <br>
        </p>
        <p>
            %s
        </p>
      </body>
    </html>
    """ %(html_to_send)  #### use substitution to add the message to html
                         ####   substitute with %s in the body 

    if htmlfile_path == "":
        msg = MIMEText(html, 'html')
        #msghtml = MIMEText(html, 'html')
    else:
        # Create a text/plain message
        fp = open(htmlfile_path, encoding="ascii", errors="surrogateescape" )
        msg = MIMEText(fp.read(), 'html')
        fp.close()
                
    msg['Subject'] = subj
    msg['From'] = me
    msg['To'] = you
    
    #msg.attach(text)
    #msg.attach(msghtml)
    
    # Send the message via our own SMTP server.
    s = smtplib.SMTP(localhostname)
    #s.set_debuglevel(1)
    #s.sendmail(me, you, text)
    s.send_message(msg)
    s.quit()
    return 0
  
  
def add_message_together( orig_msg, add_msg ):
    new_msg = orig_msg
    new_msg += "<br /><br />"  #### html line break
    new_msg += add_msg
    new_msg += "<br /><br />Enjoy your day<br />"
    #print("\n\nHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH\n")
    #print("message for email \n\n")
    #print(new_msg)
    return new_msg
    
def testproc(queue, ipaddr, cport_raw):
     
    time.sleep( 1.3)
    #queue.put("\nHELLO \n")
    ip = ipaddr
    usr = "root"
    pssw = "pass"
    cport = cport_raw
    connect_message = "connected to "
    connect_message += ip
    connect_message += " port "
    connect_message += str(cport)
    connect_message += "\n"
    #############################################################################
    #############################################################################
    #### connect to the console 
    ####
    #fos_response = anturlar.connect_tel(ip,usr,pssw,cport)
    tn = connect_console(ip,usr,pssw,cport)
    
    queue.put(connect_message)
     
    #queue.put(tn)
    time.sleep(1)
    tn.set_debuglevel(0)
    #############################################################################
    #############################################################################
    ####   setup for email 
    ####
    #send_to = ["smckie@brocade.com", "stmckie@yahoo.com"]
    send_cc = ", smckie@brocade.com"
    #############################################################################
    ####
    for line in open(cw_config_file_name,'rb').readlines():
                remains_line = str(line.strip(), encoding='utf8')
                print("\n\n====================\n")
                print(remains_line)
                print("\n====================\n")
                is_cfg_data = remains_line.split(": ")
                print("ooooooooooooooooooooooooooooooooooooooooooo")
                print("is email ")
                print(is_cfg_data)
                print("tttttttttttttttttttttttttttttttttttttttttttt")
                if is_cfg_data[0] == "EMLIST":
                    eml = is_cfg_data[1]
                    print("eml\n")
                    print(eml)
                    print("END elist\n")
                    
                if is_cfg_data[0] == "SS":
                    doss = is_cfg_data[1]
                    print("supportsave config \n")
                    print(doss)
                    print("END supportsave config\n")
                    
                if is_cfg_data[0] == "FTP":
                    ftp_data = is_cfg_data[1]
                    ftp_data = ftp_data.split(" ")
                    ftpip = ftp_data[0]
                    ftpu = ftp_data[1]
                    ftpp = ftp_data[2]
                    print("FTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTP")
                    print("FTP DATA\n\n")
                    print(ftpip)
                    print("\n")
                    print(ftpu)
                    print("\n")
                    print(ftpp)    
                    print("\n\nFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTPFTP\n\n")
    send_to = eml
    send_to += send_cc  #### to remove smckie from email remove this line
                        
    print("\n\n====================================")
    print("email list for errors is  ")
    print(send_to)
    print("====================================\n")
    #send_to = "smckie@brocade.com"  #### this works for one email address
    send_from = "console_watch_"
    subject = "An interesting event was found watching the console"
    message_TS =      "Found a TS message was sent "
    message_MAPS =    "Found a MAPS message on the Console"
    message_BNECK =   "Found a Bottleneck message on the Console"
    message_RTWR =    "Found a RTWR message on the Console"
    message_ROUTE =   "Found a ROUTE RAS LOG message on the Console"
    message_BCKCRD =  "Found a Backend Credit Error on the Console"
    message_RPM =     "Found a RPM Route Error on the Console"
    message_CxMSG =   "Found a Cx-10nn message on the Console"
    message_Cx5MSG =  "Found a Cx-5nnn message on the Console"
    message_OOM =     "Found a Out Of Memory Error on the Console"
    message_IPRULE =  "Found the message ERROR: Failed to enforce new iptables rules"
    message_ERROR  =  "Found an ERROR message: "
    
    
    #################################################################
    #################################################################
    #### clear the log file
    ####
    rasfile = "%s%s%s%s%s" % ("logs\\raslog", ip,".", cport, ".txt")  #### %s string  %d number
    cons_capture_file = "%s%s%s%s%s" % ("logs\\cons_capture", ip,".", cport, ".txt") 
    #print("my rasfile is   \n==============================\n")
    #print(rasfile)
    #print("\n====================================\n\n")
    ras_log_file = fileStuff(rasfile, 'w+b')  #### reset the log file
    #ras_log_file.clear()
    ras_log_file.close()
    
    ras_log_file = fileStuff(rasfile, 'a+b')  #### open the log file for writing
    ras_log_header = "%s%s%s" % ("RASLOG CAPTURE FILE \n", ip, "\n==========================\n\n")
    ras_log_file.write(ras_log_header)
     
    
    cons_log_file = fileStuff(cons_capture_file, 'w+b')
    cons_log_file.close()
    
    cons_log_file = fileStuff(cons_capture_file, 'a+b')
    cons_log_file.write("CONSOLE CAPTURE FILE\n")
    cons_log_file.write(ip)
    
    #############################################################################
    #### look for the following in the console output
    ####
    ####
    ####
    ####   
    ####  Message that do not require trace dump - 
    ####        they will be captured and counted.
    ####    using this regex to capture any remaining RAS log message
    ####    \[-0-9/:](19,26), \[\[A-Z0-9](2,4)-\[0-9](4)].*\\n
    ####
    capture = ""
    reg_ex_list = [b'root> ', b'.*\r\n']
    reg_ex_list_chassis = [b'.*\n']
    rasmessage_any = re.compile("[-/\d:]{3,26}, \[[A-Z0-9]{2,4}-[0-9]{4}],.*\\n")  #### tested
    rasmessage_MAPS = re.compile("\[MAPS-[0-9]{4}],.*\\n")            #### tested
    rasmessage_BNECK = re.compile("\[AN-10[1-9][0-9]],.*\\n")         #### tested 
    rasmessage_RTWR = re.compile("\[RTWR-[0-9]{4}],.*\\n")            #### tested
    rasmessage_ROUTE = re.compile("\[C[DR]{2}-5[0-9]{3}],.*\\n")      #### tested
    rasmessage_RPM = re.compile("\[RPM-710[0-9]],.*\\n")              #### tested 
    rasmessage_CxMSG = re.compile("\[C[2-9]-10[0-9]{2}],.*\\n")       #### tested
    rasmessage_Cx5MSG = re.compile("\[C[2-9]-5[0-9]{3}],.*\\n")       #### tested  supportsave
    rasmessage_OOM = re.compile("\[RM-70[0-9]{2}],.*\\n")             #### tested
    rasmessage_IPRULE = re.compile("ERROR: Failed to enforce new iptables rules")
    
    
    rasmessage_MAPS_short = rasmessage_MAPS = re.compile("\[MAPS-[0-9]{4}]") #### tested
    rasmessage_RTWR_short = rasmessage_RTWR = re.compile("\[RTWR-[0-9]{4}]") #### tested
    rasmessage_ERROR0_short = re.compile("\[FCIP-1000]|\[FCIP-5039]|\[FCIP-5665]|\[RPM-7100]|\[RPM-7101]|\[AUTH-1014],\
                                         |\[AUTH-1044]|\[SNMP-1004]|\[BLS-1000]|\[BLS-5024]|\[BLS-5039]|\[BLS-5665],\
                                         |\[MPTH-1001]|\[MPTH-1002]|\[SULB-1037]|\[FLOD-1004]|\[CDR-1002]|\[NBFS-1002],\
                                         |\[EM-1020]|\[EM-1068]|\[HLO-100[12]]|\[FABR-1011]|\[FABR-1041],\
                                         |\[ANV-1002]|\[EM-1068]|\[C[2-9]-1002]|\[CHS-1002]|\[BLS-1000],\
                                         |\[FSS-1009]|\[RAS-6000]|\[RM-7024]|\[RM-7031]|\[BLM-5047]|\[FLOD-1004],\
                                         |\[AUTH-1014]|\[BLS-5665]|\[FABR-1041]|\[NBFS-1002]|\[FCIP-1000],\
                                         |\[FLOD-1004]")
    
    
    
    
    #############################################################################
    #############################################################################
    #### setup to watch for hidden messages
    ####
    capture = ""
    cmd = "ln -s /fabos/cliexec/raslogt /sbin/errlogutest"
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    capture = tn.expect(reg_ex_list, 10)
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    #queue.put(capture)
    capture = ""
    cmd = "errlogutest -f -t3 -a1 -i -1 -t3 -s4"
    cmd = "errlogutest -f -i -1 -t3 -s4"
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    capture = tn.expect(reg_ex_list, 10)
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    #queue.put(capture)
    print("\nend for setting hidden messages\n\nuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu\n\n")
    count = 0
    new_ras_message = "old"
    
    #############################################################################
    #############################################################################
    #### get some switch info
    ####
    chass_name = "CHASSIS_NAME"
    ip_address = "-unknown-"
    ras_message_dict = {}
    ras_message_dict = {"chassis_name":chass_name}
    ####################################################################
    capture = ""
    cmd = "chassisname"
    reg_ex_list_only_root = [b'(.*\d\\r\\n )']
    reg_ex_list_only_cmd = [ cmd.encode()]
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    #capture = tn.expect(reg_ex_list_only_cmd, 10)
    capture = tn.expect(reg_ex_list_only_root, 10)
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    #############################################################################
    #############################################################################
    chass_re = re.compile('([chassisname]{11})\\r\\n([a-zA-Z0-9_]{0,31})\\r\\n')
    chass_name = chass_re.search(capture)
    #print("\n1111111111111111111111111111111111111111111111111111111111111111111\n")
    print(chass_name.group(0))
    #print("\n222222222222222222222222222222222222222222222222222222222222222222222\n")
    print(chass_name.group(1))
    #print("\n333333333333333333333333333333333333333333333333333333333333333333333\n")
    print(chass_name.group(2))
    chass_name = chass_name.group(2)
    ras_message_dict = {"chassis_name":chass_name}
    
    
    ###################################################################
    ###################################################################
    #### get the ip address  
    ####
    capture = ""
    cmd = "ipaddrshow"
    reg_ex_list_only_root = [b'(.*root> )']
    reg_ex_list_only_cmd = [ cmd.encode()]
    tn.write(cmd.encode('ascii') + b"\n")
    
    capture = tn.expect(reg_ex_list_only_root, 10)
    capture = capture[2]
    capture = capture.decode()
    #queue.put(capture)
    ipaddr_re = re.compile('(ipaddrshow)\\r\\n([A-Za-z0-9 \\r\\n]+): ([0-9\.]{7,15})')
    ip_addr = ipaddr_re.search(capture)
    
    print("\n0000000000000000000000000000000000000000000000000000000000000000\n")
    print(ip_addr.group(0))
    print("\n1111111111111111111111111111111111111111111111111111111111111111111\n")
    print(ip_addr.group(1))
    print("\n222222222222222222222222222222222222222222222222222222222222222222222\n")
    print(ip_addr.group(2))
    print("\n333333333333333333333333333333333333333333333333333333333333333333333\n")
    print(ip_addr.group(3))
    print("\n4444444444444444444444444444444444444444444444444444444444444444444444\n")
    ip_address = ip_addr.group(3)
    
    ras_message_dict["ip_address"] = ip_address
    ###################################################################
    ###################################################################
    ###################################################################
    ###################################################################
    capture = ""
    
    while TRUE :
        capture = tn.expect(reg_ex_list, 10)
        capture = capture[2]
        capture = capture.decode()
        #queue.put(capture)
        cons_log_file = fileStuff(cons_capture_file, 'a+b')
        cons_log_file.write(capture)
        cons_log_file.write("\n")
        cons_log_file.close
        
        ras_message_dict_Items = ras_message_dict.items()
        if new_ras_message == "new":
            #queue.put("\r\n-----\r\n")
            for ras, value in ras_message_dict_Items:
                add_to_queue = [ ras , value]
                #queue.put(add_to_queue)
            new_ras_message = "old"
            queue.put(list(ras_message_dict.items()))
             
        if re.search("\[TS-1006]", capture):                  #####  tested 
            print("\n\n\nTIME SERVER UPDATE \n\n\n")
            #email_sender_html(send_to, send_from, subject, message_TS)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            
            
        elif rasmessage_MAPS.search(capture):                 #### tested 
            ras_long = rasmessage_MAPS.search(capture)
            ras = rasmessage_MAPS_short.search(capture)
            message_MAPS_ras = add_message_together(message_MAPS, ras.group(0))
            ras_log_file.write(capture)
            ras_log_file.write("\n")
           
            if ras.group(0) in ras_message_dict :
                count = ras_message_dict.get(ras.group(0))
                count += 1
                ras_message_dict[ras.group(0)] = count
            else:
                ras_message_dict[ras.group(0)] = 1
            new_ras_message = "new"
               
                  
        elif rasmessage_BNECK.search(capture):                 #### need to test
            ras = rasmessage_BNECK.search(capture)
            message_BNECK_ras = add_message_together(message_BNECK, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_BNECK_ras)
            print("\n\n\nBottleneck error\n\n\n")
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            
        elif rasmessage_RTWR.search(capture):               ####  tested
            ras_long = rasmessage_RTWR.search(capture)
            ras = rasmessage_RTWR_short.search(capture)
            message_RTWR_ras = add_message_together(message_RTWR, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_RTWR_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            
            if ras.group(0) in ras_message_dict :
                count = ras_message_dict.get(ras.group(0))
                count += 1
                ras_message_dict[ras.group(0)] = count
            else:
                ras_message_dict[ras.group(0)] = 1
            new_ras_message = "new"
            
        elif rasmessage_ERROR0_short.search(capture):       #### still needs updates
            ras = rasmessage_ERROR0_short.search(capture)   #### to the ras message numbers
            message_RTWR_ras = add_message_together(message_ERROR, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_RTWR_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            
            if ras.group(0) in ras_message_dict :
                count = ras_message_dict.get(ras.group(0))
                count += 1
                ras_message_dict[ras.group(0)] = count
            else:
                ras_message_dict[ras.group(0)] = 1
            new_ras_message = "new"
          
            print("START SUPPORTSAVE")
            
            dss = DoSupportsave(ftpip, ftpu, ftpp, chass_name )
            
            print("END SUPPORTSAVE")
             
        elif rasmessage_ROUTE.search(capture):          #### need to test 
            ras = rasmessage_ROUTE.search(capture)
            message_ROUTE_ras = add_message_together(message_ROUTE, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_ROUTE_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            
        elif rasmessage_RPM.search(capture):          #### need to test 
            ras = rasmessage_RPM.search(capture)
            message_RPM_ras = add_message_together(message_RPM, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_RPM_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            print("\n\nroute programming error\n\n") 
          
        elif rasmessage_CxMSG.search(capture):          #### need to test 
            ras = rasmessage_CxMSG.search(capture)
            message_CxMSG_ras = add_message_together(message_CxMSG, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_CxMSG_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            print("\n\nCx message C3-10nn  message\n\n")  
         
        elif rasmessage_Cx5MSG.search(capture):          #### need to test 
            ras = rasmessage_Cx5MSG.search(capture)
            message_Cx5MSG_ras = add_message_together(message_Cx5MSG, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_Cx5MSG_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            print("\n\nerror error  c3-5nnn message \n\n") 
         
            if ras.group(0) in ras_message_dict :
                count = ras_message_dict.get(ras.group(0))
                count += 1
                ras_message_dict[ras.group(0)] = count
            else:
                ras_message_dict[ras.group(0)] = 1
            new_ras_message = "new"
            print("START SUPPORTSAVE")
            dss = DoSupportsave(ftpip, ftpu, ftpp, chass_name )
            print("END SUPPORTSAVE")
            
            
        #elif rasmessage_OOM.search(capture):          #### need to test 
        #    ras = rasmessage_OOM.search(capture)
        #    message_OOM_ras = add_message_together(message_OOM, ras.group(0))
        #    email_sender_html(send_to, send_from, subject, message_OOM_ras)
        #    ras_log_file.write(capture)
        #    ras_log_file.write("\n")
        #    print("\n\nsystem out of memory errors\n\n")
            
        elif rasmessage_IPRULE.search(capture):          #### need to test 
            ras = rasmessage_IPRULE.search(capture)
            message_IPRULE_ras = add_message_together(message_IPRULE, ras.group(0))
            email_sender_html(send_to, send_from, subject, message_IPRULE_ras)
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            print("\n\nERROR: FAILED to enforce new IPtables rule\n\n")
        
        #########################################################################    
        #### find any RAS log message not already captured above
        elif rasmessage_any.search(capture):
            #ras_log_file = fileStuff(rasfile, 'a+b')
            ras_log_file.write(capture)
            ras_log_file.write("\n")
            #ras_log_file.close
            print("\nfound a RAS LOG message with the second search\n\n")
            print(capture)
            
    ###################################################################
    ###################################################################
    ##### how to write and read to the switch
    ###################################################################
    ###################################################################
    ####  this section does nothing because of the loop above
    #### this is for reference on how to send commands to the
    ####  switch / console 
    ###################################################################
    capture = ""
    cmd = "setcontext 88"
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    
    
    capture = tn.expect(reg_ex_list, 10)
    
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    queue.put(capture)
    #########################################################
    #########################
    
    #fos_response = anturlar.fos_cmd_w_tn("setcontext 88", tn)
    #queue.put(fos_response)
    #queue.put("change context to 88")
   
    #time.sleep( 5.3)
    #
    #fos_response = anturlar.fos_cmd_w_tn("switchshow", tn)
    #queue.put(fos_response)
    #queue.put("change context to 88")
    
    #time.sleep( 5.3)
    
    #anturlar.close_tel_w_tn(tn)
    capture = ""
    cmd = "setcontext 25"
    print(cmd)
    tn.set_debuglevel(10)
    tn.write(cmd.encode('ascii') + b"\n")
    
    #reg_ex_list = [b"login: ", b"Password: ", b"option :", b"root> "]
    reg_ex_list = [b"i knwo u wont capture this"] 
    #capture = tn.expect("root> ", 60)
    capture = tn.expect(reg_ex_list, 10)
    #capture = tn.read_until(b'asdsad', 33)
    
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    queue.put(capture)

    capture = ""
    cmd = "fabricshow"
    print(cmd)
   
    tn.write(cmd.encode('ascii') + b"\n")
    
    reg_ex_list = [ b"root> "]
     
    capture = tn.expect(reg_ex_list, 10)
    #capture = tn.expect("root> ", 60)
    #capture = tn.read_until(b'asdsad', 33)
  
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    queue.put(capture)
    
    
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
        
    
    #############################################################################
    #### login to the switch
    reg_list = [ b"Enter your option", b"login: ", b"assword: ", b"root> " ]  
    while var <= 4:
        #print("start of the loop var is equal to ")
        capture = tn.expect(reg_list)
        print(capture)
        
        if capture[0] == 0:
            tn.write(b"1\r\n\r\n")
                    
        if capture[0] == 1:
            tn.write(b"root\r\n")
                
        if capture[0] == 2:
            tn.write(b"password\r\n")
                    
        if capture[0] == 3:
            print(capture)
            break
        
        var += 1   
        
    capture = tn.expect(reg_list,30)
    
    return tn

#################################################################################
#################################################################################
#### start main                                                              ####
#################################################################################
#################################################################################

if __name__ == "__main__":
    
    q = Queue()
    
    cw = FV(None, q)
    cw.title('FLOW VISION MONITOR')
    
    cw.mainloop()
    
    
    