"""
Padronizar as cidades digitadas pelas vítimas usando a lista oficial do IBGE.

Carta 28 (rank B) — Jutsu da Planilha Viva (aplicação no caso)

O que você aprende:
  • por que "contagem", "Belo Horizone" e "Pocos de Caldas" atrapalham qualquer contagem;
  • a normalizar texto: tirar acentos (unicodedata) + casefold + espaços;
  • a usar uma tabela de apelidos ("BH" → Belo Horizonte);
  • a corrigir erros de digitação com difflib.get_close_matches (aproximação de texto);
  • a gravar a planilha padronizada com o código IBGE e mostrar o "antes → depois".

Como rodar (dentro da pasta dia-07-csv):
    python br/03_padroniza_cidades.py
    OSINT_OFFLINE=1 python br/03_padroniza_cidades.py
(Se você rodou antes o 02_ibge_municipios.py, ele aproveita saidas/municipios_mg.csv.)
"""

import csv
import difflib              # compara textos parecidos ("Belo Horizone" ≈ "Belo Horizonte")
import json
import os
import unicodedata          # separar letras de acentos
import urllib.request
from collections import Counter
from pathlib import Path

SIMILARIDADE_MINIMA = 0.85  #@param {type:"number"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# Apelidos e siglas que a gente ouve no dia a dia (chave já normalizada).
APELIDOS = {"bh": "Belo Horizonte", "beaga": "Belo Horizonte", "jf": "Juiz de Fora",
            "gv": "Governador Valadares", "udia": "Uberlândia"}


def normalizar(texto):
    """'  Poços  de Caldas ' → 'pocos de caldas'."""
    # NFKD separa "ç" em "c" + "cedilha"; depois jogamos fora o que não é ASCII (os acentos).
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    # casefold é um lower() mais forte; split/join junta espaços repetidos.
    return " ".join(sem_acento.casefold().split())


def carregar_municipios():
    """Devolve {codigo_ibge: nome_oficial}. Ordem de preferência: CSV do script 02, API, amostra."""
    csv_02 = SAIDAS / "municipios_mg.csv"
    if csv_02.exists():
        with open(csv_02, encoding="utf-8-sig", newline="") as arquivo:
            return {int(l["codigo_ibge"]): l["municipio"] for l in csv.DictReader(arquivo, delimiter=";")}
    lista = None
    if not OFFLINE:
        try:
            url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/MG/municipios"
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=30) as resposta:
                lista = json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    if lista is None:
        lista = json.loads((PASTA_DIA / "dados" / "ibge_municipios_mg.json").read_text(encoding="utf-8"))["municipios"]
    return {m["id"]: m["nome"] for m in lista}


# ── 1. Base oficial, indexada pelo nome normalizado ───────────────────────
municipios = carregar_municipios()
por_nome = {normalizar(nome): (codigo, nome) for codigo, nome in municipios.items()}
print(f"📚 Base oficial: {len(municipios)} municípios de MG\n")


def padronizar(cidade_digitada):
    """Devolve (nome_oficial, codigo_ibge, metodo). metodo explica COMO chegamos lá."""
    chave = normalizar(cidade_digitada)
    if chave in por_nome:                                      # 1º: igual depois de normalizar
        codigo, nome = por_nome[chave]
        return nome, codigo, "exato" if nome == cidade_digitada else "normalizado"
    if chave in APELIDOS:                                      # 2º: apelido conhecido
        codigo, nome = por_nome[normalizar(APELIDOS[chave])]
        return nome, codigo, "apelido"
    parecidos = difflib.get_close_matches(chave, por_nome, n=1, cutoff=SIMILARIDADE_MINIMA)
    if parecidos:                                              # 3º: erro de digitação
        codigo, nome = por_nome[parecidos[0]]
        return nome, codigo, "aproximado"
    return "", "", "NÃO RECONHECIDA"                           # 4º: humano precisa olhar


# ── 2. Ler denúncias e padronizar ─────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")
    colunas = leitor.fieldnames
    denuncias = list(leitor)

mudancas = {}                                      # {"Belo Horizone": ("Belo Horizonte", "aproximado")}
for d in denuncias:
    nome, codigo, metodo = padronizar(d["cidade"])
    d["cidade_padronizada"], d["codigo_ibge"], d["metodo"] = nome, codigo, metodo
    if metodo != "exato":
        mudancas[d["cidade"]] = (nome, metodo)

# ── 3. Mostrar o "antes → depois" ─────────────────────────────────────────
print("✏️  Antes → depois:")
for antes, (depois, metodo) in sorted(mudancas.items()):
    print(f"   {antes!r:<24} → {depois or '???':<22} ({metodo})")

antes = Counter(d["cidade"] for d in denuncias)
depois = Counter(d["cidade_padronizada"] for d in denuncias)
print(f"\n📊 Cidades diferentes: {len(antes)} antes · {len(depois)} depois")
print("🏆 Ranking padronizado:")
for cidade, qtd in depois.most_common():
    print(f"   {cidade:<22} {'█' * qtd} {qtd}")

# ── 4. Gravar a planilha nova (com as colunas extras no final) ────────────
SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "denuncias_padronizadas.csv"
with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=colunas + ["cidade_padronizada", "codigo_ibge", "metodo"],
                              delimiter=";")
    escritor.writeheader()
    escritor.writerows(denuncias)
print(f"\n💾 {destino.relative_to(PASTA_DIA)} gravado. A coluna original 'cidade' foi mantida:")
print("   nunca apague o dado bruto; acrescente a versão tratada ao lado.")
