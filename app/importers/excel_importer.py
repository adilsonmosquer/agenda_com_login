from datetime import datetime

from openpyxl import load_workbook


MESES = {
    1: "jan",
    2: "fev",
    3: "mar",
    4: "abr",
    5: "mai",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "set",
    10: "out",
    11: "nov",
    12: "dez",
}


class ExcelImporter:

    CABECALHO = (
        "DATA",
        "DIA",
        "HORA*",
        "PROCEDIMENTOS",
        "EXECUTOR",
        "SISTEMA",
    )

    SISTEMAS_VALIDOS = {
        "SIPPES",
        "SIAPPES",
    }

    def __init__(self, arquivo):

        self.arquivo = arquivo

    @staticmethod
    def _texto(valor):

        if valor is None:
            return ""

        return str(valor).strip()

    @staticmethod
    def _formatar_data(valor):

        if valor is None:
            return ""

        if isinstance(valor, datetime):

            return (
                f"{valor.day:02d}/"
                f"{MESES[valor.month]}/"
                f"{str(valor.year)[2:]}"
            )

        texto = str(valor).strip()

        if "/" in texto:

            partes = texto.split("/")

            if len(partes) == 3:

                mes = partes[1]

                if mes.isdigit():

                    numero_mes = int(mes)

                    if numero_mes in MESES:

                        return (
                            f"{int(partes[0]):02d}/"
                            f"{MESES[numero_mes]}/"
                            f"{partes[2][-2:]}"
                        )

        return texto.lower()

    @staticmethod
    def _formatar_hora(valor):

        if valor is None:
            return ""

        if isinstance(valor, datetime):

            return valor.strftime("%H:%M")

        return str(valor).strip()

    def importar(self):

        workbook = load_workbook(
            filename=self.arquivo,
            data_only=True,
        )

        planilha = workbook.active

        cabecalho = tuple(

            self._texto(
                planilha.cell(
                    row=10,
                    column=col,
                ).value
            ).upper()

            for col in range(1, 7)

        )

        if cabecalho != self.CABECALHO:

            raise ValueError(
                "Layout do cronograma inválido. "
                "Esperado: DATA, DIA, HORA*, PROCEDIMENTOS, "
                "EXECUTOR, SISTEMA."
            )

        itens = []

        linha = 11

        while True:

            data = planilha.cell(
                linha,
                1,
            ).value

            if data is None:

                break

            descricao = self._texto(
                planilha.cell(
                    linha,
                    4,
                ).value
            )

            if descricao == "":

                break

            sistema = self._texto(
                planilha.cell(
                    linha,
                    6,
                ).value
            ).upper()

            if sistema and sistema not in self.SISTEMAS_VALIDOS:

                raise ValueError(
                    f"Sistema inválido na linha {linha}: "
                    f"'{sistema}'. Use SIPPES ou SIAPPES."
                )

            itens.append(

                {

                    "data": self._formatar_data(data),

                    "dia_semana": self._texto(
                        planilha.cell(
                            linha,
                            2,
                        ).value
                    ),

                    "horario": self._formatar_hora(
                        planilha.cell(
                            linha,
                            3,
                        ).value
                    ),

                    "descricao": descricao,

                    "executor": self._texto(
                        planilha.cell(
                            linha,
                            5,
                        ).value
                    ),

                    "sistema": sistema,

                    "cor": None,

                }

            )

            linha += 1

        return itens