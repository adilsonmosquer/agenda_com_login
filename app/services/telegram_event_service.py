from datetime import datetime

from app.models.cronograma_item import CronogramaItem
from db import db


MESES = {
    1: "jan",
    2: "fev",
    3: "mar",
    4: "abr",
    5: "mai",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "set",
    10: "out",
    11: "nov",
    12: "dez",
}


class TelegramEventService:

    @staticmethod
    def data_hoje():

        hoje = datetime.now()

        return (
            f"{hoje.day:02d}/"
            f"{MESES[hoje.month]}/"
            f"{str(hoje.year)[2:]}"
        )

    @staticmethod
    def obter(evento_id):

        return CronogramaItem.query.get(evento_id)

    @staticmethod
    def concluir(evento_id):

        evento = TelegramEventService.obter(evento_id)

        if not evento:
            return None

        evento.concluido = True

        db.session.commit()

        return evento

    @staticmethod
    def marcar_pendente(evento_id):

        evento = TelegramEventService.obter(evento_id)

        if not evento:
            return None

        evento.concluido = False

        db.session.commit()

        return evento

    @staticmethod
    def excluir(evento_id):

        evento = TelegramEventService.obter(evento_id)

        if not evento:
            return False

        db.session.delete(evento)

        db.session.commit()

        return True

    @staticmethod
    def listar_eventos_hoje():

        return (
            CronogramaItem.query
            .filter(
                CronogramaItem.data == TelegramEventService.data_hoje()
            )
            .order_by(
                CronogramaItem.horario
            )
            .all()
        )

    @staticmethod
    def listar_pendentes():

        return [
            evento
            for evento in TelegramEventService.listar_eventos_hoje()
            if not evento.concluido
        ]

    @staticmethod
    def listar_concluidos():

        return [
            evento
            for evento in TelegramEventService.listar_eventos_hoje()
            if evento.concluido
        ]

    @staticmethod
    def marcar_lembrete_enviado(evento_id):

        evento = TelegramEventService.obter(evento_id)

        if not evento:
            return

        evento.lembrete_enviado = True

        db.session.commit()

    @staticmethod
    def limpar_lembretes():

        eventos = TelegramEventService.listar_eventos_hoje()

        for evento in eventos:

            evento.lembrete_enviado = False

        db.session.commit()