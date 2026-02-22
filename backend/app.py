from flask import Flask, render_template

"""
CONFIGURAÇÃO DA APLICAÇÃO
-------------------------
- Cria uma instância da aplicação
- Inicializa o servidor Flask
- Define o contexto principal do app
"""

app = Flask(__name__)


"""
DEFINIÇÃO DAS ROTAS
-------------------
Cada rota associa uma URL a uma função Python.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return "Página sobre o MaidInDev."


"""
PONTO DE ENTRADA
----------------
Executa o servidor apenas se o arquivo for rodado diretamente.
"""

if __name__ == "__main__":
    app.run(debug=True)
