from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler.runner import TaskRunner
from app.scheduler.tasks.agenda_task import executar as agenda_task
from app.services.configuracao_service import ConfiguracaoService

scheduler = BackgroundScheduler()


def registrar_jobs(app):

    #
# Intervalo interno do Scheduler.
#
# Não é configuração do usuário.
#
     intervalo = 1

    scheduler.add_job(
        TaskRunner.executar,
        trigger="interval",
        minutes=intervalo,
        args=[
            "Agenda Diária",
            agenda_task,
            app,
        ],
        id="agenda_diaria",
        replace_existing=True,
    )

    print()

    print("=" * 60)
    print("Jobs registrados:")
    print(f"Intervalo de execução: {intervalo} minuto(s)")
    print()

    for job in scheduler.get_jobs():
        print(f"✓ {job.id}")

    print("=" * 60)
    print()