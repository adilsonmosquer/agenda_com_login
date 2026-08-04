from db import db
from app.models.cronograma_item import CronogramaItem


class EventoService:

    @staticmethod
    def concluir(evento):

        evento.concluido = True
        evento.status = "Concluído"

        db.session.commit()


    @staticmethod
    def reabrir(evento):

        evento.concluido = False
        evento.status = "Pendente"

        db.session.commit()


    @staticmethod
    def alternar_conclusao(evento):

        if evento.concluido:

            EventoService.reabrir(evento)

        else:

            EventoService.concluir(evento)


    @staticmethod
    def excluir(evento):

        if evento.origem != "MANUAL":

            return False

        db.session.delete(evento)

        db.session.commit()

        return True