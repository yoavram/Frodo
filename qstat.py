import paramiko
import getpass
import re

pattern = re.compile(r"^(?P<jobID>\d+)\s+(?P<prior>[\.\d]+)\s+(?P<name>\w+)\s+(?P<username>\w+)\s+(?P<state>\w+)\s+(?P<date>[\d\w\/]+)\s+(?P<time>[\d:]+)\s+(?P<queue>[@\w\.-]+)\s+(?P<slots>\d+)\s+(?P<jaTaskID>\d+)$", re.M)

def exec_qstat():
    # TODO read from config file
    host = raw_input("hostname:")
    port = input("port:")

    username = raw_input("username:")
    password = getpass.getpass()

    ssh = paramiko.SSHClient()
    ssh.load_host_keys("hosts")

    ssh.connect(host, port, username, password)
    print "Connected to",username+"@"+host+":"+str(port)

    stdin, stdout, stderr = ssh.exec_command("qstat")
    err = stderr.read()
    result = stdout.read()
    ssh.close()
    if err:
        #TODO something here
        print "*** ERROR:",err
    return result

def qstat_from_tmp_file():
    fin = open("tmp.txt")
    result = fin.read()
    fin.close()
    return result

def parse_qstat(qstat):
    fields = qstat[:qstat.find("\n")].split()
    values = pattern.findall(qstat)
    return fields,values

fields,values = parse_qstat(qstat_from_tmp_file())
