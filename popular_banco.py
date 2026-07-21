from app import create_app
from db import db
from app.models.cronograma_item import Event

app = create_app()

with app.app_context():

    # Evita inserir registros duplicados
    if Event.query.count() == 0:

        eventos = [
            Event(
                horario="08:00",
                descricao="Recebimento dos arquivos",
                status="Concluído",
                cor="success",
            ),
            Event(
                horario="10:00",
                descricao="Validação dos dados",
                status="Concluído",
                cor="success",
            ),
            Event(
                horario="14:00",
                descricao="Reunião de Coordenação",
                status="Pendente",
                cor="warning",
            ),
            Event(
                horario="16:00",
                descricao="Publicação",
                status="Aguardando",
                cor="secondary",
            ),
        ]

        db.session.add_all(eventos)
        db.session.commit()

        print("Eventos inseridos com sucesso!")

    else:
        print("O banco já possui eventos.")
