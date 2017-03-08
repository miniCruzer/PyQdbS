from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
db = SQLAlchemy()

class Quotes(db.Model):

    # id, channel, nickname, timestamp, quote

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nickname = db.Column(db.String())
    channel = db.Column(db.String())
    quote = db.Column(db.String())
    timestamp = db.Column(db.DateTime(), server_default=func.now())
    #score = db.Column('score', db.Integer)

    def __init__(self, channel, nickname, quote):
        self.channel = channel
        self.nickname = nickname
        self.quote = quote

    def __repr__(self):
        return "<Quote %i>" % self.id
