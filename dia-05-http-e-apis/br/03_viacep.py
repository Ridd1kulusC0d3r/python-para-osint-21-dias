"""
ViaCEP x BrasilAPI: duas fontes para o mesmo CEP (e o que fazer quando o CEP não existe).

Carta 26 (rank B) — Jutsu do Mensageiro HTTP (parte 3)

O que você aprende:
  • a consultar o ViaCEP, outra API pública de CEP;
  • que "CEP inexistente" no ViaCEP NÃO é erro HTTP: vem status 200 com {"erro": "true"};
  • a tratar o campo "erro" tanto como texto ("true") quanto como booleano (true);
  • a comparar duas fontes campo a campo (regra de ouro do OSINT: confirmar).

Como rodar (dentro da pasta dia-05-http-e-apis):
    python br/03_viacep.py
    OSINT_OFFLINE=1 python br/03_viacep.py
"""

import json
import os
import unicodedata          # comparar textos ignorando acentos
import urllib.request
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
CEP = "30130-010"  #@param {type:"string"}
CEP_INEXISTENTE = "99999-999"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                return json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


def so_digitos(texto):
    """'30130-010' → '30130010'."""
    return "".join(c for c in texto if c.isdigit())


def cep_nao_existe(resposta):
    """O ViaCEP sinaliza CEP inexistente com "erro": "true" (texto) ou true (booleano)."""
    return str(resposta.get("erro", "")).lower() == "true"


def normalizar(texto):
    """Tira acentos e deixa minúsculo, para comparar 'Praça' com 'Praca'."""
    sem_acento = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode()
    return sem_acento.casefold().strip()


# ── 1. Consulta no ViaCEP ─────────────────────────────────────────────────
cep = so_digitos(CEP)
via = buscar_json(f"https://viacep.com.br/ws/{cep}/json/", "viacep_30130010.json")
if cep_nao_existe(via):
    raise SystemExit(f"O ViaCEP diz que {CEP} não existe.")
print(f"📮 ViaCEP:    {via.get('logradouro')} · {via.get('bairro')} · {via.get('localidade')}/{via.get('uf')}")
print(f"   extras:    código IBGE {via.get('ibge')} · DDD {via.get('ddd')}")

# ── 2. Mesma pergunta à BrasilAPI ─────────────────────────────────────────
bra = buscar_json(f"https://brasilapi.com.br/api/cep/v2/{cep}", "brasilapi_cep_30130010.json")
print(f"📮 BrasilAPI: {bra.get('street')} · {bra.get('neighborhood')} · {bra.get('city')}/{bra.get('state')}")

# ── 3. Comparar campo a campo ─────────────────────────────────────────────
# Os nomes dos campos são diferentes em cada API; este dicionário faz a "tradução".
pares = {"logradouro": "street", "bairro": "neighborhood", "localidade": "city", "uf": "state"}
print("\n🔍 Comparação:")
divergencias = 0
for campo_via, campo_bra in pares.items():
    a, b = via.get(campo_via, ""), bra.get(campo_bra, "")
    igual = normalizar(a) == normalizar(b)
    divergencias += not igual          # True conta como 1, False como 0
    print(f"   {'✅' if igual else '🚩'} {campo_via:<11} ViaCEP={a!r:<28} BrasilAPI={b!r}")
print("   → As fontes concordam." if divergencias == 0 else f"   → {divergencias} divergência(s): anote e investigue.")

# ── 4. E quando o CEP não existe? ─────────────────────────────────────────
print(f"\n🧪 Testando um CEP que não existe: {CEP_INEXISTENTE}")
falso = buscar_json(f"https://viacep.com.br/ws/{so_digitos(CEP_INEXISTENTE)}/json/", "viacep_inexistente.json")
if cep_nao_existe(falso):
    print("   ❌ ViaCEP respondeu {'erro': 'true'}: o pedido deu certo (HTTP 200), mas o CEP não existe.")
    print("   💡 Por isso não basta checar o status HTTP: leia também o corpo da resposta.")
else:
    print(f"   Resposta: {falso}")
