# 🙏 Créditos

## O curso original

**Python for OSINT. 21-day course for beginners**
Autor: **cipher387**, conhecido como **Cyb_detective**

- Repositório: <https://github.com/cipher387/python-for-OSINT-21-days>
- PDF do curso: [baixar no repositório do autor](https://github.com/cipher387/python-for-OSINT-21-days/raw/main/Python%20for%20OSINT.%2021%20day%20course%20for%20beginners.pdf)
- Site: <https://cybdetective.com>
- Apoie o autor: <https://boosty.to/cyb_detective>
- Curso irmão: [Linux for OSINT. 21-day course for beginners](https://github.com/cipher387/linux-for-OSINT-21-day)
- Licença do código: MIT © 2023 Cyb_detective

O cipher387 decidiu distribuir o curso de graça para que pessoas de qualquer país e renda pudessem estudar.
Ele sugere uma doação simbólica para quem quiser se comprometer a ir até o fim. Este repositório
existe por causa desse gesto.

### O que veio do original

- A **estrutura** dos 21 dias e a ordem dos temas.
- Todo o código nas pastas `dia-XX-*/original/`, copiado **sem alteração de nenhuma linha**.
  Só foram acrescentados um cabeçalho de atribuição e comentários em pt-BR (`# 💬`).
  O teste semanal ([`ferramentas/smoke_test.py --originais`](ferramentas/smoke_test.py)) confere isso automaticamente.

### O que foi escrito aqui

- Todos os textos em pt-BR (escritos do zero; **não** são tradução do PDF).
- A camada Brasil (`br/`), a Operação Vitrine Fantasma (`caso/`), os desafios, os notebooks,
  as cartas, o site e as ferramentas.
- Arquivos `original/2026_*.py`: versões atualizadas de exemplos que pararam de funcionar,
  mantidas **ao lado** do original (veja [`ATUALIZACOES-2026.md`](ATUALIZACOES-2026.md)).

## Esta adaptação

**Deivison Lourenço** · [Ridd1kulusC0d3r](https://github.com/Ridd1kulusC0d3r)

## Fontes e serviços públicos usados na camada Brasil

| Serviço | Mantido por | Usado nos dias |
|---|---|---|
| RDAP e WHOIS do `.br` | [registro.br / NIC.br](https://registro.br) | 15 |
| Bootstrap RDAP | [IANA](https://data.iana.org/rdap/) | 15 |
| [BrasilAPI](https://brasilapi.com.br) | comunidade (código aberto) | 3, 5, 6 |
| [ViaCEP](https://viacep.com.br) | ViaCEP | 5 |
| [API de Localidades](https://servicodados.ibge.gov.br/api/docs/localidades) | IBGE | 7 |
| [Querido Diário](https://queridodiario.ok.org.br) | Open Knowledge Brasil | 9 |
| [Wayback Machine (CDX)](https://web.archive.org) | Internet Archive | 19 |

Obrigado a todas essas equipes por manterem dados públicos acessíveis.
