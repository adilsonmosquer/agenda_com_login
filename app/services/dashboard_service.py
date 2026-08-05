from datetime import datetime

from app.models.cronograma_item import CronogramaItem
from db import db


MESES = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}

MESES_TEXTO = {
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
        f"{MESES_TEXTO[hoje.month]}/"
        f"{str(hoje.year)[2:]}"
    )


def converter_data(data_texto):

    dia, mes, ano = data_texto.split("/")

    return datetime(
        2000 + int(ano),
        MESES[mes.lower()],
        int(dia),
    )


def obter_dados_dashboard():

    hoje_texto = data_hoje_cpex()

    hoje = converter_data(hoje_texto)

    todos = CronogramaItem.query.order_by(
        CronogramaItem.horario
    ).all()

    eventos_hoje = []

    proximos = []

    for evento in todos:

        try:

            data_evento = converter_data(
                evento.data
            )

        except Exception:

            continue

        if data_evento == hoje:

            eventos_hoje.append(evento)

        elif data_evento > hoje:

            proximos.append(
                (
                    data_evento,
                    evento,
                )
            )

    eventos_hoje.sort(
        key=lambda e: e.horario
    )

    proximos.sort(
        key=lambda p: (
            p[0],
            p[1].horario,
        )
    )

    if eventos_hoje:

        proximo = eventos_hoje[0]

    elif proximos:

        proximo = proximos[0][1]

    else:

        proximo = None

    if proximo:

        proximo_evento = proximo.descricao

        horario_proximo = (
            f"{proximo.data} {proximo.horario}"
        )

    else:

        proximo_evento = "Nenhum evento"

        horario_proximo = "--"

    pendentes = sum(
        1
        for evento in eventos_hoje
        if not evento.concluido
    )

    return {

        "eventos_hoje": len(eventos_hoje),

        "proximo_evento": proximo_evento,

        "horario_proximo": horario_proximo,

        "pendentes": pendentes,

        "eventos": eventos_hoje,

    }


def concluir_evento(evento_id):

    evento = CronogramaItem.query.get_or_404(
        evento_id
    )

    evento.concluido = True

    db.session.commit()


def marcar_pendente(evento_id):

    evento = CronogramaItem.query.get_or_404(
        evento_id
    )

    evento.concluido = False

    db.session.commit()


def excluir_evento(evento_id):

    evento = CronogramaItem.query.get_or_404(
        evento_id
    )

    db.session.delete(evento)

    db.session.commit()