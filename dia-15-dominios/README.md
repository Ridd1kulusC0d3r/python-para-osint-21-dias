# Dia 15 — Coleta de informações de domínio

> 🃏 Cartas **15 · 36 · 57**  ·  📘 Original: *Day 15. Domain information gathering*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-15-dominios/notebook.ipynb)

## 📖 Capítulo 15 — Quem registrou o domínio?

<!-- historia:inicio -->
Sexta-feira, 7h40. A sala do NFA ainda cheira a café requentado quando a Iara joga um post-it amarelo
na sua mesa: **`megaoferta-brasil`**.

— Todo golpe online precisa de um endereço. Pode trocar de nome, de chave PIX, de número de
WhatsApp. Mas alguém, em algum momento, **registrou esse domínio**. E registro deixa data.

Ela puxa uma cadeira.

— Tem gente que ainda chama isso só de WHOIS. Funciona, mas é texto solto, cada servidor responde de
um jeito. Hoje existe o **RDAP**, que devolve tudo em JSON, organizado. Eu quero os dois: um confirma
o outro. Se discordarem, isso também é informação.

Você abre o terminal. A pergunta do dia é simples e poderosa: **quantos dias de vida o site tinha
quando fez a primeira vítima?** Se a resposta for "menos de duas semanas", a Delegada Rita vai
querer saber disso antes do almoço.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar os exemplos originais com `dnspython` e `python-whois`.
- Entender a diferença entre **WHOIS** (texto, porta 43) e **RDAP** (JSON, HTTPS).
- Consultar domínios `.br` no **registro.br** só com a biblioteca padrão.
- Ler registros DNS (A, MX, NS, TXT) sem instalar nada.
- Calcular a idade do domínio do caso e cruzar com as denúncias.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Quando alguém compra um domínio, os dados do registro ficam guardados no **registro** daquela
terminação. Para `.br`, é o **registro.br** (NIC.br). Existem duas formas de perguntar:

| | WHOIS | RDAP |
|---|---|---|
| Transporte | TCP, porta 43 | HTTPS |
| Formato | texto livre, muda de servidor para servidor | JSON padronizado (RFC 9083) |
| Descoberta do servidor | perguntar a `whois.iana.org` | arquivo *bootstrap* da IANA |
| Melhor para | registros antigos, campos específicos do `.br` | automação e scripts |

**DNS** é outra coisa: é a "lista telefônica" que diz para onde o domínio aponta hoje (IP, servidor
de e-mail, servidores de nome). O **registro TXT com SPF** revela quais serviços podem enviar e-mail
em nome do domínio. É ótimo para descobrir o provedor de e-mail de uma empresa.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/dns_info.py`](original/dns_info.py) | Pergunta o registro A (IP) de `osintme.com` com `dnspython` |
| [`original/whois_info.py`](original/whois_info.py) | Consulta o WHOIS de `sector035.nl` com `python-whois` e mostra a data de criação |

```bash
pip install dnspython python-whois
cd dia-15-dominios
python original/dns_info.py
python original/whois_info.py
```

> 💡 Troque os domínios do autor por outros e compare. Experimente `python-whois` com um `.br`
> e veja quais campos ele consegue (ou não) separar.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Cada script tem amostra offline em `dados/`.

| Arquivo | O que faz |
|---|---|
| [`br/01_rdap_br.py`](br/01_rdap_br.py) | Descobre o servidor RDAP pelo bootstrap da IANA e consulta o domínio (padrão: `registro.br`) |
| [`br/02_whois_porta43.py`](br/02_whois_porta43.py) | WHOIS "na unha" via `socket`, com descoberta do servidor na IANA |
| [`br/03_dns_doh.py`](br/03_dns_doh.py) | IPs via `socket` e MX/NS/TXT via DNS sobre HTTPS, com leitura do SPF |
| [`br/04_caso_dominio_fantasma.py`](br/04_caso_dominio_fantasma.py) | **O caso:** RDAP x WHOIS do domínio fictício e idade do site na 1ª denúncia |

```bash
cd dia-15-dominios
python br/01_rdap_br.py
OSINT_OFFLINE=1 python br/02_whois_porta43.py     # força o modo offline
```

**O que você deve ver no caso:** o domínio fictício foi criado em 02/10/2025 e fez a primeira vítima
**10 dias depois**. As duas fontes (RDAP e WHOIS) concordam na data.

## ⚖️ Ética, LGPD e OPSEC

- Dados de registro de pessoa física no `.br` são **dados pessoais** (LGPD). Use só o necessário para
  a finalidade da investigação e registre de onde veio cada informação.
- O titular declarado pode ser **falso ou um laranja**. Registro é pista, nunca prova sozinho.
- O registro.br limita consultas. Não faça varreduras em massa: respeite os limites e o termo de uso.
- Consultas WHOIS/RDAP **não alertam** o dono do domínio. Já acessar o site do suspeito pode deixar
  rastro (seu IP nos logs dele). Veja o Dia 12.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Radar de domínios recém-nascidos**: um script que recebe uma lista de
domínios e marca os que têm menos de 90 dias.

## 🔎 Inovação OSINT do dia

**RDAP com bootstrap automático.** Em vez de decorar qual servidor atende cada terminação, o script
lê `https://data.iana.org/rdap/dns.json` e descobre sozinho. A ICANN encerrou a obrigação de WHOIS
para os gTLDs (como `.com`) em janeiro de 2025, então RDAP virou o caminho oficial para eles. No `.br`,
os dois continuam funcionando. Biblioteca Python simples: `urllib.request` + `json` (nativos).

## 📚 Para ir além

- RDAP do registro.br: <https://rdap.registro.br/>
- Bootstrap RDAP da IANA: <https://data.iana.org/rdap/>
- RFC 9083 (formato de resposta RDAP): <https://www.rfc-editor.org/rfc/rfc9083>
- DNS sobre HTTPS do Google (formato JSON): <https://developers.google.com/speed/public-dns/docs/doh/json>

## ✅ Checklist

- [ ] Rodei os dois scripts originais
- [ ] Consultei um domínio `.br` por RDAP **e** por WHOIS e comparei as datas
- [ ] Descobri o provedor de e-mail de um domínio pelo SPF
- [ ] Calculei a idade do domínio do caso na primeira denúncia
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
