from flask import Flask, jsonify, make_response
import psycopg as dados
from psycopg.rows import dict_row as dicionario
from flask_cors import CORS

servico = Flask("sessoes")
CORS(servico)

DESCRICAO = "serviço de gerenciamento de sessões do CineTicket"
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

@servico.get("/sessoes")
def get_sessoes():
    sessoes = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT sessao_id, titulo, genero, sala, tipo_sala, data_horario, preco_padrao, status, assentos_livres
        FROM cineticket.vw_resumo_sessoes
        """
    )

    sessoes = cursor.fetchall()
    sessoes = jsonify(sessoes)

    conexao.close()

    return make_response(sessoes, 200)

@servico.get("/sessoes/id/<int:id_sessao>")
def get_sessoes_por_id(id_sessao):
    sessoes = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT sessao_id, titulo, genero, sala, tipo_sala, data_horario, preco_padrao, status, assentos_livres
        FROM cineticket.vw_resumo_sessoes
        WHERE sessao_id = %s
        """, (id_sessao,))
    
    sessoes = cursor.fetchall()
    sessoes = jsonify(sessoes)

    conexao.close()

    return make_response(sessoes, 200)

@servico.get("/sessoes/titulo_filme/<string:titulo>")
def get_sessoes_por_titulo(titulo):
    sessoes = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT sessao_id, titulo, genero, sala, tipo_sala, data_horario, preco_padrao, status, assentos_livres
        FROM cineticket.vw_resumo_sessoes
        WHERE lower(titulo) LIKE %s
        """, (f"%{titulo.lower()}%",))
    
    sessoes = cursor.fetchall()
    sessoes = jsonify(sessoes)

    conexao.close()

    return make_response(sessoes, 200)

if __name__ == "__main__":
    servico.run(host="0.0.0.0", debug=True)