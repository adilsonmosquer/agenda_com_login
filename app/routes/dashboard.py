from flask_login import login_required
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)

from app.services.dashboard_service import (
    obter_dados_dashboard,
    concluir_evento,
    marcar_pendente,
    excluir_evento,
)

from app.services.telegram_service import TelegramService
from app.services.demo_service import DemoService

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


@dashboard_bp.route("/")
@login_required
def dashboard():

    dados = obter_dados_dashboard()

    return render_template(
        "dashboard.html",
        **dados,
    )


@dashboard_bp.route("/telegram/enviar")
@login_required
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

    return redirect(
        url_for("dashboard.dashboard")
    )


@dashboard_bp.route("/demo/popular")
@login_required
def popular_demo():

    DemoService.popular()

    flash(
        "Banco de demonstração criado com sucesso.",
        "success",
    )

    return redirect(
        url_for("dashboard.dashboard")
    )


@dashboard_bp.post("/evento/<int:evento_id>/concluir")
@login_required
def concluir(evento_id):

    concluir_evento(evento_id)

    flash(
        "Evento concluído.",
        "success",
    )

    return redirect(
        url_for("dashboard.dashboard")
    )


@dashboard_bp.post("/evento/<int:evento_id>/pendente")
@login_required
def pendente(evento_id):

    marcar_pendente(evento_id)

    flash(
        "Evento marcado como pendente.",
        "warning",
    )

    return redirect(
        url_for("dashboard.dashboard")
    )


@dashboard_bp.post("/evento/<int:evento_id>/excluir")
@login_required
def excluir(evento_id):

    excluir_evento(evento_id)

    flash(
        "Evento excluído.",
        "success",
    )

    return redirect(
        url_for("dashboard.dashboard")
    )
