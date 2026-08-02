import pdfplumber
import re


class PDFImporter:

    def __init__(self, arquivo):
        self.arquivo = arquivo

    def importar(self):

        itens = []

        padrao = re.compile(
            r"^(\d{1,2}/[a-z]{3}/\d{2})\s+([A-ZÇ]{3}\.)\s+(\d{2}:\d{2})\s+(.*?)\s+(.+)$",
            re.IGNORECASE,
        )

        with pdfplumber.open(self.arquivo) as pdf:

            for pagina in pdf.pages:

                texto = pagina.extract_text()

                if not texto:
                    continue

                for linha in texto.split("\n"):

                    linha = " ".join(linha.split())

                    m = padrao.match(linha)

                    if m:

                        itens.append(
                            {
                                "data": m.group(1),
                                "dia_semana": m.group(2),
                                "horario": m.group(3),
                                "descricao": m.group(4),
                                "executor": m.group(5),
                                "cor": None,
                            }
                        )

        return itens
