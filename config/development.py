import os
import logging

LOG_LEVEL = logging.DEBUG
ROOT_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__),"..",".."))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(DATA_DIR, 'log')
REPORT_DIR = "C:\\Users\\Manomay\\Desktop\\Reports"

SECRET_KEY = 'BT-=f~i1IlIHF(#'
JWT_SECRET = 'R]B+=46,e=gKtI/'

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DESKTOP-RMVRFH6/Timesheet_db?driver=SQL Server?Trusted_Connection=Yes'
# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DESKTOP-IRHNO1M\SQLEXPRESS/TimeSheet?driver=SQL Server?Trusted_Connection=Yes'
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://Manomay1:Manomay@9@DESKTOP-IRHNO1M\SQLEXPRESS/TimeSheet?driver=SQL Server?Trusted_Connection=No'
DEFAULT_PASSWORD= 'tZ4Olwg7n7od6J9lqmtTpw=='

FRONTEND_URL= 'https://www.google.com/'

MAILSERVER_DOMAIN = 'smtp.gmail.com'
MAILSERVER_PORT = 465
# MAILSERVER_USERNAME = 'unofficialfarooqsheikh@gmail.com'
# MAILSERVER_PASSWORD = 'Un0fficialfarooqsheikh'
MAILSERVER_USERNAME = 'manomaytesting@gmail.com'
MAILSERVER_PASSWORD = 'Testing@1234'

ENVIRONMENT = "DEVELOPMENT"
# flask run -h 192.168.2.111 -p 9000