from flask import current_app as app
from .users import User
from . import db

class Remainders(db.Model):
    __tablename__ = "REMAINDERS"
    EntryID	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId	= db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)	
    RemainderDate =	db.Column(db.Date)	

    def __repr__(self):
        return f"Timesheet('{self.EntryID}')"
