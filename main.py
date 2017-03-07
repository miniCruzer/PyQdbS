import os, sqlite3

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import g

from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap

import forms
import utils

app = Flask(__name__)
Bootstrap(app)

# loads default config, then gets overriden with some
# hard coded defaults, which than then be overriden
# with the config file pointed to by PYQDBS_SETTINGS

app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "qdbs.db")
))
app.config.from_envvar("PYQDBS_SETTINGS", silent=False)

nav = Nav()
nav.register_element("top", Navbar(
    "PyQdbS",
    View("Hello", 'hello'),
    View("Add a Quote", 'add_quote'),
    View("Show Quotes", 'show_quotes'),

    Subgroup("Other Stuff",
        Link("GitHub", "https://github.com/miniCruzer/PyQdbS"),
        Link("AlphaChat", "https://www.alphachat.net/"),
        Link("Shitposted", "https://shitposted.com/"),
    )
))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command("initdb")
def initdb_command():
    init_db()
    print("database initialized")


def add_quote_fromform(form):

    chan = form.channel.data
    nick = form.nick.data
    text = form.quote.data

    if utils.has_color(text):
        text = utils.strip_color(text)

    db = get_db()
    db.execute("insert into quotes (channel, nickname, quote) values (?, ?, ?)", (chan, nick, text))
    db.commit()


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/add", methods=[ "GET", "POST" ])
def add_quote():

    form = forms.AddQuote(request.form)

    if request.method == 'POST' and form.validate():
        add_quote_fromform(form)
        flash("Your quote has been submitted.")
        return redirect(url_for("add_quote"))
    else:   
        return render_template("add_quote.html", form=form)

def get_channels():
    db = get_db()
    cu = db.execute("select distinct channel from quotes")
    channels = [ chan[0] for chan in cu.fetchall() ]
    return channels

def get_submitters():
    db = get_db()
    cu = db.execute("select distinct nickname from quotes")
    submitter = [ nick[0] for nick in cu.fetchall() ]
    return submitter

@app.route("/quotes")
def show_quotes():
    db = get_db()
    cu = db.execute("select id, channel, nickname, timestamp, quote from quotes")
    quotes = cu.fetchall()

    return render_template("list_quotes.html", quotes=quotes, channels=get_channels(), submitters=get_submitters())

@app.route("/quotes/id/<int:quote_id>")
def show_quote_id(quote_id):
    db = get_db()
    cu = db.execute("select id, channel, nickname, timestamp, quote from quotes where id=?", (quote_id,))
    quotes = cu.fetchall()

    return render_template("list_quotes.html", quotes=quotes)

@app.route("/quotes/channel/<string:channel>")
def show_quote_channel(channel):
    if not channel.startswith('#'):
        channel = '#' + channel
    db = get_db()
    cu = db.execute("select id, channel, nickname, timestamp, quote from quotes where channel=?", (channel,))
    quotes = cu.fetchall()

    return render_template("list_quotes.html", quotes=quotes, criteria="from %s" % channel)

@app.route("/quotes/submitter/<string:nick>")
def show_quote_submitter(nick):
    db = get_db()
    cu = db.execute("select id, channel, nickname, timestamp, quote from quotes where nickname=?", (nick,))
    quotes = cu.fetchall()

    return render_template("list_quotes.html", quotes=quotes, criteria="submitted by %s" % nick)

nav.init_app(app)

if __name__ == "__main__":
        app.run()
