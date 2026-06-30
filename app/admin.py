from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
from django.db.models.signals import post_migrate
import json
from .models import Kanji, Alternativa, QuizSession, Resposta

# ======================================================================
# 🔑 CRIAÇÃO AUTOMÁTICA DE USUÁRIO (Sincronizado via Sinais)
# ======================================================================
def criar_admin_automatico(sender, **kwargs):
    """Garante a fabricação do administrador na nuvem de forma limpa e sem travar"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username="helio").exists():
            User.objects.create_superuser("helio", "heliojunior@edu.unifil.br", "3352")
    except Exception:
        pass

# Conecta o sinal imediatamente no momento em que o admin é lido pelo Django
post_migrate.connect(criar_admin_automatico)

# ======================================================================
# 📋 PAINEL ADMINISTRATIVO E FORMULÁRIOS
# ======================================================================
class UploadJSONForm(forms.Form):
    arquivo = forms.FileField(label="Selecione o arquivo kanjis.json")

@admin.register(Kanji)
class KanjiAdmin(admin.ModelAdmin):
    list_display = ("kanji", "leitura", "significado", "nivel")
    search_fields = ("kanji", "leitura", "significado", "nivel")
    list_filter = ("nivel",)

    def get_urls(self):
        urls = super().get_urls()
        urls_extra = [
            path("importar-json/", self.admin_site.admin_view(self.importar_json), name="importar_json_admin")
        ]
        return urls_extra + urls

    def importar_json(self, request):
        if request.method == "POST":
            form = UploadJSONForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    arquivo_json = json.load(request.FILES["arquivo"])
                    
                    for item in arquivo_json:
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

                    self.message_user(request, "🎉 Importação do banco de Kanjis realizada com sucesso!")
                    return redirect("admin:app_kanji_changelist")
                except Exception as e:
                    self.message_user(request, f"❌ Erro ao processar o JSON: {str(e)}", level='error')
                    return redirect("..")
        else:
            form = UploadJSONForm()

        return render(request, "admin/importar_json.html", {"form": form})

admin.site.register(Alternativa)
admin.site.register(QuizSession)
admin.site.register(Resposta)
