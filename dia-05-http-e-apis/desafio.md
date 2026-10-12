# 🏆 Desafio S — Dia 5: Verificador de CEPs em lote

**Carta 47 · Rank S**

## A missão

As denúncias continuam chegando, e muitas trazem um "endereço de retirada" ou de "devolução" que o
vendedor passou pelo WhatsApp. A Iara quer conferir **todos de uma vez**, sem depender de uma única API.

Escreva um script que:

1. Receba uma lista de CEPs separados por vírgula (parâmetro `CEPS`), com ou sem hífen.
2. **Não consulte** o que não tem 8 dígitos (marque "formato inválido").
3. Pergunte primeiro à **BrasilAPI**; se ela falhar ou não achar, pergunte ao **ViaCEP** (fonte reserva).
4. Reconheça CEP inexistente nas **duas** formas: HTTP 404 (BrasilAPI) e `{"erro": "true"}` (ViaCEP).
5. Registre de **qual fonte** veio cada resposta.
6. Espere um pouco entre consultas (`PAUSA_SEGUNDOS`) para não levar um 429.
7. Grave `saidas/ceps_verificados.csv` com `;` e `utf-8-sig`.
8. Funcione **sem internet** com as amostras de `dados/`.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Um CEP com problema não derruba o lote
- [ ] O CEP `99999-999` sai como 🚩 inexistente, e `1234` sai como formato inválido sem consulta
- [ ] A coluna `fonte` mostra quando o ViaCEP salvou o dia

## Dica

Faça cada fonte virar uma função que devolve **duas coisas**: os dados (ou `None`) e uma situação
(`"ok"`, `"inexistente"`, `"falhou"`). Assim o laço principal fica curto e fácil de ler.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `"".join(ch for ch in bruto if ch.isdigit())` limpa o CEP antes de tudo.
- `str(d.get("erro", "")).lower() == "true"` cobre o texto `"true"` e o booleano `True`.
- As duas APIs usam nomes de campo diferentes; cada função já devolve tudo "traduzido" para
  `logradouro/bairro/cidade/uf`, e o CSV fica uniforme.

</details>
