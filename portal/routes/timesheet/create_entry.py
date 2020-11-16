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

parser.add_argument('Name', type=str, location='headers', required=True)
parser.add_argument('Email', type=str, location='headers', required=True)
parser.add_argument('Date', type=inputs.date_from_iso8601, location='headers', required=False)
parser.add_argument('Customer', type=str, location='json', required=True)
parser.add_argument('Project', type=str, location='json', required=True)
parser.add_argument('Task', type=str, location='json', required=True)
parser.add_argument('subtask', type=str, location='json', required=True)
parser.add_argument('timespent', type=int, location='json', required=True)
parser.add_argument('description', type=str, location='json', required=True)

response_model = ns.model('Create_entry', {
    'result': fields.String,        
})


@ns.route('/Create_entry')
class Create_entry(Resource):
    @ns.doc(description='Create_entry',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args(strict=True)
        Name = args['Name']
        Email = args['Email']
        Date = args['Date']
        Customer = args['Customer']
        Project = args['Project']
        Task = args['Task']
        Subtask = args['subtask']
        timespent = args['timespent']
        description = args['description']
        
        try:
            userinfo = User.query.filter_by(Email= Email).first()
            if userinfo is None:
                LOG.debug("Unable to find user details %s", Email)
                raise UnprocessableEntity('Unable to find user details')
            entry = TimesheetEntry(UserId = userinfo.UserId, UserName = userinfo.UserName, WeekDate = Date, Customer = Customer,
                          Project = Project, Task = Task, Subtask= Subtask, timespent = timespent, description= description )
                          
            db.session.add(entry)
            db.session.commit()
            return {"result":"success"}

        except Exception as e:
            LOG.warning('Exception happened during authenticating user: %s', e)
            raise InternalServerError(e)
