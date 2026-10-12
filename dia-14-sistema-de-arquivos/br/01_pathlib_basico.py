"""
pathlib: o jeito moderno (e que funciona no Windows) de andar por pastas.

Carta 35 (rank A) — Jutsu da Sala de Evidências

O que você aprende:
  • a montar caminhos com Path e o operador / (sem se preocupar com \\ ou /);
  • glob (só na pasta) x rglob (na pasta e em TODAS as subpastas);
  • a ler tamanho e data de modificação com stat();
  • a "traduzir" os scripts originais (os.chdir + glob.glob) para pathlib.

Este script é 100% offline. Por padrão, passeia por caso/dados.

Como rodar (dentro da pasta dia-14-sistema-de-arquivos):
    python br/01_pathlib_basico.py
"""

import glob
import os
from datetime import datetime
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"   # "/" junta pedaços de caminho

# ── 1. Anatomia de um caminho ─────────────────────────────────────────────
exemplo = PASTA_CASO / "depoimentos" / "DEN-001.txt"
print("🧩 Anatomia de um caminho")
print(f"   caminho completo : {exemplo}")
print(f"   .name            : {exemplo.name}")        # nome com extensão
print(f"   .stem            : {exemplo.stem}")        # nome sem extensão
print(f"   .suffix          : {exemplo.suffix}")      # extensão
print(f"   .parent.name     : {exemplo.parent.name}") # pasta onde está
print(f"   .exists()        : {exemplo.exists()}")

# ── 2. glob x rglob ───────────────────────────────────────────────────────
print("\n📂 glob('*.txt') em caso/dados (só o primeiro nível):")
for arquivo in sorted(PASTA_CASO.glob("*.txt")):
    print(f"   {arquivo.name}")

print("\n📂 rglob('*.txt') em caso/dados (inclui subpastas):")
for arquivo in sorted(PASTA_CASO.rglob("*.txt")):
    # relative_to mostra o caminho a partir de caso/dados (mais fácil de ler)
    print(f"   {arquivo.relative_to(PASTA_CASO)}")


# ── 3. stat(): tamanho e data de modificação ──────────────────────────────
def tamanho_legivel(n):
    """1536 → '1.5 KB'."""
    for unidade in ("B", "KB", "MB", "GB"):
        if n < 1024 or unidade == "GB":
            return f"{n:.0f} {unidade}" if unidade == "B" else f"{n:.1f} {unidade}"
        n /= 1024


print(f"\n📋 Inventário de caso/dados ({'arquivo':<34} {'tamanho':>9}  modificado em)")
total = 0
for arquivo in sorted(p for p in PASTA_CASO.rglob("*") if p.is_file()):
    info = arquivo.stat()
    total += info.st_size
    modificado = datetime.fromtimestamp(info.st_mtime)   # st_mtime vem em segundos desde 1970
    print(f"   {str(arquivo.relative_to(PASTA_CASO)):<42} {tamanho_legivel(info.st_size):>9}  {modificado:%d/%m/%Y %H:%M}")
print(f"   {'TOTAL':<42} {tamanho_legivel(total):>9}")

# ── 4. Original (os + glob) x pathlib, lado a lado ────────────────────────
# O original faz os.chdir("test_dir"): muda a pasta de trabalho do programa INTEIRO.
# Isso é perigoso em scripts maiores (todo caminho relativo passa a apontar para outro lugar).
# Com pathlib, não mudamos de pasta: só dizemos onde procurar.
test_dir = PASTA_DIA / "original" / "test_dir"
print("\n🔁 Original x pathlib (na pasta original/test_dir):")
jeito_original = sorted(os.path.basename(p) for p in glob.glob(os.path.join(test_dir, "*.txt")))
jeito_pathlib = sorted(p.name for p in test_dir.glob("*.txt"))
print(f"   glob.glob   → {jeito_original}")
print(f"   Path.glob   → {jeito_pathlib}")
print(f"   Iguais? {'✅ sim' if jeito_original == jeito_pathlib else '❌ não'}")

print("\n📖 Ler sem abrir/fechar na mão:")
for arquivo in sorted(test_dir.glob("*")):
    # read_text faz open + read + close de uma vez; encoding evita surpresa no Windows
    print(f"   {arquivo.name}: {arquivo.read_text(encoding='utf-8').strip()!r}")
