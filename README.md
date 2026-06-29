# 📘 Kanji Quiz - Simulador Inteligente de Ideogramas Japoneses

O **Kanji Quiz** é uma aplicação web gamificada desenvolvida para auxiliar estudantes da língua japonesa a memorizarem de forma ativa e contextualizada os 1.447 caracteres oficiais exigidos no exame de proficiência **JLPT (N5 ao N1)**.

## 🔗 Links do Projeto
- **Página de Informações (GitHub Pages):** https://heliojunior-art.github.io/Kanji-Quiz/
- **Aplicação Online (Render):** https://kanji-quiz-d7w2.onrender.com

## 🚀 Diferenciais Técnicos e Recursos Implementados
- **Arquitetura Robusta:** Desenvolvido em Django com transações atômicas (`@transaction.atomic`) para garantir a integridade dos dados na gravação de respostas.
- **Ecossistema Padronizado e Responsivo:** Interface moderna construída sobre o Bootstrap v5, totalmente adaptada para uso em computadores e smartphones.
- **Sistema de Sessão Inteligente:** Embaralhamento dinâmico de alternativas fixado por sessão via campos JSON no banco de dados, prevenindo vícios de memorização por posição de botões.
- **Mecanismos Anti-Erro de Navegação:** Implementação de travas de histórico via JavaScript (`popstate`) para interceptar cliques acidentais no botão "Voltar" do navegador, evitando perda de progresso no quiz.
- **Pop-up Customizado de Dicas:** Integração de janelas flutuantes em CSS puro para exibição dinâmica de leituras e significados contextuais salvos no banco de dados.
- **Histórico Automático Auto-Limpante:** Painel de últimas sessões concluídas exibido em tempo real no menu inicial, integrado com rotinas de limpeza automática (`manage.py`) para ambientes de teste local.

## 📦 Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com](https://github.com/heliojunior-art/Kanji-Quiz.git)
   cd nome-do-repositorio
   ```
2. **Ative o ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Execute as migrações e importe o banco de dados:**
   ```bash
   python manage.py makemigrations app
   python manage.py migrate
   python manage.py import_kanjis kanjis.json
   ```
5. **Inicie o servidor:**
   ```bash
   python manage.py runserver
   ```

