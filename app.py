import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from globals import API_PREFIX, API_TITLE, API_VERSION, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, DEBUG, DEBUG_PATH, JWT_SECRET_KEY, PORT, SWAGGER_URL

from db import db

from resources.user import blp as UserBluprint
from resources.group import blp as GroupBluprint
from resources.demand import blp as DemandBluprint

def create_app(settings_module: str | None = None):
    """
    Creates a new instace of Flask application.
    
    Args:
        settings_module (str, optional): Configuration module to use.
    """
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_LEEWAY"] = 10
    
    # Configuración por defecto
    if settings_module is None:
        settings_module = 'globals'
    
    # Cargar configuración
    app.config.from_object(settings_module)

    # Configuración SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Si estamos en modo testing, asegurarnos de que algunas configuraciones críticas están correctas
    if settings_module == 'testing':
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        
        # Crear directorios temporales para tests si no existen
        for dir_path in [
            app.config['PUBLIC_FILE_DIR']
        ]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    db.init_app(app)

    jwt = JWTManager(app)

    CORS(
       app,
       resources={r"/api/*": {"origins": "*"}},
       allow_headers=["Content-Type", "Authorization"],
       supports_credentials=True
    )
    
    if not os.path.exists(DEBUG_PATH): os.makedirs(DEBUG_PATH)
    
    app.debug = DEBUG
    app.jinja_env.auto_reload = DEBUG
    
    app.config['API_TITLE'] = API_TITLE
    app.config['API_VERSION'] = API_VERSION
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = SWAGGER_URL
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
        
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

    ## NotImplementedError
    
    @app.errorhandler(NotImplementedError)
    def handle_not_implemented_error(error):
        response = {
            "error_message": str(error),
            "code": 501,
            "status": "Not Implemented"
        }
        return jsonify(response), 501

    api = Api(app)

    api.spec.components.security_scheme(
        'jwt', {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT', 'x-bearerInfoFunc': 'app.decode_token'}
    )

    def getApiPrefix(url): return f"{API_PREFIX}/{url}"
    
    #Routes    
    api.register_blueprint(UserBluprint, url_prefix=getApiPrefix('user'))
    api.register_blueprint(GroupBluprint, url_prefix=getApiPrefix('group'))
    api.register_blueprint(DemandBluprint, url_prefix=getApiPrefix('demand'))

    #api.register_blueprint(VersionBluprint, url_prefix=VERSION_ENDPOINT)    
    
    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        import models
        db.create_all()
    app.run(threaded=True, host="0.0.0.0", port=PORT, debug=DEBUG, use_reloader=DEBUG)