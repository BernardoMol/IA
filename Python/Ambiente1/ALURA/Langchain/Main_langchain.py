
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv() # é basicamente pedir pra carregar o arquivo .dotenv

numero_de_dias = 7
numero_de_criancas = 2
atividade = "praia"

# Configurando o acesso a API da openAI
llm = ChatOpenAI(
    api_key =  os.getenv("OPENAI_API_KEY"),
    model='gpt-3.5-turbo-0125',
    temperature = 0.5 )
# Definndo meu prompt
prompt = (
    f"Crie um roteiro de viagem de {numero_de_dias} dias, "
    f"para uma família com {numero_de_criancas} crianças, "
    f"que gostam de {atividade}."
)

# Acessandoa API commeu prompt
resposta = llm.invoke(prompt)
# print(prompt)
# print(resposta)
# print()
# print(resposta.content)

#Fazendo o acesso com um TEMPLATE de prompt (achei meio inutil por enquanto....)
template = PromptTemplate.from_template(
    "Crie um roteiro de viagem de {dias} dias, "
    "para uma família com {criancas} crianças, "
    "que gostam de {atividade}."
)
prompt2 = template.format(dias = numero_de_dias, criancas = numero_de_criancas, atividade = atividade)
print(prompt2)

resposta = llm.invoke(prompt2)
print(resposta.content)