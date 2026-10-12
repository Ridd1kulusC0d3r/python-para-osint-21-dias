# 🏆 Desafio S — Dia 11: O elo telefônico

**Carta 53 · Rank S**

## A missão

O mesmo telefone aparece escrito de cinco jeitos: `(31) 98888-0101`, `+55 31 9 8888-0101`,
`5531988880101` (dentro do link `wa.me/`), `31988880101`... Para o computador, são cinco coisas
diferentes. A Iara quer **uma** forma canônica e um mapa de onde cada número aparece.

Escreva um script que:

1. Procure telefones em **todas** as fontes de texto do caso: `conversa_whatsapp.txt`,
   `vitrine_megaoferta.html`, `depoimentos/*.txt` e a coluna `telefone_contato` de `denuncias.csv`.
2. **Normalize** cada número para `+55` + DDD + número (ex.: `+5531988880101`).
3. Monte um dicionário `telefone → conjunto de fontes`.
4. Mostre os números que aparecem em pelo menos `MIN_FONTES` fontes (padrão: 2), do mais citado
   para o menos citado.

## Critérios de rank S

- [ ] Só biblioteca padrão (`re`, `csv`, `pathlib`, `collections`)
- [ ] Os dígitos de chaves PIX e CPFs **não** viram telefones falsos
- [ ] O número dentro de `wa.me/5531988880101` é reconhecido
- [ ] O telefone do vendedor aparece no topo, ligando vitrine, conversa e depoimentos
- [ ] Um arquivo faltando não derruba o script

## Dica

Normalizar é mais fácil do que parece: `re.sub(r"\D", "", texto)` deixa só os dígitos. Depois é contar:
10 ou 11 dígitos = DDD + número; 12 ou 13 começando com `55` = com código do país.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `defaultdict(set)` evita o `if tel not in dicionario` e o `set` impede contar a mesma fonte duas vezes.
- Antes de procurar telefones, **apague** UUIDs e CPFs do texto (`re.sub`): é o mesmo truque de
  "mascarar" do script 02.
- `(?<![\d-])` e `(?![\d-])` impedem casar um pedaço de um número maior (ou de um UUID).
- Resultado: `+5531988880101` em 7 fontes (vitrine, conversa e os 5 depoimentos). Cada vítima com
  depoimento aparece em 2 fontes (depoimento + planilha), o que confirma que a planilha bate com os
  depoimentos.

</details>
