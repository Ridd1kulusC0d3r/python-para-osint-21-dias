# Dia 5 — Requisições HTTP e APIs

> 🃏 Cartas **5 · 26 · 47**  ·  📘 Original: *Day 5. Handling HTTP requests and working with APIs*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-05-http-e-apis/notebook.ipynb)

## 📖 Capítulo 5 — O endereço da loja

<!-- historia:inicio -->
Segunda-feira, 9h15. Os depoimentos que você leu ontem estão impressos e grampeados sobre a mesa,
com marca-texto amarelo em cada chave PIX. A Iara pega a folha de cima e aponta o rodapé da loja,
copiado por uma das vítimas: **Av. Afonso Pena, 1500 — Centro — CEP 30130-010**.

— Golpista adora endereço. Endereço passa confiança. Mas CEP não mente: cada número aponta para um
lugar oficial, e existem APIs públicas que respondem isso em milissegundos.

Ela escreve duas URLs no quadro branco: **BrasilAPI** e **ViaCEP**.

— Você vai perguntar às duas. Se concordarem, ótimo. Se uma cair, a outra cobre. E repare: quando a
gente conversa com uma API, ela responde com um **status**, uns **cabeçalhos** e o **corpo**. Muita
gente só olha o corpo e perde metade da história.

Você roda o primeiro pedido. A resposta volta antes de você soltar a tecla Enter, e o logradouro
que a API devolve **não é** o que está escrito no rodapé. O CEP cai no coração do Centro de Belo
Horizonte: ponto de ônibus, comércio de rua, gente passando. Nada parecido com o galpão de onde
sairiam centenas de iPhones a preço de banana.

— Anota — diz a Iara. — "Endereço declarado não bate com o CEP." Não é prova, é pista. Mas é a
primeira inconsistência documentada da loja.
<!-- historia:fim -->

## 🎯 Objetivos

- Entender o que acontece num pedido HTTP: **método**, **URL**, **status**, **cabeçalhos** e **corpo**.
- Rodar o exemplo original com `requests` e a API do GitHub.
- Fazer o mesmo pedido só com `urllib.request` (biblioteca padrão).
- Ler os cabeçalhos de **rate limit** e tratar os erros **404** e **429**.
- Consultar CEPs na **BrasilAPI** e no **ViaCEP** e comparar as duas fontes.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Quando o navegador abre uma página, ele manda um **pedido** (requisição) ao servidor e recebe uma
**resposta**. Um script faz exatamente a mesma coisa, só que sem janela.

| Parte | Exemplo | Para que serve |
|---|---|---|
| Método | `GET` | "me entregue isto" (o mais comum em OSINT) |
| URL | `https://viacep.com.br/ws/30130010/json/` | o endereço do recurso; parâmetros vêm depois do `?` |
| Status | `200`, `404`, `429` | 2xx deu certo · 4xx erro de quem pediu · 5xx erro do servidor |
| Cabeçalhos | `User-Agent`, `x-ratelimit-remaining` | metadados: quem pede, quanto ainda pode pedir… |
| Corpo | `{"logradouro": "…"}` | os dados em si (HTML, JSON, CSV…) |

Uma **API** é um "balcão de atendimento" para programas: em vez de uma página bonita, o servidor
devolve dados organizados, quase sempre em **JSON**. Muitas APIs públicas brasileiras não pedem
cadastro (BrasilAPI, ViaCEP, IBGE). Outras exigem uma **chave** e limitam quantos pedidos você faz
por hora: é o **rate limit**. Passou do limite, vem o **429 Too Many Requests**.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/api_request.py`](original/api_request.py) | Busca usuários com "javascript" na API do GitHub usando `requests` e imprime o JSON |

```bash
pip install requests
cd dia-05-http-e-apis
python original/api_request.py
```

> 💡 O autor recomenda testar APIs primeiro numa ferramenta online (como o reqbin.com) antes de
> escrever código. Vale a dica: você enxerga status e cabeçalhos sem programar nada. Ele também mantém
> uma lista com mais de cem APIs úteis para OSINT: <https://github.com/cipher387/API-s-for-OSINT>.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Cada script tem amostra offline em `dados/`.

| Arquivo | O que faz |
|---|---|
| [`br/01_github_stdlib.py`](br/01_github_stdlib.py) | O mesmo pedido do original com `urllib`, mostrando status e cabeçalhos de rate limit |
| [`br/02_cep_brasilapi.py`](br/02_cep_brasilapi.py) | Consulta um CEP na BrasilAPI v2 e lê os campos aninhados (coordenadas) |
| [`br/03_viacep.py`](br/03_viacep.py) | Consulta o ViaCEP, compara com a BrasilAPI e trata CEP inexistente (`{"erro": "true"}`) |
| [`br/04_caso_cep_rodape.py`](br/04_caso_cep_rodape.py) | **O caso:** extrai o CEP do rodapé da vitrine, trata 404/429 e cruza com o que a loja promete |

```bash
cd dia-05-http-e-apis
python br/01_github_stdlib.py
OSINT_OFFLINE=1 python br/04_caso_cep_rodape.py     # força o modo offline
```

**O que você deve ver no caso:** o script compara o logradouro que a loja **declara** no rodapé
("Av. Afonso Pena, 1500") com o logradouro que a API **devolve** para o CEP `30130-010`. Na amostra
offline (montada à mão, não baixada ao vivo) o CEP aparece como **Praça Sete de Setembro**, no Centro
de BH. Rode com internet e confira o que a API responde hoje: se o logradouro for outro que não o
declarado, essa **divergência** é a pista do capítulo, e vai para o relatório com a fonte e a hora.

> ⚠️ **Armadilha clássica:** o ViaCEP responde **HTTP 200** mesmo quando o CEP não existe; o aviso vem
> no corpo, como `{"erro": "true"}` (versões antigas mandavam o booleano `true`). Já a BrasilAPI
> responde **404**. Duas APIs, dois jeitos de dizer "não achei": seu código precisa entender os dois.

## ⚖️ Ética, LGPD e OPSEC

- **CEP não é dado pessoal**, mas CEP + número + nome de uma pessoa é. Ao consultar endereços de
  vítimas, guarde só o necessário para a finalidade do caso (LGPD, art. 6º: finalidade e necessidade).
- **Rate limit é um contrato.** Não rode laços sem pausa contra APIs gratuitas: você derruba um serviço
  que todo o país usa e ainda pode ter seu IP bloqueado. Use `time.sleep` e respeite o `Retry-After`.
- **Toda consulta deixa rastro.** O servidor da API registra seu IP, horário e o que você perguntou.
  APIs públicas de CEP são inofensivas, mas uma API que **pertence ao alvo** (o site do golpista, por
  exemplo) vê você chegando. Isso é assunto do Dia 12.
- **Leia os termos de uso.** Algumas APIs proíbem uso comercial ou armazenamento em massa.
- **Nunca coloque chaves de API no código** que vai para o GitHub. Use variáveis de ambiente.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Verificador de CEPs em lote**: consulta uma lista de CEPs em duas APIs,
com fonte reserva, pausa entre pedidos e CSV com a fonte de cada resposta.

## 🔎 Inovação OSINT do dia

**BrasilAPI.** Projeto aberto, mantido pela comunidade, que reúne várias fontes públicas brasileiras
numa API só e gratuita: CEP, CNPJ, bancos, DDD, feriados nacionais, tabela FIPE, entre outras. A rota
de CEP v2 pergunta a mais de um provedor e devolve, no campo `service`, **qual deles respondeu**:
ótimo para registrar a origem da informação no relatório. Biblioteca Python simples: `urllib.request` +
`json` (nativos). Amanhã usamos a mesma API para consultar CNPJ.

## 📚 Para ir além

- BrasilAPI (documentação): <https://brasilapi.com.br/docs>
- ViaCEP (documentação): <https://viacep.com.br/>
- Limites de uso da API REST do GitHub: <https://docs.github.com/pt/rest/using-the-rest-api/rate-limits-for-the-rest-api>
- Códigos de status HTTP explicados (MDN, em português): <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status>
- Lista de APIs para OSINT do cipher387: <https://github.com/cipher387/API-s-for-OSINT>

## ✅ Checklist

- [ ] Rodei o script original com `requests`
- [ ] Fiz o mesmo pedido com `urllib` e li os cabeçalhos de rate limit
- [ ] Consultei um CEP na BrasilAPI e no ViaCEP e comparei
- [ ] Vi a diferença entre "HTTP 404" e "HTTP 200 com erro no corpo"
- [ ] Descobri o que é o endereço do rodapé da loja
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
