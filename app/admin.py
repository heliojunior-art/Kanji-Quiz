from django.contrib import admin
from django.db.models.signals import post_migrate
from .models import Kanji, Alternativa, QuizSession, Resposta

# ======================================================================
# 🔑 CRIAÇÃO AUTOMÁTICA DE USUÁRIO
# ======================================================================
def criar_admin_automatico(sender, **kwargs):
    """Garante a fabricação do administrador na nuvem de forma limpa e sem travar"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username="helio").exists():
            User.objects.create_superuser("helio", "heliojunior@edu.unifil.br", "3352")
    except Exception:
        pass

post_migrate.connect(criar_admin_automatico)

# ======================================================================
# 📋 PAINEL ADMINISTRATIVO E FORMULÁRIOS
# ======================================================================
@admin.register(Kanji)
class KanjiAdmin(admin.ModelAdmin):
    list_display = ("kanji", "leitura", "significado", "nivel")
    search_fields = ("kanji", "leitura", "significado", "nivel")
    list_filter = ("nivel",)

admin.site.register(Alternativa)
admin.site.register(QuizSession)
admin.site.register(Resposta)