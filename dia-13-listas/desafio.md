# 🏆 Desafio S — Dia 13: Fila de diligências

**Carta 55 · Rank S**

## A missão

A Delegada Rita só tem efetivo para pedir os dados de **uma conta por vez** ao banco. Por qual chave
PIX começar? A Iara quer uma "fila de diligências" pronta para ir no ofício.

Escreva um script que, a partir de `caso/dados/denuncias.csv`:

1. **Agrupe** as denúncias por `chave_pix_destino` (uma lista de denúncias por chave).
2. **Ordene** cada lista pela data (e pelo `id`, para desempatar).
3. Para cada chave, calcule: número de vítimas, **total** com `Decimal`, primeira e última denúncia
   (`lista[0]` e `lista[-1]`), a cidade com mais vítimas (`Counter`) e as cidades em ordem alfabética
   **correta** (com acento e sem repetidos).
4. **Ordene a fila** pelo total (maior prejuízo primeiro); empate → mais vítimas primeiro.
5. Imprima e grave `saidas/fila_diligencias.txt` com os valores em formato brasileiro (`R$ 21.242,10`).

## Critérios de rank S

- [ ] Só biblioteca padrão (`csv`, `decimal`, `collections`, `unicodedata`)
- [ ] Cidades padronizadas antes de contar ("belo horizonte" e "Belo Horizone" são a mesma)
- [ ] `sort(key=...)` com **tupla** para desempatar
- [ ] O total geral bate com a soma de todas as denúncias

## Dica

`collections.defaultdict(list)` cria a lista vazia sozinho na primeira vez que a chave aparece:
`por_chave[chave].append(denuncia)`.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- Datas no formato ISO (`2025-11-30`) ordenam certo **como texto**: não precisa converter.
- `sum(..., Decimal("0"))`: o valor inicial em `Decimal` evita misturar com `int`.
- Para formatar em reais: `f"{valor:,.2f}"` dá `21,242.10`; troque `,` ↔ `.` usando um caractere
  temporário.
- Resultado: a chave `f38b2ffc-…` lidera com 16 vítimas e **R$ 21.242,10**. Ela é a chave exibida na
  vitrine (Dia 10).

</details>
