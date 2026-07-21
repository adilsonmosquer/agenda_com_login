from flask import Blueprint
from flask import render_template

from app.services.importacao_service import listar_importacoes

importacoes_bp = Blueprint("importacoes", __name__)


@importacoes_bp.route("/importacoes")
def importacoes():

    lista = listar_importacoes()

    return render_template("importacoes.html", importacoes=lista)
