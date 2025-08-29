import os  # biblioteca do sistema operacilnal # permite acessar nossas chaves de acesso
import google.generativeai as genai  # biblioteca do google
# importa as variaveis de ambiente que estão no ".env"
from dotenv import load_dotenv
load_dotenv()  # carrega as chaves de acesso

# Pré configurações
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-pro"
prompt_sistema = "Liste os nomes dos mapas mais frequentados pelos jogadores"


configuracao_modelo = {
    # "temperature": controla a criatividade/aleatoriedade da resposta.
    # Valores baixos (ex: 0.1) => respostas mais determinísticas, seguras.
    # Valores altos (ex: 2.0) => respostas mais criativas, com chance maior de "alucinação".
    "temperature": 2.0,

    # "top_p": chamado de "nucleus sampling".
    # O modelo só considera as palavras que, somadas, correspondem à fração 'p' da probabilidade.
    # Ex: 0.9 = considera apenas tokens que juntos somam 90% da probabilidade total.
    # Isso limita a aleatoriedade e controla diversidade da resposta.
    "top_p": 0.9,

    # "top_k": número máximo de tokens candidatos que o modelo avalia por vez.
    # Ex: 64 = só olha os 64 tokens mais prováveis.
    # Valores menores => respostas mais focadas; valores maiores => mais variedade.
    "top_k": 64,

    # "max_output_tokens": limite de tokens (palavras + pedaços de palavras) na saída.
    # Isso evita respostas muito longas ou consumir mais créditos do que o necessário.
    # Ex: 8192 tokens é suficiente para textos bem extensos.
    "max_output_tokens": 8192,

    # "response_mime_type": formato do conteúdo de resposta.
    # Pode ser "text/plain", "text/html", "application/json", etc.
    # Aqui está configurado para texto puro.
    "response_mime_type": "text/plain"
}

# Montagem da LLM
genai.configure(api_key=CHAVE_API_GOOGLE)
llm = genai.GenerativeModel(
    model_name=MODELO_ESCOLHIDO,
    system_instruction=prompt_sistema,
    generation_config=configuracao_modelo
)
# Comando e resposta
pergunta = "Liste três mapas do Tibia"
resposta = llm.generate_content(pergunta)
print(f"A respsota gerada para a pergunta é: {resposta.text}")
