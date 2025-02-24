#from langchain_apenai import OpenAI
from langchain_community.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def oscar(filme, ano, llm):

    prompt = PromptTemplate(
        input_variables=['filme', 'ano'],
        template="Quantos oscars o filme {filme} ganhou em {ano}"
    )

    oscar_chain = LLMChain(llm=llm, prompt=prompt)

    response = oscar_chain({'filme':filme, 'ano':ano})

    return response

llm = OpenAI(temperature=0.5, model='gpt=3.5-turbo-instruct')

if __name__=="__main__":
    response = oscar('Oppenheimer', 2024, llm)
    print(response['text'])
    