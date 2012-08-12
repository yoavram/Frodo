import paramiko
import re
from ConfigParser import ConfigParser

pattern = re.compile(r"^(?P<jobID>\d+)\s+(?P<prior>[\.\d]+)\s+(?P<name>\w+)\s+(?P<username>\w+)\s+(?P<state>\w+)\s+(?P<date>[\d\w\/]+)\s+(?P<time>[\d:]+)\s+(?P<queue>[@\w\.-]*)\s+(?P<slots>\d+)\s+(?P<jaTaskID>[\d\-:]+)$", re.M)
cfg = ConfigParser()
cfg.read('frodo.properties')

def exec_qstat():
    host = cfg.get('sge','host')
    port = cfg.getint('sge','port')

    username = cfg.get('sge','username')
    password = cfg.get('sge','password')

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

def parse_qstat1(qstat):
    fields = qstat[:qstat.find("\n")].split()
    records = pattern.findall(qstat)
    return fields,records

def parse_qstat2(qstat):
    fields,records = parse_qstat1(qstat)
    return records_to_dict(fields, records)

def records_to_dict(fields,records):
    return [dict(zip(fields,records[i])) for i in range(len(records))]

def summarize1(fields,records):
    records = records_to_dict(fields,records)
    return summarize2(records)

def summarize2(records):
    r = len(filter(lambda x: x['state'] == 'r', records))
    qw = len(filter(lambda x: x['state'] == 'qw', records))
    return {'r':r,'qw':qw}    
    
if __name__ == '__main__':
    records = parse_qstat2(qstat_from_tmp_file())
