from flask_sqlalchemy import SQLAlchemy
# from ... import APP

db = SQLAlchemy()
def init_app(app):
    db.init_app(app)
    app.logger.info("initialized models")
    with app.app_context():
        try :
            from .users import User
            from .timesheetentry import TimesheetEntry
            from .remainders import Remainders
            from .jwttokenblacklist import JWTTokenBlacklist
            from .customers import Customers
            from .projects import Projects
            from .tasks import Tasks
            from .subtasks import SubTasks
        except Exception as e:
            print(e)
        db.create_all()
        db.session.commit()
        app.logger.info('All the tables are created')
