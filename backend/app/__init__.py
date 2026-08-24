from flask import Flask 
from app.config import Config
from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.cors import cors

from app.routes.auth import auth_bp
from app.routes.vendors import vendor_bp
from app.routes.invoices import invoice_bp
from app.routes.verification import verification_bp
from app.routes.processing import processing_log_bp
from app.routes.email_logs import email_log_bp
from app.routes.reminders import reminder_bp
from app.routes.dashboard import dashboard_bp


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
    from app.models.verifications import Verification
    from app.models.processing_log import ProcessingLog

    app.register_blueprint(auth_bp,url_prefix="/api/auth")
    app.register_blueprint(vendor_bp,url_prefix="/api/vendors")
    app.register_blueprint(invoice_bp,url_prefix="/api/invoices")
    app.register_blueprint(verification_bp,url_prefix="/api/verification")
    app.register_blueprint(processing_log_bp,url_prefix="/api/processing-logs")
    app.register_blueprint(email_log_bp,url_prefix="/api/email-logs")
    app.register_blueprint(reminder_bp,url_prefix="/api/reminders")
    app.register_blueprint(dashboard_bp,url_prefix="/api/dashboard")

    with app.app_context():
        print("DATABASE:", app.config["SQLALCHEMY_DATABASE_URI"])
        print("TABLES:", db.metadata.tables.keys())
        db.create_all()


    return app
