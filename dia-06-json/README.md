# Dia 6 — JSON

> 🃏 Cartas **6 · 27 · 48**  ·  📘 Original: *Day 6. JSON*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-06-json/notebook.ipynb)

## 📖 Capítulo 6 — O CNPJ do rodapé

<!-- historia:inicio -->
Terça-feira, 8h50. Na parede do NFA, ao lado do mapa de BH, já tem um post-it novo: **"CEP = Praça
Sete. Endereço copiado."** A Iara bate com a caneta no rodapé da vitrine, logo acima do endereço.

— Agora o CNPJ. **48.217.093/0001-30.** Loja que mostra CNPJ no rodapé parece séria. A vítima vê o
número e relaxa. Quase ninguém confere.

Você abre a BrasilAPI de novo, pronto para consultar, mas ela segura sua mão.

— Calma. Lembra do Dia 2? Antes de perguntar a qualquer servidor, pergunte ao **dígito
verificador**. Se o número nem é um CNPJ possível, você não gasta consulta, não deixa seu IP em log
nenhum e já tem a resposta.

O validador roda em menos de um segundo. O final deveria ser outro. **O CNPJ do rodapé não existe.**
Não é empresa irregular, não é empresa baixada: é um número inventado.

— Isso vai para a ficha — diz a Iara. — E a ficha vai ser em **JSON**, porque daqui a duas semanas
outro script vai ler tudo isso sozinho. Ah, e quando for consultar um CNPJ de verdade, use o do
Banco do Brasil para treinar. A resposta da API é um labirinto de chaves, listas e sócios. Aprenda a
andar nele antes de precisar correr.
<!-- historia:fim -->

## 🎯 Objetivos

- Entender a estrutura de um JSON: **objetos** (`{}` → dicionário) e **listas** (`[]` → lista).
- Rodar os exemplos originais: ler um campo e ler o mesmo campo de toda uma lista.
- Navegar na resposta de CNPJ da BrasilAPI com `.get()`, inclusive no quadro de sócios (`qsa`).
- Validar um CNPJ (numérico e alfanumérico) **antes** de consultar.
- Salvar e reler uma ficha de evidências com `json.dump` / `json.load`.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
**JSON** (*JavaScript Object Notation*) é o formato que quase toda API usa para devolver dados. Ele
tem só seis tipos, e cada um vira um tipo do Python:

| No JSON | No Python | Exemplo |
|---|---|---|
| objeto `{ }` | `dict` | `{"uf": "MG"}` |
| lista `[ ]` | `list` | `["a", "b"]` |
| texto `"…"` | `str` | `"ATIVA"` |
| número | `int` / `float` | `1999.0` |
| `true` / `false` | `True` / `False` | |
| `null` | `None` | |

Para chegar num dado, você "anda" pelo caminho: `dados["qsa"][0]["nome_socio"]` = *a lista `qsa` →
o primeiro item → o campo `nome_socio`*. Se algum degrau faltar, colchetes quebram com `KeyError`
ou `IndexError`; por isso usamos `dados.get("qsa", [])`.

O JSON **não conhece** datas, `Decimal` nem conjuntos. Na hora de salvar, converta: data vira texto
ISO (`"2025-10-12"`), dinheiro vira texto (`"54877.40"`), conjunto vira lista.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/read_one_field.py`](original/read_one_field.py) | Mostra o total de resultados e o link do primeiro perfil da busca no GitHub |
| [`original/read_list_of_fields.py`](original/read_list_of_fields.py) | Percorre a lista `items` e imprime o link de cada perfil |

```bash
pip install requests
cd dia-06-json
python original/read_one_field.py
python original/read_list_of_fields.py
```

> 💡 Repare no `len(...) - 1` do segundo script: ele faz o laço **pular o último perfil**. Não mexemos
> no original (é a regra), mas é um ótimo exercício: descubra por quê e corrija numa cópia sua.
> O autor também recomenda ferramentas online como <https://jsonpathfinder.com> para descobrir o
> "caminho" até um campo num JSON grande.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Cada script tem amostra offline em `dados/`.

| Arquivo | O que faz |
|---|---|
| [`br/01_cnpj_brasilapi.py`](br/01_cnpj_brasilapi.py) | Consulta o CNPJ público do Banco do Brasil e navega por razão social, situação, CNAE, município e sócios |
| [`br/02_caso_cnpj_rodape.py`](br/02_caso_cnpj_rodape.py) | **O caso:** valida o CNPJ do rodapé antes de consultar; inválido → registra a pista, sem gastar consulta |
| [`br/03_ficha_json.py`](br/03_ficha_json.py) | Monta a ficha de evidências, salva em `saidas/ficha_evidencias.json` e confere a releitura |

```bash
cd dia-06-json
python br/01_cnpj_brasilapi.py
OSINT_OFFLINE=1 python br/02_caso_cnpj_rodape.py     # força o modo offline
python br/03_ficha_json.py
```

**O que você deve ver no caso:** `48.217.093/0001-30` **falha no dígito verificador**. Não é uma
empresa irregular: o número simplesmente não pode existir.

> 🆕 **CNPJ alfanumérico.** A partir de julho de 2026 a Receita Federal começou a emitir CNPJs com
> **letras** nas 12 primeiras posições (os dois dígitos verificadores continuam numéricos). O cálculo
> é o mesmo módulo 11, com cada caractere valendo `ord(c) - 48` (`"0"`→0, `"A"`→17). Os scripts deste
> dia já aceitam os dois formatos. Os CNPJs antigos continuam valendo.

## ⚖️ Ética, LGPD e OPSEC

- **CNPJ é público, sócio é gente.** A ficha cadastral de uma empresa é pública por lei, mas os sócios
  pessoas físicas são titulares de dados pela LGPD. Use nome de sócio só quando ele for relevante para
  a investigação, e nunca para expor alguém sem necessidade.
- **Nunca "conserte" o CNPJ do suspeito.** Trocar os dígitos finais até "dar válido" pode apontar para
  uma empresa real e inocente. Número inválido é pista, e a pista é exatamente essa.
- **Validar antes de consultar** economiza cota e reduz rastro: cada consulta registra seu IP no
  servidor da API (e, em sites de terceiros, pode chegar ao conhecimento do alvo).
- **Guarde a origem** de cada dado no próprio JSON (`"fonte": …`, `"registrado_em": …`). Uma ficha sem
  origem não serve como evidência.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Fichário de CNPJs do caso**: varre os arquivos do caso, valida cada CNPJ
encontrado, consulta só os válidos e grava um fichário JSON com a origem de cada número.

## 🔎 Inovação OSINT do dia

**CNPJ alfanumérico.** A Receita Federal (Instrução Normativa RFB nº 2.229/2024) definiu que, a partir
de julho de 2026, novas inscrições podem ter letras e números nas 12 primeiras posições. Para OSINT,
isso quebra regex e validadores antigos que só aceitam dígitos: um CNPJ legítimo novo seria
descartado como "inválido". A correção cabe numa linha (`ord(c) - 48`) e já está nos scripts. Biblioteca
Python simples: `re` (nativo) para achar candidatos; a conta é Python puro.

## 📚 Para ir além

- Documentação da rota de CNPJ da BrasilAPI: <https://brasilapi.com.br/docs#tag/CNPJ>
- Módulo `json` do Python (em português): <https://docs.python.org/pt-br/3/library/json.html>
- Notícia (Fenacon) sobre o CNPJ alfanumérico: <https://fenacon.org.br/noticias/cnpj-tera-letras-e-numeros-a-partir-de-julho-de-2026/>
- Página da Receita Federal (busque "CNPJ alfanumérico"): <https://www.gov.br/receitafederal/>
- JSON Path Finder (recomendado pelo autor): <https://jsonpathfinder.com>

## ✅ Checklist

- [ ] Rodei os dois scripts originais e entendi o `- 1` do laço
- [ ] Naveguei pela ficha de CNPJ do Banco do Brasil até a lista de sócios
- [ ] Validei o CNPJ do rodapé **antes** de consultar
- [ ] Salvei e reli a ficha de evidências em JSON
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
