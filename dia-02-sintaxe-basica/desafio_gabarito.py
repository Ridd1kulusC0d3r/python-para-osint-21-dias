"""
Gabarito do Desafio S do Dia 2 — Classificador de documentos.

Recebe uma lista misturada de "números de documento" (como os que aparecem soltos numa
conversa de WhatsApp) e, para cada um, diz:
  • o tipo provável (CPF, CNPJ numérico, CNPJ alfanumérico ou desconhecido);
  • se é válido;
  • se for inválido, quais seriam os dígitos verificadores corretos.
Só biblioteca padrão; não usa internet.
"""

DOCUMENTOS = [
    "48.217.093/0001-30",     # CNPJ do rodapé da loja (caso)
    "31.560.427/0001-71",     # "CNPJ do sócio" citado na conversa (caso)
    "019.018.791-35",         # CPF que um cliente mandou "pra nota" (caso)
    "084.520.599-47",         # CPF da denúncia DEN-007 (caso)
    "00.000.000/0001-91",     # Banco do Brasil (público)
    "00.000.000/E08G-12",     # 1º CNPJ alfanumérico emitido (filial do Banco do Brasil, público)
    "(31) 98888-0101",        # telefone com 11 dígitos: NÃO pode ser confundido com CPF
]

PESOS_CNPJ_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
PESOS_CNPJ_2 = [6] + PESOS_CNPJ_1


def mod11(soma):
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def dv_cpf(nove):
    """Recebe os 9 primeiros dígitos (texto) e devolve os 2 DV corretos (texto)."""
    numeros = [int(c) for c in nove]
    d1 = mod11(sum(n * p for n, p in zip(numeros, range(10, 1, -1))))
    d2 = mod11(sum(n * p for n, p in zip(numeros + [d1], range(11, 1, -1))))
    return f"{d1}{d2}"


def dv_cnpj(doze):
    """Recebe as 12 primeiras posições (texto, pode ter letras) e devolve os 2 DV."""
    valores = [ord(c) - 48 for c in doze]
    d1 = mod11(sum(v * p for v, p in zip(valores, PESOS_CNPJ_1)))
    d2 = mod11(sum(v * p for v, p in zip(valores + [d1], PESOS_CNPJ_2)))
    return f"{d1}{d2}"


def classificar(texto):
    """Devolve (tipo, válido?, DV corretos) para um texto qualquer."""
    limpo = "".join(c for c in texto.upper() if c.isalnum())
    tem_letra = any(c.isalpha() for c in limpo)

    # Telefone também pode ter 11 dígitos! A pista é o formato: parênteses no DDD ou +55.
    if "(" in texto or texto.strip().startswith("+"):
        return "telefone", False, "—"

    if len(limpo) == 11 and not tem_letra and "/" not in texto:
        if len(set(limpo)) == 1:
            return "CPF", False, "—"
        certo = dv_cpf(limpo[:9])
        return "CPF", limpo[9:] == certo, certo

    if len(limpo) == 14 and limpo[12:].isdigit():
        tipo = "CNPJ alfanumérico" if tem_letra else "CNPJ numérico"
        if len(set(limpo)) == 1:
            return tipo, False, "—"
        certo = dv_cnpj(limpo[:12])
        return tipo, limpo[12:] == certo, certo

    return "desconhecido", False, "—"


print(f"{'Documento':<22} {'Tipo':<18} {'Resultado':<12} DV corretos")
print("─" * 66)
contagem = {}
for doc in DOCUMENTOS:
    tipo, ok, certo = classificar(doc)
    contagem[tipo] = contagem.get(tipo, 0) + 1          # dicionário como contador
    if tipo in ("desconhecido", "telefone"):
        resultado = "⚪ ignorado"
    else:
        resultado = "✅ válido" if ok else "❌ inválido"
    print(f"{doc:<22} {tipo:<18} {resultado:<12} {certo if not ok else ''}")

print("─" * 66)
print("📊 " + " · ".join(f"{tipo}: {n}" for tipo, n in contagem.items()))
print("\n🕵️  Os dois CNPJs que o vendedor usou são inválidos: nenhuma empresa pode ter esses números.")
print("   Repare: 'DV corretos' mostra qual seria o final certo. NÃO use isso para 'consertar'")
print("   um documento e consultá-lo: o número corrigido provavelmente é de outra pessoa ou empresa.")
