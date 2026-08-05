from flask import Blueprint, render_template

from app.services.dashboard_service import obter_dados_dashboard


tv_bp = Blueprint(
    "tv",
    __name__,
)


@tv_bp.route("/tv")
def painel_tv():

    dados = obter_dados_dashboard()

    return render_template(
        "tv.html",
        **dados,
    )