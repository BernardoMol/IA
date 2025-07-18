import os
import pandas as pd
import openai
from dotenv import load_dotenv, find_dotenv
import time

# Carregar variáveis de ambiente
_ = load_dotenv(find_dotenv())
cliente = openai.Client()

# Caminho dos arquivos
FILE_PATH = "arquivos/supermarket_sales.csv"
ASSISTANT_ID_FILE = "arquivos/assistant_id.txt"

# Criar pasta "arquivos" se não existir
os.makedirs("arquivos", exist_ok=True)

# Ler CSV (só para confirmar que está OK)
dataset = pd.read_csv(FILE_PATH)
print(dataset.head(5))

# Fazer upload do arquivo para a OpenAI
file = cliente.files.create(file=open(FILE_PATH, "rb"), purpose="assistants")
print('\n' , file.id)

# Verificar se já existe um Assistant salvo
if os.path.exists(ASSISTANT_ID_FILE):
    with open(ASSISTANT_ID_FILE, "r") as f:
        assistant_id = f.read().strip()
    print(f"\n Reutilizando Assistant ID: {assistant_id}")
else:
    # Criar novo Assistant com o arquivo correto
    assistant = cliente.beta.assistants.create(
        name="Analista Financeiro de Supermercado",
        instructions="Você é um analista financeiro de um supermercado. Use o arquivo .csv para analisar as vendas do supermercado.",
        tools=[{"type": "code_interpreter"}],
        # ==================================================================
        tool_resources={"code_interpreter": {"file_ids": [file.id]}},  
        # O PROBLEMA ESTA AQUI. Sempre que o assistente for criado, ele tem um arquivo csv especifico....
        # ==================================================================
        model="gpt-4o",
    )
    assistant_id = assistant.id
    # Salvar o ID para reutilização futura
    with open(ASSISTANT_ID_FILE, "w") as f:
        f.write(assistant_id)
    print(f"\n Novo Assistant criado: {assistant_id}")

# Criar Thread
thread = cliente.beta.threads.create()

# Enviar mensagem
mensagem_texto = "Qual é o rating médio das vendas do supermercado? Utilize o arquivo em .csv. Gere tambem um grafico de pizza com o percentual de vendas por meio de pagamentoo"
message = cliente.beta.threads.messages.create(
    thread_id=thread.id, role="user", content=mensagem_texto
)

# Iniciar execução
run = cliente.beta.threads.runs.create(
    thread_id=thread.id, assistant_id=assistant_id, instructions='O nome do usuário é "Bernardo".'
)

# Aguardar resposta
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = cliente.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# Exibir resposta
if run.status == "completed":
    resposta = cliente.beta.threads.messages.list(thread_id=thread.id)
    print("\n=== RESPOSTAS ===\n")
    # print(resposta.data[0].content[0].text.value) # estrutura sem o gráfico
    print('\n COMPLETA EM CHUNK:::: \n' , resposta) # estrutura com o gráfico
    print('\n SIMPLES E DIRETA:', resposta.data[1].content[0].text.value) # estrutura com o gráfico
    print('\n DADOS DA IMAGEM: ', resposta.data[0].content[0].image_file.file_id)

    # Obter o file_id da imagem gerada
    file_id = resposta.data[0].content[0].image_file.file_id
    # Baixar a imagem usando o file_id
    image_data = cliente.files.content(file_id)
    # Salvar a imagem em um arquivo
    with open(f'arquivos/{file_id}.png', 'wb') as f:
        f.write(image_data.read())
        print(f'Imagem {file_id} salva')

else:
    print("Erro:", run.status)

# ESTE É UM EXEMPLO DE RESPOSTA DA API. O QUE FODA É QUE A OPRDEM DAS RESPOSTAS NOS ARRAYS MUDA TODA VEZ QUE VOCE GERA A RESPOSTA
# POR ISSO A DIFICULDADE DE COLOCAR A RESPOSTA SIMPLES
# TERIA QUE ITERAR SOBRE AS RESPOSTAS E DAR UM SEARCH C AS PALAVRAS CVHAVE.......TRAMPO FEIO E CHATO, PQP
# {
#   "data": [
#     {
#       "id": "msg_P9t7h9UGrOb9eSaRQwtPPR50",
#       "assistant_id": "asst_IY3Mz9SC4WEwZEuGrtTC5Wtf",
#       "attachments": [],
#       "completed_at": null,
#       "content": [
#         {
#           "type": "image_file",
#           "image_file": {
#             "file_id": "file-J8hXaE8L6jB7Db11te9kpW",
#             "detail": null
#           }
#         },
#         {
#           "type": "text",
#           "text": {
#             "annotations": [],
#             "value": "O rating médio das vendas do supermercado é de aproximadamente \\(6.97\\).\n\nAlém disso, o gráfico de pizza acima ilustra a distribuição das vendas por método de pagamento. Cada setor do gráfico representa a porcentagem de vendas realizadas através de cada método de pagamento (e-wallet, cartão de crédito, etc.)."
#           }
#         }
#       ],
#       "created_at": 1740596652,
#       "incomplete_at": null,
#       "incomplete_details": null,
#       "metadata": {},
#       "object": "thread.message",
#       "role": "assistant",
#       "run_id": "run_1kd3qnofWqhiubJxSD3tOD3x",
#       "status": null,
#       "thread_id": "thread_5Tpl27WwL4c1elgbr4pzevNB"
#     },
#     {
#       "id": "msg_ODFmurA43EyfVldwKdKzirVd",
#       "assistant_id": "asst_IY3Mz9SC4WEwZEuGrtTC5Wtf",
#       "attachments": [],
#       "completed_at": null,
#       "content": [
#         {
#           "type": "text",
#           "text": {
#             "annotations": [],
#             "value": "O arquivo CSV contém informações sobre vendas em um supermercado, incluindo, entre outras colunas, as seguintes:\n\n- `Rating`: Avaliação da venda.\n- `Payment`: Método de pagamento.\n\nVamos agora calcular o rating médio das vendas e, em seguida, criar um gráfico de pizza para mostrar a distribuição das vendas por método de pagamento."
#           }
#         }
#       ],
#       "created_at": 1740596641,
#       "incomplete_at": null,
#       "incomplete_details": null,
#       "metadata": {},
#       "object": "thread.message",
#       "role": "assistant",
#       "run_id": "run_1kd3qnofWqhiubJxSD3tOD3x",
#       "status": null,
#       "thread_id": "thread_5Tpl27WwL4c1elgbr4pzevNB"
#     },
#     {
#       "id": "msg_Gpnxl57AvlVVxshB8Jw7WclQ",
#       "assistant_id": "asst_IY3Mz9SC4WEwZEuGrtTC5Wtf",
#       "attachments": [],
#       "completed_at": null,
#       "content": [
#         {
#           "type": "text",
#           "text": {
#             "annotations": [],
#             "value": "Primeiro, vou abrir e analisar o arquivo CSV para entender sua estrutura e identificar as colunas relevantes para calcular o rating médio e o percentual de vendas por meio de pagamento. Vamos começar."
#           }
#         }
#       ],
#       "created_at": 1740596635,
#       "incomplete_at": null,
#       "incomplete_details": null,
#       "metadata": {},
#       "object": "thread.message",
#       "role": "assistant",
#       "run_id": "run_1kd3qnofWqhiubJxSD3tOD3x",
#       "status": null,
#       "thread_id": "thread_5Tpl27WwL4c1elgbr4pzevNB"
#     },
#     {
#       "id": "msg_E4uZf9uDnELAp3YKpLpu7ZSv",
#       "assistant_id": null,
#       "attachments": [],
#       "completed_at": null,
#       "content": [
#         {
#           "type": "text",
#           "text": {
#             "annotations": [],
#             "value": "Qual é o rating médio das vendas do supermercado? Utilize o arquivo em .csv. Gere tambem um grafico de pizza com o percentual de vendas por meio de pagamentoo"
#           }
#         }
#       ],
#       "created_at": 1740596631,
#       "incomplete_at": null,
#       "incomplete_details": null,
#       "metadata": {},
#       "object": "thread.message",
#       "role": "user",
#       "run_id": null,
#       "status": null,
#       "thread_id": "thread_5Tpl27WwL4c1elgbr4pzevNB"
#     }
#   ],
#   "object": "list",
#   "first_id": "msg_P9t7h9UGrOb9eSaRQwtPPR50",
#   "last_id": "msg_E4uZf9uDnELAp3YKpLpu7ZSv",
#   "has_more": false
# }
