class Pontuacao:
    def __init__(self):
        self.acertos = 0
        self.total = 0

    def registrar_resposta(self, correta):
        self.total += 1
        if correta:
            self.acertos += 1

    def mostrar_resultado(self):
        print(f"📊 Pontuação final: {self.acertos}/{self.total}")
        percentual = (self.acertos / self.total) * 100 if self.total > 0 else 0
        print(f"🎯 Desempenho: {percentual:.2f}%")