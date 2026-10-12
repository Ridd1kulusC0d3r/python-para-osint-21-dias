# 🏆 Desafio S — Dia 8: Conciliação painel × denúncias

**Carta 50 · Rank S**

## A missão

O dump do painel diz quem recebeu. A planilha diz quem denunciou. Um advogado de defesa vai perguntar:
*"como vocês sabem que o pedido 14 do painel é a mesma pessoa da denúncia DEN-014?"*. A Iara quer a
resposta pronta, linha por linha.

Escreva um script que:

1. Carregue `caso/dados/painel_dump.sql` e importe `caso/dados/denuncias.csv` **no mesmo banco**
   SQLite (sem levar CPF nem telefone, que não são necessários para conciliar).
2. Ligue cada denúncia ao pedido do painel por **nome + data + valor** (em centavos), com
   `LEFT JOIN`, para que nenhuma denúncia suma do resultado.
3. Marque 🚩 quando: a denúncia não tiver pedido correspondente, ou a chave PIX que a vítima informou
   for diferente da chave da conta que o painel registrou.
4. Conte os **pedidos sem denúncia** (vítimas que ainda não procuraram a polícia).
5. Mostre a **linha do tempo** das contas laranja: primeira e última data de uso, pedidos e total.
6. Grave `saidas/conciliacao.csv` (`;`, `utf-8-sig`).
7. Use só consultas com `?` para qualquer valor que venha de fora.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Soma em centavos inteiros (nada de `SUM(valor)` em float)
- [ ] As 37 denúncias aparecem no CSV, com a situação de cada uma
- [ ] A linha do tempo mostra em que ordem as três contas entraram em uso

## Dica

`NOT EXISTS (SELECT 1 FROM … WHERE …)` responde "quais pedidos não têm denúncia?" sem precisar de laço
em Python.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `CAST(ROUND(p.valor * 100) AS INTEGER) = d.valor_centavos` compara dinheiro sem o erro do float.
- `LEFT JOIN` mantém a denúncia mesmo sem par; o pedido vem `None` e vira 🚩.
- No caso fictício, tudo concilia: **zero divergência**. Isso é um resultado, não uma falha: diz que o
  dump é coerente com as vítimas e reforça seu valor como evidência.

</details>
