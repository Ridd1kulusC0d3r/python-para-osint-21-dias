# 🔧 O que mudou desde 2023

O curso original foi escrito em 2023. Ferramentas mudam, serviços fecham, bibliotecas trocam de nome.
**Regra do repositório:** o código original nunca é corrigido. Quando algo quebrou, a versão
atualizada fica **ao lado**, num arquivo `original/2026_<nome>.py`.

Manter esta lista também é uma lição de OSINT: toda ferramenta tem prazo de validade, e quem sabe
programar consegue consertar a própria caixa de ferramentas.

## Ambiente

| O quê | Em 2023 | Em 2026 | Onde |
|---|---|---|---|
| Ambiente online do curso | Gitpod, com 50 h grátis por mês | Deixou de ser gratuito. O próprio autor recomenda **GitHub Codespaces**; aqui também há **Google Colab** | [Dia 0](dia-00-preparacao/) |
| UTF-8 por padrão | Dependia do sistema (Windows usava cp1252) | O Python 3.15 passou a usar UTF-8 por padrão (PEP 686). Mesmo assim, o curso sempre passa `encoding="utf-8"` | [Dia 0](dia-00-preparacao/), [Dia 4](dia-04-arquivos/) |

## Bibliotecas e serviços dos exercícios originais

| Dia | Arquivo original | O que aconteceu | Versão 2026 |
|---|---|---|---|
| 3 | `launch.py` | O Blackbird mudou bastante, mas `-u/--username` continua funcionando. O Thorndyke, citado no PDF, foi arquivado | Não precisou |
| 9 | `ddg_search*.py` | O pacote `duckduckgo_search` removeu a função `ddg()` e virou **`ddgs`**: `from ddgs import DDGS; DDGS().text(...)` | [`2026_ddg_search.py`](dia-09-resultados-de-busca/original/2026_ddg_search.py), [`2026_ddg_search_to_csv.py`](dia-09-resultados-de-busca/original/2026_ddg_search_to_csv.py), [`2026_ddg_search_download_pdf.py`](dia-09-resultados-de-busca/original/2026_ddg_search_download_pdf.py) |
| 12 | `simple_proxy.py`, `proxy_permulation.py` | Os IPs de proxy do exemplo não respondem mais (proxies públicos duram horas). O código continua didático | Não precisou; veja os alertas de OPSEC do dia |
| 15 | `whois_info.py` | A ICANN encerrou a obrigação de WHOIS para gTLDs em jan/2025; o **RDAP** virou o padrão. No `.br`, os dois funcionam | Camada BR com RDAP + WHOIS ([Dia 15](dia-15-dominios/)) |
| 17 | `create_pdf.py` | O `fpdf` antigo foi substituído pelo **`fpdf2`** (mesmo `from fpdf import FPDF`). `txt=` virou `text=` (2.7.6) e `ln=` está obsoleto. O original roda, só com aviso | [`2026_create_pdf.py`](dia-17-documentos/original/2026_create_pdf.py) |
| 18 | `map.py` | O Basemap ainda instala e funciona, mas a documentação dele aponta o **Cartopy** como sucessor. É alternativa, não conserto | [`2026_map.py`](dia-18-graficos-e-mapas/original/2026_map.py) (folium) |
| 21 | — | O PDF recomenda ChatGPT, Stack Overflow e Phind. Hoje há muitos assistentes de IA; o conselho do autor continua valendo: **eles erram muito**, então entenda o código | [Dia 21](dia-21-ferramentas-de-codigo/) |

## Detalhes do código original que vale conhecer

Nada disso foi alterado no original. Está apontado nos comentários `# 💬`:

- **Dia 7 / `json_to_csv.py`:** `len(...) - 1` com `range()` pula o último item.
- **Dia 11 / `extract_emails.py`:** dentro de `[a-zA-Z0-9-_.]`, o trecho `9-_` vira um intervalo de caracteres.
- **Dia 14 / `check_re_files_contents.py`:** imprime "Math" onde queria dizer "Match".
- **Dia 17 / `create_xlsx.py`:** a fórmula `=average(B1:B4)` deixa o último funcionário de fora da média.

## Como avisar que algo quebrou

Toda segunda-feira o [teste automático](.github/workflows/testes.yml) roda todos os exercícios ao vivo
e confere se `original/` continua idêntico ao repositório do cipher387. Se algo mudar, ele abre uma issue.
Você também pode abrir uma: [🔧 Um exercício quebrou](https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias/issues/new?template=api-quebrou.yml).
