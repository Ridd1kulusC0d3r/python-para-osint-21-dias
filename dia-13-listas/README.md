# Dia 13 — Funções para trabalhar com listas

> 🃏 Cartas **13 · 34 · 55**  ·  📘 Original: *Day 13. Functions for working with lists*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-13-listas/notebook.ipynb)

## 📖 Capítulo 13 — O mapa das vítimas

<!-- historia:inicio -->
Depois de um dia inteiro pensando em IP, proxy e cabeçalho, a Iara anuncia:

— Hoje é dia de descanso. Mais ou menos.

Ela prende na parede um mapa de Minas Gerais e uma caixa de alfinetes vermelhos.

— A Delegada Rita quer saber **onde** estão as vítimas. Parece fácil: é só pegar a coluna "cidade" da
planilha. Faz aí.

Você imprime a coluna e para no meio. "Belo Horizonte", "belo horizonte", "Belo Horizone". "Poços de
Caldas" e "Pocos de Caldas". Você ordena a lista para ajudar e "Águas Lindas", da sua lista de teste,
aparece **depois** de "Zé Doca".

— O computador não sabe português — ela diz, rindo. — Para ele, "Á" é só o número 193, maior que o "z".
Lista é a ferramenta mais simples do Python e é onde mais se erra em relatório. Cidade duplicada
dobra a vítima, ordem errada esconde o padrão.

Ela entrega os alfinetes.

— Quero três respostas: quantas cidades **de verdade**, quais têm mais vítimas e quais só apareceram em
novembro. Se o golpe está se espalhando, o mapa vai mostrar.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar os cinco exemplos originais: `copy`, `sort`, `insert`, `append` e `pop`.
- Entender índices (começam em 0; negativos contam do fim) e a diferença entre `copy()` e `=`.
- Ordenar texto em português do jeito certo (acentos e maiúsculas).
- Tirar repetidos mantendo a ordem (`dict.fromkeys`) e fazer ranking (`collections.Counter`).
- Comparar grupos com conjuntos: `&`, `-`, `|`.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Uma **lista** é uma fila numerada de itens: `["BH", "Betim", "Contagem"]`. A numeração começa em
**0**, e `lista[-1]` é sempre o último.

| Quero… | Use | Muda a lista? |
|---|---|---|
| pôr no fim | `lista.append(x)` | sim |
| pôr na posição i | `lista.insert(i, x)` | sim |
| tirar da posição i | `lista.pop(i)` (devolve o item) | sim |
| tirar pelo valor | `lista.remove(x)` | sim |
| ordenar | `lista.sort()` · `sorted(lista)` | sim · **não** (devolve outra) |
| copiar | `lista.copy()` | não |
| tirar repetidos com ordem | `list(dict.fromkeys(lista))` | não |
| contar | `Counter(lista).most_common(3)` | não |

**Ordenar com acento:** `sorted()` compara os códigos Unicode das letras. Todas as maiúsculas vêm
antes das minúsculas, e as acentuadas vêm depois do "z". A solução é dar ao `sorted` uma **chave**
(`key=`): uma função que transforma cada item numa versão "comparável" (sem acento, tudo minúsculo).
O item original não muda; só a comparação.

**Conjunto (`set`)** é uma "lista sem repetidos e sem ordem". Serve para perguntar "o que tem nos
dois?" (`a & b`), "o que só tem em A?" (`a - b`) e "o que tem em algum?" (`a | b`).
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/array_copy.py`](original/array_copy.py) | Copia uma lista de cidades dos EUA e imprime com `sep=", "` |
| [`original/array_sort.py`](original/array_sort.py) | Ordena em ordem crescente e depois decrescente |
| [`original/array_insert.py`](original/array_insert.py) | Insere "Dallas" na posição 3 |
| [`original/array_append.py`](original/array_append.py) | Acrescenta "Dallas" no fim |
| [`original/array_pop.py`](original/array_pop.py) | Remove o item da posição 2 |

```bash
cd dia-13-listas
python original/array_copy.py
python original/array_sort.py
```

Nada para instalar. 💡 Repare no `array_append.py`: o `sep=";"` não aparece na saída. O comentário
`# 💬` explica por quê (e como fazer funcionar).

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão** e 100% offline.

| Arquivo | O que faz |
|---|---|
| [`br/01_capitais.py`](br/01_capitais.py) | As mesmas operações do original com capitais brasileiras, mais `remove`, `sorted`, índices negativos e a armadilha do `=` |
| [`br/02_ordenar_com_acento.py`](br/02_ordenar_com_acento.py) | Mostra por que "Águas Lindas" vai para o fim e corrige com `unicodedata` + `casefold` (e `locale.strxfrm`, se houver) |
| [`br/03_cidades_das_vitimas.py`](br/03_cidades_das_vitimas.py) | **O caso:** cidades de `denuncias.csv`: repetidos, ranking com `Counter` e outubro × novembro com conjuntos |

```bash
cd dia-13-listas
python br/01_capitais.py
python br/02_ordenar_com_acento.py
python br/03_cidades_das_vitimas.py
```

**O que você deve ver no caso:** 16 grafias diferentes viram **11 cidades**. Belo Horizonte lidera com
8 vítimas. **Betim, Divinópolis, Ipatinga e Sete Lagoas** só aparecem em novembro: o golpe se espalhou
perto da Black Friday.

## ⚖️ Ética, LGPD e OPSEC

- **Duplicata infla o número.** Antes de dizer "40 vítimas", confirme que não há a mesma denúncia
  contada duas vezes (mesmo CPF, mesma data, mesmo valor). Número errado em relatório vira manchete
  errada.
- **Agregar protege.** Para a imprensa ou para um painel, mostre "8 vítimas em Belo Horizonte", não a
  lista de nomes. Cidade + data + valor de uma cidade pequena pode reidentificar a pessoa (LGPD:
  minimização e anonimização).
- **Padronizar não é corrigir a fonte.** Guarde o valor original ao lado do padronizado: se a
  padronização errar, o original prova o que a vítima informou.
- **Cuidado com `=`**: "copiar" uma lista de evidências com `=` e depois apagar itens da "cópia" apaga
  da original também. Em evidência, use sempre `copy()` (ou trabalhe numa cópia do arquivo).

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Fila de diligências**: agrupe as denúncias por chave PIX, ordene por
data e por prejuízo e diga por qual conta a polícia deve começar.

## 🔎 Inovação OSINT do dia

**Ordenação "humana" com `natsort`.** Listas de evidências costumam ter nomes como `print_2.png`,
`print_10.png`, `print_1.png`. O `sorted()` comum devolve `print_1`, `print_10`, `print_2`. A biblioteca
Python `natsort` ordena como uma pessoa faria (1, 2, 10) e, com `ns.LOCALE`, ainda respeita acentos:

```python
# pip install natsort
from natsort import natsorted
print(natsorted(["print_10.png", "print_2.png", "print_1.png"]))
```

Útil para ordenar capturas de tela, páginas de PDF e exports de conversa numerados.

## 📚 Para ir além

- Listas no tutorial oficial: <https://docs.python.org/pt-br/3/tutorial/datastructures.html>
- HOWTO de ordenação (`key=`, estabilidade): <https://docs.python.org/pt-br/3/howto/sorting.html>
- `collections.Counter`: <https://docs.python.org/pt-br/3/library/collections.html#collections.Counter>
- `unicodedata`: <https://docs.python.org/pt-br/3/library/unicodedata.html>
- natsort: <https://github.com/SethMMorton/natsort>

## ✅ Checklist

- [ ] Rodei os cinco scripts originais
- [ ] Entendi por que `apelido = lista` não é cópia
- [ ] Ordenei cidades com acento do jeito certo
- [ ] Descobri quantas cidades de verdade há no caso e quais só aparecem em novembro
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
