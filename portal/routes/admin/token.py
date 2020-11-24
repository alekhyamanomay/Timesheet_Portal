import jwt
from flask_restx import Resource, reqparse, fields
from . import ns
from ... import APP

@ns.route("/token")
class CreateUser(Resource):
    # @ns.doc(description='token',
    #         responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    # @ns.expect(parser, validate=False)
    # @ns.marshal_with(response_model)
    def get(self):
    
        try:
            # print(x)
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNoYWlrIEZhcm9vcSIsImVtYWlsIjoic2hhaWsuZmFyb29xQG1hbm9tYXkuYml6IiwidXNlcmlkIjoxMDU4LCJleHAiOjE2MDU3OTYzNDIsInJvbGUiOiJHRU5FUklDIn0.iKXM7vrCYtRkTi0cxNKF8JemIh9C4zkRxZPv8hv19Yw'
            decoded = jwt.decode(token, key=APP.config['JWT_SECRET'])
            if decoded is None:
                raise Unauthorized()
        
        except jwt.DecodeError as e:
            raise e

        except jwt.ExpiredSignatureError as e:
            raise e
            
        except KeyError:
            raise KeyError

    