"""
Gabarito do Desafio S do Dia 20 — A API do caso.

Um servidor com três rotas, só com stdlib:
  /                      página simples explicando a API
  /api/denuncias?...     JSON com as denúncias filtradas (cidade, chave, de, ate) — SEM nome e CPF
  /api/resumo            JSON com totais por chave PIX e por mês
Com OSINT_OFFLINE=1 (ou sem terminal), sobe numa thread, testa as rotas a si mesmo e encerra.
"""

import csv
import json
import os
import sys
import threading
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORTA = 8002  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
EM_NOTEBOOK = "__file__" not in globals()
MODO_TESTE = os.environ.get("OSINT_OFFLINE") == "1" or (not EM_NOTEBOOK and not sys.stdout.isatty())

# Campos publicados pela API. Nome e CPF da vítima ficam de fora (minimização).
PUBLICOS = ["id", "data", "cidade", "uf", "valor", "produto", "chave_pix_destino"]


def chave(t):
    s = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return " ".join(s.casefold().split())


with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as f:
    DENUNCIAS = [{k: d[k] for k in PUBLICOS} for d in csv.DictReader(f, delimiter=";")]


def filtrar(p):
    """p = dicionário de parse_qs. Todos os filtros são opcionais e se somam (E)."""
    cidade = chave(p.get("cidade", [""])[0])
    pix = p.get("chave", [""])[0].lower()
    de, ate = p.get("de", ["0000-00-00"])[0], p.get("ate", ["9999-99-99"])[0]
    return [d for d in DENUNCIAS
            if cidade in chave(d["cidade"]) and d["chave_pix_destino"].startswith(pix)
            and de <= d["data"] <= ate]                    # datas ISO comparam como texto!


def resumo():
    por_chave, por_mes = defaultdict(Decimal), defaultdict(int)
    for d in DENUNCIAS:
        por_chave[d["chave_pix_destino"]] += Decimal(d["valor"])
        por_mes[d["data"][:7]] += 1
    return {"total_denuncias": len(DENUNCIAS),
            "total_valor": str(sum(por_chave.values())),           # Decimal → texto (JSON não tem Decimal)
            "por_chave_pix": {k: str(v) for k, v in sorted(por_chave.items())},
            "por_mes": dict(sorted(por_mes.items()))}


class API(BaseHTTPRequestHandler):
    def responder(self, status, corpo, tipo):
        dados = corpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("X-Content-Type-Options", "nosniff")   # o navegador não "adivinha" o tipo
        self.end_headers()
        self.wfile.write(dados)

    def json(self, status, objeto):
        self.responder(status, json.dumps(objeto, ensure_ascii=False, indent=2), "application/json")

    def do_GET(self):
        partes = urllib.parse.urlsplit(self.path)
        p = urllib.parse.parse_qs(partes.query)
        if partes.path == "/api/denuncias":
            achados = filtrar(p)
            self.json(200, {"quantidade": len(achados), "filtros": {k: v[0] for k, v in p.items()},
                            "denuncias": achados})
        elif partes.path == "/api/resumo":
            self.json(200, resumo())
        elif partes.path == "/":
            self.responder(200, "<!doctype html><meta charset='utf-8'><title>API NFA</title>"
                                "<h1>API do caso</h1><ul><li><a href='/api/resumo'>/api/resumo</a></li>"
                                "<li><a href='/api/denuncias?cidade=contagem'>/api/denuncias?cidade=contagem</a></li>"
                                "<li>/api/denuncias?chave=f38b&amp;de=2025-11-01&amp;ate=2025-11-30</li></ul>",
                           "text/html")
        else:
            self.json(404, {"erro": "rota inexistente", "rotas": ["/api/denuncias", "/api/resumo"]})

    def log_message(self, formato, *args):
        print(f"📥 {formato % args}")


try:
    servidor = ThreadingHTTPServer(("127.0.0.1", 0 if MODO_TESTE else PORTA), API)
except OSError as erro:
    raise SystemExit(f"❌ Porta {PORTA} ocupada ({erro}).")
porta = servidor.server_address[1]

if MODO_TESTE:
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{porta}"

    def get_json(caminho):
        try:
            with urllib.request.urlopen(base + caminho, timeout=10) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as erro:       # 404 também tem corpo JSON
            return erro.code, json.load(erro)

    try:
        st, r = get_json("/api/resumo")
        print(f"🧪 /api/resumo → {st}: {r['total_denuncias']} denúncias, R$ {r['total_valor']}")
        assert r["total_valor"] == "54877.40"

        st, r = get_json("/api/denuncias?" + urllib.parse.urlencode({"cidade": "juiz de fora"}))
        print(f"🧪 cidade='juiz de fora' → {r['quantidade']} denúncias")

        st, r = get_json("/api/denuncias?chave=f38b&de=2025-11-01&ate=2025-11-30")
        print(f"🧪 chave f38b em novembro → {r['quantidade']} denúncias")
        vazou = any("cpf" in d or "nome_vitima" in d for d in r["denuncias"])
        print(f"🧪 nome/CPF na resposta? {'❌ SIM' if vazou else '✅ não'}")
        assert not vazou

        st, r = get_json("/nao-existe")
        print(f"🧪 /nao-existe → {st} {r['erro']}")
        assert st == 404
    finally:
        servidor.shutdown()
        servidor.server_close()
    print("✅ API testada e encerrada.")
elif EM_NOTEBOOK:
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    print(f"🌐 API em http://127.0.0.1:{porta}")
    try:
        from google.colab import output
        output.serve_kernel_port_as_window(porta)
    except ImportError:
        pass
else:
    print(f"🌐 API em http://127.0.0.1:{porta}  (Ctrl+C para parar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
