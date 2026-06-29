from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path('menu/', views.menu, name='menu'), 
    path('admin/', admin.site.urls),

    # Quiz
    path('quiz/<int:quiz_id>/<int:questao>/', views.quiz_pergunta, name='quiz_pergunta'),
    path("responder/<int:quiz_id>/<int:kanji_id>/", views.responder, name="responder"),
    path("resultado/<int:quiz_id>/", views.quiz_final, name="quiz_final"),
    path('parar_quiz/<int:quiz_id>/', views.parar_quiz, name='parar_quiz'),
    path('resultado/<int:quiz_id>/', views.quiz_final, name='quiz_final'),

    # Biblioteca
    path("biblioteca/", views.kanji_list, name="biblioteca"),
]