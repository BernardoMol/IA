# Explorando a API da OpenAIApresentando a Assistants API
# =============================================
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

cliente = openai.Client()
# ============================================

assistant = cliente.beta.assistants.create(
    name = "Tutor de Matematica",
    instructions = 'Voce é um tutor particular de matemática. Escreva e execute codigos para responder as perguntas que lhe forem passadas.',
    tools = [{'type': 'code_interpreter'}],
    model="gpt-3.5-turbo-0125",
)

thread = cliente.beta.threads.create()
message = cliente.beta.threads.messages.create(
    thread_id = thread.id,
    role='user',
    content='Se eu jogar um dado honesto 1000 vezes, qual é a probabilidade de eu obter exatamente 150 vezes o numero 6? Resolva com um código.'
)

run = cliente.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id,
    instructions='O nome do usuário é "Bernardo"'
)


import time
while run.status in ['queued', 'in_progress', 'canceling']:
    time.sleep(1)
    run = cliente.beta.threads.runs.retrieve(    
        thread_id = thread.id,
        run_id = run.id
    )

# RESPOSTA COMPLETA
if run.status == 'completed':
    resposta = cliente.beta.threads.messages.list(
        thread_id = thread.id
    )
    print("\n=== RESPOSTA COMPLETA ===\n")
    print(resposta)

    # RESPOSTA FINAL DESTACADA
    print("\n=== RESPOSTA FINAL DESTACADA ===\n")
    print(resposta.data[0].content[0].text.value)
else:
    print('Erro:', run.status)

# LISTA DE PASSOS EXECUTADOS PELA IA
print("\n=== LISTA DE PASSOS EXECUTADOS ===\n")
run_steps = cliente.beta.threads.runs.steps.list(
    thread_id = thread.id,
    run_id = run.id
)
print(run_steps.data[0])

# TIPOS DE PASSOS
print("\n=== LISTA DE TIPOS DE PASSOSPASSOS EXECUTADOS ===\n")
for step in run_steps.data:
    print('=== step: ', step.step_details.type)
# LENDO A TOOL_CALL
    if step.step_details.type == 'tool_calls':
        print("\n=== LEITURA DO TOOLCALLS ===\n") 
        for tool_call in step.step_details.tool_calls:
            print('------')
            print(tool_call.code_interpreter.input)
            print('------')
            print('RESULT')
            print(tool_call.code_interpreter.outputs)