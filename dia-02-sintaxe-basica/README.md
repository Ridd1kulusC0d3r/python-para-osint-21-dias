# Dia 2 — Sintaxe básica: variáveis, condições, listas e laços

> 🃏 Cartas **2 · 23 · 44**  ·  📘 Original: *Day 2. Minimum Basic Syntax*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-02-sintaxe-basica/notebook.ipynb)

## 📖 Capítulo 2 — Triagem

<!-- historia:inicio -->
Quarta-feira, 9h. A Delegada Rita gostou do briefing e devolveu com uma pergunta escrita à caneta na
margem: *"Esses CPFs estão certos? Preciso intimar as vítimas para depor."*

A Iara lê, suspira e gira a cadeira para você.

— Primeira lição de triagem: **vítima digita errado**. Está nervosa, com pressa, preenchendo pelo
celular. Se a gente mandar intimação para um CPF errado, perde semanas.

Ela desenha no quadro onze quadradinhos e circula os dois últimos.

— O CPF tem dois dígitos que **conferem os outros nove**. É uma conta. Pesos, soma, resto da divisão
por onze. Dá para fazer à mão, mas trinta e sete vezes? É para isso que existem laços.

Você começa a digitar. No meio do caminho, ela se lembra de algo e puxa o print do rodapé da loja.

— Aproveita e passa esse CNPJ na mesma lógica. A conta é parecida. E desde julho tem CNPJ com
letra, então já faz o validador para os dois.

Dez minutos depois, o terminal mostra um ❌ vermelho ao lado do CNPJ da MegaOferta. A Iara nem se
surpreende.

— Empresa de verdade não erra o próprio CNPJ. Anota. É a nossa primeira pista.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar os quatro exemplos originais: variável, condição, lista e laço.
- Conhecer os tipos `str`, `int`, `float` e `bool` e converter entre eles.
- Mostrar dinheiro no formato brasileiro (`R$ 1.999,00`).
- Validar **CPF** com laços e condições, entendendo cada passo da conta.
- Validar **CNPJ numérico e alfanumérico** e descobrir a primeira pista do caso.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Quatro peças bastam para começar a automatizar:

| Peça | Para quê | Exemplo |
|---|---|---|
| **Variável** | guardar um valor com um nome | `cpf = "973.091.141-08"` |
| **Condição** (`if` / `elif` / `else`) | fazer uma coisa **ou** outra | `if len(digitos) != 11:` |
| **Lista** | guardar vários valores em ordem | `cpfs = ["973...", "188..."]` |
| **Laço** (`for`) | repetir algo para cada item | `for cpf in cpfs:` |

O que fica "dentro" de um `if` ou de um `for` é marcado pelo **recuo** (4 espaços). Errou o recuo,
o Python reclama ou, pior, faz outra coisa.

**Dígito verificador** é um número calculado a partir dos outros para pegar erros de digitação.
No CPF: multiplique os 9 primeiros dígitos pelos pesos 10, 9, …, 2, some, pegue o resto da divisão
por 11; se o resto for 0 ou 1 o DV é 0, senão é 11 − resto. Repita com 10 dígitos e pesos 11, …, 2.
No CNPJ a ideia é a mesma, com pesos `5 4 3 2 9 8 7 6 5 4 3 2` (e um `6` na frente para o 2º DV). No
**CNPJ alfanumérico**, cada caractere vale `ord(caractere) − 48`: os algarismos continuam valendo eles
mesmos, e as letras vão de A = 17 até Z = 42.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/variable.py`](original/variable.py) | Junta um nome fixo com um sobrenome digitado via `input()` |
| [`original/condition.py`](original/condition.py) | Pergunta a idade e responde com `if`/`elif` |
| [`original/list.py`](original/list.py) | Cria uma lista, usa `append()` e acessa um item pelo índice |
| [`original/loop.py`](original/loop.py) | Percorre a lista com `for` e conta de 0 a 19 com `range()` |

```bash
cd dia-02-sintaxe-basica/original
python variable.py
python condition.py
python list.py
python loop.py
```

O autor roda os scripts **de dentro da pasta** (`cd`), em vez de passar o caminho completo. As duas
formas funcionam. `variable.py` e `condition.py` usam `input()`: o script para e espera você digitar.

> 💡 Teste o `condition.py` com a idade **27**. Nada acontece! Nem `> 27` nem `< 27` é verdadeiro.
> Como você resolveria com um `else`?

## 🇧🇷 Nível 2 — Camada Brasil

| Arquivo | O que faz |
|---|---|
| [`br/01_variaveis_br.py`](br/01_variaveis_br.py) | Tipos de dado, conversões, o erro `"37" + 1` e dinheiro em `R$ 1.999,00` |
| [`br/02_valida_cpf.py`](br/02_valida_cpf.py) | Valida um CPF mostrando cada multiplicação, soma e resto |
| [`br/03_triagem_cpfs.py`](br/03_triagem_cpfs.py) | **O caso:** valida 10 CPFs das denúncias e conta válidos e inválidos |
| [`br/04_valida_cnpj.py`](br/04_valida_cnpj.py) | **O caso:** valida CNPJ numérico e alfanumérico; o do rodapé da loja falha |

```bash
cd dia-02-sintaxe-basica
python br/01_variaveis_br.py
python br/02_valida_cpf.py
python br/03_triagem_cpfs.py
python br/04_valida_cnpj.py
```

Nenhum usa internet. No `02`, troque o parâmetro `CPF` para testar outros números (fictícios!).

**O que você deve ver no caso:** dos 10 CPFs da amostra, **7 são válidos e 3 inválidos** (DEN-007,
DEN-013 e DEN-014): é para pedir à equipe que confira os documentos originais. E o CNPJ do rodapé,
`48.217.093/0001-30`, é **inválido**: a conta dá final `37`, e não `30`.

## ⚖️ Ética, LGPD e OPSEC

- **CPF é dado pessoal** (LGPD, art. 5º, I). Em investigação, trate só os necessários para a finalidade e
  nunca publique listas de CPFs, nem "de exemplo". Todos os deste repositório são fictícios.
- **Válido não é existente.** O validador só confere a matemática. Quem diz se o CPF existe e de quem
  é, é a Receita Federal, pelos canais legais.
- **Não "conserte" documentos para consultá-los.** Se um CPF ou CNPJ está inválido, o número com o DV
  "corrigido" provavelmente é **de outra pessoa ou empresa**. Consultá-lo é tratar dado de um terceiro
  sem motivo. O certo é voltar à fonte (a vítima, o documento original).
- **CPF inválido numa denúncia não é indício contra a vítima.** É, quase sempre, erro de digitação.
- **CNPJ inválido no site de uma loja é indício**, sim: empresas reais copiam o CNPJ do cartão do CNPJ.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Classificador de documentos**: uma lista misturada (CPFs, CNPJs,
telefone) e, para cada item, o tipo, a validade e os dígitos corretos.

## 🔎 Inovação OSINT do dia

**CNPJ alfanumérico em vigor.** Desde **julho de 2026**, a Receita Federal (Instrução Normativa RFB
nº 2.229/2024) pode emitir CNPJs com **letras e números** nas 12 primeiras posições, mantendo os 2
dígitos verificadores numéricos. O primeiro saiu em **31/07/2026**, para uma filial do Banco do
Brasil: `00.000.000/E08G-12` (o `br/04` usa esse número público como exemplo e ele passa na conta).
CNPJs antigos continuam valendo, e números só com algarismos ainda podem ser emitidos. Para OSINT isso quebra muita coisa:
regex que só aceita `\d{14}`, planilhas que guardam CNPJ como número (e somem com as letras e os
zeros à esquerda) e validadores antigos. A boa notícia: a conta do DV é a mesma, trocando `int(c)`
por `ord(c) - 48`. Biblioteca simples: nenhuma, só a função nativa `ord()`. Confira sempre a
documentação oficial da Receita antes de usar o validador em produção.

## 📚 Para ir além

- Tutorial oficial: controle de fluxo (`if`, `for`, `range`): <https://docs.python.org/pt-br/3/tutorial/controlflow.html>
- Listas: <https://docs.python.org/pt-br/3/tutorial/datastructures.html>
- Perguntas e respostas da Receita sobre o CNPJ alfanumérico: <https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-e-respostas/cnpj/cnpj-alfanumerico.pdf>
- Notícia do primeiro CNPJ alfanumérico (Ministério da Fazenda): <https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/julho/receita-federal-gera-o-primeiro-cnpj-em-formato-alfanumerico/>
- LGPD (Lei 13.709/2018): <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>

## ✅ Checklist

- [ ] Rodei os quatro scripts originais e respondi aos `input()`
- [ ] Descobri o que acontece no `condition.py` com a idade 27
- [ ] Entendi a conta do CPF olhando as multiplicações do `br/02`
- [ ] Rodei a triagem e anotei quais denúncias precisam de conferência
- [ ] Vi o CNPJ do rodapé falhar na validação
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
