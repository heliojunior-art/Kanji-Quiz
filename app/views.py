from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Kanji, Alternativa, Resposta, QuizSession
from django.db import transaction
from django.core.paginator import Paginator
from .management.commands.import_kanjis import Command
import random

# -------------------------------
# HOME
# -------------------------------
def home(request):
    return render(request, "home.html")

# -------------------------------
# MENU – Criar Quiz
# -------------------------------
def menu(request):
    if request.method == "POST":
        nivel = request.POST.get("nivel")
        
        quantidade = int(request.POST.get("quantidade"))

        kanjis = list(Kanji.objects.filter(nivel=nivel))
        if len(kanjis) < quantidade:
            quantidade = len(kanjis)    
        ordem_kanjis = random.sample([k.id for k in kanjis], quantidade)

        quiz = QuizSession.objects.create(
            nivel=nivel,
            quantidade=quantidade,
            acertos=0,
            ordem_kanjis=ordem_kanjis
        )
        return redirect("quiz_pergunta", **{"quiz_id": quiz.id, "questao": 1})

    return render(request, "menu.html")


# -------------------------------
# PERGUNTA DO QUIZ
# -------------------------------
def quiz_pergunta(request, quiz_id, questao):
    quiz = get_object_or_404(QuizSession, id=quiz_id)

    if questao > quiz.quantidade:
        return redirect("quiz_final", quiz_id=quiz.id)

    kanji_id = quiz.ordem_kanjis[questao - 1]
    kanji = get_object_or_404(Kanji, id=kanji_id)
    key = str(kanji.id)

    if not quiz.ordem_alternativas:
            quiz.ordem_alternativas = {}
            quiz.save()

    if key not in quiz.ordem_alternativas:
        alternativas = list(Alternativa.objects.filter(kanji=kanji))

        if not alternativas:
            campos = [
                (kanji.correta, True),
                (kanji.alternativa1, False),
                (kanji.alternativa2, False),
                (kanji.alternativa3, False),
            ]

            for texto, correta in campos:
                if texto:
                    Alternativa.objects.create(
                        kanji=kanji,
                        texto=texto,
                        correta=correta
                    )

        alternativas = list(Alternativa.objects.filter(kanji=kanji))
        random.shuffle(alternativas)
        quiz.ordem_alternativas[key] = [a.id for a in alternativas]
        quiz.save()

    ids = quiz.ordem_alternativas[key]
    alternativas = list(Alternativa.objects.filter(id__in=ids))
    alternativas.sort(key=lambda x: ids.index(x.id) if x.id in ids else 0)

    resposta = Resposta.objects.filter(
        quiz_id=quiz.id,
        kanji_id=kanji_id
    ).first()

    selecionada = resposta.alternativa.id if resposta else None
    print("QUESTAO:", questao)
    print("QUANTIDADE:", quiz.quantidade)
    print("KANJI ATUAL:", kanji, kanji_id)
    print("KANJIS RESPONDIDOS:", list(quiz.respostas.values_list("kanji", flat=True)))
    print("ALTERNATIVA SELECIONADA:", selecionada)
    print("RESPOSTA:", resposta)

    return render(request, "quiz.html", {
        "quiz": quiz,
        "kanji": kanji,
        "alternativas": alternativas,
        "selecionada": selecionada,
        "questao_atual": questao,
        "total": quiz.quantidade,
        "resposta": resposta,
    })


# -------------------------------
# REGISTRAR RESPOSTA
# -------------------------------
@transaction.atomic
def responder(request, quiz_id, kanji_id):
    if request.method != "POST":
        return redirect("menu")

    quiz = QuizSession.objects.select_for_update().get(id=quiz_id)
    kanji = get_object_or_404(Kanji, id=kanji_id)

    alternativa_id = request.POST.get("alternativa")
    questao = int(request.POST.get("questao", 1))

    print("POST alternativa:", alternativa_id)

    # ❌ impedir salvar vazio
    if not alternativa_id or alternativa_id == "None":
        return redirect("quiz_pergunta", quiz_id=quiz.id, questao=questao)

    alternativa = get_object_or_404(Alternativa, id=int(alternativa_id))

    # 🔒 salva resposta
    resposta, created = Resposta.objects.update_or_create(
        quiz=quiz,
        kanji=kanji,
        defaults={
            "alternativa": alternativa,
            "correta": alternativa.correta
        }
    )

    # ✅ só soma acerto se for nova
    if alternativa.correta and created:
        quiz.acertos += 1
        quiz.save()

    # 👉 próximo
    if 'proximo' in request.POST:
        questao += 1
        if questao > quiz.quantidade:
            return redirect("quiz_final", quiz_id=quiz.id)
        return redirect("quiz_pergunta", quiz_id=quiz.id, questao=questao)

    # 👉 anterior
    if 'anterior' in request.POST:
        questao -= 1
        if questao < 1:
            questao = 1
        return redirect("quiz_pergunta", quiz_id=quiz.id, questao=questao)

# -------------------------------
# PARAR QUIZ
# -------------------------------
def parar_quiz(request, quiz_id):
    quiz = get_object_or_404(QuizSession, id=quiz_id)
    quiz.respostas.all().delete()
    return redirect("menu")


# -------------------------------
# RESULTADO FINAL
# -------------------------------
def quiz_final(request, quiz_id):
    quiz = get_object_or_404(QuizSession, id=quiz_id)

    if quiz.finalizado_em is None:
        quiz.finalizado_em = timezone.now()
        quiz.acertos = quiz.respostas.filter(correta=True).count()
        quiz.save()

    respostas = quiz.respostas.select_related("kanji", "alternativa")

    resumo = []
    for r in respostas:
        try:
            correta_obj = r.kanji.alternativas.get(correta=True)
            correta_texto = correta_obj.texto
        except Alternativa.DoesNotExist:
            correta_texto = None
        resumo.append({
            "kanji": r.kanji,
            "escolhida": r.alternativa,
            "correta_texto": correta_texto,
            "acertou": r.correta,
            "respondido_em": r.respondido_em,
        })

    tempo_raw = quiz.tempo_total()
    if tempo_raw:
        total_segundos = int(tempo_raw.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        tempo_formatado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    else:
        tempo_formatado = "00:00:00"

    return render(request, "resultado.html", {
        "quiz": quiz,
        "respostas": respostas,
        "resumo": resumo,
        "tempo": tempo_formatado,
        "porcentagem": quiz.porcentagem(),
    })


# -------------------------------
# BIBLIOTECA DE KANJIS
# -------------------------------
def kanji_list(request):
    nivel = request.GET.get("nivel", "")
    page_number = request.GET.get("page", 1)

    if nivel:
        kanjis = Kanji.objects.filter(nivel=nivel).order_by("id").all()
    else:
        kanjis = Kanji.objects.all().order_by("id")

    paginator = Paginator(kanjis, 30)
    page_obj = paginator.get_page(page_number)

    return render(request, "biblioteca.html", {
        "kanjis": page_obj,
        "page_obj": page_obj,
        "nivel_selecionado": nivel,
    })
