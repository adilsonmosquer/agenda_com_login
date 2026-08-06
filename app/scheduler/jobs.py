from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler.runner import TaskRunner
from app.scheduler.tasks.agenda_task import executar as agenda_task
from app.scheduler.tasks.reminder_task import executar as reminder_task


scheduler = BackgroundScheduler()


def registrar_jobs(app):

    scheduler.add_job(
        TaskRunner.executar,
        trigger="cron",
        hour=8,
        minute=0,
        args=[
            "Agenda Diária",
            agenda_task,
            app,
        ],
        id="agenda_diaria",
        replace_existing=True,
    )

    scheduler.add_job(
        TaskRunner.executar,
        trigger="interval",
        minutes=1,
        args=[
            "Lembretes",
            reminder_task,
            app,
        ],
        id="lembretes",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()

    print()
    print("=" * 60)
    print("Scheduler iniciado")
    print()

    for job in scheduler.get_jobs():
        print(f"✓ {job.id}")

    print("=" * 60)
    print()