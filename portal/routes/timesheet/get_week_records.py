from datetime import date, timedelta
import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.timesheet_Entry import TimesheetEntry
# from ...models.jwttokenblacklist import JWTTokenBlacklist
from ...models import status, roles
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('UserId', type=str, location='headers', required=True)

response_model = ns.model('Get_week_records', {
post_response_model = ns.model('Get_week_records', {
    'result': fields.String,    
})

@ns.route('/Get_week_records')
class Get_week_records(Resource):
    @ns.doc(description='Get_week_records',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        records = []
        args = parser.parse_args(strict=True)
        UserId = args['UserId']
        try:
            today = date.today()    
            weekday = today.weekday()
            mon = today - timedelta(days=weekday)
            # upper bound
            sun = today + timedelta(days=(6 - weekday))
            print(today,mon,sun)
            Week_records = TimesheetEntry.query(TimesheetEntry).filter(UserId = UserId).filter(TimesheetEntry.EntryDatetime.between(mon,sun))
            # all_records = TimesheetEntry.query.filter(UserId= UserId).all()[0:20]
            for record in Week_records:
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

