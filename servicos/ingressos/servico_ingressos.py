from flask import Flask, jsonify, make_response
import psycopg as dados
from psycopg.rows import dict_row as dicionario
from flask_cors import CORS

servico = Flask("ingressos")
CORS(servico)

DESCRICAO = "serviço de gerenciamento de ingressos do CineTicket"
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

@servico.get("/ingressos")
def get_ingressos():
    ingressos = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    # Usando a nossa VIEW assim como no exemplo
    cursor.execute(
        """
        SELECT ingresso_id, comprador, titulo, data_horario, sala, poltrona, status_ingresso, preco_pago
        FROM cineticket.vw_detalhes_ingressos
        """
    )

    ingressos = cursor.fetchall()
    ingressos = jsonify(ingressos)

    conexao.close()

    return make_response(ingressos, 200)

@servico.get("/ingressos/status/<string:status>")
def get_ingressos_por_status(status):
    ingressos = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT ingresso_id, comprador, titulo, data_horario, sala, poltrona, status_ingresso, preco_pago
        FROM cineticket.vw_detalhes_ingressos 
        WHERE status_ingresso = %s
        """, (status.upper(),))
    
    ingressos = cursor.fetchall()
    ingressos = jsonify(ingressos)

    conexao.close()

    return make_response(ingressos, 200)

@servico.get("/ingressos/quantidade/<string:status>")
def get_quantidade_ingressos_por_status(status):
    ingressos = 0

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT count(*) as quantidade
        FROM cineticket.vw_detalhes_ingressos 
        WHERE status_ingresso = %s
        """, (status.upper(),))
    
    ingressos = cursor.fetchone() # Usando fetchone
    ingressos = jsonify(ingressos)

    conexao.close()

    return make_response(ingressos, 200)

if __name__ == "__main__":
    servico.run(host="0.0.0.0", debug=True)