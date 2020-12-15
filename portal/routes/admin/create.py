# from http.client import CREATED
from flask_restx import Resource, cors, fields, reqparse
from werkzeug.exceptions import Unauthorized, UnprocessableEntity
from ... import APP, LOG
from ...encryption import Encryption
from ...helpers import randomStringwithDigitsAndSymbols, token_verify_or_raise, _SendEmail, token_decode
from ...models import db,status
from ...models.users import User
from . import ns
import jwt

# from ...services.mail import send_email

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('newuser', type=str, location='json', required=True)
parser.add_argument('newuserid', type=str, location='json', required=True)
parser.add_argument('email', type=str, location='json', required=True)
parser.add_argument('manager', type=str, location='json', required=True)
parser.add_argument('manageremail', type=str, location='json', required=True)
parser.add_argument('secondarymanager', type=str, location='json', required=True)
parser.add_argument('secondarymanageremail', type=str, location='json', required=True)
parser.add_argument('role', type=str, location='json', required=True)

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
        y = token_decode(args['Authorization'])
        
        if isinstance(y,tuple):
            return {'message':"Unathorized token"}, 401

        token_verify_or_raise(args['Authorization'])
        try:
            user = User.query.filter((User.Email==args["email"]) | (User.UserId == args['newuserid'])).first()
            if user :
                LOG.debug("user exists with this email or employee id %s", args["email"])
                return {"result": "failure", "error": "user exists with this email or employee id"}, 400
            password = randomStringwithDigitsAndSymbols()
            pass_encrypt = Encryption().encrypt(password)
            
            usermodel = User(UserName=args['newuser'],
                            UserId = args['newuserid'],
                            Password=pass_encrypt,
                            Email=args['email'],
                            Status= status.STATUS_ACTIVE,
                            Role=args['role'],
                            Manager = args['manager'],
                            SecondaryManager = args['secondarymanager'],
                            SecondaryManagerEmail = args['secondarymanageremail'],
                            ManagerEmail = args['manageremail'],
                            TemporaryPassword	= True
                            )
            
            db.session.add(usermodel)
            db.session.commit()
            LOG.info("The Password for user %s is : %s", args['newuser'], password)
            
            # Notify the user the creation of his Account with Temporary Password
            subject = f"Welcome {args['newuser']}"
            body = f'''<p>Hi {args['newuser']} Welcome To Ts portal</p>
                        <p>Your Account has been Created, with the following credentials</p>
                        <p>User Name : {args['email']}</p>
                        <p>Password : {password}</p>
                        <p>Please Click on this <a href={APP.config["FRONTEND_URL"]}>link</a> or  copy paste this {APP.config["FRONTEND_URL"]}</p>
                    '''
            cc = []
            toaddress= [args['email']]
            if len(toaddress):
                _SendEmail(body=body,subject=subject,cc=cc,to_address=toaddress)
            else:
                LOG.error("CREATE USER : MAIL NOT SEND DUE TO NO TO ADDRESS GIVEN")
                UnprocessableEntity("Cannot Send Mail")
            # Mail to be sent here with the password we create

            return {"result": "success", "error": None}
        except Exception as e:
            LOG.exception(e)
            return {"result":e}
