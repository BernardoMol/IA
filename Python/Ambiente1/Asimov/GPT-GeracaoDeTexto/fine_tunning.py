import openai
from dotenv import load_dotenv, find_dotenv
import json
import requests
import yfinance as yf

_ = load_dotenv(find_dotenv())
cliente = openai.OpenAI()

## ========================= Tunning ==========================================================
with open("arquivos/chatbot_tunning.json", encoding='utf8') as f:
    json_respostas = json.load(f) # transforma a lista (que estava em JSON) em dicionarios para python
    #print(json_respostas)

with open("arquivos/chatbot_tunning_manipulado.jsonl", 'w', encoding='utf8') as F: # o "w" serve para escrever no arquivo "F"
    for entrada in json_respostas:

        #  Essa deu pau pois o formato do texto estava estranho p caralho
        # resposta = {
        #     "resposta": entrada['resposta'],
        #     "área": entrada['área'],
        #     "fonte": "AsimoBot"
        # }
        # chatbot_tunning_manipulado = {
        #     "messages": [
        #         {'role': 'user', 'content': entrada['pergunta']},
        #         {'role': 'assistant', 'content': json.dumps(resposta, ensure_ascii=False)} #Transforma a resposta em JSON
        #     ]
        # }


        resposta_formatada = f"resposta: {entrada['resposta']} | area: {entrada['área']} | Fonte: AsimoBot"
        chatbot_tunning_manipulado = {
            "messages": [
                {'role': 'user', 'content': entrada['pergunta']},
                {'role': 'assistant', 'content': resposta_formatada} #Transforma a resposta em JSON
            ]
        }
        json.dump(chatbot_tunning_manipulado, F, ensure_ascii = False)
        F.write('\n')
## ============================================================================================

# # Mandando o arquivo criado para o GPT
file = cliente.files.create(
    file = open('arquivos/chatbot_tunning_manipulado.jsonl', 'rb'),
    purpose ='fine-tune'
)

cliente.fine_tuning.jobs.create(
    training_file = file.id,
    model = "gpt-3.5-turbo-0125",
)

cliente.fine_tuning.jobs.list()
