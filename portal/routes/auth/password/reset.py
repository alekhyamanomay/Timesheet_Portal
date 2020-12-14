import jwt
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, abort
from flask_restx import Resource, reqparse, cors, fields
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, UnprocessableEntity, InternalServerError
from ....helpers import randomStringwithDigitsAndSymbols, RESPONSE_OK,_SendEmail
from ....encryption import Encryption
from ....models import db,status
from ....models.users import User
# from ....services.mail import send_email
from .. import ns
from .... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Email', type=str, location='json', required=True)

response_model = ns.model('PostPasswordReset', {
    'result': fields.String,
})


def _change_password(user):
    try:
        
        password = randomStringwithDigitsAndSymbols()
        pass_encrypt = Encryption().encrypt(password)
        user.Password = pass_encrypt
        user.TemporaryPassword = True
        message = f'<p>Dear {user.UserName}</p>' + \
                  f'<p>Your password has been reset.</p>' + \
                  f'<p>Please use this below temporary password to login. <p>'+\
                  f'<p>Password: <b style="color:red">{password}</b></p>'

        db.session.commit()
        cc= []
        _SendEmail(body=message,subject='Reset Password',cc=cc,to_address=[user.Email])
        # send_email(to_address=Email, subject='Reset Password', body=message)
        print("mail sent")
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
        if args['Email'][-11:] != "manomay.biz":
            return {"result": "failure", "error": "This mail can't request for reset password"}, 400
        user = User.query.filter_by(Email = args['Email']).first()
        if user is None:
            return {"result": "failure", "error": "User doesn't exists with this email"}, 400
        if user.Status == status.STATUS_INACTIVE:
            return {"result": "failure", "error": "User is deactivated"}, 400
        return _change_password(user)
