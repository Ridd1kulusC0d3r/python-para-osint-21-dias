"""
Rodar uma ferramenta pelo Python e registrar tudo: o "diário de bordo" forense.

Carta 24 (rank B) — Jutsu da Ferramenta de Campo (parte 2)

O que você aprende:
  • a rodar outro programa com subprocess.run (o "irmão moderno" do subprocess.call do original);
  • por que passar o comando como LISTA, sem shell=True, é mais seguro;
  • a usar sys.executable para chamar exatamente o mesmo Python que está rodando este script;
  • a capturar a saída (stdout), os erros (stderr) e o código de retorno;
  • a gravar um log com data/hora, comando, duração e resultado: boa prática forense.

Como rodar (dentro da pasta dia-03-ferramentas-de-linha-de-comando):
    python br/02_rodar_e_registrar.py
    OSINT_OFFLINE=1 python br/02_rodar_e_registrar.py
"""

import hashlib              # para calcular a "impressão digital" (SHA-256) da saída
import json
import os
import subprocess           # rodar outros programas
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
CEPS = "30130-010, 30130010, 123"  #@param {type:"string"}
FORMATO = "json"  #@param ["texto", "json", "csv"]

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
FERRAMENTA = PASTA_DIA / "br" / "01_cli_cep.py"
SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)
LOG = SAIDAS / "log_execucoes.jsonl"     # .jsonl = um JSON por linha (fácil de ir acrescentando)

# Fuso de Brasília, com plano B para Windows sem tzdata.
try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

print(f"🧰 Ferramenta: {FERRAMENTA.name}")
print(f"🐍 Python usado: {sys.executable}")
print(f"📝 Log: {LOG.relative_to(PASTA_DIA)}\n")

for cep in [c.strip() for c in CEPS.split(",") if c.strip()]:
    # ── 1. Montar o comando como LISTA ────────────────────────────────────
    # Cada pedaço é um item. Sem shell=True, o texto do CEP nunca é "interpretado"
    # pelo terminal: se alguém passasse "30130010; rm -rf /", seria só um CEP inválido.
    comando = [sys.executable, str(FERRAMENTA), "--cep", cep, "--formato", FORMATO]

    # ── 2. Rodar e capturar ───────────────────────────────────────────────
    inicio = datetime.now(FUSO)
    cronometro = time.perf_counter()
    resultado = subprocess.run(
        comando,
        capture_output=True,     # guarda stdout e stderr em vez de jogar na tela
        text=True,               # devolve texto (str) em vez de bytes
        encoding="utf-8",        # os acentos e emojis chegam inteiros (importante no Windows)
        env=dict(os.environ, PYTHONIOENCODING="utf-8"),  # o processo filho também fala UTF-8
        timeout=60,              # se travar, desiste depois de 60 segundos
        cwd=PASTA_DIA,           # roda "de dentro" da pasta do dia
    )
    duracao = time.perf_counter() - cronometro

    # ── 3. Mostrar ────────────────────────────────────────────────────────
    icone = "✅" if resultado.returncode == 0 else "❌"
    print(f"{icone} CEP {cep!r} → código de retorno {resultado.returncode} ({duracao:.2f} s)")
    for linha in resultado.stdout.strip().splitlines():
        print(f"   │ {linha}")
    for linha in resultado.stderr.strip().splitlines():
        print(f"   ⚠ {linha}")

    # ── 4. Registrar (uma linha JSON por execução) ────────────────────────
    # O SHA-256 da saída permite provar depois que o resultado guardado não foi alterado.
    registro = {
        "quando": inicio.isoformat(timespec="seconds"),
        "comando": comando[1:],                       # sem o caminho do Python, para ficar legível
        "python": sys.version.split()[0],
        "codigo_retorno": resultado.returncode,
        "duracao_s": round(duracao, 3),
        "modo_offline": "MODO OFFLINE" in resultado.stderr,
        "sha256_saida": hashlib.sha256(resultado.stdout.encode("utf-8")).hexdigest(),
        "saida": resultado.stdout,
        "erros": resultado.stderr,
    }
    # Modo "a" (append): acrescenta no fim, sem apagar as execuções anteriores.
    with open(LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
    print()

# ── 5. Reler o log ────────────────────────────────────────────────────────
linhas = LOG.read_text(encoding="utf-8").splitlines()
print(f"📚 O log tem {len(linhas)} execução(ões) registradas. A última:")
ultima = json.loads(linhas[-1])
print(f"   {ultima['quando']} · {' '.join(ultima['comando'][-4:])} · retorno {ultima['codigo_retorno']}"
      f" · sha256 {ultima['sha256_saida'][:16]}…")
