class Config:
    SECRET_KEY = "agenda_operacional"

    SQLALCHEMY_DATABASE_URI = "sqlite:///agenda.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
