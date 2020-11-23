from flask import current_app as app
from .customers import Customers
from . import db

class Projects(db.Model):
    __tablename__ = "Project"
    ProjectId	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerId	= db.Column(db.Integer, db.ForeignKey('Customer.CustomerId'))
    ProjectName = db.Column(db.String(50), nullable=False)	
    		

    def __repr__(self):
        return f"Projects('{self.ProjectId}')"
