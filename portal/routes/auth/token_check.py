import jwt
import json
from flask import request
from flask_restx import Resource, reqparse, cors, fields
from werkzeug.exceptions import Unauthorized
from . import ns
from ... import APP
from ...helpers import token_verify_or_raise

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)


response_model = ns.model('PostTokenCheck', {
    "result": fields.Boolean,
})

@ns.route('/token/check')
class TokenCheck(Resource):
    @ns.doc(description='Validates the user token',
            responses={400: 'Bad Request', 401: 'Unauthorized', 200: 'OK'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args()

        auth = token_verify_or_raise(token=args["Authorization"], user=args["username"])

        if auth["username"] != args["username"]:
            raise Unauthorized()

        return {"result": True}
