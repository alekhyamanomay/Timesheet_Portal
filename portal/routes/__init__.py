
def init_app(app):
    from .auth import login,logout
    from .admin import create, read, update, delete
    from .user import profile
    from . import index
    from .Testing import test
    from .timesheet import create_entry, delete_entry, get_history, get_monthy_records, get_week_records, Update_entry
    app.logger.info("Initialized routes")
