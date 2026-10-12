# 📖 Glossário

Termos de Python e de OSINT que aparecem no curso, explicados sem jargão. Entre parênteses, o dia em que o termo aparece primeiro.

## Python

| Termo | O que é |
|---|---|
| **Biblioteca padrão (stdlib)** | O conjunto de módulos que já vem com o Python, sem `pip install`. Toda a camada BR usa só ela. (0) |
| **Script** | Um arquivo `.py` com instruções que o Python executa de cima para baixo. (1) |
| **Variável** | Um nome que guarda um valor: `cidade = "Belo Horizonte"`. (2) |
| **f-string** | Texto com valores embutidos: `f"Olá, {nome}"`. (1) |
| **Lista** | Sequência ordenada de valores: `["BH", "Contagem"]`. (2) |
| **Dicionário** | Pares chave → valor: `{"uf": "MG"}`. É o formato natural do JSON em Python. (6) |
| **Laço (`for`)** | Repete um bloco para cada item de uma sequência. (2) |
| **Condição (`if`)** | Executa um bloco só se algo for verdadeiro. (2) |
| **Função** | Um bloco de código com nome, que recebe entradas e devolve um resultado. (2) |
| **Módulo / `import`** | Trazer código pronto para o seu script: `import json`. (3) |
| **`pip`** | O instalador de bibliotecas de terceiros (usado só no nível 1). (3) |
| **`argparse`** | Módulo para criar comandos com opções: `--cep 30130010`. (3) |
| **`subprocess`** | Módulo para rodar outros programas a partir do Python. (3) |
| **Codificação (UTF-8)** | A forma de guardar letras como bytes. Sempre use `encoding="utf-8"` para não estragar acentos. (4) |
| **`try` / `except`** | Tenta fazer algo e, se der erro, trata o erro em vez de parar o script. (5) |
| **`map`** | Aplica uma função a cada item de uma lista. (16) |
| **Expressão regular (regex)** | Um padrão de texto para encontrar CPFs, e-mails etc. Módulo `re`. (11) |
| **`pathlib`** | Jeito moderno de trabalhar com caminhos de arquivos e pastas. (14) |
| **Hash (SHA-256)** | Uma "impressão digital" de um arquivo; muda se um único byte mudar. Módulo `hashlib`. (14) |
| **Fuso horário (`zoneinfo`)** | Datas com fuso correto: `America/Sao_Paulo`. (19) |
| **doctest / unittest** | Formas de testar automaticamente se o seu código continua certo. (21) |
| **Notebook (Colab/Jupyter)** | Documento com texto e células de código que você roda uma a uma. (0) |
| **`#@param`** | Comentário especial do Colab que vira um campo de formulário. (0) |

## Internet e dados

| Termo | O que é |
|---|---|
| **HTTP / requisição** | O pedido que o seu programa faz a um site ou API. (5) |
| **API** | Um endereço feito para programas conversarem, geralmente devolvendo JSON. (5) |
| **JSON** | Formato de texto para dados estruturados (chaves e valores). (6) |
| **CSV** | Planilha em texto, com colunas separadas por vírgula ou `;` (padrão do Excel em pt-BR). (7) |
| **SQL / SQLite** | Linguagem para consultar bancos de dados; SQLite é um banco num único arquivo, já incluso no Python. (8) |
| **Dump** | Cópia de um banco de dados em texto (`.sql`). (8) |
| **Scraping (raspagem)** | Extrair informação de páginas HTML. (10) |
| **robots.txt** | Arquivo onde o site diz o que robôs podem ou não acessar. (10) |
| **User-Agent** | A "identidade" que o seu programa apresenta ao site. (12) |
| **Proxy** | Um intermediário entre você e o site; o site vê o IP do proxy. (12) |
| **Rate limit** | Limite de quantas requisições você pode fazer por minuto/hora. (5) |

## OSINT e investigação

| Termo | O que é |
|---|---|
| **OSINT** | Inteligência a partir de fontes abertas (públicas). |
| **Dork** | Busca com operadores avançados (`site:`, `filetype:`) para achar o que o buscador já indexou. (9) |
| **WHOIS** | Protocolo antigo (porta 43) para consultar quem registrou um domínio. (15) |
| **RDAP** | O substituto moderno do WHOIS, com respostas em JSON via HTTPS. (15) |
| **DNS** | Sistema que traduz nomes (`gov.br`) em endereços e diz quem recebe os e-mails (MX). (15) |
| **SPF** | Registro DNS que lista quem pode enviar e-mail por um domínio. (15) |
| **Wayback Machine** | Arquivo histórico da web, do Internet Archive. (19) |
| **CDX** | A API da Wayback que lista as capturas de uma URL. (19) |
| **Memento** | Uma captura de uma página numa data específica. (19) |
| **Laranja** | Pessoa ou empresa que empresta o nome/conta para movimentar dinheiro de outra. (8) |
| **Chave PIX aleatória** | Identificador no formato UUID (`xxxxxxxx-xxxx-…`) ligado a uma conta. (11) |
| **Sock puppet (fantoche)** | Perfil de pesquisa separado da identidade real do analista. Use com ética e dentro da lei. (12) |
| **OPSEC** | Segurança operacional: não deixar rastros que exponham você ou a investigação. (12) |
| **Cadeia de custódia** | O registro de quem coletou, quando, como e que a evidência não mudou. (14) |
| **Pivô** | Usar uma informação (e-mail, telefone, chave PIX) para chegar a outra. |
| **Falso positivo** | Algo que parece ser o que você procura, mas não é (ex.: número com cara de CPF que não passa na validação). (11) |
