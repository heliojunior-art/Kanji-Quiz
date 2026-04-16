import json
from django.core.management.base import BaseCommand
from app.models import Kanji, Alternativa


class Command(BaseCommand):
    help = "Importa Kanjis e alternativas de um arquivo JSON"

    def add_arguments(self, parser):
        parser.add_argument("arquivo", type=str)

    def handle(self, *args, **options):
        caminho = options["arquivo"]

        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        total = 0

        for item in dados:
            kanji_char = item.get("kanji")

            if not kanji_char:
                self.stdout.write(self.style.WARNING("Kanji vazio ignorado"))
                continue

            # 🔄 atualiza ou cria
            kanji, created = Kanji.objects.update_or_create(
                kanji=kanji_char,
                defaults={
                    "nivel": item.get("nivel"),
                    "leitura": item.get("leitura"),
                    "significado": item.get("significado"),
                    "exemplo_jp": item.get("exemplo_jp") or item.get("exemplo"),
                    "exemplo_romaji": item.get("exemplo_romaji"),
                    "exemplo_pt": item.get("exemplo_pt"),

                    # 🔥 mantém compatível com quiz
                    "correta": item.get("correta"),
                    "alternativa1": item.get("alternativa1"),
                    "alternativa2": item.get("alternativa2"),
                    "alternativa3": item.get("alternativa3"),
                }
            )

            # 🧹 limpa alternativas antigas (IMPORTANTE)
            kanji.alternativas.all().delete()

            alternativas_json = item.get("alternativas", [])

            if alternativas_json:
                for alt in alternativas_json:
                    texto = alt.get("texto")

                    if not texto:
                        continue

                    Alternativa.objects.create(
                        kanji=kanji,
                        texto=texto,
                        correta=bool(alt.get("correta"))
                    )

            # ✅ 2. fallback (campos do modelo)
            else:
                campos = [
                    (kanji.correta, True),
                    (kanji.alternativa1, False),
                    (kanji.alternativa2, False),
                    (kanji.alternativa3, False),
                ]

                for texto, is_correct in campos:
                    if texto:
                        Alternativa.objects.create(
                            kanji=kanji,
                            texto=texto,
                            correta=is_correct
                        )

            total += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída! {total} kanjis processados."))