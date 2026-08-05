from datetime import datetime

from app.models.cronograma_item import CronogramaItem


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


def data_hoje_cpex():

    hoje = datetime.now()

    return (
        f"{hoje.day:02d}/"
        f"{MESES[hoje.month]}/"
        f"{str(hoje.year)[2:]}"
    )


def obter_eventos_hoje():

    eventos = (

        CronogramaItem.query

        .filter(
            CronogramaItem.data == data_hoje_cpex()
        )

        .order_by(
            CronogramaItem.horario
        )

        .all()

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