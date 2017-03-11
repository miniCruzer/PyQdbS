import os

from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for

from flask import current_app

from PyQdbS import forms
from PyQdbS import quotemgr
from PyQdbS.models import Quotes

frontend = Blueprint("frontend", __name__)

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
        quotemgr.add_quote_fromform(form)
        flash("Your quote has been submitted.")
        return redirect(url_for("frontend.add_quote"))
    else:
        return render_template("add_quote.html", form=form)

@frontend.route("/quotes/")
def redir_to_page():
    return redirect(url_for('frontend.show_quotes', page=1))

@frontend.route("/quotes/page/<int:page>")
def show_quotes(page=1):
    return render_template("list_quotes.html", quotes=Quotes.query.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE']),
        channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/id/<int:quote_id>")
def show_quote_id(quote_id):
    q = quotemgr.get_quote_id(quote_id)
    return render_template("list_quotes.html", quotes=q, channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/channel/<string:channel>")
@frontend.route("/quotes/channel/<string:channel>/page/<int:page>")
def show_quote_channel(channel, page=1):
    q = quotemgr.get_quotes_for_channel(channel)
    return render_template("list_quotes.html", quotes=q.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE']),
        criteria="from %s." % channel, channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/submitter/<string:nick>")
@frontend.route("/quotes/submitter/<string:nick>/page/<int:page>")
def show_quote_submitter(nick, page=1):
    q = quotemgr.get_quotes_for_nick(nick)
    return render_template("list_quotes.html", quotes=q.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE']),
        criteria="submitted by %s." % nick, channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/random")
def show_quote_random():
    q = quotemgr.get_quote_random()
    if not q:
        return render_template("list_quotes.html", quotes=[ ],
        channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

    i = q.id
    while i == current_app.config.get("PYQDBS_LAST_RANDOM_QUOTE", -1):
        q = quotemgr.get_quote_random()
        i = q.id

    current_app.config["PYQDBS_LAST_RANDOM_QUOTE"] = i

    return render_template("list_quotes.html", quotes=q,
        channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())
