"""
Triagem de CPFs: validar uma lista inteira de denúncias e contar o resultado.

Carta 23 (rank B) — Jutsu da Triagem (parte 3, aplicação no caso)

O que você aprende:
  • a guardar vários registros numa lista de listas ([id, cpf]);
  • a transformar o validador do script 02 numa função reutilizável;
  • a percorrer a lista com for, decidir com if e ir contando com variáveis;
  • a montar uma pequena tabela com ✅ / ❌ e um resumo no final.

Os 10 CPFs abaixo foram copiados de caso/dados/denuncias.csv (fictícios).
No Dia 7 você vai aprender a ler o CSV inteiro direto do arquivo.

Como rodar (dentro da pasta dia-02-sintaxe-basica):
    python br/03_triagem_cpfs.py
"""

# ── Parâmetros ────────────────────────────────────────────────────────────
MOSTRAR_SO_INVALIDOS = False  #@param {type:"boolean"}

# ── A lista de denúncias (id, CPF informado pela vítima) ──────────────────
# Cada item da lista é outra lista com dois elementos. [0] é o id, [1] é o CPF.
DENUNCIAS = [
    ["DEN-005", "978.753.477-18"],
    ["DEN-006", "267.147.513-62"],
    ["DEN-007", "084.520.599-47"],
    ["DEN-008", "628.360.161-83"],
    ["DEN-009", "177.992.298-10"],
    ["DEN-010", "073.702.838-60"],
    ["DEN-011", "477.647.258-97"],
    ["DEN-012", "205.258.983-01"],
    ["DEN-013", "621.052.185-17"],
    ["DEN-014", "304.118.955-06"],
]


def cpf_valido(cpf):
    """Devolve True se a conta dos dígitos verificadores do CPF fecha."""
    digitos = [int(c) for c in cpf if c.isdigit()]   # mesma ideia do script 02, numa linha só
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    for posicao in (9, 10):
        soma = 0
        for i in range(posicao):
            # Peso começa em posicao+1 (10 ou 11) e diminui 1 a cada dígito.
            soma += digitos[i] * (posicao + 1 - i)
        resto = soma % 11
        dv = 0 if resto < 2 else 11 - resto
        if dv != digitos[posicao]:
            return False                              # na primeira falha, já sabemos a resposta
    return True


# ── A triagem ─────────────────────────────────────────────────────────────
validos = 0                  # contadores começam em zero
invalidos = 0
para_conferir = []           # aqui guardamos os ids que precisam de atenção

print(f"{'Denúncia':<9}  {'CPF':<15}  Resultado")
print("─" * 40)
for denuncia in DENUNCIAS:
    identificador = denuncia[0]
    cpf = denuncia[1]
    if cpf_valido(cpf):
        validos += 1
        if not MOSTRAR_SO_INVALIDOS:
            print(f"{identificador:<9}  {cpf:<15}  ✅ válido")
    else:
        invalidos += 1
        para_conferir.append(identificador)
        print(f"{identificador:<9}  {cpf:<15}  ❌ inválido")

# ── Resumo ────────────────────────────────────────────────────────────────
total = len(DENUNCIAS)
print("─" * 40)
print(f"📊 {total} CPFs analisados: {validos} válidos e {invalidos} inválidos "
      f"({invalidos / total:.0%} da amostra).")

if para_conferir:
    print(f"🔍 Pedir à equipe para conferir os documentos originais de: {', '.join(para_conferir)}")
    print("   CPF inválido numa denúncia quase sempre é erro de digitação, não fraude da vítima.")
