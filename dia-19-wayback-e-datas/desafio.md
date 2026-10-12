# 🏆 Desafio S — Dia 19: Que vitrine a vítima viu?

**Carta 61 · Rank S**

## A missão

A defesa vai perguntar: "Como vocês sabem o que o site mostrava quando a vítima comprou?". A
resposta honesta é: pela captura da Wayback **mais próxima antes** da compra. A Iara quer isso
calculado para cada uma das 37 denúncias.

Escreva um script que:

1. Leia `caso/dados/wayback_cdx_megaoferta.json` e converta cada `timestamp` (UTC) para o horário de
   Brasília.
2. Para cada denúncia, encontre a captura **mais recente com data menor ou igual** à da compra,
   usando o módulo **`bisect`** (busca binária), não um laço que testa todas.
3. Calcule a **defasagem** em dias entre a captura e a compra.
4. Conte quantas denúncias "viram" cada versão do site.
5. Liste as maiores **lacunas** entre capturas consecutivas e quantas denúncias caíram dentro delas.
6. Grave `saidas/vitrine_vista_por_denuncia.csv` (`;`, `utf-8-sig`) com o link do memento de cada uma.

## Critérios de rank S

- [ ] Só biblioteca padrão, 100% offline
- [ ] `bisect` sobre uma lista **ordenada** de datas
- [ ] Datas convertidas de UTC para America/Sao_Paulo (com plano B)
- [ ] Nenhuma denúncia associada a uma captura **posterior** à compra

## Dica

`bisect.bisect_right(lista, x)` devolve a posição onde `x` entraria, **depois** de itens iguais a
ele. Então `bisect_right(datas, dia) - 1` é o índice da última data `<= dia`. Se der `-1`, não
existe captura antes da compra.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `cabecalho, *linhas = json.loads(...)` separa o cabeçalho do resto numa linha.
- `zip(capturas, capturas[1:])` percorre pares consecutivos (a captura e a seguinte) para as lacunas.
- Resultado: a captura de 04/10 cobre 10 denúncias, a de 03/11 cobre 16 e a de 28/11 cobre 11.
  A maior lacuna (04/10 → 03/11, 30 dias) deixa 10 denúncias sem prova direta do que o site
  mostrava. DEN-018 comprou 26 dias depois da captura mais próxima.

</details>
