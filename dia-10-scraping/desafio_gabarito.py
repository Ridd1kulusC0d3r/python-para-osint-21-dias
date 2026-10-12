"""
Gabarito do Desafio S do Dia 10 — Caçador de lojas irmãs.

Extrai a "impressão digital" da vitrine do caso (generator, chaves PIX, números de
WhatsApp, e-mails escondidos em comentários) e compara com cada página salva em
dados/lojas_suspeitas/. Gera um placar de semelhança e grava saidas/lojas_irmas.csv.
100% offline: só arquivos locais e fictícios.
"""

import csv
from html.parser import HTMLParser
from pathlib import Path

PASTA_SUSPEITAS = "dados/lojas_suspeitas"  #@param {type:"string"}
PONTOS_PARA_ALERTA = 3  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# Quanto vale cada coincidência. Chave PIX e telefone pesam mais que a plataforma,
# porque muitas lojas honestas usam a mesma plataforma.
PESOS = {"generator": 1, "pix": 3, "whatsapp": 3, "email": 2}


class Digital(HTMLParser):
    """Coleta os traços que identificam quem montou a loja."""

    def __init__(self):
        super().__init__()
        self.tracos = {"generator": set(), "pix": set(), "whatsapp": set(), "email": set()}
        self.titulo = ""
        self._no_titulo = False
        self._no_pix = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name") == "generator":
            self.tracos["generator"].add(a.get("content", ""))
        if tag == "strong" and a.get("class") == "pix":
            self._no_pix = True
        if tag == "title":
            self._no_titulo = True
        href = a.get("href", "")
        if "wa.me/" in href:
            self.tracos["whatsapp"].add(href.rsplit("/", 1)[-1])     # só os dígitos
        if href.startswith("mailto:"):
            self.tracos["email"].add(href[len("mailto:"):].lower())

    def handle_endtag(self, tag):
        if tag == "strong":
            self._no_pix = False
        if tag == "title":
            self._no_titulo = False

    def handle_data(self, texto):
        if self._no_pix and texto.strip():
            self.tracos["pix"].add(texto.strip().lower())
        if self._no_titulo:
            self.titulo += texto.strip()

    def handle_comment(self, texto):
        for palavra in texto.split():
            if "@" in palavra:
                self.tracos["email"].add(palavra.strip(".,;").lower())


def digital_de(caminho):
    leitor = Digital()
    leitor.feed(caminho.read_text(encoding="utf-8"))
    return leitor


referencia = digital_de(PASTA_CASO / "vitrine_megaoferta.html")
print(f"🧬 Digital da referência ({referencia.titulo}):")
for tipo, valores in referencia.tracos.items():
    print(f"   {tipo:<9} {', '.join(sorted(valores)) or '—'}")

linhas = []
for pagina in sorted((PASTA_DIA / PASTA_SUSPEITAS).glob("*.html")):
    try:
        suspeita = digital_de(pagina)
    except (OSError, UnicodeDecodeError) as erro:
        print(f"⚠️  Não consegui ler {pagina.name}: {erro}")
        continue
    pontos, coincidencias = 0, []
    for tipo, peso in PESOS.items():
        comuns = referencia.tracos[tipo] & suspeita.tracos[tipo]     # interseção de conjuntos
        if comuns:
            pontos += peso
            coincidencias.append(f"{tipo}={'/'.join(sorted(comuns))}")
    alerta = "🚩 provável loja irmã" if pontos >= PONTOS_PARA_ALERTA else "ok"
    linhas.append({"arquivo": pagina.name, "titulo": suspeita.titulo, "pontos": pontos,
                   "coincidencias": " | ".join(coincidencias), "alerta": alerta})

linhas.sort(key=lambda l: l["pontos"], reverse=True)
print("\n🏁 Placar:")
for l in linhas:
    print(f"   {l['pontos']:>2} pts  {l['arquivo']:<36} {l['alerta']}")
    if l["coincidencias"]:
        print(f"           ↳ {l['coincidencias']}")

saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
with open(saidas / "lojas_irmas.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=["arquivo", "titulo", "pontos", "coincidencias", "alerta"], delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)
print("\n💾 saidas/lojas_irmas.csv gravado.")
