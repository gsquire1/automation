#!/usr/bin/env python3

# Script to plot the the increase in memory detected in the history files stored in FOS
# Created by: David Ward
# Shared from: https://drive.google.com/drive/folders/1kB3hWezV_cLWBX13MoD9xBinbYKfK9Py
# Updated: 3/23/18

#[]is optional
#()is required
#- dashes are option
#<this> is an argument
"""Usage: pyPlot.py <IP>...  [options] |--help


Script to process memory history files stored in FOS. Will gather from /var/log/mstatdir
for as many files as the uptime will allow up to the maximum of 31 days.

Arguments:
  IP                IPv4 or IPv6 address of switch(es) to be examined


Options:
  --version         show version of running script
  -h, --help        show this help page
  -u NAME, --user   user name to login with
                    [default: root]
  -p PASS, --pass   password for user
                    [default: password]
  --start 0-31      day number to start using. default is to use uptime of switch
  --stop 0-31       day number to end with
                    [default: 0]
  --debug           enable debugging verbosity

Limitations:
  Does not currently monitor backup CP

"""
from docopt import docopt
import paramiko
import sys, re, datetime, time
myVersion = '0.82'
import pyparsing

#import matplotlib.limage as mpimg
#TBD save as file
#TBD email out graphs
#TBD print high water mark line when known
#TBD find previous consequitive days and plot those
#Create tally counter enforcement for feedback on usage


def m_plot(plot_data, switch_info):
    import matplotlib.pyplot as mplot
    import numpy as np
    #
    # Extract dictionary data
    #dump_interval, p_name, mem_type, mem_unit, mem_list, vmem_list
    dump_interval = plot_data['dump_interval']
    p_name = plot_data['p_name']
    mem_type = plot_data['mem_type']
    mem_unit = plot_data['mem_unit']
    mem_list = plot_data['mem_list']
    vmem_list = plot_data.get('vmem_list', None)

    #
    # Return now for items we don't plot
    hush_items = 'dentry inode_cache proc_inode_cache buffer_head skbuff_head_cache vm_area_struct \
    Inactive Inactive(file) Buffers Cached Active Active(anon) AnonPages Inactive(anon) Active(file)'
    if p_name in hush_items: return

    #
    # matplot data points and graph if increasing
    # https://stackoverflow.com/questions/40529039/in-python-how-to-fit-linear-slope-to-a-graph-in-a-specified-range-of-x-values
    mid_point = (int(len(mem_list) / 2))
    min_gain = 4096
    # Find avg slope of graph with numpy
    x = np.arange (0, len(mem_list))
    #x = [x1 * 60 for x1 in range (0, len(mem_list))]
    y = list(map(float, mem_list))
    poly = np.polyfit (x, y, 1)
    #mplot.scatter (x, y)
    y_line = x * poly[0] + poly[1]
    slope = poly[0]
    ##print ('Slope', slope)
    #mplot.plot (x, y_line)
    #mplot.show ()
    #print ('Q:', len (list (set (mem_list))) / len (mem_list))
    # Change to checking on average slope of numbers
    if 0.5 < slope:
        upSlope = 1
    else:
        upSlope = 0
    # Check that avg. three points of data are all increasing
    #print('First:', mem_list[0], 'Middle:', mem_list[mid_point], 'Last:', mem_list[-1], 'for', str(p_name))
    memFirstAvg = float(mem_list[0]) + float(mem_list[1]) + float(mem_list[2]) / 3
    #print ('First:', mem_list[0], mem_list[1], mem_list[2], memFirstAvg)
    memMidAvg = float(mem_list[mid_point - 1]) + float(mem_list[mid_point]) + float(mem_list[mid_point + 1]) / 3
    #print ('Middle:', mem_list[mid_point - 1], mem_list[mid_point], mem_list[mid_point + 1], memMidAvg)
    memLastAvg = float(mem_list[-3]) + float(mem_list[-2]) + float(mem_list[-1]) / 3
    #print ('Last:', mem_list[-3], mem_list[-2], mem_list[-1], memLastAvg)
    if memFirstAvg < memLastAvg and memMidAvg < memLastAvg and memFirstAvg < memMidAvg:
        # Also check that 1/2 gain is close to 2/2 gain
        firsthalfdelta = int(memMidAvg) - int(memFirstAvg)
        secondhalfdelta = int(memLastAvg) - int(memMidAvg)
        deltagain = float(secondhalfdelta / firsthalfdelta)
        ##print('delta', deltagain)
        if deltagain < .1:
            point3check = 0
        else:
            point3check = 1
            # Print data points
    else:
        point3check = 0
   #Plot is all filters let is pass
    if point3check and upSlope:
        try:
            memoryGain = (round (float (mem_list[-1]) - float (mem_list[0]), 2))
            #print ('gain', memoryGain, '\n')
            if min_gain < memoryGain:
                # Add commas to values
                memoryGain = '{:,}'.format (round (float (mem_list[-1]) - float (mem_list[0]), 2))
                memoryGain = str (memoryGain) + ' ' + str (mem_unit)
            else:
                return
        except:
            print('Debug:-1', mem_list[-1])
            print('Debug: 0', mem_list[0], '\n\n')
            memoryGain = 'U/K'
        # Get switch dic values
        switch_ip = switch_info.get('IP', 'N/A')
        switch_type = switch_info.get('switchType', 'N/A')
        switch_ver = switch_info.get('switchVer', 'N/A')
        # Y label
        titleName = switch_ip + ', ' + switch_ver + ', ' + switch_type + '\n' + mem_type + ' memory increase for' + ' "' + p_name + '"'
        mplot.title(titleName)
        # X label
        dump_title = '@' + str (dump_interval) + ' min Interval' + ', Total gain ' + memoryGain
        mplot.xlabel (dump_title)
        #ax.yaxis.set_label_position("right")

       # mplot.ylabel('\nTotal gain ' + memoryGain, size='large')

        mplot.text(0, mem_list[0], mem_list[0])                        ;# First value
        mplot.text(len(mem_list) - 1, mem_list[-1], mem_list[-1])     ;# Last value
        #If virtual data was provided use this with two graphs
        print('Plot:', p_name, mem_list)
        if vmem_list:
            # Dash is virtual memory, need to print legend maybe...
            mplot.text(1, vmem_list[0], 'VSS')
            lines = mplot.plot(vmem_list)
            mplot.setp(lines, color='b', linestyle='--')
            lines = mplot.plot(mem_list)
            mplot.setp(lines, color='b')
            #Add in high water mark line, if value is known
            # if 'raslogd' in p_name:
            #     hwm = 11000
            #     mplot.text (1, hwm + 5, 'HWM')
            #     x = [hwm for x1 in range (0, len (mem_list))]
            #     lines = mplot.plot (x)
            #     mplot.setp (lines, color='r', linestyle='dotted')
            #Show plot
            mplot.show()


            # Save mng file for user
            #fig = mplot.figure()
            #mplot.savefig(p_name + '.png', dpi=72)

            #https://stackoverflow.com/questions/20597088/display-a-png-image-from-python-on-mint-15-linux
            #mpimg.imread(temp.png)
            #mplot.imshow(xxx)


        else:
            mplot.plot(mem_list)
            mplot.show()


def meminfo_process(dump_interval, massaged_data, switch_info):
    #
    # Process meminfo
    # Output of /proc/meminfo: 2018-02-08--00:05:00
    # =============================================
    # MemTotal:        3556548 kB
    # MemFree:         2616984 kB
    # Buffers:           10720 kB
    # Cached:           300176 kB
    # SwapCached:            0 kB
    # Active:           176988 kB
    # Inactive:         247796 kB
    regexp = re.compile('(\S+):\s+(\d+)\s+\w+', re.DOTALL)
    meminfo_all_list = regexp.findall(''.join(map(str, massaged_data)))
    # print(meminfo_all_list)
    userDictM = {}
    plot_data = {}
    plot_data['dump_interval'] = dump_interval
    minDataPoints = 9
    for p_name, p_size in meminfo_all_list:
        #print('Name:', p_name, p_size)
        if not p_name in userDictM:
            userDictM[p_name] = [float(p_size)]
        else:
            userDictM[p_name].append (float(p_size))
    # Plot lists
    plot_data['mem_type'] = 'Meminfo'
    plot_data['mem_unit'] = 'kB'
    for k in userDictM:
        if len(userDictM[k]) <= minDataPoints: continue
        ##print('Key', k, userDictM[k])
        plot_data['p_name'] = k
        plot_data['mem_list'] = userDictM[k]
        m_plot(plot_data, switch_info)


def slabinfo_process(dump_interval, massaged_data, switch_info):
    ## Slabinfo kernel process
    # Using Default value of 60 minutes to dump memory status
    #
    # Output of /bin/slabinfo (Top 20): 2018-02-02--00:05:00
    # =====================================================
    # Name                   Objects Objsize    Space Slabs/Part/Cpu  O/S O %Fr %Ef Flg
    # kmalloc-4096             12469    4096    71.9M     2196/421/0    7 3  19  11 A
    # buffer_head             195159      64    15.6M      3827/46/4   51 0   1  79 a
    # proc_inode_cache         33804     408    15.6M      1904/87/4   18 1   4  88 a ...
    regexp = re.compile('(\S+)\s+\d+\s+\d+\s+(\S+)M', re.DOTALL)
    slabinfo_all_list = regexp.findall(''.join(map(str, massaged_data)))
    userDictS = {}
    plot_data = {}
    plot_data['dump_interval'] = dump_interval
    minDataPoints = 9
    for p_name, p_size in slabinfo_all_list:
        #print('Name:', p_name, p_size)
        if not p_name in userDictS:
            userDictS[p_name] = [float(p_size)]
        else:
            userDictS[p_name].append(float(p_size))
    # Plot lists
    plot_data['mem_type'] = 'Slabinfo'
    plot_data['mem_unit'] = 'MB'
    for k in userDictS:
        if len(userDictS[k]) <= minDataPoints: continue
        ##print('Key', k, userDictS[k])
        plot_data['p_name'] = k
        plot_data['mem_list'] = userDictS[k]
        m_plot(plot_data, switch_info)


def procrank_process(dump_interval, massaged_data, switch_info):
    ##
    ## User space memory processing of procrank
    #
    # Output of /bin/procrank: 2018-02-02--00:05:01
    # ======================================================
    #   PID      Vss      Rss      Pss      Uss  cmdline
    #  1401     520K     520K      60K      36K  /sbin/oom_handler
    #  1049     468K     468K      82K      76K  /sbin/wdtd
    #  1357     708K     708K     114K      72K  /usr/sbin/crond
    #     1     676K     676K     125K     112K  init [3] ...
    #
    #
    ps_output = switch_info['ps']

    #
    regexp = re.compile('(\d+)\s+\w+\s+\w+\s+(\w+)\s+(\w+)\s+(\S+)', re.DOTALL)
    user_all_list = regexp.findall (''.join (map (str, massaged_data)))
    # print(user_all_list)

    #
    # ??? Check here for too many procs of one type???!

    # If I catch the data in order can I count on this being in order and avoid looping???
    userDictP = {}
    userDictV = {}
    plot_data = {}
    superDict = {}
    plot_data['dump_interval'] = dump_interval
    for pid, pss, uss, line in user_all_list:
        #
        # Look up superd daemon if we have not looked up before
        if ('superd' in line and ps_output is not ''):
            #2066: "['diagd0']"
            #print('### Finding buried service for', line, pid)
            # 2238    2238    2238 ?        00:00:01    msd0
            # reCalc = pid + '\s+\d+(.*\S+)\n'
            reCalc = pid + '\s+\d+\s+\d+\s+\S+\s+\S+\s+(\S+)'
            regexp = re.compile(reCalc)
            psName = regexp.findall(''.join(map(str, ps_output)))
            line = line + str(psName)
            superDict[int(pid)] = str(psName)
            print('### Finding buried service for', line, pid)
           # print('Super', superDict, str, str(psName))

        #else:
            ##print()
            #print('already found pid\n\n', 'pid', pid, 'super', superDict.keys())
            #line = line + superDict[int(pid)]
            #print('line', line)
            #exit()
        #print(superDict)


        pss = pss.strip ('K')
        uss = uss.strip ('K')
        #print(pid, pss, uss, line)
        userSpaceName = pid + '_' + line
        # print(userSpaceName)
        if userSpaceName not in userDictP:
            userDictP[userSpaceName] = [float(pss)]
        else:
            userDictP[userSpaceName].append (float(pss))
        if userSpaceName not in userDictV:
            userDictV[userSpaceName] = [float(uss)]
        else:
            userDictV[userSpaceName].append (float(uss))
    # Plot lists
    minDataPoints = 9
    plot_data['mem_type'] = 'PSS'
    plot_data['mem_unit'] = 'kB'
    for k in userDictP:
        if len(userDictP[k]) <= minDataPoints: continue
        if len(userDictV[k]) <= minDataPoints: continue
        ##print('KeyP', k, userDictP[k])
        ##print('KeyV', k, userDictV[k])
        plot_data['p_name'] = k
        plot_data['mem_list'] = userDictP[k]
        plot_data['vmem_list'] = userDictV[k]
        # Only checking for PSS leaks, VSS is only an add on for PSS with this method
        m_plot(plot_data, switch_info)


def fos_model(sin):
    sin_dict = {}
    sin_dict['12'] = '3900'
    sin_dict['27'] = '3250'
    sin_dict['32'] = '4100'
    sin_dict['34'] = '200e'
    sin_dict['42'] = '48K'
    sin_dict['44'] = '4900'
    sin_dict['46'] = '7500'
    sin_dict['55'] = '7600'
    sin_dict['58'] = '5000'
    sin_dict['62'] = 'DCX';  # Should update for DCX vs. DCX+ from core blade info
    sin_dict['64'] = '5300'
    sin_dict['66'] = '5100'
    sin_dict['67'] = 'BES'
    sin_dict['71'] = '300'
    sin_dict['76'] = '8000'
    sin_dict['77'] = 'Pluto'
    sin_dict['83'] = '7800'
    sin_dict['96'] = 'Callisto'
    sin_dict['109'] = '6510'
    sin_dict['118'] = '6505'
    sin_dict['120'] = 'DCX+'
    sin_dict['121'] = 'Pluto+'
    sin_dict['133'] = '6520'
    sin_dict['141'] = 'DCXXT'
    sin_dict['142'] = 'PlutoXT'
    sin_dict['148'] = '7840'
    sin_dict['162'] = 'G620'
    sin_dict['165'] = 'X6-4'
    sin_dict['166'] = 'X6-8'
    sin_dict['170'] = 'Chewbacca'
    sin_dict['171'] = 'AMP'
    sin_dict['173'] = 'Tyr'

    # Get just int decimal number and look up name
    sin = int(float(sin))
    return sin_dict.get(str(sin), sin)


def ver_val(run_ver):
    import hashlib, requests, os, socket, datetime
    userName = os.getlogin ()
    hostName = socket.gethostbyaddr (socket.gethostname ())[0]
    dateName = datetime.datetime.now ()
    if '/' in sys.argv[0]:
        tal_wrd = sys.argv[0].split('/')[-1].split('.')[0]
    else:
        tal_wrd = sys.argv[0].split('\\')[-1].split('.')[0]
    checkUrl = 'https://trapazoid.englab.brocade.com/ver/' + tal_wrd + '.sha'
    # Check that this is valid current version.
    hash = hashlib.sha1 (open (sys.argv[0], 'rb').read ()).hexdigest ()
    r = requests.get (checkUrl, verify=False)
    #r = requests.get ('https://docs.google.com/spreadsheets/d/1It7ov9IFPwn6Rr-s8zl5DaiYjA2QkKif7VnPJfuLRqc/edit?usp=sharing')
    check = (r.text).rstrip ()
    print (hash, check)
    if hash == check:
        print('### Running version:', myVersion, ' ###\n')
        #http://trapazoid.englab.brocade.com/cgi-bin/tallyPy.cgi?pyPlot%20daward%20myPC%202002212018
        # Post usage update
        params = {'Script': tal_wrd, 'User': userName, 'Host': hostName, 'Date': dateName}
        user_agent = r'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent, "Accept": "text/plain"}
        response = requests.post ('https://trapazoid.englab.brocade.com/cgi-bin/tallyPy.cgi', headers=headers, data=params, verify=False)
    else:
        #print ('\n#!# You are running a modified script, or a less than current one. Please try updating first #!#')
        user_input = input('\n#?# You are running a modified script, or a less than current one. Do you still want to continue? #?# ')
        print (check, 'Running version:', myVersion, '\n')
        if user_input not in 'yes':
            print('\n### Try downloading latest copy from: https://drive.google.com/drive/folders/1kB3hWezV_cLWBX13MoD9xBinbYKfK9Py ###\n')
            exit ()
    # Post usage once that is working..


def main(argv):
    # Safety and version checker
    # ver_val(myVersion)

    # Debug arg
    debug = arguments['--debug']

    #Parse user arguments
    #print ('Args', arguments)
    clientUser = arguments['--user']
    if arguments['--pass'] is None:
        clientPass = 'password'
    else:
        clientPass = arguments['--pass']
    clientIP_list = arguments['<IP>']
    # User need to be root for this
    #print('U', clientUser)
    #if clientUser is not 'root':
    #    print ('\n#!# User must be "root" for this script. Not ' + clientUser + ' #!#\n')
    #    exit()

    # Connect to client
    ssh = paramiko.SSHClient ()
    ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    #print(arguments)

    for clientIP in clientIP_list:
        switch_info = {}
        switch_info['IP'] = clientIP
        print('### Connecting to ' + clientIP + ' ###')
        ssh.connect(hostname=clientIP, username=clientUser, password=clientPass)
        stdin, stdout, stderr = ssh.exec_command('uptime')
        uptime = (''.join(map(str, stdout)))
        regexp = re.compile('(\d+) day')
        try:
            upDays = int(regexp.findall(uptime)[0])
        except:
            upDays = 0
        if 31 < upDays: upDays = 31     ;# Max of 31 days of history
        # See if days was user supplied
        if arguments['--start'] is not None:
            upDays = int(arguments['--start'])
        if int(arguments['--stop']) is not 0:
            stopDay = int(arguments['--stop']) - 1
        else:
            stopDay = 0
        print('### Collecting ' + str(upDays) + ' days of logs ###')
        #Start with oldest date and work toward most recent.
        corecmd = '/var/log/mstatdir/memorystatus'
        cmd = 'cat '
        loopCount = upDays
        while stopDay < loopCount:
            cmd = cmd + ' ' + corecmd + '.' + str (loopCount)
            loopCount -= 1
        #print(arguments)
        if int(arguments['--stop']) is 0:
            cmd = cmd + ' /var/log/mstatdir/memorystatus'
        print(cmd)
        ##cmd = 'cat ' + corecmd        ;#Practice with just todays data
        #statement = """sh -c 'grep thing file | grep thing2 | tail -1'"""
        #https://stackoverflow.com/questions/14643861/paramiko-channel-stucks-when-reading-large-ouput
        t1 = time.time()
        stdin, stdout, stderr = ssh.exec_command(cmd, bufsize=-1, timeout=None)
        baseline = (''.join(map(str, stdout)))
        #
        # Get info to decode superd info
        #Wedge_56: FID99:root > ps - ejH
        #2238    2238    2238 ?        00: 00:01    msd0
        if arguments['--start'] is None:
            stdin, stdout, stderr = ssh.exec_command('ps -ejH')
            psOutput = (''.join(map(str, stdout)))
            switch_info['ps'] = psOutput
        else:
            #If getting older data, don't lookup services
            switch_info['ps'] = ''

        #for line in baseline.split('\n'): print(line)

        # Get switch type and ver
        stdin, stdout, stderr = ssh.exec_command ('version')
        regexp = re.compile ('Fabric OS:\s+(\S+)')
        switch_info['switchVer'] = regexp.findall(''.join(map(str, stdout)))[0]

        stdin, stdout, stderr = ssh.exec_command ('switchshow')
        regexp = re.compile ('switchType:\s+(\S+)')
        sin = regexp.findall(''.join(map(str, stdout)))
        switch_info['switchType'] = fos_model(sin[0])

        ssh.close()
        t2 = time.time()
        timeDelta = (datetime.datetime.fromtimestamp(t2) - datetime.datetime.fromtimestamp(t1))
        print ('### Done collecting stats, closing connection to ' + clientIP + ' ###')

        # Parse data collection type into seperate lists. using Output of may miss latest hour findings, maybe...
        regexp = re.compile('Output of /bin/slabinfo \(Top 20.*?Output of', re.DOTALL)
        slabInfo = regexp.findall(baseline)
        regexp = re.compile('Output of /bin/procrank:.*?procrank_endrun', re.DOTALL)
        proCrank = regexp.findall(baseline)
        regexp = re.compile('Output of /proc/meminfo:.*?Output of', re.DOTALL)
        memInfo = regexp.findall(baseline)
        regexp = re.compile('Using Default value of (\d+) minutes to dump memory')
        dumpInterval = regexp.findall(baseline)[0]
        regexp = re.compile('slabinfo \(Top 20\): (\S+)')
        dateStamps = regexp.findall(baseline)
        dateStamps.sort()


        # Process meminfo
        meminfo_process(dumpInterval, memInfo, switch_info)

        # Get unique list of all services found
        slabinfo_process(dumpInterval, slabInfo, switch_info)

        # Procrank process
        procrank_process(dumpInterval, proCrank, switch_info)

        print ('\n### Finished with ' +  clientIP + ' ###\n')

    # End script
    print('\n### Script Finished ###\n')
    exit()


if __name__ == "__main__":
    arguments = docopt (__doc__, version = myVersion)
    main(sys.argv[1:])