import qstat
import time
# http://werkzeug.pocoo.org/docs/tutorial/#step-0-a-basic-wsgi-introduction
from werkzeug.wrappers import Request, Response
# http://jinja.pocoo.org/docs/api/
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'), auto_reload=True)

@Request.application
def application(request):
    now = time.asctime()
    fields,records = qstat.parse_qstat1(qstat.exec_qstat())
    summary = qstat.summarize1(fields,records)
    template = env.get_template("qstat.html")
    html = template.render(time=now, summary=summary, fields=fields, records=records)
    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    from ConfigParser import ConfigParser
    cfg = ConfigParser()
    cfg.read("frodo.properties")
    host = cfg.get('web','host')
    port = cfg.getint('web','port')
    dev = cfg.getboolean('web','development')
    run_simple(host, port, application, use_debugger=dev, use_reloader=dev)
