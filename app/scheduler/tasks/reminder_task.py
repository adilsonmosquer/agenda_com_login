from datetime import datetime, timedelta

from db import db
from app.models.cronograma_item import CronogramaItem
from app.services.telegram_service import TelegramService


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


def data_hoje():

    hoje = datetime.now()

    return (
        f"{hoje.day:02d}/"
        f"{MESES[hoje.month]}/"
        f"{str(hoje.year)[2:]}"
    )


def executar():

    agora = datetime.now()

    horario = (
        agora + timedelta(minutes=15)
    ).strftime("%H:%M")

    eventos = (
        CronogramaItem.query
        .filter(
            CronogramaItem.data == data_hoje(),
            CronogramaItem.horario == horario,
            CronogramaItem.concluido == False,
            CronogramaItem.lembrete_enviado == False,
        )
        .all()
    )

    enviados = 0

    for evento in eventos:

        texto = (
            "⏰ Lembrete\n\n"
            f"Horário: {evento.horario}\n"
            f"Evento: {evento.descricao}"
        )

        token = TelegramService.enviar_texto(
            texto
        )

        if token:

            evento.lembrete_enviado = True

            enviados += 1

    db.session.commit()

    if enviados:

        print(
            f"[ReminderTask] {enviados} lembrete(s) enviado(s)."
        )

    return enviados