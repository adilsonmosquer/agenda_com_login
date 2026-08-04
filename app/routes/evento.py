from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from db import db

from app.models.cronograma_item import CronogramaItem

from app.services.evento_service import EventoService


evento_bp = Blueprint(
    "evento",
    __name__,
)


@evento_bp.route(
    "/eventos/novo",
    methods=["GET", "POST"],
)
def novo():

    if request.method == "POST":

        evento = CronogramaItem(

            importacao_id=None,

            origem="MANUAL",

            data=request.form["data"],

            horario=request.form["horario"],

            descricao=request.form["descricao"],

            executor=request.form.get("executor"),

            observacao=request.form.get("observacao"),

            cor=request.form.get("cor"),

            status="Pendente",

            concluido=False,

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

        hoje=datetime.now().strftime("%d/%m/%Y"),

    )


@evento_bp.route(
    "/eventos/<int:id>/editar",
    methods=["GET", "POST"],
)
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

        evento.data = request.form["data"]

        evento.horario = request.form["horario"]

        evento.descricao = request.form["descricao"]

        evento.executor = request.form.get("executor")

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

        hoje=evento.data,

    )


@evento_bp.route("/eventos/<int:id>/concluir")
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


@evento_bp.route("/eventos/<int:id>/excluir")
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