# Explorando a API da OpenAI


# Para conectar com a API da openAI
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
cliente = openai.Client()

# mensagens = [{'role': 'user', 'content':'O que é uma maçã em 5 palavras'}]

# resposta  = cliente.chat.completions.create(
#     messages = mensagens,
#     model = 'gpt-3.5-turbo-0125',
#     max_tokens = 1000,
#     temperature = 0
# )

# #print(resposta)
# print(resposta.choices[0].message.content)

# mensagens.append({'role': 'assistant', 'content': resposta.choices[0].message.content})
# mensagens.append({'role': 'user', 'content': 'e qual sua cor?'})
# resposta  = cliente.chat.completions.create(
#     messages = mensagens,
#     model = 'gpt-3.5-turbo-0125',
#     max_tokens = 1000,
#     temperature = 0
# )
# print(resposta.choices[0].message.content)

# #===========================================================================================================
# #   ETAPA: AUTOMAÇÃO POR FUNÇÃO
# #===========================================================================================================
# mensagens = [{'role': 'user', 'content':'O que é uma maçã em 5 palavras'}]
# def geracao_de_texto(mensagens, model='gpt-3.5-turbo-0125', max_tokens=1000, temperature=0):
#     resposta  = cliente.chat.completions.create(
#         messages = mensagens,
#         model = model,
#         max_tokens = max_tokens,
#         temperature = temperature # É o quanto o modelo pode "viajar" na resposta, varia de 0 a 2
#     )
#     print(resposta.choices[0].message.content)
#     # print(resposta.usage) # Mostra quantos tokens (recurso) gastou
#     mensagens.append({'role': 'assistant', 'content': resposta.choices[0].message.content})
#     # resposta_modelada = resposta.choices[0].message.model_dump()
#     resposta_modelada = resposta.choices[0].message.model_dump(exclude_none=True) #tira as partes com null da resposta
#     print('Mensagem da resposta modelada: ' , resposta_modelada)
#     return mensagens

# mensagens = geracao_de_texto(mensagens)
# print(mensagens)

# #===========================================================================================================
# #   ETAPA: RESPOSTA EM STREAM DE TEXTO
# #===========================================================================================================
mensagens = [{'role': 'user', 'content':'Crie uma breve carta de apresentação para estágio'}]

resposta  = cliente.chat.completions.create(
    messages = mensagens,
    model = 'gpt-3.5-turbo-0125',
    max_tokens = 1000,
    temperature = 0,
    stream = True
)

resposta_completa = ''
for stream_resposta in resposta:
    texto = stream_resposta.choices[0].delta.content
    if texto:
        resposta_completa += texto

print(resposta_completa, end='')
