# Dia 11 — Expressões regulares

> 🃏 Cartas **11 · 32 · 53**  ·  📘 Original: *Day 11. Regular expressions*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-11-regex/notebook.ipynb)

## 📖 Capítulo 11 — A conversa

<!-- historia:inicio -->
Ontem a vitrine entregou um e-mail esquecido num comentário. Hoje a Iara chega com algo mais
quente: uma vítima exportou a conversa inteira com o "Kau" pelo WhatsApp e mandou o `.txt` para a
delegacia.

— São só catorze linhas — você diz, aliviado.

— Hoje. — Ela sorri. — Semana que vem serão catorze mil, de vinte vítimas diferentes. Ninguém lê isso
com marca-texto. Você vai ensinar o computador a reconhecer **formatos**: CPF tem cara de CPF, chave PIX
aleatória tem cara de UUID, telefone tem DDD.

Ela escreve no quadro `\d{3}\.\d{3}\.\d{3}-\d{2}` e espera.

— Parece xingamento em código, eu sei. Mas lê comigo: três dígitos, ponto, três dígitos, ponto, três
dígitos, hífen, dois dígitos.

Você roda o primeiro teste e a tela se enche de achados: três chaves PIX, dois CNPJs, dois e-mails.
A Iara aponta para os CNPJs.

— Agora a pegadinha. A regex diz que **parece** um CNPJ. Quem diz se **é** um CNPJ é o dígito
verificador. Lembra do Dia 2? Junta as duas coisas e me diz: o "CNPJ do sócio" existe?
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar o exemplo original que extrai e-mails de uma página com `re.findall`.
- Ler uma regex pedaço por pedaço: `\d`, `{n}`, `?`, `+`, `[ ]`, `( )`, `|`.
- Escrever regex **comentadas** com `re.VERBOSE` para CPF, CNPJ (inclusive alfanumérico), telefone,
  CEP, placa e chave PIX.
- Extrair entidades da conversa do caso e saber em que linha e de quem veio cada uma.
- Combinar regex + dígito verificador para eliminar falsos positivos.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Uma **expressão regular** (regex) é um "molde" de texto. Em vez de procurar a palavra exata
`31988880101`, você procura **qualquer coisa com o formato** de um telefone.

| Peça | Significa | Exemplo | Casa com |
|---|---|---|---|
| `\d` | um dígito | `\d\d` | `31` |
| `{n}` | repetir n vezes | `\d{5}` | `30130` |
| `?` | opcional | `-?` | `-` ou nada |
| `+` | uma ou mais vezes | `[a-z]+` | `kau` |
| `[ ]` | um dos caracteres | `[.-]` | `.` ou `-` |
| `\b` | borda de palavra | `\bBRA` | `BRA` no começo de palavra |
| `(?P<nome>…)` | grupo com nome | `(?P<ddd>\d{2})` | guarda `31` em `m["ddd"]` |

No Python: `re.findall` devolve a lista de achados; `re.finditer` devolve também **onde** cada um
está; `re.fullmatch` exige que o texto **inteiro** case (ótimo para validar um campo).

**Regra de ouro:** regex reconhece **formato**, não **verdade**. `111.111.111-11` tem formato de
CPF, mas não é válido. Por isso, em OSINT, usamos a regex para achar **candidatos** e depois um
teste extra (dígito verificador, consulta a uma base) para confirmar.

**CNPJ alfanumérico:** desde 31 de julho de 2026 a Receita Federal emite, gradualmente, CNPJs com letras
nas 12 primeiras posições (ex.: `12.ABC.345/01DE-35`). Os dois dígitos verificadores continuam
numéricos, e o cálculo é o mesmo, com cada caractere valendo `ord(c) − 48`. Regex antiga que só aceita
`\d` vai deixar esses CNPJs passarem despercebidos.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/extract_emails.py`](original/extract_emails.py) | Baixa uma página da CleanTalk e lista tudo que parece e-mail com `re.findall` |

```bash
pip install requests
cd dia-11-regex
python original/extract_emails.py
```

> 💡 Repare no comentário `# 💬` sobre `[a-zA-Z0-9-_.]`: o trecho `9-_` vira um **intervalo** e aceita
> mais caracteres do que parece. Coloque o hífen no fim dos colchetes (`[a-zA-Z0-9_.-]`) e compare.
> O autor também recomenda praticar regex na busca do Google Docs/Planilhas antes de ir para o código.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão** e 100% offline.

| Arquivo | O que faz |
|---|---|
| [`br/01_padroes_br.py`](br/01_padroes_br.py) | Regex comentadas de CPF, CNPJ (numérico e alfanumérico), telefone, CEP, placas, PIX e e-mail, com bateria de testes |
| [`br/02_extrai_conversa.py`](br/02_extrai_conversa.py) | Aplica tudo em `caso/dados/conversa_whatsapp.txt`: tabela entidade → ocorrências, linha e autor |
| [`br/03_regex_mais_validacao.py`](br/03_regex_mais_validacao.py) | Regex encontra, dígito verificador confirma: os CNPJs da conversa são inválidos |

```bash
cd dia-11-regex
python br/01_padroes_br.py
python br/02_extrai_conversa.py
python br/03_regex_mais_validacao.py
```

**O que você deve ver no caso:** 3 chaves PIX diferentes (a da vitrine, a "do frete" e a "do sócio"),
2 e-mails, o telefone do vendedor `+55 31 9 8888-0101` e **dois CNPJs inválidos**: o do rodapé
(`48.217.093/0001-30`) e o "do sócio" (`31.560.427/0001-71`).

## ⚖️ Ética, LGPD e OPSEC

- **Extrair em massa é tratar dado pessoal em massa.** Uma regex de CPF passada num vazamento devolve
  milhares de titulares. Aplique só em material que você tem base legal para analisar e guarde apenas o
  necessário para a finalidade.
- **Vítima também aparece na extração.** O CPF da conversa é da cliente, não do golpista. No relatório,
  separe "dados do investigado" de "dados de vítimas" e minimize (mascare) os das vítimas.
- **Falso positivo pode acusar inocente.** Um número que "parece CNPJ" pode ser um código de rastreio.
  Sempre valide (dígito verificador, fonte oficial) antes de afirmar qualquer coisa.
- **Não cole conversas reais em sites de "testar regex" online.** Teste com dados inventados (como os
  do script 01) e rode o material real só na sua máquina.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **O elo telefônico**: normalize todos os telefones de todas as fontes do
caso para um formato único e descubra quais números ligam a vitrine, a conversa e as vítimas.

## 🔎 Inovação OSINT do dia

**`iocextract`: regex prontas para indicadores de ameaça.** Em relatórios de segurança, URLs e IPs
costumam vir "desarmados" (`hxxp://exemplo[.]com`, `10[.]0[.]0[.]1`) para ninguém clicar sem querer.
A biblioteca Python `iocextract` (InQuest) já traz regex para achar URLs, IPs, e-mails e hashes nesse
formato e ainda "rearma" o texto:

```python
# pip install iocextract
import iocextract
texto = "Golpe em hxxps://megaoferta-brasil[.]example/pix"
print(list(iocextract.extract_urls(texto, refang=True)))
```

Boa companhia para os padrões brasileiros deste dia, que ela não cobre (CPF, CNPJ, PIX).

## 📚 Para ir além

- Módulo `re` (documentação oficial): <https://docs.python.org/pt-br/3/library/re.html>
- HOWTO de expressões regulares: <https://docs.python.org/pt-br/3/howto/regex.html>
- Testar regex de forma visual (use só dados inventados): <https://regex101.com/>
- Ministério da Fazenda, "Receita Federal gera o primeiro CNPJ em formato alfanumérico" (jul/2026): <https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/julho/receita-federal-gera-o-primeiro-cnpj-em-formato-alfanumerico/>
- iocextract: <https://github.com/InQuest/iocextract>

## ✅ Checklist

- [ ] Rodei o script original e corrigi o intervalo `9-_` da regex
- [ ] Todos os testes do `01_padroes_br.py` passaram
- [ ] Extraí as entidades da conversa e sei qual autor disse cada uma
- [ ] Confirmei que os dois CNPJs do vendedor são inválidos
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
