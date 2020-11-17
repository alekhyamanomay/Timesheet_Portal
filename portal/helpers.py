import os
import jwt
import time
import uuid
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from flask import current_app as app
from datetime import timedelta
from werkzeug.exceptions import Unauthorized
from .models.jwttokenblacklist import JWTTokenBlacklist
from datetime import timedelta

from flask import make_response, request
from functools import update_wrapper


RESPONSE_OK = {"result": "Success"}


def get_config_file_path():
    env = os.getenv("BACKEND_ENV", default="development")
    print('env--->',env)
    base = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.abspath(os.path.join(base, '..', 'config', env + '.py'))
    return absolute_path


def delete_excel(filename):
    time.sleep(5)  # ??!!
    print("deleting file -" + filename)
    os.remove(filename)


def converter(o):
    if isinstance(o, datetime):
        return o.__str__()



def token_verify_or_raise(token, email ,userid):
    decoded_token = token_verify(token, email ,userid)
    if decoded_token is None:
        raise Unauthorized()

    tokens = JWTTokenBlacklist.query.filter_by(JWTToken=token).scalar()
    if tokens is not None:
        raise Unauthorized()

    return decoded_token


def token_verify(token, email ,userid):
    decoded = None

    try:
        decoded = jwt.decode(token, key=app.config['JWT_SECRET'])
        print(decoded)
        if decoded["userid"] != userid or decoded["email"] != email:
            decoded = None
        print(decoded)
    except jwt.DecodeError as e:
        print("decode error", e)

    except jwt.ExpiredSignatureError:
        print("sign")
    except KeyError:
        decoded = None
        print("key error")
    return decoded



def randomStringwithDigitsAndSymbols(stringLength=10):
    """Generate a random string of letters, digits and special characters """

    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))


def isDev():
    return "development" == os.getenv("BACKEND_ENV", default="")


def isProd():
    return "production" == os.getenv("BACKEND_ENV", default="")


def isStaging():
    return "staging" == os.getenv("BACKEND_ENV", default="")


def uuid_generator():
    return str(uuid.uuid4())

def _SendEmail(to_address,subject,body,cc=[]):
    
    domain = app.config['MAILSERVER_DOMAIN']
    email= app.config['MAILSERVER_USERNAME']
    if app.config["ENVIRONMENT"] == "DEVELOPMENT":
        port= app.config['MAILSERVER_PORT']
        password= app.config['MAILSERVER_PASSWORD']

    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['from'] = email
    msg['to'] = ', '.join(to_address)
    msg['cc'] = ', '.join(cc)
    msg.attach(MIMEText(body, 'html'))
    
    if app.config["ENVIRONMENT"] == "DEVELOPMENT":
        # connecting to mailserver and send the email
        mailserver = smtplib.SMTP_SSL(domain, port=port)
        mailserver.login(email, password)

    if app.config["ENVIRONMENT"] == "PRODUCTION":
        # connecting to mailserver and send the email
        mailserver = smtplib.SMTP(domain)
    try:
        mailserver.sendmail(email, (to_address+cc), msg.as_string())

    except Exception as e:
        print(e)
        domain = app.config['MAILSERVER_DOMAIN']
        email= app.config['MAILSERVER_USERNAME']
        to_address = ["shaik.farooq@manomay.biz","neetha.pasham@manomay.biz"]
        if app.config["ENVIRONMENT"] == "DEVELOPMENT":
            port= app.config['MAILSERVER_PORT']
            password= app.config['MAILSERVER_PASSWORD']

        msg = MIMEMultipart()
        msg['subject'] = "Error Sending Mails"
        msg['from'] = email
        msg['to'] = ', '.join(to_address)
        body = f'''<p>Hi, Admin</p>
                    <p>Looks like There is some Problem triggering the Emails</p>
                    <p>Please Check!</p>
                    <p>Error is {e}</p>
                    <p>Thanks and Regards</p>
                '''
        msg.attach(MIMEText(body, 'html'))
        
        if app.config["ENVIRONMENT"] == "DEVELOPMENT":
            # connecting to mailserver and send the email
            mailserver = smtplib.SMTP_SSL(domain, port=port)
            mailserver.login(email, password)

        if app.config["ENVIRONMENT"] == "PRODUCTION":
            # connecting to mailserver and send the email
            mailserver = smtplib.SMTP(domain)
        mailserver.sendmail(email, (to_address), msg.as_string())
        return f"mail failed: {e}"
    print("mail sent") 
    return "mail sent"