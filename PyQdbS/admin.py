from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort
from flask import current_app

from wtforms import TextAreaField, validators

import flask_login

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from PyQdbS.auth import Users
from PyQdbS.auth import BcryptPasswordField
from PyQdbS.forms import LoginForm
from PyQdbS.models import Quotes, db

class PyQdbSQuoteModelView(ModelView):

    can_export = True

    column_searchable_list = [ 'quote' ]
    column_filters = [ 'channel', 'nickname' ]
    column_editable_list = [ 'channel', 'nickname' ]

    form_exclude_list = [ 'timestamp' ]
    form_excluded_columns = [ 'timestamp' ]
    form_overrides = {

        'quote': TextAreaField
    }

    form_args = {

        'channel': { 'validators' : [ validators.required() ] },
        'nickname': { 'validators' : [ validators.required() ] },
        'quote': { 'validators' : [ validators.required() ] }
    }

    form_widget_args = {

        'channel': { 'cols': 50 },
        'nickname': { 'cols': 50 },
        'timestamp': { 'cols': 50 },

        'quote': {
            'rows': 20,
            'cols': 50,
            'style': 'font-family: monospace;'

        },
    }

    def is_accessible(self):
        return flask_login.current_user.is_authenticated

class PyQdbSUserModelView(ModelView):

    form_overrides = {

        'password': BcryptPasswordField
    }

    form_args = {

        'username': { 'validators': [ validators.required() ]}
    }

    column_labels = {
        'allow_api': 'Allow API?',
        'is_admin': 'Is Admin?'
    }

    column_descriptions = {

        'allow_api': 'Allow the user to add qutoes via the API endpoint?',
        'is_admin': 'Allow the user to login to the admin panel?'
    }

    # allow inline editing of the following fields
    column_editable_list = 'username', 'is_admin', 'allow_api'

    # don't show the password hash
    column_exclude_list = 'password', 'session_token'

    # don't edit/create a session token
    form_excluded_columns = 'session_token'

    def on_model_change(self, form, model, is_created):
        prev = model.session_token
        model.make_session_token()
        new = model.session_token
        current_app.logger.debug("created a new session token for {}. {} -> {}".format(model, prev, new))


    def is_accessible(self):
        return flask_login.current_user.is_authenticated

class PyQdbSAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        return super(PyQdbSAdminIndexView, self).index()

    @expose('/login/', methods=[ 'GET', 'POST' ])
    def login(self):
        form = LoginForm(request.form)

        if form.validate_on_submit():

            user = Users.query.filter(Users.username == form.username.data).first()

            if user and user.has_admin() and user.check_password(form.password.data):

                flask_login.login_user(user)

                return redirect(url_for('admin.index'))
            else:
                flash("Invalid username or password.")
                return redirect(url_for('admin.login'))

        self._template_args['form'] = form
        return super(PyQdbSAdminIndexView, self).index()

    @expose('/logout/')
    def logout(self):
        flask_login.logout_user()
        return redirect(url_for('admin.index'))


admin = Admin(index_view=PyQdbSAdminIndexView())
admin.add_view(PyQdbSQuoteModelView(Quotes, db.session))
admin.add_view(PyQdbSUserModelView(Users, db.session))

if __name__ == "__main__":
    print("""
     cruzr │ rlygd CRUD view https://puu.sh/uAuGF/77ebda8794.png
  Lucifer7 │ it's CRUD alright xD
  Lucifer7 │ jk it's cool
     cruzr │ wow how dare you insult me
     cruzr │ > = [
  Lucifer7 │ :((((""")

