"""
Relatório preliminar do caso em Markdown (.md), gerado por código.

Carta 38 (rank A) — Jutsu do Relatório Automático

O que você aprende:
  • a juntar números de várias fontes num texto pronto para ler;
  • a escrever tabelas em Markdown (o formato do GitHub, do Obsidian e do Notion);
  • a formatar dinheiro em reais (R$ 54.877,40) e datas em dd/mm/aaaa;
  • por que um relatório gerado por script é reprodutível (e um copia-e-cola não é).

Como rodar (dentro da pasta dia-17-documentos):
    python br/01_relatorio_markdown.py
"""

import csv
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal          # dinheiro sem erro de arredondamento
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
ANALISTA = "Analista NFA"  #@param {type:"string"}
NUMERO_DO_RELATORIO = "NFA-2025-117"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

# Fuso de Brasília. No Windows pode faltar a base de fusos (tzdata): usamos -03:00 fixo.
try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))


def reais(valor):
    """Decimal('54877.4') → 'R$ 54.877,40' (ponto no milhar, vírgula no centavo)."""
    texto = f"{valor:,.2f}"                    # '54,877.40' (padrão americano)
    # Trocamos em três tempos para não confundir os símbolos:
    return "R$ " + texto.replace(",", "§").replace(".", ",").replace("§", ".")


# ── 1. Ler as fontes ──────────────────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = list(csv.DictReader(arquivo, delimiter=";"))
ficha = json.loads((PASTA_CASO / "ficha_do_caso.json").read_text(encoding="utf-8"))
rdap = json.loads((PASTA_CASO / "rdap_megaoferta.json").read_text(encoding="utf-8"))

# ── 2. Calcular os números do relatório ───────────────────────────────────
total = sum(Decimal(d["valor"]) for d in denuncias)
datas = sorted(date.fromisoformat(d["data"]) for d in denuncias)
eventos = {e["eventAction"]: e["eventDate"] for e in rdap["events"]}
criado = datetime.fromisoformat(eventos["registration"].replace("Z", "+00:00")).date()

por_chave = defaultdict(lambda: [0, Decimal("0")])   # chave → [quantidade, soma]
for d in denuncias:
    por_chave[d["chave_pix_destino"]][0] += 1
    por_chave[d["chave_pix_destino"]][1] += Decimal(d["valor"])
titular = {c["chave"]: c["titular"] for c in ficha["contas_laranja"]}

produtos = Counter(d["produto"] for d in denuncias)

# ── 3. Escrever o Markdown ────────────────────────────────────────────────
# Uma lista de linhas que depois juntamos com "\n". Mais fácil de ler que um textão.
agora = datetime.now(FUSO)
md = [
    f"# Relatório preliminar {NUMERO_DO_RELATORIO} — Operação Vitrine Fantasma",
    "",
    f"**Gerado em:** {agora:%d/%m/%Y %H:%M} (horário de Brasília)  ",
    f"**Responsável:** {ANALISTA}  ",
    "**Classificação:** uso interno · dados fictícios de estudo",
    "",
    "## 1. Resumo",
    "",
    f"- **{len(denuncias)} denúncias** recebidas entre {datas[0]:%d/%m/%Y} e {datas[-1]:%d/%m/%Y}.",
    f"- **Prejuízo declarado:** {reais(total)}.",
    f"- **Domínio:** `{ficha['dominio']}`, criado em {criado:%d/%m/%Y} "
    f"(**{(datas[0] - criado).days} dias** antes da primeira denúncia).",
    f"- **CNPJ do rodapé:** {ficha['cnpj_rodape']} (dígito verificador inválido, ver Dia 2).",
    "",
    "## 2. Para onde foi o dinheiro (chaves PIX)",
    "",
    "| Chave PIX | Titular | Denúncias | Valor |",       # cabeçalho da tabela
    "|---|---|---:|---:|",                               # ---: alinha à direita
]
for chave, (qtd, soma) in sorted(por_chave.items(), key=lambda item: -item[1][1]):
    md.append(f"| `{chave[:8]}…` | {titular.get(chave, '?')} | {qtd} | {reais(soma)} |")

md += ["", "## 3. Produtos anunciados", "", "| Produto | Denúncias |", "|---|---:|"]
for produto, qtd in produtos.most_common():
    # O "|" é o separador de colunas; se aparecer no texto, escapamos com "\|".
    md.append(f"| {produto.replace('|', chr(92) + '|')} | {qtd} |")

md += [
    "",
    "## 4. Próximos passos",
    "",
    "- [ ] Ofício às instituições de pagamento das três chaves PIX.",
    "- [ ] Pedido de dados cadastrais do domínio ao registrador.",
    "- [ ] Mapa das vítimas por cidade (Dia 18) e linha do tempo (Dia 19).",
    "",
    "---",
    "*Relatório gerado automaticamente por `br/01_relatorio_markdown.py`. "
    "Rodar de novo com os mesmos dados produz os mesmos números.*",
]

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "relatorio_preliminar.md"
destino.write_text("\n".join(md) + "\n", encoding="utf-8")

print("\n".join(md[:16]))
print("…")
print(f"\n💾 {destino.relative_to(PASTA_DIA)} gravado ({len(md)} linhas). Abra no VS Code, GitHub ou Obsidian.")
