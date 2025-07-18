# PROJETO Asimov Transcripts – Transcrevendo áudios com a API do ChatGPT
# python Webapp.py
# streamlit run Webapp.py
# tem que instalar o pytube
# pip install audioop-lts --> audioop has been removed in python version 3.13
# =============================================
import io
import openai
import streamlit as st # MUUITO absurdo, ele roda a aplicação no navegador
from streamlit_webrtc import WebRtcMode, webrtc_streamer
# from moviepy.editor import VideoFileClip -->> ESTRUTURA DESATUALIZADA
from moviepy.video.io.VideoFileClip import VideoFileClip
from pathlib import Path
import queue
import time
import pydub
from pytube import YouTube

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

cliente = openai.Client()
# ============================================


PASTA_TEMP = Path(__file__).parent / 'temp'
PASTA_TEMP.mkdir(exist_ok=True)
ARQUIVO_AUDIO_TEMP = PASTA_TEMP / 'temp_audio.mp3'
ARQUIVO_VIDEO_TEMP = PASTA_TEMP / 'temp_video.mp4'  
ARQUIVO_MIC_TEMP = PASTA_TEMP / 'temp_mic.mp3'

# ISSO SERVE PARA PODER USAR O MICROFONE/CAMERA DE FORMA GENERICA
# @st.cache_data
# def get_ice_servers():
#     return [{'urls': ['stun:stun.l.google.com:19302']}]
# ================================================================

def transcreve_tab_mic():

    microfoneAudio = st.audio_input('Grave seu Áudio 🎤',key='mic_input')
    if not microfoneAudio is None:
        transcript = cliente.audio.transcriptions.create(model='whisper-1', language='pt', response_format='text', file=microfoneAudio)
        st.write(transcript)


def transcreve_tab_video():
    st.markdown("Insira o arquivo de video e clique para transcrever")
    prompt_input = st.text_input("(OPICIONAL) Digite seu prompt", key="prompt_video")
    arquivo_video = st.file_uploader("Selecione um arquivo .mp4", type = ['mp4'])
    # st.write(str(ARQUIVO_VIDEO_TEMP)) # SO MOSTRA O CAMINHO DO ARQUIVO
    # st.write(str(ARQUIVO_VIDEO_TEMP)) # SO MOSTRA O CAMINHO DO ARQUIVO
    if not arquivo_video is None:
        with open(ARQUIVO_VIDEO_TEMP, mode='wb') as video_f:
            video_f.write(arquivo_video.read())
        moviepy_video = VideoFileClip(str(ARQUIVO_VIDEO_TEMP))
        moviepy_video.audio.write_audiofile(str(ARQUIVO_AUDIO_TEMP))
        with open(ARQUIVO_AUDIO_TEMP, mode='rb') as audio_f:
            transcricao_de_arquivos(audio_f, prompt_input)  


def transcreve_tab_audio():
    st.markdown("Insira o arquivo de audio e clique para transcrever")
    prompt_input = st.text_input("(OPICIONAL) Digite seu prompt", key="prompt_audio")
    arquivo_audio = st.file_uploader("Selecione um arquivo .mp3", type = ['mp3'])
    if not arquivo_audio is None:
        transcricao_de_arquivos(arquivo_audio, prompt_input)

def transcreve_tab_youtube(): ##legal...n da pra fazer......quebra termos de uso......
    st.markdown("Insira a URL do vídeo do YouTube e clique para transcrever")
    prompt_input = st.text_input("(OPICIONAL) Digite seu prompt", key="prompt_youtube")
    url_video = st.text_input("Digite a URL do vídeo do YouTube", key="url_video")

    if url_video:
        try:
            st.write("Baixando áudio do vídeo...")
            yt = YouTube(url_video)
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            
            # Carregar o áudio diretamente em memória usando BytesIO
            audio_data = io.BytesIO()
            audio_stream.stream_to_buffer(audio_data)
            audio_data.seek(0)  # Voltar ao início do buffer
            
            # Enviar o áudio para a transcrição
            transcricao_de_arquivos(audio_data, prompt_input)
            st.write(f"Transcrição completa para o vídeo: {url_video}")
        except Exception as e:
            st.error(f"Erro ao processar o vídeo: {str(e)}")


def transcricao_de_arquivos(arquivo, prompt):
    transcricao = cliente.audio.transcriptions.create(
        model = 'whisper-1',
        language = "pt",
        response_format='text',
        file = arquivo,
        prompt = prompt)
    st.write(transcricao) 


def main():
    st.header('Transcrever áudio para texto 🎙️', divider = True)
    st.markdown("Transcreva audios de microfone, videos ou arquivos .mp3")
    tab_mic, tab_video, tab_audio, tab_youtube = st.tabs(["Microfone", "Vídeo", "Audio.mp3", "Youtube"])

    with tab_mic:
        transcreve_tab_mic()    
    with tab_video:
        transcreve_tab_video()
    with tab_audio:
        transcreve_tab_audio()
    with tab_youtube:
        transcreve_tab_youtube()

if __name__ == '__main__':
    main()