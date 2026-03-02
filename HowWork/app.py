# ============================================
# IMPORTAÇÕES - Pegando ferramentas que vamos usar
# ============================================

# Flask é o框架 web. Importamos várias ferramentas dele:
# - Flask: cria a aplicação
# - render_template: mostra arquivos HTML
# - request: pega dados de formulários
# - redirect: manda usuário para outra página
# - url_for: cria links dinâmicos
# - session: guarda informações do usuário logado
from flask import Flask, render_template, request, redirect, url_for, session

# json: permite ler e escrever arquivos .json (nossas notícias)
import json

# os: permite verificar se arquivos existem no sistema
import os

# ============================================
# CRIAÇÃO DA APLICAÇÃO
# ============================================

# Cria o site. O __name__ ajuda o Flask a encontrar pastas e arquivos
app = Flask(__name__)

# Chave secreta para criptografar as sessões (login)
# Se mudar isso, todos os logins são invalidados!
app.secret_key = 'maid-secreta-2026'

# ============================================
# CONFIGURAÇÃO DO ADMIN
# ============================================

# Dados do administrador (VOCÊ!)
# Mude a senha depois para algo mais seguro
ADMIN_USER = "teste"
ADMIN_PASS = "teste"

# ============================================
# FUNÇÃO QUE ENVIA STATUS DO ADMIN PARA TODAS AS PÁGINAS
# ============================================

# @app.context_processor significa: esta função roda em TODAS as páginas
# e envia variáveis para o HTML automaticamente
@app.context_processor
def inject_admin_status():
    """Disponibiliza a variável admin_logado para todos os templates"""
    
    # Tenta pegar da sessão se o admin está logado.
    # Se não existir, assume False (não logado)
    admin_status = session.get('admin_logado', False)
    
    # Mostra no terminal (para debug) se o admin está logado ou não
    print(f"🔍 DEBUG: admin_logado = {admin_status}")
    
    # Envia a variável 'admin_logado' para TODOS os HTMLs
    # Assim qualquer página pode fazer {% if admin_logado %}
    return dict(admin_logado=admin_status)

# ============================================
# ROTA DE TESTE - Força admin logado (pode remover depois)
# ============================================

# @app.route cria um endereço na web
# Quando alguém acessar /forcar-admin, esta função roda
@app.route("/forcar-admin")
def forcar_admin():
    # Força a sessão a dizer que admin está logado
    session['admin_logado'] = True
    # Mostra mensagem na tela
    return "Agora você é admin! Volte para a página inicial."

# ============================================
# FUNÇÕES PARA LER E SALVAR NOTÍCIAS
# ============================================

def ler_noticias():
    """Lê as notícias do arquivo JSON"""
    
    # Verifica se o arquivo noticias.json existe (evita erro)
    if os.path.exists('noticias.json'):
        # Abre o arquivo para leitura ('r'), com codificação UTF-8 (permite acentos)
        with open('noticias.json', 'r', encoding='utf-8') as f:
            # json.load() converte o JSON para lista Python
            return json.load(f)
    
    # Se o arquivo não existir, retorna lista vazia
    return []

def salvar_noticias(noticias):
    """Salva as notícias no arquivo JSON"""
    
    # Abre o arquivo para escrita ('w'), com codificação UTF-8
    with open('noticias.json', 'w', encoding='utf-8') as f:
        # json.dump() converte lista Python para JSON e salva
        # indent=4 formata o JSON bonitinho (com espaços)
        # ensure_ascii=False permite acentos e emojis
        json.dump(noticias, f, indent=4, ensure_ascii=False)

# ============================================
# ROTAS PÚBLICAS (TODOS PODEM VER)
# ============================================

# @app.route("/") significa: quando alguém acessar a RAIZ do site...
@app.route("/")
def home():
    """Página inicial - mostra todas as notícias"""
    
    # Chama a função que lê as notícias do JSON
    noticias = ler_noticias()
    
    # noticias[::-1] inverte a lista (do fim para o começo)
    # Assim a notícia mais nova (última da lista) aparece primeiro
    noticias = noticias[::-1]
    
    # Pega as categorias de todas as notícias
    # [n['categoria'] for n in noticias] cria lista com todas as categorias
    # set() remove duplicatas
    # list() converte de volta para lista
    categorias = list(set([n['categoria'] for n in noticias]))
    
    # render_template mostra o arquivo HTML e envia dados para ele
    # Estamos enviando:
    # - noticias: lista de notícias
    # - categorias: lista de categorias únicas
    return render_template('index.html', noticias=noticias, categorias=categorias)

@app.route("/sobre")
def sobre():
    """Página Sobre - informações do site"""
    
    # Mostra o arquivo sobre.html (sem enviar dados)
    return render_template('sobre.html')

# <categoria> significa: este pedaço da URL é uma VARIÁVEL
# Exemplo: /categoria/Programação faz categoria = "Programação"
@app.route("/categoria/<categoria>")
def noticias_por_categoria(categoria):
    """Filtra notícias por categoria"""
    
    # Lê todas as notícias
    noticias = ler_noticias()
    
    # Compreensão de lista: para cada notícia em noticias,
    # mantenha apenas aquelas cuja categoria é igual à recebida
    noticias_filtradas = [n for n in noticias if n['categoria'] == categoria]
    
    # Inverte para mostrar mais novas primeiro
    noticias_filtradas = noticias_filtradas[::-1]
    
    # Pega categorias para o menu (igual na home)
    categorias = list(set([n['categoria'] for n in noticias]))
    
    # Mostra a mesma página index.html, mas só com notícias filtradas
    return render_template('index.html', noticias=noticias_filtradas, categorias=categorias)

# <int:noticia_id> significa: a variável deve ser um NÚMERO INTEIRO
@app.route("/noticia/<int:noticia_id>")
def noticia_detalhe(noticia_id):
    """Página de uma notícia específica"""
    
    # Lê todas as notícias
    noticias = ler_noticias()
    
    # Variável para guardar a notícia encontrada (começa vazia)
    noticia_encontrada = None
    
    # Percorre todas as notícias procurando pelo id
    for noticia in noticias:
        if noticia['id'] == noticia_id:
            # Achou! Guarda a notícia
            noticia_encontrada = noticia
            # Aumenta o contador de visualizações
            noticia['visualizacoes'] += 1
            # Para de procurar (já achou)
            break
    
    # Se encontrou a notícia
    if noticia_encontrada:
        # Salva as notícias (com a visualização atualizada)
        salvar_noticias(noticias)
        # Mostra a página da notícia, enviando a notícia encontrada
        return render_template('noticia.html', noticia=noticia_encontrada)
    
    # Se não encontrou, mostra erro 404 (página não encontrada)
    return "Notícia não encontrada", 404

# ============================================
# ROTAS DE ADMIN (PROTEGIDAS POR SENHA)
# ============================================

# methods=['GET', 'POST'] significa:
# - GET: quando alguém ACESSA a página
# - POST: quando alguém ENVIA o formulário
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    """Página de login do admin"""
    
    # Se o método for POST (enviou formulário)
    if request.method == 'POST':
        # Pega os dados digitados no formulário
        username = request.form['username']
        password = request.form['password']
        
        # Verifica se usuário e senha conferem com os salvos
        if username == ADMIN_USER and password == ADMIN_PASS:
            # Se acertou, MARCA na sessão que admin está logado
            # Isto é a MAGIA: agora o site "lembra" que você é admin
            session['admin_logado'] = True
            # Redireciona para o painel admin
            return redirect('/admin/painel')
        else:
            # Se errou, mostra a página de login com mensagem de erro
            return render_template('admin_login.html', erro="Usuário ou senha inválidos")
    
    # Se método for GET (só acessou a página), mostra formulário vazio
    return render_template('admin_login.html')

@app.route("/admin/logout")
def admin_logout():
    """Faz logout do admin"""
    
    # Remove a marca de admin logado da sessão
    # pop remove o item, None é valor padrão se não existir
    session.pop('admin_logado', None)
    # Redireciona para a página inicial
    return redirect('/')

# ============================================
# FUNÇÃO DECORADORA - PROTEGE ROTAS ADMIN
# ============================================

def admin_required(f):
    """Decorator para verificar se o admin está logado"""
    
    def decorated_function(*args, **kwargs):
        # Verifica se NÃO está logado
        if not session.get('admin_logado'):
            # Se não estiver, manda para o login
            return redirect('/admin/login')
        # Se estiver, executa a função original
        return f(*args, **kwargs)
    
    # Mantém o nome original da função (para não confundir o Flask)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ============================================
# ROTAS ADMIN (PROTEGIDAS)
# ============================================

# @admin_required significa: só executa se admin estiver logado!
@app.route("/admin/painel")
@admin_required
def admin_painel():
    """Painel administrativo - lista todas as notícias"""
    
    # Lê todas as notícias
    noticias = ler_noticias()
    # Inverte (mais novas primeiro)
    noticias = noticias[::-1]
    # Mostra painel com a lista de notícias
    return render_template('admin.html', noticias=noticias)

@app.route("/admin/criar", methods=['GET', 'POST'])
@admin_required
def admin_criar():
    """Criar nova notícia"""
    
    # Se enviou o formulário
    if request.method == 'POST':
        # Lê notícias existentes
        noticias = ler_noticias()
        
        # Define o ID da nova notícia
        novo_id = 1
        if noticias:
            # Pega o maior ID existente e soma 1
            # max([n['id'] for n in noticias]) encontra o maior id
            novo_id = max([n['id'] for n in noticias]) + 1
        
        # Cria um dicionário com os dados do formulário
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
        
        # Adiciona a nova notícia à lista
        noticias.append(nova_noticia)
        # Salva a lista atualizada no JSON
        salvar_noticias(noticias)
        # Volta para o painel
        return redirect('/admin/painel')
    
    # Se for GET (acessou a página), mostra formulário vazio
    # noticia=None indica que é criação (não tem notícia para editar)
    return render_template('editar.html', noticia=None)

@app.route("/admin/editar/<int:noticia_id>", methods=['GET', 'POST'])
@admin_required
def admin_editar(noticia_id):
    """Editar notícia existente"""
    
    # Lê todas as notícias
    noticias = ler_noticias()
    
    # Procura a notícia com o id recebido
    noticia_encontrada = None
    for noticia in noticias:
        if noticia['id'] == noticia_id:
            noticia_encontrada = noticia
            break
    
    # Se enviou o formulário (POST)
    if request.method == 'POST':
        # Atualiza os campos da notícia com os dados do formulário
        noticia_encontrada['titulo'] = request.form['titulo']
        noticia_encontrada['resumo'] = request.form['resumo']
        noticia_encontrada['conteudo'] = request.form['conteudo']
        noticia_encontrada['autor'] = request.form['autor']
        noticia_encontrada['data'] = request.form['data']
        noticia_encontrada['categoria'] = request.form['categoria']
        
        # Salva a lista atualizada
        salvar_noticias(noticias)
        # Volta para o painel
        return redirect('/admin/painel')
    
    # Se for GET, mostra formulário PREENCHIDO com os dados atuais
    return render_template('editar.html', noticia=noticia_encontrada)

@app.route("/admin/deletar/<int:noticia_id>")
@admin_required
def admin_deletar(noticia_id):
    """Deletar notícia"""
    
    # Lê todas as notícias
    noticias = ler_noticias()
    
    # Cria nova lista contendo apenas notícias com id DIFERENTE do recebido
    # Isso remove a notícia que queremos deletar
    noticias = [n for n in noticias if n['id'] != noticia_id]
    
    # Salva a lista (sem a notícia deletada)
    salvar_noticias(noticias)
    # Volta para o painel
    return redirect('/admin/painel')

# ============================================
# PONTO DE ENTRADA - INICIA O SERVIDOR
# ============================================

# Este bloco só executa se o arquivo for RODADO DIRETAMENTE
# (não quando importado por outro arquivo)
if __name__ == "__main__":
    # Inicia o servidor web
    # debug=True significa:
    # - Mostra erros detalhados
    # - Reinicia automaticamente quando mudamos o código
    app.run(debug=True)
