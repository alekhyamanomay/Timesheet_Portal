from . import ns
from flask import request
from flask_restx import Resource,reqparse,fields
from ...models import db
from ...models.users import User
from ...models.projects import Projects
from ...models.customers import Customers
from ... import APP, LOG

@ns.route('/parameters')
class Test(Resource):
    @ns.doc( description = 'Testing', responses={ 200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'} )
    def get(self):
        # print(Projects.query.all())
        cust_proj = {}
        customers = Customers.query.all()
        for customer in customers:
                proj_values = Projects.query.filter_by(CustomerId=customer.CustomerId).all()
                cust_proj[customer.CustomerName] = [str(p) for p in proj_values]
        return cust_proj
