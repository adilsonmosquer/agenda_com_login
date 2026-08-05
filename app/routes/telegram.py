import requests

from flask import Blueprint, request

from app.services.configuracao_service import ConfiguracaoService
from app.services.telegram_callback_service import TelegramCallbackService

bp = Blueprint(
    "telegram",
    __name__,
)


def token():

    return ConfiguracaoService.get(
        "telegram_token"
    )


def responder_callback(callback_id, texto):

    requests.post(

        f"https://api.telegram.org/bot{token()}/answerCallbackQuery",

        json={

            "callback_query_id": callback_id,

            "text": texto,

            "show_alert": False,

        },

        timeout=15,

    )


def editar_mensagem(chat_id, message_id, texto):

    requests.post(

        f"https://api.telegram.org/bot{token()}/editMessageText",

        json={

            "chat_id": chat_id,

            "message_id": message_id,

            "text": texto,

            "parse_mode": "HTML",

        },

        timeout=15,

    )


@bp.route(
    "/telegram/webhook",
    methods=["POST"],
)
def webhook():

    dados = request.get_json()

    callback = dados.get("callback_query")

    if not callback:

        return "OK"

    callback_id = callback["id"]

    acao, evento_id = callback["data"].split(":")

    chat_id = callback["message"]["chat"]["id"]

    message_id = callback["message"]["message_id"]

    sucesso, mensagem = TelegramCallbackService.processar(

        acao,

        int(evento_id),

    )

    editar_mensagem(

        chat_id,

        message_id,

        mensagem,

    )

    responder_callback(

        callback_id,

        "OK" if sucesso else mensagem,

    )

    return "OK"