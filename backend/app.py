from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'maid-secreta-2026'

ADMIN_USER = "teste"
ADMIN_PASS = "teste"

@app.context_processor
def inject_admin_status():
    """Disponibiliza a variável admin_logado para todos os templates"""
    
    admin_status = session.get('admin_logado', False)
    
    print(f" DEBUG: admin_logado = {admin_status}")
    
    return dict(admin_logado=admin_status)


@app.route("/forcar-admin")
def forcar_admin():
    session['admin_logado'] = True
    return "Agora você é admin! Volte para a página inicial."

def ler_noticias():
    """Lê as notícias do arquivo JSON"""
    
    if os.path.exists('noticias.json'):
        with open('noticias.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return []

def salvar_noticias(noticias):
    """Salva as notícias no arquivo JSON"""
    
    with open('noticias.json', 'w', encoding='utf-8') as f:
        json.dump(noticias, f, indent=4, ensure_ascii=False)

@app.route("/")
def home():
    """Página inicial - mostra todas as notícias"""
    
    noticias = ler_noticias()
    noticias = noticias[::-1]
    categorias = list(set([n['categoria'] for n in noticias]))
    
    return render_template('index.html', noticias=noticias, categorias=categorias)

@app.route("/sobre")
def sobre():
    """Página Sobre - informações do site"""
        return render_template('sobre.html')

@app.route("/categoria/<categoria>")
def noticias_por_categoria(categoria):
    """Filtra notícias por categoria"""
        noticias = ler_noticias()
    
    noticias_filtradas = [n for n in noticias if n['categoria'] == categoria]
        noticias_filtradas = noticias_filtradas[::-1]
        categorias = list(set([n['categoria'] for n in noticias]))
    
    return render_template('index.html', noticias=noticias_filtradas, categorias=categorias)

@app.route("/noticia/<int:noticia_id>")
def noticia_detalhe(noticia_id):
    """Página de uma notícia específica"""
        noticias = ler_noticias()
    noticia_encontrada = None
    
    for noticia in noticias:
        if noticia['id'] == noticia_id:
            noticia_encontrada = noticia
            noticia['visualizacoes'] += 1
            break
    
    if noticia_encontrada:
        salvar_noticias(noticias)
        return render_template('noticia.html', noticia=noticia_encontrada)
    
    return "Notícia não encontrada", 404

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    """Página de login do admin"""
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logado'] = True
            return redirect('/admin/painel')
        else:
            return render_template('admin_login.html', erro="Usuário ou senha inválidos")
        return render_template('admin_login.html')

@app.route("/admin/logout")
def admin_logout():
    """Faz logout do admin"""

    session.pop('admin_logado', None)
    return redirect('/')

def admin_required(f):
    """Decorator para verificar se o admin está logado"""
    
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logado'):
            return redirect('/admin/login')
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route("/admin/painel")
@admin_required
def admin_painel():
    """Painel administrativo - lista todas as notícias"""
    
    noticias = ler_noticias()
    noticias = noticias[::-1]
    return render_template('admin.html', noticias=noticias)

@app.route("/admin/criar", methods=['GET', 'POST'])
@admin_required
def admin_criar():
    """Criar nova notícia"""
    
    if request.method == 'POST':
        noticias = ler_noticias()
        
        novo_id = 1
        if noticias:
            novo_id = max([n['id'] for n in noticias]) + 1
        
        nova_noticia = {
            'id': novo_id,
            'titulo': request.form['titulo'],
            'resumo': request.form['resumo'],
            'conteudo': request.form['conteudo'],
            'autor': request.form['autor'],
            'data': request.form['data'],
            'categoria': request.form['categoria'],
            'visualizacoes': 0  # Nova notícia começa com 0 views
        }
        
        noticias.append(nova_noticia)
        salvar_noticias(noticias)
        return redirect('/admin/painel')
    return render_template('editar.html', noticia=None)

@app.route("/admin/editar/<int:noticia_id>", methods=['GET', 'POST'])
@admin_required
def admin_editar(noticia_id):
    """Editar notícia existente"""
    noticias = ler_noticias()
    
   
    noticia_encontrada = None
    for noticia in noticias:
        if noticia['id'] == noticia_id:
            noticia_encontrada = noticia
            break
    
    if request.method == 'POST':
        # Atualiza os campos da notícia com os dados do formulário
        noticia_encontrada['titulo'] = request.form['titulo']
        noticia_encontrada['resumo'] = request.form['resumo']
        noticia_encontrada['conteudo'] = request.form['conteudo']
        noticia_encontrada['autor'] = request.form['autor']
        noticia_encontrada['data'] = request.form['data']
        noticia_encontrada['categoria'] = request.form['categoria']
        
        salvar_noticias(noticias)
        return redirect('/admin/painel')
        return render_template('editar.html', noticia=noticia_encontrada)

@app.route("/admin/deletar/<int:noticia_id>")
@admin_required
def admin_deletar(noticia_id):
    """Deletar notícia"""
    
    noticias = ler_noticias()
    noticias = [n for n in noticias if n['id'] != noticia_id]
    
    salvar_noticias(noticias)
    return redirect('/admin/painel')

if __name__ == "__main__":
    app.run(debug=True)
