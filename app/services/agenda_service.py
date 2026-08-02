from datetime import date, datetime

from app.models.cronograma_item import CronogramaItem


def obter_eventos_hoje():

    hoje = date.today().strftime("%d/%m/%Y")

    eventos = (
        CronogramaItem.query.filter_by(data=hoje).order_by(CronogramaItem.horario).all()
    )

    agora = datetime.now().strftime("%H:%M")

    proximo_encontrado = False

    for evento in eventos:

        if evento.concluido:
            evento.situacao = "concluido"

        elif evento.horario < agora:
            evento.situacao = "atrasado"

        elif not proximo_encontrado:
            evento.situacao = "proximo"
            proximo_encontrado = True

        else:
            evento.situacao = "pendente"

    return eventos
