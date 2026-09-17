import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-jwt-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "database", "invoice.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash"
    )

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv(
            "MAIL_PORT",
            587
        )
    )

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    GOOGLE_DRIVE_INCOMING_FOLDER_ID=os.getenv(
        "GOOGLE_DRIVE_INCOMING_FOLDER_ID"
    )

    GOOGLE_DRIVE_FAILED_FOLDER_ID=os.getenv(
            "GOOGLE_DRIVE_FAILED_FOLDER_ID"
    )

    GOOGLE_DRIVE_DUPLICATE_FOLDER_ID=os.getenv(
            "GOOGLE_DRIVE_DUPLICATE_FOLDER_ID"
    )

    GOOGLE_DRIVE_COMPLETED_FOLDER_ID=os.getenv(
            "GOOGLE_DRIVE_COMPLETED_FOLDER_ID"
    )

    GOOGLE_DRIVE_PROCESSING_FOLDER_ID=os.getenv(
            "GOOGLE_DRIVE_PROCESSING_FOLDER_ID"
    )