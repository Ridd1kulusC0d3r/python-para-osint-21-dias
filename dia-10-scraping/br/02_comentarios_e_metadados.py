"""
O que o navegador esconde: comentários HTML e metadados da vitrine.

Carta 31 (rank B) — Jutsu da Vitrine Congelada (parte 2)

O que você aprende:
  • que comentários <!-- ... --> não aparecem na tela, mas estão no código;
  • a capturá-los com handle_comment;
  • a ler as tags <meta> (description, generator) e o <title>;
  • por que o "generator" funciona como impressão digital da plataforma da loja.

Este script é 100% offline: lê caso/dados/vitrine_megaoferta.html (fictício).

Como rodar (dentro da pasta dia-10-scraping):
    python br/02_comentarios_e_metadados.py
"""

from html.parser import HTMLParser
from pathlib import Path

ARQUIVO_HTML = "vitrine_megaoferta.html"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"


class LeitorDeBastidores(HTMLParser):
    """Guarda comentários, metadados e o título da página."""

    def __init__(self):
        super().__init__()
        self.comentarios = []
        self.metas = {}          # {"generator": "LojaPronta 3.2", ...}
        self.titulo = ""
        self.no_titulo = False

    def handle_comment(self, texto):
        # Chamado para cada <!-- ... -->. "texto" é o que está entre <!-- e -->.
        self.comentarios.append(texto.strip())

    def handle_starttag(self, tag, attrs):
        atributos = dict(attrs)
        if tag == "meta" and "name" in atributos:
            # <meta name="generator" content="LojaPronta 3.2">
            self.metas[atributos["name"]] = atributos.get("content", "")
        elif tag == "meta" and "charset" in atributos:
            self.metas["charset"] = atributos["charset"]
        elif tag == "title":
            self.no_titulo = True

    def handle_data(self, texto):
        if self.no_titulo:
            self.titulo += texto

    def handle_endtag(self, tag):
        if tag == "title":
            self.no_titulo = False


html = (PASTA_CASO / ARQUIVO_HTML).read_text(encoding="utf-8")
leitor = LeitorDeBastidores()
leitor.feed(html)

# ── 1. Título e metadados ─────────────────────────────────────────────────
print(f"📰 Título: {leitor.titulo.strip()}\n")
print("🏷️  Metadados:")
for nome, valor in leitor.metas.items():
    print(f"   {nome:<12} = {valor}")

# ── 2. Comentários escondidos ─────────────────────────────────────────────
print(f"\n🙈 Comentários escondidos no HTML: {len(leitor.comentarios)}")
for comentario in leitor.comentarios:
    print(f"   <!-- {comentario} -->")

# ── 3. O que isso significa para o caso ───────────────────────────────────
print("\n🧠 Leitura de analista:")
for comentario in leitor.comentarios:
    texto = comentario.lower()
    if "pix" in texto:
        print("   🚩 Um TODO fala em trocar a chave PIX antes da Black Friday:")
        print("      indica planejamento e que pode haver MAIS de uma chave em uso.")
    if "@" in texto:
        email = [p for p in comentario.split() if "@" in p][0]
        print(f"   🚩 E-mail do desenvolvedor esquecido no código: {email}")
        print("      Compare com o apelido do vendedor no WhatsApp ('Kau').")

gerador = leitor.metas.get("generator")
if gerador:
    print(f"   🧬 Plataforma declarada: '{gerador}'. Outras lojas falsas feitas na mesma")
    print("      plataforma/versão costumam repetir o mesmo 'generator', o mesmo layout e")
    print("      os mesmos erros. É uma impressão digital para achar sites irmãos.")
