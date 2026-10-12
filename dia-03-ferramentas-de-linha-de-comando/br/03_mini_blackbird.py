"""
Mini-blackbird: o username existe nestes sites? Uma versão de bolso, só com stdlib.

Carta 24 (rank B) — Jutsu da Ferramenta de Campo (parte 3)

O que você aprende:
  • como ferramentas como blackbird, Sherlock e Maigret decidem se um perfil "existe";
  • a usar o código de status HTTP (200 = achou, 404 = não achou) e, quando ele mente,
    a olhar o CONTEÚDO da resposta;
  • a descrever sites como DADOS (uma lista de dicionários), no mesmo espírito do WhatsMyName;
  • a fazer poucos pedidos, com pausa e User-Agent honesto.

As regras dos três sites abaixo seguem o projeto WhatsMyName (CC BY-SA 4.0), que é a base
do blackbird hoje.

Como rodar (dentro da pasta dia-03-ferramentas-de-linha-de-comando):
    python br/03_mini_blackbird.py
    python br/03_mini_blackbird.py --username outro_nome   # igual ao "-u" do blackbird
    OSINT_OFFLINE=1 python br/03_mini_blackbird.py          # usa a amostra de dados/
"""

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
# Padrão: o próprio autor do curso, que tem perfil público no GitHub.
USERNAME = "cipher387"  #@param {type:"string"}
PAUSA_SEGUNDOS = 1  #@param {type:"number"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# Como no script 01: a opção --username, se for passada, vence o parâmetro do topo.
parser = argparse.ArgumentParser(description="Verifica se um username existe em GitHub, GitLab e Codeberg.")
parser.add_argument("-u", "--username", default=USERNAME, help="username a procurar (padrão: %(default)s)")
USERNAME = parser.parse_known_args()[0].username

# ── 1. Os sites, descritos como dados ─────────────────────────────────────
# Para cada site: onde perguntar ("{u}" vira o username), qual status indica "existe",
# e um trecho de texto que confirma. Usamos as APIs públicas, que respondem JSON.
SITES = [
    {"nome": "GitHub", "url": "https://api.github.com/users/{u}", "perfil": "https://github.com/{u}",
     "achou_status": 200, "achou_texto": '"login"'},
    # O GitLab responde 200 SEMPRE; a diferença está no corpo: [] (lista vazia) = não existe.
    {"nome": "GitLab", "url": "https://gitlab.com/api/v4/users?username={u}", "perfil": "https://gitlab.com/{u}",
     "achou_status": 200, "achou_texto": '"id"'},
    {"nome": "Codeberg", "url": "https://codeberg.org/api/v1/users/{u}", "perfil": "https://codeberg.org/{u}",
     "achou_status": 200, "achou_texto": '"id"'},
]


def perguntar(url):
    """Devolve (status, corpo_em_texto). 404 também é uma resposta válida: o servidor RESPONDEU."""
    pedido = urllib.request.Request(url, headers={
        "User-Agent": "python-para-osint-21-dias/estudo",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(pedido, timeout=15) as resposta:
            return resposta.status, resposta.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as erro:          # 404, 403, 429... chegam aqui
        return erro.code, erro.read().decode("utf-8", errors="replace")


# ── 2. Amostra offline (respostas guardadas no formato real de cada API) ──
amostra = None
if OFFLINE:
    print("⚠️ MODO OFFLINE: usando a amostra local.")
    amostra = json.loads((PASTA_DIA / "dados" / "mini_blackbird_cipher387.json").read_text(encoding="utf-8"))
    if USERNAME != "cipher387":
        print(f"   (a amostra só existe para 'cipher387'; {USERNAME!r} não foi consultado)")
    USERNAME = "cipher387"          # a amostra só existe para este username

# Validar o username: só letras, números, ponto, hífen e sublinhado.
# Isso também evita montar URLs estranhas com espaço, "/" ou "?".
permitidos = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
if not USERNAME or not set(USERNAME) <= permitidos:
    raise SystemExit(f"❌ Username inválido: {USERNAME!r}")

print(f"🔎 Procurando o username {USERNAME!r} em {len(SITES)} sites\n")
print(f"{'Site':<10} {'Status':>6}  Resultado")
print("─" * 60)

# ── 3. Perguntar a cada site ──────────────────────────────────────────────
encontrados = []
for site in SITES:
    url = site["url"].format(u=urllib.parse.quote(USERNAME))
    if amostra is not None:
        status = amostra[site["nome"]]["status"]
        corpo = json.dumps(amostra[site["nome"]]["corpo"])
    else:
        try:
            status, corpo = perguntar(url)
        except Exception as erro:                   # sem internet, DNS, timeout...
            print(f"⚠️ MODO OFFLINE: {site['nome']} não respondeu ({type(erro).__name__}).")
            continue
        time.sleep(PAUSA_SEGUNDOS)                  # educação: uma pausa entre sites

    # A decisão: status certo E o texto que confirma.
    if status == site["achou_status"] and site["achou_texto"] in corpo:
        resultado = "✅ existe  → " + site["perfil"].format(u=USERNAME)
        encontrados.append(site["nome"])
    elif status in (403, 429):
        resultado = "🟡 bloqueado/limite de pedidos: tente mais tarde"
    else:
        resultado = "❌ não encontrado"
    print(f"{site['nome']:<10} {status:>6}  {resultado}")

# ── 4. Resumo e cautela ───────────────────────────────────────────────────
print("─" * 60)
print(f"📊 Encontrado em {len(encontrados)} de {len(SITES)} sites: {', '.join(encontrados) or 'nenhum'}")
print("⚖️  Mesmo username em dois sites NÃO prova que é a mesma pessoa. Confirme com outros elementos")
print("   (foto, bio, links cruzados, datas). E lembre: o servidor registra o seu IP a cada consulta.")
