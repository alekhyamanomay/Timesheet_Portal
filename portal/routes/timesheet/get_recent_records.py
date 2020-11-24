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
from ...models import db
from ...api import api
from . import ns
from ... import APP, LOG
from datetime import date 
parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)

response_model_child = ns.model('getrecententries', {
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

@ns.route('/get_recent_entries')
class GetHistory(Resource):
    @ns.doc(description='get_recent_entries',
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
            Recent_records = TimesheetEntry.query.filter_by(UserId= UserId).order_by(TimesheetEntry.EntryDatetime.desc()).all()[:5]
            
            if Recent_records:
                if len(Recent_records) == 1:
                    records.append({
                            "EntryId":Recent_records[0].EntryID,
                            "EntryDate":Recent_records[0].WeekDate,
                            "Customer":Recent_records[0].Customer,
                            "Project":Recent_records[0].Project,
                            "Task":Recent_records[0].TaskName,
                            "SubTask":Recent_records[0].SubTaskName,
                            "TimeSpent":Recent_records[0].Timespent,
                            "Description":Recent_records[0].Description
                            })
                else:
                    for record in Recent_records:
                        print(record.Timespent,type(record.Timespent),"**************")
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
            print(records)
            
            return {"records": records}, 200

        except Exception as e:
            LOG.warning('Exception happened during fetching records: %s', e)
            raise InternalServerError(e)


