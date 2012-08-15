import qstat
from ConfigParser import ConfigParser
import time
import os.path
# http://werkzeug.pocoo.org/docs/tutorial/#step-0-a-basic-wsgi-introduction
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
# http://jinja.pocoo.org/docs/api/
from jinja2 import Environment, FileSystemLoader

JOB_ID_KEY = 'jobID'

cfg = ConfigParser()
cfg.read("frodo.properties")
host = cfg.get('web','host')
port = cfg.getint('web','port')
dev = cfg.getboolean('web','development')    
env = Environment(loader=FileSystemLoader('./templates'), auto_reload=dev)

@Request.application
def application(request):
    now = time.asctime()
    fields,records = qstat.parse_qstat1(qstat.exec_qstat())
    summary = qstat.summarize1(fields,records)
    template = env.get_template("qstat.html")
    job_details = None
    if len(request.args) > 0 and JOB_ID_KEY in request.args:
        jobID = request.args[JOB_ID_KEY]
        job_details = qstat.parse_qstat_jobID(qstat.exec_qstat(jobID))
    html = template.render(time=now, summary=summary, fields=fields, records=records, job=job_details)
    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    run_simple(host, port, application, static_files = {'/static':  os.path.join(os.path.dirname(__file__), 'static')}, use_debugger=dev, use_reloader=dev, extra_files=['frodo.properties','qstat.py'])
