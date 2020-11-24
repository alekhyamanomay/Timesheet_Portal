import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...helpers import token_verify_or_raise, token_decode
from ...encryption import Encryption
from ...models.customers import Customers
from ...models.projects import Projects
from ...models.tasks import Tasks
from ...models.subtasks import SubTasks
from ...models import db
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)

# response_model_child = ns.model('getweekrecords', {
#     "EntryId" : fields.Integer,
#     "EntryDate": fields.String,
#     "Customer": fields.String,
#     "Project": fields.String,
#     "Task": fields.String,
#     "SubTask": fields.String,
#     "TimeSpent": fields.String,
#     "Description": fields.String
# })

# response_model = ns.model('GetUsers', {
#     "records": fields.List(fields.Nested(response_model_child))
# })

@ns.route('/get_values')
class Get_values(Resource):
    @ns.doc(description='Get_values',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    # @ns.marshal_with(response_model)
    def get(self):
        args = parser.parse_args(strict=True)
        task_subtask ={}
        cust_proj = {}
        all_values = {}
        customers = Customers.query.all()
        tasks = Tasks.query.all()
        try:
            y = token_decode(args['Authorization'])
        
            if isinstance(y,tuple):
                return {'error':"Unathorized token"}, 401
            token_verify_or_raise(args['Authorization'])

            for customer in customers:
                proj_values = Projects.query.filter_by(CustomerId=customer.CustomerId).all()
                cust_proj[customer.CustomerName] = [str(p) for p in proj_values]
            
            for task in tasks:
                subtasks_values = SubTasks.query.filter_by(TaskId = task.TaskId).all()
                task_subtask[task.TaskName] = [str(s) for s in subtasks_values]

            all_values['customer_project'] = cust_proj
            all_values['task_subtask'] = task_subtask
            
            return {"result": all_values}, 200
        except Exception as e:
            print(e)