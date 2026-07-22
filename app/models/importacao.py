from datetime import datetime

from db import db


class Importacao(db.Model):
    __tablename__ = "importacoes"

    id = db.Column(db.Integer, primary_key=True)

    arquivo = db.Column(db.String(255), nullable=False)

    periodo = db.Column(db.String(20), nullable=False, default="Não informado")

    tipo = db.Column(db.String(20), nullable=False)

    data_importacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    registros = db.Column(db.Integer, default=0)

    ativa = db.Column(db.Boolean, default=False, nullable=False)

    observacao = db.Column(db.String(300))

    itens = db.relationship(
        "CronogramaItem", back_populates="importacao", cascade="all, delete-orphan"
    )
