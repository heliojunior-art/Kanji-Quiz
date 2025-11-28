from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Kanji, Alternativa, Resposta
import random


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def iniciar_quiz(request):
    nivel = request.GET.get("nivel", "1年")
    
    # Seleciona 1 kanji aleatório
    kanjis = Kanji.objects.filter(nivel=nivel)
    kanji = random.choice(kanjis)

    alternativas = list(kanji.alternativas.all())
    random.shuffle(alternativas)

    return render(request, "quiz.html", {
        "kanji": kanji,
        "alternativas": alternativas
    })


@login_required
def responder(request, kanji_id):
    if request.method != "POST":
        return redirect("home")

    alternativa_id = request.POST.get("alternativa")
    alternativa = get_object_or_404(Alternativa, id=alternativa_id)
    kanji = alternativa.kanji

    resposta = Resposta.objects.create(
        usuario=request.user,
        kanji=kanji,
        alternativa=alternativa,
        correta=alternativa.correta
    )

    return render(request, "resultado.html", {
        "kanji": kanji,
        "alternativa": alternativa
    })
