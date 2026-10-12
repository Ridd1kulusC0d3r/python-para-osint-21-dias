"""
Gera as 63 cartas (SVG) do Formato Jutsu e o índice CARTAS.md, a partir dos dia.json.

    python ferramentas/gerar_cartas.py

Só biblioteca padrão: o SVG é montado como texto.
"""

import html
import textwrap

from comum import NIVEL_NOME, RANK_COR, RAIZ, URL_REPO, dias

PASTA = RAIZ / "cartas"
PASTA.mkdir(exist_ok=True)

ARCO = {1: "Arco I · Fundamentos", 2: "Arco II · Brasil", 3: "Arco III · Mestria"}


def svg_carta(carta, meta):
    cor = RANK_COR.get(carta["rank"], "#888")
    nome = textwrap.wrap(carta["nome"], 22)[:2]
    efeito = textwrap.wrap(carta["efeito"], 34)[:6]
    tema = textwrap.shorten(meta["titulo"], 38, placeholder="…")
    e = html.escape

    linhas_nome = "".join(
        f'<text x="150" y="{214 + i * 26}" class="nome">{e(t)}</text>' for i, t in enumerate(nome))
    linhas_efeito = "".join(
        f'<text x="30" y="{292 + i * 19}" class="efeito">{e(t)}</text>' for i, t in enumerate(efeito))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="420" viewBox="0 0 300 420" role="img" aria-label="Carta {carta['numero']}: {e(carta['nome'])}">
  <style>
    .t {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .num {{ font: 700 15px 'Segoe UI', Roboto, Arial, sans-serif; fill: #f4f1e8; }}
    .rank {{ font: 900 44px Georgia, serif; fill: {cor}; text-anchor: middle; }}
    .nome {{ font: 700 20px 'Segoe UI', Roboto, Arial, sans-serif; fill: #f4f1e8; text-anchor: middle; }}
    .tema {{ font: 500 12px 'Segoe UI', Roboto, Arial, sans-serif; fill: #b9b3a3; text-anchor: middle; letter-spacing: .5px; }}
    .efeito {{ font: 400 13.5px 'Segoe UI', Roboto, Arial, sans-serif; fill: #e8e3d6; }}
    .rod {{ font: 600 10.5px 'Segoe UI', Roboto, Arial, sans-serif; fill: #9a9484; letter-spacing: 1px; }}
  </style>
  <rect x="4" y="4" width="292" height="412" rx="18" fill="#17161a" stroke="{cor}" stroke-width="6"/>
  <rect x="16" y="16" width="268" height="388" rx="12" fill="none" stroke="{cor}" stroke-opacity=".35" stroke-width="1.5"/>
  <text x="30" y="44" class="num">Nº {carta['numero']:02d}</text>
  <text x="270" y="44" class="num" text-anchor="end">DIA {meta['dia']:02d}</text>
  <circle cx="150" cy="118" r="54" fill="{cor}" fill-opacity=".12" stroke="{cor}" stroke-width="2.5"/>
  <text x="150" y="134" class="rank">{e(carta['rank'])}</text>
  <text x="150" y="190" class="tema">{e(tema.upper())}</text>
  {linhas_nome}
  <line x1="30" y1="266" x2="270" y2="266" stroke="{cor}" stroke-opacity=".5"/>
  {linhas_efeito}
  <text x="150" y="384" class="rod" text-anchor="middle">ARCO {"I" * carta['nivel']} · {e(NIVEL_NOME[carta['nivel']].upper())}</text>
  <text x="150" y="400" class="rod" text-anchor="middle">PYJUTSU · PYTHON PARA OSINT</text>
</svg>
'''


def main():
    todas = []
    for meta in dias():
        for carta in meta.get("cartas", []):
            arquivo = PASTA / f"carta-{carta['numero']:02d}.svg"
            arquivo.write_text(svg_carta(carta, meta), encoding="utf-8")
            todas.append((carta, meta))
    todas.sort(key=lambda par: par[0]["numero"])

    linhas = ["# 🃏 As 63 cartas do PyJutsu", "",
              "Cada dia tem três cartas, uma por nível. Conquiste a carta quando terminar o exercício.", "",
              "| Nível | Cartas | Rank |", "|---|---|---|",
              "| 1 · Original (cipher387) | 1–21 | D (dias 1–10) · C (11–21) |",
              "| 2 · Camada Brasil | 22–42 | B (dias 1–10) · A (11–21) |",
              "| 3 · Desafio | 43–63 | S |", ""]
    for nivel in (1, 2, 3):
        linhas += [f"## {ARCO[nivel]}", "", "| Carta | Nº | Rank | Nome | Dia | Efeito |", "|---|---|---|---|---|---|"]
        for carta, meta in todas:
            if carta["nivel"] != nivel:
                continue
            img = f'<img src="cartas/carta-{carta["numero"]:02d}.svg" width="90" alt="Carta {carta["numero"]}">'
            alvo = f'{meta["_pasta"].name}/{carta.get("arquivo", "README.md")}'
            linhas.append(f'| {img} | {carta["numero"]} | {carta["rank"]} | [{carta["nome"]}]({alvo}) '
                          f'| [{meta["dia"]:02d}]({meta["_pasta"].name}/) | {carta["efeito"]} |')
        linhas.append("")
    (RAIZ / "CARTAS.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"🃏 {len(todas)} cartas geradas em {PASTA.relative_to(RAIZ)}/ e índice em CARTAS.md")


if __name__ == "__main__":
    main()
