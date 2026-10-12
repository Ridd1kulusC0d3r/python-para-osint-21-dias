"""
Gera o site do curso (docs/index.html) para o GitHub Pages, a partir dos dia.json.

    python ferramentas/construir_site.py

Depois, no GitHub: Settings → Pages → "Deploy from a branch" → main /docs.
Só biblioteca padrão.
"""

import html
import shutil

from comum import RAIZ, RANK_COR, URL_ORIGINAL, URL_REPO, dias

DOCS = RAIZ / "docs"
(DOCS / "cartas").mkdir(parents=True, exist_ok=True)
e = html.escape


def colab(slug):
    return f"https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/{slug}/notebook.ipynb"


def main():
    lista = dias()
    for svg in (RAIZ / "cartas").glob("*.svg"):
        shutil.copy(svg, DOCS / "cartas" / svg.name)

    cartoes = []
    for m in lista:
        slug = m["_pasta"].name
        ranks = "".join(f'<span class="rk" style="--c:{RANK_COR[c["rank"]]}" title="Carta {c["numero"]}">{c["rank"]}</span>'
                        for c in m.get("cartas", []))
        cartoes.append(f'''
      <article class="dia" data-dia="{m["dia"]}">
        <header><span class="n">{m["dia"]:02d}</span><label class="feito"><input type="checkbox" data-dia="{m["dia"]}"> feito</label></header>
        <h3>{e(m["titulo"])}</h3>
        <p class="cap">📖 {e(m.get("capitulo", ""))}</p>
        <p class="orig">📘 {e(m.get("titulo_original", ""))}</p>
        <footer><span class="ranks">{ranks}</span>
          <a href="{URL_REPO}/tree/main/{slug}">Guia</a>
          <a class="cta" href="{colab(slug)}">Abrir no Colab ↗</a></footer>
      </article>''')

    galeria = "".join(
        f'<img loading="lazy" src="cartas/carta-{c["numero"]:02d}.svg" alt="Carta {c["numero"]}: {e(c["nome"])}" width="150" height="210">'
        for m in lista for c in sorted(m.get("cartas", []), key=lambda c: c["numero"]))
    total = sum(1 for m in lista if m["dia"] > 0)

    pagina = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PyJutsu — Python para OSINT</title>
<meta name="description" content="Python para OSINT em 21 dias, edição BR: o curso do cipher387 com camada Brasil, narrativa, notebooks Colab e cartas.">
<style>
:root {{ --bg:#f6f4ee; --card:#ffffff; --ink:#1d1c20; --mute:#5f5b52; --line:#e3ded2; --acc:#1f6f5c; --acc2:#e0a400; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#121115; --card:#1b1a1f; --ink:#f1ede3; --mute:#a7a091; --line:#2c2a31; --acc:#5cc8a8; }} }}
:root[data-theme="dark"] {{ --bg:#121115; --card:#1b1a1f; --ink:#f1ede3; --mute:#a7a091; --line:#2c2a31; --acc:#5cc8a8; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
a {{ color:var(--acc); }}
.wrap {{ max-width:1120px; margin:0 auto; padding:0 16px; }}
.hero {{ padding:56px 0 28px; border-bottom:1px solid var(--line); }}
.hero small {{ letter-spacing:.14em; text-transform:uppercase; color:var(--mute); font-weight:600; }}
.hero h1 {{ font:800 clamp(2.1rem,6vw,3.6rem)/1.05 Georgia,serif; margin:.3em 0 .25em; }}
.hero p {{ max-width:62ch; color:var(--mute); font-size:1.08rem; }}
.botoes {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; }}
.btn {{ padding:10px 16px; border-radius:10px; border:1px solid var(--line); background:var(--card); color:var(--ink); text-decoration:none; font-weight:600; }}
.btn.p {{ background:var(--acc); color:#fff; border-color:var(--acc); }}
section {{ padding:36px 0; }}
h2 {{ font:700 1.6rem Georgia,serif; margin:0 0 6px; }}
.sub {{ color:var(--mute); margin:0 0 18px; }}
.progresso {{ display:flex; align-items:center; gap:12px; margin:8px 0 22px; }}
.barra {{ flex:1; height:10px; background:var(--line); border-radius:99px; overflow:hidden; }}
.barra i {{ display:block; height:100%; width:0; background:linear-gradient(90deg,var(--acc),var(--acc2)); transition:width .3s; }}
.grade {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:14px; }}
.dia {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; display:flex; flex-direction:column; gap:4px; }}
.dia.ok {{ outline:2px solid var(--acc); }}
.dia header {{ display:flex; justify-content:space-between; align-items:center; }}
.dia .n {{ font:800 1.5rem Georgia,serif; color:var(--acc); }}
.dia h3 {{ margin:2px 0; font-size:1.05rem; }}
.cap, .orig {{ margin:0; font-size:.88rem; color:var(--mute); }}
.feito {{ font-size:.82rem; color:var(--mute); cursor:pointer; }}
.dia footer {{ margin-top:auto; padding-top:10px; display:flex; align-items:center; gap:10px; flex-wrap:wrap; font-size:.9rem; }}
.ranks {{ display:flex; gap:4px; margin-right:auto; }}
.rk {{ width:24px; height:24px; border-radius:6px; display:grid; place-items:center; font:800 .78rem Georgia,serif; color:var(--c); border:1.5px solid var(--c); }}
.cta {{ font-weight:700; }}
.niveis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:14px; }}
.nivel {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; }}
.nivel b {{ display:block; font-size:1.05rem; }}
.galeria {{ display:flex; gap:10px; overflow-x:auto; padding-bottom:10px; scroll-snap-type:x mandatory; }}
.galeria img {{ flex:none; scroll-snap-align:start; border-radius:10px; }}
.tabs {{ display:flex; gap:6px; flex-wrap:wrap; }}
.tabs button {{ padding:8px 14px; border-radius:99px; border:1px solid var(--line); background:var(--card); color:var(--ink); cursor:pointer; font:inherit; }}
.tabs button[aria-selected="true"] {{ background:var(--ink); color:var(--bg); }}
.painel {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 18px; margin-top:10px; }}
.painel[hidden] {{ display:none; }}
pre {{ background:var(--bg); border:1px solid var(--line); border-radius:8px; padding:10px 12px; overflow-x:auto; font-size:.88rem; }}
footer.site {{ border-top:1px solid var(--line); padding:26px 0 40px; color:var(--mute); font-size:.92rem; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <small>Edição BR · Formato Jutsu · 63 cartas</small>
    <h1>PyJutsu — Python para OSINT em 21 dias</h1>
    <p>O curso <a href="{URL_ORIGINAL}">“Python for OSINT. 21-day course for beginners”</a> do <strong>cipher387</strong>,
       mantido intacto, com uma camada Brasil somada a cada dia, uma investigação contínua (a <em>Operação Vitrine Fantasma</em>),
       notebooks prontos no Colab e código comentado linha a linha.</p>
    <div class="botoes">
      <a class="btn p" href="{colab("dia-00-preparacao")}">Começar no Colab ↗</a>
      <a class="btn" href="{URL_REPO}">Repositório</a>
      <a class="btn" href="{URL_REPO}/blob/main/COMECE-AQUI.md">Comece aqui</a>
      <a class="btn" href="{URL_ORIGINAL}">Curso original</a>
    </div>
  </div>

  <section>
    <h2>Como cada dia funciona</h2>
    <p class="sub">Somar, nunca substituir: o exercício original continua lá e o Brasil entra ao lado.</p>
    <div class="niveis">
      <div class="nivel"><b>🥋 Nível 1 · Original</b>O código do cipher387, intacto, com comentários em pt-BR. Rank D/C.</div>
      <div class="nivel"><b>🇧🇷 Nível 2 · Camada Brasil</b>Fontes brasileiras (registro.br, BrasilAPI, IBGE, Querido Diário) só com a biblioteca padrão. Rank B/A.</div>
      <div class="nivel"><b>🏆 Nível 3 · Desafio</b>Um problema do caso para resolver sozinho, com gabarito escondido. Rank S.</div>
    </div>
  </section>

  <section>
    <h2>Os dias</h2>
    <div class="progresso"><span id="txt">0 de {total} dias</span><div class="barra"><i id="barra"></i></div></div>
    <div class="grade">{"".join(cartoes)}
    </div>
  </section>

  <section>
    <h2>As cartas</h2>
    <p class="sub">Cada dia vale três cartas. Índice completo em <a href="{URL_REPO}/blob/main/CARTAS.md">CARTAS.md</a>.</p>
    <div class="galeria">{galeria}</div>
  </section>

  <section>
    <h2>Onde estudar</h2>
    <div class="tabs" role="tablist">
      <button role="tab" aria-selected="true" data-alvo="t-colab">Google Colab</button>
      <button role="tab" aria-selected="false" data-alvo="t-win">Windows</button>
      <button role="tab" aria-selected="false" data-alvo="t-mac">macOS</button>
      <button role="tab" aria-selected="false" data-alvo="t-linux">Linux</button>
      <button role="tab" aria-selected="false" data-alvo="t-cs">Codespaces</button>
    </div>
    <div class="painel" id="t-colab"><p>Nada para instalar. Clique em <strong>Abrir no Colab</strong> em qualquer dia e rode a primeira célula (⚙️ Preparar o ambiente).</p></div>
    <div class="painel" id="t-win" hidden><p>Instale o Python 3 em <a href="https://www.python.org/downloads/">python.org</a> marcando <em>Add python.exe to PATH</em> e o <a href="https://git-scm.com/download/win">Git</a>. No PowerShell:</p><pre>git clone {URL_REPO}.git
cd python-para-osint-21-dias\\dia-01-primeiro-script
py br\\01_ola_nfa.py</pre></div>
    <div class="painel" id="t-mac" hidden><p>No Terminal (o macOS pede para instalar as ferramentas de linha de comando na primeira vez):</p><pre>git clone {URL_REPO}.git
cd python-para-osint-21-dias/dia-01-primeiro-script
python3 br/01_ola_nfa.py</pre></div>
    <div class="painel" id="t-linux" hidden><pre>sudo apt install -y python3 git     # Debian/Ubuntu
git clone {URL_REPO}.git
cd python-para-osint-21-dias/dia-01-primeiro-script
python3 br/01_ola_nfa.py</pre></div>
    <div class="painel" id="t-cs" hidden><p>No GitHub, abra o repositório e clique em <strong>Code → Codespaces → Create codespace on main</strong>. É o caminho que o próprio autor do curso recomenda desde que o Gitpod ficou pago.</p></div>
  </section>

  <footer class="site">
    Código original © 2023 Cyb_detective (<a href="{URL_ORIGINAL}">cipher387</a>), licença MIT.
    Adaptação pt-BR, camada Brasil, narrativa, notebooks e cartas © 2026 Deivison Lourenço (<a href="https://github.com/Ridd1kulusC0d3r">Ridd1kulusC0d3r</a>), MIT.
    Todos os dados do caso são fictícios. · Gostou do curso original? <a href="https://boosty.to/cyb_detective">Apoie o autor</a>.
  </footer>
</div>
<script>
(function () {{
  var CHAVE = "pyjutsu-progresso";
  function ler() {{ try {{ return JSON.parse(localStorage.getItem(CHAVE) || "[]"); }} catch (e) {{ return []; }} }}
  function gravar(v) {{ try {{ localStorage.setItem(CHAVE, JSON.stringify(v)); }} catch (e) {{}} }}
  var feitos = ler();
  var caixas = document.querySelectorAll('input[type=checkbox][data-dia]');
  function atualizar() {{
    var n = 0;
    caixas.forEach(function (c) {{
      var ok = feitos.indexOf(c.dataset.dia) > -1;
      c.checked = ok; c.closest(".dia").classList.toggle("ok", ok);
      if (ok && c.dataset.dia !== "0") n++;
    }});
    document.getElementById("txt").textContent = n + " de {total} dias";
    document.getElementById("barra").style.width = (100 * n / {total}) + "%";
  }}
  caixas.forEach(function (c) {{
    c.addEventListener("change", function () {{
      feitos = feitos.filter(function (d) {{ return d !== c.dataset.dia; }});
      if (c.checked) feitos.push(c.dataset.dia);
      gravar(feitos); atualizar();
    }});
  }});
  atualizar();
  document.querySelectorAll('[role=tab]').forEach(function (b) {{
    b.addEventListener("click", function () {{
      document.querySelectorAll('[role=tab]').forEach(function (x) {{
        x.setAttribute("aria-selected", x === b); document.getElementById(x.dataset.alvo).hidden = x !== b;
      }});
    }});
  }});
}})();
</script>
</body>
</html>
'''
    (DOCS / "index.html").write_text(pagina, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"🌐 docs/index.html gerado com {len(lista)} dias")
    atualizar_readme(lista)
    atualizar_requirements(lista)


def atualizar_readme(lista):
    """Reescreve a tabela dos dias no README da raiz (entre os marcadores)."""
    badge = "https://colab.research.google.com/assets/colab-badge.svg"
    linhas = ["| Dia | Tema | Capítulo do caso | Cartas | Notebook |", "|---|---|---|---|---|"]
    for m in lista:
        slug = m["_pasta"].name
        cartas = " · ".join(f'{c["numero"]}<sub>{c["rank"]}</sub>' for c in m.get("cartas", [])) or "—"
        linhas.append(f'| **{m["dia"]:02d}** | [{m["titulo"]}]({slug}/) | {m.get("capitulo", "")} | {cartas} '
                      f'| [![Colab]({badge})]({colab(slug)}) |')
    readme = RAIZ / "README.md"
    texto = readme.read_text(encoding="utf-8")
    inicio, fim = "<!-- tabela-dias:inicio -->", "<!-- tabela-dias:fim -->"
    antes, resto = texto.split(inicio, 1)
    _, depois = resto.split(fim, 1)
    readme.write_text(antes + inicio + "\n" + "\n".join(linhas) + "\n" + fim + depois, encoding="utf-8")
    print("📝 tabela de dias do README atualizada")


def atualizar_requirements(lista):
    """Junta as bibliotecas dos exercícios originais num requirements-original.txt."""
    libs = sorted({lib for m in lista for lib in m.get("pip_original", [])}, key=str.lower)
    texto = ("# Bibliotecas usadas SÓ pelos exercícios originais (nível 1).\n"
             "# A camada Brasil (nível 2) não precisa de nada além do Python.\n"
             "#   pip install -r requirements-original.txt\n" + "\n".join(libs) + "\n")
    (RAIZ / "requirements-original.txt").write_text(texto, encoding="utf-8")
    print(f"📦 requirements-original.txt com {len(libs)} bibliotecas")


if __name__ == "__main__":
    main()
