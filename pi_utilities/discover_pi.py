import subprocess
import paramiko
from hello_settings import SECRETS_DICT


def discover_pi():
    ips = subprocess.check_output("/usr/local/bin/nmap 172.20.10.6/24 -n -sP | grep report | awk '{print $5}'", shell=True)
    for ip_address in ips.split('\n'):
        print ip_address
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=SECRETS_DICT['PI_USERNAME'], password=SECRETS_DICT['PI_PASSWORD'])
            print '++ found pi: {}'.format(ip_address)
        except Exception as e:
            print str(e.message)
            continue


if __name__ == '__main__':
    discover_pi()