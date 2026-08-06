from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from db import db

migrate = Migrate()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar a Agenda."
    login_manager.login_message_category = "warning"

    # ==========================
    # Modelos
    # ==========================

    from app.models.importacao import Importacao
    from app.models.cronograma_item import CronogramaItem
    from app.models.configuracao import Configuracao
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # ==========================
    # Services
    # ==========================

    from app.services.configuracao_service import ConfiguracaoService
    from app.services.usuario_service import UsuarioService

    # ==========================
    # Scheduler
    # ==========================

    from app.scheduler.jobs import registrar_jobs

    # ==========================
    # Blueprints
    # ==========================

    from app.routes.dashboard import dashboard_bp
    from app.routes.importacoes import importacoes_bp
    from app.routes.agenda import agenda_bp
    from app.routes.evento import evento_bp
    from app.routes.configuracoes import configuracoes_bp
    from app.routes.tv import tv_bp
    from app.routes.telegram import bp
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(importacoes_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(evento_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(tv_bp)
    app.register_blueprint(bp)

    # ==========================
    # Inicialização
    # ==========================

    with app.app_context():

        ConfiguracaoService.criar_padroes()

        UsuarioService.criar_admin()

    registrar_jobs(app)

    return app
