"""
Checklist de OPSEC antes de uma coleta: o que a sua máquina entrega sem você perceber.

Carta 33 (rank A) — Jutsu do Disfarce Digital (parte 3)

O que você aprende:
  • a verificar automaticamente: proxy configurado?, User-Agent padrão?, fuso, idioma;
  • que fuso horário e idioma também são "impressões digitais" (o navegador os conta aos sites);
  • a gerar um registro (log) da checagem com data e hora, bom para o relatório;
  • a separar o que dá para checar por código do que exige disciplina humana.

Este script não acessa a internet: só olha a configuração da sua máquina.

Como rodar (dentro da pasta dia-12-proxies):
    python br/03_checklist_opsec.py
"""

import locale
import os
import platform
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

USER_AGENT_DO_SCRIPT = "python-para-osint-21-dias/estudo"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()

# Fuso de Brasília. No Windows sem o pacote tzdata, ZoneInfo pode falhar: usamos -03:00 fixo.
try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))

verificacoes = []      # lista de (situação, item, detalhe)


def registrar(ok, item, detalhe):
    """ok=True → ✅, ok=False → 🚩, ok=None → ℹ️ (só informativo)."""
    simbolo = {True: "✅", False: "🚩", None: "ℹ️ "}[ok]
    verificacoes.append((simbolo, item, detalhe))


# ── 1. Proxy ──────────────────────────────────────────────────────────────
proxy_proprio = os.environ.get("PROXY_URL")
# getproxies() lê todas as variáveis *_proxy do sistema; só nos interessam http e https.
proxies_sistema = {k: v for k, v in urllib.request.getproxies().items() if k in ("http", "https")}
if proxy_proprio:
    registrar(True, "Proxy", "PROXY_URL definido (confira o IP com o script 01)")
elif proxies_sistema:
    registrar(None, "Proxy", f"sem PROXY_URL, mas o sistema usa proxy para: {', '.join(sorted(proxies_sistema))}")
else:
    registrar(False, "Proxy", "nenhum proxy: o alvo verá o IP da sua conexão")

# ── 2. User-Agent ─────────────────────────────────────────────────────────
ua_padrao = dict(urllib.request.build_opener().addheaders).get("User-agent", "")
registrar(None, "UA padrão do urllib", ua_padrao)
if "python" in USER_AGENT_DO_SCRIPT.lower() or not USER_AGENT_DO_SCRIPT.strip():
    registrar(False, "UA dos seus scripts", f"'{USER_AGENT_DO_SCRIPT}' revela que é automação "
              "(ok para sites institucionais; ruim para o site do alvo)")
else:
    registrar(True, "UA dos seus scripts", USER_AGENT_DO_SCRIPT)

# ── 3. Fuso horário ───────────────────────────────────────────────────────
agora_local = datetime.now().astimezone()
nome_fuso = time.tzname[0]
registrar(None, "Fuso do sistema", f"{nome_fuso} (UTC{agora_local:%z}) · hora local {agora_local:%H:%M}")
registrar(None, "Hora de Brasília", f"{datetime.now(FUSO_BR):%d/%m/%Y %H:%M}")
if agora_local.utcoffset() == timedelta(hours=-3):
    registrar(None, "Coerência", "fuso -03:00: combina com um disfarce 'brasileiro'; "
              "se o seu proxy sai em outro país, o navegador vai contradizer o IP")

# ── 4. Idioma ─────────────────────────────────────────────────────────────
try:
    idioma = locale.getlocale()[0] or os.environ.get("LANG", "") or "não definido"
except ValueError:
    idioma = os.environ.get("LANG", "não definido")
registrar(None, "Idioma do sistema", f"{idioma} (navegadores enviam isso em Accept-Language)")

# ── 5. Máquina ────────────────────────────────────────────────────────────
registrar(None, "Sistema", f"{platform.system()} {platform.release()} · Python {platform.python_version()}")

# ── Imprimir o resultado automático ───────────────────────────────────────
print("🔐 Checagem automática de OPSEC\n")
for simbolo, item, detalhe in verificacoes:
    print(f"  {simbolo} {item:<22} {detalhe}")

# ── Checklist humano (código nenhum faz isso por você) ────────────────────
CHECKLIST = [
    "A coleta tem autorização e finalidade definida (ofício, ordem de serviço, contrato)?",
    "Estou usando o ambiente de investigação (VM/navegador separado), não o meu pessoal?",
    "O proxy/VPN é de um provedor confiável e contratado (nunca proxy gratuito desconhecido)?",
    "Conferi o IP de saída ANTES de abrir o site do alvo (script 01)?",
    "Perfil 'fantoche' (se houver) está autorizado pela instituição e respeita os termos da plataforma?",
    "Não vou interagir com o alvo (curtir, seguir, mandar mensagem) sem decisão da equipe?",
    "Estou registrando data/hora, URL e hash de tudo o que coletar (Dia 14)?",
]
print("\n📋 Checklist humano (marque antes de começar):")
for item in CHECKLIST:
    print(f"  [ ] {item}")

# ── Guardar um registro da checagem ───────────────────────────────────────
saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
with open(saidas / "checagem_opsec.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(f"Checagem de OPSEC em {datetime.now(FUSO_BR):%d/%m/%Y %H:%M:%S} (Brasília)\n\n")
    for simbolo, item, detalhe in verificacoes:
        arquivo.write(f"{simbolo} {item}: {detalhe}\n")
    arquivo.write("\nChecklist humano:\n" + "\n".join(f"[ ] {i}" for i in CHECKLIST) + "\n")
print("\n💾 saidas/checagem_opsec.txt gravado.")
