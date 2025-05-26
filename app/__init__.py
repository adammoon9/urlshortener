from flask import Flask
from .extensions import db, migrate
# from .models.url import URL
from .routes import main

def create_app(config_object=None):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)

    return app
