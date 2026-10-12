"""
Validar CPF: o algoritmo dos dígitos verificadores, passo a passo.

Carta 23 (rank B) — Jutsu da Triagem (parte 2)

O que você aprende:
  • a percorrer os caracteres de um texto com for e guardar só os dígitos;
  • a usar if/elif/else para rejeitar entradas com tamanho errado ou dígitos todos iguais;
  • a calcular os dois dígitos verificadores (DV) do CPF com laços e o resto da divisão (%);
  • que "CPF válido" quer dizer só "a conta fecha" — não que a pessoa existe.

Como rodar (dentro da pasta dia-02-sintaxe-basica):
    python br/02_valida_cpf.py

O CPF padrão é fictício (de caso/dados/denuncias.csv).
"""

# ── Parâmetros ────────────────────────────────────────────────────────────
CPF = "973.091.141-08"  #@param {type:"string"}
MOSTRAR_CONTAS = True  #@param {type:"boolean"}

# ── Como funciona (leia antes do código) ──────────────────────────────────
# Um CPF tem 11 dígitos: 9 "de base" + 2 verificadores (DV).
#   1º DV: multiplique os 9 primeiros dígitos pelos pesos 10, 9, 8, ..., 2 e some tudo.
#          Pegue o resto da divisão da soma por 11.  Resto < 2 → DV = 0.  Senão → DV = 11 − resto.
#   2º DV: a mesma coisa com os 10 primeiros dígitos (base + 1º DV) e pesos 11, 10, ..., 2.
# Se os dois DV calculados forem iguais aos dois últimos dígitos do CPF, a conta fecha.

# ── Passo 1: ficar só com os dígitos ──────────────────────────────────────
# Percorremos cada caractere; isdigit() é True para '0'...'9'. Pontos e traço ficam de fora.
digitos = []
for caractere in CPF:
    if caractere.isdigit():
        digitos.append(int(caractere))      # guardamos como número para poder multiplicar

print(f"🔢 Entrada: {CPF!r} → dígitos: {digitos}")

# ── Passo 2: checagens básicas ────────────────────────────────────────────
# if / elif / else: só UM dos blocos roda, o primeiro cuja condição for verdadeira.
valido = True
motivo = ""
if len(digitos) != 11:
    valido = False
    motivo = f"tem {len(digitos)} dígitos (precisa de 11)"
elif len(set(digitos)) == 1:
    # set() remove repetidos. Se sobrar 1 elemento, todos são iguais (ex.: 111.111.111-11).
    # Esses CPFs "fecham a conta", mas a Receita não os considera válidos.
    valido = False
    motivo = "todos os dígitos são iguais"
else:
    # ── Passo 3: calcular os dois dígitos verificadores ───────────────────
    calculados = []
    for posicao in (9, 10):                 # 1ª volta: usa 9 dígitos; 2ª volta: usa 10
        soma = 0
        peso = posicao + 1                  # 10 na 1ª volta, 11 na 2ª
        base = digitos[:posicao]            # fatia: os primeiros 9 (ou 10) dígitos
        for digito in base:
            if MOSTRAR_CONTAS:
                print(f"      {digito} × {peso:>2} = {digito * peso:>3}")
            soma += digito * peso           # += é "some ao que já tinha"
            peso -= 1                       # o peso diminui 1 a cada dígito
        resto = soma % 11                   # % é o resto da divisão
        dv = 0 if resto < 2 else 11 - resto
        print(f"   ➕ soma = {soma}; {soma} % 11 = {resto} → DV {len(calculados) + 1} = {dv}")
        calculados.append(dv)

    informados = digitos[9:]                # os dois últimos dígitos do CPF
    print(f"   🎯 DV calculados: {calculados}  ·  DV informados: {informados}")
    if calculados != informados:
        valido = False
        motivo = "os dígitos verificadores não batem"

# ── Passo 4: o veredito ───────────────────────────────────────────────────
if valido:
    print(f"\n✅ {CPF} é VÁLIDO (a conta dos dígitos verificadores fecha).")
    print("   Lembre-se: válido ≠ existente. Só a Receita confirma se o CPF existe e de quem é.")
else:
    print(f"\n❌ {CPF} é INVÁLIDO: {motivo}.")
    print("   Pode ser erro de digitação da vítima, ou um número inventado. Anote e confira o original.")
