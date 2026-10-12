"""
Gabarito do Desafio S do Dia 4 — Ficha de depoimento padronizada (e o diff).

A Delegada Rita quer cada depoimento num formato fixo, "campo: valor", um por arquivo,
e um aviso automático quando o mesmo número de WhatsApp ou a mesma chave PIX aparece em
mais de um depoimento. Este script:
  1. lê caso/dados/depoimentos/*.txt;
  2. grava saidas/fichas/<id>.txt com os campos padronizados (modo "w": a ficha é recriada);
  3. acrescenta (modo "a") uma linha por execução em saidas/historico.log;
  4. imprime os elementos repetidos entre depoimentos (os "vínculos").
Só stdlib, sem internet.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_DEPOIMENTOS = PASTA_DIA.parent / "caso" / "dados" / "depoimentos"
SAIDAS = PASTA_DIA / "saidas"
PASTA_FICHAS = SAIDAS / "fichas"
PASTA_FICHAS.mkdir(parents=True, exist_ok=True)       # parents=True cria saidas/ e fichas/ de uma vez

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

# Para cada campo: o rótulo que procuramos na linha e como cortar o valor.
# Uma função pequena (lambda) por campo deixa a regra de cada um num lugar só.
REGRAS = {
    "data":      ("DEPOIMENTO", lambda l: l.split("registrado em")[-1].strip()),
    "vitima":    ("Vítima:",    lambda l: l.split(":", 1)[1].split(" (")[0].strip()),
    "cidade":    ("Vítima:",    lambda l: l.rsplit("),", 1)[-1].strip()),
    "produto":   ("Comprei um", lambda l: l[len("Comprei um"):].split(" por ")[0].strip()),
    "valor":     ("Comprei um", lambda l: l.split(" por ", 1)[1].split(" no site")[0].strip()),
    "chave_pix": ("A chave era", lambda l: l.split("A chave era")[1].strip().rstrip(".")),
    "whatsapp":  ("WhatsApp",   lambda l: l.split("WhatsApp")[1].split(";")[0].strip()),
}

fichas = {}
for caminho in sorted(PASTA_DEPOIMENTOS.glob("*.txt")):
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = [l.strip() for l in arquivo]
    ficha = {}
    for campo, (rotulo, cortar) in REGRAS.items():
        # next(...) pega a PRIMEIRA linha que contém o rótulo (ou None se nenhuma tiver).
        linha = next((l for l in linhas if rotulo in l), None)
        ficha[campo] = cortar(linha) if linha else "(não informado)"
    fichas[caminho.stem] = ficha

    # Ficha padronizada: "campo: valor", um por linha. Modo "w" porque a ficha é REFEITA
    # do zero a partir da fonte sempre que o script roda (a fonte é o depoimento, não a ficha).
    with open(PASTA_FICHAS / f"{caminho.stem}.txt", "w", encoding="utf-8") as saida:
        saida.write(f"id: {caminho.stem}\n")
        saida.writelines(f"{campo}: {valor}\n" for campo, valor in ficha.items())
        saida.write(f"fonte: caso/dados/depoimentos/{caminho.name}\n")

print(f"🗂️  {len(fichas)} fichas gravadas em saidas/fichas/")

# ── Vínculos: valores que se repetem em mais de um depoimento ─────────────
print("\n🔗 Vínculos entre depoimentos")
for campo in ("whatsapp", "chave_pix"):
    grupos = {}
    for ident, ficha in fichas.items():
        grupos.setdefault(ficha[campo], []).append(ident)
    for valor, ids in grupos.items():
        if len(ids) > 1:
            print(f"   🚩 {campo} {valor} aparece em {len(ids)} depoimentos: {', '.join(ids)}")

# ── Histórico de execuções (modo "a": nunca apaga) ────────────────────────
with open(SAIDAS / "historico.log", "a", encoding="utf-8") as log:
    log.write(f"{datetime.now(FUSO).isoformat(timespec='seconds')}\tfichas={len(fichas)}\n")
execucoes = (SAIDAS / "historico.log").read_text(encoding="utf-8").count("\n")
print(f"\n📜 saidas/historico.log: {execucoes} execução(ões) registradas.")

# ── Conferência: a ficha relida bate com o que extraímos? ─────────────────
primeira = next(iter(fichas))
relida = dict(l.rstrip("\n").split(": ", 1) for l in open(PASTA_FICHAS / f"{primeira}.txt", encoding="utf-8"))
ok = all(relida[c] == v for c, v in fichas[primeira].items())
print(f"✅ Conferência da ficha {primeira}: {'tudo bate' if ok else 'DIVERGÊNCIA!'}")
