from flask_restx import Resource, reqparse, fields
from ...helpers import token_verify_or_raise
from ...models import db
from ...models.users import User
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
from . import ns
from ... import LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)
parser.add_argument('email', type=str, location='json', required=True)
parser.add_argument('displayname', type=str, location='json', required=True)
parser.add_argument('phonenumber', type=str, location='json', required=True)

post_response_model = ns.model('PostProfileDetails', {
    'result': fields.String,
})

@ns.route("/profile/update")
class UpdateProfileDetails(Resource):
    @ns.doc(description='Get profile details',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(post_response_model)
    def post(self):
        args = parser.parse_args(strict=False)
        username = args['username']
        token = args["Authorization"]
        ip = args['Ipaddress']
        token_verify_or_raise(token, username, ip)
        try:
            user = Users.query.filter_by(Username=username).first()
            if user is None:
                UnprocessableEntity("user is not Available")
            user.Email = args["email"]
            user.DisplayName = args["displayname"]
            user.PhoneNumber = args["phonenumber"]
            db.session.commit()
            return {"result": "success"}, 200
        except Exception as e:
            LOG.error("Exception while updating profile details", e)
            raise InternalServerError("Can't update profile details")
