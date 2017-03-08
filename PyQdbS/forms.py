from flask_wtf import FlaskForm, RecaptchaField
from wtforms import *

class AddQuote(FlaskForm):

    channel = StringField(""
        , [ validators.required() ]
        , description=u"The IRC channel this quote came from."
    )

    nick = StringField(""
        , [ validators.required() ]
        , description=u"YOUR nickname on IRC."
    )

    quote = TextAreaField(""
        , [ validators.required() ]
        , description=u"The actual quote that we're interested in."
    )

    recaptcha = RecaptchaField()

class AddQuoteRecaptcha(AddQuote):
    recaptcha = RecaptchaField()
