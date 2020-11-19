import jwt
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, abort
from flask_restx import Resource, reqparse, cors, fields
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, UnprocessableEntity, InternalServerError
from ....helpers import randomStringwithDigitsAndSymbols, token_verify_or_raise, RESPONSE_OK
from ....encryption import Encryption
from ....models import db
from ....models.users import User
from ....services.mail import send_email
from .. import ns
from .... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('request_type', type=str, location='json', required=True,
                    help='Accepted Values: [Admin|SecurityQuestion|Email]')
parser.add_argument('UserId', type=str, location='json', required=True)
parser.add_argument('Email', type=str, location='json', required=False)

response_model = ns.model('PostPasswordReset', {
    'result': fields.String,
})


def _change_password(email, UserId):
    try:
        password = randomStringwithDigitsAndSymbols()
        pass_encrypt = Encryption().encrypt(password)
        message = f'<p>Dear {username}</p>' + \
                  f'<p>Username is {username}</p>' + \
                  f'<p>Your password has been reset.</p>' + \
                  f'<p>The temporary password is: <b style="color:red">{password}</b></p>'

        user = User.query.filter_by(UserId=UserId).first()
        user.Password = pass_encrypt
        db.session.commit()

        send_email(to_address=email, subject='Reset Password', body=message)
        return RESPONSE_OK

    except Exception as e:
        LOG.warning('Unexpected error happened during changing password: %s', e)
        raise InternalServerError()


@ns.route("/password/reset")
class PasswordReset(Resource):
    @ns.doc(description='Reset Password',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 422: 'UnprocessableEntity',
                       500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    def post(self):
        args = parser.parse_args(strict=False)
        y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])
        
        Email =  y['email']
        UserId = y['userid']
            
        token_verify_or_raise(args['Authorization'], Email, UserId )

        user = User.query.filter_by(UserId=args[UserId]).first()
        if user is None:
            raise UnprocessableEntity('User not found')

        if user.Email is None:
            raise UnprocessableEntity("Please contact administrator for password reset "
                                      "Since your EmailID is not available in the system")

        return _change_password(Email, UserId)
