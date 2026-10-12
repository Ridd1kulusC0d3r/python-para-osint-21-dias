"""
Regex à brasileira: CPF, CNPJ, telefone, CEP, placa, chave PIX e e-mail.

Carta 32 (rank A) — Jutsu do Padrão Brasileiro

O que você aprende:
  • a ler uma expressão regular pedaço por pedaço (\\d, {n}, ?, [ ], ( ));
  • a escrever regex comentadas com re.VERBOSE (espaços e # viram explicação);
  • padrões dos documentos e identificadores mais comuns no Brasil;
  • a testar cada padrão com exemplos que DEVEM e que NÃO DEVEM casar.

Todos os exemplos são inventados. Como rodar (dentro da pasta dia-11-regex):
    python br/01_padroes_br.py
"""

import re

# ── Mini-dicionário de regex (cole na parede) ─────────────────────────────
#   \d       um dígito (0-9)              [A-Z]   uma letra maiúscula
#   {3}      exatamente 3 vezes           {2,5}   de 2 a 5 vezes
#   ?        "pode ter ou não" (0 ou 1)   +       uma ou mais vezes
#   [.-]     um ponto OU um hífen         \.      um ponto de verdade
#   (?: )    grupo sem captura            |       "ou"
#   \b       borda de palavra: impede casar no meio de um número maior
#   (?<!\d)  "não pode ter dígito antes"  (?!\d)  "não pode ter dígito depois"

PADROES = {
    # CPF: 000.000.000-00 ou 00000000000. Pontos e hífen são opcionais.
    "CPF": re.compile(r"""
        (?<!\d)          # não começa no meio de outro número
        \d{3} \.? \d{3} \.? \d{3}   # três blocos de 3 dígitos, ponto opcional
        -? \d{2}         # hífen opcional + 2 dígitos verificadores
        (?!\d)           # e não continua com mais dígitos
    """, re.VERBOSE),

    # CNPJ numérico: 00.000.000/0000-00 (ou só os 14 dígitos).
    "CNPJ": re.compile(r"""
        (?<!\d)
        \d{2} \.? \d{3} \.? \d{3}   # raiz: 8 dígitos
        /? \d{4}                    # barra opcional + 4 dígitos da filial (0001 = matriz)
        -? \d{2}                    # 2 dígitos verificadores
        (?!\d)
    """, re.VERBOSE),

    # CNPJ alfanumérico (novo formato da Receita a partir de julho/2026):
    # as 12 primeiras posições podem ter LETRAS maiúsculas; os 2 verificadores seguem numéricos.
    "CNPJ alfanumérico": re.compile(r"""
        (?<![A-Z0-9])
        [A-Z0-9]{2} \.? [A-Z0-9]{3} \.? [A-Z0-9]{3}
        /? [A-Z0-9]{4}
        -? \d{2}
        (?![A-Z0-9])
    """, re.VERBOSE),

    # Telefone: +55 opcional, DDD com ou sem parênteses, 9 opcional (celular), 4+4 dígitos.
    "Telefone": re.compile(r"""
        (?<!\d)
        (?: \+?55 [\s-]? )?          # código do país, opcional
        \(? [1-9]\d \)? [\s-]?       # DDD: dois dígitos, o primeiro nunca é 0
        (?: 9 [\s-]? )?              # nono dígito dos celulares, opcional
        \d{4} [\s-]? \d{4}           # número: 4 + 4
        (?!\d)
    """, re.VERBOSE),

    # CEP: 00000-000 ou 00000000.
    "CEP": re.compile(r"(?<!\d)\d{5}-?\d{3}(?!\d)"),

    # Placa Mercosul (ABC1D23) e antiga (ABC-1234).
    "Placa Mercosul": re.compile(r"\b[A-Z]{3}\d[A-Z]\d{2}\b"),
    "Placa antiga": re.compile(r"\b[A-Z]{3}-?\d{4}\b"),

    # Chave PIX aleatória: um UUID (8-4-4-4-12 caracteres hexadecimais).
    "Chave PIX aleatória": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),

    # E-mail: versão mais "certinha" que a do original (o hífen fica no fim dos colchetes).
    "E-mail": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
}

# ── Bateria de testes: (texto, deveria casar?) ────────────────────────────
TESTES = {
    "CPF": [("123.456.789-09", True), ("12345678909", True), ("123.456.789-0", False), ("1234567890912", False)],
    "CNPJ": [("12.345.678/0001-95", True), ("12345678000195", True), ("12.345.678/0001", False)],
    "CNPJ alfanumérico": [("12.ABC.345/01DE-35", True), ("12ABC34501DE35", True), ("12.ABC.345/01DE-3X", False)],
    "Telefone": [("(31) 98888-0101", True), ("+55 31 9 8888-0101", True), ("3133334444", True), ("98888", False)],
    "CEP": [("30130-010", True), ("30130010", True), ("3013-0010", False)],
    "Placa Mercosul": [("BRA2E19", True), ("BRA-2019", False)],
    "Placa antiga": [("BRA-2019", True), ("BRA2019", True), ("BRA2E19", False)],
    "Chave PIX aleatória": [("123e4567-e89b-12d3-a456-426614174000", True), ("123e4567-e89b-12d3-a456", False)],
    "E-mail": [("fulano.de_tal@exemplo.com.br", True), ("fulano@", False), ("@exemplo.com", False)],
}

# ── Rodar a bateria e mostrar o resultado ─────────────────────────────────
erros = 0
for nome, padrao in PADROES.items():
    print(f"\n🔎 {nome}")
    for texto, esperado in TESTES[nome]:
        # fullmatch exige que o TEXTO INTEIRO case (search aceitaria um pedaço).
        casou = padrao.fullmatch(texto) is not None
        ok = casou == esperado
        erros += not ok
        print(f"   {'✅' if ok else '❌'} {texto:<40} casou={casou}  (esperado={esperado})")

print(f"\n{'🎉 Todos os testes passaram!' if erros == 0 else f'⚠️ {erros} teste(s) falharam.'}")

# ── Regex acha FORMATO, não verdade ───────────────────────────────────────
print("\n🧠 Lembre-se: '111.111.111-11' casa com a regex de CPF, mas não é um CPF válido.")
print("   A regex encontra CANDIDATOS. Quem confirma é o dígito verificador (script 03).")
