"""
Validar CNPJ — numérico e o novo CNPJ alfanumérico (desde julho de 2026).

Carta 23 (rank B) — Jutsu da Triagem (parte 4)

O que você aprende:
  • a calcular os dois dígitos verificadores do CNPJ com pesos e módulo 11;
  • a usar ord() para transformar um caractere em número (valor = ord(caractere) − 48);
  • por que a MESMA conta serve para o CNPJ antigo (só números) e para o novo (com letras);
  • a primeira pista do caso: o CNPJ do rodapé da loja não passa na validação.

Contexto: a Receita Federal (IN RFB nº 2.229/2024) passou a emitir, a partir de julho de 2026,
CNPJs com letras e números nas 12 primeiras posições. O primeiro foi gerado em 31/07/2026,
para uma filial do Banco do Brasil: 00.000.000/E08G-12. Os dois últimos (os DV) continuam
numéricos, e os CNPJs antigos não mudam.

Como rodar (dentro da pasta dia-02-sintaxe-basica):
    python br/04_valida_cnpj.py
"""

# ── Parâmetros ────────────────────────────────────────────────────────────
CNPJ_RODAPE = "48.217.093/0001-30"  #@param {type:"string"}

# Pesos oficiais. O 1º DV usa 12 pesos; o 2º DV usa 13 (um 6 na frente).
PESOS_DV1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
PESOS_DV2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def valor(caractere):
    """Valor de um caractere na conta: ord() dá o código na tabela ASCII.
    '0' tem código 48, então '0'→0 ... '9'→9. 'A' tem 65, então 'A'→17 ... 'Z'→42."""
    return ord(caractere) - 48


def limpar(cnpj):
    """Tira pontos, barra, traço e espaços; põe as letras em maiúsculas."""
    limpo = ""
    for c in cnpj.upper():
        if c.isalnum():              # isalnum = letra ou número
            limpo += c
    return limpo


def digito(base, pesos):
    """Um dígito verificador: soma de valor × peso, resto por 11."""
    soma = 0
    for caractere, peso in zip(base, pesos):     # zip anda nas duas listas ao mesmo tempo
        soma += valor(caractere) * peso
    resto = soma % 11
    return "0" if resto < 2 else str(11 - resto)


def cnpj_valido(cnpj):
    """True se o CNPJ (numérico ou alfanumérico) tem os DV corretos."""
    c = limpar(cnpj)
    if len(c) != 14:
        return False
    if not c[12:].isdigit():                      # os dois DV são sempre números
        return False
    if len(set(c)) == 1:                          # 00000000000000, 11111111111111...
        return False
    dv1 = digito(c[:12], PESOS_DV1)
    dv2 = digito(c[:12] + dv1, PESOS_DV2)
    return c[12:] == dv1 + dv2


def explicar(cnpj):
    """Mostra a conta inteira, passo a passo."""
    c = limpar(cnpj)
    print(f"\n🔎 {cnpj}  →  limpo: {c}")
    if len(c) != 14:
        print(f"   ❌ tem {len(c)} caracteres (precisa de 14)")
        return
    base = c[:12]
    for numero, pesos in ((1, PESOS_DV1), (2, PESOS_DV2)):
        partes = [f"{ch}({valor(ch)})×{p}" for ch, p in zip(base, pesos)]
        soma = sum(valor(ch) * p for ch, p in zip(base, pesos))
        dv = digito(base, pesos)
        print(f"   DV{numero}: " + " + ".join(partes))
        print(f"        soma = {soma}; {soma} % 11 = {soma % 11} → DV{numero} = {dv}")
        base += dv                                # o 2º DV usa a base + o 1º DV
    esperado = base[12:]
    if c[12:] == esperado:
        print(f"   ✅ VÁLIDO: os DV informados ({c[12:]}) batem com os calculados ({esperado}).")
    else:
        print(f"   ❌ INVÁLIDO: informado {c[12:]}, mas a conta dá {esperado}.")


# ── 1. Exemplos ───────────────────────────────────────────────────────────
print("🏦 CNPJ numérico (Banco do Brasil, dado público):")
explicar("00.000.000/0001-91")

print("\n🔤 CNPJ alfanumérico (o primeiro emitido pela Receita: filial do Banco do Brasil, 31/07/2026):")
explicar("00.000.000/E08G-12")

# ── 2. A pista do caso ────────────────────────────────────────────────────
print("\n" + "═" * 60)
print("🕵️  Caso Vitrine Fantasma: o CNPJ impresso no rodapé da loja")
explicar(CNPJ_RODAPE)
if not cnpj_valido(CNPJ_RODAPE):
    print("\n🚩 PISTA: o CNPJ do rodapé não passa nem na conta dos dígitos verificadores.")
    print("   Empresa de verdade não erra o próprio CNPJ. Ele foi inventado (ou copiado errado).")
    print("   Isso já entra no relatório. No Dia 6, você vai ver que nem vale gastar uma consulta com ele.")

# ── 3. Resumo rápido ──────────────────────────────────────────────────────
print("\n📋 Resumo")
for teste in ("00.000.000/0001-91", "00.000.000/E08G-12", "12.ABC.345/01DE-35", CNPJ_RODAPE, "11.111.111/1111-11", "12.345"):
    print(f"   {teste:<22} {'✅ válido' if cnpj_valido(teste) else '❌ inválido'}")
