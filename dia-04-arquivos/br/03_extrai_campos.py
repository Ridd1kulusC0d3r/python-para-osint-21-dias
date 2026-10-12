"""
Extrair campos dos depoimentos: vítima, contato, chave PIX e valor, num resumo.

Carta 25 (rank B) — Jutsu dos Depoimentos (parte 3, aplicação no caso)

O que você aprende:
  • a procurar linhas que começam com um rótulo ("Vítima:", "Contato:") usando startswith();
  • a cortar texto com split() e partition() para pegar só o pedaço que interessa;
  • a guardar o que encontrou em dicionários (um por depoimento) e juntar tudo numa lista;
  • a gravar um resumo em texto (para gente ler) e em TSV (para planilha) em saidas/.

Sem expressões regulares: só métodos de texto. No Dia 11 você faz isso com regex.

Como rodar (dentro da pasta dia-04-arquivos):
    python br/03_extrai_campos.py
"""

from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_DEPOIMENTOS = PASTA_DIA.parent / "caso" / "dados" / "depoimentos"
SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)

fichas = []                                   # uma ficha (dicionário) por depoimento

for caminho in sorted(PASTA_DEPOIMENTOS.glob("*.txt")):
    # Começamos a ficha com o id (o nome do arquivo sem .txt) e campos vazios.
    ficha = {"id": caminho.stem, "data": "", "vitima": "", "cidade": "", "contato": "",
             "produto": "", "valor": "", "chave_pix": "", "whatsapp_vendedor": ""}

    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            # Linha 1: "DEPOIMENTO DEN-001 — registrado em 2025-11-30"
            if linha.startswith("DEPOIMENTO"):
                ficha["data"] = linha.split("registrado em")[-1].strip()

            # "Vítima: Nome (CPF ...), Cidade/MG"
            elif linha.startswith("Vítima:"):
                resto = linha[len("Vítima:"):].strip()
                # partition(" (") divide em 3 partes: antes, o separador, depois.
                nome, _, depois = resto.partition(" (")
                ficha["vitima"] = nome
                ficha["cidade"] = depois.split("),")[-1].strip()     # "Divinópolis/MG"
                # O CPF fica de FORA do resumo de propósito: ele não é necessário aqui.

            # "Contato: 37993916148"
            elif linha.startswith("Contato:"):
                ficha["contato"] = linha.split(":", 1)[1].strip()    # maxsplit=1: corta só no 1º ":"

            # "Comprei um Air Fryer 5L por R$ 149,90 no site ..."
            elif linha.startswith("Comprei um"):
                meio = linha[len("Comprei um"):].split(" no site")[0]  # "Air Fryer 5L por R$ 149,90"
                produto, _, valor = meio.partition(" por ")
                ficha["produto"] = produto.strip()
                ficha["valor"] = valor.strip()

            # "O site só aceitava PIX. A chave era f38b...419."
            elif "A chave era" in linha:
                ficha["chave_pix"] = linha.split("A chave era")[1].strip().rstrip(".")

            # "Falei com o vendedor pelo WhatsApp (31) 98888-0101; ele assinava 'Kau'."
            elif "WhatsApp" in linha:
                ficha["whatsapp_vendedor"] = linha.split("WhatsApp")[1].split(";")[0].strip()

    fichas.append(ficha)

# ── Mostrar ───────────────────────────────────────────────────────────────
for f in fichas:
    print(f"📄 {f['id']} ({f['data']}) · {f['vitima']} · {f['cidade']}")
    print(f"   🛒 {f['produto']} por {f['valor']}")
    print(f"   💳 PIX: {f['chave_pix']}")
    print(f"   📱 vendedor: {f['whatsapp_vendedor']}  ·  contato da vítima: {f['contato']}")

# ── Cruzamentos simples ───────────────────────────────────────────────────
# Um dicionário "chave PIX → lista de depoimentos" mostra quem pagou para a mesma conta.
por_chave = {}
for f in fichas:
    por_chave.setdefault(f["chave_pix"], []).append(f["id"])   # setdefault cria a lista na 1ª vez

whatsapps = {f["whatsapp_vendedor"] for f in fichas}            # set: só valores diferentes
print("\n🔗 Cruzamentos")
for numero in sorted(whatsapps):
    quantos = sum(1 for f in fichas if f["whatsapp_vendedor"] == numero)
    print(f"   WhatsApp do vendedor {numero}: citado em {quantos} de {len(fichas)} depoimentos")
for chave, ids in por_chave.items():
    print(f"   Chave {chave[:8]}… recebeu de: {', '.join(ids)}")

# ── Gravar o resumo ───────────────────────────────────────────────────────
# 1) Texto para gente ler.
with open(SAIDAS / "resumo_depoimentos.txt", "w", encoding="utf-8") as saida:
    saida.write("RESUMO DOS DEPOIMENTOS — Operação Vitrine Fantasma\n")
    saida.write("(CPFs omitidos de propósito: minimização de dados)\n\n")
    for f in fichas:
        saida.write(f"{f['id']} | {f['data']} | {f['vitima']} | {f['cidade']} | {f['produto']} | "
                    f"{f['valor']} | PIX {f['chave_pix']} | vendedor {f['whatsapp_vendedor']}\n")

# 2) TSV (separado por TAB) para colar numa planilha. utf-8-sig ajuda o Excel a ler os acentos.
colunas = list(fichas[0].keys())
with open(SAIDAS / "resumo_depoimentos.tsv", "w", encoding="utf-8-sig") as saida:
    saida.write("\t".join(colunas) + "\n")
    for f in fichas:
        saida.write("\t".join(f[c] for c in colunas) + "\n")

print("\n💾 Gravados: saidas/resumo_depoimentos.txt e saidas/resumo_depoimentos.tsv")
