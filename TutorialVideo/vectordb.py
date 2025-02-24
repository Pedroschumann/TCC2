from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings # transforma em embeddings cada chank
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import faiss # armazena em um banco de dados vetorial
from langchain_text_splitters import RecursiveCharacterTextSplitter # quebra o texto em pequenos chanks

def url_to_retriver(url):
    # 'https://pt.wikipedia.org/wiki/Oppenheimer_(filme)'
    loader = WebBaseLoader(url)
    docs = loader.load()

    embeddings = OpenAIEmbeddings()

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs) # da pra passar PDF, descrição de vídeos, textos de web scraping

    vector = faiss.from_documents(documents, embeddings)
    # da pra armazenar esses dados em um banco em nuvem, ou algum outro servidor seguro, aqui ele é apenas local

    retriver = vector.as_retriever()
    return retriver