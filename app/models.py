from django.db import models

class Kanji(models.Model):
    kanji = models.CharField(max_length=10, unique=True)
    leitura = models.CharField(max_length=100)
    significado = models.CharField(max_length=200)
    nivel = models.CharField(max_length=10)
    dica = models.TextField(blank=True, default="")
    exemplo_jp = models.TextField(blank=True, default="")
    exemplo_romaji = models.TextField(blank=True, default="")
    exemplo_pt = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.kanji} ({self.nivel})"

class Alternativa(models.Model):
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE, related_name="alternativas")
    texto = models.CharField(max_length=200)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correta' if self.correta else 'Incorreta'})"

class QuizSession(models.Model):
    nivel = models.CharField(max_length=10)
    quantidade = models.IntegerField()
    acertos = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)
    ordem_kanjis = models.JSONField(default=list)
    ordem_alternativas = models.JSONField(default=dict)

    def tempo_total(self):
        if not self.finalizado_em:
            return None
        return self.finalizado_em - self.criado_em

    def porcentagem(self):
        if self.quantidade == 0:
            return 0
        return round((self.acertos / self.quantidade) * 100)

    def __str__(self):
        return f"Quiz {self.nivel} ({self.acertos}/{self.quantidade})"

class Resposta(models.Model):
    quiz = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name="respostas")
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE, null=True, blank=True)
    correta = models.BooleanField()
    respondido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sessão {self.quiz.id} - Kanji {self.kanji.kanji} ({'Acertou' if self.correta else 'Errou'})"
