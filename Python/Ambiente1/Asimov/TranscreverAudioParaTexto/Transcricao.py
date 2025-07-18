# PROJETO Asimov Transcripts – Transcrevendo áudios com a API do ChatGPT
# python Transcricao.py

# =============================================
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

cliente = openai.Client()
# ============================================


arquivo_audio = open('media/original.mp3', mode='rb')
prompt = 'Olá, seja bem-vindo ao Asimov Transcripts. Por favor, transcreva o áudio para texto. Meu nome é Rodrigo Soares Tadewald e ensino Python'
# A idéia do prompt é colocar as palavras mais "difíceis" e incomuns para o modelo entender no início do texto

transcricao = cliente.audio.transcriptions.create(
    model = 'whisper-1',
    language = "pt",
    response_format='text',
    file = arquivo_audio,
    prompt = prompt
)

print(transcricao)


transcricao_LEGENDA = cliente.audio.transcriptions.create(
    model = 'whisper-1',
    language = "pt",
    response_format='srt',
    file = arquivo_audio,
    prompt = prompt
)

print(transcricao_LEGENDA)