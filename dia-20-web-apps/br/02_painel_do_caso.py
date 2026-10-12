"""
O painel do caso: um web app para a equipe buscar nas denúncias.

Carta 41 (rank A) — Jutsu do Painel (parte 2)

O que você aprende:
  • a ler os parâmetros da URL (?campo=cidade&q=contagem) com urllib.parse (urlsplit + parse_qs);
  • a montar um formulário HTML que envia uma busca por GET;
  • a escapar TUDO o que vai para a página com html.escape, e por que isso evita XSS;
  • a buscar sem acento e sem maiúscula (a chave de comparação do Dia 16);
  • a testar o próprio app automaticamente, inclusive com um ataque de XSS.

Como rodar (dentro da pasta dia-20-web-apps):
    python br/02_painel_do_caso.py            # abra http://127.0.0.1:8001 · Ctrl+C para parar
    OSINT_OFFLINE=1 python br/02_painel_do_caso.py   # modo teste: sobe, faz pedidos e encerra
"""

import csv
import html
import os
import sys
import threading
import unicodedata
import urllib.parse
import urllib.request
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
PORTA = 8001  #@param {type:"integer"}
ENDERECO = "127.0.0.1"  #@param ["127.0.0.1", "0.0.0.0"]
MAX_RESULTADOS = 50  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
# Modo teste com OSINT_OFFLINE=1 ou sem terminal (teste automático). Ver br/01.
EM_NOTEBOOK = "__file__" not in globals()
MODO_TESTE = os.environ.get("OSINT_OFFLINE") == "1" or (not EM_NOTEBOOK and not sys.stdout.isatty())

# Campos que podem ser buscados: nome interno → rótulo no formulário.
# O nome e o CPF das vítimas NÃO estão aqui de propósito (minimização, LGPD).
CAMPOS = {"cidade": "Cidade", "chave_pix_destino": "Chave PIX", "produto": "Produto"}


def chave(texto):
    """Sem acento, minúsculo, espaços arrumados: 'POÇOS  de caldas' → 'pocos de caldas'."""
    sem = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return " ".join(sem.casefold().split())


def reais(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")


# ── 1. Carregar os dados UMA vez, quando o servidor sobe ──────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    DENUNCIAS = list(csv.DictReader(arquivo, delimiter=";"))


def buscar(campo, termo):
    """Devolve as denúncias em que o termo aparece no campo (busca 'contém', sem acento)."""
    if campo not in CAMPOS or not termo.strip():
        return []
    alvo = chave(termo)
    return [d for d in DENUNCIAS if alvo in chave(d[campo])]


def pagina(campo, termo, resultados):
    """Monta o HTML. REGRA DE OURO: todo texto que veio de fora passa por html.escape."""
    e = html.escape
    opcoes = "".join(
        f'<option value="{e(nome)}"{" selected" if nome == campo else ""}>{e(rotulo)}</option>'
        for nome, rotulo in CAMPOS.items()
    )
    linhas = "".join(
        f"<tr><td>{e(d['id'])}</td><td>{e(d['data'])}</td><td>{e(d['cidade'])}</td>"
        f"<td>{e(d['produto'])}</td><td class='num'>{reais(Decimal(d['valor']))}</td>"
        f"<td><code>{e(d['chave_pix_destino'])}</code></td></tr>"
        for d in resultados[:MAX_RESULTADOS]
    )
    if termo:
        total = sum(Decimal(d["valor"]) for d in resultados)
        # O termo digitado aparece de volta na página: é AQUI que mora o risco de XSS.
        resumo = (f"<p><b>{len(resultados)}</b> denúncia(s) com <b>{e(CAMPOS.get(campo, '?'))}</b> "
                  f"contendo “<mark>{e(termo)}</mark>” · prejuízo {reais(total)}</p>")
        tabela = (f"<table><tr><th>ID</th><th>Data</th><th>Cidade</th><th>Produto</th><th>Valor</th>"
                  f"<th>Chave PIX</th></tr>{linhas}</table>" if resultados else "<p>Nada encontrado.</p>")
    else:
        resumo, tabela = f"<p>{len(DENUNCIAS)} denúncias carregadas. Faça uma busca.</p>", ""
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel do caso — NFA</title>
<style>
 body {{ font-family: system-ui, sans-serif; max-width: 1000px; margin: 1.5rem auto; padding: 0 1rem; }}
 form {{ display: flex; gap: .5rem; flex-wrap: wrap; margin: 1rem 0; }}
 input, select, button {{ font-size: 1rem; padding: .4rem .6rem; }}
 table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
 th, td {{ border-bottom: 1px solid #ddd; padding: .3rem .5rem; text-align: left; }}
 th {{ background: #1f5fa8; color: #fff; }} .num {{ text-align: right; white-space: nowrap; }}
 code {{ font-size: .8rem; }}
</style></head>
<body>
<h1>🕵️ Painel — Operação Vitrine Fantasma</h1>
<form method="get" action="/">
  <select name="campo">{opcoes}</select>
  <input name="q" value="{e(termo)}" placeholder="ex.: contagem, f38b, iphone" autofocus>
  <button>Buscar</button>
</form>
{resumo}
{tabela}
<p style="color:#777;font-size:.8rem">Dados fictícios de estudo · uso interno do NFA</p>
</body></html>"""


class Painel(BaseHTTPRequestHandler):
    def do_GET(self):
        # urlsplit separa "/?campo=cidade&q=belo" em caminho "/" e consulta "campo=cidade&q=belo".
        partes = urllib.parse.urlsplit(self.path)
        if partes.path != "/":
            self.send_error(404, "Página não encontrada")
            return
        # parse_qs devolve LISTAS (um parâmetro pode aparecer várias vezes): {"q": ["belo"]}.
        # Também já desfaz a codificação da URL: "belo+horizonte" → "belo horizonte".
        parametros = urllib.parse.parse_qs(partes.query)
        campo = parametros.get("campo", ["cidade"])[0]
        termo = parametros.get("q", [""])[0][:100]          # limita o tamanho da busca
        corpo = pagina(campo, termo, buscar(campo, termo)).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        # Camada extra contra XSS: o navegador só executa scripts vindos deste próprio servidor.
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'")
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, formato, *args):
        print(f"📥 {self.client_address[0]} {formato % args}")


try:
    servidor = ThreadingHTTPServer((ENDERECO, 0 if MODO_TESTE else PORTA), Painel)
except OSError as erro:
    # Acontece ao rodar a célula duas vezes no notebook: o servidor anterior ainda ocupa a porta.
    raise SystemExit(f"❌ Porta {PORTA} ocupada ({erro}). Troque PORTA ou reinicie o kernel.")
porta_real = servidor.server_address[1]

if MODO_TESTE:
    # ── Modo teste: sobe numa thread, faz pedidos a si mesmo e encerra ────
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{porta_real}/?"

    def pedir(campo, termo):
        url = base + urllib.parse.urlencode({"campo": campo, "q": termo})
        with urllib.request.urlopen(url, timeout=10) as resposta:
            return resposta.read().decode("utf-8")

    try:
        resposta = pedir("cidade", "contagem")
        achados = resposta.count("<tr><td>DEN-")
        print(f"🧪 Busca cidade='contagem' → {achados} denúncias na tabela")

        resposta = pedir("chave_pix_destino", "f38b")
        print(f"🧪 Busca chave='f38b'      → {resposta.count('<tr><td>DEN-')} denúncias na tabela")

        ataque = "<script>alert('xss')</script>"
        resposta = pedir("produto", ataque)
        seguro = ataque not in resposta and html.escape(ataque) in resposta
        print(f"🧪 Busca com <script>       → {'✅ escapado, não executa' if seguro else '❌ VULNERÁVEL'}")
        if not seguro:
            raise SystemExit("O painel devolveu o <script> sem escapar!")
    finally:
        servidor.shutdown()
        servidor.server_close()
    print("✅ Painel testado e encerrado.")
else:
    print(f"🌐 Painel em http://{ENDERECO}:{porta_real}  {'(reinicie o ambiente para parar)' if EM_NOTEBOOK else '(Ctrl+C para parar)'}")
    if EM_NOTEBOOK:
        # Num notebook, serve_forever() travaria a célula para sempre. Então o servidor roda
        # numa thread "de fundo" e a célula termina; o servidor continua vivo até o kernel reiniciar.
        threading.Thread(target=servidor.serve_forever, daemon=True).start()
        try:
            from google.colab import output       # só existe dentro do Google Colab
            output.serve_kernel_port_as_window(porta_real)
        except ImportError:
            print("   (Jupyter local: abra o endereço acima no navegador.)")
    else:
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Painel encerrado.")
            servidor.server_close()
