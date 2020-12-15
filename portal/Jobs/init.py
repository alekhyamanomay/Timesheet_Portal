import os
import sys
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
LOG = logging
def init_logger(app):
    global LOG
    log_file = os.path.join(app.config['LOG_DIR'], 'remainder.log')

    log_level =  logging.DEBUG
    log_format = Formatter(f'%(asctime)s-%(levelname)s-%(message)s')

    TWO_MEGABYTE = 2_000_000
    file_handler = RotatingFileHandler(filename=log_file, maxBytes=TWO_MEGABYTE, backupCount=3)
    file_handler.setFormatter(log_format)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)

    LOG = app.logger
    LOG.info('Initialized logger with level %s', log_level)
    print("working")
    print(LOG)

basepath =os.path.abspath(os.path.join(os.getcwd(),"..\.."))
print(basepath)
sys.path.insert(1,basepath)
# create instance of flask app
from flask import Flask
app = Flask(__name__)
configfile = os.path.abspath(os.path.join(basepath,'config','development.py'))
app.config.from_pyfile(configfile)
# create instance of sql alchemy
import portal.models as models
models.init_app(app)
init_logger(app)
app.app_context().push()



