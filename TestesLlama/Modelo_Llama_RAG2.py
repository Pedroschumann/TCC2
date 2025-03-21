from langchain.chains import RetrievalQA
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings

def perguntar(pergunta, tipoEmbeddingUsar):

    if tipoEmbeddingUsar == 1:
        embeddings = HuggingFaceEmbeddings()
        vectorstore = FAISS.load_local("bd_HuggingFace", embeddings, allow_dangerous_deserialization=True)
    
    elif tipoEmbeddingUsar == 2:
        embeddings = OllamaEmbeddings(model="llama3.2:latest")
        vectorstore = FAISS.load_local("bd_llama3", embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever()
    llm = OllamaLLM(model="llama3.2:latest", temperature=0.2)

    chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever
    )

    result = chain.invoke({"query": pergunta})
    return result['result']

if __name__ == "__main__":
    resposta = perguntar("O tabelião pode praticar atos fora do município? De qual documento está me fornecendo essa informação?", 1)
    print(resposta)

