# ⚖️ Ética, LGPD e OPSEC para OSINT no Brasil

> Leia antes do Dia 1. Isto não é aconselhamento jurídico; é o mínimo que todo analista de fontes
> abertas precisa ter em mente. Em caso de dúvida concreta, consulte um advogado.

## 1. OSINT é informação pública, com finalidade

OSINT (*Open Source Intelligence*) é inteligência produzida a partir de **fontes abertas**: o que está
publicado, acessível sem invasão, sem senha alheia e sem enganar sistemas. "Estar na internet" não é o
mesmo que "poder ser usado para qualquer coisa".

Antes de coletar, responda:

1. **Para quê?** Qual é a finalidade legítima (investigação autorizada, due diligence, pesquisa, defesa)?
2. **Do quê eu preciso?** Colete o mínimo necessário para essa finalidade.
3. **Como vou guardar?** Onde ficam os dados, quem acessa, por quanto tempo.
4. **Como vou provar de onde veio?** Fonte, data, hora e hash de cada evidência (Dia 14).

## 2. LGPD (Lei 13.709/2018) em uma página

- **Dado pessoal** é qualquer informação que identifique ou possa identificar uma pessoa: nome, CPF,
  telefone, e-mail, foto, IP, placa de carro, username.
- Dado pessoal **público** continua protegido. O tratamento precisa respeitar a **finalidade**, a
  **boa-fé** e o **interesse público** que justificaram a sua publicação (art. 7º, §§ 3º e 4º).
- Princípios que valem para qualquer coleta: finalidade, adequação, **necessidade** (o mínimo),
  segurança e prevenção (art. 6º).
- Dados **sensíveis** (saúde, religião, orientação sexual, biometria, opinião política…) exigem cuidado redobrado.
- Investigações criminais têm regras próprias (art. 4º, III), mas isso **não** autoriza qualquer pessoa a
  "investigar por conta própria" usando dados alheios.

## 3. Linhas que não se cruzam

| ❌ Não faça | Por quê |
|---|---|
| Acessar sistema, conta ou painel sem autorização, mesmo com senha "achada" | Invasão de dispositivo informático (CP, art. 154-A) |
| Baixar, comprar, compartilhar ou "consultar" vazamentos de dados reais | Tratamento ilícito de dados pessoais; pode configurar outros crimes |
| Burlar captcha, login ou bloqueio técnico para raspar dados | Viola termos de uso e pode ser acesso indevido |
| Criar perfil falso para enganar uma pessoa específica | Pode configurar falsa identidade e outros ilícitos |
| Expor publicamente dados de alguém ("doxxing") | Viola a LGPD e pode gerar responsabilidade civil e criminal |
| Usar o curso contra ex-companheiros, desafetos ou desconhecidos | Perseguição é crime (CP, art. 147-A) |

## 4. Boas práticas do curso

- **Alvos ao vivo:** só institucionais e públicos (`registro.br`, `gov.br`, IBGE, uma estatal conhecida).
- **Dados do caso:** só os de [`caso/dados/`](caso/dados/), 100% fictícios.
- **Ritmo:** respeite limites de requisição das APIs; use pausas (`time.sleep`) em laços.
- **robots.txt e termos de uso:** leia antes de raspar (Dia 10).
- **Identifique-se:** nos scripts usamos um User-Agent honesto (`python-para-osint-21-dias/estudo`).
- **IA:** nunca cole dados pessoais de um caso real em uma IA pública (Dia 21).

## 5. OPSEC: proteger a investigação e a si mesmo

- Acessar o site de um suspeito deixa seu IP nos logs dele. Prefira fontes indiretas (RDAP, Wayback, buscadores).
- Proxies e VPNs gratuitos e desconhecidos podem **ler seu tráfego** (Dia 12).
- Separe o ambiente de investigação da sua vida pessoal (navegador, contas, máquina).
- Não clique em links de golpistas. Analise cópias salvas (como a vitrine do Dia 10).

## 6. Cadeia de custódia

Se o material puder virar prova, ele precisa ter história: quem coletou, quando, como, e que não foi
alterado. O Código de Processo Penal trata da cadeia de custódia nos **arts. 158-A a 158-F** (incluídos pela
Lei 13.964/2019). No Dia 14 você gera um manifesto com **hash SHA-256** de cada arquivo.

## Referências

- [Lei 13.709/2018 (LGPD)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Lei 12.965/2014 (Marco Civil da Internet)](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm)
- [Código Penal](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm) (arts. 147-A e 154-A)
- [Código de Processo Penal](https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm) (arts. 158-A a 158-F)
- [ANPD — Autoridade Nacional de Proteção de Dados](https://www.gov.br/anpd/pt-br)
