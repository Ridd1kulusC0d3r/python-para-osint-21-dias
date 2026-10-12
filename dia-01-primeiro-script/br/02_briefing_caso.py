"""
Briefing do caso: o primeiro relatório da Operação Vitrine Fantasma na tela.

Carta 22 (rank B) — Jutsu do Primeiro Alerta (parte 2)

O que você aprende:
  • a guardar os números do caso em variáveis (texto, inteiro, decimal);
  • a montar um texto de várias linhas com aspas triplas e f-string;
  • a formatar números: casas decimais, separador de milhar, porcentagem;
  • que, se o número mudar, você troca UMA variável e o relatório inteiro se atualiza.

Os números abaixo são do caso fictício (caso/dados/). Nos próximos dias você vai
aprender a calculá-los direto dos arquivos, em vez de digitá-los.

Como rodar (dentro da pasta dia-01-primeiro-script):
    python br/02_briefing_caso.py
"""

# ── Parâmetros ────────────────────────────────────────────────────────────
ANALISTA = "Analista"  #@param {type:"string"}

# ── 1. Os fatos do caso, cada um numa variável ────────────────────────────
# Texto (str) vai entre aspas; número inteiro (int) e decimal (float) vão sem aspas.
# Em Python o decimal usa PONTO: 54877.40, e não 54.877,40.
OPERACAO = "Vitrine Fantasma"
LOJA = "MegaOferta Brasil"
DOMINIO = "megaoferta-brasil.example"
SOLICITANTE = "Delegada Rita Assunção"
TOTAL_DENUNCIAS = 37
TOTAL_CIDADES = 11
CHAVES_PIX = 3
PREJUIZO_TOTAL = 54877.40          # soma dos valores das 37 denúncias, em reais
PRIMEIRA_DENUNCIA = "12/10/2025"
ULTIMA_DENUNCIA = "30/11/2025"
DIAS_DE_GOLPE = 49                 # 30/11 menos 12/10/2025 = 49 dias
PRODUTO_ISCA = "iPhone 15 128GB"
PRECO_ISCA = 1999.00
PRECO_REFERENCIA = 5000.00         # PARÂMETRO HIPOTÉTICO: troque pelo preço que você pesquisar hoje

# ── 2. Algumas contas com as variáveis ────────────────────────────────────
# O computador faz a conta; você só escreve a fórmula.
media_por_vitima = PREJUIZO_TOTAL / TOTAL_DENUNCIAS
denuncias_por_dia = TOTAL_DENUNCIAS / DIAS_DE_GOLPE
desconto = 1 - PRECO_ISCA / PRECO_REFERENCIA       # 0.60 significa 60%

# ── 3. O briefing ─────────────────────────────────────────────────────────
# Aspas triplas (""") deixam o texto ocupar várias linhas.
# Dentro das chaves, depois dos dois-pontos, vem o FORMATO:
#   :.2f  → 2 casas decimais        :,.2f → com separador de milhar
#   :.0%  → porcentagem sem casas   :>5   → alinhado à direita em 5 espaços
briefing = f"""
╔══════════════════════════════════════════════════════════════╗
  🕵️  NÚCLEO DE FONTES ABERTAS · BRIEFING
  Operação {OPERACAO}
╚══════════════════════════════════════════════════════════════╝

  Solicitante ........ {SOLICITANTE}
  Analista ........... {ANALISTA}

  🎯 Alvo
     Loja virtual "{LOJA}"
     Endereço na web: {DOMINIO}

  📨 Denúncias
     Total ........... {TOTAL_DENUNCIAS:>5}
     Cidades de MG ... {TOTAL_CIDADES:>5}
     Período ......... {PRIMEIRA_DENUNCIA} a {ULTIMA_DENUNCIA} ({DIAS_DE_GOLPE} dias)
     Ritmo ........... {denuncias_por_dia:.2f} denúncia(s) por dia

  💸 Dinheiro
     Prejuízo total .. R$ {PREJUIZO_TOTAL:,.2f}
     Média/vítima .... R$ {media_por_vitima:,.2f}
     Chaves PIX ...... {CHAVES_PIX} diferentes

  🪤 A isca
     {PRODUTO_ISCA} por R$ {PRECO_ISCA:,.2f}: {desconto:.0%} abaixo de R$ {PRECO_REFERENCIA:,.2f}
     (preço de referência hipotético; pesquise o real antes de usar num relatório).

  ❓ Perguntas para os próximos dias
     1. Os CPFs das denúncias são válidos?          (Dia 2)
     2. Existe algum perfil "kau.ofertas" público?   (Dia 3)
     3. O que as vítimas contaram nos depoimentos?   (Dia 4)
"""

print(briefing)

# ── 4. Atenção: o formato brasileiro de dinheiro ──────────────────────────
# O Python formata no padrão americano: 54,877.40. No Brasil escrevemos 54.877,40.
# Um truque simples (que você vai entender melhor no Dia 2): trocar os símbolos de lugar.
americano = f"{PREJUIZO_TOTAL:,.2f}"                                   # "54,877.40"
brasileiro = americano.replace(",", "X").replace(".", ",").replace("X", ".")
print(f"💡 Padrão americano: {americano}  →  padrão brasileiro: R$ {brasileiro}")
