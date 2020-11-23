import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...helpers import token_verify_or_raise
from ...encryption import Encryption
from ...models.customers import Customers
from ...models.projects import projects
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
class Get_week_records(Resource):
    @ns.doc(description='Get_values',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self):

        task_subtask ={}
        cust_proj = {}
        customers = Customers.query.all()
        for customer in customers:
            cust_proj[customer.CustomerId]= Projects.query.filter_by(CustomerId=customer.CustomerId).all()
            # projects = Projects.query.filter_by(CustomerId=customer.CustomerId).all()
        
        tasks = Tasks.query.all()
        for task in tasks:
            task_subtask[task.TaskId] = SubTasks.query.filter_by(TaskId = task.TaskId).all()

        return cust_proj,task_subtask