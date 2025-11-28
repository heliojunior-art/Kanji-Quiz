class Kanji:
    def __init__(self, caractere, leituras, dificuldade):
        self.caractere = caractere
        self.leituras = leituras
        self.dificuldade = dificuldade

    def resposta_correta(self):
        return self.leituras[0]
