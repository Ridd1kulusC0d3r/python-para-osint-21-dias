# 🏆 Desafio S — Dia 10: Caçador de lojas irmãs

**Carta 52 · Rank S**

## A missão

Golpista raramente monta uma loja só. Quando uma cai, outra sobe com outro nome, mas costuma carregar
os mesmos "vícios": a mesma plataforma, a mesma chave PIX, o mesmo WhatsApp, o mesmo e-mail esquecido
num comentário. A Iara recebeu de outras delegacias três páginas salvas (fictícias) em
[`dados/lojas_suspeitas/`](dados/lojas_suspeitas). Quais delas são irmãs da MegaOferta?

Escreva um script que:

1. Extraia a **impressão digital** da vitrine do caso (`caso/dados/vitrine_megaoferta.html`):
   `generator`, chaves PIX, números de `wa.me/`, e-mails de `mailto:` **e de comentários**.
2. Extraia a mesma impressão digital de cada `.html` da pasta de suspeitas.
3. Dê **pontos** por coincidência, com pesos diferentes (plataforma vale pouco, PIX e telefone valem muito).
4. Marque com 🚩 quem passar de `PONTOS_PARA_ALERTA` (padrão: 3).
5. Grave `saidas/lojas_irmas.csv` com `;` e `utf-8-sig`.

## Critérios de rank S

- [ ] Só biblioteca padrão (`html.parser`, `csv`, `pathlib`)
- [ ] Usa **conjuntos** (`set`) e interseção (`&`) para comparar traços
- [ ] Uma página ilegível não derruba o script
- [ ] A loja sem relação com o caso fica com 0 pontos
- [ ] Explica em um comentário por que `generator` sozinho **não** prova nada

## Dica

Monte um dicionário `{"generator": set(), "pix": set(), ...}` dentro do seu `HTMLParser`. Comparar duas
lojas vira `referencia["pix"] & suspeita["pix"]`.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- O mesmo `HTMLParser` serve para a referência e para as suspeitas: escreva uma vez, use várias.
- O e-mail `kau.ofertas@example.com` só aparece num **comentário**: quem ignora `handle_comment` perde
  a ligação com a *SuperPreço Ofertas*.
- A *Clube dos Descontos* usa o **mesmo WhatsApp** do caso. A *Livraria do Bairro* não tem nada em
  comum (nem a plataforma).
- **Bônus:** a SuperPreço usa a chave `e5121482-…`, que não está na vitrine, mas aparece na conversa do
  Dia 11. Acrescente as chaves da conversa à referência e veja o placar mudar.

</details>
