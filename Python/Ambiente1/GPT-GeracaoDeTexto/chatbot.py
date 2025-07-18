import openai
from dotenv import load_dotenv, find_dotenv
import sys  # Adicionado para forçar a saída no terminal

_ = load_dotenv(find_dotenv())
cliente = openai.Client()

def geracao_de_texto(mensagens):
    # Enviando a mensagem pela API com streaming
    resposta = cliente.chat.completions.create(
        messages=mensagens,
        model='gpt-3.5-turbo-0125',
        max_tokens=1000,
        temperature=0,
        stream=True  # Ativando streaming
    )

    print('Assistant: ', end='', flush=True)  # flush=True para forçar a impressão
    resposta_completa = ''

    # Tratando a resposta da mensagem
    for stream_resposta in resposta:
        # Obtendo o texto gerado (se existir)
        texto = stream_resposta.choices[0].delta.content
        if texto is not None:  # Verifica se não é None
            resposta_completa += texto
            print(texto, end='', flush=True)  # Força a impressão imediata
            sys.stdout.flush()  # Garante que a saída é exibida imediatamente

    print('\n')  # Nova linha ao final
    mensagens.append({'role': 'assistant', 'content': resposta_completa})
    return mensagens

if __name__ == '__main__':
    mensagen = []
    while True:
        input_usuario = input('User: ')
        mensagen.append({'role': 'user', 'content': input_usuario})
        resposta = geracao_de_texto(mensagen)