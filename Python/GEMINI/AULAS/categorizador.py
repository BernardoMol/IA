import os  # biblioteca do sistema operacilnal # permite acessar nossas chaves de acesso
import google.generativeai as genai  # biblioteca do google
# importa as variaveis de ambiente que estão no ".env"
from dotenv import load_dotenv
load_dotenv()  # carrega as chaves de acesso

# Pré configurações
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-pro"
lista_de_categorias = "Saldáveis, processados, doces, salgados, naturais"

prompt_sistema = f"""
            Você é um categorizador de alimentos.
            Você deve assumir as categorias presentes na lista abaixo.
            # Lista de Categorias Válidas
            {lista_de_categorias.split(",")}
            # Formato da Saída
            Produto: Nome do Alimento
            Categoria: apresente a categoria do alimento
            # Exemplo de Saída
            Alimento: Banana
            Categoria: Saldáveis, naturais
        """

# Montagem da LLM
genai.configure(api_key=CHAVE_API_GOOGLE)
llm = genai.GenerativeModel(
    model_name=MODELO_ESCOLHIDO,
    system_instruction=prompt_sistema,
)
# Comando e resposta
pergunta = "Banana, pizza, pastel, bolo, mentos, Coca-cola, Suco de polpa, sushi"
resposta = llm.generate_content(pergunta)
print(f"A resposta gerada para a pergunta é: \n{resposta.text}")
