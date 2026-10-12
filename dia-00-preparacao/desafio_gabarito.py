"""
Gabarito do desafio de boas-vindas do Dia 0 — Meu verificador de ambiente.

Versão personalizada do br/01_verifica_ambiente.py:
  • confere se git e pip estão instalados (shutil.which);
  • testa uma lista de serviços que VOCÊ escolhe (parâmetro SERVICOS_EXTRAS);
  • grava um relatório em saidas/meu_ambiente.txt com carimbo de data/hora de Brasília.
Com OSINT_OFFLINE=1, pula os testes de internet.
"""

import os
import platform
import shutil               # shutil.which("git") diz onde está o programa (ou None se não existe)
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

SERVICOS_EXTRAS = "https://www.gov.br/pt-br, https://registro.br"  #@param {type:"string"}
MEU_NOME = "Analista do NFA"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

linhas = []                 # tudo o que imprimimos também vai para o relatório


def anotar(texto=""):
    print(texto)
    linhas.append(texto)


anotar(f"🧾 Relatório de ambiente de {MEU_NOME}")
anotar(f"   Gerado em {datetime.now(FUSO):%d/%m/%Y %H:%M:%S} (Brasília)")
anotar(f"   Python {sys.version.split()[0]} · {platform.system()} {platform.release()}")
anotar("   " + ("✅ Python 3.9+" if sys.version_info >= (3, 9) else "❌ Python antigo: atualize"))

# ── Programas externos ────────────────────────────────────────────────────
anotar("\n🧰 Programas")
for programa in ("git", "pip", "pip3"):
    caminho = shutil.which(programa)
    anotar(f"   {'✅' if caminho else '❌'} {programa:<5} {caminho or 'não encontrado'}")

# O pip também pode ser chamado como módulo do próprio Python (funciona mesmo sem "pip" no PATH).
r = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
versao_pip = (r.stdout or r.stderr).strip().split(" from ")[0]   # "pip 24.0 from /..." → "pip 24.0"
anotar(f"   {'✅' if r.returncode == 0 else '❌'} python -m pip  {versao_pip}")

# ── Meus serviços ─────────────────────────────────────────────────────────
anotar("\n🌐 Meus serviços")
urls = [u.strip() for u in SERVICOS_EXTRAS.split(",") if u.strip()]
if OFFLINE:
    print("⚠️ MODO OFFLINE: testes de internet pulados.")
    linhas.append("   (modo offline: não testado)")
else:
    for url in urls:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=10) as resposta:
                anotar(f"   ✅ {url}  (HTTP {resposta.status})")
        except Exception as erro:
            anotar(f"   ❌ {url}  ({type(erro).__name__})")

# ── Salvar ────────────────────────────────────────────────────────────────
SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)
(SAIDAS / "meu_ambiente.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n💾 saidas/meu_ambiente.txt gravado.")
