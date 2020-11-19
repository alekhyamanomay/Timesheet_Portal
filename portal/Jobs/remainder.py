import init
import os

from portal.models.users import User
from portal.models.timesheetentry import TimesheetEntry
from portal.models.remainders import Remainders
from sqlalchemy import func
from portal.models import db
from portal.helpers import _SendEmail
from datetime import datetime, timedelta

# yesterday
yesterday = (datetime.now() + timedelta(days=-1)).date()
print(yesterday)
logs_location = os.path.join(init.app.config["LOG_DIR"],"remainder.log")
if os.path.isfile(logs_location):
    print(logs_location,"Size:",os.stat(logs_location).st_size)
    if os.stat(logs_location).st_size >= 1048576:
        print('removing repitition log')
        os.remove(logs_location)
f = open(logs_location, "a")
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
    
    print(f"Triggering Remainder to {emails[i][1]}")
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
    f.write(f"Sending remainder to: {emails[i][1]}\n")
    # result = _SendEmail(["shaik.farooq@manomay.biz"],subject,body,[])
    result = "mail sent"
    print(result)
    if result == "mail sent":
        print("updating remainder table")
        f.write(f"Remainder sent successfully to {emails[i][1]}\n")
        newentry = Remainders(
                                UserId =i,
                                UserName =emails[i][0],  
                                # TriggeredDate=datetime.now().date()+ timedelta(days=-1))
                                RemainderDate=yesterday)
        db.session.add(newentry)
        db.session.commit()
    else:
        print("some issue")
        f.write(f"some error remainding to {emails[i][1]}, {result} \n")
        
f.close()