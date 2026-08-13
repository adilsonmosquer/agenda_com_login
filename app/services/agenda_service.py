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


def formatar_data_cpex(data):

    return (
        f"{data.day:02d}/"
        f"{MESES[data.month]}/"
        f"{str(data.year)[2:]}"
    )


def data_hoje_cpex():

    return formatar_data_cpex(
        datetime.now()
    )


def obter_eventos_dia(data):

    data_cpex = formatar_data_cpex(data)

    eventos = (
        CronogramaItem.query
        .filter(
            CronogramaItem.data == data_cpex
        )
        .order_by(
            CronogramaItem.horario
        )
        .all()
    )

    hoje = datetime.now().date()
    data_selecionada = data.date()

    agora = datetime.now().strftime("%H:%M")

    proximo_encontrado = False

    for evento in eventos:

        if evento.concluido:

            evento.status = "Concluído"

        elif not evento.horario:

            evento.status = "Pendente"

        elif data_selecionada < hoje:

            evento.status = "Atrasado"

        elif data_selecionada > hoje:

            evento.status = "Pendente"

        elif evento.horario < agora:

            evento.status = "Atrasado"

        elif not proximo_encontrado:

            evento.status = "Próximo"

            proximo_encontrado = True

        else:

            evento.status = "Pendente"

    return eventos


def obter_eventos_hoje():

    return obter_eventos_dia(
        datetime.now()
    )