import jwt
import json
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, reqparse, fields, inputs
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity, InternalServerError
from ...encryption import Encryption
from ...models.users import User
from ...models.timesheet_entry import TimesheetEntry
# from ...models.jwttokenblacklist import JWTTokenBlacklist
from ...models import db
from ...api import api
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('date', type=inputs.date_from_iso8601, location='headers', required=False)
parser.add_argument('customer', type=str, location='json', required=True)
parser.add_argument('project', type=str, location='json', required=True)
parser.add_argument('task', type=str, location='json', required=True)
parser.add_argument('subtask', type=str, location='json', required=True)
parser.add_argument('timespent', type=int, location='json', required=True)
parser.add_argument('description', type=str, location='json', required=True)

response_model = ns.model('Update_entry', {
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
            
            y = jwt.decode(args['Authorization'], key=APP.config['JWT_SECRET'], algorithms=['HS256'])
            Email =  y['email']
            UserID = y['userid']

            token_verify_or_raise(args['Authorization'], Email, UserID )
            userinfo = User.query.filter_by(Email= Email).first()
            if userinfo is None:
                LOG.debug("Unable to find user details %s", Email)
                raise UnprocessableEntity('Unable to find user details')
            entry = TimesheetEntry.query.filter_by(EntryId = args['entryid']).first()
            entry.WeekDate = date,
            entry.Customer = customer,
            entry.Project = project,
            entry.Task = task, 
            entry.Subtask= subtask, 
            entry.timespent = timespent, 
            entry.description= description
                    
            db.session.commit()
            return {"result":"success"}

        except Exception as e:
            LOG.warning('Exception happened during authenticating user: %s', e)
            raise InternalServerError(e)
