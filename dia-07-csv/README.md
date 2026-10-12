# Dia 7 — CSV

> 🃏 Cartas **7 · 28 · 49**  ·  📘 Original: *Day 7. CSV*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-07-csv/notebook.ipynb)

## 📖 Capítulo 7 — A planilha das vítimas

<!-- historia:inicio -->
Quarta-feira, 10h. A ficha em JSON de ontem já tem duas mentiras registradas: o endereço copiado e o
CNPJ inventado. A Iara abre na tela grande a planilha que a delegacia mandou: **37 denúncias**, uma
por linha, separadas por ponto e vírgula.

— Isso aqui foi digitado por quatro escrivães diferentes, em três turnos. Olha a coluna de cidade.

Você olha. "Belo Horizonte", "belo horizonte", "Belo Horizone". "Contagem" e "contagem".
"Poços de Caldas" e "Pocos de Caldas". Para uma pessoa, é tudo a mesma coisa. Para o computador, são
cidades diferentes.

— Se você contar vítimas por cidade agora, BH vai aparecer dividida em três, e o relatório vai dizer
que o golpe foi menor do que foi. **Dado sujo mente.** E tem mais: some o prejuízo com cuidado.
Centavo errado em relatório de fraude é pergunta do advogado de defesa.

Ela abre outra aba: a lista oficial de municípios do IBGE.

— A gente não inventa nome de cidade. A gente compara com a fonte oficial, corrige o que dá para
corrigir, e marca o resto para um humano olhar. E nunca, **nunca** apaga a coluna original.
<!-- historia:fim -->

## 🎯 Objetivos

- Entender o formato **CSV** e por que no Brasil ele costuma usar `;`.
- Rodar os exemplos originais: escrever, ler, ler uma coluna e converter JSON em CSV.
- Ler a planilha do caso com `csv.DictReader` e somar dinheiro com `Decimal`.
- Baixar os municípios de MG da **API do IBGE** e salvar em CSV que o Excel abre direito.
- Padronizar cidades digitadas à mão com `unicodedata`, apelidos e `difflib`.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
**CSV** (*Comma-Separated Values*) é uma tabela em texto puro: cada linha é uma linha da planilha, e
um separador divide as colunas. Em inglês o separador é a vírgula. No Brasil a vírgula é o separador
**decimal** (R$ 149,90), então as planilhas usam **ponto e vírgula**.

```
id;data;cidade;valor
DEN-001;2025-11-30;Governador Valadares;149.90
```

Três detalhes que derrubam quem está começando:

| Problema | Solução |
|---|---|
| Linhas em branco extras no Windows | `open(..., newline="")` |
| Acentos viram `Ã§` no Excel | grave com `encoding="utf-8-sig"` |
| `0.1 + 0.2 = 0.30000000000000004` | dinheiro com `Decimal`, nunca `float` |

`csv.reader` devolve cada linha como **lista** (`row[0]`). `csv.DictReader` devolve como
**dicionário** (`row["cidade"]`): o código fica legível e não quebra se alguém mudar a ordem das colunas.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/write_csv.py`](original/write_csv.py) | Cria `test.csv` com cabeçalho e uma linha, separados por `;` |
| [`original/read_csv.py`](original/read_csv.py) | Lê `test.csv` e imprime cada linha |
| [`original/read_csv_one_column.py`](original/read_csv_one_column.py) | Imprime só a primeira coluna |
| [`original/json_to_csv.py`](original/json_to_csv.py) | Converte a busca do GitHub (JSON) em CSV: login, perfil e avatar |

```bash
pip install requests
cd dia-07-csv/original
python write_csv.py
python read_csv.py
python read_csv_one_column.py
python json_to_csv.py          # sobrescreve o test.csv com os usuários do GitHub
```

> 💡 Rode de **dentro** de `original/`: os scripts gravam e leem `test.csv` na pasta atual. O autor
> também lembra que, muitas vezes, um conversor online (como o csvjson.com) resolve mais rápido do
> que escrever código. Vale para uma vez; para repetir toda semana, o script ganha.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Amostra offline do IBGE em `dados/`.

| Arquivo | O que faz |
|---|---|
| [`br/01_ler_denuncias.py`](br/01_ler_denuncias.py) | Lê `denuncias.csv` com `DictReader` e `;`, soma com `Decimal` e agrupa por produto e chave PIX |
| [`br/02_ibge_municipios.py`](br/02_ibge_municipios.py) | Baixa os municípios de MG do IBGE e grava `saidas/municipios_mg.csv` (`utf-8-sig`) |
| [`br/03_padroniza_cidades.py`](br/03_padroniza_cidades.py) | **O caso:** padroniza as cidades (acentos, maiúsculas, apelidos, erros de digitação) e grava `saidas/denuncias_padronizadas.csv` |

```bash
cd dia-07-csv
python br/01_ler_denuncias.py
python br/02_ibge_municipios.py
OSINT_OFFLINE=1 python br/03_padroniza_cidades.py     # força o modo offline
```

**O que você deve ver no caso:** prejuízo total de **R$ 54.877,40**. A coluna de cidade cai de
**16 grafias diferentes para 11 cidades reais**, e Belo Horizonte, antes espalhada em três grafias,
aparece com **8 vítimas**, a maior concentração.

> ⚠️ **Campos `null` na API do IBGE.** Alguns municípios vêm com `"microrregiao": null`. Atenção:
> `m.get("microrregiao", {})` **não** resolve, porque a chave existe e o valor é `None`. Use
> `(m.get("microrregiao") or {})` ou uma função que ande pelo caminho checando cada degrau (como
> a `caminho()` do script 02). A amostra offline simula isso em "Belo Oriente".

## ⚖️ Ética, LGPD e OPSEC

- **A planilha das vítimas é o arquivo mais sensível do caso.** Tem nome, CPF e telefone. Não envie
  por e-mail pessoal, não suba em planilha online pública e não cole em ferramentas de IA. Para
  análises que não precisam de identificação, trabalhe com uma cópia sem `nome_vitima`, `cpf` e
  `telefone_contato` (minimização, LGPD art. 6º, III).
- **Nunca sobrescreva o dado bruto.** Acrescente colunas tratadas ao lado (`cidade_padronizada`,
  `metodo`). Assim qualquer pessoa pode conferir o que você mudou, e por quê.
- **Correção automática erra.** `difflib` dá 71% de semelhança entre "uberaba" e "uberlandia": com um corte baixo (0,7), uma
  vítima de Uberaba que digitasse errado poderia "mudar de cidade".
  Os casos "aproximado" precisam de olho humano antes de irem para o relatório.
- **CSV abre fórmulas.** Um campo que começa com `=`, `+`, `-` ou `@` pode virar fórmula no Excel
  (*CSV injection*). Se a planilha vier de fonte não confiável, abra primeiro num editor de texto.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Resumo regional das denúncias**: vítimas e prejuízo por cidade e por
mesorregião, em CSVs com vírgula decimal que o Excel brasileiro soma sem ajuste.

## 🔎 Inovação OSINT do dia

**API de Localidades do IBGE.** É oficial, gratuita e sem cadastro: todos os estados, municípios,
distritos e as duas divisões regionais (micro/mesorregiões e as regiões imediatas/intermediárias de
2017), sempre com o **código IBGE de 7 dígitos**. Esse código é a "chave universal" para cruzar dados
públicos: o ViaCEP devolve ele (Dia 5), o Querido Diário usa ele para filtrar diários oficiais (Dia 9).
Biblioteca Python simples: `urllib.request` + `json` + `csv` (nativos).

## 📚 Para ir além

- API de Localidades do IBGE: <https://servicodados.ibge.gov.br/api/docs/localidades>
- Módulo `csv` do Python (em português): <https://docs.python.org/pt-br/3/library/csv.html>
- Módulo `difflib`: <https://docs.python.org/pt-br/3/library/difflib.html>
- OWASP sobre CSV injection: <https://owasp.org/www-community/attacks/CSV_Injection>

## ✅ Checklist

- [ ] Rodei os quatro scripts originais e entendi por que o `read_csv.py` não separa as colunas
- [ ] Somei o prejuízo com `Decimal`
- [ ] Gerei o CSV de municípios e abri no Excel/LibreOffice sem acento quebrado
- [ ] Padronizei as cidades e conferi os casos "aproximado"
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
