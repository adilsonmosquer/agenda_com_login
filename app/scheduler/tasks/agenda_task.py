from app.services.telegram_service import TelegramService


def executar():

    TelegramService.enviar()

    print(
        "[AgendaTask] Agenda enviada com sucesso."
    )