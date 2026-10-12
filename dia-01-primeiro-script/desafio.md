# 🏆 Desafio S — Dia 1: Boletim de plantão

**Carta 43 · Rank S**

## A missão

Todo fim de turno, a Iara cola no grupo da equipe um **boletim curto** do caso. Ela cansou de digitar.
Escreva um script que monte esse boletim sozinho:

1. Parâmetros no topo: `ANALISTA`, `TOTAL_DENUNCIAS` (37), `PREJUIZO_TOTAL` (54877.40) e
   `PRIMEIRA_DENUNCIA` ("2025-10-12").
2. Primeira linha com **data e hora de Brasília** (`America/Sao_Paulo`, com plano B se o fuso faltar).
3. O prejuízo em **formato brasileiro**: `R$ 54.877,40` (e não `54,877.40`).
4. A **média por vítima**, também em formato brasileiro.
5. Quantos **dias se passaram** desde a primeira denúncia até hoje.
6. Imprima o boletim e, embaixo, quantos caracteres ele tem.

## Critérios de rank S

- [ ] Só biblioteca padrão, sem `input()`
- [ ] Hora com fuso (nada de `datetime.now()` "pelado")
- [ ] Dinheiro com ponto no milhar e vírgula no decimal
- [ ] Trocar um parâmetro atualiza o boletim inteiro

## Dica

Subtrair duas datas (`date`) dá um intervalo (`timedelta`). O atributo `.days` diz quantos dias ele tem.
Para o dinheiro: formate com `:,.2f` e depois troque `,` e `.` de lugar usando um caractere "coringa"
no meio do caminho (se trocar direto, um apaga o outro!).

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `(agora.date() - date.fromisoformat(PRIMEIRA_DENUNCIA)).days` dá os dias desde a primeira denúncia.
- `f"{valor:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")` vira formato brasileiro.
- Um texto com aspas triplas e f-string mantém o boletim legível no código.

</details>
