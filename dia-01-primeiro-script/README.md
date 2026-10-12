# Dia 1 — O primeiro script

> 🃏 Cartas **1 · 22 · 43**  ·  📘 Original: *Day 1. Run the first script*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-01-primeiro-script/notebook.ipynb)

## 📖 Capítulo 1 — O primeiro alerta

<!-- historia:inicio -->
Terça-feira, 8h15. Você mal pendurou a mochila quando o telefone da mesa da Iara toca. Ela escuta,
anota, desliga.

— Era a Delegada Rita. As denúncias da MegaOferta não param de chegar. Trinta e sete até agora, de
onze cidades. Ela quer um briefing, e quer hoje.

Ela olha para você por cima dos óculos.

— E quem vai escrever é você. Em Python.

Você abre o editor que configurou ontem. O cursor pisca numa tela vazia. A Iara se inclina e digita
uma única linha: `print("Olá, NFA")`. Enter. As palavras aparecem no terminal.

— Pronto. Isso é um programa. Tudo o que você vai escrever nas próximas semanas é isso aqui, só que
maior. Agora coloca os números do caso em variáveis e faz o computador montar o texto. Se amanhã
chegarem mais dez denúncias, você muda **um número** e o relatório inteiro se atualiza.

— E a hora?

— Sempre com fuso. "Às duas da tarde" não serve para nada num inquérito. Duas da tarde **onde**?
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar o primeiro script do curso original.
- Usar `print()` com vários pedaços, `sep=` e `end=`.
- Montar textos com **f-strings** e formatar números (casas decimais, milhar, porcentagem).
- Pegar a data e a hora de **Brasília** com `zoneinfo`, com plano B se o fuso faltar.
- Escrever o primeiro briefing da Operação Vitrine Fantasma.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Um **script** é um arquivo de texto terminado em `.py`. Quando você roda `python arquivo.py`, o
**interpretador** lê o arquivo de cima para baixo e executa cada linha.

A função mais básica é o `print()`: ela mostra na tela o que estiver dentro dos parênteses. Texto vai
entre aspas (simples ou duplas, tanto faz). Para misturar texto e valores, use uma **f-string**:

```python
nome = "Iara"
print(f"Olá, {nome}!")          # Olá, Iara!
print(f"{54877.4:,.2f}")       # 54,877.40  (formato: milhar + 2 casas)
```

**Datas com fuso.** `datetime.now()` sozinho devolve a hora do relógio do computador, sem dizer de que
fuso ela é. No Google Colab, por exemplo, as máquinas rodam em **UTC** (3 horas à frente de Brasília).
Para registros de investigação, use `datetime.now(ZoneInfo("America/Sao_Paulo"))`: a hora sai certa e
o fuso fica gravado junto (`2026-10-12T09:03:11-03:00`).
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/start.py`](original/start.py) | Mostra a mensagem de boas-vindas do curso com um `print()` |

```bash
cd dia-01-primeiro-script
python original/start.py
```

O resultado deve ser `Welcome to 21 day Python course!`. O autor pede: **não siga para o Dia 2 antes
de ver essa mensagem**. Depois, troque o texto entre aspas e rode de novo.

Se der erro, confira `python --version` e `git --version` (no macOS/Linux, `python3 --version`).
Se você alterou o arquivo sem querer, apague a pasta e clone de novo, ou use o Colab.

> 💡 O autor recomenda um editor com destaque de sintaxe, como o **VS Code**. No Codespaces ele já vem
> pronto.

## 🇧🇷 Nível 2 — Camada Brasil

| Arquivo | O que faz |
|---|---|
| [`br/01_ola_nfa.py`](br/01_ola_nfa.py) | `print` com `sep`/`end`, f-strings, emojis e data/hora de Brasília com plano B |
| [`br/02_briefing_caso.py`](br/02_briefing_caso.py) | **O caso:** briefing de várias linhas com os números da operação guardados em variáveis |

```bash
cd dia-01-primeiro-script
python br/01_ola_nfa.py
python br/02_briefing_caso.py
```

Nenhum dos dois usa internet. Troque `MEU_NOME` e `ANALISTA` no topo (ou no formulário do Colab).

**O que você deve ver no caso:** 37 denúncias, 11 cidades, prejuízo de **R$ 54.877,40**, média de
R$ 1.483,17 por vítima e 49 dias entre a primeira e a última denúncia. Repare que o Python mostra
`54,877.40` (padrão americano) e que o fim do script ensina a converter para o padrão brasileiro.

## ⚖️ Ética, LGPD e OPSEC

- **Briefing é documento sensível.** Mesmo um resumo com números pode revelar a linha de investigação.
  Não cole briefing de caso real em grupo de mensagens pessoal nem em ferramenta online pública.
- **Minimização (LGPD, art. 6º, III).** Repare que o briefing não lista nome nem CPF de nenhuma vítima:
  para o objetivo dele (dar a dimensão do caso), números agregados bastam.
- **Carimbo de tempo com fuso.** Horário sem fuso é uma fonte clássica de contestação. Guarde a hora
  em ISO 8601 com o deslocamento (`-03:00`).
- **Valores de referência precisam de fonte.** O preço de referência no script é hipotético. Num
  relatório real, todo número precisa dizer de onde veio e quando foi coletado.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Boletim de plantão**: uma mensagem curta de fim de turno, com hora de
Brasília, dias desde a primeira denúncia e valores em `R$ 54.877,40`.

## 🔎 Inovação OSINT do dia

**O novo terminal interativo do Python.** Desde o Python **3.13**, digitar só `python` (ou `python3`)
abre um REPL renovado: edição de várias linhas, histórico navegável com as setas, cores no prompt e
nas mensagens de erro, e `exit` sem parênteses. Para OSINT isso é um bloco de rascunho: você cola um
pedaço de texto suspeito, testa uma formatação ou uma conta de datas em segundos e só depois leva
para o script. Atalhos úteis: **F1** abre a ajuda, **F2** mostra o histórico, **F3** entra no modo de
colar. Biblioteca necessária: nenhuma, já vem no Python.

## 📚 Para ir além

- Tutorial oficial do Python (em português): <https://docs.python.org/pt-br/3/tutorial/>
- f-strings e formatação de números: <https://docs.python.org/pt-br/3/library/string.html#formatspec>
- `zoneinfo`: <https://docs.python.org/pt-br/3/library/zoneinfo.html>
- O que há de novo no Python 3.13 (REPL novo): <https://docs.python.org/3/whatsnew/3.13.html>

## ✅ Checklist

- [ ] Rodei `original/start.py` e vi a mensagem de boas-vindas
- [ ] Troquei o texto do `print` e rodei de novo
- [ ] Rodei `br/01_ola_nfa.py` com o meu nome
- [ ] Rodei `br/02_briefing_caso.py` e entendi de onde vem cada número
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
