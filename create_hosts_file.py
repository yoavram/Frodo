from __future__ import print_function
from builtins import str
from builtins import input
import paramiko
import common
import getpass
import os

cfg = common.configuration()
host = cfg.get('sge','host')
port = cfg.getint('sge','port')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
username = str(input("Username:"))
print(username)
password = getpass.getpass()
ssh.connect(host, port, username, password)
ssh.save_host_keys("hosts")
if os.path.exists('hosts'):
	with open('hosts') as f:
		print(f.read())
else:
	print("Failed")
