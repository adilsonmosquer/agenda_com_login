import os
import time
from datetime import datetime


class TaskRunner:

    @staticmethod
    def executar(nome, tarefa, app):

        inicio = time.perf_counter()

        print()
        print("=" * 60)
        print(f"Tarefa   : {nome}")
        print(f"PID      : {os.getpid()}")
        print(f"Início   : {datetime.now():%d/%m/%Y %H:%M:%S}")
        print("=" * 60)

        try:

            with app.app_context():
                tarefa()

            tempo = time.perf_counter() - inicio

            print()
            print(f"Status   : SUCESSO")
            print(f"Fim      : {datetime.now():%d/%m/%Y %H:%M:%S}")
            print(f"Tempo    : {tempo:.2f} segundos")
            print("=" * 60)
            print()

        except Exception as erro:

            tempo = time.perf_counter() - inicio

            print()
            print(f"Status   : ERRO")
            print(f"Fim      : {datetime.now():%d/%m/%Y %H:%M:%S}")
            print(f"Tempo    : {tempo:.2f} segundos")
            print(f"Erro     : {erro}")
            print("=" * 60)
            print()

            # Não relança a exceção para evitar que o APScheduler
            # imprima um traceback enorme no terminal.
            return
        