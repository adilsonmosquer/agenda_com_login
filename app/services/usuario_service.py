from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from db import db
from app.models.usuario import Usuario


class UsuarioService:

    @staticmethod
    def criar_admin():

        if Usuario.query.first():
            return

        admin = Usuario(
            nome="Administrador",
            usuario="admin",
            senha_hash=generate_password_hash("admin123"),
            ativo=True,
            administrador=True,
        )

        db.session.add(admin)
        db.session.commit()

    @staticmethod
    def alterar_senha(
        usuario,
        senha_atual,
        nova_senha,
    ):

        if not check_password_hash(
            usuario.senha_hash,
            senha_atual,
        ):
            return False, "Senha atual incorreta."

        usuario.senha_hash = generate_password_hash(
            nova_senha
        )

        db.session.commit()

        return True, "Senha alterada com sucesso."
