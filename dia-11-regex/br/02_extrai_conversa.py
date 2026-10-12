"""
A conversa: extrair entidades do export do WhatsApp com regex.

Carta 32 (rank A) — Jutsu do Padrão Brasileiro (aplicação no caso)

O que você aprende:
  • a aplicar várias regex no mesmo texto e montar uma tabela entidade → ocorrências;
  • a usar finditer para saber EM QUE LINHA cada coisa apareceu;
  • a "mascarar" o que já foi achado para um padrão não roubar pedaço de outro
    (ex.: dígitos dentro de uma chave PIX parecendo telefone);
  • a separar data, hora, autor e mensagem de cada linha com grupos nomeados.

Este script é 100% offline: lê caso/dados/conversa_whatsapp.txt (fictício).

Como rodar (dentro da pasta dia-11-regex):
    python br/02_extrai_conversa.py
"""

import csv
import re
from pathlib import Path

ARQUIVO = "conversa_whatsapp.txt"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# Ordem importa: os mais "compridos e específicos" primeiro (PIX, e-mail, CNPJ),
# depois os que poderiam casar com pedaços deles (CPF, telefone, CEP).
PADROES = {
    "Chave PIX aleatória": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    "E-mail": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "CNPJ": r"(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}(?!\d)",
    "CPF": r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)",
    "Telefone": r"(?<!\d)(?:\+?55[\s-]?)?\(?[1-9]\d\)?[\s-]?(?:9[\s-]?)?\d{4}[\s-]?\d{4}(?!\d)",
    "CEP": r"(?<!\d)\d{5}-\d{3}(?!\d)",
    "Valor em R$": r"R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?",
}

# Linha do export: "[28/11/2025 21:14] Kau Ofertas: mensagem"
# (?P<nome>...) é um GRUPO NOMEADO: depois pegamos com m["nome"].
LINHA = re.compile(r"^\[(?P<data>\d{2}/\d{2}/\d{4}) (?P<hora>\d{2}:\d{2})\] (?P<autor>[^:]+): (?P<msg>.*)$")

texto = (PASTA_CASO / ARQUIVO).read_text(encoding="utf-8")

achados = {nome: [] for nome in PADROES}      # entidade → lista de (valor, nº da linha, autor)
for numero, linha in enumerate(texto.splitlines(), start=1):
    m = LINHA.match(linha)
    if not m:
        continue                               # linha fora do padrão (ex.: mensagem com quebra)
    msg = m["msg"]
    for nome, padrao in PADROES.items():
        for achado in re.finditer(padrao, msg):
            achados[nome].append((achado.group(), numero, m["autor"]))
        # Mascarar: troca o que foi achado por "#" do mesmo tamanho. Assim os
        # próximos padrões não enxergam mais esses caracteres.
        msg = re.sub(padrao, lambda a: "#" * len(a.group()), msg)

# ── Tabela entidade → ocorrências ─────────────────────────────────────────
print(f"{'Entidade':<22} {'Qtde':>4}  Valores (linha · autor)")
print("─" * 78)
for nome, lista in achados.items():
    if not lista:
        continue
    print(f"{nome:<22} {len(lista):>4}  {lista[0][0]}  (l.{lista[0][1]} · {lista[0][2]})")
    for valor, numero, autor in lista[1:]:
        print(f"{'':<28}{valor}  (l.{numero} · {autor})")

# ── O que o VENDEDOR revelou (só mensagens dele) ──────────────────────────
print("\n🎯 Identificadores ditos pelo vendedor:")
for nome, lista in achados.items():
    do_vendedor = sorted({valor for valor, _, autor in lista if autor.startswith("Kau")})
    if do_vendedor:
        print(f"   {nome:<22} {', '.join(do_vendedor)}")

# ── Salvar para os próximos dias ──────────────────────────────────────────
saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
with open(saidas / "entidades_conversa.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.writer(f, delimiter=";")
    escritor.writerow(["entidade", "valor", "linha", "autor"])
    for nome, lista in achados.items():
        for valor, numero, autor in lista:
            escritor.writerow([nome, valor, numero, autor])
print("\n💾 saidas/entidades_conversa.csv gravado.")
