from flask import Flask, jsonify, make_response
import psycopg as dados
from psycopg.rows import dict_row as dicionario
from flask_cors import CORS

servico = Flask("filmes")
CORS(servico)

DESCRICAO = "serviço de gerenciamento do catálogo de filmes do CineTicket"
VERSAO = "1.0"

SERVIDOR_BANCO = "dados"
PORTA_BANCO = 5432
USUARIO_BANCO = "admin"
SENHA_BANCO = "admin"
NOME_BANCO = "cineticket"

def get_conexao_com_bd():
    conexao = dados.connect(
        host = SERVIDOR_BANCO,
        port = PORTA_BANCO,
        user = USUARIO_BANCO,
        password = SENHA_BANCO,
        dbname = NOME_BANCO,
        row_factory = dicionario
    )

    return conexao

@servico.get("/")
def get_info():
    return make_response(jsonify(descricao = DESCRICAO, versao = VERSAO), 200)

@servico.get("/filmes")
def get_filmes():
    filmes = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT f.filme_id, f.titulo, f.sinopse, g.nome AS genero, f.duracao_minutos, f.classificacao
        FROM cineticket.filmes f
        JOIN cineticket.generos g ON g.genero_id = f.genero_id
        WHERE f.ativo = TRUE
        """
    )

    filmes = cursor.fetchall()
    filmes = jsonify(filmes)

    conexao.close()

    return make_response(filmes, 200)

@servico.get("/filmes/id/<int:id_filme>")
def get_filmes_por_id(id_filme):
    filmes = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT f.filme_id, f.titulo, f.sinopse, g.nome AS genero, f.duracao_minutos, f.classificacao
        FROM cineticket.filmes f
        JOIN cineticket.generos g ON g.genero_id = f.genero_id
        WHERE f.filme_id = %s AND f.ativo = TRUE
        """, (id_filme,))
    
    filmes = cursor.fetchall()
    filmes = jsonify(filmes)

    conexao.close()

    return make_response(filmes, 200)

@servico.get("/filmes/titulo/<string:titulo>")
def get_filmes_por_titulo(titulo):
    filmes = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT f.filme_id, f.titulo, f.sinopse, g.nome AS genero, f.duracao_minutos, f.classificacao
        FROM cineticket.filmes f
        JOIN cineticket.generos g ON g.genero_id = f.genero_id
        WHERE lower(f.titulo) LIKE %s AND f.ativo = TRUE
        """, (f"%{titulo.lower()}%",))
    
    filmes = cursor.fetchall()
    filmes = jsonify(filmes)

    conexao.close()

    return make_response(filmes, 200)

if __name__ == "__main__":
    servico.run(host="0.0.0.0", debug=True)