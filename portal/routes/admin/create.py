# from http.client import CREATED
from flask_restx import Resource, cors, fields, reqparse
from werkzeug.exceptions import Unauthorized, UnprocessableEntity

from ... import APP, LOG
from ...encryption import Encryption
from ...helpers import randomStringwithDigitsAndSymbols, token_verify_or_raise, _SendEmail
from ...models import db,status
from ...models.users import User
from . import ns
import jwt

# from ...services.mail import send_email

parser = reqparse.RequestParser()
# parser.add_argument('Authorization', type=str,
#                     location='headers', required=True)
parser.add_argument('UserId', type=str, location='json', required=True)
parser.add_argument('newuser', type=str, location='json', required=True)
parser.add_argument('NewUserId', type=str, location='json', required=True)
parser.add_argument('Email', type=str, location='json', required=True)
parser.add_argument('Permission', type=str, location='json', required=True)
parser.add_argument('Manager', type=str, location='json', required=True)
parser.add_argument('ManagerEmail', type=str, location='json', required=True)
parser.add_argument('SecondaryManager', type=str, location='json', required=True)
parser.add_argument('Role', type=str, location='json', required=True)

response_model = ns.model('PostUserCreate', {
    'result': fields.String,
    'error': fields.String,
})


@ns.route("/create")
class CreateUser(Resource):
    @ns.doc(description='Create New User',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=False)
    @ns.marshal_with(response_model)
    def post(self):
        
        args = parser.parse_args(strict=False)
        # token_verify_or_raise(args['Authorization'], args['username'])
        
        user = User.query.filter_by(Email=args["Email"]).first()
        if user is not None:
            return {"result": "failure", "error": "user exists with this email"}, 400
        Password = args['UserId']
        enc_pass = Encryption().encrypt(Password)
        usermodel = User(UserName=args['newuser'],
                          UserId = args['NewUserId'],
                          Password=enc_pass,
                          Email=args['Email'],
                          Status= status.STATUS_ACTIVE,
                          Role=args['Role'],
                          Permission = args['Permission'],
                          Manager = args['Manager'],
                          SecondaryManager = args['SecondaryManager'],
                          SecondaryManagerEmail = args['SecondaryManagerEmail'],
                          ManagerEmail = args['ManagerEmail']
                          )
        
        # Notify the user the creation of his Account with Temporary Password
        subject = f"Welcome {args['newuser']}"
        body = f'''<H1>Hello {args['newuser']} Welcome To EASY LIFE</H1>
                    <p>Your Account is Created, with the following credentials</p>
                    <p>User Name : {args['newuser']}</p>
                    <p>Password : {Password}</p>
                    <p>Please Click on this <a href={APP.config["FRONTEND_URL"]}>link</a> or  copy paste this {APP.config["FRONTEND_URL"]}</p>
                '''
        cc = []
        toaddress= [args['Email']]
        if len(toaddress):
            _SendEmail(body=body,subject=subject,cc=cc,to_address=toaddress)
        else:
            LOG.error("CREATE USER : MAIL NOT SEND DUE TO NO TO ADDRESS GIVEN")
            UnprocessableEntity("Cannot Send Mail")
        # Mail to be sent here with the password we created
        
        db.session.add(usermodel)
        db.session.commit()
        LOG.info("The Password for user %s is : %s", args['newuser'], Password)

        return {"result": "success", "error": None}
