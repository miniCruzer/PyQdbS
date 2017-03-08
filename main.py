import os

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
from flask_sqlalchemy import SQLAlchemy

import forms
import utils

app = Flask(__name__)
Bootstrap(app)

# loads default config, then gets overriden with some
# hard coded defaults, which than then be overriden
# with the config file pointed to by PYQDBS_SETTINGS

app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI="sqlite:////" + os.path.join(app.root_path, "qdbs.db")
))
app.config.from_envvar("PYQDBS_SETTINGS", silent=False)
db = SQLAlchemy(app)

class Quotes(db.Model):

    # id, channel, nickname, timestamp, quote

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nickname = db.Column(db.String())
    channel = db.Column(db.String())
    quote = db.Column(db.String())
    timestamp = db.Column(db.DateTime())
    #score = db.Column('score', db.Integer)

    def __init__(self, channel, nickname, quote):
        self.channel = channel
        self.nickname = nickname
        self.quote = quote

    def __repr__(self):
        return "<Quote %i>" % self.id

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


@app.cli.command("initdb")
def initdb_command():
    db.create_all()
    print("database initialized")


def add_quote_fromform(form):

    text = form.quote.data

    if utils.has_color(text):
        text = utils.strip_color(text)

    q = Quotes(form.channel.data, form.nick.data, text)

    db.session.add(q)
    db.session.commit()


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
    q = db.session.query(Quotes.channel.distinct().label("channel"))
    for c in q.all():
        yield c[0]

def get_submitters():
    q = db.session.query(Quotes.nickname.distinct().label("nick"))
    for s in q.all():
        yield s[0]

@app.route("/quotes")
def show_quotes():
    return render_template("list_quotes.html", quotes=Quotes.query.all(), channels=get_channels(), submitters=get_submitters())

@app.route("/quotes/id/<int:quote_id>")
def show_quote_id(quote_id):
    return render_template("list_quotes.html", quotes=[ Quotes.query.get(quote_id) ])

@app.route("/quotes/channel/<string:channel>")
def show_quote_channel(channel):
    q = Quotes.query.filter(Quotes.channel == channel)
    return render_template("list_quotes.html", quotes=q.all(), criteria="from %s" % channel)

@app.route("/quotes/submitter/<string:nick>")
def show_quote_submitter(nick):
    q = Quotes.query.filter(Quotes.nickname == nick)
    return render_template("list_quotes.html", quotes=q.all(), criteria="submitted by %s" % nick)

nav.init_app(app)

if __name__ == "__main__":
        app.run()
