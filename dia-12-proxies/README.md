# Dia 12 — Proxies, User-Agent e OPSEC

> 🃏 Cartas **12 · 33 · 54**  ·  📘 Original: *Day 12. Proxies*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-12-proxies/notebook.ipynb)

## 📖 Capítulo 12 — Disfarce digital

<!-- historia:inicio -->
Você chega animado: a conversa de ontem deu três chaves PIX e um telefone. A próxima ideia parece
óbvia: abrir o Instagram e o Telegram que estavam no rodapé da loja e ver o que o Kau anda postando.

A Iara segura a sua mão antes do clique.

— Pergunta rápida: quando você abre uma página, quem mais fica sabendo?

Você hesita. Ela abre o log de acesso de um servidor de testes do NFA e aponta uma linha:
`"GET / HTTP/1.1" 200 "Python-urllib/3.12"`, com o IP do prédio da delegacia.

— Esse foi o seu script de ontem, consultando o gov.br. Para um site do governo, tudo bem: você é
quem diz ser. Agora imagina essa linha no log do golpista. Ele descobre que alguém está olhando, de
onde e com que ferramenta. Uma hora depois o perfil some.

Ela escreve três palavras no quadro: **IP · cabeçalhos · hábitos**.

— Disfarce não é para enganar a vítima nem burlar a lei. É para não avisar o alvo. Hoje você vai
descobrir tudo o que a sua máquina entrega sem pedir licença, e montar o checklist que todo mundo aqui
roda antes de uma coleta.
<!-- historia:fim -->

## 🎯 Objetivos

- Rodar os exemplos originais: um proxy, uma lista de proxies e um User-Agent personalizado.
- Entender o que é um **proxy** e o que ele esconde (e o que **não** esconde).
- Descobrir o seu IP público e passar por um proxy com `urllib.request.ProxyHandler`.
- Ver o User-Agent `Python-urllib/3.x` que denuncia o robô e trocá-lo.
- Rodar um checklist de **OPSEC** (segurança operacional) antes de qualquer coleta.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Todo pedido que sai do seu computador leva um **remetente** (o seu IP) e uma "carta de
apresentação" (os **cabeçalhos HTTP**). O site guarda os dois no log.

```
Sem proxy:   você (IP 203.0.113.45) ───────────────────────▶ site   (o site vê 203.0.113.45)
Com proxy:   você ───▶ proxy (IP 198.51.100.10) ───────────▶ site   (o site vê 198.51.100.10)
```

| O que vaza | Exemplo | Como reduzir |
|---|---|---|
| IP | o endereço da sua conexão | proxy ou VPN confiável |
| User-Agent | `Python-urllib/3.12`, `python-requests/2.32` | cabeçalho `User-Agent` |
| Idioma e fuso | `Accept-Language: pt-BR`, fuso -03:00 | coerência com o disfarce |
| Hábitos | 200 pedidos em 10 s, sempre às 9h | pausas, volume baixo |

Os proxies se dividem pelo que contam ao site: **transparente** (repassa o seu IP em
`X-Forwarded-For`), **anônimo** (esconde o IP, mas avisa que é proxy com `Via`) e **elite** (não
avisa nada). Em todos os casos, **o dono do proxy vê todo o seu tráfego**. Por isso proxy gratuito de
lista da internet é perigoso: você não sabe quem está do outro lado.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/simple_proxy.py`](original/simple_proxy.py) | Faz um pedido à CleanTalk passando por um proxy fixo |
| [`original/proxy_permulation.py`](original/proxy_permulation.py) | Tenta uma lista de proxies, um por um, e imprime "No" para os que falham |
| [`original/useragent.py`](original/useragent.py) | Envia um User-Agent de navegador (Chrome 45) para o whatismybrowser.com |

```bash
pip install requests
cd dia-12-proxies
python original/useragent.py
```

> ⚠️ Os proxies escritos no código do autor são de 2023 e quase certamente não respondem mais (e os
> `someproxyN.com` são só marcadores). O autor sugere trocar por proxies de listas públicas; neste
> repositório **não recomendamos** isso (veja a ética abaixo). Use um proxy que você controle, ou só
> leia o código para entender a lógica. O `useragent.py` pode receber um bloqueio anti-robô do site;
> se acontecer, troque a URL por `https://httpbin.org/headers`.

## 🇧🇷 Nível 2 — Camada Brasil

Tudo com a **biblioteca padrão**. Cada script com internet tem amostra offline em `dados/`.

| Arquivo | O que faz |
|---|---|
| [`br/01_meu_ip.py`](br/01_meu_ip.py) | Pergunta o IP público ao ipify; usa o proxy da variável `PROXY_URL`, se existir (sem imprimir a senha) |
| [`br/02_o_que_eu_revelo.py`](br/02_o_que_eu_revelo.py) | Compara, no httpbin, os cabeçalhos do pedido "cru" e do personalizado |
| [`br/03_checklist_opsec.py`](br/03_checklist_opsec.py) | Checa proxy, UA, fuso e idioma; imprime o checklist humano e grava o registro |

```bash
cd dia-12-proxies
python br/01_meu_ip.py
PROXY_URL="http://meu-proxy.exemplo:3128" python br/01_meu_ip.py   # compare os IPs
python br/02_o_que_eu_revelo.py
python br/03_checklist_opsec.py
```

**O que você deve ver:** no pedido cru, `User-Agent: Python-urllib/3.x`. É assim que o NFA apareceria
no log do golpista. Com o UA personalizado, o pedido parece de navegador, mas **o IP continua o
mesmo**: só o proxy muda isso.

## ⚖️ Ética, LGPD e OPSEC

- **Proxy gratuito desconhecido lê o seu tráfego.** Pode registrar o que você acessa, injetar conteúdo
  e até capturar credenciais. Muitos são máquinas invadidas: usar um deles é usar o computador de uma
  vítima sem ela saber. Em investigação, use só infraestrutura contratada ou da instituição.
- **Contornar bloqueio pode ser crime.** Trocar de IP para driblar limite de uso, captcha ou banimento
  pode violar termos de uso e, dependendo do caso, configurar acesso indevido (art. 154-A do Código
  Penal). Se um site te bloqueou, a resposta é diminuir o ritmo ou pedir os dados pela via legal.
- **Contas "fantoche"** (perfis de investigação) exigem autorização da instituição, não podem se
  passar por pessoa real e quase sempre violam os termos das plataformas. É decisão da equipe e da
  chefia, nunca individual.
- **Disfarce não autoriza interação.** Observar é diferente de conversar com o alvo, que pode
  configurar outra coisa (e atrapalhar a investigação).
- **Registre a sua configuração.** O log do script 03 mostra, no relatório, de onde e como a coleta
  foi feita. Isso protege você e a validade da prova.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Classificador de proxies**: teste uma lista e diga, para cada proxy, se
está vivo, quanto demora e se **vaza o seu IP**.

## 🔎 Inovação OSINT do dia

**A impressão digital do TLS (JA3/JA4).** Trocar o User-Agent já não basta: na conexão HTTPS, antes
de qualquer cabeçalho, o cliente manda uma mensagem (*ClientHello*) cujo formato varia de programa
para programa. Serviços como a Cloudflare calculam uma "assinatura" dessa mensagem (métodos **JA3**
e o mais novo **JA4**, da FoxIO) e reconhecem um script Python mesmo com UA de Chrome. Para o analista,
a lição é de OPSEC: o disfarce precisa ser coerente em todas as camadas. A biblioteca Python
`curl_cffi` faz pedidos com o mesmo TLS de navegadores reais (`impersonate="chrome"`). Use-a só em
coletas autorizadas, nunca para burlar bloqueios.

## 📚 Para ir além

- `urllib.request.ProxyHandler`: <https://docs.python.org/pt-br/3/library/urllib.request.html#urllib.request.ProxyHandler>
- ipify (API de IP público): <https://www.ipify.org/>
- httpbin (espelho de pedidos HTTP): <https://httpbin.org/>
- JA4+ (FoxIO): <https://github.com/FoxIO-LLC/ja4>
- curl_cffi: <https://github.com/lexiforest/curl_cffi>

## ✅ Checklist

- [ ] Li os três scripts originais e entendi por que os proxies do autor não funcionam mais
- [ ] Descobri o meu IP público com o script 01
- [ ] Vi o `Python-urllib/3.x` no pedido cru e troquei o UA
- [ ] Rodei o checklist de OPSEC e respondi o checklist humano
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
