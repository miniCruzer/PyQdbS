from flask_restful import Resource, Api
from flask_restful import reqparse

import flask_login

from PyQdbS import utils
from PyQdbS import quotemgr
from PyQdbS.auth import login_manager

api = Api()

QuoteAddedSuccess   = { "result": "success" }
QuoteInvalid        = { "result": "failure", "reason": "invalid quote format" }
QuoteNotFound       = { "result": "failure", "reason": "no such quote" }

InvalidToken        = { "result": "failure", "reason": "invalid token" }

class QuoteResource(Resource):
    def get(self, quote_id):
        q = quotemgr.get_quote_id(quote_id)
        if not q:
            return QuoteNotFound
        return q.serialize()

class QuoteRandomResource(Resource):
    def get(self):
        q = quotemgr.get_quote_random()
        if not q:
            return QuoteNotFound
        return q.serialize()

required_args = ( "channel", "nickname", "quote", "token" )
parser = reqparse.RequestParser()
[ parser.add_argument(arg) for arg in required_args ]

def is_valid_quote(candidate):

    for arg in required_args:
        if arg not in candidate:
            return False

    for v in candidate.values():
        if not v:
            return False
    return True

def ensure_no_color(candidate):
    for k, v in candidate.items():
        candidate[k] = utils.strip_color(v)

class QuoteAddResource(Resource):
    @flask_login.login_required
    def post(self):
        args = parser.parse_args()

        if not is_valid_quote(args):
            return QuoteInvalid

        ensure_no_color(args)
        quotemgr.add_quote(args['channel'], args['nickname'], args['quote'])

        return QuoteAddedSuccess, 201

class GetToken(Resource):
    def post(self):
        pass

api.add_resource(QuoteResource, "/api/quotes/id/<int:quote_id>")
api.add_resource(QuoteRandomResource, "/api/quotes/random")
api.add_resource(QuoteAddResource, "/api/quotes/add")
