import jwt
import json
from datetime import datetime, timedelta
from sqlalchemy import extract
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.timesheetentry import TimesheetEntry
from ...helpers import token_verify_or_raise
from ...models import status, roles
from ...api import api
from . import ns
from ... import APP, LOG
from datetime import date 
parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)

response_model_child = ns.model('gethistory', {
    "EntryDate": fields.String,
    "Customer": fields.String,
    "Project": fields.String,
    "Task": fields.String,
    "SubTask": fields.String,
    "TimeSpent": fields.Float,
    "Description": fields.String
})

response_model = ns.model('GetUsers', {
    "records": fields.List(fields.Nested(response_model_child))
})

@ns.route('/get_history')
class GetHistory(Resource):
    @ns.doc(description='Get_history',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self):
        records = []
        Month_records = []
        args = parser.parse_args(strict=True)
        try:
            y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])
        
            Email =  y['email']
            UserId = y['userid']
            
            token_verify_or_raise(args['Authorization'], Email, UserId )
            # To get current month records
            today = date.today()    
            month = today.month
            Month_records=TimesheetEntry.query.filter_by(UserId= UserId).filter(extract('month', TimesheetEntry.EntryDatetime) == month).all()    
        
            # To get last 30 days records
            filter_after = datetime.today() - timedelta(days = 30)
            Month_records+= TimesheetEntry.query.filter_by(UserId= UserId).filter(TimesheetEntry.EntryDatetime >= filter_after).all()
            if Month_records:
                if len(Month_records) == 1:
                    records.append({
                            "EntryDate":Month_records[0].WeekDate,
                            "Customer":Month_records[0].Customer,
                            "Project":Month_records[0].Project,
                            "Task":Month_records[0].TaskName,
                            "SubTask":Month_records[0].SubTaskName,
                            "TimeSpent":Month_records[0].Timespent,
                            "Description":Month_records[0].Description
                            })
                else:
                    for record in Month_records[:-1]:
                        records.append({
                            "EntryDate":record.WeekDate,
                            "Customer":record.Customer,
                            "Project":record.Project,
                            "Task":record.TaskName,
                            "SubTask":record.SubTaskName,
                            "TimeSpent":record.Timespent,
                            "Description":record.Description
                            })
            
            return {"records": records}, 200

        except Exception as e:
            LOG.warning('Exception happened during fetching records: %s', e)
            raise InternalServerError(e)

