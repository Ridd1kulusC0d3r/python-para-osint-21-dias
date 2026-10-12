# Dia 9 — Automatizar a coleta de resultados de busca

> 🃏 Cartas **9 · 30 · 51**  ·  📘 Original: *Day 9. Automate the collection of search results*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-09-resultados-de-busca/notebook.ipynb)

## 📖 Capítulo 9 — Rastros na busca

<!-- historia:inicio -->
Sexta-feira, 8h20. Na parede do NFA, um fio vermelho agora liga três nomes de titulares a um único
post-it: **painel_dump.sql**. A Iara fica um tempo olhando para ele, depois vira a cadeira.

— Sabemos quem perdeu e quem recebeu. Agora: **o que o mundo já sabe sobre essa loja?** Golpe assim
não nasce do nada. Alguém reclamou num fórum, alguém postou o CNPJ falso num grupo, alguém usou o
mesmo apelido em outro golpe.

Você abre o navegador, mas ela fecha a aba com um gesto.

— Buscar à mão a gente faz uma vez. Investigação séria repete a mesma busca todo dia, em vários
lugares, e guarda **o que viu e quando viu**. Para isso servem os scripts. Mas cuidado: raspar o
Google é pedir para ser bloqueado e ainda quebra os termos de uso. Você vai montar as buscas, e quem
clica é você.

Ela escreve no quadro: **Querido Diário**.

— E tem uma fonte que quase ninguém lembra: o Diário Oficial. Prefeitura publica alerta ao
consumidor, contrato, sanção, empresa impedida de licitar. Se esse CNPJ falso ou esse sobrenome
aparecer lá, quero saber antes da Delegada Rita perguntar.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar a coleta de resultados de busca do original e entender por que ela precisou de atualização.
- Usar a versão 2026 com o pacote `ddgs` (`DDGS().text()`).
- Consultar os **Diários Oficiais municipais** pela API do **Querido Diário**.
- Salvar resultados de busca em CSV com a data e a hora da coleta.
- Dominar os **operadores de busca** (dorks) e gerar links clicáveis para vários buscadores.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Buscadores entendem **operadores** que refinam a busca. Saber combiná-los é uma das habilidades mais
valiosas em OSINT:

| Operador | Exemplo | Significa |
|---|---|---|
| `"…"` | `"kau.ofertas"` | exatamente esta sequência |
| `site:` | `site:gov.br` | só páginas deste domínio (e subdomínios) |
| `filetype:` | `filetype:pdf` | só arquivos deste tipo |
| `intext:` / `intitle:` | `intitle:"golpe"` | o termo no texto / no título |
| `-` | `-site:exemplo.com` | exclui |
| `OR` | `golpe OR fraude` | um ou outro |

Existem dois jeitos de automatizar: **(1)** bibliotecas que conversam com o buscador por você (como a
`ddgs`, usada pelo autor), práticas mas frágeis, porque o buscador muda e pode bloquear; e **(2)**
**APIs oficiais** de fontes específicas, como o **Querido Diário**, que existem justamente para serem
consultadas por programas. Quando houver API, prefira a API.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/ddg_search.py`](original/ddg_search.py) | Busca "osint" no DuckDuckGo com `ddg()` e imprime os resultados |
| [`original/ddg_search_to_csv.py`](original/ddg_search_to_csv.py) | Salva título, resumo e link em `search_results.csv` |
| [`original/ddg_search_download_pdf.py`](original/ddg_search_download_pdf.py) | Busca com `filetype:pdf` e baixa os arquivos (`download=True`) |

> ⚠️ **Os três originais não rodam mais.** A função `ddg()` do pacote `duckduckgo_search` foi removida,
> e o projeto passou a se chamar **`ddgs`**. Os originais ficam intactos (é a regra); ao lado, estão as
> versões atualizadas:

| Versão 2026 | O que mudou |
|---|---|
| [`original/2026_ddg_search.py`](original/2026_ddg_search.py) | `DDGS().text(..., timelimit="y", max_results=10)` |
| [`original/2026_ddg_search_to_csv.py`](original/2026_ddg_search_to_csv.py) | idem + `newline=""` e `encoding="utf-8"` no CSV |
| [`original/2026_ddg_search_download_pdf.py`](original/2026_ddg_search_download_pdf.py) | busca com `ddgs` e download de cada PDF com `urllib` |

```bash
pip install ddgs
cd dia-09-resultados-de-busca/original
python 2026_ddg_search.py
python 2026_ddg_search_to_csv.py
```

> 💡 Bibliotecas que conversam com buscadores mudam com frequência. Se o `ddgs` reclamar, atualize
> (`pip install -U ddgs`) e confira o README do projeto. O autor também lista alternativas: `ddgr`
> (DuckDuckGo no terminal), `Search-Engines-Scraper` e outras. E a dica dele vale para quase todo
> pacote: digite `--help` (ou `-h`) depois do nome de um comando para ver como usá-lo.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Amostra offline do Querido Diário em `dados/`.

| Arquivo | O que faz |
|---|---|
| [`br/01_querido_diario.py`](br/01_querido_diario.py) | Busca um termo nos Diários Oficiais de um município (padrão: "PIX" em BH, código IBGE 3106200) |
| [`br/02_querido_diario_csv.py`](br/02_querido_diario_csv.py) | Vários termos × vários municípios, com pausa, sem duplicatas, num CSV com data da coleta |
| [`br/03_dorks_br.py`](br/03_dorks_br.py) | Monta dorks (treino em `gov.br` e do caso) para Google, DuckDuckGo e Bing e grava `saidas/dorks.html` |

```bash
cd dia-09-resultados-de-busca
python br/01_querido_diario.py
OSINT_OFFLINE=1 python br/02_querido_diario_csv.py     # força o modo offline
python br/03_dorks_br.py                               # depois abra saidas/dorks.html
```

**O que você deve ver no caso:** o domínio, o apelido e o CNPJ do caso são **fictícios**, então as
dorks do caso devem voltar vazias (e isso é bom: prova que você não está mexendo em gente real). As
dorks de treino, em `gov.br`, mostram os operadores funcionando. A amostra do Querido Diário tem
trechos **inventados**, marcados como "(TRECHO FICTÍCIO)": com internet, você vê publicações reais.

> 🧭 **Querido Diário, na prática:** os campos que importam são `total_gazettes` (quantos diários
> batem com a busca) e `gazettes`, uma lista com `date`, `territory_name`, `url` (o PDF original) e
> `excerpts` (trechos onde o termo aparece). Nem todo município está coberto; confira a lista no site.

## ⚖️ Ética, LGPD e OPSEC

- **Não raspe buscadores.** Os termos de uso do Google e do Bing proíbem consultas automatizadas fora
  das APIs oficiais. Além de bloqueio e captcha, você "suja" o IP da sua organização. Gerar os links e
  clicar é legítimo; robô metralhando o buscador, não.
- **Dork é lupa, não pé de cabra.** Achar um arquivo exposto não autoriza baixá-lo, ainda mais se tiver
  dados pessoais (reveja o Dia 8). Use dorks para entender exposição e para achar fontes públicas.
- **Suas buscas contam uma história.** O buscador registra o que você procura, logado ou não. Buscar o
  nome de um suspeito na sua conta pessoal mistura sua identidade com a investigação. Use o ambiente
  de trabalho e a conta institucional (mais no Dia 12).
- **Registre data e hora da coleta.** Resultado de busca muda todo dia. O que não foi registrado
  (URL + data/hora + captura) não existe para o relatório.
- **Diário Oficial é público, mas a finalidade importa.** Nomes de servidores e cidadãos publicados
  continuam protegidos pela LGPD quando reutilizados: use só o que tiver relação com o caso.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Vigia do Diário Oficial**: consulta o Querido Diário, lembra o que já viu
e mostra só as publicações novas num HTML.

## 🔎 Inovação OSINT do dia

**Querido Diário (Open Knowledge Brasil).** Os Diários Oficiais municipais costumam ser PDFs espalhados
em milhares de sites diferentes, cada um com seu formato. O Querido Diário raspa, converte para texto e
oferece uma **API pública e gratuita** de busca por termo, município (código IBGE) e período, com links
para o PDF original. Para OSINT brasileiro, é uma das fontes oficiais mais subestimadas: contratos,
nomeações, sanções, alvarás e alertas ao consumidor, tudo pesquisável. Biblioteca Python simples:
`urllib.request` + `urllib.parse` + `json` (nativos).

## 📚 Para ir além

- Querido Diário (busca no navegador): <https://queridodiario.ok.org.br/>
- Documentação interativa da API: <https://api.queridodiario.ok.org.br/docs>
- Pacote `ddgs` no PyPI: <https://pypi.org/project/ddgs/>
- Google Hacking Database (Exploit-DB): <https://www.exploit-db.com/google-hacking-database>
- Lista de operadores de busca do autor: <https://github.com/cipher387/Advanced-search-operators-list>

## ✅ Checklist

- [ ] Entendi por que os originais quebraram e rodei a versão 2026 com `ddgs`
- [ ] Busquei um termo no Querido Diário e abri o PDF de um resultado
- [ ] Salvei resultados de busca em CSV com a data da coleta
- [ ] Gerei e abri o `dorks.html`
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
