import os
import logging

LOG_LEVEL = logging.DEBUG
ROOT_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__),"..",".."))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(DATA_DIR, 'log')

SECRET_KEY = 'BT-=f~i1IlIHF(#'
JWT_SECRET = 'R]B+=46,e=gKtI/'

SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://LAPTOP-5KNII04G/Timesheet_db?driver=SQL Server?Trusted_Connection=Yes'
# WRITE_DB = 'mssql+pyodbc://DESKTOP-IRHNO1M\SQLEXPRESS/TestDB?driver=SQL Server?Trusted_Connection=Yes'
# READ_DB = 'mssql+pyodbc://DESKTOP-IRHNO1M\SQLEXPRESS/ICBLDataView?driver=SQL Server?Trusted_Connection=No'

DEFAULT_PASSWORD= 'tZ4Olwg7n7od6J9lqmtTpw=='

FRONTEND_URL= 'https://www.google.com/'

MAILSERVER_DOMAIN = 'smtp.gmail.com'
MAILSERVER_PORT = 465
MAILSERVER_USERNAME = 'unofficialfarooqsheikh@gmail.com'
MAILSERVER_PASSWORD = 'Un0fficialfarooqsheikh'

ENVIRONMENT = "DEVELOPMENT"
# flask run -h 192.168.2.111 -p 9000