mapeamento exato de qual serviço seu copia qual serviço do professor. A lógica, os tipos de busca (por ID, por status) e a estrutura serão espelhadas:

servico_pedidos.py ➔ servico_ingressos.py

-Por que: Pedidos têm "status" (Aprovado, Cancelado) e contabilizam valores totais e quantidades. Ingressos funcionam da mesma forma (Status: Confirmado, Cancelado, Utilizado).

-Rotas que terá: Buscar todos os ingressos, buscar ingressos por status, e contar a quantidade de ingressos em um status específico (exatamente como o /pedidos/quantidade/<status> do professor).

servico_estoque.py ➔ servico_sessoes.py

-Por que: O estoque avisa a "quantidade" restante de um produto (estoque baixo). A sessão avisa a "quantidade de assentos livres" restantes em uma sala para um filme.

-Rotas que terá: Buscar todas as sessões, buscar sessão por ID, buscar sessão pelo nome/descrição do filme.

servico_avaliacoes.py ➔ servico_filmes.py

-Por que: Avaliações trazem detalhes descritivos e estatísticas de um item do catálogo (o produto). Aqui, vamos trazer os detalhes descritivos do catálogo (sinopse, classificação, gênero).

-Rotas que terá: Buscar catálogo de filmes, buscar filme por ID, buscar filme por título (semelhante à busca por descrição do produto no código do professor).