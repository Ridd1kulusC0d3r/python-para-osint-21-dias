"""
Verificador de ambiente: o seu Python está pronto para os 21 dias?

Sem carta (Dia 0 é preparação) — mas é o primeiro script que você roda.

O que você aprende:
  • a descobrir a versão do Python que está rodando o script (precisa ser 3.9 ou mais nova);
  • a conferir a codificação padrão (UTF-8 evita acentos estragados) e o fuso horário;
  • a testar, um por um, se os sites e APIs usados no curso respondem no seu computador;
  • a ler uma tabela de resultado com ✅ / ❌.

Como rodar (dentro da pasta dia-00-preparacao):
    python br/01_verifica_ambiente.py
    OSINT_OFFLINE=1 python br/01_verifica_ambiente.py   # pula os testes de internet
"""

import locale               # descobrir a codificação "preferida" do sistema
import os                   # ler a variável de ambiente OSINT_OFFLINE
import platform             # nome do sistema operacional (Windows, Linux, macOS)
import sys                  # versão do Python e codificação do terminal
import time                 # medir quanto tempo cada site demora a responder
import urllib.error         # os tipos de erro que o urllib pode levantar
import urllib.request       # fazer requisições HTTP sem instalar nada
from datetime import datetime, timedelta, timezone

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
TESTAR_INTERNET = True  #@param {type:"boolean"}
TEMPO_LIMITE = 10  #@param {type:"integer"}

OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# ── As APIs e sites que o curso usa (todos públicos e institucionais) ─────
# Cada item: (nome amigável, dia em que aparece, URL de teste).
SERVICOS = [
    ("GitHub API", 5, "https://api.github.com/users/cipher387"),
    ("BrasilAPI (CEP)", 5, "https://brasilapi.com.br/api/cep/v2/30130010"),
    ("ViaCEP", 5, "https://viacep.com.br/ws/30130010/json/"),
    ("BrasilAPI (CNPJ)", 6, "https://brasilapi.com.br/api/cnpj/v1/00000000000191"),
    ("IBGE Localidades", 7, "https://servicodados.ibge.gov.br/api/v1/localidades/estados/MG"),
    ("Querido Diário", 9, "https://api.queridodiario.ok.org.br/gazettes?size=1"),
    ("ipify (meu IP)", 12, "https://api.ipify.org?format=json"),
    ("RDAP registro.br", 15, "https://rdap.registro.br/domain/registro.br"),
    ("Bootstrap IANA", 15, "https://data.iana.org/rdap/dns.json"),
    ("Wayback CDX", 19, "https://web.archive.org/cdx/search/cdx?url=gov.br&limit=1&output=json"),
]


def testar(url):
    """Faz um pedido simples e devolve (deu_certo, detalhe, milissegundos)."""
    inicio = time.time()
    try:
        # Nos identificamos com um User-Agent honesto: alguns servidores recusam pedidos "anônimos".
        pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
        with urllib.request.urlopen(pedido, timeout=TEMPO_LIMITE) as resposta:
            resposta.read(512)                       # lemos só um pedacinho: basta saber que respondeu
            return True, f"HTTP {resposta.status}", int((time.time() - inicio) * 1000)
    except urllib.error.HTTPError as erro:          # o servidor respondeu, mas com erro (404, 429...)
        return False, f"HTTP {erro.code}", int((time.time() - inicio) * 1000)
    except Exception as erro:                       # nem respondeu (sem internet, bloqueio, DNS...)
        return False, type(erro).__name__, int((time.time() - inicio) * 1000)


# ── 1. Versão do Python ───────────────────────────────────────────────────
# sys.version_info é uma tupla: (3, 12, 4, ...). Comparar tuplas compara item a item.
print("🐍 PYTHON")
versao = ".".join(str(n) for n in sys.version_info[:3])
print(f"   Versão:  {versao}  ({sys.executable})")
if sys.version_info >= (3, 9):
    print("   ✅ 3.9 ou mais nova: tudo certo para o curso.")
else:
    print("   ❌ Versão antiga. Instale o Python 3.9+ (veja o README do Dia 0).")
print(f"   Sistema: {platform.system()} {platform.release()}")

# ── 2. Codificação (acentos!) ─────────────────────────────────────────────
# Arquivos com acento só são lidos certo se a codificação for a mesma em que foram gravados.
# No curso, gravamos e lemos SEMPRE com encoding="utf-8". Aqui vemos o padrão do seu sistema.
print("\n🔤 CODIFICAÇÃO")
preferida = locale.getpreferredencoding(False)        # o que open() usa se você não disser nada
print(f"   Padrão do open():  {preferida}")
print(f"   Terminal (stdout): {sys.stdout.encoding}")
print(f"   Modo UTF-8 ativo:  {'sim' if sys.flags.utf8_mode else 'não'}")
if preferida.lower().replace("-", "") in ("utf8",):
    print("   ✅ Padrão UTF-8.")
else:
    print("   ⚠️  O padrão NÃO é UTF-8 (comum no Windows: cp1252). Os scripts do curso já passam")
    print('      encoding="utf-8", mas nos seus scripts lembre-se de fazer o mesmo.')

# ── 3. Fuso horário ───────────────────────────────────────────────────────
# zoneinfo vem no Python 3.9+, mas no Windows pode faltar o banco de fusos (pacote tzdata).
# Por isso tentamos e, se falhar, usamos UTC-3 fixo (o Brasil não tem horário de verão desde 2019).
print("\n🕒 FUSO HORÁRIO")
try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
    print("   ✅ zoneinfo encontrou America/Sao_Paulo.")
except Exception:
    FUSO = timezone(timedelta(hours=-3))
    print("   ⚠️  Sem banco de fusos (no Windows: pip install tzdata). Usando UTC-3 fixo.")
agora = datetime.now(FUSO)
print(f"   Agora em Brasília: {agora:%d/%m/%Y %H:%M:%S}")
print(f"   Hora local do PC:  {datetime.now().astimezone():%d/%m/%Y %H:%M:%S %Z}")

# ── 4. Internet: as APIs do curso respondem? ──────────────────────────────
print("\n🌐 APIs DO CURSO")
if OFFLINE or not TESTAR_INTERNET:
    print("⚠️ MODO OFFLINE: testes de internet pulados. Os exercícios vão usar as amostras de dados/.")
    resultados = [(nome, dia, "⏭️", "não testado", 0) for nome, dia, _ in SERVICOS]
else:
    resultados = []
    for nome, dia, url in SERVICOS:
        ok, detalhe, ms = testar(url)
        resultados.append((nome, dia, "✅" if ok else "❌", detalhe, ms))
        time.sleep(0.5)                              # meio segundo entre pedidos: educação com os servidores

# Tabela alinhada: :<20 = alinhar à esquerda em 20 colunas; :>3 = à direita em 3.
print(f"   {'Serviço':<20} {'Dia':>3}  OK  {'Detalhe':<14} {'Tempo':>7}")
print("   " + "─" * 54)
for nome, dia, icone, detalhe, ms in resultados:
    tempo = f"{ms} ms" if ms else "—"
    print(f"   {nome:<20} {dia:>3}  {icone}  {detalhe:<14} {tempo:>7}")

falhas = [r for r in resultados if r[2] == "❌"]
if falhas:
    print(f"\n   {len(falhas)} serviço(s) não responderam. Sem problema: todo exercício tem amostra offline.")
    print("   Se TODOS falharam, verifique sua conexão, proxy da empresa ou firewall.")

print("\n🎉 Verificação concluída. Pode seguir para o Dia 1!")
