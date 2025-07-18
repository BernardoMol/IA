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

        return {"local": cidade_retorno, "temperatura": temperatura, "unidade": unidade}
    
    return {"erro": "Não foi possível obter os dados da cidade."}

# Ferramentas disponíveis
tools = [
    {
        "type": "function",
        "function": {
            "name": "obter_clima",
            "description": "Obtém a temperatura atual em uma dada cidade",
            "parameters": {
                "type": "object",
                "properties": {
                    "local": {  
                        "type": "string",
                        "description": "O nome da cidade. Ex: São Paulo",
                    },
                },
                "required": ["local"],
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

funcoes_disponiveis = {
    "obter_clima": obter_clima,
    "obter_dados_ativos": obter_dados_ativos,
}

if __name__ == "__main__":
    # Funções disponíveis para execução


    while True:

        mensagem_do_usuario = input("Digite sua pergunta: ")

        # Preparando a primeira mensagem para o GPT
        mensagens = [
            {"role": "user", "content": mensagem_do_usuario}
        ]

        # Solicita ao GPT para escolher as ferramentas com base na pergunta do usuário
        resposta = cliente.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=mensagens,
            tools=tools,  # Passa as ferramentas disponíveis
        )

        mensagem_resp = resposta.choices[0].message
        tool_calls = mensagem_resp.tool_calls  # Obtém as ferramentas selecionadas pelo GPT

        if tool_calls:
            mensagens.append(mensagem_resp)
            for tool_call in tool_calls:
                # Nome da função a ser chamada
                function_name = tool_call.function.name
                function_to_call = funcoes_disponiveis[function_name]

                # Argumentos para a função
                function_args = json.loads(tool_call.function.arguments)

                # Verifica se a função precisa de dados específicos e chama a função correta
                if function_name == "obter_clima":
                    cidade = function_args.get("local")
                    function_response = function_to_call(cidade)
                elif function_name == "obter_dados_ativos":
                    ticker = function_args.get("ticker")
                    function_response = function_to_call(ticker)

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
            print(mensagem_resp.content)

        else: 
            # Caso o GPT não selecione nenhuma ferramenta, apenas exibe a resposta do GPT
            print(resposta.choices[0].message.content)


####=========================================================
##-------------Apenas a conexão com a API de FINANCE---------
####=========================================================


# import yfinance as yf

# def obter_dados_ativos(ticker):

#     ativo = yf.Ticker(ticker)
#     dados = ativo.history(period="1d")
#     info = ativo.info
    
#     resultado = { # Interpolação dos dados de acordo com o Formato dos dados devolvidos pela API
#         "nome": info.get("shortName", "N/A"),
#         "preco_atual": dados["Close"].iloc[-1] if not dados.empty else "N/A",
#         "variacao": info.get("regularMarketChangePercent", "N/A"),
#         "volume": info.get("volume", "N/A"),
#         "setor": info.get("sector", "N/A"),
#         "capitalizacao_mercado": info.get("marketCap", "N/A"),
#     }
    
#     return resultado

# if __name__ == "__main__":
#     ticker = input("Digite o código do ativo (ex: TSLA, PETR4.SA): ")
#     dados_ativo = obter_dados_ativos(ticker)
    
#     print("\nDados do ativo:")
#     for chave, valor in dados_ativo.items():
#         print(f"{chave}: {valor}")