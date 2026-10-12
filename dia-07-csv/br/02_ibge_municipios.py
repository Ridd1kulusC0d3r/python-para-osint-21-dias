"""
Baixar a lista oficial de municípios de MG (API do IBGE) e salvar em CSV.

Carta 28 (rank B) — Jutsu da Planilha Viva (parte 2)

O que você aprende:
  • a transformar JSON aninhado em linhas de planilha (o "json_to_csv" do original, em versão BR);
  • a se proteger de campos que vêm null ("microrregiao": null em alguns municípios);
  • csv.DictWriter com delimiter=";" e encoding="utf-8-sig" (o Excel em português abre certinho).

Como rodar (dentro da pasta dia-07-csv):
    python br/02_ibge_municipios.py
    OSINT_OFFLINE=1 python br/02_ibge_municipios.py
"""

import csv
import gzip
import json
import os
import urllib.request
from pathlib import Path

UF = "MG"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"
SAIDAS = PASTA_DIA / "saidas"



def ler_resposta(resposta):
    """Lê a resposta HTTP e devolve o texto, descompactando se vier em gzip.

    O IBGE responde COMPACTADO (gzip) mesmo quando não pedimos. O urllib não
    descompacta sozinho, então olhamos os 2 primeiros bytes: 0x1f 0x8b é a
    "assinatura" de todo arquivo gzip (os números mágicos que você vê no Dia 14).
    """
    dados = resposta.read()
    if dados[:2] == b"\x1f\x8b" or resposta.headers.get("Content-Encoding") == "gzip":
        dados = gzip.decompress(dados)
    return dados.decode("utf-8")

def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=30) as resposta:
                return json.loads(ler_resposta(resposta))
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


def caminho(dicionario, *chaves):
    """Anda por várias chaves sem quebrar: caminho(m, "microrregiao", "nome").

    Se qualquer degrau for None ou faltar, devolve "" em vez de dar erro.
    (dados.get("microrregiao", {}) NÃO basta: se a chave existe com valor null,
    o .get devolve None, e None.get(...) quebra.)
    """
    atual = dicionario
    for chave in chaves:
        if not isinstance(atual, dict):
            return ""
        atual = atual.get(chave)
    return atual if atual is not None else ""


# ── 1. Baixar ─────────────────────────────────────────────────────────────
url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios"
resposta = buscar_json(url, "ibge_municipios_mg.json")
# A API real devolve uma LISTA; a amostra guarda a lista dentro de "municipios" (para ter o _aviso).
municipios = resposta if isinstance(resposta, list) else resposta.get("municipios", [])
print(f"🏙️  {len(municipios)} municípios recebidos para {UF}")

# ── 2. Achatar: cada município vira UMA linha com colunas simples ─────────
linhas = []
sem_micro = []
for m in municipios:
    if m.get("microrregiao") is None:
        sem_micro.append(m.get("nome"))
    linhas.append({
        "codigo_ibge": m.get("id"),
        "municipio": m.get("nome"),
        "microrregiao": caminho(m, "microrregiao", "nome"),
        "mesorregiao": caminho(m, "microrregiao", "mesorregiao", "nome"),
        # Divisão regional mais nova do IBGE (2017): regiões imediatas e intermediárias.
        "regiao_imediata": caminho(m, "regiao-imediata", "nome"),
        "regiao_intermediaria": caminho(m, "regiao-imediata", "regiao-intermediaria", "nome"),
    })

if sem_micro:
    print(f"⚠️  Vieram com microrregiao = null: {', '.join(sem_micro)} (nosso código não quebrou 😉)")

# ── 3. Gravar o CSV ───────────────────────────────────────────────────────
SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / f"municipios_{UF.lower()}.csv"
# utf-8-sig coloca uma "assinatura" (BOM) no início: é o sinal para o Excel ler como UTF-8.
with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]), delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)
print(f"💾 {destino.relative_to(PASTA_DIA)} gravado com {len(linhas)} linhas.\n")

# ── 4. Conferir: reler as 5 primeiras linhas ──────────────────────────────
with open(destino, encoding="utf-8-sig", newline="") as arquivo:
    for i, linha in enumerate(csv.DictReader(arquivo, delimiter=";")):
        if i == 5:
            break
        print(f"   {linha['codigo_ibge']}  {linha['municipio']:<22} {linha['mesorregiao']}")
