from flask import current_app as app
from .users import User
from . import db

class TimesheetEntry(db.Model):
    __bind_key__ = 'writeonly'
    __tablename__ = "TimesheetEntry"
    EntryID	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId	= db.Column(db.Integer, db.ForeignKey('User.UserId'), unique = False, nullable=True)
    UserName = db.Column(db.String(50), unique=False, nullable=True)	
    WeekDate =	db.Column(db.Date)
    Customer = db.Column(db.String(50), unique=False, nullable=True)		
    Project	= db.Column(db.String(50), unique=False, nullable=True)	
    TaskName = db.Column(db.String(50), unique=False, nullable=True)	
    SubTaskName	= db.Column(db.String(50), unique=False, nullable=True)	
    Timespent = db.Column(db.Integer, unique = False, nullable = True)
    Description	 = db.Column(db.String(255), unique=False, nullable=True)	
    EntryDatetime = db.Column(db.Time)
    Email	= db.Column(db.String(50), unique=False, nullable=True)
    Manager =  db.Column(db.String(50), unique=False, nullable=True)		

    def __repr__(self):
        return f"Timesheet('{self.EntryID}')"
