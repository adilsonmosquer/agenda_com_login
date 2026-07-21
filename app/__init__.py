from flask import Flask
from flask_migrate import Migrate

from config import Config
from db import db

# Importa os modelos para que o SQLAlchemy registre as tabelas
from app.models.importacao import Importacao
from app.models.cronograma_item import CronogramaItem

# Importa os blueprints
from app.routes.dashboard import dashboard_bp
from app.routes.importacoes import importacoes_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # Registra os blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(importacoes_bp)

    return app
