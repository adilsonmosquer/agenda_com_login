from app.models.importacao import Importacao


def listar_importacoes():

    return Importacao.query.order_by(Importacao.data_importacao.desc()).all()
