from datetime import datetime

import requests

from app.models.cronograma_item import CronogramaItem
from app.services.configuracao_service import ConfiguracaoService


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


class TelegramService:

    @staticmethod
    def data_hoje():

        hoje = datetime.now()

        return (
            f"{hoje.day:02d}/"
            f"{MESES[hoje.month]}/"
            f"{str(hoje.year)[2:]}"
        )

    @staticmethod
    def montar_mensagem(eventos, sistema, hoje):

        pendentes = sum(
            1
            for evento in eventos
            if not evento.concluido
        )

        concluidos = sum(
            1
            for evento in eventos
            if evento.concluido
        )

        mensagem = []

        mensagem.append(
            "📅 Agenda Operacional CPEx"
        )

        mensagem.append("")

        mensagem.append(
            f"🔹 SISTEMA: {sistema}"
        )

        mensagem.append(
            f"📆 {hoje}"
        )

        mensagem.append(
            "──────────────────"
        )

        for evento in eventos:

            if evento.horario:

                mensagem.append(
                    f"🕒 {evento.horario}"
                )

            else:

                mensagem.append(
                    "🕒 Sem horário"
                )

            mensagem.append(
                evento.descricao
            )

            if evento.executor:

                mensagem.append(
                    f"👤 {evento.executor}"
                )

            if evento.concluido:

                mensagem.append(
                    "✅ Concluído"
                )

            mensagem.append("")

        mensagem.append(
            "──────────────────"
        )

        mensagem.append(
            f"Total: {len(eventos)}"
        )

        mensagem.append(
            f"Pendentes: {pendentes}"
        )

        mensagem.append(
            f"Concluídos: {concluidos}"
        )

        return "\n".join(mensagem)

    @staticmethod
    def enviar_texto(texto):

        token = ConfiguracaoService.get(
            "telegram_token"
        )

        chat_id = ConfiguracaoService.get(
            "telegram_chat_id"
        )

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

            "text": texto,

        }

        resposta = requests.post(

            url,

            json=payload,

            timeout=15,

        )

        resposta.raise_for_status()

        return resposta.ok

    @staticmethod
    def enviar():

        hoje = TelegramService.data_hoje()

        eventos = (
            CronogramaItem.query
            .filter_by(data=hoje)
            .order_by(CronogramaItem.horario)
            .all()
        )

        if not eventos:

            return TelegramService.enviar_texto(
                (
                    "📅 Agenda Operacional CPEx\n\n"
                    f"📆 {hoje}\n\n"
                    "Nenhum evento para hoje."
                )
            )

        sistemas = (
            "SIPPES",
            "SIAPPES",
        )

        enviados = 0

        for sistema in sistemas:

            eventos_sistema = [
                evento
                for evento in eventos
                if evento.sistema == sistema
            ]

            if not eventos_sistema:

                continue

            mensagem = TelegramService.montar_mensagem(
                eventos_sistema,
                sistema,
                hoje,
            )

            TelegramService.enviar_texto(
                mensagem
            )

            enviados += 1

        return enviados