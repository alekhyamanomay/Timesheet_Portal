from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def init_app(app):
    db.init_app(app)
    app.logger.info("initialized models")

    with app.app_context():
        try :
            # from .Users import User
            # from .timesheet_entry import TimesheetEntry
            from .jwttokenblacklist import JWTTokenBlacklist
        except Exception as e:
            print(e)
        db.create_all()
        db.session.commit()
        app.logger.info('All the tables are created')
