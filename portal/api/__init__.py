
from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import HTTPException

api = Api(version = "string", description= "ICBL Life API", doc="/doc/", catch_all_404s=True )

def init_app(app):

    version1 = Blueprint('api', __name__, url_prefix='/version_1', template_folder='templates')

    api.init_app(version1)
    app.register_blueprint(version1)

    @api.errorhandler(HTTPException)
    def handle_exception_with_cors(error):
        return {'message': str(error)},  getattr(error, 'code', 500), {'Access-Control-Allow-Origin': '*'}
    
    app.logger.info("initiated api")