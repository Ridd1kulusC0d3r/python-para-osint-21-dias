"""
Cadeia de custódia na prática: manifesto SHA-256 das evidências e verificação.

Carta 35 (rank A) — Jutsu da Sala de Evidências (parte 3)

O que você aprende:
  • o que é um hash (uma "impressão digital" de um arquivo) e por que SHA-256;
  • a calcular o hash lendo o arquivo em BLOCOS (funciona até com arquivos de vários GB);
  • a gerar um manifesto (CSV) com caminho, tamanho, data de modificação e hash;
  • a VERIFICAR depois: o script avisa se algum arquivo foi alterado, sumiu ou apareceu.

Dois modos (parâmetro MODO):
  "gerar"     → cria saidas/manifesto_custodia.csv
  "verificar" → compara a pasta com um manifesto já existente
  "demo"      → gera, simula uma adulteração numa CÓPIA e mostra a verificação pegando

Este script é 100% offline e NUNCA altera caso/dados (a demo mexe só numa cópia em saidas/).

Como rodar (dentro da pasta dia-14-sistema-de-arquivos):
    python br/03_hash_custodia.py
"""

import csv
import hashlib
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

MODO = "demo"  #@param ["gerar", "verificar", "demo"]
PASTA_ALVO = "../caso/dados"  #@param {type:"string"}
TAMANHO_BLOCO = 65536  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
SAIDAS = PASTA_DIA / "saidas"
MANIFESTO = SAIDAS / "manifesto_custodia.csv"

# Fuso de Brasília (com plano B para Windows sem tzdata).
try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))


def sha256_do_arquivo(caminho):
    """Lê o arquivo aos pedaços e vai alimentando o hash. Memória usada: só 1 bloco."""
    h = hashlib.sha256()
    with open(caminho, "rb") as arquivo:          # "rb" = leitura BINÁRIA: o hash é dos bytes
        while True:
            bloco = arquivo.read(TAMANHO_BLOCO)
            if not bloco:                          # b"" = chegou ao fim
                break
            h.update(bloco)
    return h.hexdigest()                           # 64 caracteres hexadecimais


def gerar_manifesto(pasta, destino):
    """Percorre a pasta e grava uma linha por arquivo no CSV de manifesto."""
    linhas = []
    for arquivo in sorted(p for p in pasta.rglob("*") if p.is_file()):
        info = arquivo.stat()
        linhas.append({
            # as_posix() grava com "/" mesmo no Windows: o manifesto vale em qualquer sistema
            "arquivo": arquivo.relative_to(pasta).as_posix(),
            "bytes": info.st_size,
            "modificado_em": datetime.fromtimestamp(info.st_mtime, FUSO_BR).isoformat(timespec="seconds"),
            "sha256": sha256_do_arquivo(arquivo),
        })
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", newline="", encoding="utf-8") as f:
        f.write(f"# Manifesto de {pasta.name}/ gerado em {datetime.now(FUSO_BR):%d/%m/%Y %H:%M:%S} (Brasília)\n")
        escritor = csv.DictWriter(f, fieldnames=["arquivo", "bytes", "modificado_em", "sha256"], delimiter=";")
        escritor.writeheader()
        escritor.writerows(linhas)
    return linhas


def ler_manifesto(caminho):
    with open(caminho, encoding="utf-8") as f:
        linhas_uteis = [l for l in f if not l.startswith("#")]   # pula o comentário do topo
    return {l["arquivo"]: l for l in csv.DictReader(linhas_uteis, delimiter=";")}


def verificar(pasta, manifesto):
    """Compara o estado atual da pasta com o manifesto. Devolve a quantidade de problemas."""
    esperado = ler_manifesto(manifesto)
    atual = {p.relative_to(pasta).as_posix(): p for p in pasta.rglob("*") if p.is_file()}
    problemas = 0
    for nome in sorted(set(esperado) | set(atual)):
        if nome not in atual:
            print(f"   ❌ SUMIU      {nome}")
            problemas += 1
        elif nome not in esperado:
            print(f"   ➕ NOVO       {nome}  (não estava no manifesto)")
            problemas += 1
        elif sha256_do_arquivo(atual[nome]) != esperado[nome]["sha256"]:
            print(f"   🚩 ALTERADO   {nome}  (hash diferente)")
            problemas += 1
        else:
            print(f"   ✅ íntegro    {nome}")
    return problemas


pasta = (PASTA_DIA / PASTA_ALVO).resolve()

# ── Demonstração rápida: um caractere muda o hash inteiro ─────────────────
print("🔬 Efeito avalanche:")
for frase in ["Chave PIX: f38b2ffc", "Chave PIX: f38b2ffd"]:
    print(f"   {frase!r:<24} → {hashlib.sha256(frase.encode()).hexdigest()[:32]}…")

if MODO == "gerar":
    linhas = gerar_manifesto(pasta, MANIFESTO)
    print(f"\n🧾 {len(linhas)} arquivos no manifesto → {MANIFESTO.relative_to(PASTA_DIA)}")

elif MODO == "verificar":
    if not MANIFESTO.exists():
        raise SystemExit("Não há manifesto ainda. Rode antes com MODO = 'gerar'.")
    print(f"\n🔍 Verificando {pasta.name}/ contra o manifesto:")
    n = verificar(pasta, MANIFESTO)
    print(f"\n{'✅ Tudo íntegro.' if n == 0 else f'🚩 {n} problema(s): registre e investigue antes de usar a evidência.'}")

else:   # demo
    # 1) Copiamos as evidências para saidas/ (o original fica intocado)
    copia = SAIDAS / "copia_de_trabalho"
    if copia.exists():
        shutil.rmtree(copia)
    shutil.copytree(pasta, copia)       # copytree preserva as datas de modificação
    linhas = gerar_manifesto(copia, MANIFESTO)
    print(f"\n🧾 Manifesto gerado com {len(linhas)} arquivos. Amostra:")
    for l in linhas[:4]:
        print(f"   {l['sha256'][:16]}…  {l['bytes']:>6} B  {l['arquivo']}")

    # 2) "Alguém" mexe na cópia: troca a chave PIX de um depoimento e cria um arquivo novo
    alvo = copia / "depoimentos" / "DEN-001.txt"
    texto = alvo.read_text(encoding="utf-8")
    alvo.write_text(texto.replace("f38b2ffc", "f38b2ffd"), encoding="utf-8")
    (copia / "anotacao_solta.txt").write_text("rascunho\n", encoding="utf-8")
    print("\n😈 Simulação: 1 letra trocada em DEN-001.txt e 1 arquivo novo criado.")

    # 3) A verificação pega as duas coisas
    print("\n🔍 Verificação:")
    n = verificar(copia, MANIFESTO)
    print(f"\n🚩 {n} problema(s) detectado(s). Sem o manifesto, ninguém perceberia a troca de 1 letra.")
