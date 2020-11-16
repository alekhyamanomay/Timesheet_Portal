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
from sqlalchemy import extract
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('UserId', type=str, location='headers', required=True)

response_model = ns.model('Get_month_records', {
    'result': fields.String,    
})

@ns.route('/Get_month_records')
class Get_month_records(Resource):
    @ns.doc(description='Get_month_records',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        records = []
        args = parser.parse_args(strict=True)
        UserId = args['UserId']
        try:
            today = date.today()    
            month = today.month()
            
            Month_records = TimesheetEntry.query(TimesheetEntry).filter(extract('month', TimesheetEntry.EntryDatetime) == month).all()
            # all_records = TimesheetEntry.query.filter(UserId= UserId).all()[0:20]
            for record in Month_records:
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


# days_per_month = {1: 31, 2: 29, 3: 31, ...} # you can fill this in yourself
# # lower bound
# first = today.replace(day=1)
# # upper bound
# try:
#     last = today.replace(day=days_per_month[today.month])
# except ValueError:
#     if today.month == 2:  # Not a leap year
#         last = today.replace(day=28)
#     else:
#         raise 
    