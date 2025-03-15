import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate  # Criação de prompts estruturados
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_ollama import OllamaLLM


def perguntar(pergunta, retriever):
    llm = OllamaLLM(model="llama3.2:latest", temperature=0.0)  # Verifique se o modelo está correto

    # Prompt que direciona a LLM a usar apenas o contexto
    prompt = ChatPromptTemplate.from_template(
        """Baseie-se APENAS no seguinte contexto para responder à pergunta. Se não houver resposta no contexto, diga 'Não encontrado no contexto'. 
        
        Contexto:
        {context}
        
        Pergunta: {input}
        
        Responda apenas com trechos do contexto acima, sem adicionar informações externas.
        """
    )

    # Recuperar documentos relevantes
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
    # Criar embeddings
    embeddings = OllamaEmbeddings(model="llama3.2:latest")  # Verifique se este modelo está disponível no Ollama

    # Criar um text splitter adequado
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)

    # Texto de exemplo
    texto = "Art. 91. O plantão, regulado pelo Conselho da Magistratura, será fiscalizado pela CorregedoriaGeral da Justiça. Art. 92. A escala de juízes e servidores que atuarão no plantão judiciário, e suas alterações, deverá ser cadastrada no sítio eletrônico da Corregedoria-Geral da Justiça pelo chefe de secretaria do foro da comarca-sede da região de plantão ou de cumprimento de mandado respectiva, até o dia 25 (vinte e cinco) do mês anterior ao qual se referir.(redação alterada por meio do Provimento n. 8, de 15 de fevereiro de 2023) § 1º A publicação do nome dos juízes de plantão será divulgada apenas 5 (cinco) dias antes do início do plantão. § 2º Cópia da portaria, com nomes e telefones dos juízes e dos servidores de plantão de cada região, deverá ser afixada nos fóruns, 5 (cinco) dias antes do início do plantão (redação alterada por meio do Provimento n. 8, de 15 de fevereiro de 2023) § 3º (redação revogada por meio do Provimento n. 8, de 15 de fevereiro de 2023)"

    # Dividir o texto em pequenos chunks
    split_documents = text_splitter.split_text(texto)
    print(split_documents)
    # Criar o banco de dados vetorial
    vectorstore = FAISS.from_texts(texts=split_documents, embedding=embeddings)
    faiss.from_documents(embeddings, split_documents)

    # Salvar o banco de dados vetorial localmente
    vectorstore.save_local("DadosVetoriais2")
    print("Banco vetorial atualizado e salvo!")

    # Carregar os dados do banco vetorial FAISS
    vectorstore = FAISS.load_local("DadosVetoriais2", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    # Fazer uma pergunta
    resposta = perguntar("A publicação do nome dos juízes de plantão será divulgada em quantos dias antes do início do plantão? Em qual Art do código de normas consta essa informação?", retriever)
    print(resposta)