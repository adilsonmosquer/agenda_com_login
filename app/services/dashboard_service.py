from app.models.cronograma_item import CronogramaItem


def obter_dados_dashboard():

    eventos = CronogramaItem.query.order_by(
        CronogramaItem.data, CronogramaItem.horario
    ).all()

    if eventos:
        proximo_evento = eventos[0].descricao
        horario_proximo = f"{eventos[0].data} {eventos[0].horario}"
    else:
        proximo_evento = "Nenhum evento"
        horario_proximo = "--"

    pendentes = sum(1 for evento in eventos if not evento.concluido)

    return {
        "eventos_hoje": len(eventos),
        "proximo_evento": proximo_evento,
        "horario_proximo": horario_proximo,
        "pendentes": pendentes,
        "eventos": eventos,
    }
