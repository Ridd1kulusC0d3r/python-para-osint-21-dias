# 🏆 Desafio S — Dia 20: A API do caso

**Carta 62 · Rank S**

## A missão

O painel fez sucesso. Agora o setor de análise quer **puxar os dados direto para as planilhas e
scripts deles**, sem copiar da tela. Eles pedem uma **API**: endereços que devolvem JSON.

Escreva um servidor, só com `http.server`, que tenha:

1. `GET /api/denuncias` com filtros opcionais que se somam:
   `cidade` (contém, sem acento), `chave` (começa com), `de` e `ate` (datas `AAAA-MM-DD`).
   Resposta: `{"quantidade": N, "filtros": {...}, "denuncias": [...]}`.
2. `GET /api/resumo`: total de denúncias, total em reais, total por chave PIX e quantidade por mês.
3. `GET /`: uma página HTML curta explicando as rotas.
4. Qualquer outra rota: **404 em JSON** (`{"erro": ...}`), não uma página HTML.
5. As denúncias publicadas **não** podem conter `nome_vitima` nem `cpf`.
6. Modo teste (com `OSINT_OFFLINE=1`): sobe numa thread, testa todas as rotas a si mesmo e encerra.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] `Content-Type: application/json; charset=utf-8` nas rotas da API
- [ ] Valores em reais sem erro de arredondamento (`Decimal`, enviado como texto)
- [ ] Um `assert` garante que nome e CPF não aparecem na resposta
- [ ] O teste não trava: o script termina sozinho

## Dica

Datas no formato ISO (`2025-11-28`) podem ser comparadas **como texto**: `"2025-11-01" <= d <=
"2025-11-30"` funciona, porque a ordem alfabética é a ordem cronológica. Isso não vale para
`28/11/2025`!

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- A minimização acontece **na carga**: `{k: d[k] for k in PUBLICOS}` descarta nome e CPF antes de
  qualquer rota existir. O que não está na memória não vaza.
- `json.dumps(..., ensure_ascii=False)` mantém "Divinópolis" legível no JSON.
- `urllib.error.HTTPError` também tem corpo: `json.load(erro)` lê o JSON do 404 no teste.
- Resultados: total R$ 54877.40; `cidade=juiz de fora` → 4; chave `f38b` em novembro → 10.

</details>
