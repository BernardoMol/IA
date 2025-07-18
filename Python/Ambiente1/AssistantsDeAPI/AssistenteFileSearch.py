#==========================================================
import os
import pandas as pd
import time
#==========================================================
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
cliente = openai.Client()
#==========================================================


# Nome do arquivo para salvar o file_batch.id
FILE_BATCH_ID_FILE = "arquivos/file_batch_id.txt"

vector_store_name = 'apostilas asimov aula 15'

# Verificar se o vector store já existe
vector_store = None
stores = cliente.beta.vector_stores.list()  # Listar todos os vector stores

for store in stores.data:
    if store.name == vector_store_name:
        vector_store = store
        print(f"\n Vector store '{vector_store_name}' já existe.")
        print(f"\n ID ja existente:", vector_store.id)
        break

# Se o vector store não existir, criar um novo
if not vector_store:
    vector_store = cliente.beta.vector_stores.create(
        name=vector_store_name
    )
    print(f"\n Novo vector store '{vector_store_name}' criado.")

# Enviar os arquivos para o vector store
files = ['arquivos/Explorando a API da OpenAI.pdf', 'arquivos/Explorando o Universo das IAs com Hugging Face.pdf']
file_stream = [open(f, 'rb') for f in files]

# Verificar se já existe um file_batch ID salvo
if os.path.exists(FILE_BATCH_ID_FILE):
    with open(FILE_BATCH_ID_FILE, "r") as f:
        file_batch_id = f.read().strip()
    print(f"\n Reutilizando file_batch ID: {file_batch_id}")
else:
    # Fazer o upload dos arquivos
    file_batch = cliente.beta.vector_stores.file_batches.upload_and_poll(
        files=file_stream,
        vector_store_id=vector_store.id
    )
    
    # Salvar o file_batch.id para reutilização futura
    file_batch_id = file_batch.id
    with open(FILE_BATCH_ID_FILE, "w") as f:
        f.write(file_batch_id)  # Agora salva o ID do file_batch
    
    print(f"\n Novo file_batch criado com ID: {file_batch_id}")

# Exibir informações sobre o file_batch
print('\n', file_batch_id)

# Verificar se já existe um Assistant salvo
ASSISTANT_ID_FILE = "arquivos/assistant_tutor_id.txt"  # Nome do arquivo
if os.path.exists(ASSISTANT_ID_FILE):
    with open(ASSISTANT_ID_FILE, "r") as f:
        assistant_id = f.read().strip()
    print(f"\n Reutilizando Assistant ID: {assistant_id}")
else:
    # Criar novo Assistant com o arquivo correto
    assistant = cliente.beta.assistants.create(
        name="Tutor Asimov",
        instructions="Você é um tutor de uma escola de programação. Voce utiliza as apostilas dos cursoso para basear suas respostas. \
            Caso voce nao encontre as respostas nas apostilas informadas, voce fala que nao sabe responder.",
        tools=[{"type": "file_search"}],
        # ==================================================================
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},  
        # O PROBLEMA ESTA AQUI. Sempre que o assistente for criado, ele tem um arquivo csv especifico....
        # ==================================================================
        model="gpt-4o-mini",
    )
    print(f"\n ID ja existente para crair o TUTOR:", vector_store.id)
    assistant_id = assistant.id
    # Salvar o ID para reutilização futura no arquivo com o nome correto
    with open(ASSISTANT_ID_FILE, "w") as f:
        f.write(assistant_id)  # Agora escreve o ID corretamente
    print(f"\n Novo Assistant criado: {assistant_id}")

# Criar Thread
thread = cliente.beta.threads.create()

# Enviar mensagem
mensagem_texto = "Segundo os documentos fornecidos, o que é o Hugging face?"
message = cliente.beta.threads.messages.create(
    thread_id=thread.id, 
    role="user", 
    content=mensagem_texto,
)

# Iniciar execução
run = cliente.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
    instructions="O nome do usuário é Adriano Soares e ele é um usuário Premium.",
)


print("\n MENSAGEM RODANDO")
# Aguardar resposta
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = cliente.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"Status da execução: {run.status}")  # Adicionando o print do status

if run.status == "failed":
    print("Erro na execução:")
    print(run)  # Exibe detalhes do erro, se houver

# Exibir resposta

if run.status == "completed":
    resposta = cliente.beta.threads.messages.list(thread_id=thread.id)
    print("\n=== RESPOSTAS ===\n")
    print('\n' , resposta.data[0].content[0].text.value) 

    mensagens = list(resposta)[0].content[0].text
    anotacoes = mensagens.annotations
    print('\n ANOTAÇÕES \n', anotacoes)
    CITACOES = []
    for index, anotacao in enumerate(anotacoes): 
        CITACOES.append(anotacao)
        print('\n', anotacao.text)
        if file_cit := getattr(anotacao, 'file_citations', None):
            file = cliente.files.retrieve(file_cit.file_id)
            CITACOES.append( f'[{index}] {file.filename}' )
            print('\n', CITACOES)

# # Exibir resposta
# if run.status == "completed":
#     resposta = cliente.beta.threads.messages.list(thread_id=thread.id)
#     print("\n=== RESPOSTAS ===\n")
#     # print(resposta.data[0].content[0].text.value) # estrutura sem o gráfico
#     print('\n COMPLETA EM CHUNK:::: \n' , resposta) # estrutura com o gráfico
#     print('\n SIMPLES E DIRETA:', resposta.data[1].content[0].text.value) # estrutura com o gráfico
#     print('\n DADOS DA IMAGEM: ', resposta.data[0].content[0].image_file.file_id)

#     # Obter o file_id da imagem gerada
#     file_id = resposta.data[0].content[0].image_file.file_id
#     # Baixar a imagem usando o file_id
#     image_data = cliente.files.content(file_id)
#     # Salvar a imagem em um arquivo
#     with open(f'arquivos/{file_id}.png', 'wb') as f:
#         f.write(image_data.read())
#         print(f'Imagem {file_id} salva')

# else:
#     print("Erro:", run.status)

