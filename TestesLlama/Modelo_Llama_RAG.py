from langchain_core.prompts import ChatPromptTemplate  # Criação de prompts estruturados
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings  # Transforma os textos em embeddings
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Carregar embeddings do modelo
embeddings = OllamaEmbeddings(model="llama3.2:latest") #llama3.2:latest

# Recuperar os dados do banco vetorial FAISS
vectorstore = FAISS.load_local("DadosVetoriais", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

def perguntar(pergunta, retriever):
    llm = OllamaLLM(model="llama3.2:latest", temperature=0.3)

    # Prompt que direciona a LLM a usar apenas o contexto
    prompt = ChatPromptTemplate.from_template(
        """Baseie-se APENAS no seguinte contexto para responder à pergunta. Se não houver resposta no contexto, diga 'Não encontrado no contexto'. 
        
        Contexto:
        {context}
        
        Pergunta: {input}
        
        Responda apenas com trechos do contexto acima, sem adicionar informações externas.
        """
    )

    retrieved_docs = retriever.invoke(pergunta)
    print("Documentos recuperados:", [doc.page_content for doc in retrieved_docs])

    # Criando a cadeia que combina os documentos recuperados com o modelo de linguagem
    documents_chain = create_stuff_documents_chain(llm, prompt)

    # Criando a cadeia de recuperação (RAG)
    retriever_chain = create_retrieval_chain(retriever, documents_chain)

    # Fazendo a consulta
    response = retriever_chain.invoke({"input": pergunta})

    # Retornando a resposta correta (depende do formato de saída do modelo)
    return response.get("answer", "Resposta não encontrada no contexto.")

if __name__ == "__main__":
    #resposta = perguntar("A publicação do nome dos juízes de plantão será divulgada em quantos dias antes do início do plantão? Em qual Art do código de normas consta essa informação?", retriever)
    # A publicação do nome dos juízes de plantão será divulgada em quantos dias antes do início do plantão? Em qual Art do código de normas consta essa informação?
    resposta = perguntar("É responsabilidade do juiz a fiscalização da correta alimentação do sistema informatizado disponibilizado pelo Poder Judiciário?", retriever)
    print(resposta)

