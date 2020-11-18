from datetime import date, timedelta
import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.timesheetentry import TimesheetEntry
from ...helpers import token_verify_or_raise
# from ...models.jwttokenblacklist import JWTTokenBlacklist
from ...models import status, roles
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)

response_model_child = ns.model('getweekrecords', {
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

@ns.route('/get_week_records')
class Get_week_records(Resource):
    @ns.doc(description='Get_week_records',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self):
        records = []
        args = parser.parse_args(strict=True)
        
        try:
            y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])
        
            Email =  y['email']
            UserId = y['userid']
            
            token_verify_or_raise(args['Authorization'], Email, UserId )
            filter_after = datetime.today() - timedelta(days = 7)
            Week_records = TimesheetEntry.query.filter_by(UserId= UserId).filter(TimesheetEntry.WeekDate >= filter_after).all()
            
            # today = date.today()    
            # weekday = today.weekday()
            # mon = today - timedelta(days=weekday)
            # # upper bound
            # sun = today + timedelta(days=(6 - weekday))
            # # print(today,mon,sun)
            # Week_records = TimesheetEntry.query(TimesheetEntry).filter(UserId = UserId).filter(TimesheetEntry.WeekDate.between(mon,sun))
            
            # print(Week_records,"*********************")
            if Week_records:
                if len(Week_records) == 1:
                    records.append({
                            "EntryDate":Week_records[0].WeekDate,
                            "Customer":Week_records[0].Customer,
                            "Project":Week_records[0].Project,
                            "Task":Week_records[0].TaskName,
                            "SubTask":Week_records[0].SubTaskName,
                            "TimeSpent":Week_records[0].Timespent,
                            "Description":Week_records[0].Description
                            })
                else:
                    for record in Week_records:
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

