from flask import Blueprint, render_template

from app.services.agenda_service import obter_eventos_hoje

agenda_bp = Blueprint(
    "agenda",
    __name__,
)


@agenda_bp.route("/agenda")
def agenda():

    eventos = obter_eventos_hoje()

    return render_template(
        "agenda.html",
        eventos=eventos,
    )
