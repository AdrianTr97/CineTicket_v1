from mcp.server.mcpserver import MCPServer
import urllib.request as requisicao
import urllib.parse

NOME = "sessoes"
mcp = MCPServer(NOME)

URL_SESSOES = "http://sessoes:5000/sessoes"

INFO = {
    "nome": NOME,
    "descricao": "servico MCP com informacoes sobre a disponibilidade e horarios das sessoes do CineTicket",
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
@mcp.tool(name="informacoes", title="informacoes sobre este servico MCP", description="apresenta lista de informacoes basicas sobre este servico MCP do CineTicket")
def get_info():
    return INFO

@mcp.tool(name="sessoes", title="lista de sessoes", description="apresenta lista de sessoes com seus horarios, filmes, salas e assentos livres")
def get_sessoes():
    sucesso, conteudo, erro = acessar(URL_SESSOES)

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

@mcp.tool(name="sessoes_por_id", title="encontra informacoes de sessoes por identificador ou id da sessao", description="procura entre as informacoes de sessoes aquelas identificadas pelo id da sessao")
def get_sessoes_por_id(id_sessao):
    sucesso, conteudo, erro = acessar(f"{URL_SESSOES}/id/{id_sessao}")

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

@mcp.tool(name="sessoes_por_titulo_filme", title="encontra informacoes de sessoes pelo titulo do filme", description="procura entre as informacoes de sessoes aquelas identificadas pelo titulo do filme associado")
def get_sessoes_por_titulo(titulo):
    # Formata o titulo para a URL não quebrar caso a IA envie nomes com espaços
    titulo_url = urllib.parse.quote(titulo)
    sucesso, conteudo, erro = acessar(f"{URL_SESSOES}/titulo_filme/{titulo_url}")

    if sucesso:
        return conteudo
    else:
        return f"ocorreu um erro: {erro}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host = "0.0.0.0", streamable_http_path="/mcp")