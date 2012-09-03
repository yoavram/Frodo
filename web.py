#!/usr/bin/python
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

from ConfigParser import ConfigParser
import qstat
import time

JOB_ID_KEY = 'jobID'

cfg = ConfigParser()
cfg.read("/home/user/workspace/frodo/frodo.properties")

app = Flask(__name__)
app.debug = cfg.getboolean('web','development')
app.secret_key = cfg.get('web','secret')

@app.route('/')
def index():
    return redirect(url_for('qstat'))

@app.route('/')
@app.route('/qstat')
@app.route('/qstat/jobID/<int:jobID>')
@app.route('/qstat/username/<qusername>')
def index(jobID = None, qusername=None):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    password = session['password']
    now = time.asctime()
    result = qstat.parse_qstat1(qstat.exec_qstat(username, password, qstat_username=qusername))
    fields = result['fields']
    records = result['records']
    summary = qstat.summarize1(fields,records)
    if jobID:
        job_details = qstat.parse_qstat_jobID(qstat.exec_qstat(username, password, jobID=jobID))
    else:
        job_details = None
    return render_template("qstat.html", username=username, time=now, summary=summary, fields=fields, records=records, job=job_details)

@app.route('/qstat/json')
def qstat_json():
    if 'username' not in session:
        return {'error':'please login','url':url_for('login')}
    username = session['username']
    password = session['password']
    now = time.asctime()
    qstat_result = qstat.parse_qstat1(qstat.exec_qstat(username, password))
    qstat_result.update(qstat.summarize1(qstat_result['fields'],qstat_result['records']))
    qstat_result['time'] = now
    return jsonify(**qstat_result)

@app.route('/qstat/jobID/<int:jobID>/json')
def qstat_job_json(jobID):
    if 'username' not in session:
        return {'error':'please login','url':url_for('login')}
    username = session['username']
    password = session['password']
    now = time.asctime()
    qstat_result = qstat.parse_qstat_jobID(qstat.exec_qstat(username, password, jobID=jobID))
    qstat_result['time'] = now
    return jsonify(**qstat_result)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for("index"))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    host = cfg.get('web','host')
    port = cfg.getint('web','port')
    app.run(host=host, port=port)
