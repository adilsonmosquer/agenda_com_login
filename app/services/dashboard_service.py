from app.models.cronograma_item import CronogramaItem


def obter_dados_dashboard():

    itens = CronogramaItem.query.order_by(
        CronogramaItem.data, CronogramaItem.horario
    ).all()

    if itens:
        proximo_evento = itens[0].descricao
        horario_proximo = itens[0].horario
    else:
        proximo_evento = "Nenhum evento"
        horario_proximo = "--:--"

    pendentes = sum(1 for item in itens if not item.concluido)

    return {
        "eventos_hoje": len(itens),
        "proximo_evento": proximo_evento,
        "horario_proximo": horario_proximo,
        "pendentes": pendentes,
        "eventos": itens,
    }
