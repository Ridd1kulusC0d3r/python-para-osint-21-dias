"""
Gabarito do Desafio S do Dia 6 — Fichário de CNPJs do caso.

Varre os arquivos de texto do caso atrás de CNPJs, valida o dígito verificador
(numérico e alfanumérico), consulta na BrasilAPI só os válidos e grava
saidas/fichario_cnpjs.json com uma ficha por CNPJ e a origem de cada um.
Sem internet (ou com OSINT_OFFLINE=1), usa a amostra do CNPJ público de controle.
"""

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

# CNPJs extras para incluir (ex.: o de controle, público). Separe por vírgula.
CNPJS_EXTRAS = "00.000.000/0001-91"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"
AMOSTRAS = {"00000000000191": PASTA_DIA / "dados" / "brasilapi_cnpj_00000000000191.json"}

# Formato com máscara: 2.3.3/4-2, aceitando letras nas 12 primeiras posições (CNPJ alfanumérico).
PADRAO = re.compile(r"\b[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}/[0-9A-Z]{4}-\d{2}\b")


def limpar(cnpj):
    return re.sub(r"[^0-9A-Za-z]", "", cnpj).upper()


def cnpj_valido(cnpj):
    c = limpar(cnpj)
    if not re.fullmatch(r"[0-9A-Z]{12}\d{2}", c) or len(set(c)) == 1:
        return False

    def dv(base, pesos):
        resto = sum((ord(ch) - 48) * p for ch, p in zip(base, pesos)) % 11
        return "0" if resto < 2 else str(11 - resto)

    d1 = dv(c[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return c[12:] == d1 + dv(c[:12] + d1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])


def consultar(cnpj14):
    """Devolve (dados ou None, origem)."""
    if not OFFLINE:
        try:
            req = urllib.request.Request(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj14}",
                                         headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(req, timeout=15) as resposta:
                return json.load(resposta), "ao vivo"
        except urllib.error.HTTPError as erro:
            if erro.code == 404:
                return None, "não encontrado (404)"
        except Exception:
            pass
    if cnpj14 in AMOSTRAS:
        return json.loads(AMOSTRAS[cnpj14].read_text(encoding="utf-8")), "amostra"
    return None, "sem dados"


# ── 1. Varredura: {cnpj: [arquivos onde apareceu]} ────────────────────────
achados = {}
for arquivo in sorted(PASTA_CASO.rglob("*")):
    if arquivo.suffix.lower() in {".txt", ".html", ".csv", ".sql"}:
        for cnpj in PADRAO.findall(arquivo.read_text(encoding="utf-8")):
            achados.setdefault(cnpj, []).append(str(arquivo.relative_to(PASTA_DIA.parent)))
for extra in [c.strip() for c in CNPJS_EXTRAS.split(",") if c.strip()]:
    achados.setdefault(extra, []).append("parâmetro CNPJS_EXTRAS (controle)")

if OFFLINE:
    print("⚠️ MODO OFFLINE: usando a amostra local.")

# ── 2. Uma ficha por CNPJ ─────────────────────────────────────────────────
fichario = []
for cnpj, origens in achados.items():
    ficha = {"cnpj": cnpj, "visto_em": sorted(set(origens)), "valido": cnpj_valido(cnpj),
             "consulta": "não feita (DV inválido)", "razao_social": None, "situacao": None, "socios": []}
    if ficha["valido"]:
        dados, origem = consultar(limpar(cnpj))
        ficha["consulta"] = origem
        if dados:
            ficha["razao_social"] = dados.get("razao_social")
            ficha["situacao"] = dados.get("descricao_situacao_cadastral")
            ficha["socios"] = [{"nome": s.get("nome_socio"), "qualificacao": s.get("qualificacao_socio")}
                               for s in dados.get("qsa", [])]
    fichario.append(ficha)
    marca = "✅" if ficha["valido"] else "🚩"
    print(f"{marca} {cnpj}  {ficha['consulta']:<26} {ficha['razao_social'] or ''}")
    for origem in ficha["visto_em"]:
        print(f"      ↳ {origem}")

# ── 3. Salvar ─────────────────────────────────────────────────────────────
resumo = {"total": len(fichario), "invalidos": sum(not f["valido"] for f in fichario), "fichas": fichario}
SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "fichario_cnpjs.json", "w", encoding="utf-8") as f:
    json.dump(resumo, f, indent=2, ensure_ascii=False)
print(f"\n💾 saidas/fichario_cnpjs.json · {resumo['invalidos']} de {resumo['total']} CNPJs são inválidos.")
