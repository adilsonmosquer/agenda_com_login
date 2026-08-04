from datetime import datetime

import requests

from app.models.cronograma_item import CronogramaItem
from app.services.configuracao_service import ConfiguracaoService


class TelegramService:

    @staticmethod
    def montar_mensagem():

        hoje = datetime.now().strftime("%d/%m/%Y")

        eventos = (
            CronogramaItem.query.filter_by(data=hoje)
            .order_by(CronogramaItem.horario)
            .all()
        )

        if not eventos:
            return (
                "📅 Agenda Operacional\n\n"
                "Nenhum evento para hoje."
            )

        mensagem = []

        mensagem.append("📅 Agenda Operacional")
        mensagem.append("")
        mensagem.append(f"📆 {hoje}")
        mensagem.append("──────────────────")

        for evento in eventos:

            mensagem.append(f"🕒 {evento.horario}")
            mensagem.append(evento.descricao)

            if evento.executor:
                mensagem.append(f"👤 {evento.executor}")

            mensagem.append("")

        mensagem.append("──────────────────")
        mensagem.append(f"Total de eventos: {len(eventos)}")

        return "\n".join(mensagem)

    @staticmethod
    def enviar():

        token = ConfiguracaoService.get("telegram_token")
        chat_id = ConfiguracaoService.get("telegram_chat_id")

        if not token:
            raise Exception(
                "Token do Telegram não configurado."
            )

        if not chat_id:
            raise Exception(
                "Chat ID do Telegram não configurado."
            )

        url = (
            f"https://api.telegram.org/bot{token}/sendMessage"
        )

        payload = {
            "chat_id": chat_id,
            "text": TelegramService.montar_mensagem(),
        }

        resposta = requests.post(
            url,
            json=payload,
            timeout=15,
        )

        resposta.raise_for_status()

        return True