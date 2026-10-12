# 🏆 Desafio S — Dia 14: Triagem do pendrive apreendido

**Carta 56 · Rank S**

## A missão

Chega ao NFA a cópia de um pendrive (fictício) encontrado com um dos laranjas:
[`dados/pendrive_apreendido/`](dados/pendrive_apreendido). Antes de abrir qualquer coisa, a Iara quer
uma triagem automática que responda três perguntas:

1. **Algum arquivo mente sobre o que é?** (um `.txt` que na verdade é imagem, um `.pdf` que é ZIP…)
2. **Há duplicatas?** (mesmo conteúdo com nomes diferentes)
3. **O que já temos?** (arquivos idênticos a evidências de `caso/dados`)

Escreva um script que, para cada arquivo do pendrive (com subpastas):

- calcule o **SHA-256** em blocos;
- leia os **primeiros bytes** e descubra o tipo real pelo "número mágico" (PNG começa com
  `\x89PNG`, PDF com `%PDF-`, ZIP com `PK\x03\x04`…);
- compare o tipo real com a extensão e marque 🎭 se não baterem;
- marque ♊ as duplicatas e 📁 o que já existe em `caso/dados`;
- grave `saidas/triagem_pendrive.csv` (`;`, `utf-8-sig`).

## Critérios de rank S

- [ ] Só biblioteca padrão (`hashlib`, `pathlib`, `csv`, `collections`)
- [ ] Lê em modo binário (`"rb"`) e em blocos
- [ ] Não altera nenhum arquivo do pendrive
- [ ] Acha as 2 extensões falsas, a duplicata e os 2 arquivos já conhecidos
- [ ] Diz quantos arquivos são **realmente novos** para analisar

## Dica

Monte um dicionário `hash → caminho` com todos os arquivos de `caso/dados` **antes** de olhar o
pendrive. Depois, "já conhecido?" vira só `hash in conhecidos`.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `for pedaco in iter(lambda: f.read(65536), b""):` lê o arquivo em blocos até o fim, em uma linha.
- `PK\x03\x04` não é só `.zip`: `.docx`, `.xlsx` e `.apk` também são ZIP por dentro. Por isso há um
  dicionário de extensões compatíveis.
- `senhas.txt` é uma imagem PNG idêntica a `comprovante_pix.png`; `nota_fiscal.pdf` é um ZIP;
  `lista_mercado.txt` é a conversa do WhatsApp que já temos, e `site_backup.htm` é a vitrine.
- Resultado: 6 arquivos, só 3 realmente novos. A triagem economiza tempo e evita abrir um executável
  disfarçado.

</details>
