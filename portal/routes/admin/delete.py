from flask_restx import Resource, cors, fields, reqparse
from werkzeug.exceptions import Unauthorized, UnprocessableEntity

from ... import APP, LOG
from ...encryption import Encryption
from ...helpers import randomStringwithDigitsAndSymbols, token_verify_or_raise
from ...models import db,status
from ...models.users import User
from . import ns

# from ...services.mail import send_email

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)

parser.add_argument('name', type=str, location='json', required=True)
parser.add_argument('UserId', type=str, location='json', required=True)

response_model = ns.model('PostUserCreate', {
    'result': fields.String,
    'error': fields.String,
})


@ns.route("/delete")
class DeleteUser(Resource):
    @ns.doc(description='Delete a User',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=False)
    @ns.marshal_with(response_model)
    def delete(self):
        args = parser.parse_args(strict=False)
        token_verify_or_raise(args['Authorization'], args['username'])
        user = User.query.filter_by(UserID=args['UserId'], UserName= args["name"]).first()
        if user is not None:
            UnprocessableEntity("User not found")
        user.Status= status.STATUS_INACTIVE
        db.session.commit()
        LOG.info("User %s Deleted Successfully, by %s", args["name"],args["username"])

        return {"result": "success", "error": None}
