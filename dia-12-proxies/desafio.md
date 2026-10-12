# 🏆 Desafio S — Dia 12: Peneira de proxies

**Carta 54 · Rank S**

## A missão

O script original do autor tenta proxies um por um e imprime "No" quando falham. A Iara quer mais:
um relatório que diga **quais servem** e, principalmente, **quais entregam você**.

Escreva um script que:

1. Leia uma lista de proxies `endereço:porta` de [`dados/proxies_teste.txt`](dados/proxies_teste.txt)
   (ignorando linhas vazias e comentários `#`).
2. Descubra o seu IP real (pedido **sem** proxy a `https://httpbin.org/get`, campo `origin`).
3. Para cada proxy, faça o mesmo pedido **através dele**, medindo a latência com `time.perf_counter()`.
4. Classifique:
   - ⛔ **morto**: deu erro ou passou do `TIMEOUT`;
   - 🚩 **transparente**: o seu IP real aparece em `origin` ou em algum cabeçalho;
   - 🟡 **anônimo**: o IP não aparece, mas há cabeçalhos como `Via` ou `X-Forwarded-For`;
   - ✅ **elite**: nenhum dos dois.
5. Ordene (elite primeiro, depois o mais rápido) e grave `saidas/proxies.csv` (`;`, `utf-8-sig`).

## Critérios de rank S

- [ ] Só biblioteca padrão (`urllib.request.ProxyHandler`, `json`, `time`, `csv`)
- [ ] `except Exception` (e não `except:` sozinho): um proxy ruim não derruba o laço
- [ ] Funciona offline com a amostra `dados/teste_proxies_amostra.json`
- [ ] Explica num comentário por que "elite" **não** quer dizer "seguro"

## Dica

`build_opener(ProxyHandler({"https": "http://198.51.100.10:3128"}))` cria um abridor que passa pelo
proxy. Um `ProxyHandler({})` vazio força o pedido **direto**, ignorando o proxy do sistema.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- O httpbin devolve `origin` com **todos** os IPs vistos (`"203.0.113.45, 198.51.100.22"`). Se o seu
  está ali, o proxy é transparente.
- Normalize os nomes dos cabeçalhos com `.title()` antes de comparar (`x-forwarded-for` →
  `X-Forwarded-For`).
- Cuidado com a precedência de `and`/`or`: `if a and b or c` não é `if a and (b or c)`.
- A lista da amostra usa IPs de documentação (RFC 5737): ninguém é "testado" sem querer.

</details>
