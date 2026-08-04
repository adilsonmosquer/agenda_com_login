from app import create_app
from app.scheduler.scheduler import iniciar_scheduler

app = create_app()

with app.app_context():

    iniciar_scheduler(app)

    print()

    print("=" * 60)
    print("Worker iniciado.")
    print("Pressione CTRL+C para encerrar.")
    print("=" * 60)
    print()

    try:

        import time

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        print()

        print("Worker finalizado.")