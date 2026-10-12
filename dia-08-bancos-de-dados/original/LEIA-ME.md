# Dia 8 original: não há código do autor

No curso original, o **Dia 8 (Databases)** não traz script. O cipher387 explica que existem pacotes
Python para praticamente todo banco de dados (MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch…),
mas preferiu dar conselhos gerais em vez de exemplos para um banco específico. Em resumo, com nossas
palavras:

1. **Arquivos `.sql` aparecem muito em investigações.** São *dumps*: cópias de um banco de dados em
   forma de texto, com os comandos `CREATE TABLE` e `INSERT`. Às vezes contêm listas de contatos
   (e-mails, telefones).
2. **Eles às vezes ficam expostos e indexados por buscadores.** O autor cita o *Google Hacking
   Database* (GHDB, da Exploit-DB), que reúne consultas ("dorks") para achar esse tipo de arquivo.
3. **O jeito mais fácil de olhar um dump é convertê-lo para CSV** e abrir numa planilha. Ele indica
   conversores online.
4. Além de `.sql`, vale conhecer outros formatos de banco: Access (`.mdb`), SQL Server (`.mdf`),
   SQLite (`.sqlite`, `.db`, `.db3`…), Firebird (`.fdb`).
5. Como prática, ele sugere procurar exemplos públicos e estudar como são organizados.

## O que fizemos aqui

- [`nivel1_sql_para_csv.py`](nivel1_sql_para_csv.py) é uma **reconstrução** da prática proposta (não é
  código do autor): carrega o dump **fictício** `caso/dados/painel_dump.sql` num banco SQLite em
  memória e exporta cada tabela para CSV. É o "conversor online" do autor, só que local, sem enviar
  dado nenhum para terceiros.
- A camada BR (`../br/`) vai além: explorar a estrutura do banco, fazer `JOIN`/`GROUP BY` e montar o
  banco do caso com consultas parametrizadas.

## ⚠️ Sobre a sugestão de procurar dumps na internet

Adaptamos esse ponto. **Não baixe, não abra e não guarde vazamentos reais.** Dumps expostos costumam
ter dados pessoais de pessoas que nunca consentiram, e mexer neles pode configurar crime e violar a
LGPD (veja o README do dia). Use dorks só para **entender o risco de exposição** de uma organização
que você está autorizado a avaliar, e treine com dados fictícios, como o deste repositório.
