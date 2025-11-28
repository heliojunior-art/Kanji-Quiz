from quiz import Quiz

def escolher_nivel():
    print("Escolha o nível de dificuldade:")
    print("1. 小学1年 (GRADE 1)")
    print("2. 小学2年 (GRADE 2)")
    print("3. 小学3年 (GRADE 3)")
    while True:
        escolha = input("Digite 1, 2 ou 3: ")
        if escolha == "1":
            return "1年"
        elif escolha == "2":
            return "2年"
        elif escolha == "3":
            return "3年"
        else:
            print("Escolha inválida. Tente novamente.")
            
def escolher_quantidade():
    print("Quantas questões deseja responder?")
    print("1. 10 questões")
    print("2. 20 questões")
    print("3. 30 questões")
    
    while True:
        escolha = input("Digite 1, 2 ou 3: ")
        if escolha == "1":
            return 10
        elif escolha == "2":
            return 20
        elif escolha == "3":
            return 30
        else:
            print("Escolha inválida. Digite 1, 2 ou 3.")

def main():
    quiz = Quiz()
    nivel = escolher_nivel()
    quantidade = escolher_quantidade()
    quiz.carregar_perguntas(nivel, quantidade)

    print(f"\n📘 Iniciando quiz - Nível: 小学{nivel} - {quantidade} questões")

    while not quiz.quiz_terminado():
        pergunta = quiz.mostrar_proxima_pergunta()
        if not pergunta:
            break
        resposta = input("Digite a leitura correta do kanji: ")
        quiz.processar_resposta(resposta)

    quiz.mostrar_resultado_final()

if __name__ == "__main__":
    main()