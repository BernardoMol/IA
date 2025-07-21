
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.globals import set_debug # deixa a gente ver BEEEEM mais a fundo o processo da IA
from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv() # é basicamente pedir pra carregar o arquivo .dotenv
set_debug(True) # deixa a gente ver BEEEEM mais a fundo o processo da IA

llm = ChatOpenAI(
    api_key =  os.getenv("OPENAI_API_KEY"),
    model='gpt-3.5-turbo-0125',
    temperature = 0.5 )


class Destino(BaseModel):
    cidade = Field( "Cidade a Visitar")
    motivo = Field( "Motivo pelo qual é interessante visitar a cidade")

parseador = JsonOutputParser(pydantic_object=Destino)

modelo_cidade = PromptTemplate(
    template="""Sugira uma cidade dado interesse por {interesse}.
    {formatacao_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formatacao_de_saida": parseador.get_format_instructions()},
)

cadeia_cidade = LLMChain(prompt = modelo_cidade, llm = llm)

cadeia = SimpleSequentialChain( chains = [cadeia_cidade], verbose = True ) 

resultado = cadeia.invoke("praias") 
print(resultado)