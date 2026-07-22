from app.services.telegram_service import enviar_mensagem_telegram


def notificar_importacao(importacao):

    mensagem = f"""
📅 Agenda Operacional

Novo cronograma importado.

Período: {importacao.periodo}

Arquivo: {importacao.arquivo}

Registros: {importacao.registros}
"""

    enviar_mensagem_telegram(mensagem)
