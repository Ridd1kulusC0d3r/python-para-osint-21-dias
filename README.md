# 🥋 PyJutsu — Python para OSINT em 21 dias (edição BR)

[![Baseado em cipher387/python-for-OSINT-21-days](https://img.shields.io/badge/baseado%20em-cipher387%2Fpython--for--OSINT--21--days-1f6f5c?logo=github)](https://github.com/cipher387/python-for-OSINT-21-days)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)](LICENSE)
[![Testes](https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias/actions/workflows/testes.yml/badge.svg)](https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias/actions/workflows/testes.yml)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-00-preparacao/notebook.ipynb)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Camada BR: só stdlib](https://img.shields.io/badge/camada%20BR-s%C3%B3%20stdlib-e0a400)

> Meu caderno de estudos do curso **[Python for OSINT. 21-day course for beginners](https://github.com/cipher387/python-for-OSINT-21-days)**,
> de **[cipher387 (Cyb_detective)](https://github.com/cipher387)**, refeito em português, com uma
> **camada Brasil somada a cada dia**, uma investigação fictícia do começo ao fim, notebooks prontos
> no Google Colab e código comentado linha a linha. Compartilhado para quem quiser estudar junto.

**Todo o crédito do curso original é do cipher387.** O código dele está nas pastas `original/`,
intacto, sob licença MIT. Se o curso te ajudar, [apoie o autor](https://boosty.to/cyb_detective)
e baixe o [PDF original](https://github.com/cipher387/python-for-OSINT-21-days/raw/main/Python%20for%20OSINT.%2021%20day%20course%20for%20beginners.pdf).
Veja [`CREDITS.md`](CREDITS.md).

---

## 🧭 Como funciona

Cada dia segue a **estrutura do curso original** e tem **três níveis**. Nada é substituído: o Brasil entra ao lado.

| Nível | O que é | Rank | Cartas |
|---|---|---|---|
| 🥋 **1 · Original** | O exercício do cipher387, intacto, com comentários em pt-BR | D / C | 1–21 |
| 🇧🇷 **2 · Camada Brasil** | Fontes brasileiras (registro.br, BrasilAPI, IBGE, Querido Diário…) **só com a biblioteca padrão** | B / A | 22–42 |
| 🏆 **3 · Desafio** | Um problema do caso para resolver sozinho, com gabarito escondido | S | 43–63 |

E tudo acontece dentro de uma história: a **[Operação Vitrine Fantasma](caso/README.md)**. Você chega ao
Núcleo de Fontes Abertas, em Belo Horizonte, e tem 21 dias para desmontar uma loja virtual falsa que
aplicou o golpe do PIX em 37 pessoas durante a Black Friday. Todos os dados do caso são **fictícios**.

## 🗓️ Os 21 dias

<!-- tabela-dias:inicio -->
| Dia | Tema | Capítulo do caso | Cartas | Notebook |
|---|---|---|---|---|
| **00** | [Preparação do ambiente](dia-00-preparacao/) | O recrutamento | — | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-00-preparacao/notebook.ipynb) |
| **01** | [O primeiro script](dia-01-primeiro-script/) | O primeiro alerta | 1<sub>D</sub> · 22<sub>B</sub> · 43<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-01-primeiro-script/notebook.ipynb) |
| **10** | [Scraping (raspagem de páginas)](dia-10-scraping/) | A vitrine congelada | 10<sub>D</sub> · 31<sub>B</sub> · 52<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-10-scraping/notebook.ipynb) |
| **11** | [Expressões regulares](dia-11-regex/) | A conversa | 11<sub>C</sub> · 32<sub>A</sub> · 53<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-11-regex/notebook.ipynb) |
| **12** | [Proxies, User-Agent e OPSEC](dia-12-proxies/) | Disfarce digital | 12<sub>C</sub> · 33<sub>A</sub> · 54<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-12-proxies/notebook.ipynb) |
| **13** | [Funções para trabalhar com listas](dia-13-listas/) | O mapa das vítimas | 13<sub>C</sub> · 34<sub>A</sub> · 55<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-13-listas/notebook.ipynb) |
| **14** | [Trabalhando com o sistema de arquivos](dia-14-sistema-de-arquivos/) | A sala de evidências | 14<sub>C</sub> · 35<sub>A</sub> · 56<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-14-sistema-de-arquivos/notebook.ipynb) |
| **15** | [Coleta de informações de domínio](dia-15-dominios/) | Quem registrou o domínio? | 15<sub>C</sub> · 36<sub>A</sub> · 57<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-15-dominios/notebook.ipynb) |
| **16** | [map() e funções para strings](dia-16-map-e-strings/) | Os muitos nomes de Kau | 16<sub>C</sub> · 37<sub>A</sub> · 58<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-16-map-e-strings/notebook.ipynb) |
| **17** | [Gerando documentos](dia-17-documentos/) | O relatório preliminar | 17<sub>C</sub> · 38<sub>A</sub> · 59<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-17-documentos/notebook.ipynb) |
| **18** | [Gerando gráficos e mapas](dia-18-graficos-e-mapas/) | Onde estão as vítimas | 18<sub>C</sub> · 39<sub>A</sub> · 60<sub>S</sub> | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-18-graficos-e-mapas/notebook.ipynb) |
<!-- tabela-dias:fim -->

## 🚀 Comece aqui

- **Sem instalar nada:** clique em *Abrir no Colab* no dia que quiser e rode a primeira célula.
- **No seu computador:** siga o [`COMECE-AQUI.md`](COMECE-AQUI.md) (Windows, macOS e Linux).
- **No navegador, com terminal:** *Code → Codespaces → Create codespace on main* (é o que o próprio autor recomenda hoje).

```bash
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias/dia-15-dominios
python br/01_rdap_br.py                     # exercício BR (só stdlib)
OSINT_OFFLINE=1 python br/01_rdap_br.py     # mesmo exercício sem internet
```

## 📁 Estrutura

```
python-para-osint-21-dias/
├── dia-00-preparacao/ … dia-21-ferramentas-de-codigo/
│   ├── README.md            capítulo da história + guia do dia
│   ├── notebook.ipynb       pronto para o Colab
│   ├── original/            código do cipher387 (MIT), comentado
│   ├── br/                  camada Brasil, só stdlib
│   ├── dados/               amostras para estudar sem internet
│   └── desafio.md           nível 3 (rank S)
├── caso/                    a Operação Vitrine Fantasma (história + dados fictícios)
├── cartas/                  as 63 cartas em SVG
├── docs/                    site do curso (GitHub Pages)
└── ferramentas/             geradores de notebooks, cartas, site e testes
```

## 📚 Materiais de apoio

| | |
|---|---|
| [`COMECE-AQUI.md`](COMECE-AQUI.md) | Instalação passo a passo e primeiro script |
| [`caso/README.md`](caso/README.md) | A história, os personagens e os 21 capítulos |
| [`CARTAS.md`](CARTAS.md) | As 63 cartas do Formato Jutsu |
| [`ETICA.md`](ETICA.md) | LGPD, limites legais e OPSEC para OSINT no Brasil |
| [`GLOSSARIO.md`](GLOSSARIO.md) | Termos de Python e de OSINT, explicados sem jargão |
| [`ATUALIZACOES-2026.md`](ATUALIZACOES-2026.md) | O que mudou desde 2023 nas bibliotecas e serviços do curso |
| [`DIARIO.md`](DIARIO.md) | Modelo de diário de bordo para registrar seu progresso |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Padrão de cada dia e como contribuir |

## 🤝 Estude junto

- Terminou um dia? Abra uma issue **[🥋 Entreguei o dia](https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias/issues/new?template=entreguei-o-dia.yml)**.
- Achou uma fonte BR nova ou um jeito melhor? Pull requests são bem-vindos (veja o [`CONTRIBUTING.md`](CONTRIBUTING.md)).
- Algum exercício quebrou? Abra **[🔧 Um exercício quebrou](https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias/issues/new?template=api-quebrou.yml)**. Toda segunda-feira um teste automático roda todos os exercícios ao vivo e avisa quando alguma API muda.

## ⚖️ Uso responsável

OSINT é coleta de informação **pública**, com **finalidade legítima**. Este material é para estudo, investigação
autorizada e defesa. Nada aqui ensina a invadir sistemas, burlar autenticação ou usar dados vazados.
Leia o [`ETICA.md`](ETICA.md) antes do Dia 1.

## 📜 Licença e créditos

- Código original: © 2023 Cyb_detective ([cipher387](https://github.com/cipher387)), [MIT](https://github.com/cipher387/python-for-OSINT-21-days/blob/main/LICENSE).
- Adaptação, camada Brasil, narrativa, notebooks e cartas: © 2026 Deivison Lourenço ([Ridd1kulusC0d3r](https://github.com/Ridd1kulusC0d3r)), MIT.
- Os textos deste repositório foram escritos do zero em pt-BR; não são tradução do PDF original.
