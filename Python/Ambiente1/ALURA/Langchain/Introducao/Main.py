
from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()



cliente = OpenAI(api_key =  os.getenv("OPENAI_API_KEY"))

numero_de_dias = 7
numero_de_criancas = 2
atividade = "praia"

prompt = (
    f"Crie um roteiro de viagem de {numero_de_dias} dias, "
    f"para uma família com {numero_de_criancas} crianças, "
    f"que gostam de {atividade}."
)

mensagens = [{'role': 'user', 'content':'O que é uma maçã em 5 palavras'}]

print(prompt)
resposta = cliente.chat.completions.create(
    messages=[ {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": prompt} ],
    model='gpt-3.5-turbo-0125',
)

print(resposta) 
print("\n")
print(resposta.choices[0].message.content)