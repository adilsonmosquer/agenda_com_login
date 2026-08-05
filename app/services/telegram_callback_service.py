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

        elif acao == "pendente":

            evento = TelegramEventService.marcar_pendente(
                evento_id
            )

            if not evento:

                return (
                    False,
                    "Evento não encontrado.",
                )

            return (
                True,
                f"📌 <b>{evento.horario}</b>\n\n"
                f"{evento.descricao}\n\n"
                "Evento marcado como pendente."
            )

        elif acao == "excluir":

            sucesso = TelegramEventService.excluir(
                evento_id
            )

            if not sucesso:

                return (
                    False,
                    "Evento não encontrado.",
                )

            return (
                True,
                "🗑 Evento excluído."
            )

        elif acao == "adiar":

            return (
                False,
                "⏰ Função disponível na versão 1.1."
            )

        return (
            False,
            "Comando desconhecido."
        )