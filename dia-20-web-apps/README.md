# Dia 20 — Criando web apps

> 🃏 Cartas **20 · 41 · 62**  ·  📘 Original: *Day 20. Web apps creation*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-20-web-apps/notebook.ipynb)

## 📖 Capítulo 20 — O painel do caso

<!-- historia:inicio -->
Às 10h chega um e-mail da Delegada Rita com cópia para três escrivães: *"Recebi mais duas ligações
de vítimas. Alguém consegue me dizer se a chave PIX que elas citaram já está no caso?"*

A Iara lê em voz alta e olha para você.

— Esta é a quarta vez nesta semana. A cada pergunta, alguém tem que te chamar, você abre o terminal,
roda um script, copia o resultado e manda por e-mail. Não escala. A equipe precisa de um **painel**:
uma página onde eles digitam a cidade ou a chave PIX e veem a resposta sozinhos.

Você pensa em frameworks, servidores, hospedagem. Ela já está balançando a cabeça.

— O Python traz um servidor web de fábrica. Para uso interno, na nossa rede, é suficiente. Mas
presta atenção numa coisa: **tudo o que alguém digita no formulário volta para a página**. Se você
devolver sem tratar, qualquer um escreve um `<script>` ali e o navegador do escrivão executa. Num
painel de investigação, isso é a pior vergonha possível.

Ela escreve no quadro, sublinhado duas vezes: **`html.escape` SEMPRE**.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar o web app original com **Streamlit** (localmente e, com algum esforço, no Colab).
- Entender o ciclo pedido → resposta HTTP (método, caminho, status, cabeçalhos, corpo).
- Escrever um servidor e um formulário de busca só com `http.server`.
- Ler parâmetros da URL com `urllib.parse.parse_qs`.
- Entender **XSS** e evitá-lo com `html.escape` (e uma Content-Security-Policy).
- Testar um web app automaticamente, sem navegador.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Um **web app** é um programa que fica esperando pedidos. Quando o navegador abre
`http://127.0.0.1:8001/?campo=cidade&q=contagem`, ele manda ao servidor:

```
GET /?campo=cidade&q=contagem HTTP/1.1
```

O servidor separa o **caminho** (`/`) da **consulta** (`campo=cidade&q=contagem`), faz a busca e
responde com um **status** (`200 OK`, `404 Not Found`), **cabeçalhos** (`Content-Type: text/html`) e
o **corpo** (o HTML).

| Peça | Streamlit (original) | Biblioteca padrão (BR) |
|---|---|---|
| Servidor | embutido, `streamlit run app.py` | `http.server.ThreadingHTTPServer` |
| Formulário | `st.text_input`, `st.button` | `<form method="get">` em HTML |
| Ler o que foi digitado | variável Python | `urllib.parse.parse_qs` |
| Escapar HTML | automático | **você**: `html.escape` |

**XSS (Cross-Site Scripting):** se alguém busca `<script>…</script>` e o servidor devolve o termo do
jeito que veio, o navegador **executa** aquele código, com acesso ao que o usuário vê. `html.escape`
troca `<` por `&lt;` e `>` por `&gt;`: o navegador mostra o texto em vez de executar.

**127.0.0.1 × 0.0.0.0:** o primeiro só aceita conexões do próprio computador; o segundo, de qualquer
máquina da rede. Comece sempre pelo 127.0.0.1.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/webapp.py`](original/webapp.py) | Página com título, caixa de texto e botão que mostra o texto digitado (Streamlit) |

**No seu computador** (o jeito fácil):

```bash
pip install streamlit
cd dia-20-web-apps/original
streamlit run webapp.py       # NÃO é "python webapp.py": o Streamlit tem o próprio comando
```

O terminal mostra uma *Local URL* (`http://localhost:8501`) e uma *Network URL*. Abra a primeira no
navegador. Para parar: `Ctrl+C`.

**No Colab** (sendo honesto: dá trabalho). O Streamlit precisa de um servidor rodando o tempo todo,
e o Colab não abre portas para a internet. O caminho que costuma funcionar:

```python
!pip install -q streamlit
!streamlit run original/webapp.py --server.port 8501 --server.headless true &>/content/st.log &
from google.colab import output
output.serve_kernel_port_as_window(8501)   # abre um link para a porta, só para você
```

Se o link abrir em branco, espere alguns segundos e recarregue. Túneis públicos (ngrok,
localtunnel, cloudflared) também funcionam, mas expõem o app para a internet inteira: não use com
dados de caso. Para estudar Streamlit de verdade, rode localmente ou use o Codespaces (Dia 0).

> 💡 No `webapp.py`, a variável `nickname = textInput.title()` é calculada e nunca usada. O autor
> conta, num artigo, como usou esse mesmo esqueleto para transformar o **Maigret** (busca de
> usernames) num web app.

## 🇧🇷 Nível 2 — Camada Brasil

Só **biblioteca padrão**, 100% offline (dados do caso).

| Arquivo | O que faz |
|---|---|
| [`br/01_servidor_basico.py`](br/01_servidor_basico.py) | `BaseHTTPRequestHandler` com `do_GET`, status, cabeçalhos, 404 e log de cada pedido (porta 8000) |
| [`br/02_painel_do_caso.py`](br/02_painel_do_caso.py) | **O painel:** formulário de busca por cidade, chave PIX ou produto em `denuncias.csv`, resultados em tabela, `parse_qs`, `html.escape` e CSP (porta 8001) |

```bash
cd dia-20-web-apps
python br/02_painel_do_caso.py          # abra http://127.0.0.1:8001 · Ctrl+C para parar
OSINT_OFFLINE=1 python br/02_painel_do_caso.py   # modo teste
```

**Modo teste.** Com `OSINT_OFFLINE=1` (ou quando a saída não é um terminal, como no teste
automático), o script sobe o servidor numa *thread*, faz pedidos a si mesmo com `urllib`, imprime o
resultado e **encerra sozinho**. O painel testa inclusive um ataque: busca
`<script>alert('xss')</script>` e confere que voltou escapado.

**No Colab**, os scripts detectam o notebook, rodam o servidor em segundo plano (a célula não trava)
e chamam `google.colab.output.serve_kernel_port_as_window(porta)`, dentro de `try/except
ImportError` para não quebrar fora do Colab. Rodou a célula duas vezes e deu "porta ocupada"?
Troque `PORTA` ou reinicie o ambiente.

**O que você deve ver no caso:** busque `contagem` (4 denúncias), `f38b` no campo chave PIX (16
denúncias, a conta da Jéssica Prado Lima) e `poços` (3 denúncias: a busca sem acento acha também
"Pocos de Caldas").

## ⚖️ Ética, LGPD e OPSEC

- **O painel é interno.** Use `127.0.0.1` ou, no máximo, a rede do NFA. Nada de túnel público para
  um painel com dados de vítimas. `http.server` não tem login nem HTTPS: não serve para produção.
- **Minimização na tela.** O painel não mostra nome nem CPF das vítimas: para saber se uma chave PIX
  já está no caso, ninguém precisa deles.
- **XSS e injeção.** Todo texto vindo de fora (busca, dados raspados, relatos de vítimas) passa por
  `html.escape` antes de ir para a página. E se um dia o painel consultar um banco, use parâmetros
  `?` (Dia 8), nunca f-string em SQL.
- **Log é dado pessoal também.** O servidor registra o IP e o que cada pessoa buscou. Isso é útil
  para auditoria, mas tem que ser guardado e apagado com o mesmo cuidado que o resto do caso.
- Um web app OSINT **aberto ao público** (como o Maigret + Streamlit do autor) vira ferramenta de
  qualquer pessoa, inclusive de quem quer perseguir alguém. Pense em quem vai usar antes de publicar.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **A API do caso**: rotas JSON com filtros por cidade, chave e período,
um resumo agregado e testes automáticos (inclusive "nome e CPF não vazam").

## 🔎 Inovação OSINT do dia

**Web app em Python que roda no navegador, sem servidor: stlite.** O **stlite** é um port do
Streamlit para **Pyodide** (Python compilado para WebAssembly). O app inteiro roda **dentro do
navegador de quem abre a página**, e os dados não saem do computador da pessoa. Para OSINT isso é
interessante: dá para distribuir uma ferramenta de análise como um único arquivo HTML, que funciona
até em computador sem Python instalado e não manda nada para servidor nenhum. Limitação: pacotes que
dependem de rede ou de código nativo nem sempre funcionam no Pyodide.

## 📚 Para ir além

- `http.server`: <https://docs.python.org/pt-br/3/library/http.server.html>
- `urllib.parse` (`urlsplit`, `parse_qs`, `urlencode`): <https://docs.python.org/pt-br/3/library/urllib.parse.html>
- OWASP: prevenção de XSS: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- Streamlit: <https://docs.streamlit.io/>
- stlite: <https://github.com/whitphx/stlite>
- MDN, Content-Security-Policy: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers/Content-Security-Policy>

## ✅ Checklist

- [ ] Rodei o `webapp.py` com `streamlit run`
- [ ] Subi o servidor básico e vi o log de cada pedido
- [ ] Usei o painel para buscar por cidade, chave PIX e produto
- [ ] Testei uma busca com `<b>oi</b>` e vi o texto aparecer escapado (não em negrito)
- [ ] Rodei os dois scripts em modo teste (`OSINT_OFFLINE=1`)
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
