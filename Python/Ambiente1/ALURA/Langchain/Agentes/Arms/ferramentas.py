from langchain.prompts import PromptTemplate
from pydantic import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from typing import List
from dotenv import load_dotenv

import os

load_dotenv()

ARMS_llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

class ContextoDesejado(BaseModel):
    data:str = Field("Dada desejada para a viagem.")
    interesse: List[str] = Field("Interesses informados pelo viajante.")

class PreferenciasCliente(BaseTool):
    name: str = "Preferencia"
    description: str = """Esta ferramenta extrai a DATA e os 
        INTERESSES informados pelo usuario e indica CIDADES BRASILEIRAS 
        boas para viajar com base nestas informações."""

    def _run(self, inputDoUsuario: str) -> str:
        llm = ARMS_llm
        parser = JsonOutputParser(pydantic_object=ContextoDesejado)
        template = PromptTemplate(
            template=
                """Seu papel é EXTRAR a data desejada e os interesses do cliente para uma futura recomendação.
                Entrada:
                -----------------
                {inputDoUsuario}
                -----------------
                Formato de saída:
                {formato_saida}""",
                input_variables=["inputDoUsuario"],
                partial_variables={"formato_saida" : parser.get_format_instructions()})
        
        cadeia = template | llm | parser
        resposta = cadeia.invoke({"inputDoUsuario" : inputDoUsuario})
        print(f"RESPOSTA CRUA: {resposta}")
        
        data = resposta["data"]
        interesses = resposta["interesse"]
        
        print(f"Data: {data}")
        print(f"Interesses: {interesses}")
        
        dadosExtraidos = f"Data: {data} | Interesses: {', '.join(interesses)}"
        return dadosExtraidos
    
class CidadeInfo(BaseModel):
    nome: str = Field(description="Nome da cidade indicada.")
    atrativos: List[str] = Field(description="Lista de atrativos ou locais turísticos da cidade.")

class SugestoesDeCidades(BaseModel):
    cidades: List[CidadeInfo] = Field(description="Lista de cidades sugeridas com seus atrativos.")
  
class GerarSugestoes(BaseTool):
    name: str = "Cidades"
    description: str = """Gera sugestão de 5 cidades para o cliente visitar,
            baseado nas datas e interesses informados.
            Ou seja, esta ferramenta requer como entrada todos os dados de DATA e INTERESSES docliente"""

    def _run(self, inputGeradoPeloGEPETO: str) -> str:
        llm = ARMS_llm
        parser = JsonOutputParser(pydantic_object=SugestoesDeCidades)
        template = PromptTemplate(
            template=
                """
                Persona: você é uma agente de viagens.
                - Com a DATA e os INTERESSES passados a você: Indique 5 cidades brasileiras como destino, usando a data e os interesses informados.
                - Indique os locais mais indicados de cada cidade de acordo com os interesses.
                            
                Entrada:
                -----------------
                {data_e_interesses}
                -----------------
                Formato de saída:
                {formato_saida}""",
                input_variables=["data_e_interesses"],
                partial_variables={"formato_saida" : parser.get_format_instructions()})
        
        cadeia = template | llm | parser
        resposta = cadeia.invoke({"data_e_interesses" : inputGeradoPeloGEPETO})
        print(f"RESPOSTA CRUA: {resposta}")
        
        for cidade in resposta["cidades"]:
            nome = cidade["nome"]
            atrativos = cidade["atrativos"]
            print(f"🗺️ Cidade: {nome}")
            print(f" - Atrativos: {', '.join(atrativos)}")

        indicacoes = "\n".join(
            [f"{cidade['nome']}: {', '.join(cidade['atrativos'])}" for cidade in resposta["cidades"]]
        )
        return indicacoes

class SugestaoFinal(BaseModel):
    cidade: str = Field(description="Nome da cidade indicada.")
    atrativos: List[str] = Field(description="Lista de atrativos ou locais turísticos da cidade.")
    motivos: str = Field(description="Porque esta cidade foi escolhida entre as outras?")
    
class FiltrarSugestao(BaseTool):
    name: str = "SugestaoFinal"
    description: str = """Compara as cidades e respectivas atrações informadas,
            com base em preço e qualidade/avaliações e retorna uma sugestão final de destino."""

    def _run(self, inputCidadesEAtrativosIndicados: str) -> str:
        llm = ARMS_llm
        parser = JsonOutputParser(pydantic_object=SugestaoFinal)
        template = PromptTemplate(
            template=
                """
                
                Persona: você é uma agente de viagens.
                - Com as CIDADES e seus respectivos ATRATIVOS passados a você: 
                    - Avalie o melhor preço dos locais indicados;
                    - Avalie as melhores avaliações dos locais indicados;
                    - Avalie quais locais são mais seguros;
                - Com base nas avaliações, indique o melhor destino final dentre os informados.
                - Informe porque a cidade indicada é o melhor do que as outras como destino para o cliente.
                            
                Entrada:
                -----------------
                {cidades_e_atrativos}
                -----------------
                Formato de saída:
                {formato_saida}""",
                input_variables=["cidades_e_atrativos"],
                partial_variables={"formato_saida" : parser.get_format_instructions()})
        
        cadeia = template | llm | parser
        resposta = cadeia.invoke({"cidades_e_atrativos" : inputCidadesEAtrativosIndicados})
        print(f"RESPOSTA CRUA: {resposta}")
        
        cidade = resposta["cidade"]
        atrativos = resposta["atrativos"]
        motivos = resposta["motivos"]
        print(f"\n🏙️ {cidade}")
        for atrativo in atrativos:
            print(f" - {atrativo}")
        print(f"\n{motivos}")
        
        sugestaoFinal = f"{cidade}:\n" + "\n".join([f" - {a}" for a in atrativos]) + f"\n\nMotivos: {motivos}"
        return sugestaoFinal

