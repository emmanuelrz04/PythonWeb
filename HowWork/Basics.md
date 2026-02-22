   ANÁLOGIA

Cliente senta e pede -->	Usuário digita URL
Cozinha (backend) prepara --> Servidor Flask processa
Garçom leva o pedido -->	Rota direciona a requisição
Chef prepara a comida -->	Função Python executa
Garçom entrega o prato -->	HTML é renderizado

Em outra palavras:

1. USUÁRIO digita: http://127.0.0.1:5000/
                ↓
2. NAVEGADOR envia REQUISIÇÃO para o servidor
                ↓
3. SERVIDOR Flask recebe a requisição
                ↓
4. ROTEAMENTO: Flask procura a função certa (@app.route)
                ↓
5. FUNÇÃO Python executa (busca dados, processa)
                ↓
6. TEMPLATE recebe os dados e monta o HTML
                ↓
7. RESPOSTA volta para o navegador
                ↓
8. USUÁRIO vê a página linda
