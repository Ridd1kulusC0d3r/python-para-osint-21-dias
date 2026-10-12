# Dia 3 — Ferramentas de linha de comando

> 🃏 Cartas **3 · 24 · 45**  ·  📘 Original: *Day 3. Install and run Python command line tools*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-03-ferramentas-de-linha-de-comando/notebook.ipynb)

## 📖 Capítulo 3 — Ferramenta de campo

<!-- historia:inicio -->
Quinta-feira, 10h20. Em cinco depoimentos diferentes aparece a mesma assinatura no WhatsApp:
*"Kau"*. E num print de Instagram que uma vítima mandou, um apelido: **`kau.ofertas`**.

— Apelido é ouro — diz a Iara. — Gente que aplica golpe troca de chip, de chave PIX, de site. Mas o
apelido, por preguiça ou por vaidade, costuma ficar.

Ela abre o terminal dela e digita um comando comprido. Uma lista de sites começa a rolar na tela.

— Isso é o blackbird. Alguém já escreveu uma ferramenta que pergunta a centenas de sites se um
nome de usuário existe. A gente não precisa reinventar a roda. Mas precisa **saber rodar a roda**:
instalar, passar as opções certas, chamar de dentro de um script e, principalmente, **registrar o que
foi feito**. Se um dia isso virar prova, alguém vai perguntar: *que comando você rodou, quando e o que
saiu?*

Você anota a pergunta num post-it e cola no monitor.

— E outra coisa — ela completa, baixando a tela. — O apelido do caso pode ser de um inocente em algum
site. Primeiro a gente aprende com um alvo de treino. Depois, com autorização, no alvo de verdade.
<!-- historia:fim -->

## 🎯 Objetivos

- Instalar uma ferramenta de OSINT pelo **PyPI** (`pip install`) e pelo **GitHub** (`git clone` +
  `requirements.txt`).
- Rodar o **blackbird** pelo terminal e de dentro de um script com `subprocess`.
- Criar a sua própria ferramenta com opções (`--cep`, `--formato`) usando `argparse`.
- Rodar programas com `subprocess.run`, capturar a saída e **registrar** cada execução.
- Entender como uma ferramenta decide se um username "existe" num site.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Uma **ferramenta de linha de comando** (CLI) é um programa que você usa digitando, em vez de clicar.
Tudo o que vem depois do nome do programa são **argumentos**:

```
python blackbird.py   --username   ivanov
└──────┬──────────┘   └───┬─────┘  └──┬──┘
    programa            opção        valor
```

Há três jeitos de colocar uma ferramenta Python para rodar:

| Jeito | Comando | Quando |
|---|---|---|
| **PyPI** | `pip install nome` e depois `nome alvo` | o autor publicou no PyPI |
| **GitHub** | `git clone ...`, `pip install -r requirements.txt`, `python ferramenta.py` | só existe o repositório |
| **Do seu script** | `subprocess.run([...])` | para automatizar e registrar |

`requirements.txt` é a lista de bibliotecas que a ferramenta precisa. E o **código de retorno**
(`returncode`) é como um programa avisa se deu certo: `0` é sucesso; qualquer outro número é erro.

**Como essas ferramentas "acham" um perfil?** Elas montam a URL do perfil (`https://site/{usuario}`) e
olham a resposta: status **200** costuma ser "existe", **404** "não existe". Mas muitos sites mentem
(respondem 200 para tudo), então as boas ferramentas também procuram um **texto** na página. O projeto
comunitário **WhatsMyName** guarda essas regras para mais de 700 sites, e o blackbird usa essa base.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/launch.py`](original/launch.py) | Roda `python blackbird.py -u ivanov` de dentro do Python com `subprocess.call` |

### Instalar e rodar o blackbird (checado em outubro de 2026)

O repositório continua em <https://github.com/p1ngul1n0/blackbird>. A opção `-u` / `--username` do
curso original **continua igual**, então não foi preciso criar uma versão 2026 do `launch.py`.

```bash
cd dia-03-ferramentas-de-linha-de-comando
git clone https://github.com/p1ngul1n0/blackbird
cd blackbird
pip install -r requirements.txt
python blackbird.py --username cipher387          # o mesmo que -u
python blackbird.py --username cipher387 --csv    # também exporta CSV (há --pdf e --json)
```

Para usar o `launch.py` como o autor ensina: **copie** o arquivo para dentro da pasta `blackbird/` e rode
de lá (no macOS/Linux, se `python` não existir, edite o texto do comando para `python3`):

```bash
cp ../original/launch.py .
python launch.py
```

No **Colab**, as mesmas linhas funcionam numa célula com `!` na frente
(`!git clone ...`, `%cd blackbird`, `!pip install -r requirements.txt`, `!python blackbird.py -u cipher387`).
Atenção: a pasta `blackbird/` **não** está no `.gitignore`. Se você estiver num fork, não faça commit dela.

> ℹ️ **O que mudou desde o PDF.** O blackbird hoje usa a base **WhatsMyName**, exporta CSV/PDF/JSON e
> tem um recurso opcional de IA (`--ai`) que manda para um serviço externo a lista de sites onde o
> username foi achado. Num caso real, pense duas vezes antes de usar: é dado do caso saindo da sua
> máquina. O **Thorndyke**, a outra ferramenta citada no PDF, foi **arquivado** pelo autor em 2022 e não
> aparece mais no PyPI; pule essa parte. O próprio cipher387 lembra que **Sherlock** e **Maigret**
> cobrem mais sites (`pip install sherlock-project`, `pip install maigret`).

## 🇧🇷 Nível 2 — Camada Brasil

| Arquivo | O que faz |
|---|---|
| [`br/01_cli_cep.py`](br/01_cli_cep.py) | Sua primeira CLI: `--cep` e `--formato texto/json/csv`, com `--help` automático |
| [`br/02_rodar_e_registrar.py`](br/02_rodar_e_registrar.py) | Roda o `01` com `subprocess.run` e grava um log forense em `saidas/log_execucoes.jsonl` |
| [`br/03_mini_blackbird.py`](br/03_mini_blackbird.py) | **O caso:** um blackbird de bolso que verifica um username no GitHub, GitLab e Codeberg |

```bash
cd dia-03-ferramentas-de-linha-de-comando
python br/01_cli_cep.py --cep 30130-010
python br/01_cli_cep.py --cep 30130010 --formato json
python br/01_cli_cep.py --help
python br/02_rodar_e_registrar.py
python br/03_mini_blackbird.py --username cipher387
OSINT_OFFLINE=1 python br/03_mini_blackbird.py       # usa a amostra de dados/
```

**O que você deve ver:** o `01` mostra o endereço do CEP 30130-010, no Centro de BH (o mesmo CEP que
aparece no rodapé da loja; no Dia 5 você investiga esse endereço a fundo). O `02` roda três CEPs (um
deles inválido de propósito, para você ver o código de retorno `2`) e o log ganha três linhas a cada
execução, cada uma com data/hora, comando e o SHA-256 da saída. O `03` acha o `cipher387` no GitHub.

> 💡 Repare que o `01` manda os avisos para o **stderr** e o resultado para o **stdout**. É por isso que o
> `02` consegue guardar o JSON limpo, separado do aviso `⚠️ MODO OFFLINE`.

## ⚖️ Ética, LGPD e OPSEC

- **Ferramenta de enumeração bate na porta de centenas de sites com o seu IP.** Cada site registra o
  acesso. No trabalho, use a infraestrutura autorizada; no estudo, use alvos de treino públicos
  (como `cipher387`, o autor do curso).
- **Apelido de suspeito pode ser de um inocente.** "kau.ofertas" é fictício, mas pode existir como conta
  real de outra pessoa. Por isso o desafio só **simula** a busca dele. Consultar alguém sem finalidade
  definida é tratamento de dado pessoal sem base legal (LGPD, art. 7º).
- **Achar o mesmo username não prova identidade.** Trate como hipótese e procure elementos que
  confirmem (foto, bio, links cruzados, datas).
- **Registre o que você rodou.** Comando, versão da ferramenta, data/hora com fuso e o hash da saída. Isso
  é o começo de uma cadeia de custódia (você aprofunda no Dia 14).
- **Leia o código antes de rodar.** `git clone` + `pip install -r requirements.txt` executa código de
  terceiros na sua máquina. Prefira repositórios conhecidos e um ambiente separado (Colab, Codespaces,
  `venv` ou máquina virtual).
- **Recursos de IA embutidos enviam dados para fora.** Antes de usar `--ai` ou similares, confira o que
  é enviado e se isso é permitido no seu caso.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Lote de buscas com registro**: gerar variantes de `kau.ofertas`, simular
as buscas, executar de verdade só no alvo de treino e gravar CSV + log.

## 🔎 Inovação OSINT do dia

**WhatsMyName: as regras de detecção como dados abertos.** O projeto comunitário
[WhatsMyName](https://github.com/WebBreacher/WhatsMyName) mantém um único arquivo, `wmn-data.json`, com
as regras de mais de 700 sites: a URL a consultar (`uri_check`), o status e o texto que indicam
"existe" (`e_code`, `e_string`) e os que indicam "não existe" (`m_code`, `m_string`). O blackbird usa
essa base, e o `br/03_mini_blackbird.py` copia a mesma ideia para três sites. Como é só JSON, dá para
ler com `urllib.request` + `json` (nativos) e montar o seu verificador. Licença CC BY-SA 4.0: cite a
fonte se reaproveitar.

## 📚 Para ir além

- Blackbird: <https://github.com/p1ngul1n0/blackbird> (documentação: <https://p1ngul1n0.gitbook.io/blackbird/>)
- WhatsMyName: <https://github.com/WebBreacher/WhatsMyName>
- Sherlock: <https://github.com/sherlock-project/sherlock> · Maigret: <https://github.com/soxoj/maigret>
- `argparse`, tutorial oficial: <https://docs.python.org/pt-br/3/howto/argparse.html>
- `subprocess`: <https://docs.python.org/pt-br/3/library/subprocess.html>

## ✅ Checklist

- [ ] Clonei o blackbird, instalei os requisitos e rodei `--username cipher387`
- [ ] Rodei o `launch.py` de dentro da pasta `blackbird/`
- [ ] Usei o `--help` da minha própria CLI de CEP
- [ ] Rodei o `02` duas vezes e vi o log crescer
- [ ] Entendi por que o GitLab precisa de checagem de texto
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
