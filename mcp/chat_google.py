import asyncio
import json
import os
from contextlib import AsyncExitStack

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from google import genai

MODELO = "gemini-3.5-flash-lite"
PROMPT = """

Você é um assistente virtual de bilheteria de uma rede de cinemas chamada CineTicket. O seu nome é CineTicketBot.

Quando o usuário fizer uma saudação ou iniciar uma conversa contigo, você deve se identificar pelo seu nome e informar que você não é uma pessoa real, mas é um assistente virtual de atendimento do cinema.

Quando o usuário solicitar informações sobre filmes em cartaz, horários e vagas nas sessões, ou situação de ingressos vendidos, você deve utilizar as ferramentas MCP disponíveis para obter tais informações. Também é necessário que você identique quando mais de uma ferramenta é necessária (por exemplo, buscar a sinopse de um filme e depois ver as sessões dele). Você deve obedecer estas regras:

- se o usuário perguntar sobre o catálogo, sinopses, duração ou gêneros de filmes, você deve utilizar as ferramentas de filmes;
- se o usuário perguntar sobre os horários, salas, poltronas livres ou sessões disponíveis, você deve utilizar as ferramentas de sessoes;
- se o usuário perguntar sobre as compras de ingressos, bilhetes vendidos, métodos de pagamento ou status da compra (confirmado/cancelado), você deve utilizar as ferramentas de ingressos.
- se o usuário fizer uma pergunta que não esteja relacionada a filmes, sessões e ingressos de cinema, você deve dizer que não está capacitado para responder e deve falar para o usuário entrar em contato com os gerentes do cinema.

"""

load_dotenv()

SERVICOS_MCP = {
    "filmes":      "http://localhost:8001/mcp",
    "sessoes":     "http://localhost:8002/mcp",
    "ingressos":   "http://localhost:8003/mcp",
}

async def iniciar():
    iniciado, stack, cliente_IA = False, AsyncExitStack(), None

    try:
        # ATENÇÃO: Verifica a chave do GOOGLE no seu arquivo .env
        cliente_IA = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

        iniciado = True
    except Exception as e:
        print(f"⚠️ erro iniciando conexão com IA: {e}")

    return iniciado, stack, cliente_IA

async def conectar_servicos(stack):
    servicos = {}

    for nome_servico, url in SERVICOS_MCP.items():
        stream_leitura, stream_escrita = await stack.enter_async_context(streamable_http_client(url))

        conexao = await stack.enter_async_context(
            ClientSession(stream_leitura, stream_escrita)
        )
        await conexao.initialize()

        servicos[nome_servico] = conexao
        print(f"conectado ao serviço, '{nome_servico}'")

    return servicos

async def get_ferramentas(servicos):
    ferramentas = {}

    for nome_servico, conexao in servicos.items():
        resultado = await conexao.list_tools()

        for ferramenta in resultado.tools:
            ferramentas[ferramenta.name] = {
                "servico": {
                    "nome": nome_servico,
                    "conexao": conexao
                },
                "ferramenta": {
                    "type": "function",
                    "name": ferramenta.name,
                    "description": ferramenta.description,
                    "parameters": ferramenta.input_schema,
                }
            }

    return ferramentas

async def executar_ferramenta(ferramentas, ferramenta_desejada, argumentos):
    ferramenta = ferramentas[ferramenta_desejada]

    servico = ferramenta['servico']
    print(f"🤖 executando a ferramenta, '{ferramenta_desejada}', do serviço, '{servico['nome']}'")
    
    conexao = servico['conexao']
    resultado = await conexao.call_tool(ferramenta_desejada, arguments = argumentos)

    return extrair_texto(resultado)

def extrair_texto(resultado):
    if resultado.structured_content:
        return json.dumps(resultado.structured_content, ensure_ascii=False)

    conteudo = []
    for c in resultado.content:
        if hasattr(c, "text"):
            conteudo.append(c.text)
        else:
            conteudo.append(str(c))

    return "\n".join(conteudo)

async def chat(cliente_IA, ferramentas):
    mensagens = [
        {
            "type": "user_input",
            "content": [{ "type": "text", "text": PROMPT }]
        }
    ]

    while True:
        mensagem = input("\n👤 ")

        # para caso dar uma entrada vazia, o chat ignorará, caso apertar Enter sem querer, o terminal apenas mostrará um novo 👤  e ficará aguardando pacientemente você digitar
        if not mensagem.strip():
            continue

        mensagem = mensagem.lower()

        if mensagem in [ "sair", "/s" ]:
            break

        mensagens.append({
            "type": "user_input",
            "content": [{ "type": "text", "text": mensagem }]
        })

        while True:
            resposta = await cliente_IA.aio.interactions.create(
                model = MODELO,
                input = mensagens,
                tools = [f["ferramenta"] for f in ferramentas.values()]
            )

            execucoes = [item for item in resposta.steps if item.type == "function_call"]
            if not execucoes:
                print(f"🤖 {resposta.output_text}")

                break

            mensagens.extend(resposta.steps)
            for execucao in execucoes:
                argumentos = execucao.arguments
                resultado = await executar_ferramenta(ferramentas, execucao.name, argumentos)

                mensagens.append({
                    "type": "function_result",
                    "name": execucao.name,
                    "call_id": execucao.id,
                    "result": [{ "type": "text", "text": resultado}]
                })

async def finalizar(stack):
    await stack.aclose()

async def executar():
    iniciado, stack, cliente_IA = await iniciar()
    if iniciado:
        try:
            servicos = await conectar_servicos(stack)
            ferramentas = await get_ferramentas(servicos)

            await chat(cliente_IA, ferramentas)
        finally:
            await finalizar(stack)

if __name__ == "__main__":
    asyncio.run(executar())