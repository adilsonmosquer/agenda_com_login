import os


class Config:

    SECRET_KEY = "agenda_operacional"

    SQLALCHEMY_DATABASE_URI = "sqlite:///agenda.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB

    ALLOWED_EXTENSIONS = {"xlsx", "xls", "pdf"}
