# Dia 4 — Ler e escrever arquivos

> 🃏 Cartas **4 · 25 · 46**  ·  📘 Original: *Day 4. Reading and writing files*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-04-arquivos/notebook.ipynb)

## 📖 Capítulo 4 — Os depoimentos

<!-- historia:inicio -->
Sexta-feira, 14h. Um pen drive com etiqueta escrita à mão chega da delegacia: **"Depoimentos
MegaOferta — cópia"**. Dentro, cinco arquivos de texto, um por vítima, transcritos pelo escrivão.

A Iara espeta o pen drive, copia a pasta para o computador e devolve o original no envelope.

— Regra número um: **a gente nunca trabalha em cima do original**. Copia, e trabalha na cópia.

Você abre o primeiro. Uma senhora de Governador Valadares, uma air fryer, um PIX de R$ 149,90 e
depois outro, de "frete". O segundo, um rapaz de BH e um PlayStation. Os textos são curtos, mas cada
um tem nome, cidade, um número de telefone, uma chave PIX e o mesmo detalhe: *"ele assinava 'Kau'"*.

— Ler cinco é fácil — diz a Iara. — Agora imagina quinhentos. O que a gente quer é o script abrir
cada arquivo, pegar só o que interessa e montar um resumo. E cada coisa que você descobrir, anota
num caderno com data e hora. Caderno de verdade só cresce, nunca apaga.

Ela aponta para a tela.

— Ah, e outra coisa. Se aparecer `DivinÃ³polis` em algum lugar, a culpa não é do escrivão. É sua.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar os quatro exemplos originais: escrever, ler tudo, ler a lista de linhas e ler linha a linha.
- Entender os modos de abertura `"r"`, `"w"`, `"a"` e `"x"`.
- Usar `with open(..., encoding="utf-8")` e saber por que ele evita dois problemas comuns.
- Ler vários arquivos de uma pasta e contar linhas e palavras.
- Extrair campos (vítima, contato, chave PIX) e gravar um resumo em `saidas/`.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Para o Python, um arquivo de texto é uma sequência de linhas. Você **abre**, **lê ou escreve** e
**fecha**:

```python
with open("notas.txt", "a", encoding="utf-8") as f:   # abre (e fecha sozinho no fim do bloco)
    f.write("primeira nota\n")                         # write não pula linha: o \n é seu
```

| Modo | O que faz | Se o arquivo não existe | Se já existe |
|---|---|---|---|
| `"r"` | ler | erro | lê |
| `"w"` | escrever do zero | cria | **apaga tudo** e escreve |
| `"a"` | acrescentar no fim | cria | mantém e acrescenta |
| `"x"` | criar novo | cria | erro (protege contra sobrescrever) |

Três jeitos de ler: `f.read()` (tudo num texto), `f.readlines()` (lista de linhas, cada uma com
`\n`) e `for linha in f:` (uma por vez, sem carregar o arquivo inteiro na memória).

**Codificação.** Sem `encoding=`, o Python usa o padrão do sistema. No Linux e no macOS costuma ser
UTF-8; no Windows em português, muitas vezes é **cp1252**. Um arquivo gravado num e lido no outro
vira `VÃ­tima`. O remédio é sempre o mesmo: `encoding="utf-8"` ao **gravar e ao ler**.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/write_text.py`](original/write_text.py) | Acrescenta `"Results text"` ao `results.txt` (modo `"a"`) |
| [`original/read_file.py`](original/read_file.py) | Mostra o arquivo inteiro com `read()` |
| [`original/read_lines_loop.py`](original/read_lines_loop.py) | Percorre as linhas numerando cada uma |
| [`original/readlines.py`](original/readlines.py) | Pega a lista de linhas com `readlines()` e mostra a segunda |
| [`original/results.txt`](original/results.txt) | Arquivo de exemplo com 3 linhas (criado aqui para os scripts rodarem de primeira) |

```bash
cd dia-04-arquivos/original
python read_file.py
python read_lines_loop.py
python readlines.py
python write_text.py      # rode e depois rode read_file.py de novo: o que mudou?
```

> 💡 O `write_text.py` não coloca `\n`: depois de rodar, a última linha fica
> `...not foundResults text`. Rode duas vezes e veja grudar de novo. Para desfazer (de dentro de `original/`): `git checkout -- results.txt`.
>
> O autor também lembra do jeito mais simples de salvar a saída de qualquer script, sem uma linha de
> código: `python read_file.py > copia.txt` (o `>` manda o que iria para a tela para um arquivo).

## 🇧🇷 Nível 2 — Camada Brasil

| Arquivo | O que faz |
|---|---|
| [`br/01_ler_depoimentos.py`](br/01_ler_depoimentos.py) | Lê os 5 depoimentos do caso das três formas e monta uma tabela de linhas/palavras |
| [`br/02_anotacoes.py`](br/02_anotacoes.py) | Caderno do analista: modos `"x"`, `"a"` e `"w"`, carimbo de hora e a armadilha do cp1252 |
| [`br/03_extrai_campos.py`](br/03_extrai_campos.py) | **O caso:** extrai vítima, cidade, contato, produto, valor e chave PIX; grava resumo `.txt` e `.tsv` |

```bash
cd dia-04-arquivos
python br/01_ler_depoimentos.py
python br/02_anotacoes.py          # rode duas vezes: o caderno cresce
python br/03_extrai_campos.py
```

Nenhum usa internet: os depoimentos estão em `caso/dados/depoimentos/` (fictícios).

**O que você deve ver no caso:** "Kau" aparece nos **5 de 5** depoimentos, todos com o mesmo WhatsApp
`(31) 98888-0101`. E duas chaves PIX se repetem: `f38b2ffc…` recebeu de DEN-001 e DEN-003, e `e5121482…`
de DEN-002 e DEN-004. Mesmas contas recebendo de vítimas diferentes é o começo do mapa do dinheiro
(no Dia 8 você descobre de quem são).

## ⚖️ Ética, LGPD e OPSEC

- **Trabalhe na cópia, nunca no original.** Um `"w"` errado apaga um depoimento. Mantenha os originais
  intocados (no Dia 14 você aprende a provar isso com hash SHA-256).
- **Minimização.** O resumo do `br/03` deixa o **CPF de fora** de propósito: para cruzar chaves PIX e
  telefones ele não é necessário (LGPD, art. 6º, III). Pegue só o que a pergunta exige.
- **Depoimento de vítima é dado sensível de contexto.** Nome + cidade + valor perdido expõe a pessoa. Não
  copie para e-mail pessoal, pen drive sem controle ou nuvem pública.
- **Caderno com data e hora, só acrescentando.** Um registro que só cresce (modo `"a"`) mostra a ordem
  em que você descobriu as coisas. Isso protege você e a investigação.
- **Cuidado com `saidas/`.** A pasta está no `.gitignore` deste repositório justamente para resumos não
  irem parar no GitHub por engano. Faça o mesmo nos seus projetos.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Fichas padronizadas e vínculos**: uma ficha `campo: valor` por
depoimento, o aviso automático de WhatsApps e chaves PIX repetidos e um histórico de execuções.

## 🔎 Inovação OSINT do dia

**`Path.copy()` com metadados (Python 3.14).** Desde o Python 3.14, os caminhos do `pathlib` sabem se
copiar sozinhos: `Path("depoimentos/DEN-001.txt").copy("copia/DEN-001.txt", preserve_metadata=True)`.
Com `preserve_metadata=True`, a cópia mantém a **data de modificação** do original (no Windows os
metadados são sempre preservados). Para quem recebe evidências em pen drive, isso evita perder a
cronologia ao fazer a cópia de trabalho, sem precisar do `shutil.copy2`. Também vieram `copy_into()`,
`move()` e `move_into()`. Biblioteca simples: `pathlib`, nativo (no 3.9–3.13, use `shutil.copy2`, que
faz o mesmo).

## 📚 Para ir além

- Tutorial oficial, leitura e escrita de arquivos: <https://docs.python.org/pt-br/3/tutorial/inputoutput.html#reading-and-writing-files>
- `open()` e os modos: <https://docs.python.org/pt-br/3/library/functions.html#open>
- `pathlib` (inclui `copy()`, novo no 3.14): <https://docs.python.org/3/library/pathlib.html>
- Codificações e Unicode, guia oficial: <https://docs.python.org/pt-br/3/howto/unicode.html>

## ✅ Checklist

- [ ] Rodei os quatro scripts originais e vi o `results.txt` mudar
- [ ] Entendi por que `"w"` é perigoso para registros
- [ ] Rodei o `br/02` duas vezes e vi o caderno crescer
- [ ] Vi com meus olhos o `VÃ­tima` da armadilha do cp1252
- [ ] Descobri quais depoimentos pagaram na mesma chave PIX
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
