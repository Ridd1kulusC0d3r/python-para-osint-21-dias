"""
Primeiro contato: um mapa do repositório, dia por dia.

Sem carta (Dia 0 é preparação).

O que você aprende:
  • a localizar a pasta do repositório a partir do próprio script (pathlib);
  • a listar pastas e arquivos sem abrir o explorador de arquivos;
  • a ler o dia.json de cada dia para mostrar o título e o capítulo da história;
  • que cada dia tem o mesmo "esqueleto": original/, br/, dados/, desafio.md.

Como rodar (dentro da pasta dia-00-preparacao):
    python br/02_primeiro_contato.py
"""

import json                 # ler os arquivos dia.json
from pathlib import Path    # trabalhar com caminhos de pastas de um jeito que funciona em qualquer sistema

# ── Parâmetros ────────────────────────────────────────────────────────────
MOSTRAR_ARQUIVOS = True  #@param {type:"boolean"}

# ── Onde estamos? ─────────────────────────────────────────────────────────
# __file__ é o caminho deste script. .parent sobe uma pasta: br/ → dia-00-preparacao/ → raiz.
PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
RAIZ = PASTA_DIA.parent
print(f"📂 Repositório: {RAIZ}\n")

# ── 1. O que tem na raiz ──────────────────────────────────────────────────
# iterdir() lista o conteúdo; sorted() põe em ordem alfabética.
# Pulamos o que começa com "." (pastas ocultas, como .git).
print("🗂️  Na raiz:")
for item in sorted(RAIZ.iterdir()):
    if item.name.startswith(".") or item.name.startswith("dia-"):
        continue
    icone = "📁" if item.is_dir() else "📄"
    print(f"   {icone} {item.name}")

# ── 2. Os dias ────────────────────────────────────────────────────────────
# glob("dia-*") devolve só as pastas cujo nome começa com "dia-".
print("\n🗓️  Os dias:")
dias = sorted(p for p in RAIZ.glob("dia-*") if p.is_dir())
for pasta in dias:
    meta_arquivo = pasta / "dia.json"
    if meta_arquivo.exists():
        # Sempre com encoding="utf-8": os títulos têm acento.
        meta = json.loads(meta_arquivo.read_text(encoding="utf-8"))
        titulo = meta.get("titulo", "?")
        capitulo = meta.get("capitulo", "")
        cartas = " · ".join(str(c["numero"]) for c in meta.get("cartas", [])) or "—"
    else:
        titulo, capitulo, cartas = "(em construção)", "", "—"

    print(f"\n   📁 {pasta.name}")
    print(f"      {titulo}" + (f"  ·  📖 {capitulo}" if capitulo else "") + f"  ·  🃏 {cartas}")

    if MOSTRAR_ARQUIVOS:
        # Para cada subpasta conhecida, contamos quantos arquivos ela tem.
        for sub in ("original", "br", "dados"):
            alvo = pasta / sub
            if alvo.is_dir():
                arquivos = sorted(a.name for a in alvo.iterdir() if a.is_file())
                lista = ", ".join(arquivos[:4]) + (" …" if len(arquivos) > 4 else "")
                lista = lista or "(vazia)"
                print(f"      {sub + '/':<10} {len(arquivos):>2} arquivo(s)  {lista}")
        if (pasta / "desafio.md").exists():
            print("      🏆 desafio.md")

# ── 3. Resumo ─────────────────────────────────────────────────────────────
prontos = sum(1 for p in dias if (p / "dia.json").exists())
print(f"\n✅ {len(dias)} pastas de dias encontradas, {prontos} com dia.json.")
print("👉 Próximo passo: cd ../dia-01-primeiro-script && python br/01_ola_nfa.py")
