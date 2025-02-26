from langchain_core.prompts import ChatPromptTemplate # isso aqui é outra forma de criar prompt, pra ser mais humano igual o chat gpt
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from vectordb import url_to_retriver

#from langchain_community.llms import openai
from langchain_community.llms import ollama
from langchain_ollama import OllamaLLM

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

#from ollama import chat
#from ollama import ChatResponse

load_dotenv()
#https://pt.wikipedia.org/wiki/Oppenheimer_(filme)
retriver = url_to_retriver('https://www.planalto.gov.br/ccivil_03/leis/l9492.htm')

def perguntar(pergunta):
    llm = OllamaLLM(model="llama3.2:3b", temperature=0.5)

    prompt = ChatPromptTemplate.from_template("""Responda a pergunta com base apenas no contexto:
    {context} 
    Pergunta: {input}
    """)

    documents_chain = create_stuff_documents_chain(llm, prompt)
    retriver_chain = create_retrieval_chain(retriver, documents_chain)
    response = retriver_chain.invoke({"input":pergunta})

    return response


if __name__ == "__main__":
    response = perguntar("Quem pode fazer o cancelamento do registro de protesto além do Tabelião titular?")
    print(response['answer'])