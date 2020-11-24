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
from ...helpers import token_verify_or_raise, token_decode
from ...models import status, roles
from ...api import api
from . import ns
from ... import APP, LOG
from datetime import date 
parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)

response_model_child = ns.model('gethistory', {
    "EntryId":fields.Integer,
    "EntryDate": fields.String,
    "Customer": fields.String,
    "Project": fields.String,
    "Task": fields.String,
    "SubTask": fields.String,
    "TimeSpent": fields.String,
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
            y = token_decode(args['Authorization'])
            if isinstance(y,tuple):
                return {'error':"Unathorized token"}, 401

            Email =  y['email']
            UserId = y['userid']
            token_verify_or_raise(args['Authorization'])

            # y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])

            # Email =  y['email']
            # UserId = y['userid']
            
            # token_verify_or_raise(args['Authorization'], Email, UserId )
            # To get current month records
            today = date.today() 
            month = today.month
            if month == 1:
                month1 = 12
            else:
                month1 =  month - 1
            months = (month, month1)
            for mon in months:
                Month_records += TimesheetEntry.query.filter_by(UserId= UserId).order_by(TimesheetEntry.WeekDate.desc()).filter(extract('month', TimesheetEntry.WeekDate) == mon).all()    
        
            # To get last 30 days records
            # filter_after = datetime.today() - timedelta(days = 30)
            # Month_records+= TimesheetEntry.query.filter_by(UserId= UserId).order_by(TimesheetEntry.WeekDate.desc()).filter(TimesheetEntry.WeekDate >= filter_after).all()
            if Month_records:
                if len(Month_records) == 1:
                    records.append({
                            "EntryId":Month_records[0].EntryID,
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
                            "EntryId":record.EntryID,
                            "EntryDate":record.WeekDate,
                            "Customer":record.Customer,
                            "Project":record.Project,
                            "Task":record.TaskName,
                            "SubTask":record.SubTaskName,
                            "TimeSpent":record.Timespent,
                            "Description":record.Description
                            })
            # print(records)
            return {"records": records}, 200

        except Exception as e:
            LOG.warning('Exception happened during fetching records: %s', e)
            raise InternalServerError(e)

