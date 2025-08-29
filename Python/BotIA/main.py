import os  # biblioteca do sistema operacilnal # permite acessar nossas chaves de acesso
import google.generativeai as genai  # biblioteca do google
# importa as variaveis de ambiente que estão no ".env"
from dotenv import load_dotenv
load_dotenv()  # carrega as chaves de acesso

# Pré configurações
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-pro"
prompt_sistema = "Liste os nomes dos mapas mais frequentados pelos jogadores"
# Montagem da LLM
genai.configure(api_key=CHAVE_API_GOOGLE)
llm = genai.GenerativeModel(
    model_name=MODELO_ESCOLHIDO,
    system_instruction=prompt_sistema
)
# Comando e resposta
pergunta = "Liste três mapas do Tibia"
resposta = llm.generate_content(pergunta)
print(f"A respsota gerada para a pergunta é: {resposta.text}")
