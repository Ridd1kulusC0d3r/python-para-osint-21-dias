# 🏆 Desafio S — Dia 15: Radar de domínios recém-nascidos

**Carta 57 · Rank S**

## A missão

A Iara quer um **radar**: sempre que surgir uma nova denúncia de loja falsa, o NFA cola o domínio numa
lista e o script diz, em segundos, quais são "recém-nascidos".

Escreva um script que:

1. Receba uma lista de domínios separados por vírgula (parâmetro `DOMINIOS`).
2. Descubra o servidor RDAP de cada um pelo **bootstrap da IANA**.
3. Consulte o RDAP e extraia: data de criação, idade em dias e nameservers.
4. Marque com 🚩 quem tiver menos de `LIMITE_DIAS` (padrão: 90).
5. Grave `saidas/radar_dominios.csv` com separador `;` e codificação `utf-8-sig`
   (assim o Excel em português abre certinho).
6. Funcione **sem internet** usando as amostras (`dados/` e `caso/dados/`).

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Não quebra se um domínio não existir ou o servidor não responder
- [ ] O domínio do caso aparece como 🚩
- [ ] CSV abre no Excel sem caracteres estranhos

## Dica

Monte um dicionário `tld → servidor` uma única vez, antes do laço. Assim você baixa o bootstrap só uma vez.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `{tld: urls[0] for tlds, urls in bootstrap["services"] for tld in tlds}` cria o mapa em uma linha.
- Cada consulta fica num `try/except`: um domínio com problema não derruba o radar inteiro.
- Para o domínio fictício, a idade é medida na data da primeira denúncia, não "hoje".

</details>
