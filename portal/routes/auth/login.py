import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.jwttokenblacklist import JWTTokenBlacklist
from ...models import status, roles
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, location='json', required=True)
parser.add_argument('password', type=str, location='json', required=True)

response_model = ns.model('GetLogin', {
    'username':fields.String,
    'email': fields.String,
    'userid': fields.String,
    'role': fields.String,
    'temppassword':fields.Boolean,
    'token': fields.String,
})


@ns.route('/login')
class Login(Resource):
    @ns.doc(description='Login',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args(strict=True)
        Email = args['email']
        password = args['password']

        encrypt_password = Encryption().encrypt(password)
        try:
            print(Email, encrypt_password)
            userinfo = User.query.filter_by(Email=Email, Password=encrypt_password).first()
            if userinfo is None:
                LOG.debug("Auth failed. Username (%s) or Password is wrong", Email)
                raise UnprocessableEntity('Username or Password is incorrect.')

            if (userinfo.Status == status.STATUS_INACTIVE):
                LOG.debug("Auth failed. User is not active. Username:%s, status:%s, role:%s" % (userinfo.UserName, userinfo.Status, userinfo.Role))
                raise UnprocessableEntity('User is not active')
            
            role = userinfo.Role
            # token_create = datetime.utcnow()
            # exp = datetime.utcnow() + timedelta(hours=1, minutes=30)
            exp = datetime.utcnow() + timedelta(seconds=10)
            payload = {
                'username': userinfo.UserName,
                'email': userinfo.Email,
                'userid':userinfo.UserId,
                # 'token_create': token_create,
                'exp': exp,
                'role': role,
            }
            # print("payload - JWT Token",payload)
            token = jwt.encode(key=APP.config['JWT_SECRET'], algorithm='HS256', payload=payload )

            token = token.decode('utf-8')
            LOG.debug('User %s authenticated successfully', userinfo.UserName)
            return {
                "username": userinfo.UserName,
                "userid":userinfo.UserId,
                "email": userinfo.Email,
                "role": role,
                "temppassword":userinfo.TemporaryPassword,
                'token': str(token)
            }

        except Exception as e:
            LOG.warning('Exception happened during authenticating user: %s', e)
            raise InternalServerError(e)
