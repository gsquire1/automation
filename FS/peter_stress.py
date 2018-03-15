#!/usr/bin/env python3


# import telnetlib
# import getpass
import argparse
import csv
import sys
import time
import logging
import paramiko

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
    # pp.add_argument("ip", help="IP address of SUT")
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

    if not args.chassis_name and not args.ipaddr:
        print("Chassis Name or IP address is required")
        sys.exit()

    if args.cmdprompt and not args.switchtype:
        print("To start at the command prompt the switch type is needed.")
        sys.exit()

    if not args.cmdprompt and args.switchtype:
        print('To start at the command prompt both switch type and command prompt is requried')
        sys.exit()
    # print("Connecting to IP :  " + args.ip)
    # print("user             :  " + args.user)
    # verbose    = args.verbose

    return parser.parse_args()


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

# ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(host, port=22, username=username, password=password, timeout=3,)
# transport = ssh.get_transport()
# pause = 1

# resp1 = issue_command(transport, pause, cmd1)


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
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
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
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
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
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
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

    # create the remote directory structure
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("the command here")
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("lscfg --show")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.execute("ipaddrshow")
    logger.info("Results:\n\tstd-in = {}\n\tstd-out = {}\n\tstd-err = {}".format(
        ssh_stdin, ssh_stdout, ssh_stderr
    ))

    #ssh.close()

    # connect = check_ssh(ip, uname, pwd)
    if ssh:
        # print(ssh_stdout)
        # print(type(ssh_stdout))
        for line in ssh_stdout:
            print(line)
        # console_op = ("".join(stdout.readlines()))
        # for line in ssh_stdin:
        #     print(line)
    # if connect:
        sync_output = []
        # cmd = "switchshow"
        # cmd = "lscfg --show"
        # cmd = "ipaddrshow"
        # print(cmd)
        no_vf = "lscfg: requires VF to be supported."
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # for line in stdout:
        #     print(line)
        # console_op = ("".join(stdout.readlines()))
        # print(type(console_op))
        # # console_op = console_op.append(line.strip('\n'))
        # print(console_op)
        # sys.exit(0)
        # for line in console_op:
        #     line = line.strip('\n')
        #     print(line)
        # console_op.strip('\n')
        # print(console_op)
        # if "SWITCH" in console_op:
        #     print("FOUND IT")
        # else:
        #     print("NOT THERE")
        #     print(stdin.strip('\n'))
        #     op = stdout.readlines()
        #     print("OPOPOPOPOPOPOPOPOPOPOPOPOP")
        #     print(op)
        ssh.close()
        sys.exit()
        if no_vf in stdout:
            print("Found it")
            sys.exit(0)
        else:
            print("didn't find it")
        sys.exit()
        # for line in stdout:
        #     a = False
        #     print(line)
        #     while line != no_vf:
        #         a = True
        #     break
        if not a:
            ssh.close()
            return True
        else:
            ssh.close()
            return False
            # sync_output.append(line.strip('\n'))
            # print(sync_output)
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
            #     return True

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
    print(pa)
    # print(pa.chassis_name)
    print(pa.ipaddr)
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
    #
    #
    if pa.ipaddr:
        print("do IP steps")
        pa.chassis_name = console_info_from_ip(pa.ipaddr)
    ip = pa.ipaddr
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
    # si = anturlar.SwitchInfo()
    # a = si.director()
    # print(a)
    # connect = check_ssh(pa.ipaddr, uname, pwd)
    chassis = director(ip)
    # print("CHASSIS")
    # print(chassis)

    if chassis:
        print("Director")
    else:
        print("Pizza Box")

    vf = vf_capable(ip)
    # vf = vf_capable_transport(ip)
    print("VFVFVFVF")
    print(vf)
    if vf:
        print("VF Supported")
    else:
        print("VF not supported. Please check you are trying the correct switch")
        sys.exit(0)

    for i in range(0, 10):
        print(i)
        for fid in range(1, 9):
            print(fid)
            status = lscreate(fid, pa.ipaddr)
            print(status)
            if status:
                time.sleep(15)
                connect = check_ssh(pa.ipaddr, uname, pwd)
                if connect:
                    cmd = "setcontext %s" % fid
                print("logged into ls %s" % fid)
                # stdin, stdout, stderr = ssh.exec_command(cmd)
                cmd1 = "lscfg --config %s -slot 12 -port 0-63 -force" % fid
                stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
                time.sleep(60)
                sync_output = []
                for line in stdout:
                    print(line.strip('\n'))
                    sync_output.append(line.strip('\n'))
                    if "Configuration change successful." in sync_output:
                        print("ports moved to newfid %s" % fid)
            else:
                # print(sync_output)
                print("ports aren't moved")
                break
            ssh.exec_command("setcontext %s" % fid)
            ssh.exec_command("switchdisable;switchenable")
            print("switch toggled")
            time.sleep(350)
        ssh.close()
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
