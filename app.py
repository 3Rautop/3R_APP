from flask import Flask, request, render_template
import os
import requests # Importar requests para fazer requisições HTTP
import json     # Importar json para trabalhar com dados JSON

app = Flask(__name__)

# --- CONFIGURAÇÕES DO MERCADO LIVRE ---
# ATENÇÃO: Em uma aplicação de produção, o ideal é que esses valores venham de
# variáveis de ambiente no Render (Settings -> Environment).
# Por enquanto, você pode deixá-los aqui para facilitar o teste.
CLIENT_ID = "4669044255494880"     # <--- SEU Client ID REAL
CLIENT_SECRET = "9ckYUaWxlzI9v1P99pmJLrF6BnrEFqPV" # <--- SUA Secret Key REAL
REDIRECT_URI = "https://threer-app.onrender.com/callback" # A URL que o ML vai redirecionar

# O Code Verifier gerado pelo seu script pkce_generate.py.
# Em uma aplicação mais robusta, este valor seria armazenado temporariamente
# (ex: em uma sessão de usuário) para ser usado neste callback.
# Para o seu teste manual, você já o tem localmente.
# Se você quiser que o Render pegue o token, você teria que ter o Code Verifier aqui.
# Por simplicidade, vamos apenas exibir o code.
# CODE_VERIFIER = "bOAdg3lVr6utsysDyJUXqEAi4DYnkvwm7yhfcBP3oWw" # Você pode colar ele aqui, mas não é estritamente necessário para APENAS exibir o code.

@app.route('/')
def home():
    # Rota para a sua página inicial.
    return render_template('index.html')

@app.route('/callback')
def callback():
    """
    Esta rota é chamada pelo Mercado Livre após o usuário autorizar sua aplicação.
    Ela recebe o 'code' de autorização como um parâmetro da URL.
    """
    code = request.args.get('code') # Pega o código de autorização da URL
    state = request.args.get('state') # Pega o state (parâmetro opcional de segurança)

    if not code:
        # Se o 'code' não veio na URL, significa que houve um erro na autorização do ML.
        error_description = request.args.get('error_description', 'Código de autorização não recebido ou erro desconhecido.')
        return f"Erro na autorização do Mercado Livre: {error_description}", 400
    
    # Se chegamos aqui, o 'code' foi recebido com sucesso.
    # Agora, você pode exibir uma página de sucesso para o usuário.
    # O usuário copiará este 'code' para usar no seu script 'get_token.py' local.
    return render_template('callback_success.html', code=code)


if __name__ == '__main__':
    # Define a porta que o Render vai usar para rodar seu aplicativo.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
