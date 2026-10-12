"""
Regex acha, dígito verificador confirma: menos falso positivo.

Carta 32 (rank A) — Jutsu do Padrão Brasileiro (parte 3)

O que você aprende:
  • por que "casar com a regex" não é o mesmo que "ser um documento válido";
  • a juntar a regex do Dia 11 com o cálculo de dígito verificador do Dia 2;
  • a validar CNPJ numérico E alfanumérico com a mesma função (valor = ord(c) − 48);
  • a classificar cada achado em ✅ válido ou 🚩 inválido.

Este script é 100% offline: lê caso/dados/conversa_whatsapp.txt (fictício).

Como rodar (dentro da pasta dia-11-regex):
    python br/03_regex_mais_validacao.py
"""

import re
from pathlib import Path

ARQUIVO = "conversa_whatsapp.txt"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

RE_CPF = re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)")
# Aceita CNPJ numérico e alfanumérico (letras só nas 12 primeiras posições).
RE_CNPJ = re.compile(r"(?<![A-Z0-9])[A-Z0-9]{2}\.?[A-Z0-9]{3}\.?[A-Z0-9]{3}/?[A-Z0-9]{4}-?\d{2}(?![A-Z0-9])")


def so_caracteres(texto):
    """Tira pontos, barras e hífens: '48.217.093/0001-30' → '48217093000130'."""
    return re.sub(r"[^0-9A-Z]", "", texto.upper())


def cpf_valido(cpf):
    """Confere os 2 dígitos verificadores do CPF (mesmo algoritmo do Dia 2)."""
    n = [int(c) for c in so_caracteres(cpf)]
    if len(n) != 11 or len(set(n)) == 1:        # 111.111.111-11 passa na conta, mas é inválido
        return False
    for tamanho in (9, 10):                      # 1º DV usa 9 dígitos; 2º DV usa 10
        soma = sum(d * peso for d, peso in zip(n[:tamanho], range(tamanho + 1, 1, -1)))
        dv = (soma * 10) % 11 % 10               # resto 10 vira 0
        if dv != n[tamanho]:
            return False
    return True


def cnpj_valido(cnpj):
    """
    Confere os DVs do CNPJ. Funciona para o formato numérico e o alfanumérico:
    cada caractere vale ord(c) - 48 ('0'→0 … '9'→9, 'A'→17, 'B'→18 …). Pesos iguais aos de sempre.
    """
    c = so_caracteres(cnpj)
    if len(c) != 14 or not c[-2:].isdigit() or len(set(c)) == 1:
        return False
    valores = [ord(ch) - 48 for ch in c]
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for posicao in (12, 13):                     # 1º DV olha 12 caracteres; 2º olha 13
        p = pesos if posicao == 12 else [6] + pesos
        resto = sum(v * peso for v, peso in zip(valores[:posicao], p)) % 11
        dv = 0 if resto < 2 else 11 - resto
        if dv != valores[posicao]:
            return False
    return True


# ── 1. Teste rápido das funções com exemplos conhecidos ───────────────────
print("🧪 Autoteste:")
for exemplo, func, esperado in [
    ("00.000.000/0001-91", cnpj_valido, True),     # Banco do Brasil (CNPJ público)
    ("12.ABC.345/01DE-35", cnpj_valido, True),     # exemplo alfanumérico usado pela Receita
    ("111.111.111-11", cpf_valido, False),         # casa com a regex, mas é inválido
]:
    print(f"   {'✅' if func(exemplo) == esperado else '❌'} {exemplo:<20} válido={func(exemplo)}")

# ── 2. Aplicar na conversa ────────────────────────────────────────────────
texto = (PASTA_CASO / ARQUIVO).read_text(encoding="utf-8")

# Os CNPJs são procurados primeiro e depois "apagados" do texto, para que
# os 11 primeiros dígitos de um CNPJ não sejam confundidos com um CPF.
cnpjs = RE_CNPJ.findall(texto)
texto_sem_cnpj = RE_CNPJ.sub(" ", texto)
cpfs = RE_CPF.findall(texto_sem_cnpj)

print(f"\n🔎 Candidatos encontrados pela regex: {len(cnpjs)} CNPJ, {len(cpfs)} CPF\n")
invalidos = 0
for tipo, lista, validar in [("CNPJ", cnpjs, cnpj_valido), ("CPF", cpfs, cpf_valido)]:
    for doc in lista:
        ok = validar(doc)
        invalidos += not ok
        print(f"   {tipo:<5} {doc:<20} {'✅ dígito verificador confere' if ok else '🚩 INVÁLIDO (DV não confere)'}")

# ── 3. Leitura de analista ────────────────────────────────────────────────
print("\n🧠 Os dois CNPJs que o vendedor mandou ('pode confiar' e 'do sócio') são inválidos:")
print("   nenhuma empresa registrada pode ter esses números. Isso é pista de fraude e")
print("   também evita gastar consulta em API de CNPJ à toa.")
print("   O CPF válido é da VÍTIMA (enviado 'pra nota'): dado pessoal, trate com cuidado (LGPD).")
print(f"\n📊 Resumo: {len(cnpjs) + len(cpfs)} candidatos, {invalidos} inválidos descartados.")
