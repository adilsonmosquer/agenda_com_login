from app.scheduler.jobs import (
    scheduler,
    registrar_jobs,
)


def iniciar_scheduler(app):

    if scheduler.running:
        return

    registrar_jobs(app)

    scheduler.start()

    print()

    print("=" * 50)
    print("Scheduler iniciado.")
    print("=" * 50)
    print()