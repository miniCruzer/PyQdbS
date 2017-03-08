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
- flask_sqlalchemy
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

## reCAPTCHA

If you would like to use reCAPTCHA with PyQdbS, you need to register with Google, and set the following settings in your PYQDBS_SETTINGS file.

| Setting               |            | Description                                                                             |
| ----------------------|------------|-----------------------------------------------------------------------------------------|
| RECAPTCHA_PUBLIC_KEY 	| *required* | A public key.                                                                           |
| RECAPTCHA_PRIVATE_KEY | *required* | A private key.                                                                          |
| RECAPTCHA_API_SERVER 	| optional   | Specify your Recaptcha API server.                                                      |
| RECAPTCHA_PARAMETERS 	| optional   | A dict of JavaScript (api.js) parameters.                                               |
| RECAPTCHA_DATA_ATTRS 	| optional   | A dict of data attributes options. https://developers.google.com/recaptcha/docs/display |

This table is from the Flask-WTF documentation page [here](https://flask-wtf.readthedocs.io/en/latest/form.html#recaptcha).
You can see more settings for the HTML forms in this application [here](https://flask-wtf.readthedocs.io/en/latest/config.html).

## Notice

This is my first time working with Flask and Bootstrap. If you have any suggestions, or anything I'm doing is Not The Right Thing To Do, please open an issue.

## TODO

Some goals for the project. 

- [X] Anti-Spam
- [ ] Admin feature (editing, deleting, quote approval)
- [ ] Upvote / Downvote *
- [ ] Auto-remove timestamps from Add Quote
- [ ] RESTful API, probably Flask-Rest
- [ ] Hidden Quotes  *
- [X] Convert forms to use macros provided by `bootstrap/wtf.html`
- [ ] Multiple database backend support (via SQLAlchemy/flask_sqlalchemy)
- [X] Pagination support through the use of SQLAlchemy

* = will break SQL schema
