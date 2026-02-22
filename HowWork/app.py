# ============================================
# IMPORTAÇÕES - Pegando as ferramentas
# ============================================
from flask import Flask, render_template
# Flask = A cozinha completa
# render_template = O garçom que leva dados para o HTML

# ============================================
# CRIAÇÃO DO APP - Montando a cozinha
# ============================================
app = Flask(__name__)
# __name__ = "Este arquivo" - ajuda o Flask a se localizar

# ============================================
# DADOS - A despensa (ingredientes)
# ============================================
noticias = [...]  # Lista de dicionários (array)
# Cada dicionário = Uma notícia (título, autor, etc)

# ============================================
# ROTAS - O cardápio (o que serve em cada URL)
# ============================================
@app.route("/")  # Quando alguém pedir a página inicial
def home():      # Faça isso:
    noticias_recentes = noticias[::-1]  # Pega as notícias
    return render_template(  # Manda para o HTML
        'index.html', 
        noticias=noticias_recentes,  # Com estes ingredientes
        categorias=categorias
    )
