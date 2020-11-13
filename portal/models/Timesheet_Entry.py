from flask import current_app as app
from .Users import User
from . import db

class TimesheetEntry(db.Model):
    __tablename__ = "TimesheetEntry"
    EntryID	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId	= db.Column(db.Integer, db.ForeignKey('User.UserId'), unique = True, nullable=False)
    UserName = db.Column(db.String(50), unique=True, nullable=False)	
    WeekDate =	db.Column(db.Date)
    Customer = db.Column(db.String(50), unique=True, nullable=False)		
    Project	= db.Column(db.String(50), unique=True, nullable=False)	
    TaskName = db.Column(db.String(50), unique=True, nullable=False)	
    SubTaskName	= db.Column(db.String(50), unique=True, nullable=False)	
    Timespent = db.Column(db.Integer, unique = True, nullable = False)
    Description	 = db.Column(db.String(255), unique=True, nullable=False)	
    EntryDatetime = db.Column(db.DateTime)
    Email	= db.Column(db.String(50), unique=True, nullable=False)
    Manager =  db.Column(db.String(50), unique=True, nullable=False)		

    def __repr__(self):
        return f"Timesheet('{self.EntryID}')"
