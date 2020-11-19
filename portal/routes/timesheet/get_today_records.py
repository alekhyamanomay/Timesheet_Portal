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
from ...models import db
from sqlalchemy import and_
from ...api import api
from . import ns
from ... import APP, LOG


parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('date', type=str, location='json', required=True)
response_model_child = ns.model('gettodayrecords', {
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

@ns.route('/get_today_records')
class Get_today_records(Resource):
    @ns.doc(description='Get_today_records',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        records = []
        args = parser.parse_args(strict=True)
        
        try:
            y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])
        
            Email =  y['email']
            UserId = y['userid']
            # print(args['date'][0:10],"********")
            token_verify_or_raise(args['Authorization'], Email, UserId )
            
            Today_records = TimesheetEntry.query.filter_by(UserId = UserId).filter(TimesheetEntry.WeekDate.ilike("%" + args['date'][0:10] +"%")).all()
                            # and_ (TimesheetEntry.WeekDate.ilike("%" + args['date'][0:10] +"%"))).all()
            
            # print(Today_records,"*******")  
            if Today_records:
                if len(Today_records) == 1:
                    records.append({
                            "EntryDate":Today_records[0].WeekDate,
                            "Customer":Today_records[0].Customer,
                            "Project":Today_records[0].Project,
                            "Task":Today_records[0].TaskName,
                            "SubTask":Today_records[0].SubTaskName,
                            "TimeSpent":Today_records[0].Timespent,
                            "Description":Today_records[0].Description
                            })
                else:
                    for record in Today_records:
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
    