# contrução da API

# objetivo: contruir uma APi que recebe uma pergunta e retorna uma resposta utilizando o código do arquivo Modelo_Llama_RAG2.py
# e um método que roda o código do arquivo TesteBeautifulSoup2.py

#URL base - localhost

#Endpoints:
# /perguntar - GET
# /extrairTextos - POST

# link vídeo youtube: https://www.youtube.com/watch?v=FBLAV1SbJFk

from flask import Flask, request, jsonify
from Modelo_Llama_RAG2 import perguntar
from TesteBeautifulSoup2 import gerarBaseDados

app = Flask(__name__)

# perguntar
@app.route('/perguntar', methods=['GET'])
def realizarPergunta():
    pergunta = request.get_json().get('pergunta')
    resposta = perguntar(pergunta, 1)
    return jsonify({"resposta": resposta})

# extrairTextos com web scraping
@app.route('/extrairTextos', methods=['GET'])
def extrairTextos():
    link = request.json.get('link')
    headers = request.json.get('headers')
    tipoExtracao = request.json.get('tipoExtracao')
    texto = extrairTextos(link, headers, tipoExtracao)
    return jsonify({"texto": texto})

# Adicionar link na lista para web scraping

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='localhost')
