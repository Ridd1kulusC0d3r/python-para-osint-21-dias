# 🏆 Desafio S — Dia 9: Vigia do Diário Oficial

**Carta 51 · Rank S**

## A missão

A Iara não quer olhar o Diário Oficial todo dia à mão. Ela quer um **vigia**: um script que roda de
manhã, consulta o Querido Diário e mostra **só o que é novo** desde a última vez. Se a prefeitura
publicar um alerta sobre lojas falsas, uma sanção a uma empresa ou um termo novo ligado ao caso, o NFA
fica sabendo no mesmo dia.

Escreva um script que:

1. Receba uma lista de termos (`TERMOS`) e um código IBGE de município (`CODIGO_IBGE`).
2. Consulte o Querido Diário para cada termo, nos últimos `DIAS_PARA_TRAS` dias, com pausa entre pedidos.
3. Guarde em `saidas/vigia_estado.json` o que já foi visto (uma "impressão digital" por diário + termo).
4. Na execução seguinte, mostre **apenas as publicações novas**.
5. Gere `saidas/vigia_novidades.html` com data, termo, trecho e link (tudo com `html.escape`).
6. Funcione **sem internet** com a amostra de `dados/`.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Rodando duas vezes seguidas, a segunda mostra **zero** novidades
- [ ] Se o arquivo de estado estiver apagado ou corrompido, o script recomeça sem quebrar
- [ ] O HTML abre no navegador e nenhum trecho "quebra" a página

## Dica

Um `set` de textos (`f"{url}|{termo}"`) responde "já vi isso?" instantaneamente. Para salvar em JSON,
converta para lista ordenada (`sorted(vistos)`), como no Dia 6.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `try: ... except (FileNotFoundError, KeyError, json.JSONDecodeError)` cobre "primeira vez" e
  "estado estragado" com o mesmo tratamento: começar do zero.
- `published_since` é calculado a partir de hoje com `timedelta(days=DIAS_PARA_TRAS)`.
- Para agendar de verdade: `cron` no Linux/macOS ou o Agendador de Tarefas no Windows.

</details>
