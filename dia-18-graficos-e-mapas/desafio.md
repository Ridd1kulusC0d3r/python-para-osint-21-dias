# 🏆 Desafio S — Dia 18: Cartógrafo offline

**Carta 60 · Rank S**

## A missão

A Iara precisa levar o mapa para uma reunião numa sala sem internet. E a Delegada Rita fez uma
pergunta nova: **a que distância as vítimas estão do "endereço" da loja?**

Escreva um script que:

1. Padronize as cidades de `denuncias.csv` e conte as vítimas por cidade.
2. Converta latitude/longitude em x/y de um SVG (projeção **equirretangular**: x vem da longitude,
   y da latitude), com a longitude multiplicada pelo **cosseno da latitude média** para o mapa não
   ficar "esticado".
3. Desenhe um círculo por cidade com **área** proporcional às vítimas, com o nome ao lado, e um
   ponto preto no endereço do rodapé (centro de BH).
4. Calcule a distância em linha reta de cada cidade até o rodapé com a **fórmula de haversine**.
5. Imprima as cidades da mais perto para a mais longe e diga quantas vítimas estão a mais de 200 km.
6. Grave `saidas/mapa_offline.svg`, que abre **sem internet**.

## Critérios de rank S

- [ ] Só biblioteca padrão (`math`, `csv`, `html`...), sem azulejos online
- [ ] Norte para cima: Uberlândia à esquerda, Governador Valadares à direita, Juiz de Fora embaixo
- [ ] Raio ∝ √vítimas
- [ ] Distância BH → Uberlândia entre 450 e 500 km

## Dica

Haversine: `h = sen²(Δlat/2) + cos(lat1)·cos(lat2)·sen²(Δlon/2)` e `d = 2·R·asen(√h)`, com
R = 6371 km e todos os ângulos em **radianos** (`math.radians`).

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `y = (lat_max - lat) * escala`: subtrair do máximo inverte o eixo, porque no SVG y cresce para baixo.
- `fator = cos(latitude média)`: em -20°, um grau de longitude mede cerca de 94% de um grau de latitude.
- `map(math.radians, (*a, *b))` converte as quatro coordenadas de uma vez.
- Resultado: 17 das 37 vítimas estão a mais de 200 km; Uberlândia fica a cerca de 470 km do rodapé.

</details>
