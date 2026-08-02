from datetime import datetime

import requests
from flask import current_app

from app.models.cronograma_item import CronogramaItem


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
            return "📅 Agenda Operacional\n\n" "Nenhum evento para hoje."

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

        token = current_app.config["TELEGRAM_TOKEN"]
        chat_id = current_app.config["TELEGRAM_CHAT_ID"]

        if not token:
            raise Exception("TELEGRAM_TOKEN não configurado.")

        if not chat_id:
            raise Exception("TELEGRAM_CHAT_ID não configurado.")

        url = f"https://api.telegram.org/bot{token}/sendMessage"

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
