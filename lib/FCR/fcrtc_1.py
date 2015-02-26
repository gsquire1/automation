#!/opt/python3/bin/python3

def main():
    """
    Without the main sentinel, the code would be
    executed even if the script was imported as a module
    """
##########################################################
#import needed modules
import anturlar
import liabhar
import cofra
import maps_tools


##########################################################
#Perform config upload

def tc_22_2_1_2(ftp_ip, ftp_user, ftp_pass, clear = 0):
    """
    Test Case(s)   22.2.1.2.1, 22.2.1.2.2, 22.2.1.2.3
    Title:      FCR Enable/Disable
    Feature:    FCR 
    Enabling and disabling the FCR service
        
    """
    ###########################################################################
    ####  todo -
    ####
    ####   1.  pass / fail for each step of test case
    ####       make the test_result a list of list [ step_0 pass ][step_2 fail]
    ####   2.  ignore chassis rules on a pizza box    
    ####   3.  configupload will be tested as the config will be reset to default and then put back down
    ####
    ###########################################################################
    ####
    ####  steps
    ####
    ####  1. Do configupload
    ####  2. Do config default
    ####  3. Default status (tc 2.1.2.3)
    ####  4. FCR Functionality Persist (tc 2.1.2.1)
    ####  5. Config EX ports
    ####  6. FCR disable with EX/VEX ports enabled
    ####  7. Put switch back to original config
    ####
    #### start the test
    
#def cfgul(ftp_ip, ftp_user, ftp_pass, clear = 0):
#def cfgul():
    cofra.cfgupload(ftp_ip, ftp_user, ftp_pass, clear = 0)
    liabhar.JustSleep(3)
    cofra.cfgdownload(ftp_ip, ftp_user, ftp_pass, clear = 0)


###############################################################################
#STEVE'S EXAMPLE
####################

    test_numb = "25.01.01.03.01"
    test_summary = "%s    MAPS Catergory Management Default thresholds" % test_numb
    header = maps_tools.format_header(test_summary)
    test_result = ""
    
    p = anturlar.Maps()
    sut_ip = p.ipaddress()
    sw_rules = p.get_rules()
    
     #### set up the log file info
    f_path = '/home/run_from_here/logs/%s_%s' % (test_numb, sut_ip)
    
    f = liabhar.FileStuff(f_path, 'w+b')
    f.write(header)
    
    #sw_rules = str(sw_rules)
    #sw_rules = sw_rules.replace("'", "") #### remove ' from string
    #sw_rules = sw_rules.replace("[", "") #### remove open bracket
    #sw_rules = sw_rules.replace("]", "") #### remove ending bracket
    df_rules = maps_tools.maps_default_rule()
    
    sw_rules = sw_rules.split()
    df_rules = df_rules.split()
    
    count_df = len(df_rules)
    count = len(sw_rules)
    if count < count_df:
        loop_count = count
    else:
        loop_count = count_df
    i =0
    rule_differ = 0
    while i < loop_count:
        print("\n\ncomparing switch rule with default rule ")
        print("%s      %s " % (sw_rules[i], i ))
        if sw_rules[i] not in df_rules:
            rule_differ += 1
            test_result += sw_rules[i]
            test_result += ' step1'
            test_result += ' Fail\n'
            print("\nFail Fail Fail Fail\n\n")
        
        i += 1
        
    print("The number of rules that differ are %s " % rule_differ)
    print("The number of additional rules on the switch %s " % ( count - count_df))
    print(len(sw_rules))
    print(len(df_rules))
    f.write("The number of rules that differ are %s \r\n" % rule_differ)
    f.write("The number of additional rules on the switch %s \r\n" % ( count - count_df))
    f.write("Total number of switch rules    %s  \r\n" % len(sw_rules))
    f.write("Total number of default rules   %s  \r\n" % len(df_rules))


    if test_result == "":
        test_result = "PASS"
    
    print("="*80)
    print("\n\nTEST RESULTS FOR Test Case   25.01.01.03.01 ")
    print(test_result)
    f.write(maps_tools.format_results(test_summary, test_result))
       
    return(test_result)

if __name__ == '__main__':
    main()

