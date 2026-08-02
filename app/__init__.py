from flask import Flask
from flask_migrate import Migrate

from config import Config
from db import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importa os modelos
    from app.models.importacao import Importacao
    from app.models.cronograma_item import CronogramaItem

    # Registra os blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.importacoes import importacoes_bp
    from app.routes.agenda import agenda_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(importacoes_bp)
    app.register_blueprint(agenda_bp)

    return app
