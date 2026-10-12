# 🏆 Desafio S — Dia 4: Fichas padronizadas e vínculos

**Carta 46 · Rank S**

## A missão

A Delegada Rita gostou do resumo, mas pediu duas coisas:

> "Quero **uma ficha por depoimento**, sempre no mesmo formato, para anexar ao inquérito. E quero saber,
> sem precisar ler tudo, **quando o mesmo número ou a mesma chave PIX aparece em mais de uma denúncia**."

Escreva um script que:

1. Leia todos os arquivos de `caso/dados/depoimentos/`.
2. Extraia, de cada um: data, vítima, cidade, produto, valor, chave PIX e WhatsApp do vendedor.
   Se um campo não existir, escreva `(não informado)`.
3. Grave `saidas/fichas/<id>.txt` no formato `campo: valor`, uma linha por campo, terminando com
   `fonte: <arquivo de origem>`.
4. Mostre os **vínculos**: WhatsApps e chaves PIX que aparecem em mais de um depoimento.
5. Acrescente uma linha com data/hora de Brasília em `saidas/historico.log` a cada execução.
6. Releia uma das fichas e confira se ela bate com o que foi extraído.

## Critérios de rank S

- [ ] Só biblioteca padrão, `encoding="utf-8"` em todo `open()`
- [ ] Fichas com modo `"w"` (refeitas da fonte), histórico com modo `"a"` (nunca apaga)
- [ ] As regras de extração de cada campo ficam num lugar só (um dicionário de regras)
- [ ] O CPF **não** vai para a ficha
- [ ] Aparecem os vínculos das chaves `f38b2ffc…` e `e5121482…`

## Dica

`next((l for l in linhas if rotulo in l), None)` devolve a primeira linha que contém o rótulo, ou `None`.
E `grupos.setdefault(valor, []).append(id)` agrupa ids pelo mesmo valor sem precisar de `if`.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `REGRAS = {campo: (rótulo, função_de_corte)}`: para mudar a extração de um campo, você mexe numa linha só.
- Ficha com `"w"` e histórico com `"a"`: a ficha é um **produto** (refeito da fonte); o log é um **registro** (só cresce).
- A conferência final (`relida == extraída`) é um teste simples de que gravar e ler não perdeu nada.

</details>
