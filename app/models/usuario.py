from flask_login import UserMixin

from db import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    nome = db.Column(
        db.String(100),
        nullable=False,
    )

    usuario = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
    )

    senha_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    administrador = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )
