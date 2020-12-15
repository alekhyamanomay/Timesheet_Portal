try:
    import os
    import sys
    from datetime import datetime, timedelta
    basepath = os.path.abspath(os.path.join(os.getcwd(),"..\.."))
    print(basepath)
    sys.path.insert(1,basepath)
    print(sys.path)
    # create instance of flask app
    # help('modules')
    from flask import Flask
    app = Flask(__name__)
    configfile = os.path.abspath(os.path.join(basepath,'config','development.py'))
    app.config.from_pyfile(configfile)
    # create instance of sql alchemy
    import portal.models as models
    models.init_app(app)
    app.app_context().push()
    from sqlalchemy import func
    from portal.helpers import _SendEmail
    from portal.models import db
    from portal.models.remainders import Remainders
    from portal.models.timesheetentry import TimesheetEntry
    from portal.models.users import User
    # Logging as in writing to files
    logs_location = os.path.join(app.config["LOG_DIR"],"remainder.log")
    if os.path.isfile(logs_location):
        print(logs_location,"Size:",os.stat(logs_location).st_size)
        if os.stat(logs_location).st_size >= 1048576:
            print('removing repitition log')
            os.remove(logs_location)
    f = open(logs_location, "a")
    weekday = datetime.now().weekday()
    f.write(f'___________________________________________________________________\n')
    f.write(f'logging Started for {weekday} - day {datetime.now().strftime("%d-%m-%Y")}\n')
    # if today is Saturday or Sunday don't run this Job
    if weekday == 5 or weekday == 6:
        f.write(f'Today is either Saturday or Sunday, {datetime.now().strftime("%d-%m-%Y")} not need to run today \n')
        f.write(f'___________________________________________________________________\n')
        f.write(f'exiting...\n')
        f.close()
        exit()
    # yesterday only on tuesday,wednesday,thursday and friday
    yesterday = (datetime.now() + timedelta(days=-1)).date()
    print(yesterday)
    # if today is monday go back three days i.e friday
    if weekday == 0:
        yesterday = (datetime.now() + timedelta(days=-3)).date()
        print(yesterday)
    # if yesterday this function was ran no need to run it again
    if Remainders.query.filter_by(RemainderDate = yesterday).first():
        f.write(f'Remainder Ran {yesterday.strftime("%d-%m-%Y")} not need to run again \n')
        f.write(f'___________________________________________________________________\n')
        f.write(f'exiting...\n')
        f.close()
        exit()
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
    print(userids)
    print(emails)
    for i in timesheetdata:
        if not(i[1] < 2):
            userids.remove(i[0])
    print(userids)
    print(timesheetdata)
    tracker = []
    subject = f'Timesheet entry for {yesterday.strftime("%d-%m-%Y")}'
    for i in userids:
        print(f"Triggering Remainder to {emails[i][1]}")
        body = f'''<html>
                <body>
                <h3>Hi {emails[i][0]},</h3>
                <p>There are none or minimal entries recorded against your timesheet for {yesterday.strftime("%d-%m-%Y")} </p>
                <p>Please log on to the application and complete the TS entry immediately</p>
                <p>Please reach out to Sirisha in case of any issues</p>
                <p>Thanks,</p>
                <p>Manomay</p>
                </body>
                </html>'''
        f.write(f"Sending remainder to: {emails[i][1]}\n")
        result = _SendEmail([emails[i][1]],subject,body,[emails[i][2],emails[i][3]])
        # result = "mail sent"
        if result == "mail sent":
            print("updating remainder table")
            f.write(f"Remainder sent successfully to {emails[i][1]}\n")
            newentry = Remainders(
                                    UserId =i,
                                    UserName =emails[i][0],  
                                    # TriggeredDate=datetime.now().date()+ timedelta(days=-1))
                                    RemainderDate=yesterday)
            db.session.add(newentry)
            # db.session.commit()
        else:
            print("some issue")
            f.write(f"some error remainding to {emails[i][1]}, {result} \n")
    f.write(f'___________________________________________________________________\n')
    f.write(f'logging Ending for - day {datetime.now().strftime("%d-%m-%Y")}\n')        
    f.close()
except Exception as e:
    print(e)
    f.write(f'{str(e)}\n')
    f.write(f'exiting...\n')
    f.close()

