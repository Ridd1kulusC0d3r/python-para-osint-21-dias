"""
Caso Vitrine Fantasma: o CNPJ do rodapé da loja existe?

Carta 27 (rank B) — Jutsu do Mapa do JSON (aplicação no caso)

O que você aprende:
  • a VALIDAR um dado antes de gastar uma consulta (dígito verificador do CNPJ, Dia 2);
  • que a validação vale também para o novo CNPJ alfanumérico (letras A–Z nas 12 primeiras posições);
  • a registrar a pista num pequeno dicionário que vira JSON (amanhã ele cresce).

Como rodar (dentro da pasta dia-06-json):
    python br/02_caso_cnpj_rodape.py
    OSINT_OFFLINE=1 python br/02_caso_cnpj_rodape.py
"""

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:                              # Windows sem tzdata
    FUSO_BR = timezone(timedelta(hours=-3))


def cnpj_valido(cnpj):
    """Confere os dois dígitos verificadores. Aceita CNPJ numérico e alfanumérico.

    Cada caractere vale ord(c) - 48: '0'→0 … '9'→9, 'A'→17, 'B'→18 …
    Os pesos e o "módulo 11" são os mesmos de sempre.
    """
    limpo = re.sub(r"[^0-9A-Za-z]", "", cnpj).upper()      # tira . / -
    if not re.fullmatch(r"[0-9A-Z]{12}[0-9]{2}", limpo) or len(set(limpo)) == 1:
        return False

    def digito(base, pesos):
        soma = sum((ord(c) - 48) * p for c, p in zip(base, pesos))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    d1 = digito(limpo[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = digito(limpo[:12] + d1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return limpo[12:] == d1 + d2


# ── 1. Pegar o CNPJ do rodapé da vitrine salva ────────────────────────────
html = (PASTA_CASO / "vitrine_megaoferta.html").read_text(encoding="utf-8")
achado = re.search(r"CNPJ\s*([0-9A-Z]{2}\.?[0-9A-Z]{3}\.?[0-9A-Z]{3}/?[0-9A-Z]{4}-?\d{2})", html)
cnpj = achado.group(1) if achado else "48.217.093/0001-30"
print(f"🏷️  CNPJ no rodapé da loja: {cnpj}")

# ── 2. Validar ANTES de consultar ─────────────────────────────────────────
# Consulta custa: tempo, cota de API e um registro do seu IP lá no servidor.
# Se o número nem é um CNPJ possível, não há o que perguntar.
valido = cnpj_valido(cnpj)
pista = {
    "pista": "CNPJ do rodapé da vitrine",
    "valor": cnpj,
    "fonte": "caso/dados/vitrine_megaoferta.html (rodapé)",
    "digito_verificador_ok": valido,
    "consultado_na_api": False,
    "registrado_em": datetime.now(FUSO_BR).isoformat(timespec="seconds"),
}

if not valido:
    print("🚩 Dígito verificador INVÁLIDO: esse número não pode ser de nenhuma empresa.")
    print("   Não gastamos consulta. Um CNPJ inventado é, por si só, uma pista forte de fraude.")
    pista["conclusao"] = "CNPJ inexistente (falha no dígito verificador): provavelmente inventado."
else:
    # Só chega aqui se o número for possível. Mesmo assim pode não existir (HTTP 404).
    pista["consultado_na_api"] = True
    url = f"https://brasilapi.com.br/api/cnpj/v1/{re.sub(r'[^0-9A-Za-z]', '', cnpj)}"
    if OFFLINE:
        print("⚠️ MODO OFFLINE: CNPJ válido, mas não há amostra do caso; consulta pulada.")
        pista["conclusao"] = "Válido; consultar a API quando houver internet."
    else:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(req, timeout=15) as resposta:
                empresa = json.load(resposta)
            pista["conclusao"] = f"Existe: {empresa.get('razao_social')} ({empresa.get('descricao_situacao_cadastral')})"
        except urllib.error.HTTPError as erro:
            pista["conclusao"] = "Não encontrado na base (HTTP 404)." if erro.code == 404 else f"Erro HTTP {erro.code}"
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}).")
            pista["conclusao"] = "Válido; consulta falhou, tentar de novo."

# ── 3. Prova de que o validador funciona (testes de controle) ─────────────
# Antes de acusar um número de falso, testamos o validador com casos conhecidos.
# NUNCA "conserte" o CNPJ do suspeito para achar o "certo": o resultado pode ser
# uma empresa real e inocente, sem nada a ver com o golpe.
controles = {
    "00.000.000/0001-91": True,    # Banco do Brasil (público, válido)
    "12.ABC.345/01DE-35": True,    # exemplo de CNPJ alfanumérico (formato novo da Receita)
    "11.111.111/1111-11": False,   # todos iguais: inválido por regra
}
for numero, esperado in controles.items():
    ok = cnpj_valido(numero) == esperado
    print(f"   {'✅' if ok else '❌'} controle {numero}: {'válido' if cnpj_valido(numero) else 'inválido'}")

# ── 4. Registrar a pista ──────────────────────────────────────────────────
print("\n📝 Pista registrada:")
print(json.dumps(pista, indent=2, ensure_ascii=False))
