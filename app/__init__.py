from flask import Flask



def create_app():
    app = Flask(__name__)
    
    from app.api import api
    app.register_blueprint(api.blueprint)

    return app
