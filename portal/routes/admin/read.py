from flask_restx import Resource, reqparse, fields
from ...helpers import token_verify_or_raise
from ...models import db
from ...models.Users import User
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
from . import ns
from ... import LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
# parser.add_argument('Ipaddress', type=str, location='headers', required=True)

response_model_child = ns.model('GetGetEmployerMemberRelationChild', {
    "UserNo": fields.String,
    "UserName": fields.String,
    "Email": fields.String,
    "PhoneNumber": fields.String,
    "DisplayName": fields.String,
    "Role": fields.String,
    "Status": fields.String
})

response_model = ns.model('GetUsers', {
    "users": fields.List(fields.Nested(response_model_child))
})


@ns.route("/users/get")
class GetUsers(Resource):
    @ns.doc(description='Get profile details',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    # @ns.marshal_with(response_model)
    def get(self):
        args = parser.parse_args(strict=False)
        username = args['username']
        token = args["Authorization"]
        # ip = args['Ipaddress']
        token_verify_or_raise(token, username)
        users = User.query.all()
        # print(users)
        response = []
        for user in users:
            print(user.Username)
            response.append({
                "UserNo": user.UserID,
                "UserName": user.Username,
                "Email": user.Email,
                "DisplayName": user.Manger,
                "PhoneNumber": user.ManagerEmail,
                "Role": user.Role,
                "Status": user.Status,
            }
            )
        return {"users": response}, 200
