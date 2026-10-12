"""
Gabarito do Desafio S do Dia 17 — Fábrica de ofícios.

Para cada chave PIX que recebeu dinheiro, gera um ofício em HTML (um arquivo por instituição)
a partir de UM modelo com string.Template, com a lista de transações daquela chave.
No fim, grava um índice com o SHA-256 de cada ofício gerado.
100% offline: usa só caso/dados/.
"""

import csv
import hashlib
import html
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from string import Template          # modelo com $variaveis, da biblioteca padrão

NUMERO_BASE = 300  #@param {type:"integer"}
CIDADE_EMISSAO = "Belo Horizonte"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas" / "oficios"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

MODELO = Template("""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Ofício $numero</title>
<style>body{font-family:Georgia,serif;max-width:720px;margin:2rem auto;line-height:1.5}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #999;padding:.3rem .5rem}
.num{text-align:right}</style></head><body>
<p><b>NÚCLEO DE FONTES ABERTAS (fictício)</b><br>Ofício nº $numero/2025 — Operação Vitrine Fantasma</p>
<p>$cidade, $data_extenso.</p>
<p>À <b>$banco</b><br>Setor de atendimento a autoridades</p>
<p><b>Assunto:</b> solicitação de dados cadastrais e de movimentação da chave PIX <code>$chave</code>.</p>
<p>Em apoio à investigação conduzida pela Delegada Rita Assunção, solicitamos os dados cadastrais
do(a) titular <b>$titular</b> e o extrato das operações abaixo, que somam <b>$total</b> em
<b>$quantidade</b> transferências declaradas por vítimas.</p>
<table><tr><th>Data</th><th>Denúncia</th><th>Valor</th></tr>
$linhas
</table>
<p>Atenciosamente,<br><br>__________________________<br>Analista do NFA</p>
</body></html>
""")


def reais(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")


# ── Dados ────────────────────────────────────────────────────────────────
ficha = json.loads((PASTA_CASO / "ficha_do_caso.json").read_text(encoding="utf-8"))
contas = {c["chave"]: c for c in ficha["contas_laranja"]}

por_chave = defaultdict(list)
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    for d in csv.DictReader(arquivo, delimiter=";"):
        por_chave[d["chave_pix_destino"]].append(d)

hoje = datetime.now(FUSO)
data_extenso = f"{hoje.day} de {MESES[hoje.month - 1]} de {hoje.year}"
SAIDAS.mkdir(parents=True, exist_ok=True)

indice = []
for n, (chave, transacoes) in enumerate(sorted(por_chave.items()), start=NUMERO_BASE):
    conta = contas.get(chave, {"titular": "(desconhecido)", "banco": "(instituição a identificar)"})
    transacoes.sort(key=lambda d: d["data"])
    linhas = "\n".join(
        f"<tr><td>{'/'.join(reversed(d['data'].split('-')))}</td><td>{html.escape(d['id'])}</td>"
        f"<td class='num'>{reais(Decimal(d['valor']))}</td></tr>"
        for d in transacoes
    )
    total = sum(Decimal(d["valor"]) for d in transacoes)
    # substitute() exige TODAS as variáveis: se faltar uma, dá erro (melhor que um ofício incompleto).
    documento = MODELO.substitute(
        numero=n, cidade=html.escape(CIDADE_EMISSAO), data_extenso=data_extenso,
        banco=html.escape(conta["banco"]), titular=html.escape(conta["titular"]),
        chave=html.escape(chave), total=reais(total), quantidade=len(transacoes), linhas=linhas,
    )
    nome = f"oficio_{n}_{chave[:8]}.html"
    (SAIDAS / nome).write_text(documento, encoding="utf-8")
    hash_doc = hashlib.sha256(documento.encode("utf-8")).hexdigest()
    indice.append({"oficio": n, "arquivo": nome, "banco": conta["banco"], "titular": conta["titular"],
                   "transacoes": len(transacoes), "total": f"{total:.2f}".replace(".", ","), "sha256": hash_doc})
    print(f"📨 Ofício {n}: {conta['banco']:<30} {len(transacoes):>2} transações · {reais(total):>13}")

with open(SAIDAS / "indice_oficios.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=list(indice[0]), delimiter=";")
    escritor.writeheader()
    escritor.writerows(indice)

soma = sum(Decimal(i["total"].replace(",", ".")) for i in indice)
print(f"\n✅ {len(indice)} ofícios · soma {reais(soma)} (confere com o total das denúncias)")
print("💾 saidas/oficios/ + indice_oficios.csv (com SHA-256 de cada ofício)")
