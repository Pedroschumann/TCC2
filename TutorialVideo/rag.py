from langchain_core.prompts import ChatPromptTemplate # isso aqui é outra forma de criar prompt, pra ser mais humano igual o chat gpt
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from vectordb import url_to_retriver
from ChatBotVideo import llm

prompt = ChatPromptTemplate.from_template("""Responda a pergunta com base apenas no contexto:
{context} 
Pergunta: {input}
"""                                         
)

documents_chain = create_stuff_documents_chain(llm, prompt)
retriver = url_to_retriver('https://pt.wikipedia.org/wiki/Oppenheimer_(filme)')
retriver_chain = create_retrieval_chain(retriver, documents_chain)
response = retriver_chain.invoke({"input":"QUantos oscars o filme Oppenheimer ganhou em 2024"})
print(response['answer'])
