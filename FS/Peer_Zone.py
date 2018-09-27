#!/usr/bin/env python3

""" This script will open a connection via ssh to switch and can issue multiple commands. SSH, by nature, only
allows one command to be run per connection.I haven't figured out how to "exit" after commands have been sent."""


# import telnetlib
# import getpass
import argparse
import csv
import sys
import time
import logging
import paramiko
import re
import threading
import select
# import time

#######################################################################################################################
#
#  Identify the path that a module resides in here
#
#######################################################################################################################
sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')
sys.path.append('/home/automation/APM')
# sys.path.append('/home/RunFromHere/logs')

#######################################################################################################################
#
#  Import user created Modules here
#
#######################################################################################################################
# import sw_matrix_tools
# import anturlar
# import liabhar
# import cofra

# from anturlar import SwitchInfo
import anturlar
# import cofra
# import Config_up_down_compare


#######################################################################################################################
#  list of switch types
#  --------------------
#  62  DCX
#  64  5300
#  66  5100
#  67  Encryption switch
#  70  5410 - embedded switch
#  71  300
#  72  5480 - embedded switch
#  73  5470 - embedded switch
#  75  M5424 - embedded switch
#  77  DCX-4S
#  83  7800
#  86  5450 - embedded switch
#  87  5460 - embedded switch
#  92  VA-40FC
#  109  6510
#  117  6547  - embedded switch
#  118  6505
#  120  DCX 8510-8
#  121  DCX 8510-4
#  124  5430  - embedded switch
#  125  5431
#  129  6548  - embedded switch
#  130  M6505  - embedded switch
#  133  6520 - odin
#  134  5432  - embedded switch
#
#  141  Yoda DCX
#  142  Yoda pluto
#  148  Skybolt
#
#  162   Wedge
#  165   X6-4 (Venator)
#  166   X6-8 (Allegience)
#  170   Chewbacca
#
#######################################################################################################################
# import anturlar

def parent_parser():
    pp = argparse.ArgumentParser(add_help=False)
    # pp.add_argument("--repeat", help="repeat repeat")
    # pp.add_argument("firmware", help="firmware verison 8.1.0_bldxx")
    pp.add_argument("ip", help="IP address of SUT")
    # pp.add_argument("user", help="username for SUT")
    pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
    pp.add_argument('email', type=str, help="email address")
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp


def parse_args():
    # verb_value = "99"
    parent_p = parent_parser()
    parser = argparse.ArgumentParser(description="PARSER", parents=[parent_p])
    # parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    # parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c', '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip', '--ipaddr', help="IP address of target switch")
    parser.add_argument('-cp', '--cmdprompt', help="switch is already at command prompt")
    parser.add_argument('-t', '--switchtype', help="switch type number - required with -cp")
    # parser.add_argument('-r', '--steps', type=int, help="Steps that will be executed")
    parser.add_argument('-i', '--iterations', type=int, default=1,
                        help="How many iterations will be run that will be executed")
    # parser.add_argument('-e_ip', '--edsim_ip', help="EDSIM IP")
    # parser.add_argument('-e_pid', '--edsim_pid', help="EDSIM PID")
    # parser.add_argument('-e_port', '--edsim_port', help="EDSIM Port number to be used")
    # parser.add_argument('-e_wwn', '--edsim_wwn', help="EDSIM WWN to be used")

    # parser.add_argument('-p', '--password', help="password")
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    # group.add_argument("-q", "--quiet", action="store_true")
    # parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    # parser.add_argument("ip", help="IP address of SUT")
    # parser.add_argument("user", help="username for SUT")

    args = parser.parse_args()
    # print(args)


    # if not args.chassis_name and not args.ipaddr:
    #     print("Chassis Name or IP address is required")
    #     sys.exit()
    #
    # if args.cmdprompt and not args.switchtype:
    #     print("To start at the command prompt the switch type is needed.")
    #     sys.exit()
    #
    # if not args.cmdprompt and args.switchtype:
    #     print('To start at the command prompt both switch type and command prompt is requried')
    #     sys.exit()
    # print("Connecting to EDSIM :  " + args.edsim_ip)
    # print("user             :  " + args.user)
    # verbose    = args.verbose

    return parser.parse_args()


uname = "admin"
pwd = "password"
timeout = 30

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SSHClient():

    def __init__(self, host, username, password):
        self.connection = self.connect(host, username, password)

    @staticmethod
    def connect(host, username, password):
        """
         Initiates an SSH Connection to the Host
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(host, username=username, password=password)
            logger.info("Connection Created (host = {}, username = {}, password = *****)".format(host, username))
        except ValueError:
            logger.error("Connection Failed")

        return ssh

    def execute(self, command):
        """
         Executes a command via SSH and returns results on StdOut
        """
        logger.debug('Executing command on std out:\n\t{}'.format(command.strip()))
        return self.connection.exec_command(command.strip())

    def close(self):
        self.connection.close()

class SSH:
    shell = None
    client = None
    transport = None

    # def __init__(self, host, username, password):
        # self.connection = self.connect(host, username, password)

    def __init__(self, host, username, password):
        print("Connecting to server on ip", str(host) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(host, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((host, 22))
        self.transport.connect(username=username, password=password)

        # starts the output checking thread
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def openShell(self):
        self.shell = self.client.invoke_shell()

    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                print(strdata, end = "")
                if(strdata.endswith("$ ")):
                    print("\n$ ", end = "")

def issue_command(transport, pause, command):
    chan = transport.open_session()
    chan.exec_command(command)

    buff_size = 1024
    stdout = ""
    stderr = ""

    while not chan.exit_status_ready():
        time.sleep(pause)
        if chan.recv_ready():
            stdout += chan.recv(buff_size)

        if chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size)

    exit_status = chan.recv_exit_status()
    # Need to gobble up any remaining output after program terminates...
    while chan.recv_ready():
        stdout += chan.recv(buff_size)

    while chan.recv_stderr_ready():
        stderr += chan.recv_stderr(buff_size)

    return exit_status, stdout, stderr

def check_ssh(ip, user, pwd):
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=user, password=pwd)
        return True
    except Exception as e:
        print(e)
        return False


def console_info_from_ip(ipaddr):
    """

    """
    switchmatrix = '/home/runfromhere/ini/SwitchMatrix.csv'
    # switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return False

    for line in csv_file:
        ip_address_from_file = (line['IP Address'])

        if ip_address_from_file == ipaddr:
            swtch_name = (line['Chassisname'])

        else:
            print("\r\n")

    return swtch_name


def get_user_and_pass(chassis_name):
    """

    """
    switchmatrix = '/home/runfromhere/ini/SwitchMatrix.csv'
    # switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return False

    u_and_p = []
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            u = (line['Username'])
            p = (line['Password'])
            u_and_p += [u]
            u_and_p += [p]

    return u_and_p


def get_ip_from_file(chassis_name):
    """

    """
    switchmatrix = '/home/runfromhere/ini/SwitchMatrix.csv'
    # switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return (False)

    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            ip = (line['IP Address'])

    return pa.ipaddr


def get_peer_zone_info(result):
    effective = re.findall('(Effective configuration:[ ,:\()_A-Za-z0-9\s\t\n]+Cfg)', result, flags=re.S | re.M)
    effective = str(effective)
    # print(effective)
    peer_zone = re.findall(r'(peer_test\\t\\n[ ,:\\()_A-Za-z0-9\\s\\t\\n]+Cfg)', effective)
    if  not peer_zone:
        print("EFFECTIVE CONFIGURATION NOT FOUND")
        # zone_reset()
        ssh.close()
        sys.exit(0)
    peer_zone = str(peer_zone)
    print(peer_zone)
    return peer_zone


def lscreate(fid, ip):
    sync_output = []
    connect = check_ssh(ip, uname, pwd)
    if connect:
        print("Inside lscreate")
        cmd = "lscfg --create %s -force" % fid
        print(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        for line in stdout:
            # print line.strip('\n')
            sync_output.append(line.strip('\n'))
            # print(sync_output)
        successMsg = "Logical Switch with FID (%s) has been successfully created." % (fid)
        if successMsg in sync_output:
            print("Logical switch %s is created successfully" % fid)
            ssh.close()
            return True
        else:
            fail_message = "Attempt to create switch %s failed" % fid
            if fail_message in sync_output:
                print("Logical switch %s is not created" % fid)
            ssh.close()
            return False

    else:
        print("No connection")
        return False


def lsdelete(fid):
    sync_output = []
    connect = check_ssh(ip, uname, pwd)
    if (connect == True):
        print("Inside lsdelete")
        cmd = "lscfg --delete %s -force" % fid
        stdin, stdout, stderr = ssh.exec_command(cmd)
        for line in stdout:
            print(line.strip('\n'))
            sync_output.append(line.strip('\n'))
            if "Switch successfully deleted." in sync_output:
                print("Switch %s successfully deleted" % fid)
                ssh.close()
                return True

            else:
                print("Switch %s not deleted" % fid)
                ssh.close()
                return False

    else:
        print("No connection")
        return False


def director(ip):
    connect = check_ssh(ip, uname, pwd)
    if connect:
        print("CONNECTED")
        sync_output = []
        # cmd = "lscfg --create %s -force" % fid
        cmd = "hashow"
        print(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        for line in stdout:
            print(line.strip('\n'))
            sync_output.append(line.strip('\n'))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # print(sync_output)
        # successMsg = "hashow: Not supported on this platform."
        if "hashow: Not supported on this platform" in sync_output:
            # print("Logical switch %s is created successfully" % fid)
            # print("This is a Pizza Box")
            return False
            ssh.close()
        else:
            # print("Logical switch %s is not created" % fid)
            # print("This is a director")
            return True
            ssh.close()


def vf_capable(ip):
    # ssh = SSHClient(creds["host"], creds["user"], creds["pass"])
    ssh = SSHClient(ip, uname, pwd)
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("lscfg --show")
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("ipaddrshow")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("fosconfig --show")

    ssh_stdout=ssh_stdout.readlines()
    logger.info("Results:\n\tstd-in = {}\n\tstd-out = {}\n\tstd-err = {}".format(
        ssh_stdin, ssh_stdout, ssh_stderr))
    logger.info ("ssh succcessful. Closing connection")
    ssh.close()
    for line in ssh_stdout:
        if line != '':
            output = (line.strip('\n'))
            logger.info('   printing output')
            print(output)
        else:
            print('No information read from vf_capable function')
    if "not supported" or "requires" in line:
        print ("VF is not enabled and/or not supported on this switch")
        print("Exiting")
        sys.exit(0)
    else:
        print('We can move on now')
        #sync_output.append(line.strip('\n'))

    sys.exit(0)
    # connect = check_ssh(ip, uname, pwd)
    if connect:
        print(ssh_stdout)
    for line in ssh_stdout:
        logger.info ('(((((((((((LINE)))))))))))))))')
        print(line)

        # console_op = ("".join(stdout.readlines()))
        # for line in ssh_stdin:
        #     print(line)
        ssh.close()
        sys.exit(0)
            # # print(line.strip('\n'))
            # sync_output.append(line.strip('\n'))
            # print(sync_output)
            # novf = "lscfg: requires VF to be supported."
            # if novf in sync_output:
            #     ssh.close()
            #     return False
            # else:
            #     ssh.close()
    return True


def vf_capable_transport(ip):
    ssh = paramiko.SSHClient()
    # ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(host, port=22, username=username, password=password, timeout=3,)
    ssh.connect(ip, uname, pwd, timeout=3)
    transport = ssh.get_transport()
    pause = 1

    resp1 = issue_command(transport, pause, "lscfg --show")

# def cfgsave():
#     ssh = SSHClient.execute()
#     stdin, stdout, stderr = ssh('cfgsave')
#     stdin.write('y')
#     stdin.write('\n')
#     stdin.flush()
#     result = stdout.read().decode('ascii').strip('\n')
#     print(result)


def main():

    pa = parse_args()
    print(pa)
    # print(pa.chassis_name)
    # print(pa.ipaddr)
    # print(pa.quiet)
    # print(pa.verbose)
    # print(pa.firmware)
    # print(pa.cmdprompt)
    print("@" * 40)
    # sys.exit(0)

    ###################################################################################################################
    ###################################################################################################################
    #
    # if user enter ip address then get the chassisname from the SwitchMatrix file
    # then get the info from the SwitchMatrix file using the Chassis Name
    #
    # if pa.ipaddr:
    #     print("do IP steps")
    #     pa.chassis_name = console_info_from_ip(pa.ipaddr)
    # ip = pa.ip

    ssh = SSHClient(pa.ip, uname, pwd) # SSHClient() is a class

    def cfgadd(cfg, zone):
        stdin, stdout, stderr = ssh.execute('cfgadd %s,%s' % (cfg, zone))
        result = stdout.read().decode('utf-8')
        print(result)

    def cfgenable(cfg):
        stdin, stdout, stderr = ssh.execute('cfgenable %s' % cfg)
        stdin.write('y')
        stdin.write('\n')
        stdin.flush()
        result = stdout.read().decode('utf-8')
        print(result)

    def cfgremove(cfg, zone):
        stdin, stdout, stderr = ssh.execute('cfgremove %s,%s' % (cfg, zone))
        result = stdout.read().decode('utf-8')
        print(result)

    def cfgsave():
        stdin, stdout, stderr = ssh.execute('cfgsave')
        stdin.write('y')
        stdin.write('\n')
        stdin.flush()
        result = stdout.read().decode('utf-8')
        # result = stdout.read().decode('ascii').strip('\n')
        print(result)

    def zonedelete(zone):
        stdin, stdout, stderr = ssh.execute('zonedelete %s' % zone)
        stdin.flush()
        # stdin, stdout, stderr = ssh.execute('cfgsave')
        # stdin.write('y')
        # stdin.write('\n')
        # stdin.flush()
        result = stdout.readlines()
        for line in result:
            print(line.strip())

    def zone_reset():
        zonedelete('peer_test')
        cfgremove('"FID_10"', '"peer_test"')
        cfgenable("FID_10")

    deadbeef = ['de:ad:be:ef:de:ad:be:ef', 'de:ad:de:ad:be:ef:be:ef']
    dead1 = ['de:ad:be:ef:00:00:00:01', 'de:ad:be:ef:00:00:00:02', 'de:ad:be:ef:00:00:00:03',
             'de:ad:be:ef:00:00:00:04', 'de:ad:be:ef:00:00:00:05']
    dead2 = ['de:ad:be:ef:00:00:00:06', 'de:ad:be:ef:00:00:00:07', 'de:ad:be:ef:00:00:00:08',
             'de:ad:be:ef:00:00:00:09', 'de:ad:be:ef:00:00:00:10']
    di = "33,10;33,11;33,12"
    di1 = "33,13;33,14;33,15"
    di2 = "33,16;33,17;33,18"

    logger.info("Test Case Step 1.1")
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "peer_test" -principal "00:02:00:00:00:01:00:01;%s;%s"'\
                                        % (deadbeef[0], deadbeef[1]))
    result1 = stdout.read().decode('utf-8')
    print(result1)
    if 'Error: Invalid zone member' in result1:
        print("Invalid Zone Member = PASSED")
    else:
        print('Script failed at adding invalid zone member')
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 1.3")
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "alias_test" -member "00:02:00:00:00:01:00:01;%s;%s"'\
                                        %(deadbeef[0], deadbeef[1]))
    result2 = stdout.read().decode('utf-8')
    print(result2)
    if 'Error:' or 'Usage:' in result2:
        print("No Principle member declared = PASSED")
    else:
        print('Script failed at adding member without having a "principal" declared ')
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 1.5")
    stdin, stdout, stderr = ssh.execute('alicreate "peer_member", "00:02:00:00:00:01:00:01"')
    result3 = stdout.read().decode('utf-8')
    print(result3)
    if 'Error:' or "Usage:'" in result3:
        print("alicreate using invalid member = PASSED")
    else:
        print('Script failed at adding member without having a "principal" declared ')
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 2.1")
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "peer_test" -principal "%s;%s"'\
                                        % (deadbeef[0], deadbeef[1]))
    check = stdout.readlines()
    logger.info("ERROR_CHECK")
    print(check)
    if check:
        print("zone create failed when it should've PASSED")
        ssh.close()
        sys.exit(0)
    else:
        cfgadd('"FID_10"', '"peer_test"')
        cfgenable("FID_10")
        cfgsave()

    logger.info("Test Case Step 2.2")
    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    result5 = stdout.read().decode('utf-8')
    peer_test_zone = get_peer_zone_info(result5)

    if not peer_test_zone:
        print("ZONE CONFIGURATION NOT FOUND")
        ssh.close()
        sys.exit(0)
    peer_test_zone = str(peer_test_zone)
    prop_member = 'Property Member: 00:02:00:00:00:03:00:02'
    if prop_member in peer_test_zone:
        print("Property Member Check Passed")
    else:
        print("PROPERTY MEMBER NOT FOUND")

    # principal_member = re.findall('Principal Member\(s\):\\\\[a-z:]{0,23}\\\\[a-z:]{0,23}', peer_test_zone)

    if deadbeef[0] and deadbeef[1] in peer_test_zone:
        print("Step 2.1 Passed")
    else:
        print('Script failed at step 2.1 ')
        # zone_reset()
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 3.1")
    stdin, stdout, stderr = ssh.execute('zoneadd --peerzone "peer_test" -principal %s' % (dead1[0]))
    check = stdout.readlines()
    logger.info("ERROR_CHECK")
    print(check)
    if check:
        print("zone create failed when it should've PASSED")
        zone_reset()
        ssh.close()
        sys.exit(0)
    else:
        cfgsave()
        cfgenable("FID_10")

    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    result7 = stdout.read().decode('utf-8')

    if ' zone:\tpeer_test' and 'Property Member: 00:02:00:00:00:03:00:03' in result7:
        print("Step 3.1 Passed")
    else:
        print('Script failed at step 3.1 ')
        # zone_reset()
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 4.1")
    stdin, stdout, stderr = ssh.execute('zoneadd --peerzone "peer_test" -members "{a};{b};{c}"'
                                        .format(a=(dead1[1]), b=(dead1[2]), c=(dead1[3])))
    check = stdout.readlines()
    logger.info("ERROR_CHECK")
    print(check)
    if check:
        print("zone add failed when it should've PASSED")
        zone_reset()
        ssh.close()
        sys.exit(0)
    else:
        cfgsave()
        cfgenable("FID_10")

    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    result9 = stdout.read().decode('utf-8')
    peer_zone = get_peer_zone_info(result9)
    if not peer_zone:
        print("peer_zone CONFIGURATION NOT FOUND")
        zone_reset()
        ssh.close()
        sys.exit(0)
    peer_zone = str(peer_zone)
    print(peer_zone)
    substring = 'Property Member: 00:02:00:00:00:03:00:03'

    a = peer_zone.find(substring)
    b = peer_zone.find(deadbeef[0])
    c = peer_zone.find(deadbeef[1])
    d = peer_zone.find(dead1[0])
    e = peer_zone.find(dead1[1])
    f = peer_zone.find(dead1[2])
    g = peer_zone.find(dead1[3])
    members = [a, b, c, d, e, f, g]
    for i in members:
        if i is -1:
            print(i)
            zone_reset()
            ssh.close()
            sys.exit(0)
    else:
        print('STEP 4 PASSED')

    logger.info("Test Cases for Step 6")
    stdin, stdout, stderr = ssh.execute('zoneadd "peer_test" -member "00:02:00:00:00:01:00:01;%s;%s"'
                                        % (deadbeef[0], deadbeef[1]))
    result = stdout.read().decode('ascii').strip('\n')
    print(result)
    if 'Error:' or "Usage:'" in result2:
        print("No Principle member declared = PASSED")
    else:
        print('Script failed at Step 6')
        ssh.close()
        sys.exit(0)

    stdin, stdout, stderr = ssh.execute('zoneobjectreplace %s be:ef:be:ef:de:ad:de:ad' % deadbeef[0])
    result = stdout.read().decode('utf-8')
    print(result)
    if 'error:' in result:
        print("Step 6.3, Zone Object Replace = Failed")
    else:
        print("Step 6.3, Zone Object Replace PASSED")

    stdin, stdout, stderr = ssh.execute('zoneobjectreplace be:ef:be:ef:de:ad:de:ad %s' % deadbeef[0])
    result = stdout.read().decode('utf-8')
    if 'error:' in result:
        print("Step 6.3, Zone Object put back = Failed")
    else:
        print("Step 6.3, Zone Object put back PASSED")

    stdin, stdout, stderr = ssh.execute('zoneobjectreplace 00:02:00:00:00:03:00:03 00:02:00:00:00:04:00:04')
    result = stdout.read().decode('utf-8')
    print(result)
    if 'error:' in result:
        print('Step 6.4, Principle member cannot be modified = PASSED')
    else:
        print('Step 6.4, Script failed at Step 6.3')
        zone_reset()
        ssh.close()
        sys.exit(0)

    logger.info("Test Cases for Step 8")  # Step 7 is executed throughout this script to verify all other tests

    stdin, stdout, stderr = ssh.execute('alicreate "ali_wwn", "%s;%s"' % (deadbeef[0], deadbeef[1]))
    # result = stdout.read().decode('utf-8')
    # print(result)
    stdin, stdout, stderr = ssh.execute('alicreate "ali_wwn1", "%s;%s"' % (dead1[0], dead1[1]))
    stdin, stdout, stderr = ssh.execute('alicreate "ali_di", "%s"' % di)
    stdin, stdout, stderr = ssh.execute('alicreate "ali_di1", "%s"' % di1)
    stdin, stdout, stderr = ssh.execute('alicreate "ali_wwn_di", "%s;%s"' % (deadbeef[0], di))
    cfgsave()
    logger.info("Test Cases for Step 9")
    stdin, stdout, stderr = ssh.execute('zoneadd --peerzone peer_test -p "ali_wwn_di"')
    result = stdout.read().decode('utf-8')
    # print(result)
    stdin, stdout, stderr = ssh.execute('zoneadd --peerzone peer_test -m "ali_wwn_di"')
    result_1 = stdout.read().decode('utf-8')
    # print(result_1)
    substring = 'Error: Members of alias "ali_wwn_di" can either be WWN or D,I: alias having mixed type of'
    if substring in result and result_1:
        print('Step 9, Mixed Alias Members in peer zone member = PASSED')
    else:
        print('Step 9, Script failed at Mixed Alias Members in peer zone member')
        zone_reset()
        ssh.close()
        sys.exit(0)
    logger.info("Test Cases for Step 10")
    stdin, stdout, stderr = ssh.execute('zoneadd --peerzone peer_test -m "ali_wwn"')
    result = stdout.read().decode('utf-8')
    # print(result)
    stdin, stdout, stderr = ssh.execute('zoneadd --peerzone peer_test -p "ali_wwn"')
    result1 = stdout.read().decode('utf-8')
    # print(result1)
    substring = 'Error: Duplicates member exists'
    if substring in result and result_1:
        print('Step 10, Duplicate Members in peer zone not allowed = PASSED')
    else:
        print('Step 10, Duplicate Members in peer zone not allowed = FAILED')
        zone_reset()
        ssh.close()
        sys.exit(0)
    zone_reset()

    logger.info('Test Cases for Step 11')
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "peer_test" -p "ali_wwn;11:22:33:44:55:66:77:88"' 
                                        '-m "ali_wwn1;12:34:56:78:09:10:11:12"')
    cfgsave()
    result = stdout.read().decode('utf-8')
    print(result)
    if 'error:' in result:
        print('Step 11.2 and 11.4, Alias Mix = FAILED')
        zone_reset()
        ssh.close()
        sys.exit(0)
    else:
        print('Step 11.2 and 11.4, Alias Mix = PASSED')
    zone_reset()
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "peer_test" -p "ali_di;30,01;30,02" -m'
                                        ' "ali_di1;30,3;30,4"')
    cfgsave()
    result = stdout.read().decode('utf-8')
    print(result)
    if 'error:' in result:
        print('Step 11.1 and 11.3, Alias Mix = FAILED')
        zone_reset()
        ssh.close()
        sys.exit(0)
    else:
        print('Step 11.1 and 11.3, Alias Mix = PASSED')
    cfgadd('FID_10', 'peer_test')
    # result = stdout.read().decode('utf-8')
    # print(result)
    cfgenable('FID_10')
    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    result = stdout.read().decode('utf-8')
    check = get_peer_zone_info(result)

    logger.info('Test Cases for Step 13 and 14')
    substring = 'Property Member: 00:02:00:00:00:02:03:05'
    if substring in check:
        print('Step 12 & 13, Variable Data Type = PASSED')
    else:
        print('Step 12 & 13, Variable Data Type = FAILED')
        zone_reset()
        ssh.close()
        sys.exit(0)
    logger.info('Test Cases for Steps 14-16 and 18 are verified in other areas in the script')
    zone_reset()

    stdin, stdout, stderr = ssh.execute('alidelete  ali_wwn') # , "%s;%s"' % (deadbeef[0], deadbeef[1]))
    result = stdout.read().decode('utf-8')
    print(result)
    stdin, stdout, stderr = ssh.execute('alidelete  ali_wwn1') # , "%s;%s"' % (dead1[0], dead1[1]))
    stdin, stdout, stderr = ssh.execute('alidelete  ali_di') # , "%s"' % di)
    stdin, stdout, stderr = ssh.execute('alidelete  ali_di1') #, "%s"' % di1)
    stdin, stdout, stderr = ssh.execute('alidelete  ali_wwn_di')
    stdin, stdout, stderr = ssh.execute('alishow')
    result = stdout.read().decode('utf-8')
    print('END OF PEER ZONE SCRIPT REMEMBER TO RUN TRAFFIC AND CHECK RSCNs')
    print(result)
    cfgsave()
    # zone_reset()
    ssh.close()
    sys.exit(0)



    #################################### Sample Text ###############################################################
    # ssh = SSHClient(ip, uname, pwd)
    # connection = SSH(ip, uname, pwd)
    # connection.openShell()
    # THE BELOW WILL OPEN AN INTERACTIVE SHELL. DON'T KNOW HOW TO CLOSE IT???
    # while True:
    #     command = input('$ ')
    #     if command.startswith(" "):
    #         command = command[1:]
    #     connection.sendShell(command)
    # stdin, stdout, stderr = ssh.execute('switchshow')
    # stdin, stdout, stderr = ssh.execute('dsim --devshow')
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi rpa %s "e100"' % pa.edsim_pid)
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi gpat %s %s %s' % (pa.edsim_port, pa.edsim_pid, pa.edsim_wwn))
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi dpa %s %s %s' % (pa.edsim_port, pa.edsim_pid, pa.edsim_wwn))
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi gpat %s %s %s' % (pa.edsim_port, pa.edsim_pid, pa.edsim_wwn))
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi rpa %s "F100"' % pa.edsim_pid)
    #
    # search = re.search('(?:Virtual Fabric:\\t\\t\\t)([a-z]{0,8})', fosconfig, re.M | re.I)
    # search = re.search('(?:Virtual Fabric:\D{0,6})([a-z]{0,8})', fosconfig, re.M | re.I)
    # logger.info("THIS IS SEARCH %s" % search)
    # print('THIS IS THE RESULT OF RE.SEARCH: %s ' % search.group(0))
    # a = search.group(0)
    # b = search.group(1)
    #
    #
    # for line in foscfg:
    #     if line != '':
    #         output = (line.strip('\n'))
    #         logger.info('   printing output')
    #         print(output)
    #     else:
    #         print('No information read from vf_capable function')
    # print(output)
    # search = re.search('(requires)', output, re.M | re.I)
    # logger.info(search)
    # if search is None:
    #     print("\n\n\nVF not enabled on this switch\n\n\n")
    #     return (False)
    # else:
    #     print("\n\n\nVF is enabled on this switch\n\n\n")
    #     return (True)
    # logger.info ("ssh succcessful. Closing connection")
    # ssh.close()
    # Example on how to print Human readable results:
    # print('\n\n'+ '='*20)
    # print("Switch Name :  %s" % initial_checks[0])
    # print("IP address :  %s" % initial_checks[1])
    # print("Chassis :  %s" % initial_checks[2])
    # print("VF enabled :  %s" % initial_checks[3])
    # print("FCR enabled :  %s" % initial_checks[4])
    # print("Base configured :  %s" % initial_checks[5])
    # print('='*20 + '\n\n')
    # sys.exit(0)



if __name__ == "__main__":
    main()
