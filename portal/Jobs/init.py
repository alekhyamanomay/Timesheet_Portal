import os
import sys

basepath =os.getcwd()
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


app.app_context().push()