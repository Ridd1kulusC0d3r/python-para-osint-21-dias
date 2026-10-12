### `br/04_ia_como_apoio.md` — IA como apoio, não como substituta

> *"Ferramenta pronta todo mundo tem; quem sabe escrever a própria ferramenta enxerga o que os outros
> não veem."* — Iara Campos

O autor do curso original diz isso com todas as letras: o ChatGPT **erra muito**. Em 2026 os
assistentes de IA estão melhores, mas continuam inventando função que não existe, parâmetro que
mudou de nome e "fato" que ninguém escreveu. Em investigação, um erro desses vai parar num relatório
assinado por **você**. A regra deste repositório: **a IA sugere, você verifica, você assina.**

#### 1. Para que a IA é boa (e para que não é)

| Use para | Não use para |
|---|---|
| Explicar um trecho de código que você não entendeu | Decidir se uma pessoa é suspeita |
| Revisar seu script e apontar bugs prováveis | Ser a fonte de um fato do caso ("o CNPJ X é da empresa Y") |
| Sugerir casos de teste (doctest, unittest) | Gerar dados "de exemplo" que parecem reais e entram no relatório |
| Traduzir uma mensagem de erro em português claro | Resumir evidência sem você ler a evidência |
| Propor nomes melhores para variáveis e funções | Escrever a conclusão do dossiê |

#### 2. Um modelo de prompt para revisão de código

Copie, preencha e cole. Repare: **nenhum dado do caso vai junto**, só o código e dados fictícios.

```text
Você é um revisor de código Python experiente. Revise o script abaixo.

Contexto: script de estudo, só biblioteca padrão, Python 3.9+, roda no Windows e no Linux.
Objetivo do script: <uma frase>

Quero, nesta ordem:
1. Bugs que fariam o resultado sair ERRADO (não só feio). Para cada um: linha, por quê, correção.
2. Casos de borda que não estão tratados (arquivo vazio, acento, campo faltando, internet fora).
3. Riscos de segurança (injeção de HTML/SQL, path traversal, dados pessoais em log).
4. No máximo 3 sugestões de legibilidade.

Regras: não reescreva o script inteiro. Se não tiver certeza de algo, diga "não tenho certeza".
Cite a documentação oficial do Python quando falar de uma função da biblioteca padrão.

<cole o código aqui>
```

#### 3. Checagem de alucinação: 5 perguntas antes de aceitar uma resposta

1. **A função existe?** Abra a documentação oficial (`docs.python.org`) ou rode
   `python -c "import modulo; help(modulo.funcao)"`. Função inventada é a alucinação mais comum.
2. **O parâmetro tem esse nome nesta versão?** Bibliotecas mudam (lembra do `txt=` → `text=` do
   fpdf2 no Dia 17 e do `duckduckgo_search` → `ddgs` no Dia 9?).
3. **Eu consigo testar?** Escreva um doctest ou um unittest (scripts 01 e 02) **antes** de colar a
   sugestão no seu código. Se a IA disse que "isso corrige o bug", o teste tem que passar.
4. **A explicação bate com o que eu vejo rodando?** Rode com um exemplo pequeno e imprima o resultado.
5. **Isso é um FATO sobre o mundo?** (uma lei, uma data, quem é dono de um CNPJ, se uma API existe).
   Então a IA **não é fonte**. Procure a fonte primária: o texto da lei, a Receita, a documentação.

#### 4. Nunca cole dado pessoal de caso real em IA pública

- O que você digita num assistente público pode ser **guardado, revisado por pessoas ou usado para
  treinar** o modelo, conforme os termos do serviço. Para a LGPD, isso é um compartilhamento de dado
  pessoal com terceiro, e você precisa de base legal e de finalidade para fazer isso.
- Em caso real, troque tudo antes de pedir ajuda: nomes por `Pessoa A`, CPFs por `000.000.000-00`,
  chaves PIX por um UUID inventado, domínio por `exemplo.example`. **A IA precisa da estrutura do
  dado, não do dado.**
- Prefira ferramentas aprovadas pela sua instituição (contratos corporativos que não usam os dados
  para treino) ou modelos que rodam **localmente**, no seu computador.
- **OPSEC:** perguntar a um serviço externo "quem é o dono da chave PIX tal" pode revelar que existe
  uma investigação. Pergunte sobre **código**, nunca sobre **alvos**.

#### 5. O teste final

Se amanhã a Delegada Rita perguntar "de onde saiu este número?", você precisa responder com um
arquivo, uma linha de código e um hash. Nunca com "a IA disse".
