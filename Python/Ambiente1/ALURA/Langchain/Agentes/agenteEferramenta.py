import json
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.pydantic_v1 import Field, BaseModel
from pydantic import BaseModel, Field


from langchain.agents import Tool
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env


def busca_dados_de_estudante(estudante):
    dados = pd.read_csv("documentos/estudantes.csv")
    dados_com_esse_estudante = dados[dados["USUARIO"] == estudante]
    if dados_com_esse_estudante.empty:
        return {}
    return dados_com_esse_estudante.iloc[:1].to_dict()

class ExtratorDeEstudante(BaseModel):
    estudante:str = Field("Nome do estudante com o formato sempre em letras minúsculas, exemplo joão, pedro, maria")


# region REGIÃO DE FERRAEMNTAS
class DadosDeEstudante(BaseTool):
    name: str = "FerramentaDadosDeEestudante"
    description: str = """Esta ferramenta extrai o histórico e preferências de um estudante de acordo com seu histórico"""
    def _run(self, input: str) -> str:
       
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")
        )
       
        parser = JsonOutputParser(pydantic_object=ExtratorDeEstudante)
        template = PromptTemplate(template="""Você deve analisar a {input} para extrair o nome de usuário informado.
        Formato de saída:
        {formato_saida}""",
        input_variables=["input"],
        partial_variables={"formato_saida" : parser.get_format_instructions()}
        )
        cadeia = template | llm | parser
        resposta = cadeia.invoke({"input" : input})
        # print(resposta)
        # return resposta['estudante']
        estudante = resposta['estudante']
        dados = busca_dados_de_estudante(estudante) # estes dados retornados pelo pandas é um dicionario python
        print ("achei")
        print (dados)
        return json.dumps(dados) # devolvo transformando o dicionario em uma string json


# endregion FIM DA REGIÃO DE FERRAMENTAS

# region CRIANDO AGENTE
largeLenguageModel = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")
        )

objetoDaClasseDaFeramentaDadosDeEstudante = DadosDeEstudante()

tools = [
    Tool(
        name = objetoDaClasseDaFeramentaDadosDeEstudante.name,
        description=objetoDaClasseDaFeramentaDadosDeEstudante.description,
        func = objetoDaClasseDaFeramentaDadosDeEstudante.run,        
    )
]
prompt = hub.pull("hwchase17/openai-functions-agent")

agente = create_openai_tools_agent(largeLenguageModel, tools, prompt)
executor = AgentExecutor(agent = agente,
                         tools = tools,
                         verbose = True)

# endregion CRIANDO AGENTE

pergunta = "Quais os dados da Ana?"
resposta = executor.invoke( {"input": pergunta} )
print(resposta)
