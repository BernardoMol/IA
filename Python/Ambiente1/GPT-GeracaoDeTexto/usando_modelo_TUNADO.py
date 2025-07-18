import openai
from dotenv import load_dotenv, find_dotenv
import json
import requests
import yfinance as yf

_ = load_dotenv(find_dotenv())
cliente = openai.OpenAI()
##======================= 1 e 2 formato =============================================
# ## 1 formato
# mensagens = [{'role': 'user', 'content':'O que é uma equação quadratica?'}]

# ## 2 formato
# system_mes = '''
# Responda as perguntas em um parágrafo de até 20 palavras. Categorize as respostas no seguintes
# ,→ conteúdos: física, matemática, língua portuguesa ou outros.
# Retorne a resposta em um formato json, com as keys:
# fonte: valor deve ser sempre AsimoBot
# resposta: a resposta para a pergunta
# categoria: a categoria da pergunta
# '''
# mensagens = [{'role': 'user', 'content':system_mes}]

# resposta  = cliente.chat.completions.create(
#     messages = mensagens,
#     model = 'gpt-3.5-turbo-0125',
#     max_tokens = 1000,
#     temperature = 0
# )
# print(resposta.choices[0].message.content)

##======================= 3 formato =============================================
## PARECE COM O PRIMEIRO FORMATO, MAS ELE USA NOSSO MODELO TREINADO ANTERIORMENTE
mensagens = [{'role': 'user', 'content':'O que é uma equação quadratica?'}]
resposta  = cliente.chat.completions.create(
    messages = mensagens,
    # model = 'gpt-3.5-turbo-0125',
    model = 'ft:gpt-3.5-turbo-0125:mol::Ay0AZjqc', # Nosso modelo TUNADO
    max_tokens = 1000,
    temperature = 0
)
print(resposta.choices[0].message.content)