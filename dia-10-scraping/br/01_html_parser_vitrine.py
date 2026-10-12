"""
Raspar a vitrine congelada da loja falsa só com a biblioteca padrão (html.parser).

Carta 31 (rank B) — Jutsu da Vitrine Congelada

O que você aprende:
  • que um HTML é uma sequência de "eventos": abre tag, texto, fecha tag;
  • a usar html.parser.HTMLParser (nativo) no lugar do BeautifulSoup;
  • a "lembrar onde estou" (dentro de um produto? dentro do preço?) com variáveis;
  • a extrair produtos, preços, chave PIX, CNPJ e links da cópia salva do site.

Este script é 100% offline: lê caso/dados/vitrine_megaoferta.html (fictício).

Como rodar (dentro da pasta dia-10-scraping):
    python br/01_html_parser_vitrine.py
"""

import json                          # para salvar o resultado organizado
from decimal import Decimal          # dinheiro sem erro de arredondamento
from html.parser import HTMLParser   # o "BeautifulSoup" de bolso que vem com o Python
from pathlib import Path

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
ARQUIVO_HTML = "vitrine_megaoferta.html"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"


class LeitorDeVitrine(HTMLParser):
    """
    O HTMLParser lê o HTML do começo ao fim e chama um método a cada "evento":
      handle_starttag → achou <tag ...>
      handle_data     → achou um texto entre tags
      handle_endtag   → achou </tag>
    Nós só escrevemos o que fazer em cada caso.
    """

    def __init__(self):
        super().__init__()
        self.produtos = []        # lista de dicionários {"nome": ..., "preco": ...}
        self.links = []           # todos os href encontrados
        self.chave_pix = None
        self.textos_rodape = []   # textos soltos do <footer> (onde costuma estar o CNPJ)
        # "Onde estou agora?" Começa tudo como False/None.
        self.no_produto = False
        self.campo_atual = None   # "nome", "preco", "pix" ou None
        self.no_rodape = False

    def handle_starttag(self, tag, attrs):
        # attrs chega como lista de pares [("class", "produto")]; dict() facilita a leitura.
        atributos = dict(attrs)
        classe = atributos.get("class", "")

        if tag == "div" and classe == "produto":
            self.no_produto = True
            self.produtos.append({"nome": "", "preco": ""})   # novo produto, ainda vazio
        elif self.no_produto and tag == "h2":
            self.campo_atual = "nome"
        elif self.no_produto and tag == "span" and classe == "preco":
            self.campo_atual = "preco"
        elif tag == "strong" and classe == "pix":
            self.campo_atual = "pix"
        elif tag == "footer":
            self.no_rodape = True

        # Qualquer tag com href (links <a>) entra na lista de links.
        if "href" in atributos:
            self.links.append(atributos["href"])

    def handle_data(self, texto):
        texto = texto.strip()
        if not texto:
            return                       # ignora espaços e quebras de linha entre as tags
        if self.campo_atual == "nome":
            self.produtos[-1]["nome"] += texto    # [-1] = o último produto criado
        elif self.campo_atual == "preco":
            self.produtos[-1]["preco"] += texto
        elif self.campo_atual == "pix":
            self.chave_pix = texto
        elif self.no_rodape:
            self.textos_rodape.append(texto)

    def handle_endtag(self, tag):
        # Ao fechar a tag, saímos do "campo" em que estávamos.
        if tag in ("h2", "span", "strong"):
            self.campo_atual = None
        elif tag == "div":
            self.no_produto = False
        elif tag == "footer":
            self.no_rodape = False


def preco_para_decimal(texto):
    """'R$ 1.999,00' → Decimal('1999.00'). Tira 'R$', pontos de milhar e troca vírgula por ponto."""
    limpo = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return Decimal(limpo)


# ── 1. Ler o arquivo e alimentar o leitor ─────────────────────────────────
html = (PASTA_CASO / ARQUIVO_HTML).read_text(encoding="utf-8")
leitor = LeitorDeVitrine()
leitor.feed(html)          # feed() dispara todos os handle_* do começo ao fim

# ── 2. Produtos e preços ──────────────────────────────────────────────────
print(f"🛒 Produtos na vitrine: {len(leitor.produtos)}\n")
for produto in leitor.produtos:
    produto["valor"] = str(preco_para_decimal(produto["preco"]))   # guardamos como texto no JSON
    print(f"  • {produto['nome']:<22} {produto['preco']:>12}")

# ── 3. Chave PIX, CNPJ e links ────────────────────────────────────────────
print(f"\n💸 Chave PIX exibida: {leitor.chave_pix}")

cnpj = None
for texto in leitor.textos_rodape:
    if "CNPJ" in texto:
        # "MegaOferta ... LTDA — CNPJ 48.217.093/0001-30" → pega o que vem depois de "CNPJ"
        cnpj = texto.split("CNPJ", 1)[1].strip()
print(f"🏢 CNPJ no rodapé:    {cnpj}  (no Dia 2 você viu que ele NÃO passa no dígito verificador)")

print("\n🔗 Links encontrados:")
for link in leitor.links:
    # Classificamos o tipo de link pelo começo do endereço.
    if link.startswith("mailto:"):
        tipo = "e-mail"
    elif "wa.me" in link:
        tipo = "WhatsApp"
    else:
        tipo = "página"
    print(f"  [{tipo:<8}] {link}")

# ── 4. Salvar tudo em JSON para os próximos dias ──────────────────────────
saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
resultado = {"produtos": leitor.produtos, "chave_pix": leitor.chave_pix, "cnpj": cnpj, "links": leitor.links}
(saidas / "vitrine_extraida.json").write_text(json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n💾 saidas/vitrine_extraida.json gravado.")
