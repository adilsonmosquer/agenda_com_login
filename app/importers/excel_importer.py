from openpyxl import load_workbook


class ExcelImporter:

    def __init__(self, arquivo):
        self.arquivo = arquivo

    def importar(self):

        workbook = load_workbook(
            filename=self.arquivo,
            data_only=True,
        )

        planilha = workbook.active

        itens = []

        for linha in planilha.iter_rows(min_row=2, values_only=True):

            if not linha or linha[0] is None:
                continue

            itens.append(
                {
                    "data": linha[0],
                    "dia_semana": linha[1],
                    "horario": linha[2],
                    "descricao": linha[3],
                    "executor": linha[4],
                    "cor": None,
                }
            )

        return itens
