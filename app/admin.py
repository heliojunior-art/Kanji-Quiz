from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
import json
from .models import Kanji, Alternativa

class UploadJSONForm(forms.Form):
    arquivo = forms.FileField()

@admin.register(Kanji)
class KanjiAdmin(admin.ModelAdmin):
    list_display = ("kanji", "leitura", "significado", "nivel")
    search_fields = ("kanji", "leitura", "significado")

    def get_urls(self):
        urls = super().get_urls()
        urls_extra = [
            path("importar-json/", self.admin_site.admin_view(self.importar_json))
        ]
        return urls_extra + urls

    def importar_json(self, request):
        if request.method == "POST":
            form = UploadJSONForm(request.POST, request.FILES)
            if form.is_valid():
                arquivo = json.load(request.FILES["arquivo"])
                for item in arquivo:
                    kanji = Kanji.objects.create(
                        caractere=item.get("kanji"),
                        leitura=item.get("leitura"),
                        significado=item.get("significado"),
                        nivel=item.get("nivel"),
                        exemplo_jp=item.get("exemplo_jp") or item.get("exemplo"),
                        exemplo_romaji=item.get("exemplo_romaji"),
                        exemplo_pt=item.get("exemplo_pt")
                    )

                    # criar alternativas se presentes no JSON
                    for alt in item.get("alternativas", []):
                        Alternativa.objects.create(
                            kanji=kanji,
                            texto=alt.get("texto"),
                            correta=bool(alt.get("correta"))
                        )

                self.message_user(request, "Importação concluída!")
                return redirect("..")
        else:
            form = UploadJSONForm()

        return render(request, "admin/importar_json.html", {"form": form})
