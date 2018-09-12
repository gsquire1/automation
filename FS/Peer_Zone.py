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
        result = stdout.read().decode('ascii').strip('\n')
        print(result)

    def cfgenable(cfg):
        stdin, stdout, stderr = ssh.execute('cfgenable %s' % cfg)
        stdin.write('y')
        stdin.write('\n')
        stdin.flush()
        result = stdout.read().decode('ascii').strip('\n')
        print(result)

    def cfgremove(cfg, zone):
        stdin, stdout, stderr = ssh.execute('cfgremove %s,%s' % (cfg, zone))
        result = stdout.read().decode('ascii').strip('\n')
        print(result)

    def cfgsave():
        stdin, stdout, stderr = ssh.execute('cfgsave')
        stdin.write('y')
        stdin.write('\n')
        stdin.flush()
        result = stdout.read().decode('ascii').strip('\n')
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
    di = "33,10;33,11;33,12"
    di1 = "33,13;33,14;33,15"




    logger.info("Test Case Step 1.1")
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "peer_test" -principal "00:02:00:00:00:01:00:01;%s;%s"'\
                                        % (deadbeef[0], deadbeef[1]))
    result1 = stdout.read().decode('ascii').strip('\n')
    print(result1)
    if 'Error: Invalid zone member' in result1:
        print("Invalid Zone Member = PASSED")
    else:
        print('Script failed at adding invalid zone member')
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 1.3")
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "peer_test" -member "00:02:00:00:00:01:00:01;%s;%s"'\
                                        %(deadbeef[0], deadbeef[1]))
    result2 = stdout.read().decode('ascii').strip('\n')
    print(type(result2))
    print(result2)
    if 'Error:' or 'Usage:' in result2:
        print("No Principle member declared = PASSED")
    else:
        print('Script failed at adding member without having a "principal" declared ')
        ssh.close()
        sys.exit(0)

    logger.info("Test Case Step 1.5")
    stdin, stdout, stderr = ssh.execute('alicreate "peer_member", "00:02:00:00:00:01:00:01"')
    result3 = stdout.read().decode('ascii').strip('\n')
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

    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    result5 = stdout.read().decode('utf-8')#.strip('\n')
    # result5 = stdout.readlines()
    print(result5)
    effective = re.findall('(Effective configuration:[ ,:\()_A-Za-z0-9\s\t\n]+Cfg)', result5, flags=re.S | re.M)
    if effective:
        print(type(effective))
        effective = str(effective)
        print(effective)
    else:
        print("EFFECTIVE CONFIGURATION NOT FOUND")
        ssh.close()
        sys.exit(0)
    # print(type(effective))
    print(effective)
    zone = re.findall(r'(peer_test\\t\\n[ ,:\\()_A-Za-z0-9\\s\\t\\n]+Cfg)', effective)
    if not zone:
        print("ZONE CONFIGURATION NOT FOUND")
        ssh.close()
        sys.exit(0)
    # logger.info("PRINT ZONE AND ZONE TYPE")
    zone = str(zone)
    a = zone.replace('\\t', '')
    a = a.replace('\\n', '')
    a = a.replace('\\\\', '')
    # print("ZONE_REPLACE")
    # print(a)
    prop_member = re.findall('(Property Member: 00:02:00:00:00:03:00:02)', zone)
    if not prop_member:
        print("PROPERTY MEMBER NOT FOUND")
        zone_reset()
        ssh.close()
        sys.exit(0)
    print("PROPERTY MEMBER")
    print(prop_member)
    principal_member = re.findall('Principal Member\(s\):\\\\[a-z:]{0,23}\\\\[a-z:]{0,23}', a)
    if not principal_member:
        print("PRINCIPAL MEMBER NOT FOUND")
        zone_reset()
        ssh.close()
        sys.exit(0)
    # print("PRINCIPAl MEMBER")
    # print(type(principal_member))
    # print(principal_member)
    b = str(principal_member)

    if deadbeef[0] and (deadbeef[1]) in b:
        print("Step 2.1 Passed")
    else:
        print('Script failed at step 2.1 ')
        zone_reset()
        ssh.close()
        sys.exit(0)
    # zone_reset()
    # ssh.close()
    # sys.exit(0)

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
    print(result7)
    zone_reset()
    ssh.close()
    sys.exit(0)

    if ' zone:\tpeer_test' and 'Property Member: 00:02:00:00:00:03:00:03' in result7:
        print("Step 3.1 Passed")
    else:
        print('Script failed at step 3.1 ')
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
        ssh.close()
        sys.exit(0)
    else:
        cfgsave()

    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    # result9 = stdout.read().decode('ascii')# .strip('\n')
    # print("RESULT9_RESULT9")
    result9 = stdout.readlines()#.decode('ascii')# .strip('\n')
    # print(result9)
    if ' zone:\tpeer_test\t\n' and 'Property Member: 00:02:00:00:00:03:00:03'\
        and 'Principal Member(s):\n'\
        and '\t\t%s; %s; \n' % ((deadbeef[0]), (deadbeef[1]))\
        and '\t\tde:ad:be:ef:00:00:00:01\n'\
        and '   Peer Member(s):\n'\
        and '\t\tde:ad:be:ef:00:00:00:02; de:ad:be:ef:00:00:00:03; \n'\
        and '\t\tde:ad:be:ef:00:00:00:04\n' in result9:
        print("Step 4.1 Passed")
    else:
        print("Step 4.1 Failed")
        ssh.close()
        sys.exit()
    ssh.close()
    sys.exit(0)

    logger.info("Test Cases for Step 6")
    stdin, stdout, stderr = ssh.execute('zoneadd "peer_test" -member "00:02:00:00:00:01:00:01;%s;%s"' \
                                        % (deadbeef[0], deadbeef[1]))
    result = stdout.read().decode('ascii').strip('\n')
    print(result)
    if 'Error:' or "Usage:'" in result2:
        print("No Principle member declared = PASSED")
    else:
        print('Script failed at Step 6')
        ssh.close()
        sys.exit(0)

    stdin, stdout, stderr = ssh.execute('zoneobjectreplace 00:02:00:00:00:03:00:03 00:02:00:00:00:04:00:04')
    result = stdout.read().decode('ascii')
    print(result)
    if 'error:' in result:
        print("Principle member cannot be modified = PASSED")
    else:
        print('Script failed at Step 6')
        ssh.close()
        sys.exit(0)
    zonedelete('peer_test')

    # logger.info("Test Cases for Step 8") # Step 7 is executed throughout this script to verify all other tests
    # stdin, stdout, stderr = ssh.execute('alicreate "ali_wwn", "%s;%s"' % (deadbeef[0], deadbeef[1]))
    # stdin, stdout, stderr = ssh.execute('alicreate "ali_wwn1", "%s;%s"' % (dead1[0], dead1[1]))
    # stdin, stdout, stderr = ssh.execute('alicreate "ali_di", "%s"' % di)
    # stdin, stdout, stderr = ssh.execute('alicreate "ali_di1", "%s"' % di1)
    # cfgsave()
    # # ssh.close()
    # # sys.exit()
    # stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "ali_test" -principal "ali_di" -members "ali_di1"')
    # stdin, stdout, stderr = ssh.execute('cfgadd "FID_10", "ali_test"')
    # cfgenable("FID_10")
    stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    # result10 = stdout.readlines()  # .decode('ascii')# .strip('\n')
    result10 = stdout.read().decode('utf-8').strip('\n')
    print("RESULT10_RESULT10")
    print(result10)
    print('AAAAAAAAAAAAAAAAAAAA')
    a = result10.index(' zone:\tali_test\t\n')
    print(a)
    if (' zone:\tali_test\t\n' and '   Property Member: 00:02:00:00:00:02:00:03\n' and '   Created by: User\n' in result10):
         # and '   Principal Member(s):\n' in result10:
         # and '\t\t33,10\n'
         # and '\t\t33,11\n'
         # and '\t\t33,12\n')
    #     and '   Peer Member(s):\n'\
    #     and '\t\t33,13\n'\
    #     and '\t\t33,14\n' \
    #     and '\t\t33,15\n' in result10:
        print("Principal = D,I and Members = D,I Passed")
    else:
        print("Principal = D,I and Members = D,I Failed")
        ssh.close()
        sys.exit()
    ssh.close()
    sys.exit()
    stdin, stdout, stderr = ssh.execute('zonecreate --peerzone "ali_test1" -principal "ali_di" -members\
     "33,13;33,14;33,15"')
    stdin, stdout, stderr = ssh.execute('cfgadd "FID_10", "ali_test1"')
    cfgenable("FID_10")

    # for line in result:
    #     if 'Error:' or "Usage:'" in line:
    #         print("zone create failed when it should've PASSED")
    #         ssh.close()
    #         sys.exit(0)
    #     else:
    #         pass
    # # stdin, stdout, stderr = ssh.execute('cfgshow')
    # stdin, stdout, stderr = ssh.execute('zoneshow --peerzone all')
    # result = stdout.readlines()
    # sync_output = []
    # for line in result:
    #     print(line)
    #     sync_output.append(result)
    #     # sync_output.append(line.strip('\t\n'))
    # logger.info("PRINTING SYNC OUTPUT")
    # print(sync_output)
    ssh.close()
    sys.exit()
    # if ' zone:\tpeer_test' and 'de:ad:be:ef:de:ad:be:ef; de:ad:de:ad:be:ef:be:ef; 'and '10:00:00:04:05:06:07:08' \
    #         in sync_output:
    #     print("YES")
    # else:
    #     print("NO")
    # stdin, stdout, stderr = ssh.execute('zonedelete peer_test')
    # stdin.flush()
    # stdin, stdout, stderr = ssh.execute('cfgsave')
    # stdin.write('y')
    # stdin.write('\n')
    # stdin.flush()
    # result = stdout.readlines()
    # for line in result:
    #     print(line.strip())


    # for line in result4:
        # print(line.strip('\n'))
        # sync_output.append(line.strip())
        #sync_output.append(line.strip('\n'))
        # print(sync_output)
        # if "Configuration change successful." in sync_output:
        #     print("ports moved to newfid %s" % fid)
        # else:
        #     # print(sync_output)
        #     print("ports aren't moved")
    # for line in result4:
    #     print(line.strip())
        # if 'peer_test' in line:
        #     print("YES")
        # else:
        #     print('NO')

    # stdin, stdout, stderr = ssh.execute('cfgtransabort')
    # checks = stdout.readlines()
    # for line in checks:
    #     print(line)

    #     # logger.info("THIS IS ZONECREATE CMD LINE OUTPUT:  \n   %s" % line)
    #     # print(line.strip())
    #     if 'Error: Invalid zone member' in line:
    #         print("Invalid Zone Member = PASSED")
    #     else:
    #         print('Script failed at adding invalid zone member')
    #         ssh.close()
    #         sys.exit(0)

    # stdin, stdout, stderr = ssh.execute('switchshow')
    # stdin, stdout, stderr = ssh.execute('dsim --devshow')
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi rpa %s "e100"' % pa.edsim_pid)
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi gpat %s %s %s' % (pa.edsim_port, pa.edsim_pid, pa.edsim_wwn))
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi dpa %s %s %s' % (pa.edsim_port, pa.edsim_pid, pa.edsim_wwn))
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi gpat %s %s %s' % (pa.edsim_port, pa.edsim_pid, pa.edsim_wwn))
    # stdin, stdout, stderr = ssh.execute('dsim --fdmi rpa %s "F100"' % pa.edsim_pid)
    # fosconfig = stdout.readlines()
    # for line in fosconfig:
    #     print(line.strip('\n'))
    # ssh.close()
    # sys.exit(0)

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
    #
    # search = re.search('(?:Virtual Fabric:\\t\\t\\t)([a-z]{0,8})', fosconfig, re.M | re.I)
    # search = re.search('(?:Virtual Fabric:\D{0,6})([a-z]{0,8})', fosconfig, re.M | re.I)
    # logger.info("THIS IS SEARCH %s" % search)
    # print('THIS IS THE RESULT OF RE.SEARCH: %s ' % search.group(0))
    # a = search.group(0)
    # b = search.group(1)
    # #if 'enabled' in fosconfig:
    # if 'enabled' in a:
    #     print('true_dat')
    # else:
    #     print('false')
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("lscfg --show")
    # lscfg = ssh_stdout.readlines()
    # print(lscfg)
    # ssh.close()
    # sys.exit(0)
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
    #
    # connect = check_ssh(ip, uname, pwd)
    # # if connect == True:
    # if connect:
    #     print("Inside deffaultmove")
    #     stdin2, stdout2, stderr2 = ssh.exec_command("lscfg --config 128 -slot 2 -port 0-47 -force")
    #     time.sleep(10)
    #     sync_output = []
    #     for line in stdout2:
    #         print(line.strip('\n'))
    #         sync_output.append(line.strip('\n'))
    #         if "Configuration change successful." in sync_output:
    #             print("ports moved to default fid 128")
    #         time.sleep(900)
    #     else:
    #         print(sync_output)
    #         print("ports aren't moved")
    # ssh.close()
    #
    # for fid in range(85, 95):
    #     print(fid)
    # # stat = lsdelete(fid)
    # time.sleep(60)


if __name__ == "__main__":
    main()
