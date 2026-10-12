# Dia 0 — Preparação do ambiente

> 🃏 Sem cartas (dia de preparação)  ·  📘 Original: *Day 0. Preparing for work*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-00-preparacao/notebook.ipynb)

## 📖 Capítulo 0 — O recrutamento

<!-- historia:inicio -->
Segunda-feira, 8h. O crachá ainda está quente da impressora quando você atravessa o corredor do
**Núcleo de Fontes Abertas**, no centro de Belo Horizonte. Numa mesa cheia de post-its, uma mulher de
óculos levanta os olhos do monitor.

— Você é a pessoa nova? Iara. Iara Campos. Senta aí.

Ela empurra um notebook na sua direção.

— Aqui a gente não espera a ferramenta perfeita aparecer. Ferramenta pronta todo mundo tem. Quem sabe
escrever a própria enxerga o que os outros não veem. Você já programou?

Você balança a cabeça. Ela sorri, como quem já ouviu essa resposta muitas vezes.

— Ótimo. Então ninguém te ensinou vício. Hoje é só montar a bancada: um Python funcionando, o caderno
do curso baixado e um teste para ver se as fontes que a gente usa respondem daqui. Amanhã chega o
primeiro caso.

Ela aponta para um quadro branco onde alguém escreveu, em letras grandes: **MegaOferta Brasil — 37
denúncias**.

— Esse aí vai ser o seu professor nos próximos 21 dias.
<!-- historia:fim -->

## 🎯 Objetivos

- Escolher **onde** você vai estudar: Google Colab, GitHub Codespaces ou o seu computador.
- Baixar (clonar) este repositório e entender como ele está organizado.
- Rodar o seu **primeiro script** e saber ler o resultado.
- Entender o que é o **modo offline** (`OSINT_OFFLINE=1`) e por que todo exercício tem um.
- Conferir versão do Python, codificação de texto e fuso horário.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Para programar você precisa de duas coisas: o **interpretador Python** (o programa que lê o seu
arquivo `.py` e executa linha por linha) e um lugar para **escrever e rodar** o código. Existem três
caminhos, e todos servem para o curso inteiro:

| Caminho | Instala algo? | Como é | Bom para |
|---|---|---|---|
| **Google Colab** | Não | Notebook no navegador, com células de texto e de código | Começar já, até no celular |
| **GitHub Codespaces** | Não | Um VS Code com terminal Linux no navegador | Quem quer o "terminal de verdade" do curso original |
| **Local** | Python 3.9+ e Git | O seu editor e o seu terminal | Estudar sem internet e montar um laboratório próprio |

**Git** é o programa que copia ("clona") repositórios do GitHub e guarda o histórico de mudanças.
**pip** é o instalador de bibliotecas extras; aqui ele só é usado no nível 1 (exercícios originais).
A camada Brasil usa só a **biblioteca padrão**, que já vem com o Python.

Um detalhe que pega muita gente: **codificação**. É a regra que transforma letras em bytes. Se um
arquivo foi gravado em UTF-8 e lido como cp1252 (padrão antigo do Windows), `Divinópolis` vira
`DivinÃ³polis`. Por isso todo script do curso diz `encoding="utf-8"` ao abrir arquivos.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

O Dia 0 do curso original **não tem código**: é só preparação. Leia o resumo em
[`original/LEIA-ME.md`](original/LEIA-ME.md).

O autor usava o **Gitpod** nos exemplos. Esse serviço deixou de ser uma opção gratuita para o curso, e
o próprio cipher387 avisa no README do repositório dele que dá para seguir tudo pelo **GitHub
Codespaces**. É o que este repositório também recomenda como caminho com terminal no navegador.

## 🇧🇷 Nível 2 — Camada Brasil

### Caminho A — Google Colab (recomendado para começar)

1. Clique no botão **Abrir no Colab** lá em cima (ou no README de qualquer dia).
2. Entre com uma conta Google.
3. Rode a primeira célula (**⚙️ Preparar o ambiente**): ela baixa o repositório e entra na pasta do dia.
4. Rode as demais células na ordem, clicando no ▶️. Os campos de formulário à direita podem ser
   editados sem mexer no código.
5. Para guardar suas mudanças: **Arquivo → Salvar uma cópia no Drive**.

### Caminho B — GitHub Codespaces

1. Crie uma conta gratuita no GitHub e abra
   <https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias>.
2. Clique em **Code → Codespaces → Create codespace on main**.
3. Quando o editor abrir, use o terminal na parte de baixo:

```bash
cd dia-00-preparacao
python br/01_verifica_ambiente.py
```

A conta gratuita do GitHub inclui uma cota mensal de Codespaces (hoje, 120 horas de núcleo e 15 GB
de armazenamento; uma máquina de 2 núcleos gasta 2 horas da cota por hora de uso). **Desligue o
codespace quando terminar** e apague os que não usa mais.

### Caminho C — No seu computador

<details>
<summary><b>🪟 Windows</b></summary>

1. Baixe o Python em <https://www.python.org/downloads/>. Na primeira tela do instalador, marque
   **"Add python.exe to PATH"**.
2. Baixe o Git em <https://git-scm.com/download/win> e instale com as opções padrão.
3. Abra o **PowerShell** e rode:

```powershell
py --version
git --version
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias\dia-00-preparacao
py br\01_verifica_ambiente.py
```

- Se os acentos aparecerem estranhos no terminal, rode antes: `$env:PYTHONUTF8=1`
- Modo offline no PowerShell: `$env:OSINT_OFFLINE=1; py br\01_verifica_ambiente.py`
- Para voltar ao modo normal: `Remove-Item Env:OSINT_OFFLINE`
- Se o verificador avisar que falta o banco de fusos: `py -m pip install tzdata`

</details>

<details>
<summary><b>🍎 macOS</b></summary>

1. Abra o **Terminal** e rode `python3 --version`. Se o macOS oferecer instalar as "ferramentas de
   linha de comando", aceite: isso instala o Git também.
2. Se a versão for menor que 3.9, instale a mais nova em <https://www.python.org/downloads/>.

```bash
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias/dia-00-preparacao
python3 br/01_verifica_ambiente.py
OSINT_OFFLINE=1 python3 br/01_verifica_ambiente.py
```

No macOS e no Linux o comando costuma ser `python3` (e não `python`). Onde o curso disser `python`,
use `python3`.

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
sudo apt install -y python3 git          # Debian/Ubuntu
# sudo dnf install -y python3 git        # Fedora
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias/dia-00-preparacao
python3 br/01_verifica_ambiente.py
OSINT_OFFLINE=1 python3 br/01_verifica_ambiente.py
```

Para os exercícios originais (nível 1), crie um ambiente virtual antes de usar o pip:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-original.txt
```

</details>

### Os scripts do dia

| Arquivo | O que faz |
|---|---|
| [`br/01_verifica_ambiente.py`](br/01_verifica_ambiente.py) | Confere Python ≥ 3.9, codificação, fuso de Brasília e se as APIs do curso respondem (tabela ✅/❌) |
| [`br/02_primeiro_contato.py`](br/02_primeiro_contato.py) | Mostra o "mapa" do repositório: o que tem na raiz e em cada dia |

### Como rodar um script

Sempre **de dentro da pasta do dia**, apontando para o arquivo:

```bash
cd dia-00-preparacao
python br/01_verifica_ambiente.py            # normal (usa a internet)
OSINT_OFFLINE=1 python br/01_verifica_ambiente.py   # sem internet
python br/02_primeiro_contato.py
```

**Modo offline.** Todo exercício que consulta a internet tem uma **amostra** em `dados/` com o mesmo
formato da resposta real. Se a internet cair, a API mudar ou você definir `OSINT_OFFLINE=1`, o script
avisa com `⚠️ MODO OFFLINE` e usa a amostra. Você nunca fica travado.

**O que você deve ver:** no verificador, a versão do Python com ✅, a codificação (no Windows talvez
apareça `cp1252` com um aviso, é normal), a hora de Brasília e a tabela das APIs.

## ⚖️ Ética, LGPD e OPSEC

- **Separe o laboratório da vida pessoal.** Use uma conta Google/GitHub só para estudo, sem dados de
  trabalho. Notebooks do Colab ficam no seu Drive; codespaces ficam na sua conta do GitHub.
- **Nunca coloque dados reais de investigação** num notebook ou codespace público ou compartilhado.
  Neste curso, o único "caso" é fictício (`caso/dados/`).
- **Fork público é público.** Se você fizer um fork para anotar, tudo o que você commitar fica visível
  para qualquer pessoa. Nada de tokens, senhas ou chaves de API no código.
- **Seu IP aparece para cada API consultada.** No computador do trabalho, pode passar pelo proxy da
  empresa; confira as regras antes. O verificador mostra exatamente quais serviços o curso contata.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Meu verificador de ambiente**: personalize o verificador, confira `git` e
`pip` e grave um relatório em `saidas/`. É um desafio de boas-vindas: não conta como carta.

## 🔎 Inovação OSINT do dia

**Python 3.15 e o fim da armadilha dos acentos.** O Python 3.15.0 saiu em 09/10/2026 e, pela
[PEP 686](https://peps.python.org/pep-0686/), passa a usar **UTF-8 por padrão** ao abrir arquivos,
inclusive no Windows. Para quem coleta dados brasileiros, isso acaba com boa parte do
`DivinÃ³polis`. Mas atenção: este curso roda do 3.9 em diante e muita gente ainda vai usar versões
antigas por anos. Por isso os scripts continuam dizendo `encoding="utf-8"` explicitamente. O
verificador do dia mostra qual é o padrão na sua máquina (`locale.getpreferredencoding`) e se o modo
UTF-8 está ativo (`sys.flags.utf8_mode`). Biblioteca simples: `locale` e `sys`, nativos.

## 📚 Para ir além

- Guia de instalação do Python (oficial): <https://wiki.python.org/moin/BeginnersGuide/Download>
- Instalar o Git: <https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git>
- Cota gratuita do Codespaces: <https://docs.github.com/en/billing/concepts/product-billing/github-codespaces>
- Bem-vindo ao Colab: <https://colab.research.google.com/>
- PEP 686 (UTF-8 por padrão): <https://peps.python.org/pep-0686/>
- O passo a passo completo também está em [`COMECE-AQUI.md`](../COMECE-AQUI.md).

## ✅ Checklist

- [ ] Escolhi meu caminho (Colab, Codespaces ou local)
- [ ] Clonei o repositório (ou abri o notebook do Dia 0)
- [ ] Rodei `br/01_verifica_ambiente.py` e vi o Python com ✅
- [ ] Rodei o mesmo script com `OSINT_OFFLINE=1` e vi o aviso `⚠️ MODO OFFLINE`
- [ ] Rodei `br/02_primeiro_contato.py` e entendi a estrutura de um dia
- [ ] Fiz o desafio de boas-vindas
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
