import paramiko
import re
from ConfigParser import ConfigParser

pattern = re.compile(r"^(?P<jobID>\d+)\s+(?P<prior>[\.\d]+)\s+(?P<name>\w+)\s+(?P<username>\w+)\s+(?P<state>\w+)\s+(?P<date>[\d\w\/]+)\s+(?P<time>[\d:]+)\s+(?P<queue>[@\w\.-]*)\s+(?P<slots>\d+)\s+(?P<jaTaskID>[\d\-:]+)$", re.M)
ja_task_ID_pattern = re.compile(r'^(\d+)-(\d+):\d+$')

def smart_get_option(cfg, section, option):
    if cfg.has_section(section):
        if cfg.has_option(section, option):
            return cfg.get(section, option)
    return None

cfg = ConfigParser()
cfg.read('frodo.properties')
host = cfg.get('sge','host')
port = cfg.getint('sge','port')
    
def exec_qstat(username, password, jobID = None, qstat_username=None):
    ssh = paramiko.SSHClient()
    ssh.load_host_keys("hosts")
    ssh.connect(host, port, username, password)
    query = "qstat"
    if jobID:
        query += " -j " + str(jobID)
    if qstat_username:
        query += " -u " + username
    stdin, stdout, stderr = ssh.exec_command(query)
    err = stderr.read()
    result = stdout.read()
    ssh.close()
    if err:
        #TODO something here
        print "*** ERROR:",err
    return result

def qstat_from_tmp_file(filename="tmp.txt"):
    fin = open(filename)
    result = fin.read()
    fin.close()
    return result

def parse_qstat1(qstat):
    fields = qstat[:qstat.find("\n")].split()
    records = pattern.findall(qstat)
    return {'fields':fields, 'records':records}

def parse_qstat2(qstat):
    fields,records = parse_qstat1(qstat)
    return records_to_dict(fields, records)

def records_to_dict(fields,records):
    return [dict(zip(fields,records[i])) for i in range(len(records))]

def parse_qstat_jobID(qstat):
    qstat = qstat[qstat.find('\n')+1:]
    records = [map(str.strip, x.split(':',1)) for x in qstat.split('\n')]
    if len(records)>0:
        records = map(tuple, records)[:-1]
        records = messy_tuples_to_dict(records)
    return records

def messy_tuples_to_dict(tuples):
    dic = {}
    for tup in tuples:
        if len(tup)==2:
            k,v = tup
            dic[k] = v
    if 'scheduling info' in dic:
        dic.pop('scheduling info')
    if 'env_list' in dic:
        env_list = dic.pop('env_list').split(',')
        env_dict = {}
        for x in env_list:
            k,v = x.split('=',1)
            if k.upper() != k:
                env_dict[k] = v
        dic['params'] = env_dict
    return dic
    

def summarize1(fields,records):
    records = records_to_dict(fields,records)
    return summarize2(records)

def summarize2(records):
    r = len(filter(lambda x: x['state'] == 'r', records))
    qws = filter(lambda x: x['state'] == 'qw', records)
    qw = sum( map(qw_tasks, qws) )
    return {'r':r,'qw':qw, 'total':r+qw}

def qw_tasks(record):
    ja_task_ID = record['ja-task-ID']
    m = ja_task_ID_pattern.match(ja_task_ID)
    t0 = int(m.groups()[0])
    t1 = int(m.groups()[1])
    return t1-t0+1
    
if __name__ == '__main__':
    #records = parse_qstat2(qstat_from_tmp_file("tmp.txt"))
    #job = parse_qstat_jobID(qstat_from_tmp_file("tmp2.txt"))
    pass
