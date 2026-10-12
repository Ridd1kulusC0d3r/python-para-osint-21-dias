# Dia 16 — map() e funções para strings

> 🃏 Cartas **16 · 37 · 58**  ·  📘 Original: *Day 16. List mapping and functions for work with strings*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-16-map-e-strings/notebook.ipynb)

## 📖 Capítulo 16 — Os muitos nomes de Kau

<!-- historia:inicio -->
Segunda-feira. O post-it de sexta continua colado no monitor, agora com mais uma linha escrita pela
Iara: **`Kaua T Brandao — KTB123`**.

— O RDAP te deu um nome sem acento e com o meio abreviado — ela diz, apoiando a caneca na sua mesa. —
O WhatsApp diz "Kau Ofertas". O Telegram, `kauofertas`. O e-mail, `kau.ofertas`. O registro que a
Delegada Rita mandou diz **Kauã Teixeira Brandão**. Quantas pessoas são essas?

Você arrisca: uma só?

— Pode ser. Mas o computador acha que são cinco. Para ele, "Brandão" e "brandao" são palavras
diferentes, e "Kaua T" não tem nada a ver com "Kauã Teixeira". Hoje você vai ensinar o computador a
enxergar como a gente.

Ela desenha no quadro uma seta saindo de um nome e se abrindo em dezenas de setas menores.

— E vai fazer o caminho inverso também: a partir do nome, **gerar** os usernames que ele pode ter
usado em outros lugares. Golpista reaproveita apelido. Sempre. A lista sai daqui e alimenta as
ferramentas do Dia 3.
<!-- historia:fim -->

## 🎯 Objetivos

- Entender `map()`: aplicar uma função a cada item de uma lista.
- Usar `title()`, `capitalize()`, `replace()` e `split()` como no curso original.
- Corrigir o `title()` para nomes brasileiros (da, de, dos, e).
- Remover acentos com `unicodedata` e criar uma "chave de comparação".
- Gerar variantes de username a partir de um nome e de um apelido.
- Desmontar uma linha de conversa exportada com `split`, `strip` e `join`.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
**`map(função, lista)`** pega uma função e a aplica em **cada** item da lista, devolvendo os
resultados na mesma ordem. É o jeito curto de escrever um laço `for` que transforma tudo:

```python
list(map(str.upper, ["ana", "bia"]))   # ['ANA', 'BIA']
[n.upper() for n in ["ana", "bia"]]   # a mesma coisa, como "list comprehension"
```

Repare que a função vai **sem parênteses**: você entrega a função ao `map`, e ele a chama.
`map()` devolve um objeto "preguiçoso"; `list()` força o cálculo. Seu par é **`filter(função, lista)`**,
que fica só com os itens para os quais a função devolve `True`.

Os métodos de texto mais úteis em OSINT:

| Método | Exemplo | Resultado |
|---|---|---|
| `title()` | `"maria da silva".title()` | `'Maria Da Silva'` (erra o "da") |
| `capitalize()` | `"belo horizonte".capitalize()` | `'Belo horizonte'` |
| `replace(a, b)` | `"kau_ofertas".replace("_", ".")` | `'kau.ofertas'` |
| `split(sep, n)` | `"a:b:c".split(":", 1)` | `['a', 'b:c']` |
| `sep.join(lista)` | `".".join(["kau", "ofertas"])` | `'kau.ofertas'` |
| `strip()` | `"  oi \n".strip()` | `'oi'` |
| `casefold()` | `"BRANDÃO".casefold()` | `'brandão'` |

**Acentos** não se tiram com `replace` letra por letra: a forma normalizada **NFKD** do Unicode
separa "ã" em "a" + "~", e aí basta descartar os acentos soltos (`unicodedata.combining`).
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/array_map.py`](original/array_map.py) | Dobra cada número de uma lista com `map()` |
| [`original/capallwords.py`](original/capallwords.py) | Maiúscula em todas as palavras com `title()` |
| [`original/capfirstword.py`](original/capfirstword.py) | Maiúscula só na primeira letra com `capitalize()` |
| [`original/replace.py`](original/replace.py) | Troca `_` por `-` em várias palavras |
| [`original/split_string.py`](original/split_string.py) | Quebra uma linha separada por `;` |

Nenhum precisa de `pip install`.

```bash
cd dia-16-map-e-strings
python original/array_map.py
python original/split_string.py
```

> 💡 Rode `split_string.py` e repare na **linha em branco** no fim: o `;` final gera um pedaço vazio.
> Em dados reais, isso vira uma coluna fantasma. Como você resolveria? (dica: `strip(";")` antes.)

O autor também cita o **chepy**, uma versão em Python do CyberChef (decodifica Base64, URL, binário
etc.). Vale conhecer: `pip install chepy`.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão** e 100% offline (usa os dados do caso).

| Arquivo | O que faz |
|---|---|
| [`br/01_nomes_br.py`](br/01_nomes_br.py) | `nome_br()`: corrige o `title()` (da/de/dos/e minúsculas) e aplica com `map` nos nomes das vítimas |
| [`br/02_sem_acento.py`](br/02_sem_acento.py) | Chave de comparação sem acento (NFKD + `casefold`); `map` + `filter`; o sobrenome do suspeito nas fontes |
| [`br/03_variantes_username.py`](br/03_variantes_username.py) | Gera centenas de usernames prováveis de "Kauã Teixeira Brandão" e `kau.ofertas` → `saidas/variantes_username.txt` |
| [`br/04_split_e_join.py`](br/04_split_e_join.py) | Desmonta `[data hora] autor: mensagem` da conversa do WhatsApp e grava `saidas/conversa_estruturada.csv` |

```bash
cd dia-16-map-e-strings
python br/01_nomes_br.py
python br/03_variantes_username.py
```

**O que você deve ver no caso:** RDAP e WHOIS trazem `Kaua T Brandao`, que vira a mesma chave que
`Kauã Teixeira Brandão` quando você tira os acentos e aceita a inicial do meio. As iniciais **ktb**
batem com o handle `KTB123` do registro. E o sobrenome Brandão reaparece no titular de uma das contas
laranja (`M. R. Brandão Comércio ME`): parentesco? coincidência? Anote como **hipótese**.

## ⚖️ Ética, LGPD e OPSEC

- **Variante não é identidade.** Achar uma conta `kaua.brandao` em uma rede social não prova nada;
  existem homônimos. Só junte perfis com vínculos independentes (mesma foto, mesmo telefone, mesma
  chave PIX, horários coerentes) e registre cada vínculo.
- **Sobrenome igual não é parentesco.** No relatório, escreva "titular com o mesmo sobrenome",
  nunca "parente do suspeito", até que algo confirme.
- Testar centenas de usernames em sites de terceiros é **coleta automatizada**: respeite limites, não
  faça login com conta fantoche para isso e lembre que a requisição sai do seu IP (Dia 12).
- Ao padronizar nomes de vítimas, você está **tratando dados pessoais** (LGPD). Trabalhe numa cópia,
  nunca altere a planilha original da denúncia (Dia 14: cadeia de custódia).

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Detector de grafias compatíveis**: decidir se duas formas de um nome
podem ser a mesma pessoa, aceitando iniciais abreviadas.

## 🔎 Inovação OSINT do dia

**Comparação "aproximada" de nomes com RapidFuzz.** Quando os nomes têm erros de digitação ("Brandao"
× "Brnadão"), a comparação exata falha. A biblioteca **RapidFuzz** (`pip install rapidfuzz`, licença
MIT) calcula semelhança entre textos muito rápido, com funções como `fuzz.ratio` e
`fuzz.token_sort_ratio` (que ignora a ordem das palavras: "Brandão Kauã" × "Kauã Brandão").
Combine com a chave sem acento desta carta: normalize primeiro, compare depois. Na biblioteca padrão,
`difflib.SequenceMatcher` faz algo parecido, só que mais devagar.

## 📚 Para ir além

- Documentação de `map`, `filter` e funções nativas: <https://docs.python.org/pt-br/3/library/functions.html>
- Métodos de string: <https://docs.python.org/pt-br/3/library/stdtypes.html#string-methods>
- `unicodedata` e formas de normalização: <https://docs.python.org/pt-br/3/library/unicodedata.html>
- chepy (citado pelo autor): <https://pypi.org/project/chepy/>
- RapidFuzz: <https://github.com/rapidfuzz/RapidFuzz>

## ✅ Checklist

- [ ] Rodei os cinco scripts originais e entendi o que o `map()` devolve
- [ ] Vi o `title()` errar em "Maria Da Silva" e consertei com `nome_br()`
- [ ] Transformei "Kauã Brandão" em "kaua brandao"
- [ ] Gerei a lista de variantes de username do suspeito
- [ ] Desmontei a conversa do WhatsApp em um CSV
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
