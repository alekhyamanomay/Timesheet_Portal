from flask_restx import Resource, reqparse, fields
from ...helpers import token_verify_or_raise
from ...models import db
from ...models.users import User
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
from . import ns
from ... import LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)

response_model_child = ns.model('GetGetEmployerMemberRelationChild', {
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

response_model = ns.model('GetUsers', {
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
        username = args['username']
        token = args["Authorization"]
        # ip = args['Ipaddress']
        token_verify_or_raise(args['Authorization'], Email, UserID )
        users = User.query.all()
        # print(users)
        response = []
        for user in users:
            print(user.Username)
            response.append({
                "userid": user.UserID,
                "username": user.Username,
                "email": user.Email,
                "manger": user.Manger,
                "manageremail": user.ManagerEmail,
                "secondarymanager": user.SecondaryManager,
                "secondarymanageremail": user.SecondaryManagerEmail,
                "role": user.Role,
                "status": user.Status,
            }
            )
        return {"users": response}, 200
