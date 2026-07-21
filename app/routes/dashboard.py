from flask import Blueprint, render_template

from app.services.dashboard_service import obter_dados_dashboard

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():

    dados = obter_dados_dashboard()

    return render_template(
        "dashboard.html",
        **dados
    )