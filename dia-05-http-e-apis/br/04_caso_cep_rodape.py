"""
Caso Vitrine Fantasma: o CEP do rodapé da loja leva a um depósito?

Carta 26 (rank B) — Jutsu do Mensageiro HTTP (aplicação no caso)

O que você aprende:
  • a extrair o CEP do rodapé da cópia salva do site (caso/dados/vitrine_megaoferta.html);
  • a tratar os erros HTTP mais comuns de APIs: 404 (não encontrado) e 429 (pediu demais);
  • a respeitar o cabeçalho Retry-After e tentar de novo com espera crescente;
  • a cruzar o endereço oficial do CEP com o que a loja promete.

Como rodar (dentro da pasta dia-05-http-e-apis):
    python br/04_caso_cep_rodape.py
    OSINT_OFFLINE=1 python br/04_caso_cep_rodape.py
"""

import json
import os
import re                   # expressão regular para achar o CEP no HTML (mais no Dia 11)
import time                 # esperar entre tentativas
import urllib.error         # os tipos de erro HTTP (HTTPError, URLError)
import urllib.request
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
TENTATIVAS = 3  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def pedir_com_paciencia(url, tentativas=TENTATIVAS):
    """GET que entende 404 e 429. Devolve o dicionário, ou None se o recurso não existe."""
    pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
    for tentativa in range(1, tentativas + 1):
        try:
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                return json.load(resposta)
        except urllib.error.HTTPError as erro:
            if erro.code == 404:
                # 404 = "não encontrei". Para CEP, significa CEP inexistente: não adianta insistir.
                print("   ❌ HTTP 404: o servidor diz que esse CEP não existe.")
                return None
            if erro.code == 429 and tentativa < tentativas:
                # 429 = "muitos pedidos". O servidor pode dizer quanto esperar (Retry-After).
                espera = int(erro.headers.get("Retry-After") or 2 ** tentativa)
                print(f"   ⏳ HTTP 429: pedimos rápido demais. Esperando {espera}s (tentativa {tentativa}).")
                time.sleep(espera)
                continue
            raise                       # outros erros sobem para quem chamou
    return None


# ── 1. Achar o CEP no rodapé da vitrine salva ─────────────────────────────
html = (PASTA_CASO / "vitrine_megaoferta.html").read_text(encoding="utf-8")
# Padrão: 5 dígitos, hífen opcional, 3 dígitos. O Dia 11 explica regex em detalhe.
achado = re.search(r"CEP\s*(\d{5}-?\d{3})", html)
cep_rodape = achado.group(1) if achado else "30130-010"
# Também pegamos a linha de endereço inteira para comparar depois.
linha_endereco = next((linha.strip() for linha in html.splitlines() if "CEP" in linha), "")
linha_endereco = re.sub(r"<[^>]+>", "", linha_endereco)      # tira as tags <p>...</p>
print(f"🏷️  Rodapé da loja: {linha_endereco}")
print(f"📮 CEP encontrado: {cep_rodape}\n")

# ── 2. Consultar o CEP (BrasilAPI) ────────────────────────────────────────
cep = cep_rodape.replace("-", "")
url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
dados = None
if not OFFLINE:
    try:
        dados = pedir_com_paciencia(url)
    except Exception as erro:
        print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
else:
    print("⚠️ MODO OFFLINE: usando a amostra local.")
if dados is None:
    dados = json.loads((PASTA_DIA / "dados" / "brasilapi_cep_30130010.json").read_text(encoding="utf-8"))

# ── 3. O que é esse endereço de verdade? ──────────────────────────────────
oficial = f"{dados.get('street')}, {dados.get('neighborhood')}, {dados.get('city')}/{dados.get('state')}"
print(f"🗺️  Endereço oficial do CEP: {oficial}")

# ── 4. Cruzar o que o SITE DIZ com o que a API RESPONDE ───────────────────
# Não decidimos de antemão o que a API "deveria" dizer: comparamos o que veio.
def simplificar(texto):
    """'Av. Afonso Pena' → 'afonso pena' (tira tipo de logradouro, acento e caixa)."""
    import unicodedata
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().casefold()
    t = re.sub(r"^(av\.?|avenida|r\.?|rua|pca\.?|praca|al\.?|alameda)\s+", "", t.strip())
    return " ".join(t.split())

rua_no_rodape = linha_endereco.split(",")[0].split("—")[0].strip()   # ex.: "Av. Afonso Pena"
rua_da_api = dados.get("street") or ""
print("\n🔍 Cruzamento (declarado x oficial):")
print(f"   • O site declara:  {rua_no_rodape!r}")
print(f"   • O CEP pertence a: {rua_da_api or '(API não informou logradouro)'!r}")
if rua_da_api and simplificar(rua_no_rodape) != simplificar(rua_da_api):
    print("   🚩 DIVERGÊNCIA: o logradouro do CEP não é o logradouro que a loja escreveu.")
    print("      CEPs de centro de cidade às vezes cobrem praças e cruzamentos, então isso é PISTA,")
    print("      não prova. Mas é exatamente o tipo de detalhe que golpista não confere.")
    conclusao = "Endereço declarado no rodapé não corresponde ao logradouro do CEP informado."
elif rua_da_api:
    print("   ✅ O logradouro bate. Ainda assim: o endereço tem cara de depósito de eletrônicos?")
    conclusao = "Logradouro confere com o CEP; verificar se o local é compatível com a operação."
else:
    conclusao = "API sem logradouro para o CEP; consultar outra fonte (ViaCEP)."
print(f"   • Bairro/cidade do CEP: {dados.get('neighborhood')}, {dados.get('city')}/{dados.get('state')}")

print(f"\n📝 Para o relatório: '{conclusao}'")
print("   Registre também a fonte (campo 'service' da BrasilAPI) e a data/hora da consulta.")
print("   Próximo passo sugerido pela Iara: olhar o local no Street View (sem sair da sala!).")
