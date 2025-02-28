from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaEmbeddings # transforma em embeddings cada chank
#from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.vectorstores import FAISS # armazena em um banco de dados vetorial
from langchain_text_splitters import RecursiveCharacterTextSplitter # quebra o texto em pequenos chanks

def url_to_retriver(url):
    # 'https://pt.wikipedia.org/wiki/Oppenheimer_(filme)'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"} # Evitar bloqueio por User-Agent: Alguns sites bloqueiam solicitações automáticas se não houver um User-Agent configurado.
    loader = WebBaseLoader(url, requests_kwargs={"headers": headers})
    docs = loader.load()

    for doc in docs:
        print(doc.page_content)

    #embeddings = OpenAIEmbeddings()
    embeddings = OllamaEmbeddings(model="llama3.2:1b")

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs) # da pra passar PDF, descrição de vídeos, textos de web scraping

    vector = FAISS.from_documents(documents, embeddings)
    # da pra armazenar esses dados em um banco em nuvem, ou algum outro servidor seguro, aqui ele é apenas local

    retriver = vector.as_retriever()
    return retriver