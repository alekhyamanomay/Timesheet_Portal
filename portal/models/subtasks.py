from flask import current_app as app
from .tasks import Tasks
from . import db

class SubTasks(db.Model):
    __tablename__ = "SubTask"
    SubtaskId	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    TaskId	= db.Column(db.Integer, db.ForeignKey('Task.TaskId'))
    SubtaskName = db.Column(db.String(50), nullable=False)	
    		

    def __repr__(self):
        return f"{self.SubtaskName}"
