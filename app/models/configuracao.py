from db import db


class Configuracao(db.Model):
    __tablename__ = "configuracoes"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    categoria = db.Column(
        db.String(50),
        nullable=False,
    )

    chave = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    valor_atual = db.Column(
        db.String(500),
        nullable=False,
    )

    valor_padrao = db.Column(
        db.String(500),
        nullable=False,
    )

    tipo = db.Column(
        db.String(20),
        nullable=False,
    )

    descricao = db.Column(
        db.String(255),
    )

    editavel = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    obrigatorio = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    reiniciar = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    def __repr__(self):

        return (
            f"<Configuracao {self.chave}="
            f"{self.valor_atual}>"
        )