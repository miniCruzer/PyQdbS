from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from wtforms import TextAreaField, validators

import flask_login

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from PyQdbS.auth import Users
from PyQdbS.auth import LoginForm
from PyQdbS.models import Quotes, db

class PyQdbSModelView(ModelView):

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

class PyQdbSAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        return super(PyQdbSAdminIndexView, self).index()

    @expose('/login/', methods=[ 'GET', 'POST' ])
    def login(self):
        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate():
            user = Users.query.filter(Users.username == form.username.data).first()
            if user and user.check_password(form.password.data):
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
admin.add_view(PyQdbSModelView(Quotes, db.session))

if __name__ == "__main__":
    print("""
     cruzr │ rlygd CRUD view https://puu.sh/uAuGF/77ebda8794.png
  Lucifer7 │ it's CRUD alright xD
  Lucifer7 │ jk it's cool
     cruzr │ wow how dare you insult me
     cruzr │ > = [
  Lucifer7 │ :((((""")

