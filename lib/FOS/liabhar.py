#!/usr/bin/env python3


import smtplib
import random
import argparse
import difflib
import filecmp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import datetime
import time


"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""





class dateTimeStuff:
    
    def __init__(self):
        pass
    
    def current(self):
        i = datetime.datetime.today()  #### ISO format 2013-02-21 06:35:45.707450
        return(i) 
    
    def stamp(self):
        t = time.time()  #### timestamp in form 1361446545.52
                         #### use datetime.dat e.fromtimestamp(t) to get a date 2013-02-21
        return(t)
    
    def simple(self):
        s = datetime.date.today()  #### format is 2013-02-21
        return(s)
    
    def simple_no_dash(self):
        s = datetime.date.today()  #### format is 2013-02-21
        w = str(s)
        ss = w.replace("-","")
        return(ss)
    
    #def ordinal(self):
    #    o = today.ordinal() #### format is 734920
    #    return o

class FileStuff:
    """
        a simple class to open files for reading and writing
        
    """
    def __init__(self, name, mode = 'r'):
        self.name = name
        self.mode = mode
        self._f = open(name, mode,0)
    
    def __del__(self):
        #self._f.close()
        self._f.close()
        
    def __iter__(self):
        return(self)
    
    def write(self, some_text):
        """
        Write some files with utf_8 encoding
        """
        self._f.write(some_text.encode('utf-8'))
        #self._f.write(some_text)
    
    def clear(self, mode= 'w+'):
        """
        Clear files/overwrite
        """
        self._f.write(" ")
    
    def close(self):    
        """
        Close file
        """
        self._f.close()
        
    def readlines(self):
        """
        Reads entire file into memory
        """
        self._f.readlines()
        
    def readline(self):
        """
        Reads file one line at a time
        """
        self._f.readline()
        
    def read(self):
        """
        Reads file into 1 entire string.
        Good for handling text all at once.
        Use with RegEx
        """
        self._f.read()


def cls():
    """
       clear the screen
       valid for Linux or Windows
    """
    from subprocess import call
    from platform import system
    os = system()
    if os == 'Linux':
        call('clear', shell = True)
    elif os == 'Windows':
        call('cls', shell = True)
    
def count_down(stop):
    """
        print to the screen a countdown timer
        pass only the amount of time to wait
    """
    print("\n\n")
    while  stop >= 0 :
        print("     ",end="")
        print(stop, end="\r")
        time.sleep(1)
        print("          ", end="\r")
        stop += -1
    
    return(True)

def file_diff(a,b,extend_name=""):
    """
    Compare two files for differences, print only differences to console and
    put in a file in logs directory.
    """

    #a = "/home/RunFromHere/logs/10.38.36.67.txt"
    #b = "/home/RunFromHere/logs/10.38.36.167.txt"
    #difference = ("/home/RunFromHere/logs/difference_%s.txt" % c)
    difference = ("logs/difference_%s.txt" % extend_name)
    #filecmp = difflib.Differ()
    
    z = filecmp.cmp(a,b)
    if z == True:
        print("\n\nThe files are the same")
        return(True)
    else:
        with open (a) as File1:
            c = File1.readlines() 
        with open (b) as File2:
            d = File2.readlines()
    print('\n')
    for line in difflib.context_diff(c,d, fromfile=(a), tofile=(b), n=0):
        print((line))
    with open (difference, 'w') as differ:
        for line in difflib.context_diff(c,d, fromfile=(a), tofile=(b), n=0):
            differ.write(line)    
    return(False) ## false would mean that there are differences 


def diff_compare(text_1, text_2):
    """
        compare string text line by line
        return the differences
    """
    print("\n"*10)
    print("TeXT  1: \n  ", text_1)
    print("TEXT 2: \n ", text_2)
    print("\n"*10)
    text_lines_1 = text_1.splitlines()
    text_lines_2 = text_2.splitlines()
    r = ""
    d = difflib.Differ()
    diff = d.compare(text_lines_1, text_lines_2)
    
    r = r.join(diff)
    
    return(r)

def diff_ncompare(text_1, text_2):
    """
        compare list text line by line
        return the differences
    """
    print("\n"*10)
    print("TeXT  1: \n  ", text_1)
    print("TEXT 2: \n ", text_2)
    print("\n"*10)
    text_lines_1 = text_1.splitlines()
    text_lines_2 = text_2.splitlines()
    r = ""
     
    diff = difflib.ndiff(text_lines_1, text_lines_2)
    
    r = r.join(list(diff))
    
    return(r)
    
    
    


def email_sender(who_to, who_from, subj, msg_to_send, txtfile_path = ""):
    """
    #############################################################################
        send an email from your script in plain text
        
        useage is email_sender(senders_email, recipients_email, \
                                subject, message , or text_file)
        
        This is a simple one time send script - - for a client with
        user interface features other choices are available including
        PyMailGUI, pymail, and PyMailCGI
        also see popmail.py for a script that can retrieve mail
    #############################################################################    
    """
    
    msg = ""
    localhostname = "mail.brocade.com"
  
    print("Sending your message via Email")

    if txtfile_path == "":
        msg = MIMEText(msg_to_send, 'plain')
    else:
        # Create a text/plain message
        fp = open(txtfile_path, encoding="ascii", errors="surrogateescape" )
        msg = MIMEText(fp.read())
        fp.close()
                
    msg['Subject'] = subj
    msg['From'] = who_from
    msg['To'] = who_to
    # Send the message via our own SMTP server.
    s = smtplib.SMTP(localhostname)
    #s.set_debuglevel(1)              #### enable to show all email tasks
    #s.sendmail(me, you, text)
    s.send_message(msg)
    s.quit()
    if s:
        print("Failed Recipients: " , s)
    else:
        print("No Errors on Sending Emails")
    
    return(True)

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
    
    msg = ""
    localhostname = "mail.brocade.com"
   
    print("sending the message via email")
    
    text = "the plain part of the email "
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="http://www.python.org">link</a> you wanted.
           <br>
           
           Message:<br>
           replace_me
           
           
        </p>
      </body>
    </html>
    """
    html = html.replace("replace_me", html_to_send)

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
    return(True)

def JustSleep(s):
    time.sleep(s)

    
def platform():
    """
        print the platform 
        
    """
    
    #from subprocess import call
    #from platform import system
    #os = system()
    #print(os)
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        os = "linux"
    elif _platform == "darwin":
        os = "OS X"
    elif _platform == "win32":
        os = "Windows"
        
    return(os)    




def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    pp.add_argument("--repeat", help="repeat repeat")
    pp.add_argument("ip", help="IP address of SUT")
    pp.add_argument("user", help="username for SUT")
    pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
    
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    
    return(pp) 

def parse_args(args):
    
    global tn,sw_user
    verb_value = "99"
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    #parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-s', '--suite', type=str, help="Suite file name")
    parser.add_argument('-p', '--password', help="password")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    #group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")
    #
    args = parser.parse_args()
    #print("Connecting to IP :  " + args.ip)
    #print("user             :  " + args.user)
    ipaddr = args.ip
    sw_user = args.user
    verbose = args.verbose
    fid = args.fid
    
    #if args.verbose >= 2:
    #    print("verbosity is Enabled and set to 2")
    #elif args.verbose >= 1:
    #    print("verbosity is Enabled and set to 1")
    #else:
    #    print("verbosity        :  disabled")
    #if args.fid == 0:
    #    print("fid              :  no fid given")
    #else:
    #    print("Using fid number :  %s " % fid)

    return(parser.parse_args())

def parse_args_fillword(args):
    global tn,sw_user
    parent_p = parent_parser()
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")
    #parser.add_argument("-f", "--fid", type=int, default=0, help="Choose the FID to operate on")
    parser.add_argument("fillword_number", default=None, type=int, choices=[0, 1, 2, 3],
            help="Choose a number below for type of fillword to be used:\n\
    0 - idle-idle   - IDLE in Link Init, IDLE as fill word - default\n\
    1 - arbff-arbff - ARBFF in Link Init, ARBFF as fill word\n\
    2 - idle-arbff  - IDLE  in Link Init, ARBFF as fill word -SW\n\
    3 - aa-then-ia  - If ARBFF/ARBFF failed, then do IDLE/ARBFF")
    args = parser.parse_args()
    print("Connecting to IP :  " + args.ip)
    print("user             :  " + args.user)
    ipaddr = args.ip
    sw_user = args.user
    verbose = args.verbose
    fid = args.fid
    if args.verbose >= 2:
        print("verbosity is Enabled and set to 2")
    elif args.verbose >= 1:
        print("verbosity is Enabled and set to 1")
    else:
        print("verbosity        :  disabled")
    if args.fid == 0:
        print("fid              :  no fid given")
    else:
        print("Using fid number :  %s " % fid)

    return(parser.parse_args())


    
def random_number():
    """
        returns a random number between 0.0 and 1.0 
    """
    n = random.random() #### random.randrange also
    return(n)

def random_number_int(x):
    """
    returns a random interger between 0 and the number passed in
    
    """
    my_int = random_number() * x
    y = round(my_int) - 0.5
    y = int(y) + (y>0)
    return(y)

def space(a=8):
    """
        Prints a number of blank lines passed to the procedure
    """
    for i in range(a):
        print("\n") 
    return(True)



    

    
    

    
    
    
    
    