from . import ns
from flask import request
from flask_restx import Resource,reqparse,fields
from ...models import db
from ...models.Users import User
from ... import APP, LOG

# response_model = ns.model('Client_details', {
#     'ID': fields.String,
#     'Client_Name': fields.String,
#     'DateOfBirth': fields.DateTime
# })

@ns.route('/testing')
class Test(Resource):

    @ns.doc( description = 'Testing', responses={ 200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'} )
    def get(self):
        
        print(request.path)
        print(request.args)
        print(request.base_url)
        print(request.blueprint)
        print(request.data)
        return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    
