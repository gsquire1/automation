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


# import re

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
# import anturlar
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
    # print("Connecting to IP :  " + args.ip)
    # print("user             :  " + args.user)
    # verbose    = args.verbose

    # return parser.parse_args()
    return args


uname = "admin"
pwd = "password"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SSHClient(object):

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
        print(host, username, password)
        print("Connecting to server on ip", str(host) + ".")
        # sys.exit(0)
        self.client = paramiko.client.SSHClient()  # Sets self.client as paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(host, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((host, 22))
        self.transport.connect(username=username, password=password)

        # starts the output checking thread
        # thread = threading.Thread(target=self.process)
        # thread.daemon = True
        # thread.start()

    def closeConnection(self):
        if self.client is not None:
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
            print('BBBBBBBBBBBBBBBBBBBBBBBBBB')
            if self.shell is not None and self.shell.recv_ready():
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
        cmd = "lscfg --delete %s -force" % (fid)
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


def main():

    pa = parse_args()
    print("@" * 40)
    print(pa)
    print(pa.ip)
    print("@" * 40)
    # sys.exit(0)

    ###################################################################################################################
    ###################################################################################################################
    #
    # if user enter ip address then get the chassisname from the SwitchMatrix file
    # then get the info from the SwitchMatrix file using the Chassis Name
    #
    #
    #
    # if pa.ipaddr:
    #     print("do IP steps")
    #     pa.chassis_name = console_info_from_ip(pa.ipaddr)
    # cons_info = console_info(pa.chassis_name)
    # console_ip = cons_info[0]
    # console_port = cons_info[1]
    # console_ip_bkup = cons_info[2]
    # console_port_bkup = cons_info[3]
    # power_pole_info = pwr_pole_info(pa.chassis_name)
    # usr_pass = get_user_and_pass(pa.chassis_name)
    # user_name = usr_pass[0]
    # usr_psswd = usr_pass[1]
    # ipaddr_switch = get_ip_from_file(pa.chassis_name)
    # steps_to_run = pa.steps
    # fid_to_compare = 128
    #################################### Sample Text ###############################################################
    # ssh = SSHClient(ip, uname, pwd)
    ip = pa.ip
    connection = SSH(ip, uname, pwd)
    print('AAAAAAAAAAAAAAAAAAAAA')
    connection.openShell()
    while True:
        command = input('$ ')
        if command.startswith('exit'):
            break
        if command.startswith(" "):
            command = command[1:]
        connection.sendShell(command)

    SSH.closeConnection(connection)
    sys.exit(0)

    # ssh = SSHClient(pa.ip, uname, pwd) # SSHClient() is a class

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
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("fosconfig --show")
    # fosconfig = ssh_stdout.readlines()
    # fosconfig = (str(fosconfig))
    # # print(fosconfig)
    # # ssh.close()
    # # sys.exit(0)
    # # search = re.search('(?:Virtual Fabric:\\t\\t\\t)([a-z]{0,8})', fosconfig, re.M | re.I)
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
    # # for line in foscfg:
    # #     if line != '':
    # #         output = (line.strip('\n'))
    # #         logger.info('   printing output')
    # #         print(output)
    # #     else:
    # #         print('No information read from vf_capable function')
    # # print(output)
    # # search = re.search('(requires)', output, re.M | re.I)
    # # logger.info(search)
    # # if search is None:
    # #     print("\n\n\nVF not enabled on this switch\n\n\n")
    # #     return (False)
    # # else:
    # #     print("\n\n\nVF is enabled on this switch\n\n\n")
    # #     return (True)
    # # logger.info ("ssh succcessful. Closing connection")
    # # ssh.close()
    # # Example on how to print Human readable results:
    # # print('\n\n'+ '='*20)
    # # print("Switch Name :  %s" % initial_checks[0])
    # # print("IP address :  %s" % initial_checks[1])
    # # print("Chassis :  %s" % initial_checks[2])
    # # print("VF enabled :  %s" % initial_checks[3])
    # # print("FCR enabled :  %s" % initial_checks[4])
    # # print("Base configured :  %s" % initial_checks[5])
    # # print('='*20 + '\n\n')
    # sys.exit(0)
    #
    # chassis = director(ip)
    # if chassis:
    #     print("Director")
    # else:
    #     print("Pizza Box")
    #
    # vf = vf_capable(ip)
    # # vf = vf_capable_transport(ip)
    # print("VFVFVFVF")
    # print(vf)
    # if vf:
    #     print("VF Supported")
    # else:
    #     print("VF not supported. Please check you are trying the correct switch")
    #     sys.exit(0)
    # sys.exit(0)
    # for i in range(0, 10):
    #     print(i)
    #     for fid in range(1, 9):
    #         print(fid)
    #         status = lscreate(fid, pa.ipaddr)
    #         print(status)
    #         if status:
    #             time.sleep(15)
    #             connect = check_ssh(pa.ipaddr, uname, pwd)
    #             if connect:
    #                 cmd = "setcontext %s" % fid
    #             print("logged into ls %s" % fid)
    #             # stdin, stdout, stderr = ssh.exec_command(cmd)
    #             cmd1 = "lscfg --config %s -slot 12 -port 0-63 -force" % fid
    #             stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
    #             time.sleep(60)
    #             sync_output = []
    #             for line in stdout:
    #                 print(line.strip('\n'))
    #                 sync_output.append(line.strip('\n'))
    #                 if "Configuration change successful." in sync_output:
    #                     print("ports moved to newfid %s" % fid)
    #         else:
    #             # print(sync_output)
    #             print("ports aren't moved")
    #             break
    #         ssh.exec_command("setcontext %s" % fid)
    #         ssh.exec_command("switchdisable;switchenable")
    #         print("switch toggled")
    #         time.sleep(350)
    #     ssh.close()
    # # connect = check_ssh(ip, uname, pwd)
    # # # if connect == True:
    # # if connect:
    # #     print("Inside deffaultmove")
    # #     stdin2, stdout2, stderr2 = ssh.exec_command("lscfg --config 128 -slot 2 -port 0-47 -force")
    # #     time.sleep(10)
    # #     sync_output = []
    # #     for line in stdout2:
    # #         print(line.strip('\n'))
    # #         sync_output.append(line.strip('\n'))
    # #         if "Configuration change successful." in sync_output:
    # #             print("ports moved to default fid 128")
    # #         time.sleep(900)
    # #     else:
    # #         print(sync_output)
    # #         print("ports aren't moved")
    # # ssh.close()
    # #
    # # for fid in range(85, 95):
    # #     print(fid)
    # # # stat = lsdelete(fid)
    # # time.sleep(60)


if __name__ == "__main__":
    main()
