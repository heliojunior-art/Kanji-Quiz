from django.db import models
from django.contrib.auth.models import User  # Se quiser usar o sistema de login do Django

class Kanji(models.Model):
    caractere = models.CharField(max_length=10)
    significado = models.CharField(max_length=255, blank=True, null=True)
    nivel = models.CharField(max_length=10)  # Ex: "1年", "2年"

    def __str__(self):
        return self.caractere


class Alternativa(models.Model):
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE, related_name="alternativas")
    texto = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correta' if self.correta else 'Errada'})"


class Resposta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    correta = models.BooleanField()
    respondido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta de {self.usuario} para {self.kanji}"
