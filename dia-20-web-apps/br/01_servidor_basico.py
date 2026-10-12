"""
Seu primeiro servidor web, só com a biblioteca padrão (http.server).

Carta 41 (rank A) — Jutsu do Painel

O que você aprende:
  • o que acontece quando o navegador pede uma página: requisição GET → resposta com status e HTML;
  • a escrever um "handler" com BaseHTTPRequestHandler e o método do_GET;
  • a escolher o endereço: 127.0.0.1 (só o seu computador) × 0.0.0.0 (toda a rede);
  • a testar o próprio servidor sem navegador, com urllib.

Como rodar (dentro da pasta dia-20-web-apps):
    python br/01_servidor_basico.py           # abra http://127.0.0.1:8000 · Ctrl+C para parar
    OSINT_OFFLINE=1 python br/01_servidor_basico.py   # modo teste: sobe, faz 1 pedido e encerra
"""

import os
import sys
import threading
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ── Parâmetros ────────────────────────────────────────────────────────────
PORTA = 8000  #@param {type:"integer"}
ENDERECO = "127.0.0.1"  #@param ["127.0.0.1", "0.0.0.0"]

# Modo teste: o teste automático não pode ficar esperando você apertar Ctrl+C.
# Entra em modo teste com OSINT_OFFLINE=1 ou quando o script roda "sem terminal"
# (saída redirecionada, como no teste automático). No Colab, nunca.
EM_NOTEBOOK = "__file__" not in globals()
MODO_TESTE = os.environ.get("OSINT_OFFLINE") == "1" or (not EM_NOTEBOOK and not sys.stdout.isatty())

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))


class Pagina(BaseHTTPRequestHandler):
    """Cada vez que chega um pedido, o servidor cria um objeto desta classe e chama do_GET."""

    def do_GET(self):
        # self.path é o caminho pedido: "/", "/favicon.ico", "/qualquer/coisa"...
        if self.path != "/":
            self.send_error(404, "Página não encontrada")   # resposta pronta de erro
            return
        agora = datetime.now(FUSO)
        corpo = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>NFA</title></head>
<body style="font-family: system-ui; max-width: 600px; margin: 3rem auto">
  <h1>🕵️ Núcleo de Fontes Abertas</h1>
  <p>Servidor no ar. Hora do servidor: <b>{agora:%d/%m/%Y %H:%M:%S}</b> (Brasília).</p>
  <p>Amanhã isto vira o painel do caso.</p>
</body></html>"""
        dados = corpo.encode("utf-8")              # a rede transporta BYTES, não texto
        self.send_response(200)                    # 200 = OK
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()                         # linha em branco: acabaram os cabeçalhos
        self.wfile.write(dados)                    # o corpo da resposta

    def log_message(self, formato, *args):
        """Cada pedido vira uma linha no terminal: quem, quando, o quê."""
        print(f"📥 {self.client_address[0]} → {formato % args}")


# ── Subir o servidor ──────────────────────────────────────────────────────
# Porta 0 = "sistema, me dá uma porta livre qualquer" (útil no teste, para não dar conflito).
try:
    servidor = ThreadingHTTPServer((ENDERECO, 0 if MODO_TESTE else PORTA), Pagina)
except OSError as erro:
    # Acontece ao rodar a célula duas vezes no notebook: o servidor anterior ainda ocupa a porta.
    raise SystemExit(f"❌ Porta {PORTA} ocupada ({erro}). Troque PORTA ou reinicie o kernel.")
porta_real = servidor.server_address[1]

if MODO_TESTE:
    # Thread = o servidor roda "em paralelo", enquanto o resto do script continua.
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    with urllib.request.urlopen(f"http://127.0.0.1:{porta_real}/", timeout=10) as resposta:
        html_recebido = resposta.read().decode("utf-8")
        print(f"🧪 Modo teste: GET / → HTTP {resposta.status}, {len(html_recebido)} caracteres")
        print("   " + next(l.strip() for l in html_recebido.splitlines() if "<h1>" in l))
    servidor.shutdown()
    servidor.server_close()
    print("✅ Servidor respondeu e foi encerrado.")
else:
    print(f"🌐 Servidor no ar em http://{ENDERECO}:{porta_real}  {'(reinicie o ambiente para parar)' if EM_NOTEBOOK else '(Ctrl+C para parar)'}")
    if ENDERECO == "0.0.0.0":
        print("⚠️ 0.0.0.0 = qualquer computador da sua rede consegue abrir. Use só se precisar.")
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
            print("\n👋 Servidor encerrado.")
            servidor.server_close()
