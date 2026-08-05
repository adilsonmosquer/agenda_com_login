from app.services.telegram_event_service import (
    TelegramEventService,
)


class TelegramCallbackService:

    @staticmethod
    def processar(acao, evento_id):

        if acao == "concluir":

            evento = TelegramEventService.concluir(
                evento_id
            )

            if not evento:

                return (
                    False,
                    "Evento não encontrado.",
                )

            return (
                True,
                f"✅ <b>{evento.horario}</b>\n\n"
                f"{evento.descricao}\n\n"
                "Evento concluído."
            )

        if acao == "ocultar":

            evento = TelegramEventService.ocultar(
                evento_id,
                usuario="Telegram",
                motivo="Ocultado pelo usuário",
            )

            if not evento:

                return (
                    False,
                    "Evento não encontrado.",
                )

            return (
                True,
                "🙈 <b>Evento ocultado.</b>\n\n"
                "Ele não aparecerá mais na Agenda, "
                "Dashboard, Tela TV e Telegram.\n\n"
                "Pode ser restaurado posteriormente."
            )

        if acao == "restaurar":

            evento = TelegramEventService.restaurar(
                evento_id,
                usuario="Telegram",
            )

            if not evento:

                return (
                    False,
                    "Evento não encontrado.",
                )

            return (
                True,
                f"♻️ <b>{evento.horario}</b>\n\n"
                f"{evento.descricao}\n\n"
                "Evento restaurado."
            )

        if acao == "adiar":

            return (
                False,
                "⏰ Função disponível na Sprint 9.4."
            )

        return (
            False,
            "Comando desconhecido."
        )