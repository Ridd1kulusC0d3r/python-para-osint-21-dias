# Dia 10 — Scraping (raspagem de páginas)

> 🃏 Cartas **10 · 31 · 52**  ·  📘 Original: *Day 10. Scraping*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-10-scraping/notebook.ipynb)

## 📖 Capítulo 10 — A vitrine congelada

<!-- historia:inicio -->
Os buscadores e os Diários Oficiais de ontem trouxeram nomes, mas nenhum endereço de site no ar.
A MegaOferta Brasil sumiu. A Iara não parece preocupada: ela abre um pendrive etiquetado
**"vitrine — cópia de 29/11"**.

— Uma das vítimas salvou a página no navegador antes de pagar. Para ela, era só um print caprichado.
Para nós, é o código-fonte inteiro da loja.

Ela abre o arquivo no navegador. Você vê iPhones, PlayStations, um selo "Só no PIX". Depois ela aperta
**Ctrl+U** e a tela vira uma sopa de tags.

— O cliente vê a vitrine. Nós lemos os bastidores. Programador apressado deixa bilhete no código,
e plataforma de loja pronta assina o próprio nome no cabeçalho.

Ela empurra o teclado para você.

— Quero três coisas: a lista de produtos com preço, tudo o que identifica quem recebe o dinheiro, e
qualquer coisa que o navegador **não mostra**. E nada de instalar biblioteca: o Python já traz um
leitor de HTML. Se um dia precisarmos visitar um site de verdade, primeiro perguntamos ao `robots.txt`
o que ele permite.

Você respira fundo e escreve `from html.parser import HTMLParser`.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar o exemplo original com `requests` + `BeautifulSoup`.
- Entender o HTML como uma árvore de **tags**, **atributos** e **textos**.
- Raspar uma página salva com `html.parser`, sem instalar nada.
- Achar o que o navegador esconde: **comentários** e **metadados** (`<meta name="generator">`).
- Consultar o `robots.txt` com `urllib.robotparser` antes de visitar um site real.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
**Raspar** (*scraping*) é ler o HTML de uma página e tirar dele só o que interessa. Um trecho de HTML
tem três ingredientes:

```html
<span class="preco">R$ 1.999,00</span>
 └tag┘ └─atributo─┘ └──texto──┘
```

Para achar elementos, usamos **seletores** parecidos com os do CSS:

| Seletor | Significa |
|---|---|
| `h1` | todo elemento `<h1>` |
| `.preco` | elementos com `class="preco"` |
| `#pagamento` | o elemento com `id="pagamento"` |
| `div.produto` | `<div>` com a classe `produto` |

O **BeautifulSoup** monta a árvore inteira e deixa você perguntar `soup.find("h1")`. O
**`html.parser`** da biblioteca padrão é mais "baixo nível": ele lê o arquivo do começo ao fim e avisa
você a cada tag que abre, cada texto e cada tag que fecha. Dá mais trabalho, mas não precisa instalar
nada e ensina como a coisa funciona por dentro.

Duas armadilhas comuns: (1) muitos sites montam o conteúdo com **JavaScript** depois de carregar, e
o Python só recebe o "esqueleto" (aí entram ferramentas como Selenium ou Playwright); (2) antes de
escrever um raspador, procure se já existe ferramenta pronta para aquele site.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/scraping.py`](original/scraping.py) | Baixa a página do pacote `duckduckgo-search` no PyPI e imprime o título `<h1>` com BeautifulSoup |

```bash
pip install requests beautifulsoup4
cd dia-10-scraping
python original/scraping.py
```

> 💡 Troque a URL por outra página pública e mude `"h1"` para `"title"` ou `"h2"`. Depois experimente
> `soup.find_all("a")` para listar todos os links.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Os dois primeiros são 100% offline (cópia salva da loja fictícia).

| Arquivo | O que faz |
|---|---|
| [`br/01_html_parser_vitrine.py`](br/01_html_parser_vitrine.py) | Extrai da vitrine: produtos, preços (em `Decimal`), chave PIX, CNPJ e links; salva JSON |
| [`br/02_comentarios_e_metadados.py`](br/02_comentarios_e_metadados.py) | Pega `<title>`, `<meta>` e os **comentários escondidos** com `handle_comment` |
| [`br/03_raspar_com_etica.py`](br/03_raspar_com_etica.py) | Lê o `robots.txt`, espera, baixa `https://www.gov.br/pt-br` e lista título e links |

```bash
cd dia-10-scraping
python br/01_html_parser_vitrine.py
python br/02_comentarios_e_metadados.py
OSINT_OFFLINE=1 python br/03_raspar_com_etica.py   # força o modo offline
```

**O que você deve ver no caso:** 6 produtos "Só no PIX", a chave `f38b2ffc-…`, o CNPJ inválido do
rodapé e dois comentários esquecidos pelo desenvolvedor: um **TODO para trocar a chave PIX antes da
Black Friday** e o e-mail **`kau.ofertas@example.com`**. O `generator` é **LojaPronta 3.2**.

## ⚖️ Ética, LGPD e OPSEC

- **Página salva é a melhor fonte.** Analisar uma cópia (como a da vítima) não deixa rastro no
  servidor do suspeito. Visitar o site ao vivo deixa seu IP no log dele e pode alertá-lo (Dia 12).
- **`robots.txt` não é lei, mas é a vontade declarada do dono do site.** Respeite-o, junto com os
  **termos de uso**. Contornar bloqueio técnico (captcha, login, limite) pode configurar ilícito.
- **Ritmo humano:** pausa entre pedidos e User-Agent honesto. Raspar rápido demais derruba sites
  pequenos e dá bloqueio de IP.
- **Raspou dado pessoal? Aplica-se a LGPD.** Colete só o necessário para a finalidade, guarde com
  segurança e registre data/hora e URL de cada coleta (o script 03 já faz isso).
- O fato de uma página ser pública não autoriza montar bases em massa de pessoas (ex.: raspar perfis
  de uma rede social inteira).

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Caçador de lojas irmãs**: compare a "impressão digital" da vitrine do
caso com outras páginas salvas e descubra quais foram montadas pela mesma pessoa.

## 🔎 Inovação OSINT do dia

**Extrair só o texto principal com `trafilatura`.** Em vez de escrever um seletor para cada site, a
biblioteca Python `trafilatura` tenta separar automaticamente o conteúdo principal (texto do artigo,
título, data, autor) do "lixo" da página (menus, rodapés, anúncios). É muito usada para montar bases de
notícias. Uso básico:

```python
# pip install trafilatura
import trafilatura
html = trafilatura.fetch_url("https://www.gov.br/pt-br")
print(trafilatura.extract(html))
```

Ótima para monitorar notícias sobre golpes; fraca para lojas e páginas com pouco texto corrido.

## 📚 Para ir além

- `html.parser` (documentação oficial): <https://docs.python.org/pt-br/3/library/html.parser.html>
- `urllib.robotparser`: <https://docs.python.org/pt-br/3/library/urllib.robotparser.html>
- Beautiful Soup: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
- Protocolo de exclusão de robôs (RFC 9309): <https://www.rfc-editor.org/rfc/rfc9309>
- trafilatura: <https://trafilatura.readthedocs.io/>

## ✅ Checklist

- [ ] Rodei o script original e troquei a URL/seletor
- [ ] Listei os produtos e preços da vitrine com `html.parser`
- [ ] Achei os dois comentários escondidos e o `generator`
- [ ] Consultei o `robots.txt` antes de baixar uma página pública
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
