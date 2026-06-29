import json
from django.core.management.base import BaseCommand
from app.models import Kanji, Alternativa

class Command(BaseCommand):
    help = "Importa Kanjis e suas respectivas alternativas a partir de um arquivo JSON."

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Caminho para o arquivo JSON contendo os dados.")

    def handle(self, *args, **options):
        caminho_arquivo = options["json_file"]

        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado."))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Erro: O arquivo não é um JSON válido."))
            return

        self.stdout.write(self.style.WARNING("Iniciando a importação dos Kanjis..."))

        for item in dados:
            kanji_obj, created = Kanji.objects.update_or_create(
                kanji=item["kanji"],
                defaults={
                    "leitura": item["leitura"],
                    "significado": item["significado"],
                    "nivel": item["nivel"],
                    "dica": item.get("dica", ""),
                    "exemplo_jp": item.get("exemplo_jp", ""),
                    "exemplo_romaji": item.get("exemplo_romaji", ""),
                    "exemplo_pt": item.get("exemplo_pt", ""),
                }
            )

            if kanji_obj:
                kanji_obj.alternativas.all().delete()
                
                campos_alternativas = [
                    (item.get("correta"), True),
                    (item.get("alternativa1"), False),
                    (item.get("alternativa2"), False),
                    (item.get("alternativa3"), False),
                ]

                for texto, eh_correta in campos_alternativas:
                    if texto:
                        Alternativa.objects.create(
                            kanji=kanji_obj,
                            texto=texto,
                            correta=eh_correta
                        )

        self.stdout.write(self.style.SUCCESS("✨ Importação concluída com sucesso no banco de dados!"))
