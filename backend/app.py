# ============================================
# MAID IN DEV - SITE DE NOTÍCIAS DE TECNOLOGIA
# ESTILO: MAID DE ANIMES
# ============================================

# Importando as ferramentas necessárias do Flask
# Flask: framework para criar sites
# render_template: função para mostrar páginas HTML
from flask import Flask, render_template

# ============================================
# PASSO 1: CRIAR A APLICAÇÃO
# ============================================
# __name__ é uma variável especial do Python que representa o nome do arquivo atual
# O Flask usa isso para encontrar os arquivos do site (templates, imagens, etc)
app = Flask(__name__)

# ============================================
# PASSO 2: CRIAR O BANCO DE DADOS FICTÍCIO (LISTA DE NOTÍCIAS)
# ============================================
# No lugar de um banco de dados de verdade, usamos uma lista de dicionários
# Cada dicionário é uma notícia
noticias = [
    {
        'id': 1,  # Identificador único da notícia
        'titulo': 'Nova versão do Python é lançada com recursos inspirados em animes',  # Título chamativo
        'resumo': 'A versão 3.12 traz melhorias de performance e uma nova biblioteca para criar assistentes virtuais com estética anime.',  # Resumo curto
        'conteudo': '''
            <p>A comunidade Python está em festa com o lançamento da versão 3.12, que inclui recursos inovadores 
            inspirados no universo dos animes. A nova biblioteca "MaidAI" permite criar assistentes virtuais 
            com personalidade de maid, perfeitas para sites temáticos.</p>
            
            <p>Os desenvolvedores agora podem implementar personagens que interagem com os usuários de forma 
            divertida e estilosa. A biblioteca inclui mais de 50 expressões faciais no estilo anime e 
            vozes personalizáveis.</p>
            
            <p>O criador da biblioteca, conhecido como "Sensei-Dev", comentou: "Queria trazer a fofura das maids 
            para o mundo da programação. Agora qualquer site pode ter sua própria maid digital!"</p>
        ''',  # Conteúdo completo em HTML
        'autor': 'Maid-chan',  # Nome do autor (tema maid)
        'data': '22 de Fevereiro de 2026',  # Data da publicação
        'categoria': 'Programação',  # Categoria da notícia
        'imagem': 'url_da_imagem_python.jpg',  # Nome da imagem (placeholder)
        'visualizacoes': 1337  # Número de visualizações (número maneiro)
    },
    {
        'id': 2,
        'titulo': 'VS Code ganha tema oficial "Maid Mode" com avental animado',
        'resumo': 'A Microsoft lançou uma extensão que transforma sua IDE em uma maid virtual enquanto você codifica.',
        'conteudo': '''
            <p>O editor de código mais usado do mundo agora pode se transformar em uma maid virtual! A extensão 
            "Maid Mode" para VS Code adiciona um personagem animado que fica no canto da tela usando um avental 
            e ajudando o programador com dicas de código.</p>
            
            <p>A personagem, chamada "Code-chan", reage ao que você está digitando. Se você cometer um erro, 
            ela faz uma expressão triste. Se acertar um código complexo, ela comemora com sparkles!</p>
            
            <p>A extensão já tem mais de 100 mil downloads e está entre as mais baixadas da semana. 
            "Programar nunca foi tão fofo", comentou um usuário no Twitter.</p>
        ''',
        'autor': 'Dev-sama',
        'data': '21 de Fevereiro de 2026',
        'categoria': 'Ferramentas',
        'imagem': 'url_da_imagem_vscode.jpg',
        'visualizacoes': 2500
    },
    {
        'id': 3,
        'titulo': 'Inteligência Artificial cria personagens maid em segundos',
        'resumo': 'Nova ferramenta de IA gera artes de maid personalizadas apenas com descrições em texto.',
        'conteudo': '''
            <p>A empresa AnimeTech lançou uma IA especializada em criar personagens no estilo maid. Basta 
            descrever características como cor do cabelo, estilo de avental e expressão facial, e a IA gera 
            uma arte única em poucos segundos.</p>
            
            <p>A ferramenta está sendo usada por desenvolvedores para criar mascotes para seus sites e 
            aplicativos. "Antes eu precisava contratar um ilustrador. Agora eu mesmo posso criar minha 
            própria maid digital", comemorou um usuário.</p>
            
            <p>A IA entende mais de 200 estilos diferentes de avental e 50 tipos de laços. Também é possível 
            gerar animações simples da personagem acenando ou piscando.</p>
        ''',
        'autor': 'IA-chan',
        'data': '20 de Fevereiro de 2026',
        'categoria': 'Inteligência Artificial',
        'imagem': 'url_da_imagem_ia.jpg',
        'visualizacoes': 890
    },
    {
        'id': 4,
        'titulo': 'Framework web "Flask" completa 15 anos com tema especial',
        'resumo': 'Comunidade celebra aniversário do micro-framework com camiseta temática de maid.',
        'conteudo': '''
            <p>O Flask, um dos frameworks web mais amados do Python, completou 15 anos. Para celebrar, 
            a comunidade lançou uma edição limitada de camisetas com o logotipo do Flask vestido de maid.</p>
            
            <p>"O Flask é simples, elegante e eficiente - assim como uma boa maid", brincou o criador do 
            framework em seu blog. "Nada mais justo que homenagear essa estética tão amada pelos 
            desenvolvedores."</p>
            
            <p>A camiseta já está em pré-venda e todo o lucro será doado para projetos de ensino de 
            programação para jovens.</p>
        ''',
        'autor': 'Flask-sensei',
        'data': '19 de Fevereiro de 2026',
        'categoria': 'Web',
        'imagem': 'url_da_imagem_flask.jpg',
        'visualizacoes': 420
    }
]

# ============================================
# PASSO 3: CRIAR A LISTA DE CATEGORIAS
# ============================================
# Extraímos as categorias únicas das notícias
# Isso ajuda a filtrar notícias por categoria depois
categorias = []
for noticia in noticias:
    # Se a categoria ainda não estiver na lista, adiciona
    if noticia['categoria'] not in categorias:
        categorias.append(noticia['categoria'])

# ============================================
# PASSO 4: ROTA PRINCIPAL (PÁGINA INICIAL)
# ============================================
# @app.route("/") é um "decorador" - ele diz ao Flask:
# "Quando alguém acessar a URL / (raiz do site), execute esta função"
@app.route("/")
def home():
    """
    Função que controla a página inicial do site.
    Mostra todas as notícias em ordem (da mais nova para a mais velha).
    """
    # Invertendo a lista para mostrar as notícias mais novas primeiro
    # [::-1] é um "slice" que significa: do início ao fim, mas de trás pra frente
    noticias_recentes = noticias[::-1]
    
    # render_template = função que procura um arquivo HTML na pasta 'templates'
    # e envia dados do Python para ele
    # Estamos enviando:
    # - noticias: a lista completa de notícias
    # - categorias: lista de categorias para o menu
    return render_template(
        'index.html',
        noticias=noticias_recentes,
        categorias=categorias
    )

# ============================================
# PASSO 5: ROTA PARA FILTRAR POR CATEGORIA
# ============================================
# <categoria> é um "parâmetro dinâmico" - pode ser qualquer texto
# Exemplo: /categoria/Programação mostra só notícias de programação
@app.route("/categoria/<categoria>")
def noticias_por_categoria(categoria):
    """
    Filtra as notícias por categoria.
    Exibe apenas as notícias que pertencem à categoria escolhida.
    """
    # List comprehension: uma forma compacta de criar listas
    # Para cada notícia em noticias, inclua na lista se a categoria for igual à escolhida
    noticias_filtradas = [noticia for noticia in noticias if noticia['categoria'] == categoria]
    
    # Inverte para mostrar as mais recentes primeiro
    noticias_filtradas = noticias_filtradas[::-1]
    
    # Mostra a mesma página inicial, mas só com as notícias filtradas
    return render_template(
        'index.html',
        noticias=noticias_filtradas,
        categorias=categorias,
        categoria_atual=categoria  # Informa qual categoria está sendo mostrada
    )

# ============================================
# PASSO 6: ROTA PARA VER UMA NOTÍCIA ESPECÍFICA
# ============================================
# <int:noticia_id> significa: o parâmetro é um número inteiro
# Exemplo: /noticia/1 mostra a notícia com id = 1
@app.route("/noticia/<int:noticia_id>")
def noticia_detalhe(noticia_id):
    """
    Mostra uma notícia completa quando o usuário clica nela.
    noticia_id é o número que vem depois de /noticia/ na URL
    """
    # Procura a notícia com o id especificado
    noticia_encontrada = None  # Começa como vazio
    
    for noticia in noticias:
        if noticia['id'] == noticia_id:
            noticia_encontrada = noticia
            # Incrementa o contador de visualizações (só por diversão)
            noticia['visualizacoes'] += 1
            break  # Para de procurar depois que encontra
    
    # Se não encontrou a notícia, mostra página 404
    if noticia_encontrada is None:
        return "Notícia não encontrada", 404
    
    # Pega 3 notícias aleatórias para sugerir (as primeiras 3 diferentes da atual)
    noticias_sugeridas = []
    for noticia in noticias:
        if noticia['id'] != noticia_id and len(noticias_sugeridas) < 3:
            noticias_sugeridas.append(noticia)
    
    # Mostra a página da notícia
    return render_template(
        'noticia.html',
        noticia=noticia_encontrada,
        noticias_sugeridas=noticias_sugeridas
    )

# ============================================
# PASSO 7: ROTA SOBRE (PÁGINA DE INFORMAÇÕES)
# ============================================
@app.route("/sobre")
def sobre():
    """
    Página com informações sobre o site e sua temática maid.
    """
    return render_template(
        'sobre.html',
        categorias=categorias
    )

# ============================================
# PASSO 8: INICIAR O SERVIDOR
# ============================================
# Este bloco só executa se o arquivo for rodado diretamente
# (não quando é importado por outro arquivo)
if __name__ == "__main__":
    # app.run() inicia o servidor web
    # debug=True significa que o servidor reinicia automaticamente quando mudamos o código
    # Isso é ótimo para desenvolvimento, mas NÃO use em produção
    app.run(debug=True)
