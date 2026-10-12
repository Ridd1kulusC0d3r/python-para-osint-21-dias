# Dia 14 — Trabalhando com o sistema de arquivos

> 🃏 Cartas **14 · 35 · 56**  ·  📘 Original: *Day 14. Working with the file system*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-14-sistema-de-arquivos/notebook.ipynb)

## 📖 Capítulo 14 — A sala de evidências

<!-- historia:inicio -->
Duas semanas de NFA e a pasta do caso já virou um labirinto: depoimentos, a conversa, a cópia da
vitrine, o dump do painel, a planilha das vítimas, CSVs que você mesmo gerou. A Iara abre o
explorador de arquivos e cruza os braços.

— Se a Delegada Rita perguntar "em quais arquivos aparece a chave `f38b2ffc`?", quanto tempo você
leva para responder?

Você começa a abrir arquivo por arquivo. Ela interrompe no terceiro.

— Agora a pergunta que importa de verdade: como você **prova** que este depoimento é o mesmo que a
vítima entregou, e que ninguém trocou uma letra no meio do caminho?

Ela escreve no quadro: **SHA-256**.

— É a impressão digital do arquivo. Mudou um byte, mudou o hash inteiro. O Código de Processo Penal
chama isso de **cadeia de custódia**: cada vestígio precisa ter a história documentada, de quem
coletou até quem analisou. Para prova digital, o hash é o lacre.

Hoje você vai fazer o Python andar pelas pastas sozinho, achar padrões em tudo e lacrar cada arquivo
com um manifesto. Amanhã, quando alguém duvidar, o manifesto responde.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar os quatro exemplos originais com `glob` e `os`.
- Usar `pathlib`: caminhos com `/`, `glob`, `rglob`, `stat`, `read_text`.
- Varrer uma pasta inteira atrás de CPFs, chaves PIX e e-mails (regex do Dia 11).
- Calcular **SHA-256** em blocos com `hashlib` e gerar um **manifesto de custódia**.
- Verificar depois se algum arquivo foi alterado, sumiu ou apareceu.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
**Andar por pastas.** O original usa `os.chdir("test_dir")` + `glob.glob("*.txt")`. Funciona, mas o
`chdir` muda a pasta do programa inteiro. O `pathlib` faz o mesmo sem mudar de pasta:

| Original (`os` + `glob`) | `pathlib` |
|---|---|
| `os.chdir("test_dir")` + `glob.glob("*.txt")` | `Path("test_dir").glob("*.txt")` |
| `glob.glob("**/*.txt", recursive=True)` | `Path("test_dir").rglob("*.txt")` |
| `open(f).read()` | `Path(f).read_text(encoding="utf-8")` |
| `os.path.getsize(f)` | `Path(f).stat().st_size` |

**Hash** é uma conta que transforma qualquer arquivo numa sequência de tamanho fixo (no SHA-256, 64
caracteres). Mesma entrada → mesmo hash, sempre. Um byte diferente → hash completamente diferente
(efeito avalanche). Não dá para "voltar" do hash ao arquivo. Por isso o hash serve de **lacre**: anote-o
no momento da coleta; se depois bater, o arquivo é o mesmo.

**Cadeia de custódia** é a documentação da história de cada vestígio, da coleta ao descarte. Está nos
**arts. 158-A a 158-F do Código de Processo Penal**, incluídos pela **Lei 13.964/2019** (o "Pacote
Anticrime"). Para evidência digital, o manifesto com hash, data e responsável é a forma prática de
cumprir essa exigência.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/print_files_names.py`](original/print_files_names.py) | Lista os `.txt` e depois todos os arquivos de `test_dir` |
| [`original/print_files_contents.py`](original/print_files_contents.py) | Mostra o conteúdo de cada `.txt` com `readlines()` |
| [`original/check_files_contents.py`](original/check_files_contents.py) | Imprime os arquivos que contêm o caractere `"2"` |
| [`original/check_re_files_contents.py`](original/check_re_files_contents.py) | Imprime os arquivos que contêm um e-mail (regex do Dia 11) |
| [`original/test_dir/`](original/test_dir) | Pasta de teste do autor (`file1.txt`, `file2.txt`, `file3.csv`) |

```bash
cd dia-14-sistema-de-arquivos/original     # os scripts originais esperam test_dir ao lado
python print_files_names.py
python check_re_files_contents.py
```

Nada para instalar. ⚠️ Rode **de dentro de `original/`**: o `os.chdir("test_dir")` procura a pasta
a partir de onde você está.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão** e 100% offline. Nenhum script altera `caso/dados`.

| Arquivo | O que faz |
|---|---|
| [`br/01_pathlib_basico.py`](br/01_pathlib_basico.py) | Anatomia de um caminho, `glob` × `rglob`, inventário com tamanho e data, e o original traduzido para `pathlib` |
| [`br/02_varre_evidencias.py`](br/02_varre_evidencias.py) | Varre `caso/dados` atrás de CPFs, chaves PIX e e-mails; mostra quais valores ligam vários arquivos |
| [`br/03_hash_custodia.py`](br/03_hash_custodia.py) | Manifesto SHA-256 (`gerar`), `verificar` e uma `demo` que adultera uma **cópia** e mostra a detecção |

```bash
cd dia-14-sistema-de-arquivos
python br/01_pathlib_basico.py
python br/02_varre_evidencias.py
python br/03_hash_custodia.py          # MODO = "demo" (troque para "gerar" ou "verificar")
```

**O que você deve ver no caso:** a chave `f38b2ffc-…` aparece em **6 arquivos** (vitrine, conversa,
planilha, dump e dois depoimentos). Os dois e-mails do vendedor ligam a vitrine à conversa. Na demo, a
troca de **uma letra** num depoimento é pega pelo hash.

## ⚖️ Ética, LGPD e OPSEC

- **Nunca trabalhe no original.** Faça a cópia de trabalho, calcule o hash do original **antes**, e
  analise só a cópia. A demo do script 03 segue essa regra.
- **Hash no momento da coleta.** Um hash calculado uma semana depois prova só que o arquivo não mudou
  *desde então*. Registre também quem coletou, quando, de onde e com qual ferramenta (art. 158-B do
  CPP: as etapas vão do reconhecimento ao descarte).
- **SHA-256, não MD5.** MD5 e SHA-1 têm colisões conhecidas (dois arquivos diferentes com o mesmo
  hash). Se um laudo antigo traz MD5, calcule também o SHA-256.
- **Abrir arquivo altera metadados.** Abrir um documento num editor pode mudar a data de acesso ou até
  regravar o arquivo. Ler com Python em modo `"rb"` não altera o conteúdo, mas em perícia de verdade
  usa-se bloqueador de escrita e imagem forense.
- **Varredura acha dados de terceiros.** O script 02 encontra 38 CPFs, quase todos de vítimas. Ele
  mostra só a contagem na tela: é minimização (LGPD) na prática.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Triagem do pendrive apreendido**: descubra arquivos com extensão
mentirosa, duplicatas e o que já está no caso, só com hash e "números mágicos".

## 🔎 Inovação OSINT do dia

**Hash "difuso" (fuzzy hashing) com `ppdeep`.** O SHA-256 diz só "igual" ou "diferente": mudou uma
vírgula, o hash não tem nada a ver. Já o *fuzzy hashing* (algoritmo do **ssdeep**) gera hashes que
ficam **parecidos** quando os arquivos são parecidos, e dá uma nota de semelhança de 0 a 100. Serve
para achar a mesma vitrine falsa com o preço trocado, ou versões de um mesmo documento. A biblioteca
`ppdeep` implementa o ssdeep em Python puro:

```python
# pip install ppdeep
import ppdeep
a = ppdeep.hash(open("vitrine_v1.html", "rb").read())
b = ppdeep.hash(open("vitrine_v2.html", "rb").read())
print(ppdeep.compare(a, b))   # 0 a 100
```

Use o SHA-256 para **integridade** (prova) e o fuzzy hash para **semelhança** (pista).

## 📚 Para ir além

- `pathlib` (documentação oficial): <https://docs.python.org/pt-br/3/library/pathlib.html>
- `hashlib`: <https://docs.python.org/pt-br/3/library/hashlib.html>
- Código de Processo Penal, arts. 158-A a 158-F: <https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm>
- Lei 13.964/2019: <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13964.htm>
- Lista de assinaturas de arquivo ("magic numbers"): <https://en.wikipedia.org/wiki/List_of_file_signatures>
- ppdeep: <https://github.com/elceef/ppdeep>

## ✅ Checklist

- [ ] Rodei os quatro scripts originais de dentro de `original/`
- [ ] Usei `rglob` para listar todos os arquivos do caso, com subpastas
- [ ] Descobri em quantos arquivos aparece cada chave PIX
- [ ] Gerei o manifesto SHA-256 e vi a demo pegar a adulteração
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
