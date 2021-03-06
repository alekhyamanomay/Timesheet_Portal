import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.timesheetentry import TimesheetEntry
from ...helpers import token_verify_or_raise, token_decode
# from ...models.jwttokenblacklist import JWTTokenBlacklist
from ...models import db
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str,
                    location='headers', required=True)
parser.add_argument('entryid', type=str, location='json', required=True)
parser.add_argument('date', type=str, location='json', required=False)
parser.add_argument('customer', type=str, location='json', required=True)
parser.add_argument('project', type=str, location='json', required=True)
parser.add_argument('task', type=str, location='json', required=True)
parser.add_argument('subtask', type=str, location='json', required=True)
parser.add_argument('timespent', type=float, location='json', required=True)
parser.add_argument('description', type=str, location='json', required=True)

response_model = ns.model('update_entry', {
    'result': fields.String,    
})


@ns.route('/update_entry')
class Update_entry(Resource):
    @ns.doc(description='Update_entry',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args(strict=True)
        
        Date = args['date']
        Customer = args['customer']
        Project = args['project']
        Task = args['task']
        Subtask = args['subtask']
        timespent = args['timespent']
        description = args['description']
        
        try:
            y = token_decode(args['Authorization'])
        
            if isinstance(y,tuple):
                return {'error':"Unathorized token"}, 401

            Email =  y['email']
            UserId = y['userid']
            token_verify_or_raise(args['Authorization'])
            
            userinfo = User.query.filter_by(Email= Email).first()
            if userinfo is None:
                LOG.debug("Unable to find user details %s", Email)
                raise UnprocessableEntity('Unable to find user details')
            entry = TimesheetEntry.query.filter_by(EntryID = args['entryid']).first()
            entry.WeekDate = Date
            entry.Customer = Customer
            entry.Project = Project
            entry.TaskName = Task
            entry.SubtaskName = Subtask
            entry.Timespent = timespent
            entry.Description= description
            
            db.session.commit()
            return {"result":"success"}

        except Exception as e:
            LOG.warning('Exception happened during authenticating user: %s', e)
            raise InternalServerError(e)
