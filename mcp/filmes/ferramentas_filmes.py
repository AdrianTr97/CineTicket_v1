from mcp.server.mcpserver import MCPServer
import urllib.request as requisicao
import urllib.parse

NOME = "filmes"
mcp = MCPServer(NOME)

URL_FILMES = "http://filmes:5000/filmes"

INFO = {
    "nome": NOME,
    "descricao": "servico MCP do catalogo de filmes em cartaz do CineTicket"
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

        print(f"ocorreu um erro acessando: {url}, erro: {erro}")

    return sucesso, conteudo, erro

@mcp.tool(name = "informacoes", title = "informacoes sobre o servico MCP de filmes", description = "apresenta informacoes basicas sobre o servico MCP do CineTicket")
def get_info():
    return INFO

@mcp.tool(name = "catalogo_filmes", title = "resumo dos filmes em cartaz", description = "apresenta uma lista com resumos e dados dos filmes em cartaz no CineTicket")
def get_filmes():
    sucesso, conteudo, erro = acessar(URL_FILMES)

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

@mcp.tool(name = "filmes_por_id", title = "encontra filmes pelo seu id", description = "procura por um filme no catalogo identificado pelo seu id")
def get_filmes_por_id(id_filme):
    sucesso, conteudo, erro = acessar(f"{URL_FILMES}/id/{id_filme}")

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

@mcp.tool(name = "filmes_por_titulo", title = "encontra filmes pelo seu titulo", description = "procura por filmes no catalogo identificados pelo seu titulo")
def get_filmes_por_titulo(titulo):
    # Formata o titulo para a URL não quebrar caso a IA envie nomes com espaços
    titulo_url = urllib.parse.quote(titulo)
    sucesso, conteudo, erro = acessar(f"{URL_FILMES}/titulo/{titulo_url}")

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

if __name__ == "__main__":
    mcp.run(transport = "streamable-http", streamable_http_path = "/mcp", host = "0.0.0.0")
