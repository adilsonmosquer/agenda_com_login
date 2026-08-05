from db import db


class CronogramaItem(db.Model):
    __tablename__ = "cronograma_itens"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    importacao_id = db.Column(
        db.Integer,
        db.ForeignKey("importacoes.id"),
        nullable=True,
    )

    origem = db.Column(
        db.String(20),
        nullable=False,
        default="IMPORTACAO",
    )

    data = db.Column(
        db.String(10),
        nullable=False,
    )

    dia_semana = db.Column(
        db.String(20),
    )

    horario = db.Column(
        db.String(5),
        nullable=False,
    )

    descricao = db.Column(
        db.String(300),
        nullable=False,
    )

    executor = db.Column(
        db.String(100),
    )

    cor = db.Column(
        db.String(20),
    )

    status = db.Column(
        db.String(20),
        default="Pendente",
    )

    concluido = db.Column(
        db.Boolean,
        default=False,
    )

    lembrete_enviado = db.Column(
    db.Boolean,
    nullable=False,
    default=False,
    )

    observacao = db.Column(
        db.String(300),
    )

    importacao = db.relationship(
        "Importacao",
        back_populates="itens",
    )