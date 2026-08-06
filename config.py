import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "agenda_operacional")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///agenda.db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        os.getcwd(),
        "uploads",
    )

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "xlsx",
        "xls",
        "pdf",
    }

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
