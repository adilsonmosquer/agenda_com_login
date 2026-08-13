from datetime import datetime, timedelta

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.services.agenda_service import obter_eventos_dia


agenda_bp = Blueprint(
    "agenda",
    __name__,
)


@agenda_bp.route("/agenda")
@login_required
def agenda():

    data_parametro = request.args.get("data")

    if data_parametro:

        try:

            data = datetime.strptime(
                data_parametro,
                "%Y-%m-%d",
            )

        except ValueError:

            data = datetime.now()

    else:

        data = datetime.now()

    eventos = obter_eventos_dia(data)

    return render_template(
        "agenda.html",
        eventos=eventos,
        data_selecionada=data,
        timedelta=timedelta,
    )