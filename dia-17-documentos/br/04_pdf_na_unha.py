"""
Bônus: um PDF de verdade escrito "na unha", só com a biblioteca padrão.

Carta 38 (rank A) — Jutsu do Relatório Automático (bônus)

O que você aprende:
  • que um PDF é, por dentro, um arquivo de texto com "objetos" numerados;
  • o papel da tabela xref (o índice com a posição em bytes de cada objeto);
  • a escrever texto com acentos usando a fonte embutida Helvetica + WinAnsiEncoding;
  • a conferir se o arquivo gerado é um PDF válido (cabeçalho %PDF, xref e %%EOF).

Para relatórios de verdade, prefira fpdf2 ou o "Imprimir como PDF" do navegador (script 02).
Este exercício é para você nunca mais achar que PDF é mágica.

Como rodar (dentro da pasta dia-17-documentos):
    python br/04_pdf_na_unha.py
"""

import csv
from decimal import Decimal
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
TITULO = "Operação Vitrine Fantasma"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"


def texto_pdf(texto):
    """Prepara um texto para dentro de ( ) no PDF.

    1. Parênteses e barra invertida têm significado especial: escapamos com "\\".
    2. A fonte embutida usa WinAnsiEncoding, que é praticamente o cp1252 do Windows:
       por isso codificamos em cp1252 (é ele que tem "ã", "ç", "é"...).
    Caracteres que não existem no cp1252 (emojis, por exemplo) viram "?".
    """
    texto = texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return texto.encode("cp1252", errors="replace")


def data_br(iso):
    """'2025-10-12' → '12/10/2025'."""
    return "/".join(reversed(iso.split("-")))


# ── 1. Conteúdo: algumas linhas de resumo do caso ─────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = list(csv.DictReader(arquivo, delimiter=";"))
total = sum(Decimal(d["valor"]) for d in denuncias)
total_br = f"{total:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")

linhas = [
    (18, TITULO),
    (12, "Relatório preliminar — Núcleo de Fontes Abertas (dados fictícios)"),
    (12, ""),
    (12, f"Denúncias recebidas: {len(denuncias)}"),
    (12, f"Prejuízo declarado: R$ {total_br}"),
    (12, f"Período: {data_br(min(d['data'] for d in denuncias))} a {data_br(max(d['data'] for d in denuncias))}"),
    (12, "Pagamento exclusivamente por PIX, três chaves de destino."),
    (12, ""),
    (10, "Este PDF foi escrito byte a byte por br/04_pdf_na_unha.py (só stdlib)."),
]

# ── 2. O "fluxo de conteúdo": os comandos de desenho da página ────────────
# BT/ET = começa/termina texto · Tf = fonte e tamanho · Td = move o cursor · Tj = escreve
# A origem (0,0) do PDF é o canto INFERIOR esquerdo. A4 = 595 x 842 pontos.
comandos = [b"BT", b"/F1 18 Tf", b"56 780 Td"]
tamanho_anterior = 18
for i, (tamanho, texto) in enumerate(linhas):
    if i > 0:
        comandos.append(f"0 -{int(tamanho_anterior * 1.6)} Td".encode())  # desce uma linha
    comandos.append(f"/F1 {tamanho} Tf".encode())
    comandos.append(b"(" + texto_pdf(texto) + b") Tj")
    tamanho_anterior = tamanho
comandos.append(b"ET")
# Uma linha horizontal azul embaixo do título (re = retângulo, f = preencher)
comandos.append(b"0.12 0.37 0.66 rg 56 770 483 2 re f")
conteudo = b"\n".join(comandos)

# ── 3. Os objetos do PDF ──────────────────────────────────────────────────
objetos = [
    b"<< /Type /Catalog /Pages 2 0 R >>",                                  # 1: a raiz
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",                           # 2: lista de páginas
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "                # 3: a página A4
    b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "                # 4: a fonte
    b"/Encoding /WinAnsiEncoding >>",
    b"<< /Length " + str(len(conteudo)).encode() + b" >>\nstream\n"         # 5: o desenho
    + conteudo + b"\nendstream",
]

# ── 4. Montar o arquivo, anotando a posição (em bytes) de cada objeto ─────
# O comentário com 4 bytes acima de 127 avisa aos programas que o arquivo é binário.
pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
posicoes = []
for numero, corpo in enumerate(objetos, start=1):
    posicoes.append(len(pdf))                      # onde este objeto começa
    pdf += f"{numero} 0 obj\n".encode() + corpo + b"\nendobj\n"

# A tabela xref: uma linha de EXATAMENTE 20 bytes por objeto (10 dígitos, espaço, 5 dígitos...)
inicio_xref = len(pdf)
pdf += f"xref\n0 {len(objetos) + 1}\n".encode()
pdf += b"0000000000 65535 f \n"                    # o objeto 0 é sempre esse "livre"
for pos in posicoes:
    pdf += f"{pos:010d} 00000 n \n".encode()
pdf += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{inicio_xref}\n%%EOF\n".encode()

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "relatorio_na_unha.pdf"
destino.write_bytes(bytes(pdf))

# ── 5. Autoverificação: o arquivo se parece com um PDF válido? ────────────
dados = destino.read_bytes()
ok_cabecalho = dados.startswith(b"%PDF-")
ok_fim = dados.rstrip().endswith(b"%%EOF")
xref_declarado = int(dados.rsplit(b"startxref", 1)[1].split()[0])
ok_xref = dados[xref_declarado:xref_declarado + 4] == b"xref"
ok_objetos = all(dados[p:].startswith(f"{n} 0 obj".encode()) for n, p in enumerate(posicoes, 1))

print(f"📄 {destino.relative_to(PASTA_DIA)} · {len(dados)} bytes")
print(f"   {'✅' if ok_cabecalho else '❌'} começa com %PDF-")
print(f"   {'✅' if ok_xref else '❌'} startxref aponta para a palavra 'xref'")
print(f"   {'✅' if ok_objetos else '❌'} cada posição da xref aponta para o objeto certo")
print(f"   {'✅' if ok_fim else '❌'} termina com %%EOF")
if not (ok_cabecalho and ok_fim and ok_xref and ok_objetos):
    raise SystemExit("❌ O PDF gerado está inconsistente.")
print("🎉 Abra o arquivo no navegador ou no leitor de PDF: os acentos aparecem certinhos.")
