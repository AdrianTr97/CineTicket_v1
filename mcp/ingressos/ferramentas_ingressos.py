from mcp.server.mcpserver import MCPServer
import urllib.request as requisicao

NOME = "ingressos"
mcp = MCPServer(NOME)

URL_INGRESSOS = "http://ingressos:5000/ingressos"

INFO = {
    "nome": NOME,
    "descricao": "servico MCP com informacoes sobre os ingressos vendidos do CineTicket",
    "versao": "1.0"
}

def acessar(url):
    sucesso, conteudo, erro = False, None, None

    try:
        resposta = requisicao.urlopen(url)
        if resposta.code == 200:
            conteudo = resposta.read().decode("utf-8")

            sucesso = True
    except Exception as e:
        erro = str(e)

        print(f"ocorreu um erro acessando '{url}': {erro}")

    return sucesso, conteudo, erro

# nao acentuar os nomes das funcoes, pois o MCP nao aceita acentos
@mcp.tool(name="informacoes", title="informacoes sobre este servico MCP", description="apresenta lista de informacoes basicas sobre este servico MCP")
def get_info():
    return INFO

@mcp.tool(name="ingressos", title="lista de ingressos", description="apresenta lista de ingressos vendidos na bilheteria")
def get_ingressos():
    sucesso, conteudo, erro = acessar(URL_INGRESSOS)

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

@mcp.tool(name="ingressos_por_status", title="encontra ingressos por status", description="procura entre os ingressos aqueles identificados pelo status (ex: CONFIRMADO, CANCELADO, UTILIZADO)")
def get_ingressos_por_status(status):
    sucesso, conteudo, erro = acessar(f"{URL_INGRESSOS}/status/{status}")

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

@mcp.tool(name="quantidade_ingressos_por_status", title="obtem quantidade de ingressos por status", description="retorna a quantidade de ingressos associados a um determinado status")
def get_quantidade_ingressos_por_status(status):
    sucesso, conteudo, erro = acessar(f"{URL_INGRESSOS}/quantidade/{status}")

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host = "0.0.0.0", streamable_http_path="/mcp")