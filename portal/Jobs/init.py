from flask import Flask
import sys
sys.path.insert(1,"C:\\Users\\Manomay\\Desktop\\TimeSheetPortal\\Code")
import portal.models as models
app = Flask(__name__) 
app.config.from_pyfile("C:\\Users\\Manomay\\Desktop\\TimeSheetPortal\\Code\\config\\development.py")
models.init_app(app)
app.app_context().push()