from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)

from app.services.dashboard_service import obter_dados_dashboard
from app.services.telegram_service import TelegramService
from app.services.demo_service import DemoService

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


@dashboard_bp.route("/")
def dashboard():

    dados = obter_dados_dashboard()

    return render_template(
        "dashboard.html",
        **dados,
    )


@dashboard_bp.route("/telegram/enviar")
def enviar_telegram():

    try:

        TelegramService.enviar()

        flash(
            "Agenda enviada ao Telegram.",
            "success",
        )

    except Exception as erro:

        flash(
            str(erro),
            "danger",
        )

    return redirect(url_for("dashboard.dashboard"))
@dashboard_bp.route("/demo/popular")
def popular_demo():

    DemoService.popular()

    flash(
        "Banco de demonstração criado com sucesso.",
        "success",
    )

    return redirect(url_for("dashboard.dashboard"))
