"""
Gerador de dorks: montar buscas avançadas e abrir com um clique (sem raspar buscador).

Carta 30 (rank B) — Jutsu do Diário Oficial (parte 3)

O que você aprende:
  • os operadores de busca mais úteis: site:, filetype:, intext:, intitle:, aspas, -excluir, OR;
  • a montar a URL de busca do Google, DuckDuckGo e Bing com urllib.parse.quote_plus;
  • a gerar uma página HTML com os links (html.escape para não quebrar o HTML);
  • por que NÃO raspamos o buscador: termos de uso, bloqueios e captchas. Você clica, você lê.

Como rodar (dentro da pasta dia-09-resultados-de-busca):
    python br/03_dorks_br.py
    (depois abra saidas/dorks.html no navegador)
"""

import html                 # escapar textos antes de colocar no HTML
import urllib.parse         # transformar a busca em texto seguro para URL
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Parâmetros: termos do caso (FICTÍCIOS) e um alvo institucional ────────
DOMINIO_LOJA = "megaoferta-brasil.example"  #@param {type:"string"}
APELIDO = "kau.ofertas"  #@param {type:"string"}
CNPJ_RODAPE = "48.217.093/0001-30"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
SAIDAS = PASTA_DIA / "saidas"

try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))

# ── 1. O "cardápio" de buscas (grupo, objetivo, consulta) ─────────────────
DORKS = [
    ("Treino com fonte oficial", "PDFs do governo que citam CNPJ",
     'site:gov.br filetype:pdf intext:"CNPJ"'),
    ("Treino com fonte oficial", "Alertas oficiais sobre golpes com PIX",
     'site:gov.br intitle:"golpe" "PIX"'),
    ("Treino com fonte oficial", "Planilhas públicas de contratos em MG",
     'site:mg.gov.br (filetype:xlsx OR filetype:csv) "contrato"'),
    ("Caso: a loja", "Páginas que citam o domínio (fora do próprio site)",
     f'"{DOMINIO_LOJA}" -site:{DOMINIO_LOJA}'),
    ("Caso: a loja", "Reclamações de consumidores",
     f'"megaoferta brasil" (golpe OR reclamação OR "não entregou")'),
    ("Caso: a loja", "O CNPJ inventado em outros sites (reaproveitado?)",
     f'"{CNPJ_RODAPE}"'),
    ("Caso: o vendedor", "O apelido em redes e fóruns",
     f'"{APELIDO}"'),
    ("Caso: o vendedor", "Apelido + WhatsApp/Telegram",
     f'"{APELIDO}" (whatsapp OR telegram OR "t.me")'),
]

# ── 2. Cada buscador tem seu endereço de busca ────────────────────────────
BUSCADORES = {
    "Google": "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
    "Bing": "https://www.bing.com/search?q=",
}


def link(base, consulta):
    """quote_plus troca espaço por '+' e codifica aspas, dois-pontos, acentos…"""
    return base + urllib.parse.quote_plus(consulta)


# Mostrar no terminal um exemplo de "antes e depois" da codificação
exemplo = DORKS[0][2]
print(f"🔤 Consulta:  {exemplo}")
print(f"🔗 Na URL:    {link(BUSCADORES['Google'], exemplo)}\n")

# ── 3. Montar o HTML ──────────────────────────────────────────────────────
agora = datetime.now(FUSO_BR).strftime("%d/%m/%Y %H:%M")
partes = [
    "<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>",
    "<title>Dorks do caso Vitrine Fantasma</title>",
    "<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}"
    "code{background:#f1f1f1;padding:2px 6px;border-radius:4px}td,th{padding:6px;border-bottom:1px solid #ddd;"
    "text-align:left;vertical-align:top}table{border-collapse:collapse;width:100%}</style></head><body>",
    "<h1>🔎 Dorks — Operação Vitrine Fantasma</h1>",
    f"<p>Gerado em {agora} (horário de Brasília). Clique, leia e <b>registre</b> o que achar "
    "(URL + data/hora + captura de tela).</p>",
]
grupo_atual = None
for grupo, objetivo, consulta in DORKS:
    if grupo != grupo_atual:                          # novo grupo → nova tabela
        if grupo_atual is not None:
            partes.append("</table>")
        partes.append(f"<h2>{html.escape(grupo)}</h2><table><tr><th>Objetivo</th><th>Consulta</th><th>Abrir</th></tr>")
        grupo_atual = grupo
    botoes = " · ".join(
        f"<a href='{html.escape(link(base, consulta), quote=True)}' target='_blank' rel='noopener noreferrer'>{nome}</a>"
        for nome, base in BUSCADORES.items())
    partes.append(f"<tr><td>{html.escape(objetivo)}</td><td><code>{html.escape(consulta)}</code></td><td>{botoes}</td></tr>")
partes.append("</table><p><small>Os dados do caso são fictícios: as buscas do caso devem voltar vazias. "
              "Use as de treino para ver os operadores funcionando.</small></p></body></html>")

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "dorks.html"
destino.write_text("\n".join(partes), encoding="utf-8")

# ── 4. Resumo no terminal ─────────────────────────────────────────────────
for grupo, objetivo, consulta in DORKS:
    print(f"   [{grupo}] {objetivo}\n      {consulta}")
print(f"\n💾 {len(DORKS)} dorks × {len(BUSCADORES)} buscadores em {destino.relative_to(PASTA_DIA)}")
print("   Abra no navegador. Nada foi buscado automaticamente: quem clica é você.")
