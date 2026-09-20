-- CineTicket - Fictional Cinema Database
-- PostgreSQL
-- All data is fictitious and intended for classroom use.

DROP SCHEMA IF EXISTS cineticket CASCADE;
CREATE SCHEMA cineticket;
SET search_path TO cineticket;

CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(25),
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE,
    fidelidade_pontos INT DEFAULT 0
);

CREATE TABLE salas (
    sala_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    capacidade INT NOT NULL CHECK (capacidade > 0),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('STANDARD', 'VIP', 'IMAX', '3D'))
);

CREATE TABLE generos (
    genero_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE filmes (
    filme_id SERIAL PRIMARY KEY,
    genero_id INT NOT NULL REFERENCES generos(genero_id),
    titulo VARCHAR(150) NOT NULL,
    sinopse VARCHAR(500) NOT NULL,
    duracao_minutos INT NOT NULL CHECK (duracao_minutos > 0),
    classificacao VARCHAR(10) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE sessoes (
    sessao_id SERIAL PRIMARY KEY,
    filme_id INT NOT NULL REFERENCES filmes(filme_id),
    sala_id INT NOT NULL REFERENCES salas(sala_id),
    data_horario TIMESTAMP NOT NULL,
    preco_padrao NUMERIC(10,2) NOT NULL CHECK (preco_padrao > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('DISPONIVEL','LOTADA','CANCELADA','ENCERRADA'))
);

CREATE TABLE ingressos (
    ingresso_id SERIAL PRIMARY KEY,
    sessao_id INT NOT NULL REFERENCES sessoes(sessao_id) ON DELETE CASCADE,
    cliente_id INT REFERENCES clientes(cliente_id),
    poltrona VARCHAR(10) NOT NULL,
    tipo_ingresso VARCHAR(20) NOT NULL CHECK (tipo_ingresso IN ('INTEIRA', 'MEIA', 'CORTESIA')),
    preco_pago NUMERIC(10,2) NOT NULL CHECK (preco_pago >= 0),
    data_compra TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('CONFIRMADO','CANCELADO','UTILIZADO')),
    UNIQUE(sessao_id, poltrona)
);

CREATE TABLE pagamentos (
    pagamento_id SERIAL PRIMARY KEY,
    ingresso_id INT NOT NULL UNIQUE REFERENCES ingressos(ingresso_id),
    metodo VARCHAR(30) NOT NULL CHECK (metodo IN ('PIX','CARTAO_CREDITO','CARTAO_DEBITO','DINHEIRO')),
    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('APROVADO','RECUSADO','ESTORNADO'))
);

-- ==========================================
-- INSERÇÃO DE DADOS
-- ==========================================

-- Generos
INSERT INTO generos (nome) VALUES ('Ação'), ('Ficção Científica'), ('Drama'), ('Comédia'), ('Animação'), ('Terror'), ('Aventura');

-- Salas (Ajustado para 4 salas)
INSERT INTO salas (nome, capacidade, tipo) VALUES 
('Sala 1', 250, 'IMAX'), ('Sala 2', 120, 'VIP'), ('Sala 3', 180, '3D'), ('Sala 4', 200, 'STANDARD');

-- Clientes (Quadruplicado - 40 clientes)
INSERT INTO clientes (nome, email, telefone, fidelidade_pontos) VALUES 
('Daniela Almeida', 'daniela@example.com', '4495614226', 150),
('Helena Teixeira', 'helena@example.com', '4491445199', 30),
('Bruno Silva', 'bruno@example.com', '4499996414', 500),
('Carlos Vieira', 'carlos@example.com', '4493109911', 0),
('Ana Mendes', 'ana@example.com', '4496438436', 120),
('Igor Ferreira', 'igor@example.com', '4496855396', 50),
('Sabrina Nogueira', 'sabrina@example.com', '4491852264', 300),
('Rafael Barbosa', 'rafael@example.com', '4492651177', 10),
('Vanessa Costa', 'vanessa@example.com', '4493351868', 80),
('Thiago Dias', 'thiago@example.com', '4496007072', 250),
('Lucas Martins', 'lucas.m@example.com', '4498112345', 40),
('Mariana Rocha', 'mariana.r@example.com', '4498223456', 210),
('Felipe Carvalho', 'felipe.c@example.com', '4498334567', 0),
('Juliana Pereira', 'juliana.p@example.com', '4498445678', 320),
('Gabriel Souza', 'gabriel.s@example.com', '4498556789', 15),
('Aline Castro', 'aline.c@example.com', '4498667890', 95),
('Rodrigo Lima', 'rodrigo.l@example.com', '4498778901', 0),
('Fernanda Gomes', 'fernanda.g@example.com', '4498889012', 410),
('Matheus Santos', 'matheus.s@example.com', '4498990123', 60),
('Camila Oliveira', 'camila.o@example.com', '4499101234', 180),
('Eduardo Araujo', 'eduardo.a@example.com', '4499212345', 25),
('Patricia Ribeiro', 'patricia.r@example.com', '4499323456', 75),
('Leonardo Fernandes', 'leonardo.f@example.com', '4499434567', 0),
('Larissa Moura', 'larissa.m@example.com', '4499545678', 130),
('Gustavo Azevedo', 'gustavo.a@example.com', '4499656789', 450),
('Beatriz Cardoso', 'beatriz.c@example.com', '4499767890', 20),
('Diego Monteiro', 'diego.m@example.com', '4499878901', 55),
('Amanda Freitas', 'amanda.f@example.com', '4499989012', 290),
('Vitor Correia', 'vitor.c@example.com', '4498109123', 10),
('Natalia Barros', 'natalia.b@example.com', '4498210234', 360),
('Marcelo Diniz', 'marcelo.d@example.com', '4498321345', 85),
('Letícia Neves', 'leticia.n@example.com', '4498432456', 115),
('Ricardo Machado', 'ricardo.m@example.com', '4498543567', 40),
('Carolina Borges', 'carolina.b@example.com', '4498654678', 220),
('Fernando Moraes', 'fernando.m@example.com', '4498765789', 5),
('Priscila Cunha', 'priscila.c@example.com', '4498876890', 145),
('André Viana', 'andre.v@example.com', '4498987901', 70),
('Renata Pires', 'renata.p@example.com', '4499098012', 310),
('Alexandre Duarte', 'alexandre.d@example.com', '4499209123', 0),
('Tatiana Batista', 'tatiana.b@example.com', '4499310234', 190);

-- Filmes (Tropa de Elite inserido)
INSERT INTO filmes (genero_id, titulo, sinopse, duracao_minutos, classificacao) VALUES 
(2, 'Matrix', 'Um hacker descobre que a realidade é uma simulação.', 136, '14 Anos'),
(1, 'Vingadores: Ultimato', 'Os heróis sobreviventes tentam reverter as ações de Thanos.', 181, '12 Anos'),
(1, 'O Cavaleiro das Trevas', 'Batman enfrenta o Coringa em Gotham.', 152, '14 Anos'),
(2, 'Interestelar', 'Viagem através de um buraco de minhoca em busca de um lar.', 169, '10 Anos'),
(5, 'Toy Story 4', 'Woody e Buzz em uma nova aventura com Garfinho.', 100, 'Livre'),
(3, 'Coringa', 'A história de origem de Arthur Fleck.', 122, '16 Anos'),
(7, 'Jurassic Park', 'Dinossauros de volta à vida em um parque temático.', 127, '12 Anos'),
(1, 'Tropa de Elite', 'O dia a dia do BOPE na cidade do Rio de Janeiro e a luta contra o crime.', 115, '16 Anos');

-- Sessoes (Hoje e Amanhã - Ajustado para não usar Sala 5)
INSERT INTO sessoes (filme_id, sala_id, data_horario, preco_padrao, status) VALUES 
(1, 1, CURRENT_DATE + TIME '14:00:00', 40.00, 'DISPONIVEL'),
(1, 1, CURRENT_DATE + TIME '18:00:00', 40.00, 'DISPONIVEL'),
(2, 2, CURRENT_DATE + TIME '19:30:00', 65.00, 'LOTADA'),
(4, 3, CURRENT_DATE + TIME '20:00:00', 45.00, 'DISPONIVEL'),
(5, 4, CURRENT_DATE + TIME '13:00:00', 30.00, 'DISPONIVEL'),
(6, 4, CURRENT_DATE + TIME '21:30:00', 30.00, 'DISPONIVEL'),
(7, 1, CURRENT_DATE + INTERVAL '1 day' + TIME '15:00:00', 40.00, 'DISPONIVEL'),
(8, 2, CURRENT_DATE + INTERVAL '1 day' + TIME '19:00:00', 30.00, 'DISPONIVEL');

-- Ingressos e Pagamentos
INSERT INTO ingressos (sessao_id, cliente_id, poltrona, tipo_ingresso, preco_pago, status) VALUES 
(1, 1, 'H04', 'INTEIRA', 40.00, 'CONFIRMADO'),
(1, 2, 'H05', 'MEIA', 20.00, 'CONFIRMADO'),
(1, NULL, 'F01', 'INTEIRA', 40.00, 'CONFIRMADO'),
(1, 3, 'G10', 'INTEIRA', 40.00, 'CANCELADO'),
(3, 4, 'A01', 'INTEIRA', 65.00, 'CONFIRMADO'),
(3, 5, 'A02', 'MEIA', 32.50, 'CONFIRMADO'),
(3, 6, 'D04', 'INTEIRA', 65.00, 'CONFIRMADO'),
(3, 7, 'D05', 'INTEIRA', 65.00, 'CONFIRMADO'),
(4, 8, 'E07', 'INTEIRA', 45.00, 'CONFIRMADO'),
(4, 9, 'E08', 'MEIA', 22.50, 'CONFIRMADO'),
(5, 10, 'B01', 'MEIA', 15.00, 'CONFIRMADO'),
(5, 10, 'B02', 'MEIA', 15.00, 'CONFIRMADO'),
(5, 10, 'B03', 'INTEIRA', 30.00, 'CONFIRMADO'),
(8, 25, 'C01', 'INTEIRA', 30.00, 'CONFIRMADO'),
(8, 30, 'C02', 'INTEIRA', 30.00, 'CONFIRMADO');

INSERT INTO pagamentos (ingresso_id, metodo, status) VALUES 
(1, 'PIX', 'APROVADO'), (2, 'CARTAO_CREDITO', 'APROVADO'),
(3, 'DINHEIRO', 'APROVADO'), (4, 'PIX', 'ESTORNADO'),
(5, 'CARTAO_CREDITO', 'APROVADO'), (6, 'CARTAO_DEBITO', 'APROVADO'),
(7, 'PIX', 'APROVADO'), (8, 'PIX', 'APROVADO'),
(9, 'CARTAO_CREDITO', 'APROVADO'), (10, 'CARTAO_CREDITO', 'APROVADO'),
(11, 'PIX', 'APROVADO'), (12, 'PIX', 'APROVADO'), (13, 'PIX', 'APROVADO'),
(14, 'PIX', 'APROVADO'), (15, 'PIX', 'APROVADO');


-- ==========================================
-- VIEWS PARA OS SERVIÇOS WEB / PYTHON
-- ==========================================

-- View 1: Lista consolidada de filmes em cartaz e horários (Facilita o servico_filmes e servico_sessoes)
CREATE VIEW vw_resumo_sessoes AS
SELECT 
    s.sessao_id, f.titulo, g.nome AS genero, sa.nome AS sala, sa.tipo AS tipo_sala,
    s.data_horario, s.preco_padrao, s.status,
    sa.capacidade - (SELECT COUNT(*) FROM ingressos i WHERE i.sessao_id = s.sessao_id AND i.status = 'CONFIRMADO') AS assentos_livres
FROM sessoes s
JOIN filmes f ON f.filme_id = s.filme_id
JOIN generos g ON g.genero_id = f.genero_id
JOIN salas sa ON sa.sala_id = s.sala_id
WHERE f.ativo = TRUE;

-- View 2: Relatório de ingressos vendidos (Facilita o servico_ingresso)
CREATE VIEW vw_detalhes_ingressos AS
SELECT 
    i.ingresso_id, f.titulo, s.data_horario, sa.nome AS sala, i.poltrona, 
    COALESCE(c.nome, 'Cliente Anônimo') AS comprador, 
    i.tipo_ingresso, i.preco_pago, i.status AS status_ingresso, p.metodo AS metodo_pagamento
FROM ingressos i
JOIN sessoes s ON s.sessao_id = i.sessao_id
JOIN filmes f ON f.filme_id = s.filme_id
JOIN salas sa ON sa.sala_id = s.sala_id
LEFT JOIN clientes c ON c.cliente_id = i.cliente_id
JOIN pagamentos p ON p.ingresso_id = i.ingresso_id;


-- ==========================================
-- ÍNDICES DE PERFORMANCE
-- ==========================================
CREATE INDEX idx_sessoes_filme ON sessoes(filme_id);
CREATE INDEX idx_sessoes_data ON sessoes(data_horario);
CREATE INDEX idx_ingressos_sessao ON ingressos(sessao_id);
CREATE INDEX idx_ingressos_cliente ON ingressos(cliente_id);
CREATE INDEX idx_filmes_genero ON filmes(genero_id);