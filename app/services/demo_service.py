from datetime import datetime, timedelta

from db import db
from app.models.importacao import Importacao
from app.models.cronograma_item import CronogramaItem


class DemoService:

    @staticmethod
    def popular():

        CronogramaItem.query.delete()
        Importacao.query.delete()

        importacao = Importacao(
            arquivo="Cronograma_Demo.pdf",
            periodo="08/2026",
            tipo="PDF",
            data_importacao=datetime.now(),
            registros=0,
            ativa=True,
            observacao="Base de demonstração"
        )

        db.session.add(importacao)
        db.session.flush()

        eventos = [
            ("08:00", "Conferência Inicial", "ST Adilson"),
            ("09:00", "Atualização SIAPPES", "Seção Sistemas"),
            ("10:30", "Conferência Financeira", "Tesouraria"),
            ("14:00", "Reunião da Chefia", "Chefe da Seção"),
            ("16:00", "Encerramento do Expediente", ""),
        ]

        hoje = datetime.now()

        total = 0

        for dia in range(7):

            data = (hoje + timedelta(days=dia)).strftime("%d/%m/%Y")

            for horario, descricao, executor in eventos:

                item = CronogramaItem(
                    importacao_id=importacao.id,
                    data=data,
                    horario=horario,
                    descricao=descricao,
                    executor=executor,
                    concluido=False,
                )

                db.session.add(item)
                total += 1

        importacao.registros = total

        db.session.commit()