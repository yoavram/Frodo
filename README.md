== Frodo ==

Frodo is a web server that monitors an SGE ([[http://en.wikipedia.org/wiki/Oracle_Grid_Engine | Sun Grid Engine]], or as it is called now, Oracle Grid Engine) cluster by SSHing to it and running the [[http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html | {{{qstat}}}]] command on it.\\
It displays the results of the {{{qstat}}} command, together with some summary statistics, to the user, and allows the user to get more information on specific jobs via the {{{qstat -j}}} and to get information on what other users are running using {{{qstat -u}}}.\\
The output is displayed on a browser, saving the effort to connect to the cluster head node via terminal, as well as providing the user with extra information and an automatic refresh.

== Development ==
*Frodo is still in development, but is considered semi-stable
*The back end is written in Python 2.7.2
*The front end is written with HTML+CSS+JavaScript
*The stable version is [[https://bitbucket.org/yoavram/frodo/src/355c5a593cfb/ | tag v1]]
*See the [[ToDo]] list for a development plan

== Requirements ==
* [[https://bitbucket.org/yoavram/frodo/src/8e3c93faf600/ | v0]]:
** [[http://www.lag.net/paramiko/ | paramiko]] as an SSH implementation
** [[http://werkzeug.pocoo.org/ | Werkzeug]] as a web application framework
** [[http://jinja.pocoo.org/ | Jinja]] as a templating engine

* [[https://bitbucket.org/yoavram/frodo/src/355c5a593cfb/ | v1]] (Where filenames are given, they are included in the repository. Only Python packages must be manually installed on the server):
** [[http://www.lag.net/paramiko/ | paramiko]] as an SSH implementation
** [[http://flask.pocoo.org/ | Flask]] as a web application microframework, based on [[http://werkzeug.pocoo.org/ | Werkzeug]] and [[http://jinja.pocoo.org/ | Jinja]]
** [[http://twitter.github.com/bootstrap | Twitter Bootstrap]] as a front end (JavaScript and CSS) framework, including:
*** Bootstrap core - {{{bootstrap.min.js}}} & {{{bootstrap.min.css}}}
*** Bootstrap Responsive plugin for mobile browsers - {{{bootstrap-responsive.min.css}}}
*** Bootstrap Tooltip plugin - {{{bootstrap-tooltip.js}}}
*** Glyphicons Halflings Free icons - {{{glyphicons-halflings.png}}} & {{{glyphicons-halflings-white.png}}}
*** jQuery - {{{jquery-1.7.2.min.js}}}
** Frodo supports running behind an Apache webserver (instead of Flask's development webserver) using [[http://flask.pocoo.org/docs/deploying/mod_wsgi/ | mod_wsgi]] - {{{frodo.wsgi}}}

== Installation ==
To start using Frodo v1:
* Use a computer with network access (via SSH) to the SGE cluster, and network access (via WWW or a proxy) to the potential clients
* Check that you know how to connect to the SGE server via SSH with passwor authentication
* Make sure you have installed Python - probably Python 2.7.x, but other versions may do the trick
* Make sure you install the python requirements (see above)
* Get Frodo by one of the following ways:
**Download Frodo v1 from the [[https://bitbucket.org/yoavram/frodo/downloads | downloads]] section (available in zip/gzip/bz2) to your server
**Clone the repository to the server, and set the head to tag v1 (this option allows you to stay up-to-date using {{{hg pull -u}}} commands):
{{{
#!sh
$ hg clone https://bitbucket.org/yoavram/frodo
$ hg update -r v1
}}}
* Create a paramiko {{{hosts}}} file to allow paramiko to SSH to the SGE server (see the paramiko documentation on how to [[http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html#save_host_keys | save host keys to file]])
* Create a configuration file {{{frodo.properties}}}, with the following sections and options:
{{{
#!python
[sge]
# the following are used for SSHing the SGE server

#SGE server SSH listening address
host = localhost
#SGE server SSH listening port
port = 22

[web]
# the follwoing are used for the browsing to the Frodo web server

# Frodo server address
host = localhost
# note that port 80 will require extra configuration and/or sudo privileges
port = 8080
# see http://flask.pocoo.org/docs/quickstart/#sessions for why Flask uses secrets and how to generate them
secret = OneRingToBringThemAllAndInTheDarknessBindThem
# True means that debug output is shown on the console and that any change to the files will cause the server to reload
development = True 

}}} 
* Start the server by running {{{$python web.py}}}
** If you want to deploy using a different webserver read the [[[[http://flask.pocoo.org/docs/deploying/ | Flask documentation]]
** I use Apache with [[[[http://flask.pocoo.org/docs/deploying/mod_wsgi/ | mod_wsgi]] and frodo.wsgi (in the root directory of the repository)
* Open your favorite browser and point it to the host and port you've given in the {{{[web]}}} section of the configuration file
* Login with the username and password you use for the SGE cluster. Frodo **WILL NOT** save your username and password to file or send it anywhere. The credentials are kept in the [[http://flask.pocoo.org/docs/quickstart/#sessions | session]] variable of Flask and are only used to connect to the host you give in the {{{[sge]}}} section of the configuration file using SSH
* Review jobs running on the cluster under your username 
* Clicking on a job ID will bring to the left pane any arguments you have given when running the job (arguments must not be all-caps, all-caps arguments are ignored)
* Pointing the browser to {{{/qstat/username/<username>}}}, replacing <username> with the username of some other user than yourself, will show that user's queue status (using {{{qstat -u <username>}}})
* Clicking the Refresh, Pause, Play and Logout buttons will refresh the page, pause automatic refreshing, resume automatic refreshing (every 15 mins, hardcoded in {{{qstat.html}}}), and logout your user
* The time and date of the last refresh are shown at the top of the screen

== Contact ==

If you have any problems using Frodo or you wish to contribute to the code, please feel free to contact [[https://bitbucket.org/account/notifications/send/?receiver=yoavram&subject=frodo | me]].\\
*[[http://www.yoavram.com | My homepage]]
*[[http://www.twitter.com/yoavram | My twitter]]

== License ==
Frodo by Yoav Ram is licensed under a [[http://creativecommons.org/licenses/by-sa/3.0/|Creative Commons Attribution-ShareAlike 3.0 Unported License]].\\\\
[[http://creativecommons.org/licenses/by-sa/3.0/|{{http://i.creativecommons.org/l/by-sa/3.0/88x31.png}}]]
