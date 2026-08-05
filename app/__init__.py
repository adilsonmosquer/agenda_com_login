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

    # ==========================
    # Modelos
    # ==========================

    from app.models.importacao import Importacao
    from app.models.cronograma_item import CronogramaItem
    from app.models.configuracao import Configuracao

    # ==========================
    # Services
    # ==========================

    from app.services.configuracao_service import (
        ConfiguracaoService,
    )

    # ==========================
    # Blueprints
    # ==========================

    from app.routes.dashboard import dashboard_bp
    from app.routes.importacoes import importacoes_bp
    from app.routes.agenda import agenda_bp
    from app.routes.evento import evento_bp
    from app.routes.configuracoes import configuracoes_bp
    from app.routes.tv import tv_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(importacoes_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(evento_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(tv_bp)

    # ==========================
    # Inicialização
    # ==========================

    with app.app_context():

        ConfiguracaoService.criar_padroes()

    return app