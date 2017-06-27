# PyQdbS

This is one of those silly quote database systems similar to the original [QdbS](http://www.qdbs.org/news.php) system in PHP.
The original QdbS hasn't been updated since 2007, and it's written in PHP. No thanks. :-1:

I only build/test on Python 3.5 and later. It might work on earlier versions of Python.

You can see a live version of this at [nou.fyi](https://www.nou.fyi) used on [AlphaChat](https://www.alphachat.net).

This repository is still **highly alpha** software, and is very subject to changes in requirements, dependencies, and SQL schema (e.g. your quotes database becomes incompatible).

## Features

- Admin interface (create, read, update, delete, and export quotes)
- Random Quotes
- REST API to retrieve quotes
- reCAPTCHA for anti spam

## Requirements

All modules are available from PyPi.

- Python 3.5 or later
- Flask
- flask_nav
- flask_bootstrap
- flask_sqlalchemy
- flask_wtf
- flask_admin (optional: only required for the admin interface)
- flask_login (optional: only required for the admin interface)
- WTForms
- uwsgi (optional: only for deploying with WSGI)

## Installation

1. Clone this repository.
2. Install the dependencies via `pip install -U -r requirements.txt`
3. Rename `PyQdbS/config.example.py` to `PyQdbS/config.py` and edit the config. See the [Configruation](#Configuration).
3. Run `$ export FLASK_APP=pyqdbs.py`
4. Initialize the database. You can run `flask initdb` to do this. If you are using the admin interface, run `flask admin` to create the admin user and password.

:warning:Change the SECRET_KEY in the config or sessions will not be secure, as they are cryptographically signed by Flask.:warning:

### Configuration

Edit the ProductionConfig class in `PyQdbS/config.py` and read the comments on each line to understand how each option works.
If you choose to use PostgreSQL you'll need to create a user and a database before `flask initdb` will work.

#### Creating a PostgreSQL database

PostgreSQL configurations differs on each OS, so this might not work on your distribution. Use Google if this doesn't work on your distro.
To create a user, run the following commands from a root prompt.

If you wish to use PostgreSQL you need to install `pyscopg2` from pip, which is included in requirements.txt.

```
# su - postgres
$ createuser qdbs
$ createdb -O qdbs qdbs
```

After following the above steps,

### Deploying

There are a few options for deploying this. To understand all the available methods, see the [Flask Deploying Options](http://flask.pocoo.org/docs/0.12/deploying/).
For self-hosting, I recommend the [nginx](http://flask.pocoo.org/docs/0.12/deploying/fastcgi/#configuring-nginx) WSGI method.

A reverse proxy will work, but is not a good idea.

#### WSGIServer

This assumes you have PyQdbS installed as a 'qdbs' user with a $HOME of `/var/lib/qdbs`, and the PyQdbS repository at `/var/lib/qdbs/pyqdbs/`.

I recommend using nginx with the uwsgi protocol.

The following command in the root directory of the PyQdbS repo should work. You can adjust the mount point to "/quotes" instead of "/", or anything else you desire.
Since nginx and PyQdbS run in separate processes, I put the nginx user in a a group with the PyQdbS user, and give the uwsgi.sock file a umask of 0770.

```
$ uwsgi -s /var/lib/qdbs/uwsgi.sock --manage-script-name --mount /=pyqdbs:app
$ chmod 0770 /var/lib/qdbs/uwsgi.sock

```
You'll want your nginx config locations to look something like this within your `server { }` block.

```
location / {
    try_files $uri @pyqdbs;
}

location @pyqdbs {

    include         uwsgi_params;
    uwsgi_pass      unix:/var/lib/qdbs/uwsgi.sock;
}

```

## reCAPTCHA

If you would like to use reCAPTCHA with PyQdbS, you need to register with Google, and set the following settings in your config.py file.

| Setting               |            | Description                                                                             |
| ----------------------|------------|-----------------------------------------------------------------------------------------|
| RECAPTCHA_PUBLIC_KEY  | *required* | A public key.                                                                           |
| RECAPTCHA_PRIVATE_KEY | *required* | A private key.                                                                          |
| RECAPTCHA_API_SERVER  | optional   | Specify your Recaptcha API server.                                                      |
| RECAPTCHA_PARAMETERS  | optional   | A dict of JavaScript (api.js) parameters.                                               |
| RECAPTCHA_DATA_ATTRS  | optional   | A dict of data attributes options. https://developers.google.com/recaptcha/docs/display |

This table is from the Flask-WTF documentation page [here](https://flask-wtf.readthedocs.io/en/latest/form.html#recaptcha).
You can see more settings for the HTML forms in this application [here](https://flask-wtf.readthedocs.io/en/latest/config.html).

## Admin

The admin interface is enabled by default, and can be disabled by setting `PQYDBS_ENABLE_ADMIN` to False. Use the command `flask admin` to create an administrator user. The password will be printed out. If you forget the password, you can re-run `flask admin`.

## API

PyQdbS supports quote retrieval.

## Notice

This is my first time working with Flask and Bootstrap. If you have any suggestions, or anything I'm doing is Not The Right Thing To Do, please open an issue.

## TODO

Some goals for the project.

- [X] Anti-Spam
- [X] Admin feature (editing, deleting)
  - [X] Set admin password after logging in
- [ ] Quote approval *
- [ ] Upvote / Downvote *
- [ ] Auto-remove timestamps from Add Quote
- [X] RESTful API, probably Flask-Rest
  - [ ] Authenticate adding quotes via an API key
- [ ] Hidden Quotes  *
- [X] Convert forms to use macros provided by `bootstrap/wtf.html`
- [X] Multiple database backend support (via SQLAlchemy/flask_sqlalchemy)
- [X] Pagination support through the use of SQLAlchemy

* = will break SQL schema
