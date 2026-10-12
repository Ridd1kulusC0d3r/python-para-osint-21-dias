# 🚀 Comece aqui

Três caminhos. Escolha **um**.

| Caminho | Precisa instalar? | Bom para |
|---|---|---|
| **A. Google Colab** | Não | Começar em 1 minuto, inclusive pelo celular ou tablet |
| **B. GitHub Codespaces** | Não | Ter um terminal Linux completo no navegador |
| **C. No seu computador** | Python 3.9+ e Git | Estudar offline e montar seu próprio laboratório |

---

## A. Google Colab (recomendado para começar)

1. Abra o notebook do Dia 0: [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-00-preparacao/notebook.ipynb)
2. Faça login com uma conta Google.
3. Rode a primeira célula (**⚙️ Preparar o ambiente**) clicando no ▶️ à esquerda. Ela baixa o
   repositório e entra na pasta do dia.
4. Rode as células seguintes na ordem. As que têm **formulário** à direita podem ser editadas sem mexer no código.
5. Para salvar o que você mudou: **Arquivo → Salvar uma cópia no Drive**.

> Cada dia tem o seu notebook. O link está no README do dia e na tabela do [README principal](README.md).

## B. GitHub Codespaces

1. Entre no GitHub e abra <https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias>.
2. **Code → Codespaces → Create codespace on main**.
3. Quando o editor abrir, use o terminal na parte de baixo:

```bash
cd dia-01-primeiro-script
python br/01_ola_nfa.py
```

O plano gratuito do GitHub inclui algumas horas de Codespaces por mês. Desligue o codespace quando terminar.

## C. No seu computador

<details>
<summary><b>🪟 Windows</b></summary>

1. Baixe o Python em <https://www.python.org/downloads/>. Na instalação, marque **"Add python.exe to PATH"**.
2. Baixe o Git em <https://git-scm.com/download/win> (pode aceitar as opções padrão).
3. Abra o **PowerShell** e rode:

```powershell
py --version
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias\dia-00-preparacao
py br\01_verifica_ambiente.py
```

Dica: se os acentos aparecerem estranhos no terminal, rode antes `$env:PYTHONUTF8=1`.
Para testar sem internet: `$env:OSINT_OFFLINE=1; py br\01_verifica_ambiente.py`.

</details>

<details>
<summary><b>🍎 macOS</b></summary>

1. Abra o **Terminal** e rode `python3 --version`. Se o macOS pedir para instalar as ferramentas de
   linha de comando, aceite (isso instala o Git também).
2. Se a versão for menor que 3.9, instale a mais nova em <https://www.python.org/downloads/>.

```bash
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias/dia-00-preparacao
python3 br/01_verifica_ambiente.py
```

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
sudo apt install -y python3 git          # Debian/Ubuntu (Fedora: sudo dnf install python3 git)
git clone https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias.git
cd python-para-osint-21-dias/dia-00-preparacao
python3 br/01_verifica_ambiente.py
```

</details>

### Exercícios originais (nível 1)

Os exercícios do cipher387 usam bibliotecas de terceiros. Instale todas de uma vez, de preferência num
ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-original.txt
```

A camada Brasil (nível 2) **não precisa de nada disso**: só do Python.

## Rotina de cada dia

1. Leia o **capítulo da história** no README do dia (2 minutos).
2. Rode o **exercício original** (nível 1) e mude alguma coisa nele.
3. Rode os **exercícios BR** (nível 2) na ordem `01_`, `02_`…
4. Tente o **desafio S** (nível 3) antes de abrir o gabarito.
5. Responda o **quiz** do notebook.
6. Anote no seu [`DIARIO.md`](DIARIO.md) e, se quiser, registre a entrega numa issue
   [🥋 Entreguei o dia](https://github.com/Ridd1kulusC0d3r/python-para-osint-21-dias/issues/new?template=entreguei-o-dia.yml).

## Sem internet?

Todo exercício BR tem uma **amostra offline**. Defina a variável `OSINT_OFFLINE=1` e o script usa os
arquivos da pasta `dados/` em vez de consultar a internet. Quando isso acontece, aparece a mensagem
`⚠️ MODO OFFLINE`.

| Onde | Como |
|---|---|
| Linux/macOS | `OSINT_OFFLINE=1 python3 br/arquivo.py` |
| Windows (PowerShell) | `$env:OSINT_OFFLINE=1; py br\arquivo.py` |
| Colab | `import os; os.environ["OSINT_OFFLINE"] = "1"` numa célula antes |

## Problemas comuns

| Sintoma | Solução |
|---|---|
| `python: command not found` | No macOS/Linux use `python3`; no Windows, `py` |
| `ModuleNotFoundError` num exercício **original** | Faltou `pip install -r requirements-original.txt` |
| `FileNotFoundError` | Você está na pasta errada. Entre na pasta do dia antes de rodar (`cd dia-XX-...`) |
| Acentos viram `Ã©` | Arquivo lido sem `encoding="utf-8"`, ou terminal do Windows antigo (`$env:PYTHONUTF8=1`) |
| `HTTP Error 429` | Muitas consultas seguidas. Espere um pouco; respeite o limite da API |
| `⚠️ MODO OFFLINE` sem você pedir | A API não respondeu. O script seguiu com a amostra local. Se repetir, abra uma issue |
