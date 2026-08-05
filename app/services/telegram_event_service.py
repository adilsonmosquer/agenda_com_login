from app import db
from app.models.cronograma_item import CronogramaItem


class TelegramEventService:

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
    def ocultar(
        evento_id,
        usuario="Telegram",
        motivo="Ocultado pelo usuário",
    ):

        evento = TelegramEventService.obter(evento_id)

        if not evento:

            return None

        evento.ocultar(
            usuario=usuario,
            motivo=motivo,
        )

        db.session.commit()

        return evento

    @staticmethod
    def restaurar(
        evento_id,
        usuario="Sistema",
    ):

        evento = TelegramEventService.obter(evento_id)

        if not evento:

            return None

        evento.restaurar(
            usuario=usuario,
        )

        db.session.commit()

        return evento

    @staticmethod
    def listar_ativos():

        return (
            CronogramaItem.query
            .filter_by(
                ativo=True
            )
            .order_by(
                CronogramaItem.data,
                CronogramaItem.horario,
            )
            .all()
        )

    @staticmethod
    def listar_ocultados():

        return (
            CronogramaItem.query
            .filter_by(
                ativo=False
            )
            .order_by(
                CronogramaItem.data,
                CronogramaItem.horario,
            )
            .all()
        )