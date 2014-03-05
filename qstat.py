#!/usr/bin/python
# Frodo - A web app for monitoring SGE cluster status: https://bitbucket.org/yoavram/frodo
# Copyright (c) 2012 by Yoav Ram.
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.
import paramiko
import re
import common
import subprocess

pattern = re.compile(r"^(?P<jobID>\d+)\s+(?P<prior>[\.\d]+)\s+(?P<name>\w+)\s+(?P<username>\w+)\s+(?P<state>\w+)\s+(?P<date>[\d\w\/]+)\s+(?P<time>[\d:]+)\s+(?P<queue>[@\w\.-]*)\s+(?P<slots>\d+)\s+(?P<jaTaskID>[\d\-:]*)$", re.M)
ja_task_ID_pattern = re.compile(r'^(\d+)-(\d+):\d+$')

def smart_get_option(cfg, section, option):
    if cfg.has_section(section):
        if cfg.has_option(section, option):
            return cfg.get(section, option)
    return None

cfg = common.configuration()
host = cfg.get('sge','host')
port = cfg.getint('sge','port')

def local_qstat(jobID = None, qstat_username=None):
    query = ["qstat"]
    if jobID:
        query.append("-j")
        query.append(str(jobID))
    if qstat_username:
        query.append("-u")
        query.append(str(qstat_username))
    #print "query:",query
    try:
        result = subprocess.check_output(query)    
        return result
    except subprocess.CalledProcessError as e:
        return str(e)
    
def exec_qstat(username, password, jobID = None, qstat_username=None):
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(common.hosts())
    try:
        ssh.connect(host, port, username, password)
    except paramiko.SSHException as e:
        ssh.close()
        return str(e)
    query = "python ~/workspace/Frodo/qstat.py "
    if jobID:
        query += str(jobID)
    elif qstat_username:
        query += qstat_username
    #print "query:",query
    stdin, stdout, stderr = ssh.exec_command(query)
    err = stderr.read()
    result = stdout.read()
    ssh.close()
    if err:
        return("Error: " + err)
    return result

def qstat_from_tmp_file(filename="tmp.txt"):
    fin = open(filename)
    result = fin.read()
    fin.close()
    return result

def parse_qstat1(qstat):
    fields = qstat[:qstat.find("\n")].split()
    try:
        ind = [fields.index('prior'), fields.index('slots')]
    except ValueError:
        return {'fields':fields, 'records':[]}
    ind.sort(reverse=True)
    for i in ind: fields.pop(i)
    records = pattern.findall(qstat)
    for j in range(len(records)):
        records[j] = list(records[j])
        for i in ind: records[j].pop(i)
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
    if m:
        t0 = int(m.groups()[0])
        t1 = int(m.groups()[1])
        return t1-t0+1
    else:
        return 1
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        additional = sys.argv[1]
        if additional.isdigit():
            print parse_qstat_jobID(local_qstat(jobID=additional))
        else:
            print parse_qstat1(local_qstat(qstat_username=additional))
    else:        
        print parse_qstat1(local_qstat())
    #records = parse_qstat2(qstat_from_tmp_file("tmp.txt"))
    #job = parse_qstat_jobID(qstat_from_tmp_file("tmp2.txt"))
    
