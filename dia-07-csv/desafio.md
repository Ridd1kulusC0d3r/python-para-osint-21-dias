# 🏆 Desafio S — Dia 7: Resumo regional das denúncias

**Carta 49 · Rank S**

## A missão

A Delegada Rita ligou: o Ministério Público quer saber **em que regiões de Minas** o golpe pegou mais
gente, porque pode haver outras delegacias com o mesmo caso. Ela precisa de uma planilha que abra
direto no Excel, sem ninguém "arrumar" nada.

Escreva um script que:

1. Padronize a coluna `cidade` de `caso/dados/denuncias.csv` com a base do IBGE (como no script 03).
2. Descubra a **mesorregião** de cada cidade (campo `microrregiao → mesorregiao → nome`), sem quebrar
   quando `microrregiao` vier `null`.
3. Calcule, com `Decimal`, **vítimas e prejuízo por cidade** e **por mesorregião**.
4. Grave `saidas/resumo_por_cidade.csv` e `saidas/resumo_por_mesorregiao.csv` com `;`,
   `utf-8-sig` e **vírgula decimal** (`21441,30`), para o Excel brasileiro reconhecer como número.
5. Mostre um relatório de qualidade: quantas cidades estavam certas, quantas foram normalizadas,
   aproximadas ou não reconhecidas.
6. **Confira** que a soma por cidade bate com o total da planilha original.
7. Funcione **sem internet** com a amostra do IBGE.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Nenhuma cidade some: as não reconhecidas aparecem marcadas para revisão humana
- [ ] A soma confere (✅) e os valores abrem como número no Excel em pt-BR
- [ ] A Região Metropolitana de BH aparece em primeiro lugar

## Dica

`(m.get("microrregiao") or {}).get("mesorregiao")`: o `or {}` troca `None` por um dicionário vazio,
e o `.get` seguinte não quebra.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `defaultdict(lambda: {"vitimas": 0, "prejuizo": Decimal("0"), …})` cria o "acumulador" de cada
  cidade na primeira vez que ela aparece.
- `f"{valor:.2f}".replace(".", ",")` gera `21441,30`: sem separador de milhar, o Excel em português
  entende como número e você pode somar a coluna.
- A conferência final (`total == conferido`) é o tipo de teste que evita entregar um relatório errado.

</details>
