# Frodo

Frodo is a web server that monitors an SGE ([Sun Grid Engine](http://en.wikipedia.org/wiki/Oracle_Grid_Engine), or as it is called now, Oracle Grid Engine) cluster by SSHing to it and running the [qstat](http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html) command on it.

It displays the results of the `qstat` command, together with some summary statistics, to the user, and allows the user to get more information on specific jobs via the `qstat -j` and to get information on what other users are running using `qstat -u`.

The output is displayed on a browser, saving the effort to connect to the cluster head node via terminal, as well as providing the user with extra information and an automatic refresh.

Screenshots: [Login](http://i.imgur.com/rlt6t.png), [qstat](http://i.imgur.com/LPAZY.png).

## Development 

*Frodo* is still in development, but is considered semi-stable

  - The back end is written in Python 2.7.2
  - The front end is written with HTML + CSS + JavaScript
  - The stable version is [v1]

## Requirements 

Where filenames are given, they are included in the repository. Only Python packages must be manually installed on the server.

  - [v0](https://github.com/yoavram/Frodo/tree/d1acc74011adc5c648d357291f792c880c4313ca):
    - [paramiko](http://www.lag.net/paramiko/) as an SSH implementation
    - [Werkzeug](http://werkzeug.pocoo.org/) as a web application framework
    - [Jinja](http://jinja.pocoo.org/) as a templating engine
  - [v1]:
    - [paramiko](http://www.lag.net/paramiko/) as an SSH implementation
    - [Flask](http://flask.pocoo.org/) as a web application microframework, based on [Werkzeug](http://werkzeug.pocoo.org/) and [Jinja](http://jinja.pocoo.org/)
    - [Twitter Bootstrap](http://twitter.github.com/bootstrap) as a front end (JavaScript and CSS) framework, including:
      - Bootstrap core - *bootstrap.min.js* & *bootstrap.min.css*
      - Bootstrap Responsive plugin for mobile browsers - *bootstrap-responsive.min.css*
      - Bootstrap Tooltip plugin - *bootstrap-tooltip.js*
      - Glyphicons Halflings Free icons - *glyphicons-halflings.png* & *glyphicons-halflings-white.png*
    - jQuery - *jquery-1.9.1.min.js*
    
    - Frodo supports running behind an Apache webserver (instead of Flask's development webserver) using [mod_wsgi](http://flask.pocoo.org/docs/deploying/mod_wsgi/) - *frodo.wsgi*

## Installation
To start using Frodo [v1]:

  - Use a computer with network access (via SSH) to the SGE cluster, and network access (via WWW or a proxy) to the potential clients
  - Check that you know how to connect to the SGE server via SSH with passwor authentication
  - Make sure you have installed Python - probably Python 2.7.x, but other versions may do the trick
  - Make sure you install the python requirements (see above)
  - Get Frodo by one of the following ways:
    - Download Frodo v1 as a [zip file](https://github.com/yoavram/Frodo/archive/a88abf06efe808c74807fc0e5e39c51707f156d6.zip) to your server
    - Clone the repository to the server, and set the head to tag v1 (this option allows you to stay up-to-date using `git pull` commands):
    
```bash
	git clone https://github.com/yoavram/Frodo.git
	git checkout v1
```

  - Create a paramiko *hosts* file to allow paramiko to SSH to the SGE server (see the paramiko documentation on how to [save host keys to file](http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html#save_host_keys))
  - Create a configuration file *frodo.properties*, with the following sections and options:
  
```python
	[sge]
	# the following are used for SSHing the SGE server

	# SGE server SSH listening address
	host = localhost
	# SGE server SSH listening port
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
```

  - Start the server by running `python web.py`
    - If you want to deploy using a different webserver read the [Flask documentation](http://flask.pocoo.org/docs/deploying/)
    - I use Apache with [mod_wsgi](http://flask.pocoo.org/docs/deploying/mod_wsgi/) and *frodo.wsgi* (in the root directory of the repository)
  - Open your favorite browser and point it to the host and port you've given in the *[web]* section of the configuration file
  - Login with the username and password you use for the SGE cluster. Frodo **WILL NOT** save your username and password to file or send it anywhere. The credentials are kept in the [session](http://flask.pocoo.org/docs/quickstart/#sessions) variable of Flask and are only used to connect to the host you give in the *[sge]* section of the configuration file using SSH
  - Review jobs running on the cluster under your username 
  - Clicking on a job ID will bring to the left pane any arguments you have given when running the job (arguments must not be all-caps, all-caps arguments are ignored)
  - Pointing the browser to */qstat/username/<username>*, replacing *<username>* with the username of some other user than yourself, will show that user's queue status (using `qstat -u <username>`)
  - Clicking the Refresh, Pause, Play and Logout buttons will refresh the page, pause automatic refreshing, resume automatic refreshing (every 15 mins, hardcoded in *qstat.html*), and logout your user
  - The time and date of the last refresh are shown at the top of the screen

## ToDo

  - Add some intuitive way to get to /qstat/username/<username>
  - Error messages
    - `"error: [Errno 113] No route to host"` thrown on `ssh.connect()` when the host is unavailable
  - Flashing? see Flask docs
  - Use AJAX/jQuery instead of refreshing

## Contact

If you have any problems using Frodo or you wish to contribute to the code, please feel free to contact [yoavram](https://github.com/yoavram).

  - [My homepage](http://www.yoavram.com/)
  - [My twitter](http://www.twitter.com/yoavram/)

## License
Frodo by Yoav Ram is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-nc-sa/3.0/). 
Frodo could be available under a more permissive license for the right reason - please contact [Yoav](https://github.com/yoavram) if you want to discuss it.

[![CC-BY-NC-SA 3.0](http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)

[v1]: https://github.com/yoavram/Frodo/commit/a88abf06efe808c74807fc0e5e39c51707f156d6