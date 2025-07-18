import openai
from dotenv import load_dotenv, find_dotenv
import json
import requests

_ = load_dotenv(find_dotenv())
cliente = openai.OpenAI()

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
    }
]

funcoes_disponiveis = {
    "obter_clima": obter_clima,
}

cidade = input("Digite o nome da cidade: ")

# mensagens = [ {"role": "user", "content": f"Qual é a temperatura em {cidade} ?"} ]

mensagens = [
    {"role": "user", "content": cidade}
]

resposta = cliente.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=mensagens,
    tools=tools,
    # tool_choice="auto", #--> Força o GPT a usar a(s) ferramenta(s) determinada(s)
)

mensagem_resp = resposta.choices[0].message
tool_calls = mensagem_resp.tool_calls

if tool_calls:
    mensagens.append(mensagem_resp)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = funcoes_disponiveis[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            cidade=function_args.get("local"),
        )

        # ✅ Convertendo a resposta da função para uma string JSON
        mensagens.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_response),  # ✅ Corrigido
        })

    segunda_resposta = cliente.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
    )

    mensagem_resp = segunda_resposta.choices[0].message
    print(mensagem_resp.content)

else: 
    print(resposta.choices[0].message.content)
    # print(resposta.choices[0].message.role)
    # # Não se coloca o "ChatCompletionMessage.content", coloca-se o ".content" direto após o "message" (ou qualquer outro atributo, como o regusal, role, etc...)


####=========================================================
##-------------Apenas a conexão com a API do clima-----------
####=========================================================
# import requests

# _ = load_dotenv(find_dotenv())
# cliente = openai.OpenAI()

# def obter_clima(cidade):
#     API_KEY = "6239db3a9267bd3a128bd6ff38d6247a"  # Substitua pela sua chave de API
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric"
#     resposta = requests.get(url)

#     if resposta.status_code == 200:
#         dados = resposta.json()
#         temperatura = dados["main"]["temp"]
#         unidade = "°C"
#         cidade_retorno = dados["name"]

#         return {"local": cidade_retorno, "temperatura": temperatura, "unidade": unidade}
    
#     return {"erro": "Não foi possível obter os dados da cidade."}

# cidade = input("Digite o nome da cidade: ")
# # dados_clima = obter_clima(cidade)

# if "erro" not in dados_clima:
#     print(f"📍 Cidade: {dados_clima['local']}")
#     print(f"🌡️ Temperatura: {dados_clima['temperatura']} °C")
# else:
#     print("❌ Não foi possível obter os dados da cidade.")