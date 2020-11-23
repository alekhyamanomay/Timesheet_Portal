from flask import current_app as app
from . import db

class Customers(db.Model):
    __tablename__ = "Customer"
    CustomerId	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(50), nullable=False)	

    projects = db.relationship('Projects', backref='customers', uselist=True)		

    def __repr__(self):
        return f"Customers('{self.CustomerId}')"
