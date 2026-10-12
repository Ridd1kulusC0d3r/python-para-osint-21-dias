# Dia 21 original: não há código do autor

A pasta `Day_21` **não existe** no repositório do cipher387. O último dia do curso é uma conversa
sobre **ferramentas que ajudam a escrever e entender código**. Em resumo, com as nossas palavras:

| O que o autor recomenda | Para quê | Comentário em 2026 |
|---|---|---|
| **Verificadores de sintaxe online** (ex.: ExtendsClass Python Tester) | Achar rapidamente o erro que impede o script de rodar | O próprio Python faz isso offline: `python -m py_compile arquivo.py` (veja `nivel1_checar_sintaxe.py`) |
| **Verificadores de estilo** (ex.: PythonChecker) | Apontar espaços, quebras de linha e comentários longos: o que não quebra o código, mas o deixa difícil de ler | Hoje o padrão é rodar localmente o `ruff` ou o `flake8` (regras da PEP 8) |
| **ChatGPT** | Revisar, sugerir soluções e explicar código dos outros | O autor avisa, com ênfase, que ele **erra muito**: tente entender a solução sozinho (veja `br/04_ia_como_apoio.md`) |
| **Stack Overflow** | Comunidade com milhões de perguntas e respostas sobre Python | Ainda é a referência; leia as respostas mais votadas **e** a data delas |
| **Phind** | Buscador com IA que resume respostas do Stack Overflow e de sites técnicos | Ferramentas desse tipo mudam rápido; confira se ainda existe antes de depender dela |
| **Adrenaline** | Fazer perguntas a um chatbot sobre o conteúdo de repositórios GitHub grandes | Idem: o mercado de "converse com o seu repositório" muda todo mês |
| Lista do autor: <https://github.com/cipher387/code-understanding-tools> | Mais ferramentas para entender código | Vale como índice; confira se cada link continua no ar |

No fim, o autor sugere os próximos passos: praticar investigações usando ferramentas OSINT escritas
em Python, fazer cursos maiores (como o learnpython.org) se a ideia for desenvolver projetos sérios,
e publicar as próprias ferramentas.

## O que está nesta pasta

| Arquivo | O que é |
|---|---|
| [`nivel1_checar_sintaxe.py`](nivel1_checar_sintaxe.py) | **Reconstrução nossa** da prática proposta (não é código do autor): um verificador de sintaxe offline com `ast` e `py_compile` |
| [`codigo_com_erro.py`](codigo_com_erro.py) | Um script com **erro de sintaxe de propósito**, para o verificador encontrar. Ele não roda, e é para não rodar |

```bash
cd dia-21-ferramentas-de-codigo/original
python nivel1_checar_sintaxe.py                    # verifica o codigo_com_erro.py
python nivel1_checar_sintaxe.py ../br/*.py         # verifica outros arquivos
```
