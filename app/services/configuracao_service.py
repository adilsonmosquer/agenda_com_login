from flask import current_app

from app.models.configuracao import Configuracao
from db import db


class ConfiguracaoService:

    @staticmethod
    def get(chave, default=None):

        config = Configuracao.query.filter_by(
            chave=chave
        ).first()

        if config:
            return config.valor_atual

        return default

    @staticmethod
    def set(chave, valor):

        config = Configuracao.query.filter_by(
            chave=chave
        ).first()

        if config:

            config.valor_atual = str(valor)

        else:

            config = Configuracao(

                categoria="Sistema",

                chave=chave,

                valor_atual=str(valor),

                valor_padrao=str(valor),

                tipo="texto",

                descricao="",

                editavel=True,

                obrigatorio=False,

                reiniciar=False,

            )

            db.session.add(config)

        db.session.commit()

        return config

    @staticmethod
    def listar():

        return Configuracao.query.order_by(

            Configuracao.categoria,

            Configuracao.chave,

        ).all()

    @staticmethod
    def existe(chave):

        return (

            Configuracao.query.filter_by(

                chave=chave

            ).count()

            > 0

        )

    @staticmethod
    def criar_padroes():

        padroes = [

            # ==========================
            # Telegram
            # ==========================

            {
                "categoria": "Telegram",
                "chave": "telegram_token",
                "valor": current_app.config.get(
                    "TELEGRAM_TOKEN",
                    "",
                ),
                "tipo": "texto",
                "descricao": "Token do Bot",
            },

            {
                "categoria": "Telegram",
                "chave": "telegram_chat_id",
                "valor": current_app.config.get(
                    "TELEGRAM_CHAT_ID",
                    "",
                ),
                "tipo": "texto",
                "descricao": "Chat ID",
            },

            # ==========================
            # Agenda
            # ==========================

            {
                "categoria": "Agenda",
                "chave": "hora_resumo",
                "valor": "08:00",
                "tipo": "hora",
                "descricao": "Horário do resumo diário",
            },

            {
                "categoria": "Agenda",
                "chave": "antecedencia_lembrete",
                "valor": "15",
                "tipo": "numero",
                "descricao": "Antecedência dos lembretes (minutos)",
            },

            # ==========================
            # Tela TV
            # ==========================

            {
                "categoria": "Tela TV",
                "chave": "tempo_tela",
                "valor": "60",
                "tipo": "numero",
                "descricao": "Tempo de atualização da Tela TV (segundos)",
            },

            # ==========================
            # Backup
            # ==========================

            {
                "categoria": "Backup",
                "chave": "hora_backup",
                "valor": "02:00",
                "tipo": "hora",
                "descricao": "Horário do backup automático",
            },

        ]

        alterado = False

        for item in padroes:

            config = Configuracao.query.filter_by(
                chave=item["chave"]
            ).first()

            if config is None:

                db.session.add(

                    Configuracao(

                        categoria=item["categoria"],

                        chave=item["chave"],

                        valor_atual=item["valor"],

                        valor_padrao=item["valor"],

                        tipo=item["tipo"],

                        descricao=item["descricao"],

                        editavel=True,

                        obrigatorio=False,

                        reiniciar=False,

                    )

                )

                alterado = True

            else:

                # Migração automática do .env para o banco.
                # Só preenche quando o banco estiver vazio.

                if (
                    not config.valor_atual
                    and item["valor"]
                ):

                    config.valor_atual = item["valor"]

                    config.valor_padrao = item["valor"]

                    alterado = True

        if alterado:

            db.session.commit()