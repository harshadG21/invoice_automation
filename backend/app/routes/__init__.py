from flask import Flask

from app.config import Config

from app.extensions.database import db
from app.extensions.jwt import jwt 
from app.extensions.cors import cors

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    jwt.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/api/*":{
                "origins":app.config["FRONTEND_URL"]
            }
        }
    )

    return app