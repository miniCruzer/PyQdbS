import os

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)

from PyQdbS import forms, quotemgr
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
    quotes = Quotes.query.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE'])
    return render_template("list_quotes.html", quotes=quotes, channels=quotemgr.get_channels(),
                           submitters=quotemgr.get_submitters())

@frontend.route("/quotes/id/<int:quote_id>")
def show_quote_id(quote_id):
    q = quotemgr.get_quote_id(quote_id)

    return render_template("list_quotes.html", quotes=q, channels=quotemgr.get_channels(),
                           submitters=quotemgr.get_submitters())

@frontend.route("/quotes/channel/<string:channel>")
@frontend.route("/quotes/channel/<string:channel>/page/<int:page>")
def show_quote_channel(channel, page=1):
    q = quotemgr.get_quotes_for_channel(channel)
    quotes = q.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE'])

    return render_template("list_quotes.html", quotes=quotes, criteria="from %s." % channel,
                           channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/submitter/<string:nick>")
@frontend.route("/quotes/submitter/<string:nick>/page/<int:page>")
def show_quote_submitter(nick, page=1):
    q = quotemgr.get_quotes_for_nick(nick)
    quotes = q.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE'])

    return render_template("list_quotes.html", quotes=quotes, criteria=f"submitted by {nick}.",
                           channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/random")
def show_quote_random():
    q = quotemgr.get_quote_random()
    if not q:
        return render_template("list_quotes.html", quotes=[ ],
                               channels=quotemgr.get_channels(),
                               submitters=quotemgr.get_submitters())

    i = q.id
    while i == current_app.config.get("PYQDBS_LAST_RANDOM_QUOTE", -1):
        q = quotemgr.get_quote_random()
        i = q.id

    current_app.config["PYQDBS_LAST_RANDOM_QUOTE"] = i

    return render_template("list_quotes.html", quotes=q,
        channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())

@frontend.route("/quotes/search/<string:term>/<int:page>")
def show_quotes_search(term, page=1):
    q = Quotes.query.filter(Quotes.quote.ilike(f"%{term}%"))
    pages = q.paginate(page, current_app.config['PYQDBS_QUOTES_PER_PAGE'])
    print(pages)

    return render_template("list_quotes.html", quotes=pages or [], criteria=f"matching {term!r}",
                           channels=quotemgr.get_channels(), submitters=quotemgr.get_submitters())


@frontend.route("/search", methods=["GET", "POST"])
@frontend.route("/search/<string:term>", methods=["GET", "POST"])
def search_quotes(term=None):

    form = forms.SearchForm(request.form)

    if request.method == 'POST' and form.validate():
        return redirect(url_for("frontend.show_quotes_search", term=form.term.data, page=1))

    return render_template("search.html", search_form=form)

