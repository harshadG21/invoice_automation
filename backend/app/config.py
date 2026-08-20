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