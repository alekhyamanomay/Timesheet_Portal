from flask_restx import Resource, cors, fields, reqparse
from werkzeug.exceptions import Unauthorized, UnprocessableEntity

from ... import APP, LOG
from ...encryption import Encryption
from ...helpers import randomStringwithDigitsAndSymbols, token_verify_or_raise, token_decode
from ...models import db,status
from ...models.users import User
from . import ns
import jwt

# from ...services.mail import send_email

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('userid', type=str, location='json', required=True)

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
    def post(self):
        args = parser.parse_args(strict=False)
        y = token_decode(args['Authorization'])
        
        if isinstance(y,tuple):
            return {"error":y[0]}, y[1]

        Email =  y['email']
        UserId = y['userid']
        token_verify_or_raise(args['Authorization'])
        # y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])
        
        # Email =  y['email']
        # UserId = y['userid']
            
        # token_verify_or_raise(args['Authorization'], Email, UserId )
        user = User.query.filter_by(UserId=args['userid']).first()
        if user is not None:
            UnprocessableEntity("User not found")
        user.Status= status.STATUS_INACTIVE
        db.session.commit()
        LOG.info("User %s Deleted Successfully, by %s", user.UserName)

        return {"result": "success", "error": None}
