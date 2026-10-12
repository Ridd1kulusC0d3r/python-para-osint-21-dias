"""
Gerador dos dados SINTÉTICOS da "Operação Vitrine Fantasma".

Tudo o que este script produz é inventado: pessoas, CPFs, telefones, chaves PIX,
domínio e empresa. A semente é fixa, então qualquer pessoa que rodar este script
obtém exatamente os mesmos arquivos (reprodutibilidade = ciência).

Como rodar (a partir da raiz do repositório):
    python caso/gerar_dados.py

Só biblioteca padrão.
"""

import csv          # escrever planilhas .csv
import json         # escrever amostras .json
import random       # sortear dados fictícios
import uuid         # gerar chaves PIX aleatórias (formato UUID)
from pathlib import Path  # montar caminhos de pasta de forma portátil

# Semente fixa: garante que o "acaso" seja sempre o mesmo.
random.seed(2026)

PASTA = Path(__file__).resolve().parent / "dados"
PASTA.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# 1. Funções de apoio
# ----------------------------------------------------------------------------

def digitos_cpf(nove):
    """Recebe 9 dígitos e devolve os 11 com os 2 verificadores calculados."""
    numeros = list(nove)
    for peso_inicial in (10, 11):
        soma = sum(d * p for d, p in zip(numeros, range(peso_inicial, 1, -1)))
        resto = (soma * 10) % 11
        numeros.append(0 if resto == 10 else resto)
    return numeros


def gerar_cpf(valido=True):
    """CPF fictício formatado. Se valido=False, estraga um dígito verificador."""
    nove = [random.randint(0, 9) for _ in range(9)]
    d = digitos_cpf(nove)
    if not valido:
        d[-1] = (d[-1] + random.randint(1, 9)) % 10  # "erro de digitação"
    s = "".join(map(str, d))
    return f"{s[:3]}.{s[3:6]}.{s[6:9]}-{s[9:]}"


def gerar_cnpj(base8, filial="0001", valido=True):
    """CNPJ numérico fictício. Se valido=False, os verificadores ficam errados
    (garantia de que o número NÃO pertence a nenhuma empresa real)."""
    numeros = [int(c) for c in base8 + filial]
    for pesos in ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
                  [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]):
        soma = sum(n * p for n, p in zip(numeros, pesos))
        resto = soma % 11
        numeros.append(0 if resto < 2 else 11 - resto)
    if not valido:
        numeros[-1] = (numeros[-1] + 3) % 10
    s = "".join(map(str, numeros))
    return f"{s[:2]}.{s[2:5]}.{s[5:8]}/{s[8:12]}-{s[12:]}"


def telefone(formato):
    """Telefone fictício de MG em vários formatos (bom para treinar regex)."""
    ddd = random.choice(["31", "31", "31", "34", "32", "38", "35", "37"])
    n = f"9{random.randint(8000, 9999)}{random.randint(1000, 9999)}"
    if formato == 0:
        return f"({ddd}) {n[:5]}-{n[5:]}"
    if formato == 1:
        return f"+55 {ddd} {n[0]} {n[1:5]}-{n[5:]}"
    return f"{ddd}{n}"


# ----------------------------------------------------------------------------
# 2. Elenco fictício do caso
# ----------------------------------------------------------------------------

DOMINIO = "megaoferta-brasil.example"     # .example é reservado (RFC 2606): nunca existirá
CNPJ_RODAPE = gerar_cnpj("48217093", valido=False)  # CNPJ do site falso: dígito verificador ERRADO de propósito
CHAVES_PIX = [str(uuid.UUID(int=random.getrandbits(128))) for _ in range(3)]
CONTAS_LARANJA = [
    {"titular": "Jéssica Prado Lima", "banco": "Banco Digital Fictício S.A.", "chave": CHAVES_PIX[0]},
    {"titular": "Wellington Arruda Paz", "banco": "Pague Já IP (fictício)", "chave": CHAVES_PIX[1]},
    {"titular": "M. R. Brandão Comércio ME", "banco": "Cooperativa Imaginária", "chave": CHAVES_PIX[2]},
]
SUSPEITO = {"nome": "Kauã Teixeira Brandão", "apelido": "kau.ofertas",
            "telefone": "(31) 98888-0101", "email": f"financeiro@{DOMINIO}"}

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Eduarda", "Felipe", "Gabriela", "Henrique",
         "Isabela", "João", "Karina", "Lucas", "Mariana", "Natália", "Otávio", "Paula",
         "Rafael", "Sabrina", "Tiago", "Vanessa", "Wagner", "Yasmin", "Zé Carlos", "Letícia"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Pereira", "Costa", "Rodrigues", "Almeida",
              "Nascimento", "Lima", "Araújo", "Fernandes", "Carvalho", "Gomes", "Martins",
              "Rocha", "Ribeiro", "Barbosa", "Moreira", "Teixeira", "Mendonça"]

# Cidades como as vítimas DIGITARAM (com erros de propósito para os dias 7, 13 e 16)
CIDADES = ["Belo Horizonte", "Belo Horizonte", "BH", "belo horizonte", "Belo Horizone",
           "Contagem", "contagem", "Betim", "Uberlândia", "Uberlandia", "Juiz de Fora",
           "juiz de fora", "Montes Claros", "Ipatinga", "Governador Valadares", "Sete Lagoas",
           "Divinópolis", "Divinopolis", "Uberaba", "Poços de Caldas", "Pocos de Caldas"]

PRODUTOS = [("iPhone 15 128GB", 1999.00), ("Smart TV 55\" 4K", 1299.90),
            ("PlayStation 5", 1899.00), ("Air Fryer 5L", 149.90),
            ("Notebook i7 16GB", 2499.00), ("Galaxy S24", 1799.00)]

RELATOS = ["Paguei no PIX e o site sumiu.", "Recebi código de rastreio falso.",
           "Vendedor parou de responder no WhatsApp.", "Pediram mais um PIX de 'frete'.",
           "O CNPJ do rodapé não existe.", "Vi o anúncio no Instagram patrocinado.",
           "Me mandaram um boleto depois do PIX.", "O site cobrava só à vista no PIX."]

# ----------------------------------------------------------------------------
# 3. denuncias.csv — 37 denúncias (o coração do caso)
# ----------------------------------------------------------------------------

denuncias = []
for i in range(1, 38):
    nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"
    produto, valor = random.choice(PRODUTOS)
    dia = random.choice([3, 7, 12, 18, 21, 24, 27, 28, 29, 30])  # concentração perto da Black Friday
    mes = random.choice([10, 11, 11, 11])
    denuncias.append({
        "id": f"DEN-{i:03d}",
        "data": f"2025-{mes:02d}-{dia:02d}",
        "nome_vitima": nome,
        "cpf": gerar_cpf(valido=random.random() > 0.22),
        "cidade": random.choice(CIDADES),
        "uf": "MG",
        "valor": f"{valor:.2f}",
        "produto": produto,
        "chave_pix_destino": random.choice(CHAVES_PIX),
        "telefone_contato": telefone(random.randint(0, 2)),
        "relato_curto": random.choice(RELATOS),
    })

with open(PASTA / "denuncias.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(denuncias[0]), delimiter=";")
    w.writeheader()
    w.writerows(denuncias)

# ----------------------------------------------------------------------------
# 4. depoimentos/*.txt — 5 depoimentos longos
# ----------------------------------------------------------------------------

dep_pasta = PASTA / "depoimentos"
dep_pasta.mkdir(exist_ok=True)
for d in denuncias[:5]:
    texto = (
        f"DEPOIMENTO {d['id']} — registrado em {d['data']}\n"
        f"Vítima: {d['nome_vitima']} (CPF {d['cpf']}), {d['cidade']}/MG\n"
        f"Contato: {d['telefone_contato']}\n\n"
        f"Comprei um {d['produto']} por R$ {d['valor'].replace('.', ',')} no site {DOMINIO}.\n"
        f"O site só aceitava PIX. A chave era {d['chave_pix_destino']}.\n"
        f"Falei com o vendedor pelo WhatsApp {SUSPEITO['telefone']}; ele assinava 'Kau'.\n"
        f"{d['relato_curto']}\n"
        "Depois de dois dias o site mostrava 'em manutenção' e depois saiu do ar.\n"
    )
    (dep_pasta / f"{d['id']}.txt").write_text(texto, encoding="utf-8")

# ----------------------------------------------------------------------------
# 5. conversa_whatsapp.txt — export de conversa (mina de ouro para regex)
# ----------------------------------------------------------------------------

linhas = [
    f"[28/11/2025 21:14] Kau Ofertas: Boa noite! O iPhone sai por 1.999 no PIX 🔥",
    f"[28/11/2025 21:15] Cliente: Qual o CNPJ da loja?",
    f"[28/11/2025 21:15] Kau Ofertas: CNPJ {CNPJ_RODAPE}, pode confiar",
    f"[28/11/2025 21:16] Kau Ofertas: Chave PIX: {CHAVES_PIX[0]}",
    f"[28/11/2025 21:20] Cliente: Paguei. Meu CPF é {gerar_cpf()} pra nota",
    f"[28/11/2025 21:21] Kau Ofertas: Recebido! Qualquer coisa {SUSPEITO['email']}",
    f"[29/11/2025 09:02] Kau Ofertas: Falta o PIX do frete, R$ 89,90 na chave {CHAVES_PIX[1]}",
    f"[29/11/2025 09:05] Cliente: Me liga no {telefone(0)}",
    f"[29/11/2025 09:06] Kau Ofertas: Liga no meu outro número +55 31 9 8888-0101",
    f"[29/11/2025 09:30] Kau Ofertas: Envio pra CEP 30130-010? Confirma o endereço",
    f"[29/11/2025 10:11] Kau Ofertas: Se preferir manda e-mail pra kau.ofertas@example.com",
    f"[30/11/2025 18:44] Kau Ofertas: Estamos com problema no site, usa a chave do sócio {CHAVES_PIX[2]}",
    f"[30/11/2025 18:45] Kau Ofertas: CNPJ do sócio: {gerar_cnpj('31560427', valido=False)}",
    f"[01/12/2025 08:00] Cliente: O site saiu do ar?? Quero meu dinheiro!",
]
(PASTA / "conversa_whatsapp.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

# ----------------------------------------------------------------------------
# 6. vitrine_megaoferta.html — a "evidência": cópia salva do site falso
# ----------------------------------------------------------------------------

def brl(valor):
    """1999.0 -> '1.999,00' (formato de moeda brasileiro)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


itens_html = "\n".join(
    f'      <div class="produto"><h2>{p}</h2><span class="preco">R$ {brl(v)}</span>'
    f'<span class="selo">Só no PIX</span></div>'
    for p, v in PRODUTOS
)
html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>MegaOferta Brasil — As melhores ofertas do Brasil!</title>
  <meta name="description" content="Loja oficial MegaOferta Brasil. Entrega para todo o Brasil.">
  <meta name="generator" content="LojaPronta 3.2">
  <!-- TODO: trocar a chave pix antes da black friday -->
  <!-- contato dev: kau.ofertas@example.com -->
</head>
<body>
  <header><h1>MegaOferta Brasil</h1><p>Black Friday o ano todo!</p></header>
  <main>
{itens_html}
  </main>
  <section id="pagamento">
    <p>Pagamento exclusivo via PIX. Chave: <strong class="pix">{CHAVES_PIX[0]}</strong></p>
    <p>Atendimento WhatsApp: <a href="https://wa.me/5531988880101">(31) 98888-0101</a></p>
  </section>
  <footer>
    <p>MegaOferta Brasil Comércio Eletrônico LTDA — CNPJ {CNPJ_RODAPE}</p>
    <p>Av. Afonso Pena, 1500 — Centro — Belo Horizonte/MG — CEP 30130-010</p>
    <p><a href="https://instagram.example/megaoferta.br">Instagram</a> ·
       <a href="https://t.me.example/kauofertas">Telegram</a> ·
       <a href="mailto:{SUSPEITO['email']}">E-mail</a></p>
  </footer>
</body>
</html>
"""
(PASTA / "vitrine_megaoferta.html").write_text(html, encoding="utf-8")

# ----------------------------------------------------------------------------
# 7. painel_dump.sql — "dump" do painel administrativo da loja (Dia 8)
# ----------------------------------------------------------------------------

sql = ["-- Dump fictício do painel da loja MegaOferta (Operação Vitrine Fantasma)",
       "CREATE TABLE contas_recebimento (id INTEGER PRIMARY KEY, titular TEXT, banco TEXT, chave_pix TEXT);",
       "CREATE TABLE pedidos (id INTEGER PRIMARY KEY, data TEXT, cliente TEXT, cidade TEXT, produto TEXT, valor REAL, conta_id INTEGER);"]
for i, c in enumerate(CONTAS_LARANJA, 1):
    sql.append(f"INSERT INTO contas_recebimento VALUES ({i}, '{c['titular']}', '{c['banco']}', '{c['chave']}');")
for i, d in enumerate(denuncias, 1):
    conta = CHAVES_PIX.index(d["chave_pix_destino"]) + 1
    nome = d["nome_vitima"].replace("'", "''")
    sql.append(f"INSERT INTO pedidos VALUES ({i}, '{d['data']}', '{nome}', '{d['cidade']}', "
               f"'{d['produto'].replace(chr(34), '')}', {d['valor']}, {conta});")
(PASTA / "painel_dump.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")

# ----------------------------------------------------------------------------
# 8. Amostras de domínio (Dia 15) e Wayback (Dia 19)
# ----------------------------------------------------------------------------

rdap = {
    "objectClassName": "domain",
    "ldhName": DOMINIO,
    "status": ["active"],
    "events": [
        {"eventAction": "registration", "eventDate": "2025-10-02T14:31:08Z"},
        {"eventAction": "last changed", "eventDate": "2025-11-20T03:12:44Z"},
        {"eventAction": "expiration", "eventDate": "2026-10-02T14:31:08Z"},
    ],
    "nameservers": [{"ldhName": "ns1.hospedagem-barata.example"},
                    {"ldhName": "ns2.hospedagem-barata.example"}],
    "entities": [{"roles": ["registrant"], "handle": "KTB123",
                  "vcardArray": ["vcard", [["version", {}, "text", "4.0"],
                                           ["fn", {}, "text", "Kaua T Brandao"]]]}],
    "_aviso": "AMOSTRA FICTÍCIA para estudo — não é resposta real de nenhum servidor RDAP",
}
(PASTA / "rdap_megaoferta.json").write_text(json.dumps(rdap, indent=2, ensure_ascii=False), encoding="utf-8")

whois = f"""% AMOSTRA FICTÍCIA — formato inspirado no WHOIS do registro.br
domain:      {DOMINIO}
owner:       Kaua T Brandao
owner-c:     KTB123
nserver:     ns1.hospedagem-barata.example
nserver:     ns2.hospedagem-barata.example
created:     20251002 #12345678
changed:     20251120
expires:     20261002
status:      published
"""
(PASTA / "whois_megaoferta.txt").write_text(whois, encoding="utf-8")

cdx = [["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"],
       ["example,megaoferta-brasil)/", "20251004101500", f"https://{DOMINIO}/", "text/html", "200", "AAA111", "5120"],
       ["example,megaoferta-brasil)/", "20251103220012", f"https://{DOMINIO}/", "text/html", "200", "BBB222", "6301"],
       ["example,megaoferta-brasil)/", "20251128233001", f"https://{DOMINIO}/", "text/html", "200", "CCC333", "6420"],
       ["example,megaoferta-brasil)/", "20251201080515", f"https://{DOMINIO}/", "text/html", "200", "DDD444", "880"],
       ["example,megaoferta-brasil)/", "20251205120000", f"https://{DOMINIO}/", "text/html", "404", "EEE555", "312"]]
(PASTA / "wayback_cdx_megaoferta.json").write_text(json.dumps(cdx, indent=1), encoding="utf-8")

# ----------------------------------------------------------------------------
# 9. ficha.json — gabarito do caso (para quem cria exercícios)
# ----------------------------------------------------------------------------

ficha = {"dominio": DOMINIO, "cnpj_rodape": CNPJ_RODAPE, "chaves_pix": CHAVES_PIX,
         "contas_laranja": CONTAS_LARANJA, "suspeito": SUSPEITO,
         "total_denuncias": len(denuncias),
         "aviso": "Todos os dados são fictícios e gerados por caso/gerar_dados.py (semente 2026)."}
(PASTA / "ficha_do_caso.json").write_text(json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✅ Dados sintéticos gerados em {PASTA}")
