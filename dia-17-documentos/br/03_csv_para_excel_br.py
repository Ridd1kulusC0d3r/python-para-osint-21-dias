"""
CSV que abre certo no Excel brasileiro: ";", utf-8-sig e vírgula decimal.

Carta 38 (rank A) — Jutsu do Relatório Automático (parte 3)

O que você aprende:
  • por que um CSV "normal" (vírgula, UTF-8 sem BOM) abre bagunçado no Excel em português;
  • o que é o BOM do utf-8-sig e por que ele salva os acentos;
  • a escrever números com vírgula decimal (1.899,00) e datas dd/mm/aaaa;
  • a evitar a "injeção de fórmula" (CSV injection) ao exportar dados de terceiros.

Como rodar (dentro da pasta dia-17-documentos):
    python br/03_csv_para_excel_br.py
"""

import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
GERAR_VERSAO_ERRADA = True  #@param {type:"boolean"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"


def numero_br(valor):
    """Decimal('1899.00') → '1899,00' (sem separador de milhar: o Excel entende melhor)."""
    return f"{valor:.2f}".replace(".", ",")


def data_br(iso):
    """'2025-11-28' → '28/11/2025'."""
    ano, mes, dia = iso.split("-")
    return f"{dia}/{mes}/{ano}"


def seguro(texto):
    """Protege contra CSV injection: célula que começa com = + - @ vira texto.

    Se uma 'vítima' digitar =HIPERLINK("http://site-malicioso"...) no relato, o Excel
    executaria como fórmula. Um apóstrofo na frente faz o Excel tratar como texto.
    """
    return "'" + texto if texto[:1] in ("=", "+", "-", "@") else texto


# ── 1. Ler as denúncias ───────────────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = list(csv.DictReader(arquivo, delimiter=";"))

SAIDAS.mkdir(exist_ok=True)

# ── 2. (Didático) a versão ERRADA, para você comparar no Excel ───────────
if GERAR_VERSAO_ERRADA:
    with open(SAIDAS / "denuncias_ERRADO.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)                       # vírgula, sem BOM, ponto decimal
        escritor.writerow(["id", "data", "cidade", "produto", "valor"])
        for d in denuncias:
            escritor.writerow([d["id"], d["data"], d["cidade"], d["produto"], d["valor"]])
    print("❌ saidas/denuncias_ERRADO.csv: no Excel pt-BR tudo cai numa coluna só e 'Divinópolis' vira 'DivinÃ³polis'.")

# ── 3. A versão CERTA ─────────────────────────────────────────────────────
# utf-8-sig grava 3 bytes invisíveis no começo (EF BB BF, o "BOM"). É o sinal que o
# Excel procura para saber que o arquivo está em UTF-8. Sem ele, o Excel chuta Windows-1252.
with open(SAIDAS / "denuncias_excel_br.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.writer(f, delimiter=";")         # ";" porque no Brasil a vírgula é decimal
    escritor.writerow(["ID", "Data", "Cidade", "Produto", "Valor (R$)", "Relato"])
    for d in denuncias:
        escritor.writerow([d["id"], data_br(d["data"]), seguro(d["cidade"]),
                           seguro(d["produto"]), numero_br(Decimal(d["valor"])), seguro(d["relato_curto"])])
print("✅ saidas/denuncias_excel_br.csv: colunas separadas, acentos certos, valores somáveis.")

# ── 4. Uma tabela-resumo por mês (pronta para virar gráfico no Excel) ────
por_mes = defaultdict(lambda: [0, Decimal("0")])
for d in denuncias:
    mes = d["data"][:7]                              # '2025-11'
    por_mes[mes][0] += 1
    por_mes[mes][1] += Decimal(d["valor"])

NOMES_MES = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
             "agosto", "setembro", "outubro", "novembro", "dezembro"]
with open(SAIDAS / "resumo_por_mes.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.writer(f, delimiter=";")
    escritor.writerow(["Mês", "Denúncias", "Prejuízo (R$)"])
    for mes in sorted(por_mes):
        ano, m = mes.split("-")
        qtd, soma = por_mes[mes]
        escritor.writerow([f"{NOMES_MES[int(m)]}/{ano}", qtd, numero_br(soma)])
        print(f"   {NOMES_MES[int(m)]:>9}/{ano}: {qtd:>2} denúncias · R$ {numero_br(soma)}")
print("✅ saidas/resumo_por_mes.csv gravado.")

# ── 5. Prova de que o BOM está lá ─────────────────────────────────────────
primeiros = (SAIDAS / "denuncias_excel_br.csv").read_bytes()[:3]
print(f"\n🔬 Primeiros 3 bytes do arquivo certo: {primeiros.hex(' ').upper()}  (EF BB BF = BOM do UTF-8)")
print("💡 Ao ler esse arquivo de volta no Python, use encoding='utf-8-sig' para o BOM não grudar no 1º cabeçalho.")
