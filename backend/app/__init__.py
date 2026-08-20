from flask import Flask 
from app.config import Config
from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.cors import cors

from app.routes.auth import auth_bp
from app.routes.vendors import vendor_bp

def create_app():
    app=Flask(__name__)

    #Load configurations
    app.config.from_object(Config)

    #Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources=({r"/api/*": {"origins": app.config["FRONTEND_URL"]}})
    )


    from app.models.user import User
    from app.models.vendor import Vendor
    from app.models.invoice import Invoice
    from app.models.email_log import EmailLog
    from app.models.verification import Verification
    from app.models.processing_log import ProcessingLog

    app.register_blueprint(auth_bp,url_prefix="/api/auth")
    app.register_blueprint(vendor_bp,url_prefix="/api/vendors")


    with app.app_context():
        print("DATABASE:", app.config["SQLALCHEMY_DATABASE_URI"])
        print("TABLES:", db.metadata.tables.keys())
        db.create_all()


    return app
