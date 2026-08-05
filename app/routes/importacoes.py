from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from werkzeug.utils import secure_filename

from app.services.importacao_service import (
    excluir_importacao,
    importar_cronograma,
    listar_importacoes,
)

importacoes_bp = Blueprint(
    "importacoes",
    __name__,
)


EXTENSOES_EXCEL = {
    "xlsx",
    "xls",
}


def arquivo_permitido(nome_arquivo):

    if "." not in nome_arquivo:

        return False

    extensao = nome_arquivo.rsplit(".", 1)[1].lower()

    return extensao in EXTENSOES_EXCEL


@importacoes_bp.route(
    "/importacoes",
    methods=["GET", "POST"],
)
def importacoes():

    if request.method == "POST":

        if "arquivo" not in request.files:

            flash(
                "Nenhum arquivo enviado.",
                "danger",
            )

            return redirect(request.url)

        arquivo = request.files["arquivo"]

        if arquivo.filename == "":

            flash(
                "Selecione um arquivo Excel.",
                "warning",
            )

            return redirect(request.url)

        if not arquivo_permitido(
            arquivo.filename
        ):

            flash(
                "Somente arquivos Excel (.xlsx ou .xls) são permitidos.",
                "danger",
            )

            return redirect(request.url)

        nome = secure_filename(
            arquivo.filename
        )

        destino = (
            Path(
                current_app.config["UPLOAD_FOLDER"]
            )
            / nome
        )

        destino.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        arquivo.save(destino)

        try:

            importar_cronograma(

                arquivo_path=destino,

                nome_arquivo=nome,

            )

            flash(

                "Cronograma importado com sucesso.",

                "success",

            )

        except Exception as erro:

            flash(

                f"Erro durante a importação: {erro}",

                "danger",

            )

        return redirect(
            url_for(
                "importacoes.importacoes"
            )
        )

    return render_template(

        "importacoes.html",

        importacoes=listar_importacoes(),

    )


@importacoes_bp.post(
    "/importacoes/<int:importacao_id>/excluir"
)
def excluir(importacao_id):

    try:

        excluir_importacao(
            importacao_id
        )

        flash(
            "Importação excluída com sucesso.",
            "success",
        )

    except Exception as erro:

        flash(
            f"Erro ao excluir: {erro}",
            "danger",
        )

    return redirect(
        url_for(
            "importacoes.importacoes"
        )
    )