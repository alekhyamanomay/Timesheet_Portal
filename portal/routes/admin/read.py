from flask_restx import Resource, reqparse, fields
from ...helpers import token_verify_or_raise, token_decode
from ...models import db
from ...models.users import User
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
from . import ns
from ... import APP, LOG
import jwt

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)

response_model_child = ns.model('Getusersdata', {
    "userid": fields.String,
    "username": fields.String,
    "email": fields.String,
    "manager": fields.String,
    "manageremail": fields.String,
    "secondarymanager": fields.String,
    "secondarymanageremail": fields.String,
    "role": fields.String,
    "status": fields.String
})

response_model = ns.model('GetUsersData', {
    "users": fields.List(fields.Nested(response_model_child))
})


@ns.route("/users/get")
class GetUsers(Resource):
    @ns.doc(description='Get profile details',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self):
        args = parser.parse_args(strict=False)

        y = token_decode(args['Authorization'])
        
        if isinstance(y,tuple):
            return {'message':"Unathorized token"}, 401

        Email =  y['email']
        UserId = y['userid']
        token_verify_or_raise(args['Authorization'])

        users = User.query.all()
        response = []
        for user in users:
            response.append({
                "userid": user.UserId,
                "username": user.UserName,
                "email": user.Email,
                "manager": user.Manager,
                "manageremail": user.ManagerEmail,
                "secondarymanager": user.SecondaryManager,
                "secondarymanageremail": user.SecondaryManagerEmail,
                "role": user.Role,
                "status": user.Status,
            }
            )
        return {"users": response}, 200
