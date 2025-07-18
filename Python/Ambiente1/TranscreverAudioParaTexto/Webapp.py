# PROJETO Asimov Transcripts – Transcrevendo áudios com a API do ChatGPT
# python Webapp.py
# streamlit run Webapp.py

# pip install audioop-lts --> audioop has been removed in python version 3.13
# =============================================

import openai
import streamlit as st # MUUITO absurdo, ele roda a aplicação no navegador
from streamlit_webrtc import WebRtcMode, webrtc_streamer
# from moviepy.editor import VideoFileClip -->> ESTRUTURA DESATUALIZADA
from moviepy.video.io.VideoFileClip import VideoFileClip
from pathlib import Path
import queue
import time
import pydub

# Pra quem está fazendo em 12/2024 ou adiante, o Streamlit possui um componente chamado 'audio_input', (https://docs.streamlit.io/develop/api-reference/widgets/st.audio_input). 

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
    # DEFASADO, A BIBLIOTECA DA STREAMLIT JA TEM UMA FUNÇÃO QUE CAPTURA O AUDIO DO MICROFONE E O TRANSCREVE
    # webrtc_ctx = webrtc_streamer(
    #     key = "microfone",
    #     mode = WebRtcMode.SENDONLY,
    #     audio_receiver_size = 1024,
    #     # rtc_configuration={'iceServers': get_ice_servers()}, # para usar o ice_servers
    #     media_stream_constraints={'video': False, 'audio': True} 
    # )

    # if not webrtc_ctx.state.playing: 
    #     st.write("Não está capturando áudio!")
    #     return
    
    # container = st.empty()
    # container.markdown("Começe a falar...")
    # chunk_audio = pydub.AudioSegment.empty() #é o que usamos para transcrever os bites em texto
    
    # while True:
    #     if webrtc_ctx.audio_receiver:
    #         try:
    #             audio_data = webrtc_ctx.audio_receiver.get_frames(timeout=2) # tempo atentando pegar audio
    #             st.write(f"Capturando {len(audio_data)} quadros de áudio...")  # Depuração
    #         except queue.Empty:
    #             st.write("Sem áudio recebido, tentando novamente...")  # Depuração
    #             time.sleep(0.1)
    #             continue
    #         for frame in audio_data:
    #             sound = pydub.AudioSegment(
    #                 data = frame.to_ndarray().tobytes(),
    #                 sample_width = frame.format.bytes,
    #                 frame_rate = frame.sample_rate,
    #                 channels=len(frame.layout.channels)
    #             )
    #             chunk_audio += sound

    #         if len(chunk_audio) > 0:
    #             container.markdown("Gravando...")
    #             chunk_audio.export(ARQUIVO_MIC_TEMP, format='mp3')
    #             transcricao_de_arquivos(ARQUIVO_MIC_TEMP, prompt_input=None)
    #             chunk_audio = pydub.AudioSegment.empty()
    #     else:
    #         break
    


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
    tab_mic, tab_video, tab_audio = st.tabs(["Microfone", "Vídeo", "Audio .mp3"])

    with tab_mic:
        transcreve_tab_mic()    
    with tab_video:
        transcreve_tab_video()
    with tab_audio:
        transcreve_tab_audio()

if __name__ == '__main__':
    main()