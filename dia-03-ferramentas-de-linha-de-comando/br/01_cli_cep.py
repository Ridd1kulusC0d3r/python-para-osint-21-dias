"""
Sua primeira ferramenta de linha de comando: consultar um CEP com --cep e --formato.

Carta 24 (rank B) — Jutsu da Ferramenta de Campo (parte 1)

O que você aprende:
  • o que são "argumentos de linha de comando" (o que vem depois do nome do script);
  • a criar opções como --cep e --formato com argparse (nativo), com ajuda automática (--help);
  • a validar a entrada antes de gastar uma consulta;
  • a devolver o resultado em formatos diferentes: texto para gente, JSON ou CSV para máquina.

Usa a BrasilAPI (https://brasilapi.com.br/api/cep/v2/{cep}). No Dia 5 você aprende HTTP a fundo;
aqui o foco é a "casca" da ferramenta.

Como rodar (dentro da pasta dia-03-ferramentas-de-linha-de-comando):
    python br/01_cli_cep.py                         # usa o CEP padrão (parâmetro abaixo)
    python br/01_cli_cep.py --cep 30130-010
    python br/01_cli_cep.py --cep 30130010 --formato json
    python br/01_cli_cep.py --help                  # a ajuda que o argparse escreve sozinho
    OSINT_OFFLINE=1 python br/01_cli_cep.py         # sem internet, usa dados/
"""

import argparse             # o "leitor" de argumentos de linha de comando
import json
import os
import sys                  # sys.exit para sair com código de erro
import urllib.request
from pathlib import Path

# ── Parâmetros (valem quando você NÃO passa --cep / --formato) ────────────
CEP_PADRAO = "30130-010"  #@param {type:"string"}
FORMATO_PADRAO = "texto"  #@param ["texto", "json", "csv"]

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
            # Mensagens de aviso vão para stderr: assim não "sujam" a saída JSON/CSV (stdout).
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.", file=sys.stderr)
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.", file=sys.stderr)
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


# ── 1. Descrever as opções da ferramenta ──────────────────────────────────
# O ArgumentParser monta, sozinho, a mensagem de --help e as mensagens de erro.
parser = argparse.ArgumentParser(
    prog="cli_cep",
    description="Consulta um CEP na BrasilAPI e mostra o endereço.",
    epilog="Exemplo: python br/01_cli_cep.py --cep 30130-010 --formato json",
)
parser.add_argument("--cep", default=CEP_PADRAO,
                    help=f"CEP com ou sem traço (padrão: {CEP_PADRAO})")
parser.add_argument("--formato", choices=["texto", "json", "csv"], default=FORMATO_PADRAO,
                    help="como mostrar o resultado (padrão: %(default)s)")

# parse_known_args (em vez de parse_args) ignora argumentos "estranhos". Isso evita erro
# no Colab/Jupyter, que passa os próprios argumentos escondidos para o Python.
args, _ = parser.parse_known_args()

# ── 2. Validar ANTES de consultar ─────────────────────────────────────────
# Ficamos só com os dígitos; um CEP tem exatamente 8.
cep = "".join(c for c in args.cep if c.isdigit())
if len(cep) != 8:
    print(f"❌ CEP inválido: {args.cep!r} (precisa de 8 dígitos).", file=sys.stderr)
    sys.exit(2)                 # código 2 = "uso errado" (convenção de ferramentas de terminal)

# ── 3. Consultar ──────────────────────────────────────────────────────────
# Só existe amostra offline do CEP 30130-010. Para outro CEP sem internet, avisamos.
amostra = "cep_30130010.json"
if (OFFLINE and cep != "30130010"):
    print(f"⚠️  Não há amostra para {cep}; mostrando a do 30130-010 só como exemplo.", file=sys.stderr)
dados = buscar_json(f"https://brasilapi.com.br/api/cep/v2/{cep}", amostra)

# Os campos que nos interessam (usamos .get para não quebrar se algum faltar).
campos = {
    "cep": dados.get("cep", cep),
    "logradouro": dados.get("street", ""),
    "bairro": dados.get("neighborhood", ""),
    "cidade": dados.get("city", ""),
    "uf": dados.get("state", ""),
    "fonte": dados.get("service", ""),
}

# ── 4. Mostrar no formato pedido ──────────────────────────────────────────
if args.formato == "json":
    # JSON: bom para outro programa ler. ensure_ascii=False mantém os acentos.
    print(json.dumps(campos, ensure_ascii=False, indent=2))
elif args.formato == "csv":
    # CSV com ";" (padrão do Excel em português): cabeçalho + uma linha.
    print(";".join(campos.keys()))
    print(";".join(str(v) for v in campos.values()))
else:
    print(f"📮 CEP {campos['cep'][:5]}-{campos['cep'][5:]}")
    print(f"   🛣️  {campos['logradouro'] or '(sem logradouro: CEP geral da cidade?)'}")
    print(f"   🏘️  {campos['bairro']} — {campos['cidade']}/{campos['uf']}")
    print(f"   🔗 fonte dos dados: {campos['fonte']}")
