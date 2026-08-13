from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import login_required

from db import db

from app.models.cronograma_item import CronogramaItem
from app.services.evento_service import EventoService


MESES = {
    1: "jan",
    2: "fev",
    3: "mar",
    4: "abr",
    5: "mai",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "set",
    10: "out",
    11: "nov",
    12: "dez",
}


SISTEMAS_VALIDOS = {
    "SIPPES",
    "SIAPES",
}


def formatar_data_cpex(data):

    if not data:
        return ""

    try:

        dt = datetime.strptime(
            data,
            "%Y-%m-%d",
        )

        return (
            f"{dt.day:02d}/"
            f"{MESES[dt.month]}/"
            f"{str(dt.year)[2:]}"
        )

    except ValueError:

        return data


def obter_sistema():

    sistema = (
        request.form.get("sistema") or ""
    ).strip().upper()

    if sistema and sistema not in SISTEMAS_VALIDOS:

        raise ValueError(
            "Sistema inválido. Use SIPPES ou SIAPES."
        )

    return sistema or None


evento_bp = Blueprint(
    "evento",
    __name__,
)


@evento_bp.route(
    "/eventos/novo",
    methods=["GET", "POST"],
)
@login_required
def novo():

    if request.method == "POST":

        try:

            sistema = obter_sistema()

        except ValueError as erro:

            flash(
                str(erro),
                "danger",
            )

            return render_template(
                "evento_form.html",
                evento=None,
                titulo="Novo Evento",
                hoje=datetime.now().strftime(
                    "%Y-%m-%d"
                ),
            )

        evento = CronogramaItem(

            importacao_id=None,

            origem="MANUAL",

            data=formatar_data_cpex(
                request.form["data"]
            ),

            horario=request.form["horario"],

            descricao=request.form["descricao"],

            executor=request.form.get("executor"),

            sistema=sistema,

            observacao=request.form.get("observacao"),

            cor=request.form.get("cor"),

            status="Pendente",

            concluido=False,

            lembrete_enviado=False,

        )

        db.session.add(evento)

        db.session.commit()

        flash(
            "Evento cadastrado com sucesso.",
            "success",
        )

        return redirect(
            url_for("agenda.agenda")
        )

    return render_template(

        "evento_form.html",

        evento=None,

        titulo="Novo Evento",

        hoje=datetime.now().strftime("%Y-%m-%d"),

    )


@evento_bp.route(
    "/eventos/<int:id>/editar",
    methods=["GET", "POST"],
)
@login_required
def editar(id):

    evento = CronogramaItem.query.get_or_404(id)

    if evento.origem != "MANUAL":

        flash(
            "Eventos importados não podem ser editados.",
            "warning",
        )

        return redirect(
            url_for("agenda.agenda")
        )

    if request.method == "POST":

        try:

            sistema = obter_sistema()

        except ValueError as erro:

            flash(
                str(erro),
                "danger",
            )

            return render_template(
                "evento_form.html",
                evento=evento,
                titulo="Editar Evento",
                hoje=datetime.now().strftime(
                    "%Y-%m-%d"
                ),
            )

        evento.data = formatar_data_cpex(
            request.form["data"]
        )

        evento.horario = request.form["horario"]

        evento.descricao = request.form["descricao"]

        evento.executor = request.form.get("executor")

        evento.sistema = sistema

        evento.observacao = request.form.get("observacao")

        evento.cor = request.form.get("cor")

        db.session.commit()

        flash(
            "Evento atualizado com sucesso.",
            "success",
        )

        return redirect(
            url_for("agenda.agenda")
        )

    return render_template(

        "evento_form.html",

        evento=evento,

        titulo="Editar Evento",

        hoje=datetime.now().strftime("%Y-%m-%d"),

    )


@evento_bp.route(
    "/eventos/<int:id>/concluir"
)
@login_required
def concluir(id):

    evento = CronogramaItem.query.get_or_404(id)

    EventoService.alternar_conclusao(evento)

    flash(
        "Status atualizado.",
        "success",
    )

    return redirect(
        url_for("agenda.agenda")
    )


@evento_bp.route(
    "/eventos/<int:id>/excluir"
)
@login_required
def excluir(id):

    evento = CronogramaItem.query.get_or_404(id)

    if EventoService.excluir(evento):

        flash(
            "Evento excluído.",
            "success",
        )

    else:

        flash(
            "Eventos importados não podem ser excluídos.",
            "warning",
        )

    return redirect(
        url_for("agenda.agenda")
    )