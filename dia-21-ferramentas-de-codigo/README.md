# Dia 21 — Ferramentas para ajudar você a trabalhar com código

> 🃏 Cartas **21 · 42 · 63**  ·  📘 Original: *Day 21. Tools to help you work with code*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-21-ferramentas-de-codigo/notebook.ipynb)

## 📖 Capítulo 21 — O dossiê

<!-- historia:inicio -->
Último dia. A Iara chega com dois cafés e senta ao seu lado, sem pressa.

— Antes de entregar, a gente revisa. Não o texto: o **código**. Um dossiê só é tão confiável quanto
o script que gerou cada número dele.

Ela pede que você rode os testes. O doctest do CPF passa. O unittest das expressões regulares passa.
Você troca, de propósito, um peso no cálculo do dígito verificador, e duas linhas ficam vermelhas na
hora.

— É isso. Teste não serve para provar que está certo; serve para avisar **rápido** quando ficou
errado. E a IA? — ela pergunta, já sabendo a resposta.

— Ajuda a revisar, mas não é fonte — você responde. — E nada do caso vai para ela.

Às 15h, o `dossie.html` sai com seis verificações verdes no fim: idade do domínio, as três
contas laranja, R$ 54.877,40, a linha do tempo da Black Friday e o hash de cada evidência.

A Delegada Rita lê em silêncio, folheia até a página dos hashes e levanta os olhos.

— Quem fez as ferramentas?

A Iara aponta para você. Vinte e um dias atrás, você nunca tinha escrito um `print`.
<!-- historia:fim -->

## 🎯 Objetivos

- Conhecer as ferramentas que o autor recomenda (verificadores de sintaxe e de estilo, IA, Stack
  Overflow) e as equivalentes offline da biblioteca padrão.
- Achar erros de sintaxe com `ast` e `py_compile`, sem enviar o código para lugar nenhum.
- Escrever testes com **`doctest`** e **`unittest`**.
- Gerar o **dossiê final** do caso, com autoverificação dos números.
- Usar IA como **apoio** à programação, com checagem de alucinação e sem expor dados do caso.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Existem três tipos de problema no código, e cada um tem a sua ferramenta:

| Problema | Exemplo | Quem acha |
|---|---|---|
| **Sintaxe**: o Python nem consegue ler | esqueceu o `:` no fim do `for` | `python -m py_compile`, `ast.parse`, o próprio editor |
| **Estilo**: roda, mas é difícil de ler | linhas enormes, nomes `x1`, `x2` | verificadores de estilo (PEP 8): `ruff`, `flake8` |
| **Lógica**: roda e dá o resultado **errado** | peso trocado no dígito verificador | **testes**: `doctest`, `unittest` |

O terceiro é o perigoso: nenhum verificador de sintaxe ou estilo vai notar. Por isso existem os
testes, que são exemplos com resposta conhecida:

```python
def dobro(x):
    """
    >>> dobro(21)
    42
    """
    return x * 2
```

`doctest.testmod()` roda os `>>>` da documentação e compara. O `unittest` organiza testes maiores
em classes, com `assertEqual`, `assertTrue` e companhia.

**IA** (ChatGPT e afins) ajuda nos três, mas **erra com confiança**. Trate a resposta como a de um
colega apressado: útil para dar ideias, nunca aceita sem testar.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

O Dia 21 do curso **não tem código**: é uma lista comentada de ferramentas. Resumo e comentários em
[`original/LEIA-ME.md`](original/LEIA-ME.md).

| Arquivo | O que é |
|---|---|
| [`original/LEIA-ME.md`](original/LEIA-ME.md) | O que o autor recomenda, com notas de 2026 |
| [`original/nivel1_checar_sintaxe.py`](original/nivel1_checar_sintaxe.py) | **Reconstrução nossa** da prática: verificador de sintaxe offline com `ast` + `py_compile` |
| [`original/codigo_com_erro.py`](original/codigo_com_erro.py) | Script com erro de sintaxe **de propósito** (não roda) |

```bash
cd dia-21-ferramentas-de-codigo/original
python nivel1_checar_sintaxe.py              # aponta linha, coluna e a mensagem do Python
python -m py_compile codigo_com_erro.py      # a mesma checagem, direto no terminal
```

> 💡 Por que offline? Colar código num site de verificação é **enviar o código para terceiros**. Se
> ele tiver uma chave de API, um caminho de pasta do caso ou um dado de teste real, vazou.

## 🇧🇷 Nível 2 — Camada Brasil

Só **biblioteca padrão**, 100% offline.

| Arquivo | O que faz |
|---|---|
| [`br/01_doctest_cpf.py`](br/01_doctest_cpf.py) | A função de CPF do Dia 2 com 11 exemplos `>>>` (máscara, dígitos iguais, vazio, exceção) |
| [`br/02_unittest_regex.py`](br/02_unittest_regex.py) | 8 testes `unittest` para os padrões do Dia 11, com `subTest` e um teste de integração com a conversa |
| [`br/03_dossie_final.py`](br/03_dossie_final.py) | **O grande final:** `saidas/dossie.html` com domínio, contas laranja (do dump), cidades, CNPJs, linha do tempo, hashes e autoverificação |
| [`br/04_ia_como_apoio.md`](br/04_ia_como_apoio.md) | Como usar IA como apoio: modelo de prompt de revisão, 5 perguntas contra alucinação e por que nunca colar dado de caso real |

```bash
cd dia-21-ferramentas-de-codigo
python br/01_doctest_cpf.py
python br/02_unittest_regex.py
python br/03_dossie_final.py       # depois abra saidas/dossie.html
```

**O que você deve ver no caso:** seis checagens ✅ antes de o dossiê ser gravado. Se você alterar
qualquer arquivo de `caso/dados/` de um jeito que faça os números deixarem de bater (por exemplo,
mudar um valor no `denuncias.csv` sem mudar no dump), o script **se recusa** a gerar o dossiê.

> 🔁 Experimente o ciclo completo: no `01_doctest_cpf.py`, troque `(n + 1 - i)` por `(n - i)` e rode.
> O doctest acusa na hora. Desfaça a troca. Esse é o seu "verificador de lógica".

## ⚖️ Ética, LGPD e OPSEC

- **Nunca cole dado de caso real numa IA pública** (nomes, CPFs, chaves PIX, prints de conversa).
  Anonimize: a IA precisa da *estrutura* do dado, não do dado. Detalhes em `br/04_ia_como_apoio.md`.
- **IA não é fonte.** Se o relatório diz "o CNPJ X pertence a Y", a fonte tem que ser a Receita (ou
  outra primária), nunca "o assistente disse".
- **Perguntar também revela.** Buscar no Stack Overflow ou numa IA "como achar o dono da chave PIX
  f38b…" expõe o alvo e a investigação. Pergunte sobre **código**, com exemplos inventados.
- **Testes protegem pessoas.** Um bug no validador de CPF pode descartar uma denúncia verdadeira ou
  "confirmar" um documento falso. Testar é parte da responsabilidade de quem assina o relatório.
- **O dossiê vai circular.** Ele traz titulares das contas e o nome declarado no domínio: tudo é
  **declaração**, e o documento diz isso na seção de limitações. Hipótese não vira fato por estar
  bem formatada.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **O revisor do curso**: um script que lê (sem executar) **todos** os
`br/*.py` do repositório com `ast` e confere as regras do [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## 🔎 Inovação OSINT do dia

**Ruff: verificador de estilo e de bugs, rápido o bastante para rodar a cada gravação.** O **Ruff**
(`pip install ruff`, licença MIT, escrito em Rust) junta num só programa as regras de vários
verificadores clássicos (flake8, isort, pyupgrade e muitos plugins) e ainda formata o código
(`ruff format`). É o "PythonChecker" que o autor recomenda, só que offline: `ruff check .` na pasta do
repositório aponta imports não usados, variáveis locais que nunca são lidas, nomes indefinidos e padrões
propensos a bug. Para ferramentas OSINT que você vai publicar, colocar `ruff check` num
GitHub Action é o jeito mais barato de manter a qualidade.

## 📚 Para ir além

- `doctest`: <https://docs.python.org/pt-br/3/library/doctest.html>
- `unittest`: <https://docs.python.org/pt-br/3/library/unittest.html>
- `ast`: <https://docs.python.org/pt-br/3/library/ast.html>
- PEP 8, o guia de estilo do Python: <https://peps.python.org/pep-0008/>
- Ruff: <https://docs.astral.sh/ruff/>
- Lista de ferramentas do autor: <https://github.com/cipher387/code-understanding-tools>
- Próximo passo sugerido pelo autor: <https://www.learnpython.org/>

## ✅ Checklist

- [ ] Li o `original/LEIA-ME.md` e achei o erro do `codigo_com_erro.py` (antes de rodar o verificador!)
- [ ] Rodei o doctest e vi ele falhar quando estraguei a função de propósito
- [ ] Rodei os 8 testes do unittest
- [ ] Gerei o dossiê final, com as seis checagens verdes
- [ ] Li o guia de IA como apoio e montei o meu próprio prompt de revisão
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md) e completei as 63 cartas 🃏
