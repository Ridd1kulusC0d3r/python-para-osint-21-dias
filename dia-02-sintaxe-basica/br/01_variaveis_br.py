"""
Variáveis à brasileira: tipos de dado e dinheiro no formato R$ 1.999,00.

Carta 23 (rank B) — Jutsu da Triagem (parte 1)

O que você aprende:
  • os quatro tipos básicos: texto (str), inteiro (int), decimal (float) e verdadeiro/falso (bool);
  • a descobrir o tipo de qualquer valor com type();
  • a converter de um tipo para outro (int("37"), str(37), float("149.90"));
  • por que "37" + 1 dá erro e como resolver;
  • a escrever uma função que mostra dinheiro no padrão brasileiro.

Como rodar (dentro da pasta dia-02-sintaxe-basica):
    python br/01_variaveis_br.py
"""

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
VALOR_PIX = 1999.0  #@param {type:"number"}
VALOR_DIGITADO = "1.999,00"  #@param {type:"string"}

# ── 1. Os quatro tipos básicos ────────────────────────────────────────────
# Em Python você não precisa declarar o tipo: ele é deduzido pelo valor.
vitima = "Mariana Lima Carvalho"     # str: texto, sempre entre aspas
parcelas = 1                         # int: número inteiro
valor = 1899.00                      # float: número com casas decimais (ponto, não vírgula!)
pagou_no_pix = True                  # bool: True (verdadeiro) ou False (falso)

print("🧪 Os quatro tipos básicos")
# type() diz o tipo; .__name__ mostra só o nome curto (str, int...).
for nome, conteudo in [("vitima", vitima), ("parcelas", parcelas),
                       ("valor", valor), ("pagou_no_pix", pagou_no_pix)]:
    print(f"   {nome:<13} = {conteudo!r:<26} → {type(conteudo).__name__}")
# O !r mostra o valor "como o Python vê" (texto aparece com aspas).

# ── 2. Converter tipos ────────────────────────────────────────────────────
# Dados que chegam de formulários, planilhas e sites quase sempre chegam como TEXTO.
print("\n🔄 Convertendo tipos")
total_texto = "37"
print(f"   '37' é {type(total_texto).__name__}; int('37') + 1 = {int(total_texto) + 1}")
print(f"   str(37) + ' denúncias' = {str(37) + ' denúncias'!r}")
print(f"   float('149.90') = {float('149.90')}")

# Tentar somar texto com número dá TypeError. O try/except mostra o erro sem parar o script.
try:
    print(total_texto + 1)
except TypeError as erro:
    print(f"   ❌ '37' + 1 → TypeError: {erro}")

# ── 3. Nomes de variáveis ─────────────────────────────────────────────────
# Pode: letras, números (menos no começo) e _. Use nomes que expliquem o conteúdo.
# Pode acento? Pode (valor_médio funciona), mas o costume é evitar em nomes de variáveis.
cidade_da_vitima = "Divinópolis"     # bom: diz o que é
x = "Divinópolis"                    # ruim: daqui a uma semana você não lembra o que é x
print(f"\n🏷️  Nome claro: cidade_da_vitima = {cidade_da_vitima!r}  (melhor que x = {x!r})")


# ── 4. Dinheiro no formato brasileiro ─────────────────────────────────────
# Uma FUNÇÃO é um bloco de código com nome que você pode reaproveitar.
# def cria a função; o que vem entre parênteses são as entradas; return devolve o resultado.
def reais(numero):
    """Transforma 1999.0 em 'R$ 1.999,00'."""
    americano = f"{numero:,.2f}"                      # '1,999.00' (milhar com vírgula, decimal com ponto)
    # Trocamos os símbolos usando um "coringa" (§) para um não apagar o outro.
    brasileiro = americano.replace(",", "§").replace(".", ",").replace("§", ".")
    return f"R$ {brasileiro}"


def ler_reais(texto):
    """O caminho inverso: transforma 'R$ 1.999,00' (ou '1.999,00') em 1999.0."""
    limpo = texto.replace("R$", "").strip()           # tira o símbolo e os espaços das pontas
    limpo = limpo.replace(".", "").replace(",", ".")  # '1.999,00' → '1999.00'
    return float(limpo)


print("\n💸 Dinheiro à brasileira")
for v in (VALOR_PIX, 149.9, 54877.4, 0.5, 1234567.891):
    print(f"   {v!r:>12} → {reais(v)}")

convertido = ler_reais(VALOR_DIGITADO)
print(f"\n   Texto digitado {VALOR_DIGITADO!r} → número {convertido} → de volta: {reais(convertido)}")

# ── 5. Um cuidado com float ───────────────────────────────────────────────
# O computador guarda decimais em binário, e alguns valores não "fecham" exatamente.
print(f"\n⚠️  0.1 + 0.2 = {0.1 + 0.2}  (por isso, para somar dinheiro de verdade, o Dia 7 usa Decimal)")
