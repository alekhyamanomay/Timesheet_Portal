import jwt
import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, jsonify, request, abort, current_app as app
from flask_restx import Resource, reqparse, cors, fields
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, UnprocessableEntity, InternalServerError
from ....helpers import randomStringwithDigitsAndSymbols, token_verify_or_raise
from ....encryption import Encryption
from ....models import db
from ....models.Users import User
from ....models.security_question import SecurityQuestion
from .. import ns
from .... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
# parser.add_argument('Ipaddress', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('user', type=str, location='json', required=True)
parser.add_argument('oldPassword', type=str, location='json', required=True)
parser.add_argument('newPassword', type=str, location='json', required=True)

response_model = ns.model('PostPasswordChange', {
    'result': fields.String,
})

@ns.route("/password/change")
class PasswordChange(Resource):
    @ns.doc(description='Change Password',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 422: 'UnprocessableEntity',
                       500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args(strict=False)
        token = token_verify_or_raise(token=args["Authorization"], user=args["username"])

        # TODO:
        # Verify the role from token before proceeding with password chanaging

        UserId = args["UserId"]
        old_pass = args["oldPassword"]
        new_pass = args["newPassword"]
        try:
            user = User.query.filter_by(UserId=UserId).first()
            if user is None:
                raise UnprocessableEntity('Username is not valid')

            if user.Password != Encryption().encrypt(old_pass):
                raise BadRequest('Old Password is wrong')
            new_password = Encryption().encrypt(new_pass)
            user.Password = new_password
            db.session.commit()
            return {"result": "Password changed successfully"}, 200

        except KeyError as e:
            print(e)
            raise InternalServerError()
