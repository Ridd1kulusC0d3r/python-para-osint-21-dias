# Dia 19 — Wayback Machine e funções de data e hora

> 🃏 Cartas **19 · 40 · 61**  ·  📘 Original: *Day 19. Wayback Machine and time/date functions*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-19-wayback-e-datas/notebook.ipynb)

## 📖 Capítulo 19 — O site que sumiu

<!-- historia:inicio -->
— Clica no link da loja — pede a Iara.

Você clica. **404.** A MegaOferta Brasil não existe mais.

— Era isso que ele queria — ela diz, sem surpresa. — Site falso tem prazo de validade. Some antes da
primeira intimação. Só que a internet tem memória.

Ela abre o site do Internet Archive e digita o domínio. Aparece uma régua do tempo com bolinhas
azuis: cinco capturas, entre outubro e dezembro.

— Cada bolinha é uma foto do site num momento. Mas olhar uma por uma no navegador não é análise. A
API devolve a lista inteira em JSON: data, status, tamanho da página. E o **tamanho** fala. Uma
vitrine cheia de produtos pesa seis mil bytes; um aviso de "em manutenção" pesa oitocentos.

Ela pega o calendário de mesa e circula uma data em novembro.

— Agora o mais importante: **datas**. Junta o nascimento do domínio, as capturas e as denúncias numa
linha só. E me diz uma coisa: em que dia caiu a Black Friday do ano passado? Aposto que as
denúncias se amontoam em volta dela.
<!-- historia:fim -->

## 🎯 Objetivos

- Baixar cópias antigas de um site com o pacote `wayback`, como no curso original.
- Consultar a **API CDX** da Wayback Machine só com a biblioteca padrão.
- Converter timestamps `AAAAMMDDhhmmss` e Unix em datas com fuso.
- Trabalhar com `America/Sao_Paulo`, `dd/mm/aaaa` e dias da semana em português sem `locale`.
- Montar a linha do tempo do caso e calcular a Black Friday com `calendar`.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
A **Wayback Machine** (Internet Archive) guarda "fotos" de páginas web ao longo do tempo. Cada foto
é um **memento**. Para saber quais existem, pergunte ao índice **CDX**:

```
https://web.archive.org/cdx/search/cdx?url=gov.br&output=json&limit=5
```

A resposta é uma lista de listas, e a **primeira linha é o cabeçalho**:
`urlkey, timestamp, original, mimetype, statuscode, digest, length`.
O `timestamp` (`20251128233001`) está sempre em **UTC**. O `digest` é a impressão digital do
conteúdo: muda quando a página muda. Para abrir a cópia: `https://web.archive.org/web/<timestamp>/<url>`.

**Datas em Python** têm uma pegadinha: um `datetime` pode ser **ingênuo** (sem fuso, "hora do
relógio de alguém") ou **consciente** (com fuso). Evidência sempre com fuso:

| Precisa de | Use |
|---|---|
| Fuso de Brasília | `ZoneInfo("America/Sao_Paulo")` (no Windows, `pip install tzdata` ou -03:00 fixo) |
| Texto → data | `datetime.strptime("28/11/2025", "%d/%m/%Y")` |
| Data → texto | `f"{d:%d/%m/%Y}"` ou `d.strftime(...)` |
| Somar dias | `d + timedelta(days=30)` |
| Unix → data | `datetime.fromtimestamp(1764375240, FUSO)` |

O Brasil **não tem mais horário de verão desde 2019**, mas datas antigas ainda estão em -02:00 nos
meses de verão. O `ZoneInfo` sabe disso; o fuso fixo, não.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/date_time.py`](original/date_time.py) | Data e hora atuais, ano, mês e data por extenso com `strftime` |
| [`original/download_mementos.py`](original/download_mementos.py) | Baixa para arquivos `.html` as cópias de `nasa.gov` feitas antes de 1999 (pacote `wayback`) |

```bash
pip install wayback
cd dia-19-wayback-e-datas/original
python date_time.py
python download_mementos.py     # demora; grava vários .html na pasta atual
```

> 💡 No `date_time.py`, `%A %d %B %Y` sai em inglês ("Monday 12 October 2026"). O `br/01` mostra como
> ter "segunda-feira, 12 de outubro de 2026" em qualquer computador.

> ⚠️ O `download_mementos.py` usa `open(fileName, "a")`: rodar duas vezes **acrescenta** o HTML de
> novo no mesmo arquivo. E, no Windows, sem `encoding="utf-8"` pode dar erro de acento.

## 🇧🇷 Nível 2 — Camada Brasil

Só **biblioteca padrão**. O script 02 consulta a API ao vivo e tem amostra offline; o 03 é 100%
offline (dados do caso).

| Arquivo | O que faz |
|---|---|
| [`br/01_datas_br.py`](br/01_datas_br.py) | Fuso America/Sao_Paulo com plano B, strptime/strftime, timestamp Unix, timedelta, dias da semana em português e o horário de verão de 2018 |
| [`br/02_wayback_cdx.py`](br/02_wayback_cdx.py) | API CDX para uma página `.gov.br`: cabeçalho, conversão de timestamp, capturas por ano, status, digests e links das cópias |
| [`br/03_linha_do_tempo_caso.py`](br/03_linha_do_tempo_caso.py) | **O caso:** RDAP + Wayback + denúncias numa linha do tempo; queda do `length`; 404 final; Black Friday com `calendar` |

```bash
cd dia-19-wayback-e-datas
python br/02_wayback_cdx.py
python br/03_linha_do_tempo_caso.py
```

**O que você deve ver no caso:** domínio registrado em 02/10/2025; primeira vítima 10 dias depois;
Black Friday em **28/11/2025**; **12 das 37 denúncias (32%)** entre 25/11 e 01/12, mais que o dobro
da média diária; em 01/12 a página encolhe 86% ("manutenção"); em 05/12, 404.

## ⚖️ Ética, LGPD e OPSEC

- **O arquivo também guarda dados pessoais.** Páginas antigas podem mostrar telefone, e-mail ou foto
  de alguém que depois os apagou de propósito. Use só o necessário para a finalidade e não
  republique; o direito de apagar não some só porque existe uma cópia.
- **Consultar a Wayback não alerta o alvo**: a requisição vai para o Internet Archive, não para o site
  do suspeito. Já abrir o site vivo deixa o seu IP nos logs dele.
- **Capture antes que suma.** Num golpe ativo, peça a captura (Save Page Now) e salve você também uma
  cópia com hash (Dia 14) e data/hora com fuso. A Wayback pode não ter a página que você precisa.
- **Captura é indício, não certidão.** Para uso em processo, registre a URL do memento, o timestamp,
  o hash do conteúdo baixado e como você o obteve. Algumas páginas são capturadas incompletas
  (sem imagens ou sem JavaScript).
- Respeite os limites da API: nada de laço sem pausa baixando milhares de mementos.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Que vitrine a vítima viu?**: para cada denúncia, achar a captura mais
recente antes da compra (com `bisect`) e medir as lacunas sem prova.

## 🔎 Inovação OSINT do dia

**Um índice só para vários arquivos: `cdx_toolkit`.** A biblioteca `cdx_toolkit`
(`pip install cdx_toolkit`) consulta com a mesma interface o CDX da **Wayback Machine** e o do
**Common Crawl**, um rastreamento público da web feito várias vezes por ano. Quando a Wayback não
tem a página, o Common Crawl às vezes tem. E não depender de uma única fonte é lição aprendida: em
outubro de 2024 o Internet Archive sofreu ataques de negação de serviço e um vazamento de dados de
cerca de 31 milhões de contas, e ficou fora do ar por dias. Para OSINT, a regra fica: consulte mais de um arquivo e **guarde a sua cópia**.

## 📚 Para ir além

- Documentação da API CDX (servidor pywb/Wayback): <https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server>
- Pacote `wayback` (EDGI): <https://wayback.readthedocs.io/>
- `datetime` e `zoneinfo`: <https://docs.python.org/pt-br/3/library/datetime.html> · <https://docs.python.org/pt-br/3/library/zoneinfo.html>
- `calendar`: <https://docs.python.org/pt-br/3/library/calendar.html>
- cdx_toolkit: <https://github.com/commoncrawl/cdx_toolkit>
- Save Page Now (capturar uma página agora): <https://web.archive.org/save>

## ✅ Checklist

- [ ] Rodei `date_time.py` e `download_mementos.py`
- [ ] Converti um timestamp CDX e um timestamp Unix em data de Brasília
- [ ] Vi o deslocamento -02:00 de dezembro de 2018
- [ ] Consultei a API CDX de uma página `.gov.br`
- [ ] Montei a linha do tempo do caso e achei a Black Friday
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
