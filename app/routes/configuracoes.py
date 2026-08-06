from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from app.services.configuracao_service import ConfiguracaoService


configuracoes_bp = Blueprint(
    "configuracoes",
    __name__,
)


@configuracoes_bp.route(
    "/configuracoes",
    methods=["GET", "POST"],
)
@login_required
def configuracoes():

    if request.method == "POST":

        configuracoes = ConfiguracaoService.listar()

        for configuracao in configuracoes:

            valor = request.form.get(configuracao.chave)

            if valor is not None:

                ConfiguracaoService.set(
                    configuracao.chave,
                    valor,
                )

        flash(
            "Configurações salvas com sucesso.",
            "success",
        )

        return redirect(
            url_for("configuracoes.configuracoes")
        )

    categorias = {}

    for configuracao in ConfiguracaoService.listar():

        categoria = configuracao.categoria

        if categoria not in categorias:

            categorias[categoria] = []

        categorias[categoria].append(configuracao)

    return render_template(
        "configuracoes.html",
        categorias=categorias,
    )
