from app.models.configuracao import Configuracao
from db import db


class ConfiguracaoService:

    @staticmethod
    def obter(chave, padrao=None):

        configuracao = Configuracao.query.filter_by(
            chave=chave
        ).first()

        if configuracao:

            return configuracao.valor_atual

        return padrao

    @staticmethod
    def definir(chave, valor):

        configuracao = Configuracao.query.filter_by(
            chave=chave
        ).first()

        if not configuracao:

            raise ValueError(
                f"Configuração '{chave}' não encontrada."
            )

        configuracao.valor_atual = str(valor)

        db.session.commit()

    @staticmethod
    def listar():

        return (
            Configuracao.query
            .order_by(
                Configuracao.categoria,
                Configuracao.chave,
            )
            .all()
        )

    @staticmethod
    def existe(chave):

        return (
            Configuracao.query.filter_by(
                chave=chave
            ).first()
            is not None
        )

    @staticmethod
    def criar(
        categoria,
        chave,
        valor,
        tipo,
        descricao="",
        editavel=True,
        obrigatorio=False,
        reiniciar=False,
    ):

        if ConfiguracaoService.existe(chave):

            return

        configuracao = Configuracao(

            categoria=categoria,

            chave=chave,

            valor_atual=str(valor),

            valor_padrao=str(valor),

            tipo=tipo,

            descricao=descricao,

            editavel=editavel,

            obrigatorio=obrigatorio,

            reiniciar=reiniciar,

        )

        db.session.add(configuracao)

        db.session.commit()