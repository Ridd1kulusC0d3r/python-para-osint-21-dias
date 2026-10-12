# Dia 8 — Bancos de dados

> 🃏 Cartas **8 · 29 · 50**  ·  📘 Original: *Day 8. Databases*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-08-bancos-de-dados/notebook.ipynb)

## 📖 Capítulo 8 — O dump do painel

<!-- historia:inicio -->
Quinta-feira, 16h30. A planilha padronizada de ontem ainda está aberta quando a Delegada Rita entra
na sala do NFA com um envelope pardo e um pen drive lacrado.

— Um ex-funcionário da hospedagem que atendia a loja procurou a delegacia. Diz que isso é uma cópia
do banco de dados do painel administrativo. Veio com termo de entrega assinado.

A Iara confere o lacre, anota a hora e só então pluga o pen drive. Dentro, um único arquivo:
**`painel_dump.sql`**.

— Primeiro o hash — ela diz, antes que você pergunte. — Depois a gente abre. E abre em memória, sem
espalhar cópia pelo disco.

Você roda o SHA-256, anota no termo, e carrega o dump no SQLite. Duas tabelas: **pedidos** e
**contas_recebimento**. Uma coluna chamada `conta_id` liga uma à outra.

— Esse fio é tudo — diz a Iara, apontando para a tela. — Até agora a gente sabia **quem perdeu**.
Com um `JOIN`, a gente descobre **quem recebeu**. Três contas, três titulares. E olha o sobrenome da
terceira.

A Delegada se inclina sobre seu ombro. Pela primeira vez no caso, o dinheiro tem destino.
<!-- historia:fim -->

## 🎯 Objetivos

- Entender o que é um **dump `.sql`** e por que ele aparece em investigações.
- Converter um dump em CSV (a prática proposta pelo autor), sem enviar nada a sites de terceiros.
- Explorar um banco desconhecido: `sqlite_master`, `PRAGMA table_info`, `LIMIT`.
- Responder perguntas com `JOIN`, `GROUP BY`, `COUNT` e `SUM` (em centavos!).
- Criar o banco do caso e consultar com **parâmetros `?`**, entendendo o SQL injection.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Um **banco de dados relacional** guarda tabelas, como planilhas, que se ligam por colunas em comum.
Um **dump** é o banco inteiro "impresso" como texto: os comandos `CREATE TABLE` (a estrutura) e
`INSERT` (as linhas). Qualquer programa de banco consegue reconstruí-lo.

```sql
SELECT c.titular, COUNT(*), SUM(p.valor)      -- 3. o que mostrar
  FROM pedidos p                              -- 1. de onde
  JOIN contas_recebimento c ON c.id = p.conta_id  -- 2. ligando as tabelas
 GROUP BY c.id                                -- 4. um resultado por conta
```

O Python já vem com o **SQLite** (`import sqlite3`): um banco inteiro num único arquivo, sem servidor.
É perfeito para análise: você importa o que tem (CSV, dump) e faz perguntas em SQL.

Duas regras de ouro: **dinheiro em centavos inteiros** (o tipo `REAL` é float e erra), e **nunca
monte SQL colando texto** do usuário: use `?` e passe os valores separados.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

O Dia 8 original **não tem código**: o autor dá conselhos sobre dumps `.sql`, o Google Hacking
Database e conversores de SQL para CSV. Resumimos tudo em [`original/LEIA-ME.md`](original/LEIA-ME.md)
e reconstruímos a prática proposta, só com biblioteca padrão:

| Arquivo | O que faz |
|---|---|
| [`original/LEIA-ME.md`](original/LEIA-ME.md) | Resumo da proposta do autor, com nossas palavras, e o alerta sobre vazamentos reais |
| [`original/nivel1_sql_para_csv.py`](original/nivel1_sql_para_csv.py) | **Reconstrução** (não é código do autor): dump fictício → SQLite em memória → um CSV por tabela |

```bash
cd dia-08-bancos-de-dados
python original/nivel1_sql_para_csv.py
```

> 💡 O autor sugere conversores online de SQL para CSV. Para dados de caso, **não use**: você estaria
> enviando evidência (e dados pessoais) para o servidor de um desconhecido. O script local faz o mesmo.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão** e 100% offline (os dados são os fictícios de `caso/dados/`).

| Arquivo | O que faz |
|---|---|
| [`br/01_explorar_dump.py`](br/01_explorar_dump.py) | Hash do dump, tabelas (`sqlite_master`), colunas (`PRAGMA table_info`), contagens e primeiras linhas |
| [`br/02_quem_recebeu.py`](br/02_quem_recebeu.py) | **O caso:** `JOIN` pedidos × contas, total por conta laranja em R$ e conferência com a planilha |
| [`br/03_banco_do_caso.py`](br/03_banco_do_caso.py) | Cria `saidas/caso.db` com as denúncias, consulta por mês e cidade e demonstra SQL injection |

```bash
cd dia-08-bancos-de-dados
python br/01_explorar_dump.py
python br/02_quem_recebeu.py
python br/03_banco_do_caso.py
```

**O que você deve ver no caso:**

| Conta (titular) | Pedidos | Recebido |
|---|---|---|
| Jéssica Prado Lima | 16 | R$ 21.242,10 |
| M. R. Brandão Comércio ME | 10 | R$ 17.840,90 |
| Wellington Arruda Paz | 11 | R$ 15.794,40 |
| **Total** | **37** | **R$ 54.877,40** |

O total do painel bate **centavo por centavo** com a planilha das vítimas. E a terceira conta tem o
mesmo sobrenome do vendedor "Kau": uma hipótese para investigar, não uma conclusão.

## ⚖️ Ética, LGPD e OPSEC

- **Vazamento real não é material de estudo.** Baixar, guardar ou compartilhar dumps com dados
  pessoais de terceiros viola a LGPD e pode configurar crime. Invadir um sistema para obtê-los é o
  crime do **art. 154-A do Código Penal** (invasão de dispositivo informático, Lei 12.737/2012, com
  penas aumentadas pela Lei 14.155/2021). Mesmo um arquivo "achado" no Google não vira dado público.
- **Dorks do GHDB** servem para entender **exposição**: avaliar se uma organização que você está
  autorizado a proteger deixou arquivo aberto. Achou algo de terceiros? Não abra; registre a URL e
  avise o responsável ou a autoridade competente.
- **Prova recebida exige cadeia de custódia.** Hash SHA-256 antes de abrir, registro de quem entregou,
  quando e como (arts. 158-A a 158-F do CPP; o Dia 14 aprofunda). Trabalhe numa cópia; o original
  fica lacrado.
- **Minimize.** O banco de análise (`caso.db`) não leva nome, CPF nem telefone das vítimas, porque as
  perguntas do dia não precisam deles.
- **Não use conversores online** para arquivos de caso. Tudo o que você precisa está no `sqlite3`.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Conciliação painel × denúncias**: liga cada denúncia ao seu pedido no
painel, aponta divergências, conta "vítimas silenciosas" e monta a linha do tempo dos laranjas.

## 🔎 Inovação OSINT do dia

**datasette.** Ferramenta open source criada por Simon Willison que transforma qualquer arquivo SQLite
num site navegável: busca, filtros, facetas, exportação para CSV/JSON e um campo para escrever SQL.
Com `pip install datasette` e `datasette saidas/caso.db`, a equipe inteira explora o banco do caso
pelo navegador, sem programar. Rode sempre **localmente** (`127.0.0.1`) para dados sensíveis.
Para quem quer ficar na stdlib: `sqlite3` + `csv` resolvem tudo deste dia.

## 📚 Para ir além

- Módulo `sqlite3` do Python (em português): <https://docs.python.org/pt-br/3/library/sqlite3.html>
- Funções de data do SQLite (`strftime`): <https://www.sqlite.org/lang_datefunc.html>
- Google Hacking Database (Exploit-DB): <https://www.exploit-db.com/google-hacking-database>
- datasette: <https://datasette.io/>
- OWASP sobre SQL injection: <https://owasp.org/www-community/attacks/SQL_Injection>

## ✅ Checklist

- [ ] Li o resumo do Dia 8 original e rodei a reconstrução (dump → CSV)
- [ ] Calculei o hash do dump antes de abrir
- [ ] Listei tabelas e colunas de um banco desconhecido
- [ ] Descobri quanto cada conta laranja recebeu, em centavos
- [ ] Vi o SQL injection acontecer (e ser bloqueado com `?`)
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
