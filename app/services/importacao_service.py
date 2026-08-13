from pathlib import Path

from flask import current_app

from app.importers.excel_importer import ExcelImporter
from app.models.cronograma_item import CronogramaItem
from app.models.importacao import Importacao
from db import db


def listar_importacoes():

    return (
        Importacao.query
        .order_by(
            Importacao.data_importacao.desc()
        )
        .all()
    )


def importar_cronograma(
    arquivo_path,
    nome_arquivo,
):

    extensao = nome_arquivo.rsplit(".", 1)[1].lower()

    if extensao not in ("xlsx", "xls"):

        raise ValueError(
            "Somente arquivos Excel (.xlsx ou .xls) são permitidos."
        )

    itens = ExcelImporter(
        arquivo_path
    ).importar()

    importacao = Importacao(

        arquivo=nome_arquivo,

        periodo="Não informado",

        tipo="excel",

        registros=len(itens),

        ativa=True,

    )

    db.session.add(importacao)

    db.session.flush()

    for item in itens:

        db.session.add(

            CronogramaItem(

                importacao_id=importacao.id,

                origem="IMPORTACAO",

                data=item["data"],

                dia_semana=item["dia_semana"],

                horario=item["horario"],

                descricao=item["descricao"],

                executor=item["executor"],

                sistema=item.get("sistema"),

                cor=item.get("cor"),

                status="Pendente",

                concluido=False,

                lembrete_enviado=False,

            )

        )

    db.session.commit()

    return importacao


def excluir_importacao(importacao_id):

    importacao = Importacao.query.get_or_404(
        importacao_id
    )

    caminho = (
        Path(
            current_app.config["UPLOAD_FOLDER"]
        )
        / importacao.arquivo
    )

    db.session.delete(importacao)

    db.session.commit()

    if caminho.exists():

        caminho.unlink()