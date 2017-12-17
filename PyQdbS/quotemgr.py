from sqlalchemy.sql.expression import func

from PyQdbS import utils
from PyQdbS.models import Quotes, db


def add_quote(chan, nick, quote):

    db.session.add(Quotes(chan, nick, quote))
    db.session.commit()

def add_quote_fromform(form):

    text = form.quote.data

    if utils.has_color(text):
        text = utils.strip_color(text)

    text = utils.remove_timestamps(text)

    add_quote(form.channel.data, form.nick.data, text)

def get_quote_id(quote_id):
    return Quotes.query.get(quote_id)

def get_quote_random():
    return Quotes.query.order_by(func.random()).first()

def get_channels():
    q = db.session.query(Quotes.channel.distinct())
    for c in q.all():
        yield c[0]

def get_submitters():
    q = db.session.query(Quotes.nickname.distinct())
    for s in q.all():
        yield s[0]

def get_quotes_for_channel(channel):
    return Quotes.query.filter(Quotes.channel == channel)

def get_quotes_for_nick(nick):
    return Quotes.query.filter(Quotes.nickname == nick)
