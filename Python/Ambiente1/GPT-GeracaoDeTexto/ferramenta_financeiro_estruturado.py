import openai
from dotenv import load_dotenv, find_dotenv
import json
import requests
import yfinance as yf

_ = load_dotenv(find_dotenv())
cliente = openai.OpenAI()


def obter_dados_ativos(ticker, period="1d"): # Se o usuário nao me falar o dia, 

    ativo = yf.Ticker(ticker)
    dados = ativo.history(period)
    info = ativo.info
    
    resultado = { 
        "nome": info.get("shortName", "N/A"),
        "preco_atual": dados["Close"].iloc[-1] if not dados.empty else "N/A",
        "variacao": info.get("regularMarketChangePercent", "N/A"),
        "volume": info.get("volume", "N/A"),
        "setor": info.get("sector", "N/A"),
        "capitalizacao_mercado": info.get("marketCap", "N/A"),
    }
    
    return resultado

def obter_clima(cidade):
    API_KEY = "6239db3a9267bd3a128bd6ff38d6247a"  # Substitua pela sua chave de API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        temperatura = dados["main"]["temp"]
        unidade = "°C"
        cidade_retorno = dados["name"]

        return {"cidade": cidade_retorno, "temperatura": temperatura, "unidade": unidade}
    
    return {"erro": "Não foi possível obter os dados da cidade."}

def chamando_gpt(mensagens):
    # Defino as ferramentas disponíveis para o GTPT
    tools = [
        {
            "type": "function",
            "function": {
                "name": "obter_clima",
                "description": "Obtém a temperatura atual em uma dada cidade",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cidade": {  
                            "type": "string",
                            "description": "O nome da cidade. Ex: São Paulo",
                        },
                    },
                    "required": ["cidade"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "obter_dados_ativos",
                "description": "Obtém informações de ativos ao entrar com o nome da empresa ou com sua sigla (exemplo: Tesla = TSLA, Banco do Brasil = BSA3)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {  
                            "type": "string",
                            "description": "O nome da empresa ou sua sigla. Exemplo: Tesla = TSLA, Banco do Brasil = BSA3",
                        },
                    },
                    "required": ["ticker"],
                },
            },
        },
    ]
    # Faço a pergunta ao GPT
    resposta = cliente.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=mensagens,
            tools=tools,  # Passa as ferramentas disponíveis
        )
    # Verifico quais ferramentas o GPT pediu para usar (se é que pediu alguma)
    mensagem_resp = resposta.choices[0].message
    tool_calls = mensagem_resp.tool_calls  # Obtém as ferramentas selecionadas pelo GPT
    # Verifico se realmente alguma ferramenta foi solicitada pelo GPT
    if tool_calls:
        mensagens.append(mensagem_resp)
        resposta = chamando_ferramentas(mensagens,tool_calls)
        return resposta
    else:
        # Se o GPT nao pediu para usar ferramenta nenhuma, só devolve o que ele respondeu
        return resposta
    
def chamando_ferramentas(mensagens,tool_calls):
    
    # Falo quais funções o GPT tem para usar
    funcoes_disponiveis = {
        "obter_clima": obter_clima,
        "obter_dados_ativos": obter_dados_ativos,
    }
    # Percorro todas as ferramentas/funções que o GPT pediu
    for tool_call in tool_calls:
        # Nome da função a ser chamada
        function_name = tool_call.function.name
        function_to_call = funcoes_disponiveis[function_name]

        if function_to_call:  # Se a função existir no dicionário
            function_args = json.loads(tool_call.function.arguments)  # Extrai os argumentos
            function_response = function_to_call(**function_args)  # Chama a função dinamicamente

        # Convertendo a resposta da função para uma string JSON
        mensagens.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_response),  # Corrigido
        })

    # Chama novamente o GPT para gerar uma resposta final com base nas chamadas de ferramenta
    segunda_resposta = cliente.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
    )

    # Exibe a resposta final do GPT
    mensagem_resp = segunda_resposta.choices[0].message
    return mensagem_resp.content
 
if __name__ == "__main__":
    # Funções disponíveis para execução
    while True:
        mensagem_do_usuario = input("Digite sua pergunta: ")
        if mensagem_do_usuario.lower() == 'sair':
            break
        else:
            # Preparando a primeira mensagem para o GPT
            mensagem = [{"role": "user", "content": mensagem_do_usuario}]
            resposta_pergunta = chamando_gpt(mensagem)
            
            # Certificando-se de imprimir corretamente a resposta como string
            print(resposta_pergunta if isinstance(resposta_pergunta, str) else resposta_pergunta.choices[0].message.content)