from flask import Flask, render_template
from flask.ext import login

from ConfigParser import ConfigParser
import qstat
import time

JOB_ID_KEY = 'jobID'

cfg = ConfigParser()
cfg.read("frodo.properties")
host = cfg.get('web','host')
port = cfg.getint('web','port')
dev = cfg.getboolean('web','development')

app = Flask(__name__)
app.debug = dev
#login_manager = login.LoginManager()
#login_manager.setup_app(app)

@app.route('/')
@app.route('/jobID/<int:jobID>')
def root_q(jobID = None):
    now = time.asctime()
    fields,records = qstat.parse_qstat1(qstat.qstat_from_tmp_file())
    summary = qstat.summarize1(fields,records)
    if jobID:
        job_details = qstat.parse_qstat_jobID(qstat.qstat_from_tmp_file("tmp2.txt"))
    else:
        job_details = None
    return render_template("qstat.html", time=now, summary=summary, fields=fields, records=records, job=job_details)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
