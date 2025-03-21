import requests
from bs4 import BeautifulSoup
import re
import os
from langchain.chains import RetrievalQA
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import FAISS # armazena em um banco de dados vetorial
from langchain_text_splitters import RecursiveCharacterTextSplitter # quebra o texto em pequenos chanks
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
os.environ['USER_AGENT'] = 'myagent'

def extrairTexto(link, headers):
    requisicao = requests.get(link, headers=headers)
    #print(requisicao)

    textoRetorno = ""

    # Verificando se a requisição foi bem-sucedida
    if requisicao.status_code == 200:
        site = BeautifulSoup(requisicao.text, "html.parser")

        # Filtrando os parágrafos que não possuem a tag <strike> dentro deles
        paragrafos_filtrados = []

        for p in site.find_all("p"):
            if not p.find("strike") and not p.find("s") and not "redação revogada" in p.get_text().lower() and not "nossas redes sociais" in p.get_text().lower():
                paragrafos_filtrados.append(p)
        
        for texto in paragrafos_filtrados:
            paragrafo = texto.get_text()
            texto_limpo = re.sub(r'\s+', ' ', paragrafo.replace("\n", " ")).strip()
            if texto_limpo and "(VETADO)" not in texto_limpo:
                textoRetorno += "\n"+texto_limpo
        
    else:
        print(f"Erro ao acessar a página. Código de status: {requisicao.status_code}")
    
    return textoRetorno

def extrairLinks(link, headers, tipoExtracao):
    '''
        Método retorna um array com os diferentes links encontrados, não retorna links repetidos.

        tipos de extração:
        1 - qualquer <a> presente na página
        2 - os <a> dentro de listas <li>, considerando apenas as <li> mais internas. (Usado no código de normas)
    '''

    requisicao = requests.get(link, headers=headers)
    #print(requisicao)

    linksRetorno = []

    # Verificando se a requisição foi bem-sucedida
    if requisicao.status_code == 200:
        site = BeautifulSoup(requisicao.text, "html.parser")

        if tipoExtracao == 1: 
            links = site.find_all("a", href=True)
            for link in links:
                linksRetorno.append(link["href"])
        
        elif tipoExtracao == 2:
            for li in site.find_all("li"):
                if not li.find("li") and not li.find("ul"):
                    link = li.find("a", href=True)
                    if link and "http" in link["href"]:
                        linksRetorno.append(link["href"])

    else:
        print(f"Erro ao acessar a página. Código de status: {requisicao.status_code}")

    return linksRetorno

def adicionarTextoAoBancoVetorial(vectorstore, texto, text_splitter, embeddings):
    split_documents = text_splitter.split_text(texto)
    
    if vectorstore:
        vectorstore.add_texts(split_documents)
    else:
        vectorstore = FAISS.from_texts(texts=split_documents, embedding=embeddings)

    return vectorstore

def gerarBaseDados():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    link_lei_9492_protestos = "https://www.planalto.gov.br/ccivil_03/leis/l9492.htm"
    link_codigo_normas = "https://www.tjsc.jus.br/web/codigo-de-normas/indice"
    link_lei_8935_cartorios = "https://www.planalto.gov.br/ccivil_03/leis/l8935.htm"

    embeddings = HuggingFaceEmbeddings()
    #embeddings = OllamaEmbeddings(model="llama3.2:latest")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n(?=Art\\.\s\d+)", "\n\n", ".", " "],  # Priorizando quebras antes de artigos
        chunk_size=1000,  # Boa relação entre precisão e contexto
        chunk_overlap=200  # Mantendo uma sobreposição para continuidade do sentido
    )

    vectorstore = None

# ====================================== Código de Normas =======================================

    links = extrairLinks(link_codigo_normas, headers, 2)
    for link in links:
        texto = extrairTexto(link, headers)
        if texto.strip():
            vectorstore = adicionarTextoAoBancoVetorial(vectorstore, texto, text_splitter, embeddings)
    print("Texto código de normas extraído e adicionado ao banco vetorial")

# ====================================== Lei de protestos ======================================

    texto = extrairTexto(link_lei_9492_protestos, headers)
    if texto.strip():
        vectorstore = adicionarTextoAoBancoVetorial(vectorstore, texto, text_splitter, embeddings)
    print("Texto lei 9492 (protestos) extraído e adicionado ao banco vetorial")

# ====================================== Lei dos cartórios ======================================

    texto = extrairTexto(link_lei_8935_cartorios, headers)
    if texto.strip():
        vectorstore = adicionarTextoAoBancoVetorial(vectorstore, texto, text_splitter, embeddings)
    print("Texto lei 8935 (cartorios) extraído e adicionado ao banco vetorial")


    vectorstore.save_local("bd_HuggingFace")
    print("Banco vetorial salvo!")

if __name__ == "__main__":
    gerarBaseDados()