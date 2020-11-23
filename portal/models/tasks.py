from flask import current_app as app
from . import db


class Tasks(db.Model):
    __tablename__ = "Task"
    TaskId	= db.Column(db.Integer, primary_key=True, autoincrement=True)
    TaskName = db.Column(db.String(50), nullable=False)	
    subtasks = db.relationship('SubTasks', backref='tasks', lazy=True)		

    def __repr__(self):
        return f"Tasks('{self.TaskId}')"
