# Como contribuir (e o padrão de cada dia)

Este repositório é um **caderno de estudos compartilhado**. Toda contribuição segue duas regras de ouro:

1. **Somar, nunca substituir.** O exercício original do cipher387 continua lá, intacto. A camada
   Brasil entra **ao lado**, mesmo que o dia fique com dois (ou mais) exercícios.
2. **Simples primeiro.** Os exercícios BR usam **só a biblioteca padrão do Python** e são comentados
   como se o leitor nunca tivesse programado.

## Estrutura de um dia

```
dia-15-dominios/
├── README.md            ← capítulo da história + conceito + guia dos exercícios
├── dia.json             ← metadados: cartas, quiz, bibliotecas do original
├── original/            ← código do cipher387 (MIT) com cabeçalho de atribuição
│   └── whois_info.py
├── br/                  ← camada Brasil (stdlib), numerada na ordem de estudo
│   ├── 01_rdap_br.py
│   └── 02_whois_porta43.py
├── dados/               ← amostras offline (o exercício roda mesmo sem internet)
├── desafio.md           ← nível 3 (rank S), gabarito em <details>
├── desafio_gabarito.py  ← o mesmo gabarito, em código executável
└── notebook.ipynb       ← GERADO por ferramentas/construir_notebooks.py (não edite à mão)
```

## Os três níveis (e as 63 cartas)

| Nível | O quê | Rank | Carta |
|---|---|---|---|
| 1 | Exercício **original** do cipher387 | D (dias 1–10) · C (11–21) | nº do dia (1–21) |
| 2 | Exercício **BR** | B (dias 1–10) · A (11–21) | dia + 21 (22–42) |
| 3 | **Desafio** | S | dia + 42 (43–63) |

## Arquivos `original/`

* Cópia **exata** do arquivo do repositório do cipher387. Nenhuma linha de código é alterada.
* No topo, o cabeçalho abaixo. No meio, comentários explicativos começando com `# 💬`.
* Se o código original quebrou com o tempo (biblioteca mudou, serviço saiu do ar), **não conserte o
  original**: crie ao lado um `2026_<nome>.py` com a versão atualizada e registre em
  [`ATUALIZACOES-2026.md`](ATUALIZACOES-2026.md).

```python
# ──────────────────────────────────────────────────────────────────────────
# Título: Consulta WHOIS de um domínio
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_15/whois_info.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
```

## Arquivos `br/`

* Só **biblioteca padrão**. Nada de `pip install`.
* Docstring no topo: primeira linha = título; depois "Carta", "O que você aprende", "Como rodar".
* Comentário explicando **cada bloco** (e cada linha nova para iniciante).
* Parâmetros no topo com `#@param` (vira formulário no Colab):
  `DOMINIO = "registro.br"  #@param {type:"string"}`
* Sem `input()` (o teste automático precisa rodar sozinho). Use os parâmetros do topo.
* Arquivos gerados vão para `PASTA_DIA / "saidas"` (a pasta `saidas/` é ignorada pelo git).
* Se consulta a internet, **tem amostra offline** em `dados/` e usa o padrão abaixo. A mensagem
  `⚠️ MODO OFFLINE` é exatamente essa: o teste semanal procura por ela para saber se uma API quebrou.
* Precisa rodar **sem erro** com `OSINT_OFFLINE=1 python br/arquivo.py` a partir da pasta do dia.

```python
import json
import os
import urllib.request
from pathlib import Path

# Pasta do dia: funciona como script (python br/x.py) e como célula no Colab.
PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                return json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))
```

## `dia.json`

```json
{
  "dia": 15,
  "slug": "dia-15-dominios",
  "titulo": "Coleta de informações de domínio",
  "titulo_original": "Day 15. Domain information gathering",
  "capitulo": "Quem registrou o domínio?",
  "pip_original": ["dnspython", "python-whois"],
  "cartas": [
    {"numero": 15, "nivel": 1, "rank": "C", "nome": "…", "efeito": "até 140 caracteres", "arquivo": "original/whois_info.py"},
    {"numero": 36, "nivel": 2, "rank": "A", "nome": "…", "efeito": "…", "arquivo": "br/01_rdap_br.py"},
    {"numero": 57, "nivel": 3, "rank": "S", "nome": "…", "efeito": "…", "arquivo": "desafio.md"}
  ],
  "quiz": [
    {"pergunta": "…", "opcoes": ["…", "…", "…", "…"], "correta": 1, "explicacao": "…"}
  ],
  "inovacao": {"titulo": "…", "resumo": "…"}
}
```

`correta` é o índice (começando em 0) da opção certa. Três perguntas por dia.

## `README.md` de cada dia

Seções, nesta ordem. Os marcadores HTML são lidos pelo gerador de notebooks.

```markdown
# Dia 15 — Coleta de informações de domínio
> 🃏 Cartas 15 · 36 · 57  ·  📘 Original: *Day 15. Domain information gathering*
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-15-dominios/notebook.ipynb)

## 📖 Capítulo 15 — Quem registrou o domínio?
<!-- historia:inicio -->
(cena curta, 120–220 palavras, em 2ª pessoa, com Iara Campos)
<!-- historia:fim -->

## 🎯 Objetivos
## 🧠 Conceito em 2 minutos
<!-- conceito:inicio -->
<!-- conceito:fim -->
## 🥋 Nível 1 — Exercício original (cipher387)
## 🇧🇷 Nível 2 — Camada Brasil
## ⚖️ Ética, LGPD e OPSEC
## 🏆 Nível 3 — Desafio S
## 🔎 Inovação OSINT do dia
## 📚 Para ir além
## ✅ Checklist
```

## Dados

* Dados do caso: só os de [`caso/dados/`](caso/dados) (fictícios). Para alvos ao vivo, use apenas
  alvos institucionais públicos (`registro.br`, `gov.br`, o CNPJ de uma estatal etc.).
* Amostras de API em `dados/` levam o campo `"_aviso": "AMOSTRA ilustrativa…"` quando forem JSON.

## Antes do pull request

```bash
python ferramentas/smoke_test.py --offline     # todos os exercícios BR rodam sem internet
python ferramentas/construir_notebooks.py      # regenera os notebooks
python ferramentas/gerar_cartas.py             # regenera as cartas
```
