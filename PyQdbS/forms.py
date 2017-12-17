from flask_wtf import FlaskForm, RecaptchaField
from wtforms import *


class TagListField(Field):

    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [ x.strip() for x in valuelist[0].split(',') ]
        else:
            self.data = [ ]

class BetterTagListField(TagListField):
    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(BetterTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item

class LoginForm(FlaskForm):
    username = StringField("Username", [ validators.required() ])
    password = PasswordField("Password", [ validators.required() ])
    submit = SubmitField('Submit')

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

    submit = SubmitField("Submit")

    tags = BetterTagListField(""
        , [ validators.optional() ]
        , description=u"Tags for this quote."
    )

    recaptcha = RecaptchaField()

class AddQuoteRecaptcha(AddQuote):
    recaptcha = RecaptchaField()

class SearchForm(FlaskForm):
    term = StringField("Search Term")
    submint = SubmitField("Search")
