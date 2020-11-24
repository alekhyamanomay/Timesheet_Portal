from flask import current_app as app
from .users import User
from . import db

class TimesheetEntry(db.Model):
    __tablename__ = "TimesheetEntry"
    EntryID	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId	= db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)	
    WeekDate =	db.Column(db.Date)
    Customer = db.Column(db.String(50),nullable=False)		
    Project	= db.Column(db.String(50), nullable=False)	
    TaskName = db.Column(db.String(50), nullable=False)	
    SubTaskName	= db.Column(db.String(50), nullable=False)	
    Timespent = db.Column(db.Float(), nullable = False)
    Description	 = db.Column(db.String(255), nullable=False)	
    EntryDatetime = db.Column(db.DateTime, nullable = False)
    Email	= db.Column(db.String(50), nullable=False)
    Manager =  db.Column(db.String(50), nullable=True)			

    def __repr__(self):
        return f"Timesheet('{self.EntryID}')"
