import jwt
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, abort, current_app as app
from flask_restx import Resource, reqparse, fields
from ...helpers import randomStringwithDigitsAndSymbols, token_verify, token_verify_or_raise
from ...encryption import Encryption
from ...models import db, status, roles
from ...models.Users import User
from werkzeug.exceptions import Unauthorized, BadRequest, UnprocessableEntity, InternalServerError
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)


response_model = ns.model('GetGetProfileDetails', {
    "Username": fields.String,
    "DisplayName": fields.String,
    "Email": fields.String,
})


@ns.route("/profile/get/<Username>")
class GetProfileDetails(Resource):
    @ns.doc(description='Get profile details',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self, Username):
        args = parser.parse_args(strict=False)

        username = args['username']
        token = args["Authorization"]
        ip = args['Ipaddress']
        token_verify_or_raise(token, username, ip)
        try:
            users = Users.query.filter_by(Username=Username).first()
            if users is None:
                raise UnprocessableEntity("Not a valid username")
            return {
                       "Username": users.Username,
                       "DisplayName": users.DisplayName,
                       "Email": users.Email,
                   }, 200
        except UnprocessableEntity as e:
            LOG.error("Invalid Username", e)
            raise UnprocessableEntity("Not a valid username")
        except Exception as e:
            LOG.error("Exception while fetching profile details", e)
            raise InternalServerError("Can't fetch profile details")
