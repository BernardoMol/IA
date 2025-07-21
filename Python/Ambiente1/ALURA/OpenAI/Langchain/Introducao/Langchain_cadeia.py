
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.globals import set_debug # deixa a gente ver BEEEEM mais a fundo o processo da IA
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv() # é basicamente pedir pra carregar o arquivo .dotenv
set_debug(False) # se estiver como "TRUE" deixa a gente ver BEEEEM mais a fundo o processo da IA

llm = ChatOpenAI(
    api_key =  os.getenv("OPENAI_API_KEY"),
    model='gpt-3.5-turbo-0125',
    temperature = 0.5 )

modelo_cidade = ChatPromptTemplate.from_template(
    "Sugira uma cidade dado meu interesse por {interesse}"
)
modelo_restaurantes = ChatPromptTemplate.from_template(
    "Sugira restaurantes em {cidade}"
)
modelo_cultural = ChatPromptTemplate.from_template(
    "Sugira atividades e locais culturais em {cidade}"
)

cadeia_cidade = LLMChain(prompt = modelo_cidade, llm = llm)
cadeia_restaurantes = LLMChain(prompt = modelo_restaurantes, llm = llm)
cadeia_cultural = LLMChain(prompt = modelo_cultural, llm = llm)

# a Simple pega a saida da chain anterior e usa como entrada da posterior
cadeia = SimpleSequentialChain( chains = [cadeia_cidade,cadeia_restaurantes,cadeia_cultural], verbose = False ) # verbose TRUE nos da mais logs
# resolve o problema, mas ele gera prompts enormes internamente, consumindo mais tokens
  
resultado = cadeia.invoke("praias") #IMPORTANTE: passamos o parametro "interesse", o "ciade" ele descobre sozinhio
print(resultado)