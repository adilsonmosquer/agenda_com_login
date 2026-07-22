from pathlib import Path

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import secure_filename

from db import db
from app.models.importacao import Importacao
from app.services.importacao_service import listar_importacoes

importacoes_bp = Blueprint("importacoes", __name__)


def arquivo_permitido(nome_arquivo):

    extensao = Path(nome_arquivo).suffix.lower().replace(".", "")

    return extensao in current_app.config["ALLOWED_EXTENSIONS"]


@importacoes_bp.route("/importacoes", methods=["GET", "POST"])
def importacoes():

    if request.method == "POST":

        if "arquivo" not in request.files:
            return redirect(request.url)

        arquivo = request.files["arquivo"]

        if arquivo.filename == "":
            return redirect(request.url)

        if arquivo and arquivo_permitido(arquivo.filename):

            nome = secure_filename(arquivo.filename)

            destino = Path(current_app.config["UPLOAD_FOLDER"]) / nome
            destino.parent.mkdir(parents=True, exist_ok=True)
            arquivo.save(destino)

            extensao = destino.suffix.replace(".", "").upper()

            nova_importacao = Importacao(
                arquivo=nome, tipo=extensao, registros=0, status="Arquivo recebido"
            )

            db.session.add(nova_importacao)
            db.session.commit()

            return redirect(url_for("importacoes.importacoes"))

    lista = listar_importacoes()

    return render_template("importacoes.html", importacoes=lista)
