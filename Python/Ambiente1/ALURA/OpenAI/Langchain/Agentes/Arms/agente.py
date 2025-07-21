from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from langchain.agents import create_openai_tools_agent
from langchain import hub  
from langchain.agents import Tool
from ferramentas import PreferenciasCliente, GerarSugestoes, FiltrarSugestao

load_dotenv()

ARMS_llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

class ARMSagenteOpenAI:
    def __init__(self):
        ARMS_llm  
        preferencias = PreferenciasCliente()
        sugestoes = GerarSugestoes()
        sugestaoFinal = FiltrarSugestao()
        self.tools = [
            #from langchain.agents import Tool
            Tool(name = preferencias.name,
                func = preferencias.run,
                description = preferencias.description),
            Tool(name = sugestoes.name,
                func = sugestoes.run,
                description = sugestoes.description),
            Tool(name = sugestaoFinal.name,
                func = sugestaoFinal.run,
                description = sugestaoFinal.description),
        ]     
        prompt = hub.pull("hwchase17/openai-functions-agent") #from langchain import hub 
        self.agente = create_openai_tools_agent(ARMS_llm, self.tools, prompt)  
        
        
        
