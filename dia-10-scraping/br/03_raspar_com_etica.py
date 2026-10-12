"""
Raspar com educação: consultar o robots.txt antes de baixar uma página pública.

Carta 31 (rank B) — Jutsu da Vitrine Congelada (parte 3)

O que você aprende:
  • o que é o robots.txt e como lê-lo com urllib.robotparser (nativo);
  • a se identificar com um User-Agent honesto e a esperar entre pedidos;
  • a baixar uma página pública e extrair o <title> e os links com html.parser;
  • a transformar links relativos ("/pt-br/servicos") em absolutos com urljoin.

Alvo padrão: o portal https://www.gov.br/pt-br (página pública institucional).

Como rodar (dentro da pasta dia-10-scraping):
    python br/03_raspar_com_etica.py
    OSINT_OFFLINE=1 python br/03_raspar_com_etica.py   # usa as amostras de dados/
"""

import os
import time                          # para esperar entre um pedido e outro
import urllib.parse                  # urlsplit e urljoin
import urllib.request
import urllib.robotparser            # o "leitor de robots.txt" do Python
from html.parser import HTMLParser
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
URL = "https://www.gov.br/pt-br"  #@param {type:"string"}
USER_AGENT = "python-para-osint-21-dias/estudo"  #@param {type:"string"}
PAUSA_SEGUNDOS = 2  #@param {type:"integer"}
MAX_LINKS = 15  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def baixar_texto(url, amostra):
    """Baixa uma página como texto; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                # O servidor diz a codificação no cabeçalho; se não disser, assumimos utf-8.
                codificacao = resposta.headers.get_content_charset() or "utf-8"
                return resposta.read().decode(codificacao, errors="replace")
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return (PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8")


class LeitorDeLinks(HTMLParser):
    """Pega o <title> e todos os <a href> da página."""

    def __init__(self):
        super().__init__()
        self.titulo = ""
        self.no_titulo = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.no_titulo = True
        elif tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_data(self, texto):
        if self.no_titulo:
            self.titulo += texto

    def handle_endtag(self, tag):
        if tag == "title":
            self.no_titulo = False


# ── 1. Ler o robots.txt do site ───────────────────────────────────────────
# O robots.txt fica SEMPRE na raiz: https://www.gov.br/robots.txt
partes = urllib.parse.urlsplit(URL)
url_robots = f"{partes.scheme}://{partes.netloc}/robots.txt"
print(f"🤖 Lendo {url_robots}")

texto_robots = baixar_texto(url_robots, "robots_gov_br.txt")
regras = urllib.robotparser.RobotFileParser()
regras.parse(texto_robots.splitlines())     # parse() aceita a lista de linhas que já baixamos

permitido = regras.can_fetch(USER_AGENT, URL)
print(f"   Posso baixar {URL}?  {'✅ sim' if permitido else '⛔ não'}")
atraso = regras.crawl_delay(USER_AGENT)     # alguns sites pedem um intervalo mínimo
if atraso:
    print(f"   O site pede {atraso} s entre pedidos (Crawl-delay). Vamos respeitar.")
    PAUSA_SEGUNDOS = max(PAUSA_SEGUNDOS, int(atraso))

if not permitido:
    raise SystemExit("⛔ O robots.txt pede para robôs não acessarem esta página. Paramos aqui.")

# ── 2. Esperar um pouco e baixar a página ─────────────────────────────────
if not OFFLINE:
    time.sleep(PAUSA_SEGUNDOS)   # educação: não emende pedidos em sequência
html = baixar_texto(URL, "gov_br_pt-br.html")

# ── 3. Extrair título e links ─────────────────────────────────────────────
leitor = LeitorDeLinks()
leitor.feed(html)
print(f"\n📰 Título: {' '.join(leitor.titulo.split())}")

# urljoin resolve links relativos: "/pt-br/servicos" + URL → "https://www.gov.br/pt-br/servicos"
absolutos = []
for link in leitor.links:
    completo = urllib.parse.urljoin(URL, link)
    if completo.startswith("http") and completo not in absolutos:   # sem repetidos, sem "javascript:"
        absolutos.append(completo)

internos = [l for l in absolutos if urllib.parse.urlsplit(l).netloc == partes.netloc]
print(f"🔗 {len(absolutos)} links únicos ({len(internos)} do próprio site). Primeiros {MAX_LINKS}:")
for link in absolutos[:MAX_LINKS]:
    marca = "🏠" if link in internos else "🌍"
    print(f"   {marca} {link}")

# ── 4. Guardar a lista (com data/hora da coleta, boa prática de registro) ─
saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
carimbo = time.strftime("%Y-%m-%d %H:%M:%S")
with open(saidas / "links_coletados.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(f"# Coleta de {URL} em {carimbo} (hora local) — UA: {USER_AGENT}\n")
    arquivo.write("\n".join(absolutos) + "\n")
print("\n💾 saidas/links_coletados.txt gravado.")
