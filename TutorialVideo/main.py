from langchain_community.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

def generate_cat_name(animal_type, color):
    llm =  openai(temperature=0.5)

    prompt_animal_name = PromptTemplate(
        input_variables=['animal_type', 'color'],
        template= "Tenho um {animal_type} filhote novo da cor {color} e gostaria de dar um nome legal para ele, me dê uma lista de 5 nomes."
    )

    animal_name_chain = LLMChain(llm=llm, prompt=prompt_animal_name)
    response = animal_name_chain({'animal_type':animal_type, 'color':color})
    return response

if __name__ == "__main__":
    print(generate_cat_name('gatinho', "marrom"))