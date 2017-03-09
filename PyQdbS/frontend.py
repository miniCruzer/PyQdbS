import os

from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for

from flask import current_app

from PyQdbS import forms
from PyQdbS import utils
from PyQdbS.models import Quotes, db

frontend = Blueprint("frontend", __name__)

def add_quote_fromform(form):

    text = form.quote.data

    if utils.has_color(text):
        text = utils.strip_color(text)

    q = Quotes(form.channel.data, form.nick.data, text)

    db.session.add(q)
    db.session.commit()


@frontend.route("/")
def hello():
    return render_template("index.html")

@frontend.route("/add", methods=[ "GET", "POST" ])
def add_quote():

    if current_app.config["PYQDBS_ENABLE_RECAPTCHA"]:
        form = forms.AddQuoteRecaptcha(request.form)
    else:
        form = forms.AddQuote(request.form)

    if request.method == 'POST' and form.validate():
        print("POST")
        add_quote_fromform(form)
        flash("Your quote has been submitted.")
        return redirect(url_for("frontend.add_quote"))
    else:   
        return render_template("add_quote.html", form=form)

def get_channels():
    q = db.session.query(Quotes.channel.distinct())
    for c in q.all():
        yield c[0]

def get_submitters():
    q = db.session.query(Quotes.nickname.distinct())
    for s in q.all():
        yield s[0]

@frontend.route("/quotes/")
def redir_to_page():
    return redirect(url_for('frontend.show_quotes', page=1))

@frontend.route("/quotes/page/<int:page>")
def show_quotes(page=1):
    return render_template("list_quotes.html", quotes=Quotes.query.paginate(page, current_app.config['PQYDBS_QUOTES_PER_PAGE']), 
        channels=get_channels(), submitters=get_submitters())

@frontend.route("/quotes/id/<int:quote_id>")
def show_quote_id(quote_id):
    return render_template("list_quotes.html", quotes=Quotes.query.paginate(1, 1), channels=get_channels(), submitters=get_submitters())

@frontend.route("/quotes/channel/<string:channel>")
@frontend.route("/quotes/channel/<string:channel>/page/<int:page>")
def show_quote_channel(channel, page=1):
    q = Quotes.query.filter(Quotes.channel == channel)
    return render_template("list_quotes.html", quotes=q.paginate(page, current_app.config['PQYDBS_QUOTES_PER_PAGE']),
        criteria="from %s" % channel, channels=get_channels(), submitters=get_submitters())

@frontend.route("/quotes/submitter/<string:nick>")
@frontend.route("/quotes/submitter/<string:nick>/page/<int:page>")
def show_quote_submitter(nick, page=1):
    q = Quotes.query.filter(Quotes.nickname == nick)
    return render_template("list_quotes.html", quotes=q.paginate(page, current_app.config['PQYDBS_QUOTES_PER_PAGE']),
        criteria="submitted by %s" % nick, channels=get_channels(), submitters=get_submitters())

