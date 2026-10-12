# 🏆 Desafio S — Dia 17: Fábrica de ofícios

**Carta 59 · Rank S**

## A missão

Com o relatório preliminar em mãos, a Delegada Rita vai oficiar as instituições de pagamento que
receberam os PIX. São três chaves, três instituições, e a Iara não quer **ninguém** digitando ofício.

Escreva um script que:

1. Agrupe as denúncias de `denuncias.csv` por `chave_pix_destino`.
2. Descubra titular e instituição de cada chave em `ficha_do_caso.json`.
3. A partir de **um único modelo** (use `string.Template`, da biblioteca padrão), gere **um ofício
   HTML por chave**, com número sequencial, data por extenso em português ("12 de outubro de 2026"),
   tabela das transações daquela chave e total em reais.
4. Grave os ofícios em `saidas/oficios/` e um `indice_oficios.csv` (`;`, `utf-8-sig`) com número,
   instituição, quantidade, total e **SHA-256** de cada ofício.
5. Confira: a soma dos três ofícios tem que dar o total das denúncias.

## Critérios de rank S

- [ ] Só biblioteca padrão, 100% offline
- [ ] Um modelo só; nenhum texto de ofício repetido no código
- [ ] Todo texto vindo dos dados passa por `html.escape`
- [ ] Data por extenso sem depender do `locale` do sistema
- [ ] A soma confere com R$ 54.877,40

## Dica

`Template("Olá, $nome").substitute(nome="Rita")` troca `$nome`. Prefira `substitute` a
`safe_substitute`: se faltar uma variável, ele dá erro, e um erro é melhor do que um ofício com
"$titular" escrito no meio.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `defaultdict(list)` agrupa as denúncias por chave numa passada só.
- A data por extenso usa uma lista `MESES` própria: `f"{d.day} de {MESES[d.month - 1]} de {d.year}"`.
- O hash é calculado sobre os bytes exatos que foram gravados (`documento.encode("utf-8")`).
- Resultado: Cooperativa Imaginária (10 transações, R$ 17.840,90), Banco Digital Fictício
  (16, R$ 21.242,10) e Pague Já IP (11, R$ 15.794,40), somando R$ 54.877,40.

</details>
