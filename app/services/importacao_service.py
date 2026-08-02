from app.importers.excel_importer import ExcelImporter
from app.importers.pdf_importer import PDFImporter
from app.models.cronograma_item import CronogramaItem
from app.models.importacao import Importacao
from db import db


def listar_importacoes():
    return Importacao.query.order_by(Importacao.data_importacao.desc()).all()


def importar_cronograma(
    arquivo_path,
    nome_arquivo,
):

    extensao = nome_arquivo.rsplit(".", 1)[1].lower()

    if extensao in ("xlsx", "xls"):

        itens = ExcelImporter(arquivo_path).importar()

    elif extensao == "pdf":

        itens = PDFImporter(arquivo_path).importar()

    else:
        raise ValueError("Formato de arquivo não suportado.")

    importacao = Importacao(
        arquivo=nome_arquivo,
        periodo="Não informado",
        tipo=extensao,
        registros=len(itens),
        ativa=True,
    )

    db.session.add(importacao)
    db.session.flush()

    for item in itens:

        cronograma = CronogramaItem(
            importacao_id=importacao.id,
            data=item["data"],
            dia_semana=item["dia_semana"],
            horario=item["horario"],
            descricao=item["descricao"],
            executor=item["executor"],
            cor=item.get("cor"),
        )

        db.session.add(cronograma)

    db.session.commit()

    return importacao


from pathlib import Path
from flask import current_app


def excluir_importacao(importacao_id):

    importacao = Importacao.query.get_or_404(importacao_id)

    caminho = Path(current_app.config["UPLOAD_FOLDER"]) / importacao.arquivo

    db.session.delete(importacao)
    db.session.commit()

    if caminho.exists():
        caminho.unlink()
