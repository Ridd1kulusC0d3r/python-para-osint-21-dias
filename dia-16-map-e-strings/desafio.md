# 🏆 Desafio S — Dia 16: Detector de grafias compatíveis

**Carta 58 · Rank S**

## A missão

O RDAP diz `Kaua T Brandao`. A Delegada Rita diz `Kauã Teixeira Brandão`. A Iara quer uma função
que responda, sem achismo: **essas duas grafias podem ser a mesma pessoa?**

Escreva um script que:

1. Tenha uma função `compativel(nome1, nome2)` que devolva `True` ou `False`.
2. Ignore acentos, maiúsculas, pontuação (`T.`) e partículas (da, de, dos, e).
3. Aceite **inicial no lugar do nome do meio** (`T` ≈ `Teixeira`), mas exija o **último sobrenome
   por extenso** (para não juntar "K. Brandão" com qualquer Brandão).
4. Recolha as grafias de nome que aparecem no RDAP, no WHOIS e em `denuncias.csv`, e **agrupe** as
   compatíveis entre si.
5. Liste os pares "quase iguais" que a regra **não** juntou, para revisão humana.

## Critérios de rank S

- [ ] Só biblioteca padrão, 100% offline
- [ ] `compativel("Kaua T Brandao", "Kauã Teixeira Brandão")` é `True`
- [ ] `compativel("M. R. Brandão", "Kauã Teixeira Brandão")` é `False`
- [ ] O script tem pelo menos 4 `assert` testando a regra
- [ ] Mostra o que precisa de revisão humana (a máquina sugere, você decide)

## Dica

Transforme cada nome numa lista de "tokens" limpos primeiro. Depois compare os tokens dois a dois com
`zip()`. Dois tokens combinam se forem iguais **ou** se um deles tiver uma letra só e for a inicial do
outro.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `"".join(c if c.isalnum() else " " for c in texto)` troca toda pontuação por espaço de uma vez.
- `all(pedaco_compativel(a, b) for a, b in zip(t1, t2))` exige que **todos** os pares combinem.
- O agrupamento usa `for ... else`: o `else` só roda quando o laço termina **sem** `break`, ou seja,
  quando nenhum grupo existente aceitou o nome, e aí ele inaugura um grupo novo.
- Resultado no caso: `Kaua T Brandao` (RDAP/WHOIS) cai no mesmo grupo de `Kauã Teixeira Brandão`;
  nenhuma vítima é agrupada com o suspeito; e "Tiago Lima Moreira × Tiago Silva Moreira" aparece para
  revisão (são pessoas diferentes, com o mesmo primeiro e último nome).

</details>
