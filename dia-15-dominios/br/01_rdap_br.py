"""
RDAP: o "WHOIS moderno", em JSON, consultado só com a biblioteca padrão.

Carta 36 (rank A) — Jutsu do Registro Estruturado

O que você aprende:
  • o que é RDAP e por que ele está substituindo o WHOIS;
  • como descobrir QUAL servidor RDAP atende um domínio (bootstrap da IANA);
  • como ler datas de registro, alteração e expiração, servidores DNS e status.

Como rodar (dentro da pasta dia-15-dominios):
    python br/01_rdap_br.py
    OSINT_OFFLINE=1 python br/01_rdap_br.py   # sem internet, usa dados/
"""

import json                 # converter o texto JSON em dicionário Python
import os                   # ler a variável de ambiente OSINT_OFFLINE
import urllib.request       # fazer requisições HTTP sem instalar nada
from datetime import datetime, timezone  # calcular a idade do domínio
from pathlib import Path    # montar caminhos de arquivo

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
DOMINIO = "registro.br"  #@param {type:"string"}

# ── Onde estão as amostras offline ────────────────────────────────────────
# Funciona rodando como script (python br/01_rdap_br.py) e como célula do Colab.
PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            # Alguns servidores recusam pedidos sem User-Agent; nos identificamos.
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                return json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


# ── Passo 1: descobrir o servidor RDAP certo ──────────────────────────────
# A IANA publica um arquivo "bootstrap" dizendo qual servidor responde por
# cada terminação (TLD). Ex.: ".br" → https://rdap.registro.br/
bootstrap = buscar_json("https://data.iana.org/rdap/dns.json", "iana_rdap_dns.json")

tld = DOMINIO.rsplit(".", 1)[-1].lower()   # "registro.br" → "br"
servidor = None
for terminacoes, urls in bootstrap["services"]:   # cada item: [[tlds], [urls]]
    if tld in terminacoes:
        servidor = urls[0]                         # pegamos o primeiro servidor
        break

if servidor is None:
    raise SystemExit(f"Nenhum servidor RDAP conhecido para .{tld}")

print(f"🔎 Servidor RDAP para .{tld}: {servidor}")

# ── Passo 2: consultar o domínio ──────────────────────────────────────────
# O caminho padrão do RDAP é /domain/<nome>. Garantimos uma barra entre eles.
url = servidor.rstrip("/") + "/domain/" + DOMINIO
dados = buscar_json(url, "rdap_registro_br.json")

print(f"\n🌐 Domínio: {dados.get('ldhName', DOMINIO)}")
print(f"📌 Status:  {', '.join(dados.get('status', []))}")

# ── Passo 3: eventos (datas) ──────────────────────────────────────────────
# "events" é uma lista de {eventAction, eventDate}. Guardamos num dicionário.
datas = {e["eventAction"]: e["eventDate"] for e in dados.get("events", [])}
for acao, quando in datas.items():
    print(f"🗓️  {acao:<14} → {quando}")

# ── Passo 4: idade do domínio (sinal de alerta clássico) ──────────────────
if "registration" in datas:
    # fromisoformat entende "2025-10-02T14:31:08Z" se trocarmos o Z por +00:00
    criado = datetime.fromisoformat(datas["registration"].replace("Z", "+00:00"))
    idade = (datetime.now(timezone.utc) - criado).days
    print(f"\n⏳ Idade do domínio: {idade} dias")
    if idade < 90:
        print("🚩 Domínio com menos de 90 dias: combine com outros sinais antes de concluir algo.")

# ── Passo 5: servidores DNS ───────────────────────────────────────────────
for ns in dados.get("nameservers", []):
    print(f"🧭 Nameserver: {ns.get('ldhName')}")
