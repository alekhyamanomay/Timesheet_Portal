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
# parser.add_argument('Ipaddress', type=str, location='json', required=False)
parser.add_argument('EntryId', type=str, location='headers', required=True)
parser.add_argument('Email', type=str, location='headers', required=True)

response_model = ns.model('Delete_entry', {
    'result': fields.String,    
})


@ns.route('/Delete_entry')
class Delete_entry(Resource):
    @ns.doc(description='Delete_entry',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args(strict=True)
        
        try:
            userinfo = User.query.filter_by(Email= Email).first()
            if userinfo is None:
                LOG.debug("Unable to find user details %s", Email)
                raise UnprocessableEntity('Unable to find user details')
            entry = TimesheetEntry.query.filter_by(EntryId = args['EntryId']).first()
                          
            db.session.delete(entry)
            db.session.commit()
            return {"result":"success"}

        except Exception as e:
            LOG.warning('Exception happened during authenticating user: %s', e)
            raise InternalServerError(e)
