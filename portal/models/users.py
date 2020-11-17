from flask import current_app as app
from . import db

class User(db.Model):
    # __bind_key__ = 'writeonly'
    __tablename__ = "User"
    UniqueuserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId	= db.Column(db.Integer, unique = True, nullable = False)
    Password = db.Column(db.String(150), nullable=False)
    UserName = db.Column(db.String(50), unique=False, nullable=False)	
    Email	= db.Column(db.String(50), unique=True, nullable=False)
    Permission	= db.Column(db.String(20), unique=True, nullable=False)
    Manager	 = db.Column(db.String(50), nullable=True)
    ManagerEmail  = db.Column(db.String(50), nullable=True)
    SecondaryManager = db.Column(db.String(50), nullable=True)
    SecondaryManagerEmail = db.Column(db.String(50),nullable=True)
    timesheet_entry = db.relationship('TimesheetEntry', backref='User', lazy=True)
    Role = db.Column(db.String(150), nullable=False)
    Status = db.Column(db.String(150), nullable=False)
  
    def __repr__(self):
        return f"User('{self.UserName}')"

