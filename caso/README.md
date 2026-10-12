# 🕵️ Operação Vitrine Fantasma — a bíblia do caso

> Toda a narrativa deste repositório é **ficção**. Pessoas, empresas, CPFs, CNPJs,
> telefones, chaves PIX e o domínio `megaoferta-brasil.example` foram **inventados**
> e gerados por [`gerar_dados.py`](gerar_dados.py) com semente fixa (2026).
> Qualquer semelhança com pessoas reais é coincidência. Os CNPJs da história têm
> dígito verificador **errado de propósito**, para que nunca coincidam com uma empresa real.

## O cenário

Belo Horizonte, novembro de 2025. Em plena Black Friday, o **Núcleo de Fontes Abertas (NFA)**,
uma unidade fictícia de apoio a investigações, recebe **37 denúncias** sobre a loja virtual
**MegaOferta Brasil**: iPhones a R$ 1.999, PlayStation 5 a R$ 1.899, pagamento **só no PIX**.
As vítimas pagaram e o site desapareceu.

Você é a pessoa recém-chegada ao NFA. Sua mentora é a **Iara Campos**, analista sênior de OSINT,
que tem uma regra: *"ferramenta pronta todo mundo tem; quem sabe escrever a própria ferramenta
enxerga o que os outros não veem"*. Durante 21 dias você vai aprender Python resolvendo o caso.

## Elenco

| Personagem | Papel |
|---|---|
| **Você** | Analista recém-chegado(a) ao NFA |
| **Iara Campos** | Mentora, analista sênior de OSINT |
| **Delegada Rita Assunção** | Quem pediu o apoio do NFA e vai receber o dossiê |
| **"Kau" / kau.ofertas** | Vendedor da loja; nome que aparece nos registros: *Kauã Teixeira Brandão* |
| Jéssica Prado Lima, Wellington Arruda Paz, M. R. Brandão Comércio ME | Titulares das contas que receberam os PIX ("laranjas") |
| 37 vítimas | Pessoas de várias cidades de MG (nomes gerados aleatoriamente) |

## Os 21 capítulos

| Dia | Capítulo | O que acontece no caso |
|---|---|---|
| 0 | **O recrutamento** | Iara monta seu ambiente (Colab, Codespaces ou local) |
| 1 | **O primeiro alerta** | Seu primeiro script imprime o briefing do caso |
| 2 | **Triagem** | Variáveis, condições e laços para validar os CPFs das denúncias |
| 3 | **Ferramenta de campo** | Rodar ferramentas de linha de comando contra o apelido do vendedor |
| 4 | **Os depoimentos** | Ler e anotar os depoimentos das vítimas em arquivos de texto |
| 5 | **O endereço da loja** | Consultar o CEP do rodapé via API: é uma avenida movimentada no centro, não um depósito |
| 6 | **O CNPJ do rodapé** | Ler JSON de APIs; o CNPJ da loja não passa nem na validação |
| 7 | **A planilha das vítimas** | Consolidar denúncias em CSV e padronizar cidades com a base do IBGE |
| 8 | **O dump do painel** | Um informante entrega um `.sql` do painel da loja: quem recebeu o dinheiro? |
| 9 | **Rastros na busca** | Automatizar buscas na web e em Diários Oficiais (Querido Diário) |
| 10 | **A vitrine congelada** | Raspar a cópia salva do site falso: produtos, preços, chave PIX, comentários no HTML |
| 11 | **A conversa** | Expressões regulares para extrair CPFs, CNPJs, telefones, e-mails e chaves PIX |
| 12 | **Disfarce digital** | Proxies, User-Agent e OPSEC: não deixar rastro do NFA |
| 13 | **O mapa das vítimas** | Listas: ordenar cidades com acento, remover duplicatas |
| 14 | **A sala de evidências** | Varrer pastas, achar padrões e gerar hash SHA-256 (cadeia de custódia) |
| 15 | **Quem registrou o domínio?** | WHOIS, RDAP e DNS do domínio da loja |
| 16 | **Os muitos nomes de Kau** | Strings e `map`: normalizar nomes e gerar variantes de username |
| 17 | **O relatório preliminar** | Gerar documentos (DOCX/PDF/XLSX e HTML/Markdown só com stdlib) |
| 18 | **Onde estão as vítimas** | Gráficos e mapas das denúncias |
| 19 | **O site que sumiu** | Wayback Machine e datas: linha do tempo do golpe e o efeito Black Friday |
| 20 | **O painel do caso** | Um web app para a equipe consultar o caso |
| 21 | **O dossiê** | Ferramentas de apoio ao código, revisão final e entrega à Delegada Rita |

## Arquivos de dados (`caso/dados/`)

| Arquivo | Usado nos dias |
|---|---|
| `denuncias.csv` | 2, 7, 13, 16, 17, 18, 19, 20 |
| `depoimentos/*.txt` | 4, 14 |
| `conversa_whatsapp.txt` | 11, 14 |
| `vitrine_megaoferta.html` | 10, 14 |
| `painel_dump.sql` | 8 |
| `rdap_megaoferta.json`, `whois_megaoferta.txt` | 15 |
| `wayback_cdx_megaoferta.json` | 19 |
| `ficha_do_caso.json` | gabarito para quem cria exercícios (spoiler!) |

Para regenerar: `python caso/gerar_dados.py`.
