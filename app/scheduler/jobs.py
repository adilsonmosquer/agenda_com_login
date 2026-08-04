from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler.runner import TaskRunner
from app.scheduler.tasks.agenda_task import executar as agenda_task

scheduler = BackgroundScheduler()


def registrar_jobs(app):

    scheduler.add_job(
        TaskRunner.executar,
        trigger="interval",
        minutes=2,
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

    for job in scheduler.get_jobs():
        print(f"✓ {job.id}")

    print("=" * 60)
    print()