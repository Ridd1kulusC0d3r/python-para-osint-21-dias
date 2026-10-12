# 🏆 Desafio S — Dia 3: Lote de buscas com registro

**Carta 45 · Rank S**

## A missão

O vendedor assina "Kau" e usa o apelido **`kau.ofertas`**. Golpista troca de conta, mas costuma repetir o
apelido com pequenas variações: `kau_ofertas`, `kau-ofertas`, `kauofertas`...

A Iara quer um **lote**: um script que gera as variantes, monta o comando da ferramenta de campo para
cada uma e **registra tudo**. Mas ela impõe uma regra:

> "O apelido do caso é inventado, só que pode existir de verdade, como conta de um desconhecido. Então
> para ele a gente **só simula**. Para provar que o lote funciona, roda de verdade num alvo de treino
> público: `cipher387`."

Escreva um script que:

1. Gere as variantes de `APELIDO_DO_CASO` trocando o separador por `.`, `_`, `-` e nenhum.
2. Para cada variante, monte o comando `br/03_mini_blackbird.py --username <variante>` e **só registre**
   (modo simulação).
3. Para `ALVO_DE_TREINO`, rode o comando de verdade com `subprocess.run` (lista, **sem** `shell=True`)
   e capture o resultado de cada site.
4. Grave `saidas/lote_buscas.csv` (separador `;`, `utf-8-sig`) com data/hora de Brasília, username,
   modo, código de retorno e resultado.
5. Acrescente (modo `"a"`) uma linha por comando em `saidas/log_lote.txt`.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Comando como lista e `sys.executable` (nada de `"python ..."` com `shell=True`)
- [ ] Nenhuma consulta real ao apelido do caso
- [ ] O log cresce a cada execução, sem apagar o anterior
- [ ] Roda com `OSINT_OFFLINE=1`

## Dica

Um `set` elimina variantes repetidas: `{sep.join(partes) for sep in (".", "_", "-", "")}`.
E o processo filho herda as variáveis de ambiente: se você rodar com `OSINT_OFFLINE=1`, o
mini-blackbird também entra no modo offline sozinho.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- A função `rodar()` usa `[sys.executable, str(FERRAMENTA), "--username", username]`: o mesmo Python, sem shell.
- Separar "simulação" de "execução" é uma decisão **ética**, não técnica: o código é o mesmo.
- O CSV guarda o que foi feito e **quando**; o log em modo `"a"` vira o histórico do analista.

</details>
