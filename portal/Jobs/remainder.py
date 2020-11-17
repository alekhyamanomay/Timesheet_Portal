# from flask import Flask
# import portal.models as models
# app = Flask(__name__)
# app.config['SQLALCEMY_TRACK_MODIFICATIONS'] = False
# app.config['WRITE_DB'] = 'mssql+pyodbc://DESKTOP-IRHNO1M\SQLEXPRESS/TestDB?driver=SQL Server?Trusted_Connection=Yes'
# models.init_app(app)
# from portal.models.users import Users
# app.app_context().push()
# print(Users.query.all())
from threading import Thread
import time
import init
import threading
from portal.models.users import User
from portal.models.timesheetentry import TimesheetEntry
from sqlalchemy import func
from portal.models import db
from portal.helpers import _SendEmail
from datetime import datetime, timedelta

# yesterday
yesterday = (datetime.now() + timedelta(days=-1)).date()
print(yesterday)

# get all users
users = User.query.all()
# get timesheet data of yesterday and group by userid
timesheetdata = db.session.query(TimesheetEntry.UserId, func.sum(TimesheetEntry.Timespent), func.count(
    TimesheetEntry.UserId)).filter_by(WeekDate=yesterday).group_by(TimesheetEntry.UserId).all()
print(timesheetdata)
userids = []
emails = {}
for i in users:
    if i.UserId != 1001 and i.Status == "ACTIVE":
        emails[i.UserId] = [i.UserName, i.Email, i.ManagerEmail, i.SecondaryManagerEmail]
        userids.append(i.UserId)
# print(userids)
# print(emails)
for i in timesheetdata:
    if not(i[1] < 2 and i[2] < 2):
        userids.remove(i[0])
print(userids)
print(timesheetdata)
tracker = []
subject = f"Timesheet entry for {yesterday}"
for i in userids:
    
    print(f"heeeya,{emails[i][1]}")
    body = f'''<html>
            <body>
            <h1>Hi {emails[i][0]},</h1>
            <p>There are none or minimal entries recorded against your timesheet for {yesterday} </p>
            <p>Please log on to the application and complete the TS entry immediately</p>
            <p>Please reach out to Sirisha in case of any issues</p>
            <p>Thanks,</p>
            <p>Manomay</p>
            </body>
            </html>'''
        
    # if emails[i][1] == "shaik.farooq@manomay.biz":
    #     _SendEmail([emails[i][1]],subject,body,cc=[])
    # time.sleep(0.75)
    result = _SendEmail(init.app,["shaik.farooq@manomay.biz"],subject,body,[])
    if result == "mail sent":
        pass
        