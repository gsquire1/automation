import paramiko
# import sys
import time

ipaddr = "10.38.36.250"
uname = "root"
pwd = "password"
yesSync = 0


def check_ssh(ipaddr, user, pwd):
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ipaddr, username=user, password=pwd)
        return True
    except Exception as e:
        # print e
        return False


def haFailover():
    print("Inside HAFailover function")
    connect = check_ssh(ipaddr, uname, pwd)
    if connect == True:
        stdin, stdout, stderr = ssh.exec_command('echo y|hafailover')
        print("Executed hafailover")
        time.sleep(150)
        ssh.close()
        return True
    else:
        print("No connection")
        return False


def haShow(yesSync):
    print("Inside HAShow")
    sync_output = ''
    connect = check_ssh(ipaddr, uname, pwd)
    if connect == True:
        print("inside hashow connect")
        stdin, stdout, stderr = ssh.exec_command('hashow | grep synchronized')
        # print stdout
        for line in stdout:
            print("hashow output %s" % (line.strip('\n')))
        sync_output = line.strip('\n')
        ssh.close()
        if sync_output == 'HA enabled, Heartbeat Up, HA State synchronized':
            print("HA synchronized")
            return True
        else:
            print("Not synchronized yet, Trying again")
            time.sleep(60)
            yesSync += 1
            if yesSync < 5:
                return haShow(yesSync)
            else:
                print("Tried max times of HAShow")
                return False
    else:
        print("No connection")
        return False


if __name__ == "__main__":

    for i in range(0, 1):
        print(i)
        status = haFailover()
        print("Hafailover status %s" % status)
        if status:
            stat = haShow(yesSync)
            print("Hashow status %s" % stat)
            if not stat:
                break
        else:
            print("No connection")
            break
