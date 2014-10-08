#!/opt/python3/bin/python3

###############################################################################
####   Import system modules here                                          ####
###############################################################################

import os,sys
sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/FCR')
sys.path.append('/home/automation/APM')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')


from multiprocessing import Process,Queue
import getpass
import time
###############################################################################
####   Import user modules here and set system paths                       ####
###############################################################################
import liabhar
import anturlar
import cofra
###############################################################################
####   Import test case modules here                                       ####
###############################################################################
import fvtc_0
import fcrtc_0
import fos_gen_tc_0
import traffic_tools


###############################################################################
####   Print the summary of what will be tested                            ####
###############################################################################

def header(theargs, these):
    
    print("\n")
      
    print("    IP ADDRESS of TARGET SWITCH     :   %s " % theargs.ip)
    print("    FABRIC ID                       :   %s " % theargs.fid)
    print("    FABRIC WIDE TEST                :   %s " % theargs.fabwide)
    print("    USER NAME                       :   %s " % theargs.user)
    print("\n")
    print("    SUITE FILE USED                 :   %s " % theargs.suite)
    print("\n")
    print("    VERBOSE                         :   %s " % theargs.verbose)
    print("    REPEAT THE TEST                 :   %s " % theargs.repeat)
    print("    QUIET MODE                      :   %s " % theargs.quiet)
    print("    IP FILE                         :   %s " % theargs.ipfile)

    print("\n\n\n")
    print("      SUITE FILE INCLUDES THE FOLLOWING")
    print("             TEST CASES  TO RUN   ")
    print("="*60)
    
    for t in these:
        print("      %s" % t)
    

###############################################################################
####  Start the test process
###############################################################################

def testprocess( theargs, run_these, password ):
    print("\n\n\n")
    print("="*60)
    #header(theargs, run_these)
    #print(theargs)
    #print(run_these)l = sys.argparse.Namespace

            
                
    conn_value = anturlar.connect_tel(theargs, password )
    
    for i in run_these:
        print("run these test   %s"%i )
        #test_to_run = "test_case_0."
        test_to_run = ""
        paramlist = ""
        i.pop(0)
        h = True
        for j in i:
            if h :
                h = False
                test_to_run = test_to_run + j +"("
            else:
                test_to_run = test_to_run + j 
                paramlist = j
            
        test_to_run = test_to_run + ")"
        #print("\n\n", test_to_run, "\n\nEND OF TEST TO RUN")
        conout = anturlar.fos_cmd("switchshow")
        
        if paramlist == "" :
            eval(test_to_run)
        else:
            print("\n\n param list is  %s "%paramlist)
            eval(test_to_run)
            
###############################################################################        
#### close the telnet connection and end the test
###############################################################################
    anturlar.close_tel
###############################################################################  
    
    
def user_start():
    go = False
    start = 'n'
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nSTART THE TEST ?  [y/n] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                sys.exit()
                
        if start == 'y':
            go = True
        else:
            sys.exit()
###############################################################################


def main():   
    
    ###########################################################################
    ####  the module will start a suite of test 
    ####  
    ####   1. start from the command line - parse the args
    ####   2. determine if switch or fabric test  - user input default to switch
    ####   3. determine which test case to run  - read from a config file
    ####   4. start each test case in a seperate process
    ####   5. return the results of the complete suite -- need to wait for each 
    ####          process to exit ( each test case to complete )
    ####
    ####
    ###############################################################################
    ####    Step 1
    #### parse of the command line is done when the test is started            ####
    ###############################################################################
    #### confirm you are in your $HOME directory
    ####  if not move to the user HOME directory and continue
    ####    ####    ####
    liabhar.cls()
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)
    cwd = os.getcwd()
    path = os.path.join(cwd,"logs")
    if os.path.exists(path):
        pass
        ##liabhar.count_down(1)
    else:
        print("\n\nChanging to your HOME directory\n\n")
        homepath = os.getenv('HOME')
        os.chdir(homepath)
        cwd = os.getcwd()
        print(cwd)
    pa = liabhar.parse_args(sys.argv)
    #print(pa)
    ###########################################################################
    ####  if no password ask the user for the password
    ####
    ###########################################################################
    pw = "password"
    if not pa.password:
        pw = getpass.getpass()
    ###############################################################################
    ####    Step 2                                                             ####
    ####   is the testing switch only or fabric wide                           ####
    ####    the variable is in the parse args  fabwide 0 = switch only         ####
    ###############################################################################
    #print("#"*80)
    #print("#"*80)
    if pa.fabwide == False:
        print("    Testing in switch mode")
    else:
        print("    Testing in fabric wide mode")
    ###############################################################################
    ####    Step 3                                                             ####
    ####   what test case do i run  -- read a config file                      ####
    ####          the file is in logs/config or logs  still open question      ####
    ###############################################################################  
    #suite_name = pa.suite
    cw_config_file_name = "%s%s%s"%("ini/",pa.suite,".txt")
    fileIN = open( cw_config_file_name, 'rb')
    testcaselist = []
    #print("Running the following Test Cases")
    #print("#"*32)
    for line in fileIN:
        line = str(line.strip(), encoding='utf8')
        line = line.split(" ")
        #for j in line:
            #print("list item  %s  "%j )
        if line[0] == 'Y':
            testcaselist.append(line)
    #print("test case list  \n")
    #print(testcaselist)
    #print("#"*80)
    #print("#"*80)
    ###########################################################################
    ####    Step 4                                                         ####
    #### Start the appropriate test to each switch  or  Fabrica Wide  or   ####
    ####   or read the file for a list of IP.                              ####
    ####                                                                   ####
    ###########################################################################
    #### take the testcaselist
    if pa.fabwide:
        conn_value = anturlar.connect_tel(pa, pw )
        si = anturlar.SwitchInfo
        fabi = anturlar.FabricInfo(pa.fid)
        fablist = fabi.ipv4_plus_fcr_list(pa,pw)
        anturlar.close_tel()
                
        time.sleep(1)
        liabhar.cls()
        print("@"*60)
        print("@"*60)
        print("\n    FABRIC LIST OF IP TO BE TESTED : ")
        print("-"*60)
        for ip in fablist:
            print("    %s" % ip)
        
        header(pa, testcaselist)
        user_start()
        for ip in fablist:
            #print("\n\n\n\n%s"%ip)
            pa.ip = ip
            p = Process(target=testprocess, args=(pa, testcaselist, pw))
            p.daemon = False
            p.start()
            
    elif pa.ipfile:
        
        pass
    
    else:
         
        header(pa,testcaselist)
        user_start()
        p = Process(target=testprocess, args=(pa, testcaselist, pw))
        #p.daemon = True  #### use True value all child process will stop when the main process stops
        p.daemon = False  #### this will run in the background even if this script finishes
        p.start()
        time.sleep(0.1)
    #print("\nprocess exit code is %s"%p.exitcode)
    #time.sleep(5.1)
    #print("\nprocess exit code is %s"%p.exitcode)
    print("\n\n        TESTING STARTED IN ANOTHER CONNECTION ")
    print("            EXITING THIS CONNECTION")   
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)



#################################################################################
#################################################################################
####
####
main()







