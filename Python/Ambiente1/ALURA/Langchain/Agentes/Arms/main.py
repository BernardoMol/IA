from langchain.agents import AgentExecutor
from agente import ARMSagenteOpenAI
from dotenv import load_dotenv

load_dotenv()

# pergunta = "Quero viajar com minha noiva dia 13/06/2026. Quero visitar os melhores restaurantes e locais romanticos. Qual a melhor cidade?"
pergunta = "Quero viajar com meu pai no final deste ano. Gostamos de cerveja, interior, fazendas, roça essas coisasa. Qual a melhor cidade?"

agente = ARMSagenteOpenAI()
executor = AgentExecutor(agent=agente.agente,
                        tools=agente.tools,
                        verbose=True)
resposta = executor.invoke({"input" : pergunta})
print(resposta)