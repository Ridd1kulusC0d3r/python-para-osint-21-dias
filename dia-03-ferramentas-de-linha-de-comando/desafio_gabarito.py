"""
Gabarito do Desafio S do Dia 3 — Lote de buscas com registro.

Golpistas trocam de conta, mas costumam repetir o apelido com pequenas variações.
Este script:
  1. gera variantes de um apelido (separadores . _ - e sem separador);
  2. monta, para cada variante, o comando do br/03_mini_blackbird.py (como LISTA, sem shell=True);
  3. em modo SIMULAÇÃO (padrão para o apelido fictício do caso) só registra os comandos;
     para o alvo de treino público (cipher387), roda de verdade e captura a saída;
  4. grava saidas/lote_buscas.csv (abre no Excel) e acrescenta cada execução em saidas/log_lote.txt.

Por que simular o apelido do caso? "kau.ofertas" é inventado, mas pode existir de verdade,
como conta de um desconhecido, em algum site. Consultá-lo seria investigar um inocente.
"""

import csv
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

APELIDO_DO_CASO = "kau.ofertas"  #@param {type:"string"}
ALVO_DE_TREINO = "cipher387"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
FERRAMENTA = PASTA_DIA / "br" / "03_mini_blackbird.py"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"
SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))


def variantes(apelido):
    """'kau.ofertas' → ['kau-ofertas', 'kau.ofertas', 'kau_ofertas', 'kauofertas']"""
    partes = apelido.replace("_", ".").replace("-", ".").split(".")
    return sorted({sep.join(partes) for sep in (".", "_", "-", "")})   # set: sem repetidos


def rodar(username):
    """Roda o mini-blackbird e devolve (código de retorno, linhas com resultado por site)."""
    comando = [sys.executable, str(FERRAMENTA), "--username", username]
    r = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", timeout=120,
                       cwd=PASTA_DIA, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    sites = [l for l in r.stdout.splitlines() if l.startswith(("GitHub", "GitLab", "Codeberg"))]
    return r.returncode, sites


# ── 1. Montar o lote ──────────────────────────────────────────────────────
lote = [(v, "simulação") for v in variantes(APELIDO_DO_CASO)] + [(ALVO_DE_TREINO, "execução")]
print(f"🧬 Variantes de {APELIDO_DO_CASO!r}: {', '.join(v for v, _ in lote[:-1])}")
print(f"🎯 Alvo de treino (público): {ALVO_DE_TREINO!r}\n")
if OFFLINE:
    print("⚠️ MODO OFFLINE: o alvo de treino será verificado com a amostra local.\n")

# ── 2. Processar ──────────────────────────────────────────────────────────
linhas = []
with open(SAIDAS / "log_lote.txt", "a", encoding="utf-8") as log:
    for username, modo in lote:
        quando = datetime.now(FUSO).isoformat(timespec="seconds")
        comando_txt = f"python br/03_mini_blackbird.py --username {username}"
        if modo == "simulação":
            print(f"📝 [simulação] {comando_txt}")
            linhas.append({"quando": quando, "username": username, "modo": modo,
                           "retorno": "", "resultado": "não consultado (apelido fictício)"})
        else:
            codigo, sites = rodar(username)
            print(f"▶️  [execução] {comando_txt}  → retorno {codigo}")
            for s in sites:
                print(f"     {s}")
            linhas.append({"quando": quando, "username": username, "modo": modo,
                           "retorno": codigo, "resultado": " | ".join(" ".join(s.split()) for s in sites)})
        log.write(f"{quando}\t{modo}\t{comando_txt}\n")

# ── 3. Salvar ─────────────────────────────────────────────────────────────
with open(SAIDAS / "lote_buscas.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)

print(f"\n💾 saidas/lote_buscas.csv ({len(linhas)} linhas) e saidas/log_lote.txt gravados.")
print("⚖️  Num caso real, só rode o lote com autorização e finalidade definida, e trate cada")
print("   'encontrado' como hipótese: mesmo apelido não quer dizer mesma pessoa.")
