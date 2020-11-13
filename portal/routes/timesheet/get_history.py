import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.timesheet_Entry import TimesheetEntry
# from ...models.Customers import Customers
# from ...models.Tasks import Tasks
# from ...models.Subtask import Subtasks
# from ...models.Projects import Projects
# from ...models.jwttokenblacklist import JWTTokenBlacklist
from ...models import status, roles
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('UserId', type=str, location='headers', required=True)

response_model = ns.model('Get_history', {
post_response_model = ns.model('Get_history', {
    'result': fields.String,    
})

@ns.route('/Get_history')
class GetHistory(Resource):
    @ns.doc(description='Get_history',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        records = []
        args = parser.parse_args(strict=True)
        UserId = args['UserId']
        try:
            all_records = TimesheetEntry.query.filter(UserId= UserId).all()[0:20]
            for record in all_records:
                records.append({
                    "EntryDate":record.EntryDatetime,
                    "Customer":record.Customer,
                    "Project":record.Project,
                    "Task":record.TaskName,
                    "SubTask":record.SubTaskName,
                    "TimeSpent":record.TimeSpent,
                    "Description":record.Description
                    })
        except Exception as e:
            LOG.warning('Exception happened during fetching records: %s', e)
            raise InternalServerError(e)

