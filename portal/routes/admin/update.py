from flask_restx import Resource, reqparse, fields
from ...helpers import token_verify_or_raise
from ...models import db
from ...models.Users import User
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
from . import ns
from ... import LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('UserId', type=str, location='headers', required=True)
parser.add_argument('email', type=str, location='json', required=True)
parser.add_argument('Manager', type=str, location='json', required=True)
parser.add_argument('ManagerEmail', type=str, location='json', required=True)
parser.add_argument('role', type=str, location='json', required=True)
parser.add_argument('status', type=str, location='json', required=True)

post_response_model = ns.model('PostProfileDetails', {
    'result': fields.String,
})

@ns.route("/update")
class UpdateUser(Resource):
    @ns.doc(description='Get profile details',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(post_response_model)
    def post(self):
        args = parser.parse_args(strict=False)
        username = args['username']
        token = args["Authorization"]
        UserId = args['UserId']
        token_verify_or_raise(token, username)
        try:
            user = User.query.filter_by(UserId=UserId).first()
            if user is None:
                UnprocessableEntity("user is not Available")
            user.Email = args["email"]
            user.Manager = args["Manager"]
            user.ManagerEmail = args["ManagerEmail"]
            user.SecondaryManager = args['SecondaryManager']
            user.Role = args["role"]
            user.Status = args["status"]
            db.session.commit()
            return {"result": "success"}, 200
        except Exception as e:
            LOG.error("Exception while updating user details", e)
            raise InternalServerError("Can't update user details")
