
def init_app(app):
    from .auth import login,logout
    from .auth.password import change, reset
    from .admin import create, read, update, delete
    # from .admin import read
    # from .user import profile
    from . import index
    # from .Testing import test
    from .reports import parameters,projects_report,remainder_reports
    from .timesheet import (create_entry, delete_entry, get_recent_records,parameters,
                           get_history, get_today_records, get_week_records, update_entry)
    app.logger.info("Initialized routes")
