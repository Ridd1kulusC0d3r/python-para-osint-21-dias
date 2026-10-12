"""
Navegar num JSON de verdade: a ficha de um CNPJ na BrasilAPI.

Carta 27 (rank B) — Jutsu do Mapa do JSON

O que você aprende:
  • a diferença entre dicionário {chave: valor} e lista [item, item] num JSON;
  • a usar .get("campo", "padrão") para não quebrar quando um campo falta;
  • a percorrer uma lista de dicionários (o quadro de sócios, "qsa");
  • a listar as chaves de um JSON desconhecido antes de sair escrevendo código.

Alvo de demonstração: o CNPJ 00.000.000/0001-91 (Banco do Brasil), um cadastro público
de empresa estatal. Dados de CNPJ são públicos por lei, mas sócios pessoas físicas
continuam tendo direitos pela LGPD: veja o README.

Como rodar (dentro da pasta dia-06-json):
    python br/01_cnpj_brasilapi.py
    OSINT_OFFLINE=1 python br/01_cnpj_brasilapi.py
"""

import json
import os
import urllib.request
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
CNPJ = "00.000.000/0001-91"  #@param {type:"string"}

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


# ── 1. Consultar ──────────────────────────────────────────────────────────
numeros = "".join(c for c in CNPJ if c.isdigit())        # a API quer só os 14 dígitos
dados = buscar_json(f"https://brasilapi.com.br/api/cnpj/v1/{numeros}", "brasilapi_cnpj_00000000000191.json")

# ── 2. Primeiro, reconhecer o terreno: que chaves vieram? ─────────────────
# Diante de um JSON novo, a primeira coisa é olhar as chaves. Isso evita "chutar" nomes.
chaves = sorted(k for k in dados if not k.startswith("_"))   # ignoramos o "_aviso" da amostra
print(f"🗝️  O JSON tem {len(chaves)} chaves no primeiro nível. Algumas: {', '.join(chaves[:8])}…\n")

# ── 3. Campos simples (texto e número) ────────────────────────────────────
# dados["campo"] quebra (KeyError) se o campo não existir; dados.get("campo", "—") não quebra.
print(f"🏢 Razão social:     {dados.get('razao_social', '—')}")
print(f"🏷️  Nome fantasia:    {dados.get('nome_fantasia') or '(sem nome fantasia)'}")
print(f"📌 Situação:         {dados.get('descricao_situacao_cadastral', '—')}")
print(f"🗓️  Início atividade: {dados.get('data_inicio_atividade', '—')}")
print(f"🏭 CNAE principal:   {dados.get('cnae_fiscal', '—')} · {dados.get('cnae_fiscal_descricao', '—')}")
print(f"⚖️  Natureza:         {dados.get('natureza_juridica', '—')}")
print(f"📍 Município/UF:     {dados.get('municipio', '—')}/{dados.get('uf', '—')}")

# Números vêm como número mesmo (float): dá para formatar em reais.
capital = dados.get("capital_social")
if isinstance(capital, (int, float)):
    # Truque para o padrão brasileiro: formata em inglês e troca os separadores.
    em_reais = f"{capital:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"💰 Capital social:   R$ {em_reais}")

# ── 4. Lista de dicionários: o quadro de sócios e administradores (QSA) ───
# "qsa" é uma LISTA. Cada item é um DICIONÁRIO com nome_socio, qualificacao_socio etc.
socios = dados.get("qsa", [])                 # se não vier, usamos lista vazia
print(f"\n👥 QSA: {len(socios)} pessoa(s)/empresa(s)")
for posicao, socio in enumerate(socios, start=1):
    print(f"   {posicao}. {socio.get('nome_socio', '?'):<22} → {socio.get('qualificacao_socio', '?')}")

# ── 5. Lista dentro do JSON: atividades secundárias ───────────────────────
secundarias = dados.get("cnaes_secundarios", [])
print(f"\n🏭 Atividades secundárias: {len(secundarias)}")
for cnae in secundarias[:3]:                  # [:3] = só as três primeiras
    print(f"   • {cnae.get('codigo')} {cnae.get('descricao')}")
