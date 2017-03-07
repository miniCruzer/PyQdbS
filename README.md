# PyQdbS

This is one of those silly quote database systems similar to the original [QdbS](http://www.qdbs.org/news.php) system in PHP.
The original QdbS hasn't been updated since 2007, and it's written in PHP. No thanks. :-1:

I only build/test on Python 3.5 and later. It might work on earlier versions of Python.

You can see a live version of this at [nou.fyi](https://www.nou.fyi) used on [AlphaChat](https://www.alphachat.net).

This repository is still **highly alpha** software, and is very subject to changes in requirements, dependencies, and SQL schema (e.g. your quotes database becomes incompatible).

## Requirements

All modules are available from PyPi.

- Python 3.5 or later
- Flask
- flask_nav
- flask_bootstrap
- WTForms
- flup6 (for deploying with WSGI)

## Installation

1. Clone this repository.
2. Install the dependencies via `pip install -r requirements.txt`
3. Initialize the database. You can run `flask initdb` to have this automated, **or** run `sqlite3 qdbs.db < schmeal.sql`.
4. Create an environment variable called `PYQDBS_SETTINGS`, and make it point to a configuration file similar to the example.

:warning:Change the SECRET_KEY in the config or sessions will not be secure, as they are cryptographically signed by Flask.:warning:

### Deploying

There are a few options for deploying this. To understand all the available methods, see the [Flask Deploying Options](http://flask.pocoo.org/docs/0.12/deploying/).
For self-hosting, I recommend the [nginx](http://flask.pocoo.org/docs/0.12/deploying/fastcgi/#configuring-nginx) WSGI method.

A reverse proxy will work, but is not a good idea.

#### WSGIServer

This assumes you have PyQdbS installed as a 'qdbs' user with a $HOME of `/var/lib/qdbs`, and the PyQdbS repository at `/var/lib/qdbs/pyqdbs/`

1. If needed, edit `qdbs.fcgi` if you would like to change where the UNIX scoket gets created. Your web-server will need permission to speak to this file.
2. Optionally create an init script to launch this service for you. An OpenRC init script is provided in the dist folder that can be adapted to your setup.
3. Configure nginx. You'll want some location blocks, similar to this:

```
location / {

    try_files $uri @pyqdbs;
}

location @pyqdbs {

    include             fastcgi_params;
    fastcgi_param       PATH_INFO $fastcgi_script_name;
    fastcgi_param       SCRIPT_NAME "";
    fastcgi_pass        unix:/var/lib/qdbs/fcgi.sock;
}
```

## Notice

This is my first time working with Flask and Bootstrap. If you have any suggestions, or anything I'm doing is Not The Right Thing To Do, please open an issue.

## TODO

Some goals for the project. 

- [ ] Anti-Spam 
- [ ] Admin feature (editing, deleting, quote approval)
- [ ] Upvote / Downvote *
- [ ] Auto-remove timestamps from Add Quote
- [ ] RESTful API, probably Flask-Rest
- [ ] Hidden Quotes  *

* = will break SQL schema
