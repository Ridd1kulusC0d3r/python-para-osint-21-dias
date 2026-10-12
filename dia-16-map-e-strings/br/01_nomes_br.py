"""
Nomes brasileiros com maiúsculas certas: o title() erra, a gente conserta.

Carta 37 (rank A) — Jutsu dos Muitos Nomes

O que você aprende:
  • por que "maria da silva".title() vira "Maria Da Silva" (e por que isso atrapalha);
  • a escrever uma função que deixa da/de/do/das/dos/e em minúsculas;
  • a aplicar essa função em uma lista inteira com map().

Como rodar (dentro da pasta dia-16-map-e-strings):
    python br/01_nomes_br.py
"""

import csv                  # ler a planilha de denúncias
from pathlib import Path    # montar caminhos de arquivo

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
QUANTOS_MOSTRAR = 8  #@param {type:"integer"}

# ── Onde estão os dados do caso ───────────────────────────────────────────
PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# Palavras que, no meio de um nome brasileiro, ficam em minúsculas.
PARTICULAS = {"da", "de", "do", "das", "dos", "e", "d'"}


def nome_br(texto):
    """Põe um nome no formato brasileiro.

    "MARIA DA SILVA" → "Maria da Silva" · "joão dos santos e souza" → "João dos Santos e Souza"
    """
    # 1. split() sem argumento quebra em QUALQUER quantidade de espaços e
    #    ignora espaços nas pontas: "  ana   lima " → ["ana", "lima"]
    palavras = texto.lower().split()
    resultado = []
    # 2. enumerate dá a posição (0, 1, 2...) junto com a palavra
    for posicao, palavra in enumerate(palavras):
        if posicao > 0 and palavra in PARTICULAS:
            resultado.append(palavra)               # partícula no meio: fica minúscula
        else:
            resultado.append(palavra.capitalize())  # "brandão" → "Brandão"
    # 3. join() faz o caminho inverso do split(): cola a lista com um espaço
    return " ".join(resultado)


# ── 1. O problema do title() ──────────────────────────────────────────────
exemplos = ["MARIA DA SILVA", "joão dos santos e souza", "  kauã   teixeira brandão ", "ANA DE JESUS"]
print("🔤 title() do Python  ×  nome_br() desta carta\n")
for exemplo in exemplos:
    print(f"   {exemplo.strip().title():<28} → {nome_br(exemplo)}")

# ── 2. Lendo os nomes das vítimas ─────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    nomes = [linha["nome_vitima"] for linha in csv.DictReader(arquivo, delimiter=";")]

# Simulamos o que acontece de verdade: cada sistema grava de um jeito.
# map(str.upper, nomes) aplica o método upper() em cada nome (tudo MAIÚSCULO).
gritados = list(map(str.upper, nomes))

# ── 3. A mágica: map() aplica nome_br em cada item ────────────────────────
# Repare: passamos nome_br SEM parênteses. Quem chama a função é o map().
consertados = list(map(nome_br, gritados))

print(f"\n📋 {len(nomes)} nomes de vítimas: do sistema que grita → padrão brasileiro\n")
for antes, depois in zip(gritados[:QUANTOS_MOSTRAR], consertados[:QUANTOS_MOSTRAR]):
    print(f"   {antes:<30} → {depois}")

# ── 4. Conferência: voltamos ao original? ─────────────────────────────────
# zip() junta duas listas lado a lado; contamos quantos pares são iguais.
iguais = sum(1 for original, refeito in zip(nomes, consertados) if original == refeito)
print(f"\n✅ {iguais} de {len(nomes)} nomes voltaram exatamente como estavam na planilha.")

# ── 5. Por que isso importa em OSINT ──────────────────────────────────────
# Em buscas, "Kauã Teixeira Brandão" e "KAUÃ TEIXEIRA BRANDÃO" são o mesmo texto
# para um humano, mas NÃO para o computador. Padronizar antes de comparar evita
# perder um vínculo (falso negativo) ou duplicar uma pessoa no relatório.
print("\n💡 Padronize ANTES de comparar ou deduplicar. Amanhã esses nomes vão para o relatório.")
